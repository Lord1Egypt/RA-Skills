# OpenClaw Token Saver

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive guide for reducing OpenClaw token consumption by 50-90%.

## 🎯 Overview

This skill provides **automatic token monitoring** and **20+ manual strategies** across 5 categories to minimize token usage.

### Automatic Triggers

The skill automatically activates when:

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Token Warning | 70% | 💡 Suggest compression |
| Token Critical | 80% | ⚠️ Force optimization |
| Token Emergency | 90% | 🚨 Emergency reset |
| Per-turn limit | 4000 tokens | Warn input size |
| Conversation length | 10 turns | Suggest compact |

### Trigger Flow

```
User Input → Check Token Usage → Trigger? → Show Recommendations
                  ↓
            [70%] Warning Banner
            [80%] Critical Alert + Auto-suggest
            [90%] Emergency + Force Action
```

1. **Context Slimming** - Reduce conversation history overhead
2. **Tool Optimization** - Streamline prompts and responses
3. **Caching & Reuse** - Leverage caching mechanisms
4. **Model Control** - Smart model selection and limits
5. **Local Alternatives** - Self-hosted solutions

## 📊 Token Savings by Category

| Category | Potential Savings |
|----------|------------------|
| Context Slimming | 30-60% |
| Tool Optimization | 20-40% |
| Caching & Reuse | 40-70% |
| Model Control | 50-80% |
| Local Alternatives | 100% |

## 🚀 Quick Start

### Installation

```bash
clawhub install openclaw-token-saver
```

### Or manual install

```bash
git clone https://github.com/yourusername/openclaw-token-saver.git
cp -r openclaw-token-saver ~/.openclaw/workspace/skills/
```

## 🤖 Automatic Mode

### Enable Auto-Monitoring

Copy the config file to your OpenClaw config:

```bash
cp config/token-saver.json ~/.openclaw/config/token-saver.json
```

### How It Works

1. **Background Monitoring** - Watches token usage in real-time
2. **Smart Triggers** - Activates at 70%/80%/90% thresholds
3. **Contextual Suggestions** - Recommends actions based on usage pattern
4. **One-click Actions** - Provides `/compact`, `/nc`, `/reset` shortcuts

### Example Auto-Response

```
⚠️ Token Usage Alert
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current: 8,234 / 10,000 (82.3%)
Status: CRITICAL

Recommended Actions:
1. /compact - Compress conversation history
2. /nc - Switch to minimal context
3. /reset - Reset session (keep memory)

Press 1, 2, or 3 to apply, or continue to ignore.
```

## 💡 Top 5 Quick Wins

### 1. Enable Auto-Compact
```bash
clawhub install claw-compact
```

### 2. Limit History
```json
{
  "max_history_messages": 10
}
```

### 3. Use Context Commands
- `/nc` - Minimal context
- `/cc` - Compact context
- `/fc` - Full context (when needed)

### 4. Disable Unused Tools
```json
{
  "tools": {
    "enabled": ["read", "write", "exec"]
  }
}
```

### 5. Set Token Budget
```json
{
  "token_budget": {
    "per_session": 50000
  }
}
```

## 📚 Detailed Strategies

### Context Management

#### Manual Compression
Send `/compact` in conversation to summarize history.

#### Sliding Window
Keep only recent messages:
```json
{
  "max_history_messages": 10,
  "max_history_tokens": 4000
}
```

#### Layered Context
| Command | Context | Use Case |
|---------|---------|----------|
| `/nc` | Current + System | Quick queries |
| `/cc` | Last 10 messages | Normal tasks |
| `/fc` | Full history | Complex analysis |

### Tool Optimization

#### Minimize Tool Descriptions
Keep skill descriptions under 100 characters.

#### Limit Tool Returns
```json
{
  "web_search": {
    "max_results": 3,
    "max_chars": 500
  },
  "web_fetch": {
    "max_chars": 3000
  }
}
```

### Caching Strategies

#### Enable Prompt Caching
```json
{
  "model": {
    "enable_prompt_caching": true
  }
}
```

#### Heartbeat for Cache Warmth
Set heartbeat < cache TTL:
```json
{
  "heartbeat": {
    "interval_minutes": 55
  },
  "cache": {
    "ttl_minutes": 60
  }
}
```

### Model Selection

#### Tiered Model Usage
```json
{
  "models": {
    "simple": "gpt-3.5-turbo",
    "standard": "gpt-4",
    "complex": "gpt-4o"
  }
}
```

#### Automatic Downgrade
Configure fallback to cheaper models.

### Local Deployment

#### Ollama Setup
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run local model
ollama run qwen2.5:14b
```

#### OpenClaw Configuration
```json
{
  "model": {
    "provider": "ollama",
    "base_url": "http://localhost:11434",
    "model": "qwen2.5:14b"
  }
}
```

## 🔧 Configuration Examples

### Minimal Config (Max Savings)
```json
{
  "context": {
    "max_history_messages": 5
  },
  "tools": {
    "enabled": ["read", "write"]
  },
  "limits": {
    "max_retries": 0,
    "token_budget_per_turn": 2000
  }
}
```

### Balanced Config
```json
{
  "context": {
    "max_history_messages": 10,
    "auto_compact": true
  },
  "tools": {
    "enabled": ["read", "write", "exec", "web_search"]
  },
  "model": {
    "default": "gpt-3.5-turbo",
    "complex_tasks": "gpt-4"
  },
  "limits": {
    "max_iterations": 10,
    "token_budget_per_session": 50000
  }
}
```

### Power User Config
```json
{
  "context": {
    "strategy": "adaptive",
    "compress_threshold": 5000
  },
  "cache": {
    "enabled": true,
    "ttl_minutes": 60
  },
  "tools": {
    "enabled": "all",
    "max_response_chars": 5000
  },
  "model": {
    "provider": "ollama",
    "local_fallback": true
  }
}
```

## 📈 Monitoring Savings

### Check Token Usage
```bash
openclaw status
```

### View Session Stats
```
Token Usage: 12,345 / 50,000 (24%)
Messages: 15
Compression: 3 times
```

## 🛠️ Recommended Skills

| Skill | Purpose | Savings |
|-------|---------|---------|
| claw-compact | Auto-compression | 30-50% |
| qmd | Local indexing | 80%+ |
| exa-search | Efficient search | 70%+ |

## 🤝 Contributing

Contributions welcome! Please submit PRs with:
- New token-saving strategies
- Configuration examples
- Benchmarks

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- OpenClaw Community
- Anthropic Claude Team
- Ollama Project

---

**Start saving tokens today!** 💰
