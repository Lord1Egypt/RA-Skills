# 📸 PhotoIndexWithLLM — Español

## Descripción General

PhotoIndexWithLLM es un sistema inteligente de indexación, análisis y búsqueda de fotos impulsado por grandes modelos de Visión-Lenguaje (VL).

## Inicio Rápido

```bash
# Instalar dependencias
pip install requests

# Escanear fotos
python skill.py scan --dir /home/user/Photos

# Buscar fotos
python skill.py search "playa atardecer"

# Salida JSON
python skill.py search "playa" --format json
```

## Plataformas Soportadas

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## Formatos de Imagen Soportados (17 tipos)

| Tipo | Formatos |
|------|----------|
| Comunes | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon DSLR | `.cr2` |
| Nikon DSLR | `.nef` |
| Sony DSLR | `.arw` |
| Otros RAW | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## Protección de Privacidad

- Modo local únicamente por defecto
- Las fotos nunca salen de su equipo
- La transferencia remota requiere consentimiento del usuario

## Comandos Completos

```bash
# Escanear fotos
python skill.py scan --dir /home/user/Photos

# Buscar fotos
python skill.py search "playa atardecer"

# Escanear y buscar
python skill.py scan_and_search --dir /home/user/Photos --query "playa"

# Anotar
python skill.py annotate --photo /photos/img001.jpg --type person --name Carlos

# Entrenar modelo
python skill.py train

# Ver estadísticas
python skill.py stats

# Probar conexión
python skill.py test
```

## Contacto

**Autor**: Beijing Lao Li (beijingLL)
**ClawHub ID**: 43622283
