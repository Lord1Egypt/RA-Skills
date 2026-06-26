# Model Usage Monitor

[![Version](https://img.shields.io/badge/version-1.0.1-blue)](https://clawhub.ai)
[![License](https://img.shields.io/badge/license-MIT--0-green)](https://spdx.org/licenses/MIT-0.html)

> **OpenClaw Model Usage Monitoring & Alerting Skill**

Monitor and analyze AI model usage, calculate costs, track cache hit rates, and receive hourly automated alerts.

## ⚠️ Security & Permissions Declaration

**This skill performs read-only monitoring of local log files:**

| Operation | Purpose | Scope |
|-----------|---------|-------|
| Read `semantic_check.log` | Parse model usage statistics | Read-only, local file |
| Read OpenClaw gateway logs | Detect usage anomalies | Read-only, local files |
| Send alert notifications | Notify user of cost spikes | Local OpenClaw API only |
| Create Cron Job (optional) | Hourly automated checks | Local Cron only |

**What this skill does NOT do:**
- Does NOT modify any configuration or log files
- Does NOT access external servers or APIs
- Does NOT use encrypted or obfuscated code
- Does NOT require payment or licensing
- Does NOT access model credentials
- **Fully transparent** — all source code is readable

## Features

- Parse semantic router logs and analyze model usage distribution
- Estimate model call counts and costs
- Calculate cache hit rates
- Hourly automated alert checks
- Real-time monitoring mode

## Installation

```bash
# The skill includes monitoring scripts and auto-configuration
bash ~/.openclaw/workspace/skills/model-usage-monitor/install.sh
```

## Usage

### View Monitoring Reports

```bash
# Full report
python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py

# JSON format
python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py --format json

# Alert check only
python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py --alert-check
```

### Real-time Monitoring

```bash
python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py --live
```

## Alert Thresholds

| Type | Threshold | Description |
|------|-----------|-------------|
| Frequent Opus calls | >5 times/hour | Prevent unexpected high-cost model usage |
| High Opus cost | >$0.50/hour | Cost control |
| High total cost | >$2.00/hour | Overall budget control |

## File Structure

```
.skills/model-usage-monitor/
├── README.md           # This file
├── SKILL.md            # Skill documentation (Chinese)
├── install.sh          # Transparent installation script
├── monitor.py          # Core monitoring script
├── setup.py            # Auto-installation/configuration
└── config.json         # Default configuration
```

## Technical Details

- Uses only local file operations
- Read-only log analysis — zero system impact
- Based on semantic_check.log and gateway.log analysis
- No external network calls
- No encrypted or obfuscated code

## 📄 License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

**Maintainer**: halfmoon82  
**Last Updated**: 2026-03-12
