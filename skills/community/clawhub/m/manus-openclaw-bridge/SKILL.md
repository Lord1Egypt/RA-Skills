---
name: manus-openclaw-bridge
description: Connect OpenClaw to Manus task APIs for chat-driven image generation, document/slides jobs, task polling, output collection, and messaging-surface return flows.
version: 1.0.2
requires:
  - OpenClaw
  - Bash
  - curl
  - Python 3.9+
  - Node.js 18+
config:
  - MANUS_API_KEY (required, local only, stored in ~/.config/manus-openclaw-bridge/manus.env)
  - MANUS_API_BASE (required, HTTPS only, explicitly set in ~/.config/manus-openclaw-bridge/manus.env)
  - MANUS_AGENT_PROFILE (optional)
  - MANUS_TASK_MODE (optional)
external_services:
  - Manus API
security_notes:
  - No secrets are bundled in the package.
  - Downloader accepts only HTTPS URLs from allowlisted Manus-controlled hosts.
  - Redirect targets are revalidated before file bytes are written.
---

# Manus OpenClaw Bridge

Use this skill to turn OpenClaw into a Manus launcher and result collector.

## Requirements

Runtime dependencies:
- OpenClaw
- Bash
- `curl`
- Python 3.9+
- Node.js 18+ (required for slides JSON -> PPTX conversion)

Required local configuration:
- `~/.config/manus-openclaw-bridge/manus.env`
- `MANUS_API_KEY` must be supplied by each installer
- `MANUS_API_BASE` must be supplied explicitly by each installer and must use `https://`

Read `REQUIREMENTS.md` for a concise dependency and configuration summary.
Read `SECURITY.md` for the download and credential safety model.

## Quick start

1. Read `references/setup.md` if Manus API access is not configured yet.
2. Put the Manus API key and Manus API base URL in `~/.config/manus-openclaw-bridge/manus.env`.
3. Submit a task with `scripts/manus_submit.sh` or `scripts/manus_prompt.sh`.
4. Poll/download results with `scripts/manus_get_task.sh` or `scripts/manus_wait_and_collect.py`.
5. If the result is a slides JSON bundle, convert it with `scripts/manus_slides_json_to_pptx.mjs`.
6. If the user is on Feishu, return downloaded files with the normal OpenClaw message/file send flow.

## Workflow

### 1. Submit a new Manus task

Use `scripts/manus_submit.sh "<prompt>"` when the prompt is already clean.

Use `scripts/manus_prompt.sh "Manus, generate an image of a rainy forest"` when the message may contain a leading `Manus` trigger and mixed punctuation.

Defaults:
- `MANUS_AGENT_PROFILE=manus-1.6`
- `MANUS_TASK_MODE=agent`
- `MANUS_API_BASE` must be set explicitly to your Manus API base URL

### 2. Inspect an existing task

Use `scripts/manus_get_task.sh <task_id>` to fetch the raw task payload.

### 3. Wait for completion and collect files

Use `python3 scripts/manus_wait_and_collect.py <task_id> [timeout_seconds]`.

This writes downloaded files to `tmp/manus/` under the skill folder and prints a JSON summary with:
- `task_id`
- `status`
- `task_title`
- `task_url`
- `files[]`
- `raw`

Download safety rules:
- only `https://` URLs are accepted
- only Manus-controlled allowlisted hosts are accepted
- redirect targets are validated again after connection open
- if Manus returns any other URL, the script refuses to fetch it and records a `download_error`

### 4. Handle slides/report outputs

If Manus returns a slides JSON artifact instead of a ready-made `.pptx`, convert it with:

```bash
node scripts/manus_slides_json_to_pptx.mjs <slides.json> <output.pptx>
```

Read `references/slides.md` when the task is slide-heavy.

### 5. Return results to the user

Prefer this pattern:
- If Manus returns downloadable files, send the files.
- If Manus returns images, send image files directly.
- If Manus returns only text/status, send a short summary plus the task URL when available.
- If Manus is still running, acknowledge quickly and poll with a bounded interval instead of a tight loop.

## Feishu return pattern

When the current conversation is Feishu:
- Download files first with `scripts/manus_wait_and_collect.py`.
- Send each saved file path back through OpenClaw’s normal reply/file mechanism.
- For images, prefer image/file upload rather than pasting long CDN URLs.
- If there are multiple files, send the best result first, then the rest if useful.

Read `references/feishu-return.md` when wiring file return behavior.

## OpenClaw integration notes

- Keep secrets out of the skill package. Never hardcode `MANUS_API_KEY` in scripts or docs.
- Store keys and endpoints in `~/.config/manus-openclaw-bridge/manus.env` on each recipient machine.
- For direct-message style image requests, a simple trigger is enough: strip `Manus,` or `manus:` and forward the remainder.
- For group chats, define an explicit trigger rule to avoid accidental job launches.
- If returning files to Feishu/Telegram/etc., use the platform’s native send/upload tool after `manus_wait_and_collect.py` downloads the outputs.
- If the request is long-running, prefer acknowledging first and completing asynchronously.

## When to read references

- Read `references/setup.md` for first-time installation and environment setup.
- Read `references/chat-patterns.md` when wiring the Manus flow into OpenClaw message handling rules.
- Read `references/feishu-return.md` when returning Manus images/files into Feishu.
- Read `references/feishu-skill-template.md` when another OpenClaw user wants a ready-made Feishu routing pattern.
- Read `references/openclaw-integration.md` for a full end-to-end integration pattern.
- Read `references/slides.md` when handling deck-generation outputs.
