# SKILL.md — Local AI Stack

## Purpose
Transform any Mac into a powerful offline AI workstation. Installs Ollama (local model runner) + OpenCode (terminal coding agent) with the best pre-selected models. Fully offline — no API costs, no internet required.

## What You Get
- **Ollama** — Local model runner (14GB models, ~$0 to run)
- **OpenCode** — Terminal coding agent with free built-in models
- **4 curated models** — qwen2.5-coder, mistral, gemma3, llama3.2
- **Bi-weekly auto-updates** — New models pulled automatically
- **OpenClaw integration** — Works with your existing agent

## Requirements
- macOS (Apple Silicon recommended)
- 24GB+ RAM (for larger models)
- 50GB+ free disk space
- Homebrew installed

## Installation

### Step 1: Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Or download from: https://ollama.com/download

### Step 2: Pull Models
```bash
ollama pull qwen2.5-coder    # Best for coding
ollama pull mistral          # Fast tasks
ollama pull gemma3          # Reasoning
ollama pull llama3.2        # General purpose
```

### Step 3: Install OpenCode
```bash
brew install opencode
```

### Step 4: Configure OpenCode
```bash
# Test free built-in model
opencode run "Hello" --model opencode/big-pickle
```

## Usage

### Ollama Commands
```bash
# Run a local model
ollama run qwen2.5-coder "Write a Python function..."

# List installed models
ollama list

# Pull latest model version
ollama pull qwen2.5-coder

# Remove a model
ollama rm mistral
```

### OpenCode Commands
```bash
# Interactive coding session
opencode

# Single command
opencode run "Write a React component" --model opencode/big-pickle

# List available models
opencode models

# Help
opencode --help
```

## Model Selection Guide

| Model | Size | Best For |
|-------|------|----------|
| qwen2.5-coder | 4.7GB | Coding (primary) |
| mistral | 4.4GB | Fast responses |
| gemma3 | 3.3GB | Reasoning |
| llama3.2 | 2.0GB | General purpose |

## When to Use Local vs Cloud

### Use Local When:
- Offline (no internet)
- Privacy-sensitive work
- Quick coding tasks
- Cost-sensitive (zero API fees)
- Simple to medium complexity tasks

### Use Cloud When:
- Complex multi-step reasoning
- Web search required
- Long creative writing
- Image generation
- Advanced AI capabilities

## Bi-Weekly Auto-Update

Add to cron for automatic model updates:
```bash
# Edit crontab
crontab -e

# Add this line (1st and 15th of each month at 9 AM)
0 9 1,15 * * /path/to/update-models.sh
```

## Troubleshooting

### Ollama won't start
```bash
# Check if running
ps aux | grep ollama

# Start manually
ollama serve

# Check logs
cat ~/.ollama/ollama.log
```

### Model runs out of memory
- Close other apps
- Use smaller model (llama3.2 instead of qwen2.5-coder)
- Check available RAM: `top | head -20`

### OpenCode not found
```bash
# Find installation
which opencode

# Reinstall if needed
brew reinstall opencode
```

## Files

- Models stored: `~/.ollama/models/`
- Config: `~/.ollama/config.json`
- Logs: `~/.ollama/ollama.log`

## License
Ollama: MIT
OpenCode: MIT

## Author
Built with ❤️ for the OpenClaw community

## Notes
- Models load into RAM when used, unload when idle
- Only one model runs at a time by default
- For best performance, use Apple Silicon Mac with 24GB+ RAM