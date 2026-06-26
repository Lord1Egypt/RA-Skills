---
name: neomano-vps-monitoring
description: Monitor DigitalOcean VPS (Droplets) by fetching metrics from the DigitalOcean API (v2): list droplets, fetch CPU/memory/disk/bandwidth time-series, and produce quick summaries. Use when the user asks for server metrics, droplet utilization, bandwidth, or health checks for their DigitalOcean servers.
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "requires": { "bins": ["python3"], "env": ["DIGITALOCEAN_TOKEN"] },
      "primaryEnv": "DIGITALOCEAN_TOKEN"
    },
    "clawdbot": {
      "emoji": "📈",
      "requires": { "bins": ["python3"], "env": ["DIGITALOCEAN_TOKEN"] },
      "primaryEnv": "DIGITALOCEAN_TOKEN"
    }
  }
---

## Credentials

Set `DIGITALOCEAN_TOKEN` (recommended: `~/.openclaw/.env`).

## What it can do

- List droplets (`/v2/droplets`) and find a droplet by name.
- Fetch metrics (Monitoring API):
  - CPU: `/v2/monitoring/metrics/droplet/cpu`
  - Memory usage % (computed): `memory_available` + `memory_total`
  - Disk usage % (computed): `filesystem_free` + `filesystem_size`
  - Bandwidth: `/v2/monitoring/metrics/droplet/bandwidth` (requires `direction=inbound|outbound`)

## Run

```bash
python3 {baseDir}/scripts/do_metrics.py droplets
python3 {baseDir}/scripts/do_metrics.py cpu --droplet "web-1" --minutes 60
python3 {baseDir}/scripts/do_metrics.py memory --droplet "web-1" --minutes 60
python3 {baseDir}/scripts/do_metrics.py bandwidth --droplet "web-1" --minutes 60
```

Notes:
- Output is JSON (raw time-series + a small computed summary).
- Requires that DigitalOcean Monitoring is enabled for the droplet.
