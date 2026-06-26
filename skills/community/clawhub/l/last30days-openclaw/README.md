# last30days-openclaw

OpenClaw adaptation of **@mvanhorn's** `last30days-skill`:
<https://github.com/mvanhorn/last30days-skill>

## Attribution (required)

- **Original author:** [@mvanhorn](https://github.com/mvanhorn)
- **Original project:** <https://github.com/mvanhorn/last30days-skill>
- **Original license:** MIT
- **This adaptation license:** MIT (preserved)

This repository is a **separate adaptation** for OpenClaw packaging and runtime conventions.
It does **not** replace the upstream project and should not be represented as the original work.

## What came from upstream vs what changed

### Upstream/original work (credited to @mvanhorn)
- Research engine (`scripts/last30days.py`)
- Source connectors and scoring pipeline (`scripts/lib/*`)
- Watchlist/briefing/history architecture (`scripts/watchlist.py`, `scripts/briefing.py`, `scripts/store.py`)
- X search vendor integration (`scripts/lib/vendor/bird-search/*`)
- Research methodology and source synthesis structure

### OpenClaw adaptation work (this repo)
- OpenClaw skill metadata (`skill.json`)
- OpenClaw usage docs (`SKILL.md`)
- OpenClaw workspace path defaults:
  - `~/.openclaw/workspace/.secrets/last30days.env`
  - `~/.openclaw/workspace/data/last30days/*`
- Setup helper for OpenClaw secrets (`scripts/setup_openclaw_env.sh`)
- OpenClaw cron/watchlist runner (`scripts/openclaw_watchlist_run.sh`)
- Updated path/help text for OpenClaw operations

## Sources supported

- Reddit
- X / Twitter
- YouTube
- TikTok
- Instagram Reels
- Hacker News
- Polymarket
- Web search backends (Brave/Parallel/OpenRouter or OpenClaw web_search)

## OpenClaw quick start

```bash
cd ~/.openclaw/workspace/skills/last30days-openclaw
./scripts/setup_openclaw_env.sh
python3 scripts/last30days.py --diagnose
python3 scripts/openclaw_run.py "openclaw agent frameworks" --quick --search hn,polymarket
```

## API key handling in OpenClaw

Primary secrets file:

`~/.openclaw/workspace/.secrets/last30days.env`

Recommended keys:

- `SCRAPECREATORS_API_KEY` (Reddit + TikTok + Instagram)
- `XAI_API_KEY` (optional fallback for X when Bird cookie auth is unavailable)
- `BRAVE_API_KEY` / `PARALLEL_API_KEY` / `OPENROUTER_API_KEY` (optional native web search)

## macOS X cookie support

The vendored Bird module supports browser cookie auth on macOS.

```bash
node scripts/lib/vendor/bird-search/bird-search.mjs --whoami
```

If unavailable, use `AUTH_TOKEN` and `CT0` in the secrets file.

## Watchlist + OpenClaw cron integration

Use:

```bash
~/.openclaw/workspace/skills/last30days-openclaw/scripts/openclaw_watchlist_run.sh
```

as the scheduled command in your OpenClaw cron/scheduler job.

## Compatibility note

Upstream `last30days-skill` remains compatible with Claude Code, Pi, and Codex variants.
This adaptation is specifically tuned for OpenClaw workspace conventions and tool orchestration.

## License

MIT (same as upstream). See `LICENSE`.

---

If you publish this adaptation (GitHub/ClawHub), keep the attribution block above intact and link back to the upstream project.
