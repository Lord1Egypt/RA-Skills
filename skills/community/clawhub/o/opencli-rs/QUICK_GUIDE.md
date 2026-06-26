# Quick Guide: OpenCLI Skill for OpenClaw

## 🔗 GitHub Repository
https://github.com/smallnest/opencli-skill

## 📋 What's Included

### Core Files
1. **SKILL.md** - Main skill documentation for OpenClaw
2. **README.md** - GitHub repository documentation
3. **install.sh** - One-click installation script
4. **LICENSE** - MIT License

### Example Scripts
- `examples/collect-hot-content.sh` - Multi-platform data collection
- `examples/automate-cursor.sh` - Cursor IDE automation
- `examples/download-content.sh` - Content downloading

### Configuration
- `config/agent-integration.md` - AI Agent integration guide
- `package.json` - Package configuration

## 🚀 How to Use

### Option 1: Direct Installation
```bash
# Clone the repository
git clone https://github.com/smallnest/opencli-skill.git
cd opencli-skill

# Run installation
bash install.sh

# Install Chrome extension (required for browser commands)
# 1. Download from: https://github.com/jackwener/opencli/releases
# 2. Load in chrome://extensions
```

### Option 2: OpenClaw Integration
```bash
# Copy to OpenClaw skills directory
cp -r opencli-skill ~/.openclaw/workspace/skills/opencli

# The skill will be automatically detected by OpenClaw
# Next time you start OpenClaw, you can use OpenCLI commands
```

## 💡 Quick Examples

### Basic Commands
```bash
# List all available commands
opencli list

# Get Bilibili hot videos
opencli bilibili hot --limit 5 -f json

# Control Cursor IDE
opencli cursor status
opencli cursor send "Hello, help me with this code"
```

### Run Example Scripts
```bash
# Collect data from multiple platforms
bash examples/collect-hot-content.sh

# Automate Cursor IDE
bash examples/automate-cursor.sh

# Download content
bash examples/download-content.sh
```

## 🎯 Key Features

1. **AI Agent Ready** - JSON/YAML outputs for easy parsing
2. **Multi-Platform** - 50+ websites and desktop apps
3. **Desktop Automation** - Control Cursor, Codex, Antigravity
4. **Content Download** - Images, videos, articles
5. **Zero LLM Cost** - Deterministic outputs

## 🔧 Requirements

- Node.js >= 20.0.0
- Chrome browser (for browser commands)
- Chrome extension installed
- Target websites logged in (for authenticated operations)

## 🆘 Troubleshooting

```bash
# Check connection
opencli doctor

# Check daemon status
curl localhost:19825/status

# View logs
curl localhost:19825/logs
```

## 📚 Documentation

- Full OpenCLI documentation: https://github.com/jackwener/opencli
- OpenClaw documentation: https://docs.openclaw.ai
- Skill documentation: See SKILL.md

## 🎉 Enjoy!

With this skill package, you can now automate websites, control desktop apps, and manage CLI tools through your AI Agent. Happy automating! 🚀