# Systemd Service (Linux)

Alternative to cron for Linux servers.

```ini
# /etc/systemd/system/openclaw-watchdog.service
[Unit]
Description=OpenClaw Gateway Watchdog
After=network.target

[Service]
Type=oneshot
ExecStart=/root/.openclaw/watchdog.sh
User=root

[Timer]
# /etc/systemd/system/openclaw-watchdog.timer
[Unit]
Description=Run OpenClaw Watchdog every minute

[Timer]
OnCalendar=*:0/1
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl enable openclaw-watchdog.timer
sudo systemctl start openclaw-watchdog.timer
```
