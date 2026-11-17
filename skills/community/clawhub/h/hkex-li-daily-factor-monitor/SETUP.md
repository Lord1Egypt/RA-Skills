# Setup: HKEX L&I Daily Factor Monitor

## Requirements
- `curl` and `jq` for announcement discovery.
- `pdftotext` (from `poppler-utils`) for PDF data extraction.
- A Telegram channel/bot configured in OpenClaw for delivery.

## Configuration
1. Create a config directory: `mkdir -p ~/.config/hkex-li-daily-factor-monitor`
2. Copy `config.example.json` to `~/.config/hkex-li-daily-factor-monitor/config.json`.
3. Edit the file to set your `openclaw_workspace` and `history_days`.

## Installation
Install via ClawdHub:
```bash
clawhub install hkex-li-daily-factor-monitor
```
