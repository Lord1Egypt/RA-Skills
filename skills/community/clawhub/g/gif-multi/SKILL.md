---
name: gif-multi
description: "Search and send GIF reactions on any messaging platform (Telegram, WhatsApp, Discord, Signal, etc). Auto-detects your enabled channels."
version: 1.1.2
author: chdlc
license: MIT-0
metadata:
  openclaw:
    requires:
      bins: ["python3", "ffmpeg", "curl"]
    primaryEnv: GIPHY_API_KEY
---

# GIF Multi — Cross-platform GIF reaction

Search Giphy and send animated GIFs optimized for your current messaging channel.

## Initial setup

**1. Get a Giphy API Key**
   https://developers.giphy.com → "Create an App" → API (free, 1,000 req/day)

**2. Configure it**
   - Via `openclaw.json` (recommended):
     ```json
     { "skills": { "entries": { "gif-multi": { "env": { "GIPHY_API_KEY": "your_key" } } } } }
     ```
   - Or in `~/.openclaw/.env`:
     ```bash
     echo 'GIPHY_API_KEY=your_key' >> ~/.openclaw/.env
     ```

**3. Verify everything is ready**
   ```bash
   python3 {baseDir}/scripts/gif_multi.py --check
   ```

## Daily workflow

1. **Detect channel** from inbound metadata (`channel` field in session context).
2. **Verify config**: if missing or current channel not listed, run:
   `python3 {baseDir}/scripts/gif_multi.py --discover`
   - **First time ever** (no config): after `--discover`, briefly tell the user the skill is ready (one sentence).
   - **New channel detected**: `--discover` adds it silently. Casually mention it works here too if natural.
   - **Missing API key**: `--check` shows setup instructions; relay them to the user.
3. **Search and convert**:
   `python3 {baseDir}/scripts/gif_multi.py "<query>" --channel <channel>`
4. **Send** the output file with `message(action=send, media=<path>)`.
5. **Clean up**: `exec(rm <path>)` after sending.

The `--discover` only runs once per new channel — after that, the channel stays in config and discovery is skipped.

Each search gets a unique timestamp, so concurrent channels, topics, or threads never collide. Orphan files >10 min are cleaned automatically.

## Usage mode

The config's `"mode"` field controls when GIFs are sent:

- **`natural`** (default) — spontaneous, like emoji reactions. The agent uses its judgment to send GIFs when the conversation flows.
- **`on_request`** — only when the user explicitly asks ("send a gif of...", "reaction gif").

Change mode:
```bash
python3 {baseDir}/scripts/gif_multi.py --mode natural
python3 {baseDir}/scripts/gif_multi.py --mode on_request
```

The user can also say it in conversation: "stop sending GIFs without asking" → switches to `on_request`. "feel free to send GIFs naturally" → switches to `natural`.

## Notes

- Output is JSON with `path` to the file in `.gif_cache/`.
- Config is stored at `{baseDir}/config.json` (inside the skill folder).
- Rating defaults to `g`; override with `--rating pg|pg-13|r`.
- Giphy free limit: 1,000 requests/day.
- If the API key is missing, the script returns instructions in the `help` field.
