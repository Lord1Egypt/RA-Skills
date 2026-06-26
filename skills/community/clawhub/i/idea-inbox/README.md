# idea-inbox (灵感妙计)

A personal idea inbox that writes to Feishu/Lark Bitable.

## What it does

- Triggered by DM messages starting with `idea:` or `灵感：`
- Uses an LLM to produce:
  - Category (single-select)
  - Tags (multi-select, auto-add new tags)
  - AI summary (rewritten/condensed original)
- Writes a record into a Bitable "idea inbox".
- Daily digest at configurable time (default 10:02 Asia/Shanghai). If 0 new items today, do not send.

## Setup

This skill is designed to be **zero-config**:

- On first run, it creates a new Bitable App named `灵感妙计` with required fields.
- It then saves config to `~/.openclaw/idea-inbox/config.json`.

## Model auth

- Prefers `~/.codex/auth.json` + `~/.codex/config.toml` (do **not** read API keys from env).
- Optional fallback model config can be placed into `config.json`.
