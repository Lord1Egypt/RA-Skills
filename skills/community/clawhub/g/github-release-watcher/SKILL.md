# GitHub Release Watcher

Monitor GitHub repositories for new releases and get notified.

## Setup

1. Requires `gh` CLI (GitHub CLI), authenticated
2. Edit `repos.txt` — one `owner/repo` per line, `#` for comments

## Usage

```bash
# Check all repos for new releases
bash scripts/check_releases.sh

# Use custom config file
bash scripts/check_releases.sh /path/to/repos.txt

# Dry run (show all latest releases regardless of state)
rm -f scripts/.last_seen.json && bash scripts/check_releases.sh
```

## Integration

### Cron (recommended)
Run daily via OpenClaw cron job to get notified of new releases:
```
Schedule: daily at 09:00
Payload: "Check for new GitHub releases using the github-release-watcher skill"
```

### Heartbeat
Add to HEARTBEAT.md for periodic checks (1x/day recommended).

## Output

- `🆕 **owner/repo** → tag (name)` — new release detected
- `✅ No new releases detected.` — all repos up to date

## State

Release state stored in `scripts/.last_seen.json`. Delete to reset.

## Adding Repos

Edit `repos.txt`:
```
# My tools
owner/repo
another/repo
```
