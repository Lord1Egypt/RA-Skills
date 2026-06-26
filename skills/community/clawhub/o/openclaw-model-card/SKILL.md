---
name: openclaw-model-card
description: Generate OpenClaw model inventory and model-card images from openclaw.json. Use when asked to list all configured models, verify default/fallback chains, or render/share a visual model card screenshot.
---

# OpenClaw Model Card

Use this skill to output OpenClaw model configuration in a consistent way.

## Core workflow

1. Run text output:
   ```bash
   python3 skills/openclaw-model-card/scripts/show-model-config.py --config /path/to/openclaw.json
   ```
2. If user wants a screenshot/image card, render image:
   ```bash
   python3 skills/openclaw-model-card/scripts/show-model-config.py --config /path/to/openclaw.json --image ./model-card.png
   ```
3. If running in chat surfaces where terminal output is invisible to the user, send the script output via messaging tool instead of paraphrasing.

## Rules

- Do not handcraft model lists when this skill is requested; always use the script output.
- Prefer `--config` explicitly for reproducibility.
- Keep sensitive config files out of git; only publish generated, sanitized artifacts.

## Notes

- `md2img.js` depends on `wkhtmltoimage`.
- The script includes consistency checks (missing model refs, alias conflicts, suspicious contextWindow).
