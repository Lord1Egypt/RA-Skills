# Jarvis Browser Setup Skill

## Installation

```bash
# Skill in OpenClaw laden
openclaw skill install jarvis-browser-setup.skill
```

## Verwendung

```bash
# Setup für neuen Nutzer starten
python3 ~/.openclaw/workspace/skills/jarvis-browser-setup/scripts/setup.py
```

## Was es macht

1. 🔑 Generiert eindeutigen Auth Token (48 Zeichen, kryptografisch sicher)
2. 🌐 Ermittelt Server IP-Adresse
3. 📦 Kopiert Server + Extension Files
4. ⚙️  Konfiguriert alles mit neuem Token
5. 📝 Erstellt README mit Anleitung

## Ausgabe

```
jarvis-browser-setup-20260322/
├── config.json          # Deine Konfiguration (Token, IP)
├── server/              # Python WebSocket Server
├── extension/           # Chrome Extension (vorkonfiguriert)
└── README.md            # Setup-Anleitung
```

## Wichtig

- Jeder Nutzer bekommt eigenen **einzigartigen Token**
- Token nie teilen!
- Server läuft auf Port 8765
- Extension zeigt grünes "ON" wenn verbunden

## Beispiel-Token

```
XsJ3N-mAtusZ+WSPr0Ca!ExnVdQ8UuGd8J9PCwo9l8bmX3ACylw6Nv
```

Erstellt: 2026-03-22
