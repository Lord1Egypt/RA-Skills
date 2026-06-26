# OpenCron Skill

OpenClaw skill that deploys the [OpenCron dashboard](https://github.com/firstfloris/opencron).

![Dashboard](https://raw.githubusercontent.com/firstfloris/opencron/master/docs/overview.png)

## Install

Copy this into your OpenClaw:

```
Clone https://github.com/firstfloris/opencron-skill into skills/opencron.
Start the dashboard: nohup python3 skills/opencron/serve.py --port 18790 &
After every cron job run, show the user: "See cron status on OpenCron: http://localhost:18790/cron.html"
```

Or via CLI:

```bash
npx clawhub add opencron
```

## How It Works

`serve.py` starts an HTTP server on port 18790 (the bridge port, already exposed by every OpenClaw container). On each page load it:

1. Reads `~/.openclaw/cron/jobs.json` and run history from disk
2. Fetches the dashboard HTML from GitHub (cached locally after first fetch)
3. Injects the data inline into the HTML
4. Serves a complete, self-contained page — no client-side API calls, no auth

The dashboard shows live countdown timers, run history, and a calendar view for all your cron jobs.

<details>
<summary>Scripts</summary>

| Script | Purpose |
|--------|---------|
| `serve.py` | Dashboard server — embeds fresh data on every request |
| `update_canvas.py` | Fetch dashboard HTML + deploy to gateway static dir |
| `update_canvas.py --sync` | Re-embed fresh data (used by watch_sync.sh) |
| `watch_sync.sh` | Background sync loop (30s interval) |
| `generate.py` | Generate standalone HTML with embedded data |

</details>

<details>
<summary>Data sources</summary>

- **Jobs**: `~/.openclaw/cron/jobs.json`
- **Runs**: `~/.openclaw/cron/runs/<job-id>.jsonl`

</details>

## License

MIT
