# Systemd Setup — Polymarket Optimizer

**Run polymarket-optimizer as a scheduled systemd timer on Wesley's VPS**

> **Note for Wesley Agent:** OpenClaw manages scheduling via cron jobs. This guide is for running directly on the VPS host as a fallback.

---

## Option A — OpenClaw Cron Job (Recommended)

Add to OpenClaw's cron configuration:

```
# Polymarket optimizer — every 6 hours
0 */6 * * * docker exec openclaw-yyvg-openclaw-1 python3 /data/.openclaw/workspace/skills/polymarket-optimizer/polymarket_optimizer.py
```

The optimizer runs once and exits — cron handles the scheduling.

---

## Option B — Systemd Timer (Direct VPS)

Systemd timers are more reliable than cron for services. Use a timer + service pair.

### Step 1: Create Service File

```bash
sudo nano /etc/systemd/system/polymarket-optimizer.service
```

Paste:

```ini
[Unit]
Description=Polymarket Optimizer — Parameter Tuner
Documentation=https://github.com/georges91560/polymarket-optimizer
After=network-online.target docker.service

[Service]
Type=oneshot
User=root
WorkingDirectory=/docker/openclaw-yyvg

# Load credentials from Wesley's .env
EnvironmentFile=/docker/openclaw-yyvg/.env

# Run inside OpenClaw Docker container
ExecStart=/usr/bin/docker exec openclaw-yyvg-openclaw-1 \
  python3 /data/.openclaw/workspace/skills/polymarket-optimizer/polymarket_optimizer.py

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=polymarket-optimizer
```

### Step 2: Create Timer File

```bash
sudo nano /etc/systemd/system/polymarket-optimizer.timer
```

Paste:

```ini
[Unit]
Description=Run Polymarket Optimizer every 6 hours
Requires=polymarket-optimizer.service

[Timer]
OnBootSec=5min          # First run 5 minutes after boot
OnUnitActiveSec=6h      # Then every 6 hours
Unit=polymarket-optimizer.service

[Install]
WantedBy=timers.target
```

### Step 3: Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable polymarket-optimizer.timer
sudo systemctl start polymarket-optimizer.timer
sudo systemctl status polymarket-optimizer.timer
```

Expected:
```
● polymarket-optimizer.timer - Run Polymarket Optimizer every 6 hours
   Active: active (waiting) since ...
   Trigger: 2026-03-05 20:00:00 UTC (in 5h 30min)
```

---

## Run Manually (Any Time)

```bash
# Trigger immediately without waiting for timer
sudo systemctl start polymarket-optimizer.service

# Check what happened
sudo journalctl -u polymarket-optimizer.service -n 50
```

---

## Daily Operations

```bash
# Check timer status (next run time)
sudo systemctl status polymarket-optimizer.timer

# List all timers
sudo systemctl list-timers

# View optimizer logs
sudo journalctl -u polymarket-optimizer.service -n 100

# Real-time logs during manual run
sudo journalctl -u polymarket-optimizer.service -f
```

---

## Quick Reference

```bash
# Timer control
sudo systemctl start polymarket-optimizer.timer     # Start timer
sudo systemctl stop polymarket-optimizer.timer      # Stop timer
sudo systemctl status polymarket-optimizer.timer    # Check timer

# Manual run
sudo systemctl start polymarket-optimizer.service   # Run now

# Logs
sudo journalctl -u polymarket-optimizer.service -n 50
sudo journalctl -u polymarket-optimizer.service --since today
```

---

**Version:** 1.0.0 | **Author:** Georges Andronescu (Wesley Armando)
