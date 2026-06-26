---
name: last30days-openclaw
description: OpenClaw adaptation of @mvanhorn's last30days skill. Research any topic from the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, and web. Includes watchlists, briefing generation, and historical query mode.
license: MIT
metadata:
  upstream_author: "@mvanhorn"
  upstream_repo: "https://github.com/mvanhorn/last30days-skill"
  adaptation: "OpenClaw adaptation by Tommy"
---

# last30days-openclaw

> **Attribution:** This skill is an OpenClaw adaptation of **@mvanhorn's** MIT-licensed project: <https://github.com/mvanhorn/last30days-skill>.

## What is original vs adapted

### Original (from @mvanhorn)
- Core Python research engine (`scripts/last30days.py` + `scripts/lib/*`)
- Multi-source data collection and ranking logic
- Watchlist, briefing, and history database architecture
- Vendored `bird-search` X client and source connectors

### OpenClaw adaptation (this folder)
- OpenClaw skill packaging (`skill.json`, this `SKILL.md`)
- OpenClaw-first storage paths under `~/.openclaw/workspace`
- OpenClaw secrets file convention: `~/.openclaw/workspace/.secrets/last30days.env`
- OpenClaw cron helper: `scripts/openclaw_watchlist_run.sh`
- Setup helper for secrets: `scripts/setup_openclaw_env.sh`

## Runtime paths (OpenClaw defaults)

- Secrets: `~/.openclaw/workspace/.secrets/last30days.env`
- DB: `~/.openclaw/workspace/data/last30days/research.db`
- Briefings: `~/.openclaw/workspace/data/last30days/briefs/`
- Output artifacts: `~/.openclaw/workspace/data/last30days/out/`

## Setup

```bash
cd ~/.openclaw/workspace/skills/last30days-openclaw
./scripts/setup_openclaw_env.sh
python3 scripts/last30days.py --diagnose
```

## macOS X-cookie support (Bird)

The vendored Bird client reads browser cookies on macOS.

- Log into x.com in Safari/Chrome/Firefox
- Verify auth:

```bash
node scripts/lib/vendor/bird-search/bird-search.mjs --whoami
```

If that fails, set `AUTH_TOKEN` + `CT0` in the secrets file.

## Command routing

Use first token to route mode:

- `watch ...` → watchlist management
- `briefing ...` → briefing generation
- `history ...` → history/FTS queries
- anything else → one-shot research

## One-shot research (default mode)

Run via OpenClaw `exec`:

```bash
cd ~/.openclaw/workspace/skills/last30days-openclaw
python3 scripts/openclaw_run.py "TOPIC"
# equivalent engine call:
# python3 scripts/last30days.py "TOPIC" --emit=compact --no-native-web
```

- Use `--quick` or `--deep` for depth.
- Use `--store` to persist findings.
- Use `--search reddit,x,youtube,tiktok,instagram,hn,polymarket,web` for source subsets.

## Watchlist mode

```bash
python3 scripts/watchlist.py add "TOPIC"
python3 scripts/watchlist.py list
python3 scripts/watchlist.py run-one "TOPIC"
python3 scripts/watchlist.py run-all
```

### OpenClaw cron integration

Use this wrapper in a scheduled exec/cron job:

```bash
~/.openclaw/workspace/skills/last30days-openclaw/scripts/openclaw_watchlist_run.sh
```

This writes logs to:
`~/.openclaw/workspace/logs/last30days-watchlist.log`

## Briefing mode

```bash
python3 scripts/briefing.py generate
python3 scripts/briefing.py generate --weekly
python3 scripts/briefing.py show --date YYYY-MM-DD
```

## History mode

```bash
python3 scripts/store.py query "TOPIC" --since 7d
python3 scripts/store.py search "QUERY"
python3 scripts/store.py trending
python3 scripts/store.py stats
```

## Notes

- If native web keys are absent, run with `--no-native-web` and use OpenClaw's `web_search` tool for web supplementation.
- Preserve source weighting in synthesis: Reddit/X/YouTube/TikTok/Instagram/HN/Polymarket signals first, web second.
- Never remove attribution to @mvanhorn when republishing this adaptation.
