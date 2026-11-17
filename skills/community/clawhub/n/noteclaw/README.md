# noteClaw

Mirror Microsoft OneNote notebooks into **local Markdown + git snapshots**, so an agent can query notes by time window, keyword, or section, and produce periodic reports of what changed.

Read-only. Nothing is ever written back to OneNote.

## What it does

- **Mirror**: notebooks → `store/<notebook>/<section>/NNN_<title>.md`, one git snapshot per sync
- **Query** (purely local, zero network, zero LLM cost): `list` / `since` / `week` / `grep` / `fetch` / `diff`
- **Report**: change reports derived from git history
- **Incremental**: ETag-based change detection, pulls changed pages only

## Requirements

- Python ≥ 3.9 (uses `zoneinfo`), standard library only, no third-party dependencies
- git (for snapshot history)
- Network access to `graph.microsoft.com` and `login.microsoftonline.com`
- A personal Microsoft account (@outlook / @hotmail / personal @live; organization accounts are unverified)

## Install

```bash
openclaw skills install @jellyjujube/noteclaw
```

Manual install: place this directory at `<workspace>/skills/noteclaw/`.

## Quick start

```bash
# 1. Create the data directory (all artifacts land here; do this before authorizing)
mkdir -p ~/onenote-mirror && cd ~/onenote-mirror
git init
git config user.name "Your Name" && git config user.email "you@example.com"
printf '.auth/\ncache/\n__pycache__/\n' >> .gitignore

# 2. One-time authorization
python3 <skill>/scripts/auth_code.py                  # prints the authorization link
python3 <skill>/scripts/auth_code.py --code-url "<full URL pasted back>"

# 3. Cold start
python3 <skill>/scripts/graph_sync.py --list-notebooks
python3 <skill>/scripts/graph_sync.py --all
python3 <skill>/scripts/html2md.py

# 4. Daily use
python3 <skill>/scripts/graph_sync.py && python3 <skill>/scripts/html2md.py
python3 <skill>/scripts/notequery.py grep --kw KEYWORD
python3 <skill>/scripts/notequery.py diff
```

Full documentation (workflow, scheduled sync, troubleshooting) is in [`SKILL.md`](./SKILL.md).

## Security and boundaries

- Authorization is **read-only** for OneNote; the scripts call OneNote endpoints only and never touch the drive
- Credentials live only in `.auth/`, environment variables, and `rclone.conf` (read-only), and are never committed; the token file is mode 0600
- The built-in `client_id` / `client_secret` are the **publicly published rclone OneDrive application** (shared by all rclone users — <https://rclone.org/onedrive/>), so nothing needs to be registered in Azure
- Change detection relies on ETag by default — Graph page timestamps may not update on content-only edits, so "what changed" is answered by git `diff`
- Images are not downloaded; in-body images appear as `[image: <resource-id>]` placeholders, and LaTeX / HTML layout is not reconstructed
- Encrypted sections and inaccessible notebooks are skipped automatically

## License

MIT-0 (MIT No Attribution). See [`LICENSE`](./LICENSE).
