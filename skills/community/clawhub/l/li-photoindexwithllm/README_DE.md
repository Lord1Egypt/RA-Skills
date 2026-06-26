# 📸 PhotoIndexWithLLM — Deutsch

## Übersicht

PhotoIndexWithLLM ist ein intelligentes System zur Foto-Indizierung, -Analyse und -Suche, das auf Vision-Language (VL) Großmodellen basiert.

## Schnellstart

```bash
# Abhängigkeiten installieren
pip install requests

# Fotos scannen
python skill.py scan --dir /home/user/Photos

# Fotos suchen
python skill.py search "Strand Sonnenuntergang"

# JSON-Ausgabe
python skill.py search "Strand" --format json
```

## Unterstützte Plattformen

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## Unterstützte Bildformate (17 Typen)

| Typ | Formate |
|-----|---------|
| Allgemein | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon DSLR | `.cr2` |
| Nikon DSLR | `.nef` |
| Sony DSLR | `.arw` |
| Andere RAW | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## Datenschutz

- Standardmäßig nur lokaler Modus
- Fotos verlassen niemals Ihr Gerät
- Remote-Übertragung erfordert Benutzerbestätigung

## Vollständige Befehle

```bash
# Fotos scannen
python skill.py scan --dir /home/user/Photos

# Fotos suchen
python skill.py search "Strand Sonnenuntergang"

# Scannen und Suchen
python skill.py scan_and_search --dir /home/user/Photos --query "Strand"

# Annotieren
python skill.py annotate --photo /photos/img001.jpg --type person --name Hans

# Modell trainieren
python skill.py train

# Statistiken anzeigen
python skill.py stats

# Verbindung testen
python skill.py test
```

## Kontakt

**Autor**: Beijing Lao Li (beijingLL)
**ClawHub ID**: 43622283
