# OpenClaw Expert Brain

Skill de Claude Code para consultar el manual interactivo de OpenClaw via NotebookLM.

## Descripción

Este skill permite a los arquitectos consultar una base de conocimiento con **185 fuentes curadas** sobre OpenClaw directamente desde Claude Code. Usa `nlm` (notebooklm-mcp-cli) para hacer queries al notebook via API, sin necesidad de Chromium.

## Instalación

1. Asegúrate de tener `nlm` instalado:
   ```bash
   pip install notebooklm-mcp-cli
   ```

2. Autentica con Google:
   ```bash
   nlm login --provider openclaw
   ```

3. (Opcional) Configura la variable de entorno:
   ```bash
   export OPENCLAW_NOTEBOOK_ID=577a138c-807f-45d7-9ff4-cb1d6da190c0
   ```

## Uso desde terminal

```bash
python3 scripts/ask.py --question "¿cómo instalo OpenClaw en un VPS?"
python3 scripts/ask.py -q "how do I create a custom skill?"
python3 scripts/ask.py -q "troubleshooting gateway errors" --notebook-id 577a138c-807f-45d7-9ff4-cb1d6da190c0
```

## Por qué nlm en vez de Chromium

La versión anterior usaba patchright (fork de Playwright) + Chromium headless para hacer scraping de la interfaz web de NotebookLM. Esto implicaba:

- **200MB** de Chromium para descargar
- Selectores CSS frágiles que rompen cuando NotebookLM actualiza su UI
- Dependencias complejas de sistema (libglib2, libnss3, etc.)

Esta versión usa `nlm notebook query` que accede a NotebookLM via API oficial, resultando en:

- Sin dependencias de sistema pesadas
- Sin selectores CSS que se rompen
- Respuestas más rápidas y confiables
- Mantenimiento mínimo

## Fuentes del notebook

El notebook `577a138c-807f-45d7-9ff4-cb1d6da190c0` contiene 185 fuentes curadas:

| Categoría | Fuentes |
|---|---|
| Documentación oficial docs.openclaw.ai | 16 páginas |
| GitHub oficial (openclaw, clawhub, skills, community) | ~30 repos |
| Tutoriales en español | 25+ artículos y videos |
| Skills y ClawHub | 30+ guías y ejemplos |
| Multi-agent y cron | 25 fuentes avanzadas |
| Troubleshooting y seguridad | 20 fuentes |

## Licencia

MIT License — ver LICENSE para detalles.
