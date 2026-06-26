# 📸 PhotoIndexWithLLM — Français

## Aperçu

PhotoIndexWithLLM est un système intelligent d'indexation, d'analyse et de recherche de photos alimenté par des grands modèles Vision-Language (VL).

## Démarrage Rapide

```bash
# Installer les dépendances
pip install requests

# Analyser les photos
python skill.py scan --dir /home/user/Photos

# Rechercher des photos
python skill.py search "plage coucher de soleil"

# Sortie JSON
python skill.py search "plage" --format json
```

## Plateformes Supportées

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## Formats d'Image Supportés (17 types)

| Type | Formats |
|------|---------|
| Courants | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon DSLR | `.cr2` |
| Nikon DSLR | `.nef` |
| Sony DSLR | `.arw` |
| Autres RAW | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## Protection de la Vie Privée

- Mode local uniquement par défaut
- Les photos ne quittent jamais votre appareil
- Le transfert vers un modèle distant nécessite le consentement de l'utilisateur

## Commandes Complètes

```bash
# Analyser les photos
python skill.py scan --dir /home/user/Photos

# Rechercher des photos
python skill.py search "plage coucher de soleil"

# Analyser et rechercher
python skill.py scan_and_search --dir /home/user/Photos --query "plage"

# Annoter
python skill.py annotate --photo /photos/img001.jpg --type person --name Jean

# Entraîner le modèle
python skill.py train

# Voir les statistiques
python skill.py stats

# Tester la connexion
python skill.py test
```

## Contact

**Auteur**: Beijing Lao Li (beijingLL)
**ClawHub ID**: 43622283
