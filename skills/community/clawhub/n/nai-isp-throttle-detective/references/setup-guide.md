# ISP Throttle Detective — Setup Guide

## Quick Start

```bash
# 1. Run a speed test and log it
python3 scripts/speedtest.py | python3 scripts/log_result.py

# 2. Analyze patterns (after collecting a few days of data)
python3 scripts/analyze.py

# 3. Generate a full evidence report
python3 scripts/report.py
```

## Configuration

Copy the example config and customize:

```bash
mkdir -p ~/.isp-throttle-detective
cp assets/config.example.json ~/.isp-throttle-detective/config.json
```

All scripts automatically detect `~/.isp-throttle-detective/config.json`. Pass `--config /path/to/config.json` to override.

### Key config options

| Field | Default | Description |
|-------|---------|-------------|
| `log_file` | `~/.isp-throttle-detective/speed_log.jsonl` | Where results are stored |
| `timeout_seconds` | `30` | Max seconds per download test |
| `max_download_bytes` | `25000000` | Cap download at 25 MB per test |
| `peak_hours` | `[18-23, 0]` | Hours considered "peak" (0-23) |
| `endpoints` | See example | Dict of test targets |

## Scheduling Tests

### macOS (launchd) — every 30 minutes

Create `~/Library/LaunchAgents/com.isp-throttle-detective.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.isp-throttle-detective</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/sh</string>
    <string>-c</string>
    <string>python3 /path/to/skills/isp-throttle-detective/scripts/speedtest.py | python3 /path/to/skills/isp-throttle-detective/scripts/log_result.py</string>
  </array>
  <key>StartInterval</key>
  <integer>1800</integer>
  <key>RunAtLoad</key>
  <false/>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.isp-throttle-detective.plist
```

### Linux (cron) — every 30 minutes

```bash
crontab -e
# Add:
*/30 * * * * python3 /path/to/skills/isp-throttle-detective/scripts/speedtest.py | python3 /path/to/skills/isp-throttle-detective/scripts/log_result.py >> ~/.isp-throttle-detective/cron.log 2>&1
```

## Script Reference

### speedtest.py

Downloads from multiple endpoints, measures download + upload speed in Mbps.

```bash
python3 speedtest.py                        # uses default config
python3 speedtest.py --config /path/to/config.json
```

Output: JSON to stdout, progress to stderr.

### log_result.py

Appends speedtest output to the log with enriched fields (hour, day_of_week).

```bash
python3 speedtest.py | python3 log_result.py
python3 log_result.py --input result.json
python3 log_result.py --log /custom/log.jsonl
```

### analyze.py

Reads the log and outputs patterns: by hour, by day, trend, anomalies, CDN discrimination.

```bash
python3 analyze.py                  # human-readable
python3 analyze.py --json           # machine-readable JSON
python3 analyze.py --days 30        # limit to last 30 days
python3 analyze.py --log /path/to/log.jsonl
```

### report.py

Generates a full markdown evidence report with tables, trend data, and conclusions.

```bash
python3 report.py                   # saves to ~/.isp-throttle-detective/reports/
python3 report.py --out report.md   # custom output path
python3 report.py --days 30         # analyze last 30 days
```

## Interpreting Results

### Peak vs Off-Peak

A drop of **>20%** in speed during peak hours is a strong throttling signal. ISPs often cap bandwidth during high-congestion windows (typically 6pm–midnight).

### CDN Discrimination

If CDN speeds (Netflix, YouTube, streaming platforms) are consistently **<75% of general internet speeds**, the ISP is likely selectively throttling streaming traffic. This is distinct from general congestion and requires a different argument to the ISP.

### Trend

- **Declining:** File a support ticket immediately, reference the trend data in the report
- **Stable:** No infrastructure degradation
- **Improving:** ISP may have upgraded capacity recently

### Anomalies

Z-score < -2.0 means the reading is more than 2 standard deviations below your personal average. Multiple anomalies at the same hour suggest systematic throttling, not random variation.

## Building an ISP Complaint

Use `report.py` to generate the evidence. Key points to include in your complaint:

1. **Test dates and frequency** — shows this is systematic, not a one-time glitch
2. **Peak vs off-peak table** — the clearest evidence of throttling behavior
3. **CDN ratio** — if applicable, shows discriminatory traffic management
4. **Trend chart** — if service is degrading over time

Ask specifically: "Is traffic shaping or throttling applied to my connection during peak hours or for specific endpoints?"

If the ISP disputes your data, reference the multiple independent endpoints tested (Cloudflare, Google, etc.) — if all show the same pattern, it's the ISP's network, not a single server issue.
