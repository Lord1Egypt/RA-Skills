# status-page-gen Setup Guide

## Overview

`status-page-gen` generates a lightweight, self-contained HTML status page for your self-hosted services. No Node.js, no Docker — pure Python stdlib.

---

## 1. Configure Your Services

Copy the example config:

```bash
cp ~/.openclaw/workspace/skills/status-page-gen/assets/services.example.json \
   ~/.openclaw/workspace/skills/status-page-gen/assets/services.json
```

Edit `services.json`. Each service needs at minimum a `name` and `url`:

```json
{
  "services": [
    {
      "name": "My App",
      "url": "https://myapp.example.com",
      "health_endpoint": "/health",
      "expected_status": 200,
      "ping_host": "myapp.example.com",
      "tags": ["web"]
    }
  ]
}
```

### Field Reference

| Field | Required | Default | Description |
|---|---|---|---|
| `name` | ✓ | — | Display name |
| `url` | ✓ | — | Base URL of the service |
| `health_endpoint` | — | `/` | Path appended to `url` for health check |
| `expected_status` | — | `200` | HTTP status code considered "up" |
| `ping_host` | — | derived from `url` | Hostname for ICMP ping |
| `tags` | — | `[]` | Display labels (monitoring, media, etc.) |

### Status Logic

| HTTP | Ping | Result |
|---|---|---|
| ✓ | ✓ | `up` |
| ✓ | ✗ | `up` (ICMP may be firewalled) |
| ✗ | ✓ | `degraded` |
| ✗ | ✗ | `down` |

---

## 2. Run Manually

```bash
cd ~/.openclaw/workspace/skills/status-page-gen

# Check services
python3 scripts/check_services.py \
  --config assets/services.json \
  --output /tmp/status_check.json \
  --verbose

# Check SSL certs (HTTPS services only)
python3 scripts/check_certs.py \
  --config assets/services.json \
  --output /tmp/cert_check.json \
  --verbose

# Append to history log
python3 scripts/history.py \
  --append /tmp/status_check.json \
  --db assets/history.json

# Generate page
python3 scripts/generate_page.py \
  --services /tmp/status_check.json \
  --certs /tmp/cert_check.json \
  --history assets/history.json \
  --title "My Homelab Status" \
  --output ~/status.html
```

---

## 3. Schedule with Cron

Run every 5 minutes:

```bash
crontab -e
```

Add:

```cron
*/5 * * * * cd ~/.openclaw/workspace/skills/status-page-gen && \
  python3 scripts/check_services.py --config assets/services.json --output /tmp/status_check.json 2>/dev/null && \
  python3 scripts/check_certs.py --config assets/services.json --output /tmp/cert_check.json 2>/dev/null && \
  python3 scripts/history.py --append /tmp/status_check.json --db assets/history.json 2>/dev/null && \
  python3 scripts/generate_page.py --services /tmp/status_check.json --certs /tmp/cert_check.json --history assets/history.json --title "My Status" --output /var/www/html/status.html 2>/dev/null
```

### macOS LaunchAgent

Alternatively, use a macOS LaunchAgent for more reliable scheduling. Create `~/Library/LaunchAgents/com.statuspage.check.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.statuspage.check</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-c</string>
    <string>cd ~/.openclaw/workspace/skills/status-page-gen && python3 scripts/check_services.py --config assets/services.json --output /tmp/status_check.json && python3 scripts/check_certs.py --config assets/services.json --output /tmp/cert_check.json && python3 scripts/history.py --append /tmp/status_check.json --db assets/history.json && python3 scripts/generate_page.py --services /tmp/status_check.json --certs /tmp/cert_check.json --history assets/history.json --output ~/status.html</string>
  </array>
  <key>StartInterval</key><integer>300</integer>
  <key>RunAtLoad</key><true/>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.statuspage.check.plist
```

---

## 4. Serving the Status Page

### Locally with Python

```bash
cd ~ && python3 -m http.server 8080
# Open http://localhost:8080/status.html
```

### Nginx (if installed)

Copy `status.html` to your web root:

```bash
cp ~/status.html /var/www/html/status.html
```

### Push to GitHub Gist

Using the GitHub CLI (`gh`):

```bash
# First time: create the Gist
gh gist create ~/status.html --filename index.html --public --desc "My Service Status"

# Subsequent updates (replace GIST_ID with your Gist ID)
gh gist edit GIST_ID -f index.html ~/status.html
```

The page will be available at: `https://gist.githack.com/YOUR_USERNAME/GIST_ID/raw/index.html`

---

## 5. History and Uptime

The history module appends each check run to `assets/history.json`. Uptime percentages (24h, 7d, 30d) appear on the status page once you have enough history.

Prune old data to keep the file manageable:

```bash
# Keep only the last 30 days
python3 scripts/history.py --prune 30 --db assets/history.json
```

---

## 6. SSL Certificate Monitoring

`check_certs.py` only checks HTTPS services. By default it warns when a cert has ≤ 30 days remaining.

Customize the warning threshold:

```bash
python3 scripts/check_certs.py --config assets/services.json --warn-days 60
```

---

## 7. Troubleshooting

**Ping always fails:** Some hosts block ICMP. Ping failures for HTTPS/HTTP-passing services don't mark them as down — they show as `up`. Only when both HTTP and ping fail does a service go `down`.

**SSL check fails with "verification failed":** The cert may use a private/self-signed CA. This is reported as an error (not a full check failure) in the cert section.

**HTTP check times out:** Adjust with `--timeout 15` (default is 10s).

**Page doesn't refresh:** The HTML includes `<meta http-equiv="refresh" content="300">` — it auto-refreshes every 5 minutes in the browser.
