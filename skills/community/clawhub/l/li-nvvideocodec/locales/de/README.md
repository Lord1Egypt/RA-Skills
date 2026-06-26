# li_nvvideocodec - NVIDIA AV1 Videokomprimierung

**Version**: 1.0.1  
**Sprache**: Deutsch (de)

## 📋 Übersicht

Ein Batch-Videokomprimierungstool mit NVIDIA GPU-hardwarebeschleunigter AV1-Codierung. Komprimieren Sie Videos effizient mit intelligenter Validierung und mehreren Komprimierungsprofilen.

## ✨ Funktionen

- 🎯 **Intelligente Validierung** - Automatischer Test der Komprimierung
- 📊 **Drei Profile** - Konservativ/Ausgewogen/Aggressiv
- 🖥️ **Cross-Platform** - Windows & Ubuntu Linux
- 📈 **Echtzeit-Fortschritt** - Live-Fortschrittsanzeige
- 🔒 **Sicher** - Originaldateien geschützt

## 🚀 Schnellstart

```bash
# Interaktiver Modus
python scripts/compress_videos.py

# Befehlszeilenmodus
python scripts/compress_videos.py -i "/path/to/videos" -p B --no-confirm

# Testmodus
python scripts/compress_videos.py -i "/path/to/videos" -p B --test
```

## 📊 Komprimierungsprofile

| Profil | Auflösung | CRF | FPS | Audio | Einsparung |
|--------|----------|-----|-----|-------|-----------|
| **A** | Original | 23 | Original | 128k | 40-60% |
| **B** ⭐ | 1280x720 | 24 | 24 | 96k | 65-75% |
| **C** | 1280x720 | 28 | 15 | 64k | 78-85% |

## ⚙️ Anforderungen

- **FFmpeg** mit av1_nvenc-Unterstützung
- **NVIDIA GPU** (GTX 1650+)
- **Python 3.7+**

## 🤖 Agent-Nutzung

```bash
# Umgebung prüfen
python agent_interface.py --action check

# Videos analysieren
python agent_interface.py --action analyze -i "/path/to/videos"

# Komprimieren
python agent_interface.py --action compress -i "/path/to/videos" -p B
```
