# openclaw-skill-minimax-tracker

<p align="center">
  <img src="https://raw.githubusercontent.com/QiaoTuCodes/openclaw-skill-whisper-stt/main/assets/openclaw-skill-logo.png" alt="MiniMax Tracker" width="500" style="visibility: visible; max-width: 100%;">
</p>

<p align="center">
  <strong>📊 MiniMax API Usage Tracker Skill for OpenClaw</strong>
</p>

<p align="center">
  <a href="https://github.com/QiaoTuCodes/openclaw-skill-minimax-tracker/releases"><img src="https://img.shields.io/github/v/release/QiaoTuCodes/openclaw-skill-minimax-tracker?include_prereleases&style=for-the-badge" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
  <a href="https://github.com/QiaoTuCodes/openclaw-skill-minimax-tracker/stargazers"><img src="https://img.shields.io/github/stars/QiaoTuCodes/openclaw-skill-minimax-tracker?style=for-the-badge" alt="Stars"></a>
</p>

> Track and monitor MiniMax API usage with real-time progress bars and automated reminders for OpenClaw agents.

## ✨ Features

- 📊 **Real-time Usage Tracking** - Track prompts usage in real-time
- 📈 **Progress Bar Display** - Visual progress bar with key metrics
- ⏰ **Auto Reset Calculation** - Calculate reset time based on MiniMax rules
- 🔔 **Scheduled Reminders** - Cron-based usage check reminders
- 💾 **Persistent Storage** - JSON-based usage history
- 🔄 **Agent Integration** - Easy integration with OpenClaw agents

## 📦 Installation

```bash
# Clone to your OpenClaw workspace
cd ~/openclaw-workspace/skills
git clone https://github.com/QiaoTuCodes/openclaw-skill-minimax-tracker.git

# Or copy manually
cp -r openclaw-skill-minimax-tracker ~/openclaw-workspace/skills/
```

## 🚀 Quick Start

```bash
# View current status
python3 openclaw-skill-minimax-tracker/minimax_tracker.py status

# Add usage (after each API call)
python3 openclaw-skill-minimax-tracker/minimax_tracker.py add

# View compact progress bar
python3 openclaw-skill-minimax-tracker/minimax_tracker.py compact
```

## 📊 Progress Bar Format

```
[████████████████████] 98% RST:18:00 TTL:1h40m PKG:Starter USE:2/40 REM:38 NXT:19:19
```

**Legend:**
| Abbr | Meaning |
|------|---------|
| RST | Reset time |
| TTL | Time until reset |
| PKG | Package name |
| USE | Used prompts |
| REM | Remaining prompts |
| NXT | Next reminder time |

## 🔧 Configuration

Edit `minimax_tracker.py` to customize:

```python
CONFIG = {
    "max_prompts": 40,           # Max prompts per month
    "reset_hour_start": 15,      # Reset window start (15:00 UTC+8)
    "reset_hour_end": 20,        # Reset window end (20:00 UTC+8)
    "check_interval_hours": 3,   # Reminder interval
}
```

## 🤖 OpenClaw Integration

### Agent Code Integration

```python
import subprocess

# Track usage after API call
result = subprocess.run(
    ["python3", "~/openclaw-workspace/skills/openclaw-skill-minimax-tracker/minimax_tracker.py", "add", "1"],
    capture_output=True, text=True
)
print(result.stdout)
```

### Cron Setup (Every 3 Hours)

```json
{
  "name": "minimax-usage-check",
  "schedule": "0 */3 * * *",
  "payload": {
    "kind": "agentTurn",
    "message": "Run: python3 ~/openclaw-workspace/skills/openclaw-skill-minimax-tracker/minimax_tracker.py compact"
  }
}
```

## 📖 Documentation

- [English README](README.md)
- [中文文档](README-CN.md)
- [Skill Definition](SKILL.md)

## 🔨 Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

## 📂 Project Structure

```
openclaw-skill-minimax-tracker/
├── SKILL.md                    # OpenClaw skill definition
├── minimax_tracker.py          # Main Python script
├── README.md                   # English documentation
├── README-CN.md                # Chinese documentation
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
└── assets/                     # Logo and assets
    └── icon.png
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 👥 Authors

- **魏然 (Weiran)** - [GitHub](https://github.com/QiaoTuCodes)
- **焱焱 (Yanyan)** - AI Assistant

## 🔗 Related Links

- [OpenClaw Docs](https://docs.openclaw.ai)
- [Skill Marketplace](https://clawhub.com)
- [MiniMax Platform](https://platform.minimaxi.com)

---

<p align="center">
  <sub>Built with ❤️ for the OpenClaw community</sub>
</p>
