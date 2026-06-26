---
name: openclaw-expert-brain
slug: openclaw-expert-brain
version: 1.0.0
description: Manual interactivo de OpenClaw con 185 fuentes curadas en NotebookLM. Pregunta sobre instalación, configuración, skills, troubleshooting, multi-agent, cron, seguridad. Responde en español e inglés.
author: radelqui
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["python3", "nlm"]
---

# OpenClaw Expert Brain

Manual interactivo de OpenClaw potenciado por NotebookLM con 185 fuentes curadas.

## Cuándo activar este skill

Activa cuando el usuario:
- Pregunta sobre OpenClaw: instalación, configuración, setup, skills, ClawHub
- Dice "help", "ayuda", "manual", "how to", "cómo se hace"
- Menciona problemas: "error", "no funciona", "troubleshooting", "fix"
- Pregunta sobre multi-agent, cron, seguridad, MCP, mcporter
- Usa frases como "pregunta al manual", "consulta el brain", "ask expert"

## Uso

```bash
# Preguntar algo sobre OpenClaw
python3 {baseDir}/scripts/ask.py --question "¿cómo instalo OpenClaw en un VPS?"

# Preguntar en inglés
python3 {baseDir}/scripts/ask.py --question "how do I create a custom skill?"

# Con notebook ID explícito
python3 {baseDir}/scripts/ask.py --question "troubleshooting gateway errors" --notebook-id 577a138c-807f-45d7-9ff4-cb1d6da190c0
```

## Requisitos

- `nlm` CLI instalado: `pip install notebooklm-mcp-cli`
- Auth Google activa: `nlm login --provider openclaw`
- Variable opcional: `OPENCLAW_NOTEBOOK_ID` (por defecto usa el notebook oficial)

## Notebook de referencia

Consulta un cuaderno NotebookLM con 185 fuentes curadas:
- Documentación oficial docs.openclaw.ai (16 páginas)
- GitHub oficial: openclaw, clawhub, skills, community
- Tutoriales en español: 25+ artículos y videos
- Skills y ClawHub: 30+ guías y ejemplos
- Multi-agent y cron: 25 fuentes avanzadas
- Troubleshooting y seguridad: 20 fuentes

## Notas

- Respuestas en 5-10 segundos (sin Chromium, via API nlm)
- Responde en el idioma de la pregunta (español/inglés)
- Cero alucinaciones: solo responde con info de las 185 fuentes
- No requiere Chromium ni patchright
