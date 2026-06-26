# OpenCron Skill

OpenClaw skill that deploys the [OpenCron dashboard](https://github.com/firstfloris/opencron).

![Dashboard](https://raw.githubusercontent.com/firstfloris/opencron/master/docs/overview.png)

## Install

Copy this into your OpenClaw:

```
Clone https://github.com/firstfloris/opencron-skill into skills/opencron.
Run python3 skills/opencron/update_canvas.py to deploy the dashboard.
Run nohup sh skills/opencron/watch_sync.sh & to start background sync.
After every cron job run, show the user: "See cron status on OpenCron: <dashboard-url>"
```

Or via CLI:

```bash
npx clawhub add opencron
```

```bash
npx opencron-skill add
```

<details>
<summary>Manual setup</summary>

### 1. Deploy

```bash
python3 skills/opencron/update_canvas.py
```

Fetches the latest dashboard from GitHub and writes live job data.

### 2. Start sync

```bash
nohup sh skills/opencron/watch_sync.sh &
```

### 3. Open

```bash
open "http://$(curl -s ifconfig.me):${CANVAS_PORT:-8090}/cron.html?token=${OPENCLAW_GATEWAY_TOKEN}"
```

### Scripts

| Script | Purpose |
|--------|---------|
| `update_canvas.py` | Fetch dashboard HTML from GitHub + write JSON to canvas |
| `watch_sync.sh` | Background sync loop (30s interval) |
| `generate.py` | Generate standalone HTML with embedded data |
| `serve.py` | Local HTTP server for development |

### External Serving

For access outside Docker, use `nginx-canvas.conf.template`:

- Token validation via query parameter
- Rate limiting (10 req/s per IP)
- Security headers (CSP, X-Frame-Options)
- Run log JSONL serving from `/runs/`

```yaml
# docker-compose.yml
canvas-proxy:
  image: nginx:alpine
  restart: unless-stopped
  environment:
    OPENCLAW_GATEWAY_TOKEN: ${OPENCLAW_GATEWAY_TOKEN}
  volumes:
    - ./nginx-canvas.conf.template:/etc/nginx/templates/default.conf.template:ro
    - ./cron/runs:/openclaw-data/cron/runs:ro
  ports:
    - "127.0.0.1:${CANVAS_PORT:-8090}:80"
```

### Data Sources

- **Jobs**: `~/.openclaw/cron/jobs.json`
- **Runs**: `~/.openclaw/cron/runs/<job-id>.jsonl`

</details>

## License

MIT
