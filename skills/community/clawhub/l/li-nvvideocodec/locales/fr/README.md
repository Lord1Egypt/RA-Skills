# li_nvvideocodec - Compresseur Vidéo NVIDIA AV1

**Version**: 1.0.1  
**Langue**: Français (fr)

## 📋 Aperçu

Un outil de compression vidéo par lots utilisant l'encodage AV1 accéléré par le GPU NVIDIA. Compressez efficacement vos vidéos avec une validation intelligente et plusieurs profils de compression.

## ✨ Fonctionnalités

- 🎯 **Validation Intelligente** - Test automatique de l'efficacité
- 📊 **Trois Profils** - Conservateur/Équilibré/Aggressif
- 🖥️ **Multi-Plateforme** - Windows & Ubuntu Linux
- 📈 **Progression en Temps Réel** - Affichage en direct
- 🔒 **Sécurisé** - Fichiers originaux protégés

## 🚀 Démarrage Rapide

```bash
# Mode interactif
python scripts/compress_videos.py

# Mode ligne de commande
python scripts/compress_videos.py -i "/path/to/videos" -p B --no-confirm

# Mode test
python scripts/compress_videos.py -i "/path/to/videos" -p B --test
```

## 📊 Profils de Compression

| Profil | Résolution | CRF | FPS | Audio | Économie |
|--------|-----------|-----|-----|-------|----------|
| **A** | Original | 23 | Original | 128k | 40-60% |
| **B** ⭐ | 1280x720 | 24 | 24 | 96k | 65-75% |
| **C** | 1280x720 | 28 | 15 | 64k | 78-85% |

## ⚙️ Prérequis

- **FFmpeg** avec support av1_nvenc
- **NVIDIA GPU** (GTX 1650+)
- **Python 3.7+**

## 🤖 Utilisation Agent

```bash
# Vérifier l'environnement
python agent_interface.py --action check

# Analyser les vidéos
python agent_interface.py --action analyze -i "/path/to/videos"

# Compresser
python agent_interface.py --action compress -i "/path/to/videos" -p B
```
