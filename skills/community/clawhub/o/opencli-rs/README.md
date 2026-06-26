# OpenCLI Skill for OpenClaw

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![GitHub](https://img.shields.io/github/license/smallnest/opencli-skill)](LICENSE)
[![OpenCLI](https://img.shields.io/badge/OpenCLI-Integration-green)](https://github.com/jackwener/opencli)

A comprehensive skill package for integrating [OpenCLI](https://github.com/jackwener/opencli) with [OpenClaw](https://openclaw.ai), enabling AI Agents to automate websites, control desktop apps, and manage CLI tools.

## 🌟 Features

- **🤖 AI Agent Ready** - Structured JSON/YAML outputs for easy parsing
- **🌐 Multi-Platform** - 50+ websites and desktop applications
- **🖥️ Desktop Automation** - Control Electron apps like Cursor, Codex, Antigravity
- **📥 Content Download** - Download images, videos, articles
- **🔧 External CLI Hub** - Unified management of gh, docker, obsidian, etc.
- **⚡ Zero LLM Cost** - Deterministic outputs, no token consumption

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/smallnest/opencli-skill.git
cd opencli-skill
```

### 2. Run Installation Script
```bash
bash install.sh
```

### 3. Install Chrome Extension
1. Download `opencli-extension.zip` from [OpenCLI Releases](https://github.com/jackwener/opencli/releases)
2. Open `chrome://extensions`, enable Developer mode
3. Click "Load unpacked extension" and select the extracted folder

## 🚀 Quick Start

### Basic Usage
```bash
# List all available commands
opencli list

# List commands in YAML format (AI-friendly)
opencli list -f yaml

# Get Bilibili hot videos
opencli bilibili hot --limit 10 -f json

# Get Zhihu hot topics
opencli zhihu hot -f table

# Control Cursor IDE
opencli cursor status
opencli cursor send "Analyze this code"
```

### Example Scripts
```bash
# Collect hot content from multiple platforms
bash examples/collect-hot-content.sh

# Automate Cursor IDE tasks
bash examples/automate-cursor.sh

# Download content (images, videos, articles)
bash examples/download-content.sh
```

## 📁 Project Structure

```
opencli-skill/
├── SKILL.md                    # Main skill documentation
├── README.md                   # This file
├── install.sh                  # One-click installation script
├── examples/                   # Ready-to-use example scripts
│   ├── collect-hot-content.sh  # Multi-platform data collection
│   ├── automate-cursor.sh      # Cursor IDE automation
│   └── download-content.sh     # Content downloading
├── config/                     # Configuration files
│   └── agent-integration.md    # AI Agent integration guide
└── package.json               # Package configuration
```

## 🎯 Use Cases

### 1. **AI Agent Automation**
```bash
# AI discovers available commands
opencli list -f yaml

# AI executes platform operations
opencli twitter trending --limit 10 -f json
opencli bilibili search "AI tutorial" --limit 20 -f json
```

### 2. **Data Collection**
```bash
# Collect daily trending data
bash examples/collect-hot-content.sh

# Schedule with cron
0 9 * * * /path/to/opencli-skill/examples/collect-hot-content.sh
```

### 3. **Desktop App Control**
```bash
# Control Cursor IDE
opencli cursor send "Refactor this function"
opencli cursor history --limit 5 -f json

# Control Antigravity
opencli antigravity status
opencli antigravity ask "Explain quantum computing"
```

### 4. **Content Management**
```bash
# Download Xiaohongshu notes
opencli xiaohongshu download abc123 --output ./downloads

# Export Zhihu articles
opencli zhihu download https://zhuanlan.zhihu.com/p/xxx --download-images

# Download Twitter media
opencli twitter download elonmusk --limit 20 --output ./twitter
```

## 🔧 Integration with OpenClaw

### Add to OpenClaw Skills Directory
```bash
# Copy skill to OpenClaw skills directory
cp -r opencli-skill ~/.openclaw/workspace/skills/opencli
```

### Use in OpenClaw Sessions
```bash
# In OpenClaw, the skill will be automatically detected
# You can now use OpenCLI commands through the skill
```

## 📊 Output Formats

All commands support multiple output formats:
- `-f table` - Human-readable table (default)
- `-f json` - JSON format for AI Agents
- `-f yaml` - YAML format for configuration
- `-f md` - Markdown format
- `-f csv` - CSV format for spreadsheets

## 🔗 Related Projects

- **[OpenCLI](https://github.com/jackwener/opencli)** - Universal CLI hub that this skill integrates with
- **[OpenClaw](https://openclaw.ai)** - AI Agent platform that uses this skill
- **[OpenCLI Documentation](https://github.com/jackwener/opencli/blob/main/README.zh-CN.md)** - Chinese documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- [OpenCLI](https://github.com/jackwener/opencli) by @jackwener for the amazing CLI hub
- [OpenClaw](https://openclaw.ai) community for the AI Agent platform
- All contributors and users of this skill package

---

**Happy Automating!** 🚀

If you find this skill useful, please ⭐ star the repository!