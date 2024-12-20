import streamlit as st
from PIL import Image
import io
import os

def convertir_formato(imagen, formato):
    """Convierte una imagen a un formato específico y optimiza la compresión."""
    try:
        buffer = io.BytesIO()
        if formato.lower() == "jpg" or formato.lower() == "jpeg":
            # Ajusta la calidad JPEG (valores entre 0 y 95, siendo 95 la mayor calidad)
            imagen_sin_transparencia = imagen.convert("RGB") if imagen.mode == "RGBA" else imagen
            imagen_sin_transparencia.save(buffer, format="JPEG", quality=70, optimize=True, progressive=True)
        elif formato.lower() == "png":
            # Optimización PNG
            imagen.save(buffer, format="PNG", optimize=True, compress_level=9)
        elif formato.lower() == "webp":
             # Optimizacion Webp
             imagen.save(buffer, format="WEBP", quality = 70, method = 6)
        elif formato.lower() == "gif":
             imagen.save(buffer, format="GIF", optimize=True)
        else:
             imagen.save(buffer, format=formato.upper())
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"Error al convertir a formato {formato}: {e}")
        return None

def redimensionar_imagen(imagen, ancho, alto, mantener_ratio):
    """Redimensiona una imagen a un ancho y alto específicos, manteniendo el ratio si se solicita."""
    try:
        if mantener_ratio:
           imagen.thumbnail((ancho, alto))  # thumbnail mantiene el ratio
           return imagen
        else:
           imagen_redimensionada = imagen.resize((ancho, alto))
           return imagen_redimensionada
    except Exception as e:
        st.error(f"Error al redimensionar la imagen: {e}")
        return imagen

def main():
    st.title("Convertidor y Redimensionador de Imágenes")

    uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Imagen Original", use_container_width=True)
            
            st.subheader("Opciones de Conversión")
            
            formato_seleccionado = st.selectbox("Selecciona el formato de salida",
                                             options=["png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"],
                                              index=0 )

            convertir = st.checkbox("Convertir formato")
            
            buffer_convertido = None
            image_convertida = None

            if convertir:
              buffer_convertido = convertir_formato(image, formato_seleccionado)
              if buffer_convertido:
                  st.success(f"Imagen convertida a formato {formato_seleccionado.upper()}")
                  image_convertida = Image.open(buffer_convertido)
                  st.image(image_convertida, caption="Imagen convertida", use_container_width=True)


            st.subheader("Descarga Inicial")
            
            if convertir and buffer_convertido:
                buffer_descarga = io.BytesIO()
                image_convertida.save(buffer_descarga, format = formato_seleccionado.upper() if formato_seleccionado.lower() != "gif" else "GIF", save_all = True, optimize=True)
                buffer_descarga.seek(0)
                st.download_button(
                    label="Descargar Imagen Convertida",
                    data=buffer_descarga,
                    file_name=f"imagen_convertida.{formato_seleccionado.lower()}",
                    mime=f"image/{formato_seleccionado.lower()}"
                )

            else:
                buffer_descarga = io.BytesIO()
                formato_default = "JPEG" if image.mode != "RGBA" and image.mode != "LA" else "PNG"
                image.save(buffer_descarga, format = image.format if image.format else formato_default , optimize = True, progressive = True, quality=70 if formato_default == "JPEG" else None)
                buffer_descarga.seek(0)
                st.download_button(
                    label="Descargar Imagen Original",
                    data=buffer_descarga,
                    file_name=f"imagen_original.{image.format.lower() if image.format else formato_default.lower()}",
                    mime=f"image/{image.format.lower() if image.format else formato_default.lower()}"
                )


            st.subheader("Opciones de Redimensionamiento")
            ancho = st.number_input("Ancho:", min_value=1, value=image.width)
            alto = st.number_input("Alto:", min_value=1, value=image.height)
            mantener_ratio = st.checkbox("Mantener relación de aspecto")
            redimensionar = st.checkbox("Redimensionar imagen")
            
            if redimensionar:
              if convertir and image_convertida is not None:
                  image_redimensionada = redimensionar_imagen(image_convertida, int(ancho), int(alto), mantener_ratio)
              else:
                  image_redimensionada = redimensionar_imagen(image, int(ancho), int(alto), mantener_ratio)
              
              st.success(f"Imagen redimensionada a {ancho}x{alto}")
              st.image(image_redimensionada, caption="Imagen Redimensionada", use_container_width=True)


              st.subheader("Descarga de Imagen Redimensionada")
              buffer_descarga_redimensionada = io.BytesIO()
              
              formato_redimensionada = image_redimensionada.format if image_redimensionada.format else "PNG"
              
              image_redimensionada.save(buffer_descarga_redimensionada, format=formato_redimensionada if formato_redimensionada.lower() != "gif" else "GIF",  save_all=True, optimize=True)
              buffer_descarga_redimensionada.seek(0)
              st.download_button(
                label="Descargar Imagen Redimensionada",
                data=buffer_descarga_redimensionada,
                file_name=f"imagen_redimensionada.{formato_redimensionada.lower()}",
                mime=f"image/{formato_redimensionada.lower()}"
              )

        except Exception as e:
            st.error(f"Error al cargar la imagen: {e}")

if __name__ == "__main__":
    main()
