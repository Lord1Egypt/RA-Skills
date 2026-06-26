# Polymarket News Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://openclaw.ai)

> **Stay informed about Polymarket updates, security alerts, and critical events**

Automatically monitors official Polymarket sources and alerts you when something important happens.

## 🚀 Features

- 📰 **The Oracle Blog** - RSS feed monitoring
- 🔌 **API Status** - Real-time health checks
- 🚨 **Smart Alerts** - Importance-based notifications
- 🔍 **Security Detection** - Phishing, exploits, scams
- 📊 **Breaking News** - Critical updates immediately
- 💾 **No External Dependencies** - Pure Python

## 📦 Installation

```bash
git clone https://github.com/mig6671/polymarket-news-monitor.git
cd polymarket-news-monitor
python3 scripts/polymarket-monitor.py
```

## 📝 Usage

### Basic
```bash
python3 scripts/polymarket-monitor.py
```

### With Options
```bash
python3 scripts/polymarket-monitor.py --data-dir ./my-data --min-importance 2
```

### Cron (Every 30 minutes)
```bash
*/30 * * * * /path/to/polymarket-monitor.py --config config.json
```

## ⚙️ Configuration

Create `config.json`:
```json
{
  "data_dir": "./data",
  "min_importance": 4,
  "notification": {
    "enabled": true,
    "method": "webhook",
    "webhook": "https://hooks.slack.com/services/YOUR/WEBHOOK"
  }
}
```

## 🎯 Alert Levels

| Level | Score | Example |
|-------|-------|---------|
| 🔴 Critical | ≥ 7 | Security breach, API down |
| 🟠 High | 4-6 | Breaking changes, maintenance |
| 🟡 Medium | 2-3 | General updates |

## 📚 Documentation

See [SKILL.md](SKILL.md) for detailed documentation.

## 🔗 Official Sources

- Blog: https://news.polymarket.com/
- Platform: https://polymarket.com
- Docs: https://docs.polymarket.com/

## ⚠️ Disclaimer

This is an **unofficial** monitoring tool. Not affiliated with Polymarket. Always verify on official channels.

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

**Made for OpenClaw** 🦞
