---
name: ocr-scanner-image
version: 1.0.0
description: Perform OCR on image files (jpg, png, bmp, gif, tiff) using the system's `tesseract` binary and return extracted plain text.
---

# OCR‑Scanner‑Image (funktionierender Skill)

## Überblick
Dieser Skill nutzt das lokale **Tesseract‑OCR**‑Programm, um Text aus gängigen Bildformaten zu extrahieren. Er ist sofort einsetzbar, weil `tesseract` bereits auf dem System installiert ist.

## Verwendung
```bash
# Aufruf über das Skill‑Skript (empfohlen)
~/.openclaw/workspace/skills/ocr-scanner-image/scripts/ocr.sh <Pfad‑zur‑Bilddatei>
```
Beispiel:
```bash
~/.openclaw/workspace/skills/ocr-scanner-image/scripts/ocr.sh /root/.openclaw/media/inbound/916f6187-cc22-4c62-bcfc-7b72198c8a10.png
```
Der erkannte Text wird auf **STDOUT** ausgegeben.

## Optionen
- Der Aufruf nutzt `-l eng`, um die englische Sprachdatei zu erzwingen.  Für andere Sprachen kannst du das Flag anpassen, z. B. `-l deu` für Deutsch.
- Wenn du die Sprache automatisch erkennen lassen möchtest, entferne das `-l`‑Flag.

## Integration in OpenClaw (optional)
Falls du den Skill später über das OpenClaw‑CLI ausführen willst, kannst du einen Alias in deiner `~/.bashrc` (oder `~/.zshrc`) hinzufügen:
```bash
alias ocr-image='~/.openclaw/workspace/skills/ocr-scanner-image/scripts/ocr.sh'
```
Dann kannst du einfach `ocr-image <datei>` tippen.

## Hinweis
Der ursprüngliche Platzhalter‑Skill war nicht funktionsfähig.  Durch das Hinzufügen dieses Bash‑Wrappers wird er zu einem echten OCR‑Tool, das sofort einsatzbereit ist.
