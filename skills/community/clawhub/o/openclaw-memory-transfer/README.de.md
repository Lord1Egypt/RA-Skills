# openclaw-memory-transfer

> **Reibungslose Gedächtnismigration für OpenClaw.** Bringen Sie Ihre Erinnerungen von ChatGPT, Claude, Gemini, Copilot und mehr mit — in unter 10 Minuten.

[![Powered by MyClaw.ai](https://img.shields.io/badge/Powered%20by-MyClaw.ai-blue)](https://myclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[English](README.md) | [中文](README.zh-CN.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Italiano](README.it.md) | [Español](README.es.md)

---

Sie haben Monate (oder Jahre) mit ChatGPT verbracht. Es kennt Ihren Schreibstil, Ihre Projekte, Ihre Vorlieben. Beim Wechsel zu OpenClaw sollte nichts davon bei Null anfangen.

**Memory Transfer** extrahiert alles, was Ihr alter KI-Assistent über Sie weiß, bereinigt die Daten und importiert sie in OpenClaws Gedächtnissystem.

## Verwendung

Sagen Sie Ihrem OpenClaw-Agent:

```
Ich komme von ChatGPT
```

## Unterstützte Quellen

| Quelle | Methode | Ihre Aktion |
|--------|---------|-------------|
| **ChatGPT** | ZIP-Datenexport | Export in Einstellungen klicken, ZIP hochladen |
| **Claude.ai** | Prompt-geführt | Einen Prompt kopieren, Ergebnis einfügen |
| **Gemini** | Prompt-geführt | Einen Prompt kopieren, Ergebnis einfügen |
| **Copilot** | Prompt-geführt | Einen Prompt kopieren, Ergebnis einfügen |
| **Claude Code** | Auto-Scan | Nichts — automatisch |
| **Cursor** | Auto-Scan | Nichts — automatisch |
| **Windsurf** | Auto-Scan | Nichts — automatisch |

## Was wird migriert

| Kategorie | Ziel | Beispiele |
|-----------|------|----------|
| Identität | `USER.md` | Name, Beruf, Sprache, Zeitzone |
| Kommunikationsstil | `USER.md` | Schreibton, Formatvorlieben |
| Wissen | `MEMORY.md` | Projekte, Fachkenntnisse, Erkenntnisse |
| Verhaltensmuster | `MEMORY.md` | Workflows, Gewohnheiten, Korrekturen |
| Tool-Präferenzen | `TOOLS.md` | Tech-Stack, Plattformen |

## Installation

```bash
clawhub install openclaw-memory-transfer
```

## Lizenz

MIT

---

**Powered by [MyClaw.ai](https://myclaw.ai)**
