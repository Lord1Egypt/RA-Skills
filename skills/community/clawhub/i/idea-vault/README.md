# Idea Vault (OpenClaw Skill)

Capture links + messy notes + timestamps from chat and save them as searchable markdown entries.

## What it does

- Saves YouTube/web/note-only captures to a local vault
- Parses messy timestamps (`24.21`, `@45:00`, `1:02:33`, etc.)
- Fetches YouTube transcripts (TranscriptAPI preferred)
- Upserts duplicate links/videos as addendums
- Supports query + annotate workflows

## Skill files

- `SKILL.md` — agent instructions
- `scripts/idea_vault.py` — extract/fetch/query/save helper
- `requirements.txt` — Python dependency (`requests`)
- `.env.example` — environment setup template

## Install

```bash
git clone https://github.com/<YOUR_USER>/idea-vault-skill.git ~/.openclaw/skills/idea-vault
cd ~/.openclaw/skills/idea-vault
python3 -m pip install -r requirements.txt
```

## Environment

Copy `.env.example` and set at least:

- `IDEA_VAULT_DIR` (where entries are stored)
- `IDEA_VAULT_TRANSCRIPTAPI_KEY` (recommended for reliable YouTube transcripts)

Optional:

- `IDEA_VAULT_YTDLP_BIN`
- `IDEA_VAULT_YTDLP_COOKIES`

## Quick usage

In chat:
1. Drop a link and your notes/timestamps
2. Send `vault` or `/vault`
3. Ask: “what did I save this week?” / “show notes about X”

## Privacy + security notes

- This skill makes outbound requests to YouTube, TranscriptAPI (if configured), and captured source/asset URLs.
- `yt-dlp` is invoked via `subprocess.run([...], shell=False)`.
- Use environment variables for keys; never commit secrets.
- If you do not want external transcript API calls, leave `IDEA_VAULT_TRANSCRIPTAPI_KEY` unset and rely on local fallback behavior.

## Notes

- Python 3 required
- `yt-dlp` is optional fallback when transcript fetch needs it
- No secrets should be committed (keep API keys in env only)
