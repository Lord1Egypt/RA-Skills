---
name: polymarket-news-monitor
description: Monitor official Polymarket sources (The Oracle blog, API status) for important updates, security alerts, and breaking news. Automatic importance scoring with instant notifications for critical events.
---

# Polymarket News Monitor 📰🔔

> **Stay informed about Polymarket updates, security alerts, and critical events**

Automatically monitors official Polymarket sources and alerts you when something important happens.

## Features

### 📊 Monitored Sources
- **The Oracle** (news.polymarket.com) - Official Polymarket blog
- **Breaking News** - Real-time updates from polymarket.com
- **API Status** - CLOB API health monitoring

### 🚨 Alert Types
- **🔴 Critical:** Security incidents, API outages, exploits
- **🟠 High:** Breaking changes, maintenance, regulatory updates
- **🟡 Medium:** General announcements, feature updates

### 🎯 Smart Detection
- Keyword-based importance scoring
- Duplicate detection (remembers seen articles)
- Configurable alert thresholds
- Multiple notification methods

## Quick Start

### Installation

```bash
# Clone skill
git clone https://github.com/yourusername/polymarket-news-monitor.git
cd polymarket-news-monitor

# Install (no dependencies!)
python3 scripts/polymarket-monitor.py
```

### Basic Usage

```bash
# Run once
python3 scripts/polymarket-monitor.py

# With custom data directory
python3 scripts/polymarket-monitor.py --data-dir /path/to/data

# Lower threshold (more alerts)
python3 scripts/polymarket-monitor.py --min-importance 2
```

### Cron Setup (Recommended)

```bash
# Check every 30 minutes
*/30 * * * * /path/to/polymarket-monitor.py --data-dir /path/to/data

# Check every hour with notifications
0 * * * * /path/to/polymarket-monitor.py --config config.json
```

## Configuration

### Config File (config.json)

```json
{
  "data_dir": "./data",
  "check_interval": 1800,
  "min_importance": 4,
  "notification": {
    "enabled": true,
    "method": "webhook",
    "webhook": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
  }
}
}
```

### Notification Methods

| Method | Description | Setup |
|--------|-------------|-------|
| `console` | Print to stdout | Default, no setup |
| `webhook` | HTTP POST to URL | Set `webhook` URL |
| `telegram` | Telegram bot (coming soon) | Set `telegram_token` and `chat_id` |
| `email` | Email alerts (coming soon) | Set SMTP credentials |

## Importance Scoring

### Keywords (2 points each)
- security, maintenance, api, update, regulation
- usdc, withdrawal, deposit, outage, downtime

### Security Alerts (5 points each)
- phishing, hack, exploit, scam, fraud
- private key, seed phrase, credential, attack

### Critical Patterns (+3 points)
- system.*down, security.*incident
- api.*deprecated, withdrawal.*disabled

### Alert Levels
| Score | Level | Action |
|-------|-------|--------|
| ≥ 7 | 🔴 Critical | Immediate notification |
| 4-6 | 🟠 High | Standard notification |
| 2-3 | 🟡 Medium | Log only (if min_importance ≤ 3) |

## Output Example

```
🔍 Polymarket News Monitor
==================================================
[2026-02-21 14:08:16] Starting Polymarket News Monitor
[2026-02-21 14:08:16] =
==================================================
[2026-02-21 14:08:16] Checking The Oracle...
[2026-02-21 14:08:17] Found: 5 new articles
[2026-02-21 14:08:17] Checking API status...
[2026-02-21 14:08:18] Found: 0 issues
[2026-02-21 14:08:18] =
==================================================
[2026-02-21 14:08:18] Total: 5 items, 2 important
[2026-02-21 14:08:18] 🚨 IMPORTANT ALERTS:

🔴 **Polymarket Alert** (The Oracle) - HIGH

**New Security Guidelines Released**

🔗 URL: https://news.polymarket.com/p/security-update
📅 Time: Mon, 21 Feb 2026 13:00:00 GMT
⚡ Importance: 8/10
🏷️ Keywords: security, phishing, credential

---
```

## Data Files

| File | Description |
|------|-------------|
| `data/news_state.json` | Seen articles hash (deduplication) |
| `data/alerts.json` | Important alerts history |
| `data/monitor.log` | Runtime log |

## API Endpoints Used

- `https://news.polymarket.com/feed` - RSS feed
- `https://clob.polymarket.com/health` - API health

## Security

✅ **No sensitive data stored**  
✅ **No API keys required**  
✅ **Read-only monitoring**  
✅ **Local data only**

## Official Sources

- Blog: https://news.polymarket.com/
- Platform: https://polymarket.com
- Docs: https://docs.polymarket.com/
- Twitter: @Polymarket

## Disclaimer

This is an unofficial monitoring tool. Always verify information on official Polymarket channels. Not affiliated with Polymarket.

## License

MIT - Free for personal and commercial use.

---

**Created for ClawHub** 🦞  
**Version:** 1.0.0  
**Last Updated:** 2026-02-21
