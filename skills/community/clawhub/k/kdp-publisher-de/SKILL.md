---
name: kdp-publisher
description: Baut KDP-fertige PDFs aus Markdown-Kapiteln im professionellen OpenClaw-Buchstil (Inter-Font, 6x9 inch, Typst-basiert). Verwendung: "Bau mir ein PDF aus [Dateiname]" oder "Kompiliere Kapitel 3".
---

# kdp-publisher — KDP PDF Builder

Dieser Skill wandelt Markdown-Kapitel in KDP-fertige PDFs um — im Buchstil von "OpenClaw – Agentic Authorship".

## Voraussetzungen prüfen

```bash
# Python-Abhängigkeiten installieren (einmalig):
pip install requests qrcode

# Skill-Verzeichnis:
ls $OPENCLAW_WORKSPACE/skills/kdp-publisher/scripts/
```

## Verwendung

**Ein Kapitel:**
```bash
cd $OPENCLAW_WORKSPACE/skills/kdp-publisher/scripts
python3 build-book.py --chapter /pfad/zu/kapitel.md /pfad/output/kapitel.pdf
```

**Ganzes Buch (alle Kapitel in der konfigurierten Reihenfolge):**
```bash
cd $OPENCLAW_WORKSPACE/skills/kdp-publisher/scripts
python3 build-book.py /pfad/output/buch.pdf
```

## Was passiert im Hintergrund

1. `build-book.py` orchestriert den Build
2. `md2typ.py` konvertiert Markdown → Typst
3. `compile.py` generiert QR-Codes + sendet an TypeTex API → PDF

## Markdown-Format

| Element | Syntax |
|---|---|
| Kapitelüberschrift | `# Titel` |
| Abschnitt | `## Titel` |
| Tipp-Box | `> **TIPP:** Text` |
| Warn-Box | `> **WARNUNG:** Text` |
| Hinweis-Box | `> **HINWEIS:** Text` |
| Erfolg-Box | `> **ERFOLG:** Text` |
| Zitat | `> Text` |
| QR-Code | `[QR-CODE: ID – Label]` |
| QR mit Hinweis | `[QR-CODE: ID – Label \| Hinweistext]` |

## QR-Codes konfigurieren

QR-Code-URLs werden aus einer `links.json` geladen. Standardpfad:
```
$OPENCLAW_WORKSPACE/links.json
```

Format:
```json
{
  "eigene_projekte": { "DASHBOARD_URL": "https://deine-domain.de" },
  "qr_codes": {
    "MEIN-QR": {
      "target": "{{DASHBOARD_URL}}/seite",
      "print_url": "deine-domain.de/seite"
    }
  }
}
```

## Häufige Probleme

- **QR nicht gefunden:** ID in `links.json` prüfen, kein `_`-Präfix
- **API-Timeout:** Kapitel einzeln kompilieren statt ganzes Buch
- **Font fehlt:** TypeTex API stellt Inter und Liberation Mono bereit — kein lokales Install nötig
