# Systemd Setup — Polymarket Executor

**Run polymarket-executor as a professional systemd service on Wesley's VPS**

Auto-start on boot · Auto-restart on crash · Centralized logs · Easy control

> **Note for Wesley Agent:** OpenClaw manages this via cron jobs. This guide is for running the executor directly on the VPS host (outside Docker) or as a fallback if cron jobs are unavailable.

---

## Prerequisites

- VPS with Ubuntu/Debian (root@srv1406447)
- Polymarket executor installed in workspace
- Environment variables configured in `.env`

---

## Option A — OpenClaw Cron Job (Recommended for Wesley)

Add to OpenClaw's cron job list:

```
# Run executor every 5 minutes (continuous scan via loop — only launch once)
0 * * * * docker exec openclaw-yyvg-openclaw-1 python3 /data/.openclaw/workspace/skills/polymarket-executor/polymarket_executor.py

# The script loops internally — cron just ensures it restarts if it crashes
```

The executor runs its own internal loop (5 min scan interval). Cron ensures it restarts automatically if it crashes.

---

## Option B — Systemd Service (Direct VPS)

### Step 1: Create Service File

```bash
sudo nano /etc/systemd/system/polymarket-executor.service
```

Paste:

```ini
[Unit]
Description=Polymarket Executor — Multi-Strategy Trading Bot
Documentation=https://github.com/georges91560/polymarket-executor
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/docker/openclaw-yyvg

# Load credentials from Wesley's .env
EnvironmentFile=/docker/openclaw-yyvg/.env

# Run inside OpenClaw Docker container
ExecStart=/usr/bin/docker exec openclaw-yyvg-openclaw-1 \
  python3 /data/.openclaw/workspace/skills/polymarket-executor/polymarket_executor.py

# Restart policy
Restart=on-failure
RestartSec=30
StartLimitInterval=300
StartLimitBurst=5

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=polymarket-executor

# Resource limits
MemoryMax=1G
CPUQuota=100%

[Install]
WantedBy=multi-user.target
```

### Step 2: Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable polymarket-executor
sudo systemctl start polymarket-executor
sudo systemctl status polymarket-executor
```

Expected:
```
● polymarket-executor.service - Polymarket Executor
   Active: active (running) since ...
   Main PID: 12346 (docker)

polymarket-executor[12346]: [MODE] 📄 PAPER TRADING
polymarket-executor[12346]: [GAMMA] Fetched 2,341 markets
polymarket-executor[12346]: [SCAN] Found 8 opportunities
```

---

## Daily Operations

```bash
# Real-time logs
sudo journalctl -u polymarket-executor -f

# Last 100 lines
sudo journalctl -u polymarket-executor -n 100

# Today's logs
sudo journalctl -u polymarket-executor --since today

# Stop
sudo systemctl stop polymarket-executor

# Restart
sudo systemctl restart polymarket-executor

# Check status
sudo systemctl status polymarket-executor
```

---

## Monitor Performance Files

```bash
# Portfolio status
docker exec openclaw-yyvg-openclaw-1 \
  python3 -c "import json; p=json.load(open('/data/.openclaw/workspace/portfolio.json')); print(f'Capital: \${p[\"current_capital\"]:.2f} | P&L: {p[\"daily_pnl\"]:+.2f}')"

# Paper trades count
docker exec openclaw-yyvg-openclaw-1 \
  python3 -c "import json; t=json.load(open('/data/.openclaw/workspace/paper_trades.json')); print(f'Total trades: {len(t)} | Resolved: {sum(1 for x in t if x[\"status\"] in [\"won\",\"lost\",\"closed\"])}')"

# Live opportunities log
docker exec openclaw-yyvg-openclaw-1 \
  tail -5 /data/.openclaw/workspace/live_trades.jsonl
```

---

## Test Auto-Restart

```bash
# Get PID
sudo systemctl status polymarket-executor | grep "Main PID"

# Kill process (simulates crash)
sudo kill -9 <PID>

# Wait 30 seconds, then verify auto-restart
sudo systemctl status polymarket-executor
# Should show new PID and "active (running)"
```

---

## Troubleshooting

**Service won't start — wrong Docker container name**
```bash
# Find correct container name
docker ps --format "{{.Names}}"
# Update ExecStart with correct name
```

**Service won't start — .env not found**
```bash
ls /docker/openclaw-yyvg/.env
# If missing, create it with required variables
```

**"Container not running" error**
```bash
# Ensure OpenClaw is up first
cd /docker/openclaw-yyvg
docker compose up -d
```

**High memory usage**
```bash
# Reduce scan workers in learned_config.json
# scan_workers: 25 instead of 50
```

---

## Quick Reference

```bash
sudo systemctl start polymarket-executor      # Start
sudo systemctl stop polymarket-executor       # Stop
sudo systemctl restart polymarket-executor    # Restart
sudo systemctl status polymarket-executor     # Status
sudo journalctl -u polymarket-executor -f     # Live logs
sudo systemctl enable polymarket-executor     # Enable on boot
sudo systemctl disable polymarket-executor    # Disable on boot
```

---

**Version:** 2.0.0 | **Author:** Georges Andronescu (Wesley Armando)
