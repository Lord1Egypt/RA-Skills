# OpenClaw Direct Setup

**Double-click to install! No Docker required.**

## Quick Start

**Windows:** Double-click `setup.bat` or `setup.ps1`
**Linux/Mac:** Run `bash setup.sh`

The script will:
1. Check if Node.js is installed
2. Install OpenClaw globally
3. Create config with your LLM settings
4. Start the gateway

That's it!

## Requirements

- **Node.js** - Download from https://nodejs.org (LTS version)
- **npm** - Comes with Node.js

## What Gets Installed

- OpenClaw: `npm install -g openclaw`
- Config: `~/.openclaw/openclaw.json`
- Workspace: `~/.openclaw/workspace`

## Configuration Options

During setup, you'll be asked for:

| Option | Default | Description |
|--------|---------|-------------|
| Port | 18789 | Gateway port |
| LLM Base URL | http://localhost:8000/v1 | Your LLM API endpoint |
| LLM Model | ServiceNow-AI/Apriel-1.6-15b-Thinker:Q4_K_M | Model ID |

## Common LLM Setups

### Ollama
```
LLM Base URL: http://localhost:11434/v1
LLM Model: llama3
```

### LM Studio
```
LLM Base URL: http://localhost:1234/v1
LLM Model: llama-3-8b
```

### vLLM
```
LLM Base URL: http://localhost:8000/v1
LLM Model: mistral-7b
```

### OpenAI
```
LLM Base URL: https://api.openai.com/v1
LLM Model: gpt-4o
```

After installation, edit `~/.openclaw/openclaw.json` to add your API key.

## After Installation

- **URL:** http://localhost:18789
- **Auth Token:** Shown after installation
- **Config:** `~/.openclaw/openclaw.json`

### Commands

```bash
# Start gateway
openclaw gateway

# Stop gateway
openclaw gateway stop

# Check status
openclaw status
```

## Uninstall

```bash
npm uninstall -g openclaw
rm -rf ~/.openclaw
```

## Problems?

1. **Node.js not found** - Restart after installing Node.js
2. **Port in use** - Choose a different port during setup
3. **LLM not connecting** - Check your LLM is running and the URL is correct