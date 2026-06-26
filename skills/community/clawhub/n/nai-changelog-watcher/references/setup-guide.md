# Changelog Watcher — Setup Guide

## Directory Layout

After skill installation, the working directory is:
```
~/.openclaw/workspace/skills/changelog-watcher/
├── SKILL.md
├── scripts/
│   ├── check_github.py
│   ├── check_npm.py
│   ├── compare_versions.py
│   └── format_report.py
├── references/
│   └── setup-guide.md       ← you are here
├── assets/
│   └── watchlist.example.json
├── watchlist.json            ← create this (user config)
└── state.json                ← auto-created on first run
```

---

## 1. Create watchlist.json

Copy the example and edit it:

```bash
cp assets/watchlist.example.json watchlist.json
```

Each entry has a `source` field (`"github"` or `"npm"`) plus source-specific fields:

### GitHub entry
```json
{
  "source": "github",
  "owner": "anthropics",
  "repo": "anthropic-sdk-python",
  "name": "Anthropic Python SDK",
  "include_prereleases": false
}
```

### npm entry
```json
{
  "source": "npm",
  "package": "@anthropic-ai/sdk",
  "name": "Anthropic JS SDK"
}
```

- `name` is optional but recommended — it appears in the report header.
- `include_prereleases` is optional (default `false`); set to `true` to include alpha/beta/RC releases.

---

## 2. First Run (Baseline)

On first run, `compare_versions.py` records current versions as the baseline and reports **zero new releases**. This is intentional — it prevents flooding you with the entire release history.

```bash
cd ~/.openclaw/workspace/skills/changelog-watcher
python3 scripts/compare_versions.py --update-state
```

After this, `state.json` is created with current versions.

---

## 3. Checking for Updates

Run the full pipeline:

```bash
python3 scripts/compare_versions.py --update-state | python3 scripts/format_report.py
```

- `--update-state` writes new versions back to `state.json` so the next run only shows truly new releases.
- Omit `--update-state` to do a dry-run (check but don't advance the state).

### Custom paths

```bash
python3 scripts/compare_versions.py \
  --watchlist /path/to/watchlist.json \
  --state /path/to/state.json \
  --update-state
```

---

## 4. Cron Schedule

To run daily at 9am ET and save the report:

```cron
0 9 * * * cd ~/.openclaw/workspace/skills/changelog-watcher && python3 scripts/compare_versions.py --update-state | python3 scripts/format_report.py >> reports/$(date +\%Y-\%m-\%d).md 2>/dev/null
```

Create the reports dir first: `mkdir -p reports`

---

## 5. GitHub Rate Limits

The GitHub public API allows **60 requests/hour** without authentication. Each GitHub entry in your watchlist costs 1 request per run.

- If rate limited, `compare_versions.py` skips that entry with a warning and continues.
- To increase the limit to 5,000/hr, set a `GITHUB_TOKEN` env var in your scripts or pass it as an `Authorization: Bearer <token>` header. The scripts are designed to work without a token; add one only if needed.
- Spread watches across time: if you have 50+ repos, run checks every 2 hours instead of every hour.

---

## 6. state.json Format

Auto-managed. Don't edit manually unless resetting a specific entry.

```json
{
  "github:nodejs/node": "v22.12.0",
  "github:neovim/neovim": "v0.10.2",
  "npm:next": "15.1.6",
  "npm:typescript": "5.7.2"
}
```

To **reset** a specific package (force it to re-check from the current version), delete its key and run again.

---

## 7. Individual Script Usage

Run scripts standalone for debugging:

```bash
# Check a single GitHub repo
python3 scripts/check_github.py nodejs node --limit 5

# Check a single npm package
python3 scripts/check_npm.py next

# Format a saved JSON file
python3 scripts/format_report.py new_releases.json

# Full pipeline, dry-run (no state update)
python3 scripts/compare_versions.py | python3 scripts/format_report.py
```

---

## 8. Exit Codes

| Code | Meaning |
|------|---------|
| 0    | Success |
| 1    | General error (bad args, file not found, etc.) |
| 2    | Rate limited |
| 3    | Package/repo not found |
