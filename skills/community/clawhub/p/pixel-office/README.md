# OpenClaw Bot Dashboard Skill

🚀 Launch and manage the OpenClaw Dashboard web UI for monitoring all your bots, agents, models, and sessions.

[![ClawHub](https://img.shields.io/badge/ClawHub-openclaw--bot--dashboard-blue)](https://clawhub.com)
[![GitHub](https://img.shields.io/badge/GitHub-xmanrui%2Fopenclaw--bot--dashboard-green)](https://github.com/xmanrui/openclaw-bot-dashboard)

## 🎯 What This Skill Does

This skill automatically:
1. ✅ Detects your operating system (macOS/Windows/Linux)
2. ✅ Checks if git is installed
3. ✅ Downloads/clones the [OpenClaw Dashboard](https://github.com/xmanrui/OpenClaw-bot-review) project
4. ✅ Installs dependencies (npm install)
5. ✅ Checks for updates and pulls latest code
6. ✅ Starts the development server in background
7. ✅ Returns the access URL (local + network)

## 📦 Installation

### From ClawHub (Recommended)
```bash
npx clawhub install openclaw-bot-dashboard
```

### From skills.sh
```bash
npx skills add xmanrui/openclaw-bot-dashboard
```

### From GitHub
```bash
git clone https://github.com/xmanrui/openclaw-bot-dashboard.git ~/.openclaw/skills/openclaw-bot-dashboard
```

## 🎮 Usage

Just say any of these trigger phrases:

**中文：**
- "打开 OpenClaw-bot-review"
- "打开 Openclaw dashboard"
- "打开 bot review"
- "打开机器人大盘"
- "打开 bot-review"
- "打开openclaw机器人大盘"

**English:**
- "open openclaw dashboard"
- "open OpenClaw-bot-review"
- "open bot review"
- "open bot-review"
- "launch bot review"
- "start dashboard"

The skill will automatically handle everything and give you the access URL!

## 🌟 Features

### Smart Update Management
- **With git**: Automatically checks for updates via `git fetch` and pulls latest code
- **Without git**: Force re-downloads the latest ZIP to ensure you're always up-to-date

### Cross-Platform Support
- ✅ macOS
- ✅ Windows (PowerShell & cmd)
- ✅ Linux

### Automatic Service Management
- Stops old service before starting new one
- Ensures clean restart with latest code
- Background process management

### What You Get

The OpenClaw Dashboard provides:
- 📊 **Bot Overview** - All agents with status, model, platform bindings
- 🤖 **Model List** - All configured providers and models
- 💬 **Session Management** - Browse all sessions with token usage
- 📈 **Statistics** - Token consumption and response time trends
- 🧩 **Skill Inventory** - View all installed skills
- 🚨 **Alert Center** - Configure alert rules with notifications
- 🏥 **Gateway Health** - Real-time gateway status monitoring
- 🎨 **Pixel Office** - Fun animated pixel-art office visualization

## 📋 Prerequisites

- **Node.js 18+** must be installed
- **OpenClaw** installed with config at `~/.openclaw/openclaw.json`

## 📂 Installation Directory

The dashboard project will be installed at:
- **macOS/Linux**: `~/projects/OpenClaw-bot-review/`
- **Windows**: `%USERPROFILE%\projects\OpenClaw-bot-review\`

## 🔄 How It Works

1. **Check if service is running** → Stop old service if exists
2. **Check git availability** → Determines update strategy
3. **Check for updates**:
   - With git: `git fetch` + `git pull` if needed
   - Without git: Delete old directory + re-download ZIP
4. **Install dependencies** → `npm install` if needed
5. **Start service** → `npm run dev` in background
6. **Wait for ready** → Poll until server responds
7. **Return URLs** → Local + network access addresses

## 🛠️ Troubleshooting

### Port 3000 already in use
The skill automatically stops any service running on port 3000 before starting.

### Node.js not found
Install Node.js 18+ from https://nodejs.org/

### OpenClaw config not found
The dashboard reads from `~/.openclaw/openclaw.json`. Make sure OpenClaw is properly installed.

### Download failed
Check your internet connection or manually download from GitHub.

## 🎨 Dashboard Features

- **Auto-refresh** - Configurable intervals (10s, 30s, 1min, 5min, 10min)
- **i18n** - Chinese and English UI language switching
- **Dark/Light Theme** - Theme switcher in sidebar
- **Live Config** - Reads directly from OpenClaw config, no database needed
- **Pixel Office** - Animated characters representing your agents

## 📸 Screenshots

Visit the [OpenClaw Dashboard repository](https://github.com/xmanrui/OpenClaw-bot-review) to see screenshots.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- **Dashboard Project**: https://github.com/xmanrui/OpenClaw-bot-review
- **OpenClaw**: https://github.com/openclaw/openclaw
- **ClawHub**: https://clawhub.com
- **skills.sh**: https://skills.sh

## 👤 Author

**xmanrui**
- GitHub: [@xmanrui](https://github.com/xmanrui)

## 🙏 Acknowledgments

- OpenClaw team for the amazing agent framework
- OpenClaw Dashboard project for the beautiful UI

---

Made with ❤️ for the OpenClaw community
