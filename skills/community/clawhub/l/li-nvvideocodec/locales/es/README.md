# li_nvvideocodec - Compresor de Video NVIDIA AV1

**Versión**: 1.0.1  
**Idioma**: Español (es)

## 📋 Descripción

Una herramienta de compresión de video por lotes que utiliza codificación AV1 acelerada por GPU NVIDIA. Comprima videos eficientemente con validación inteligente y múltiples perfiles de compresión.

## ✨ Características

- 🎯 **Validación Inteligente** - Prueba automática de efectividad
- 📊 **Tres Perfiles** - Conservador/Equilibrado/Agresivo
- 🖥️ **Multiplataforma** - Windows & Ubuntu Linux
- 📈 **Progreso en Tiempo Real** - Visualización en vivo
- 🔒 **Seguro** - Archivos originales protegidos

## 🚀 Inicio Rápido

```bash
# Modo interactivo
python scripts/compress_videos.py

# Modo línea de comandos
python scripts/compress_videos.py -i "/path/to/videos" -p B --no-confirm

# Modo prueba
python scripts/compress_videos.py -i "/path/to/videos" -p B --test
```

## 📊 Perfiles de Compresión

| Perfil | Resolución | CRF | FPS | Audio | Ahorro |
|--------|-----------|-----|-----|-------|--------|
| **A** | Original | 23 | Original | 128k | 40-60% |
| **B** ⭐ | 1280x720 | 24 | 24 | 96k | 65-75% |
| **C** | 1280x720 | 28 | 15 | 64k | 78-85% |

## ⚙️ Requisitos

- **FFmpeg** con soporte av1_nvenc
- **NVIDIA GPU** (GTX 1650+)
- **Python 3.7+**

## 🤖 Uso con Agent

```bash
# Verificar entorno
python agent_interface.py --action check

# Analizar videos
python agent_interface.py --action analyze -i "/path/to/videos"

# Comprimir
python agent_interface.py --action compress -i "/path/to/videos" -p B
```
