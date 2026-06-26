# Module 4: Context and Costs — Ollama, Model Routing, and Optimization

## Table of Contents
1. [Ollama Integration for Local LLMs](#ollama-integration-for-local-llms)
2. [Context Management Strategies](#context-management-strategies)
3. [Smart Model Routing](#smart-model-routing)
4. [Prompt Caching](#prompt-caching)
5. [Cost Optimization](#cost-optimization)
6. [Monitoring and Budgeting](#monitoring-and-budgeting)

---

## Ollama Integration for Local LLMs

### Why Local LLMs?

Running LLMs locally through **Ollama** provides:
- **Privacy**: Data never leaves your machine
- **Cost**: Zero per-token fees after hardware investment
- **Latency**: No network round-trips
- **Availability**: Works offline
- **Customization**: Run fine-tuned models

### Installing Ollama

#### macOS
```bash
# Using Homebrew
brew install ollama

# Or download from https://ollama.com
```

#### Linux
```bash
# Install script (recommended)
curl -fsSL https://ollama.com/install.sh | sh

# Or manual installation
curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/local/bin/ollama
chmod +x /usr/local/bin/ollama

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama
```

#### Windows (WSL2)
```bash
# Inside WSL2
curl -fsSL https://ollama.com/install.sh | sh

# Ensure WSL2 has GPU access (NVIDIA)
# Install CUDA toolkit in WSL2:
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install -y cuda-toolkit
```

### Real Model Recommendations

Based on current performance testing, here are the recommended models:

| Model | Parameters | Use Case | VRAM | Speed | Quality |
|-------|------------|----------|------|-------|---------|
| **llama3.1:8b** | 8B | General chat, coding help | 6GB | 30-50 t/s | ⭐⭐⭐ |
| **llama3.1:70b** | 70B | Complex reasoning, analysis | 40GB | 5-10 t/s | ⭐⭐⭐⭐⭐ |
| **glm-5:cloud** | 744B MoE | State-of-the-art reasoning | Cloud | Variable | ⭐⭐⭐⭐⭐ |
| **kimi-k2.5:cloud** | MoE | Long context, coding | Cloud | Variable | ⭐⭐⭐⭐⭐ |
| **codellama:34b** | 34B | Code completion | 20GB | 10-20 t/s | ⭐⭐⭐⭐ |
| **mistral:7b** | 7B | Fast responses, simple tasks | 5GB | 40-60 t/s | ⭐⭐⭐ |
| **nemotron-3-super:cloud** | Cloud | Instruction following | Cloud | Variable | ⭐⭐⭐⭐ |

### Pulling and Running Models

```bash
# List available models
ollama list

# Pull recommended models
ollama pull llama3.1:8b
ollama pull llama3.1:70b
ollama pull codellama:34b
ollama pull mistral:7b

# Pull cloud models via Ollama
ollama pull glm-5:cloud
ollama pull kimi-k2.5:cloud

# Run a model interactively
ollama run llama3.1:8b

# Run with custom parameters
ollama run llama3.1:8b --temperature 0.7 --top_p 0.9
```

### OpenClaw Ollama Configuration

```json5
// ~/.openclaw/openclaw.json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/glm-5:cloud",
        "fallbacks": [
          "ollama/llama3.1:8b",
          "anthropic/claude-sonnet-4-5"
        ]
      },
      "models": {
        "ollama/llama3.1:8b": {
          "alias": "Local Fast",
          "cost": { "input": 0, "output": 0 }
        },
        "ollama/glm-5:cloud": {
          "alias": "GLM-5 Cloud",
          "cost": { "input": 0, "output": 0 }
        }
      }
    }
  },
  
  "models": {
    "mode": "merge",
    "providers": {
      "ollama": {
        "baseUrl": "http://localhost:11434",
        "api": "openai",
        "models": [
          {
            "id": "llama3.1:8b",
            "name": "Llama 3.1 8B",
            "contextWindow": 128000,
            "maxTokens": 4096,
            "cost": { "input": 0, "output": 0 }
          },
          {
            "id": "llama3.1:70b",
            "name": "Llama 3.1 70B",
            "contextWindow": 128000,
            "maxTokens": 4096,
            "cost": { "input": 0, "output": 0 }
          },
          {
            "id": "glm-5:cloud",
            "name": "GLM-5 744B MoE",
            "contextWindow": 128000,
            "maxTokens": 8192,
            "cost": { "input": 0, "output": 0 }
          },
          {
            "id": "kimi-k2.5:cloud",
            "name": "Kimi K2.5",
            "contextWindow": 256000,
            "maxTokens": 8192,
            "cost": { "input": 0, "output": 0 }
          }
        ]
      }
    }
  }
}
```

### Hardware Requirements

| Model | VRAM Required | RAM Required | GPU Example | Speed |
|-------|---------------|--------------|-------------|-------|
| Llama 3.1 8B | 6GB | 16GB | RTX 3060 12GB | 30-50 t/s |
| Llama 3.1 70B | 40GB | 64GB | RTX A6000 (48GB) | 5-10 t/s |
| Mistral 7B | 5GB | 16GB | RTX 3060 | 40-60 t/s |
| CodeLlama 34B | 20GB | 32GB | RTX 4090 (24GB) | 10-20 t/s |

### Running Ollama on CPU vs GPU

```bash
# GPU (default if available)
ollama run llama3.1:8b

# Force CPU
CUDA_VISIBLE_DEVICES="" ollama run llama3.1:8b

# Specific GPU
CUDA_VISIBLE_DEVICES=0 ollama run llama3.1:8b

# Multi-GPU
CUDA_VISIBLE_DEVICES=0,1 ollama run llama3.1:70b
```

---

## Context Management Strategies

### Understanding Context Windows

| Model | Context Window | Cost per 1M tokens (Input) | Cost per 1M tokens (Output) |
|-------|----------------|---------------------------|----------------------------|
| GPT-5.2 | 128K | $2.50 | $10.00 |
| Claude 3.5 Sonnet | 200K | $3.00 | $15.00 |
| Claude 4 Opus | 200K | $15.00 | $75.00 |
| Llama 3.1 (local) | 128K | $0 | $0 |
| GLM-5 (cloud) | 128K | $0 | $0 |
| Gemini 1.5 Pro | 2M | $3.50 | $10.50 |

### Context Pruning Strategies

#### 1. Session Compaction

```json5
{
  "session": {
    "compaction": {
      "enabled": true,
      "maxMessages": 50,
      "summaryModel": "ollama/llama3.1:8b"
    }
  }
}
```

#### 2. Selective Context Loading

```json5
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "lightContext": true
      },
      "context": {
        "bootstrapFiles": ["SOUL.md", "IDENTITY.md", "USER.md", "AGENTS.md"]
      }
    }
  }
}
```

#### 3. Skill-Based Context Control

```markdown
---
name: lightweight-task
description: A task that doesn't need full context
metadata:
  {
    "openclaw":
      {
        "context": { "lightweight": true }
      }
  }
---

# Lightweight Task

This skill skips heavy bootstrap context.
```

### Token Counting and Monitoring

```bash
# Check current session tokens
openclaw status

# Output shows:
# - Current model
# - Tokens used this session
# - Estimated cost
```

### Message Management Commands

```bash
# Reset session (clears context)
/new
/reset

# Compact session (summarize history)
/compact

# Check status
/status
```

---

## Smart Model Routing

### Provider Configuration with Real Examples

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/glm-5:cloud",
        "fallbacks": [
          "openrouter/z-ai/glm-5",
          "anthropic/claude-sonnet-4-5",
          "ollama/llama3.1:8b"
        ]
      }
    }
  },
  
  "models": {
    "mode": "merge",
    "providers": {
      "anthropic": {
        "apiKey": { "source": "env", "id": "ANTHROPIC_API_KEY" },
        "models": [
          {
            "id": "claude-sonnet-4-5",
            "name": "Claude 3.5 Sonnet",
            "cost": { "input": 0.003, "output": 0.015 },
            "contextWindow": 200000
          },
          {
            "id": "claude-opus-4-6",
            "name": "Claude 4 Opus",
            "cost": { "input": 0.015, "output": 0.075 },
            "contextWindow": 200000
          }
        ]
      },
      
      "openai": {
        "apiKey": { "source": "env", "id": "OPENAI_API_KEY" },
        "models": [
          {
            "id": "gpt-5.2",
            "name": "GPT-5.2",
            "cost": { "input": 0.0025, "output": 0.01 },
            "contextWindow": 128000
          }
        ]
      },
      
      "openrouter": {
        "apiKey": { "source": "env", "id": "OPENROUTER_API_KEY" },
        "models": [
          {
            "id": "z-ai/glm-5",
            "name": "GLM-5 via OpenRouter",
            "cost": { "input": 0.001, "output": 0.005 },
            "contextWindow": 128000
          }
        ]
      },
      
      "ollama": {
        "baseUrl": "http://localhost:11434",
        "api": "openai",
        "models": [
          {
            "id": "llama3.1:8b",
            "name": "Llama 3.1 8B Local",
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 128000
          },
          {
            "id": "glm-5:cloud",
            "name": "GLM-5 Cloud",
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 128000
          }
        ]
      }
    }
  }
}
```

### Task-Based Model Selection

```javascript
// Router configuration for different task types
{
  "routing": {
    "rules": [
      {
        "pattern": "code review|review.*code|PR review",
        "model": "anthropic/claude-opus-4-6",
        "priority": "quality"
      },
      {
        "pattern": "quick fix|simple edit|one-liner",
        "model": "ollama/llama3.1:8b",
        "priority": "speed"
      },
      {
        "pattern": "architecture|design|complex.*debug",
        "model": "ollama/glm-5:cloud",
        "priority": "quality"
      },
      {
        "pattern": "heartbeat|status check|monitor",
        "model": "ollama/llama3.1:8b",
        "priority": "cost"
      }
    ]
  }
}
```

### Dynamic Model Switching

```bash
# In chat, switch models
/model glm-5
/model claude-sonnet-4-5
/model llama3.1:8b

# Check available models
/models

# Check current model
/status
```

---

## Prompt Caching

### Understanding Prompt Caching

Prompt caching stores the processed version of prompts to reduce:
- **Token costs**: Cached tokens are significantly cheaper
- **Latency**: No re-processing of identical prefixes
- **API load**: Reduced compute for providers

### Real Cost Comparison

| Provider | Cache Write | Cache Read | Regular Input | Savings |
|----------|-------------|------------|---------------|---------|
| **Anthropic** | 1.25x input | 0.1x input | 1x | ~90% |
| **OpenAI** | 1x input | 0.5x input | 1x | ~50% |
| **Local (Ollama)** | N/A | N/A | $0 | 100% |

### Actual Prompt Caching Example

```json5
// OpenClaw configuration with prompt caching
{
  "models": {
    "providers": {
      "anthropic": {
        "cache": {
          "enabled": true,
          "ttlMinutes": 60
        },
        "models": [
          {
            "id": "claude-sonnet-4-5",
            "cost": {
              "input": 0.003,
              "output": 0.015,
              "cacheRead": 0.0003,    // 90% cheaper!
              "cacheWrite": 0.00375   // 25% premium for first write
            }
          }
        ]
      }
    }
  }
}
```

### Cost Calculation Example

**Scenario**: 50 messages, 2000 tokens of system prompt each

Without caching:
```
50 messages × 2000 tokens × $0.003 = $300
```

With caching (assuming 90% cache hit rate):
```
First message: 2000 × $0.00375 = $7.50 (cache write)
Remaining 49 messages: 49 × 2000 × $0.0003 = $29.40 (cache read)
Total: $36.90 (88% savings!)
```

### Cache Optimization Strategies

#### 1. Stable System Prompts

Keep system prompts consistent to maximize cache hits:

```markdown
# SOUL.md (stable, cached)
Core personality - rarely changes
→ Cached efficiently

# HEARTBEAT.md (stable, cached)
Checklist - changes occasionally  
→ Cached efficiently

# USER.md (semi-stable)
Preferences - update as needed
→ Cache invalidated on change
```

#### 2. Skill Ordering

```json5
{
  "skills": {
    "load": {
      "order": "alphabetical"  // consistent ordering for better caching
    }
  }
}
```

---

## Cost Optimization

### Detailed Cost Comparison

#### Cloud Providers (per 1M tokens)

| Provider/Model | Input | Output | Cache Read | Cache Write |
|----------------|-------|--------|------------|-------------|
| **OpenAI GPT-5.2** | $2.50 | $10.00 | $1.25 | $2.50 |
| **OpenAI GPT-5.2-mini** | $0.15 | $0.60 | $0.075 | $0.15 |
| **Anthropic Claude Sonnet 4.5** | $3.00 | $15.00 | $0.30 | $3.75 |
| **Anthropic Claude Haiku 4.1** | $0.25 | $1.25 | $0.025 | $0.31 |
| **Anthropic Claude Opus 4.6** | $15.00 | $75.00 | $1.50 | $18.75 |
| **Google Gemini 1.5 Pro** | $3.50 | $10.50 | Varies | Varies |
| **Google Gemini 1.5 Flash** | $0.35 | $1.05 | Varies | Varies |

#### Local/Ollama Costs

| Model | Setup Cost | Running Cost | Break-even vs Cloud |
|-------|-----------|--------------|---------------------|
| Llama 3.1 8B | $0 (existing hardware) | ~$0.10/day electricity | Immediate |
| RTX 4090 setup | ~$2,000 | ~$0.50/day electricity | 6-12 months |
| RTX A6000 setup | ~$5,000 | ~$1/day electricity | 12-18 months |

### Cost Monitoring Script

```bash
#!/bin/bash
# ~/.openclaw/scripts/cost-monitor.sh

# Daily cost report
echo "=== OpenClaw Daily Cost Report ==="
echo "Date: $(date)"

# Get usage from session logs
SESSION_DIR="$HOME/.openclaw/agents/default/sessions"
TODAY=$(date +%Y-%m-%d)

# Calculate today's cost
TODAY_COST=0
for session in "$SESSION_DIR"/*.jsonl; do
  if [ -f "$session" ]; then
    SESSION_DATE=$(head -1 "$session" | jq -r '.timestamp' | cut -dT -f1)
    if [ "$SESSION_DATE" = "$TODAY" ]; then
      COST=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$session")
      TODAY_COST=$(echo "$TODAY_COST + $COST" | bc)
    fi
  fi
done

echo "Today's estimated cost: \$$TODAY_COST"

# Weekly average
WEEK_COST=0
for i in {0..6}; do
  DAY=$(date -d "$i days ago" +%Y-%m-%d)
  DAY_COST=0
  for session in "$SESSION_DIR"/*.jsonl; do
    if [ -f "$session" ]; then
      SESSION_DATE=$(head -1 "$session" | jq -r '.timestamp' | cut -dT -f1 2>/dev/null)
      if [ "$SESSION_DATE" = "$DAY" ]; then
        COST=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$session" 2>/dev/null)
        DAY_COST=$(echo "$DAY_COST + $COST" | bc)
      fi
    fi
  done
  WEEK_COST=$(echo "$WEEK_COST + $DAY_COST" | bc)
done

WEEKLY_AVG=$(echo "scale=2; $WEEK_COST / 7" | bc)
echo "7-day average: \$$WEEKLY_AVG/day"
echo "Projected monthly: \$$$(echo "scale=2; $WEEKLY_AVG * 30" | bc)"

# Budget check
DAILY_BUDGET=10.00
if (( $(echo "$TODAY_COST > $DAILY_BUDGET" | bc -l) )); then
  echo "⚠️  WARNING: Daily budget exceeded!"
fi
```

### Smart Model Routing Configuration

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/glm-5:cloud",
        "fallbacks": [
          "openrouter/z-ai/glm-5",
          "anthropic/claude-sonnet-4-5",
          "ollama/llama3.1:8b"
        ]
      }
    }
  },
  
  "routing": {
    "strategies": {
      "cost_optimized": {
        "description": "Minimize costs while maintaining quality",
        "tiers": [
          { "model": "ollama/llama3.1:8b", "maxTokens": 500 },
          { "model": "ollama/glm-5:cloud", "maxTokens": 2000 },
          { "model": "anthropic/claude-haiku-4-1", "maxTokens": 4000 }
        ]
      },
      "quality_optimized": {
        "description": "Best quality regardless of cost",
        "tiers": [
          { "model": "ollama/glm-5:cloud", "maxTokens": 8000 },
          { "model": "anthropic/claude-opus-4-6", "maxTokens": 8000 },
          { "model": "anthropic/claude-sonnet-4-5", "maxTokens": 8000 }
        ]
      },
      "balanced": {
        "description": "Balance cost and quality",
        "tiers": [
          { "model": "ollama/llama3.1:8b", "maxTokens": 1000 },
          { "model": "ollama/glm-5:cloud", "maxTokens": 4000 },
          { "model": "anthropic/claude-sonnet-4-5", "maxTokens": 8000 }
        ]
      }
    }
  }
}
```

---

## Monitoring and Budgeting

### Cost Tracking Setup

```json5
{
  "models": {
    "providers": {
      "anthropic": {
        "models": [
          {
            "id": "claude-sonnet-4-5",
            "cost": {
              "input": 0.003,
              "output": 0.015,
              "cacheRead": 0.0003,
              "cacheWrite": 0.00375
            }
          }
        ]
      }
    }
  },
  
  "usage": {
    "tracking": true,
    "reportFrequency": "session",
    "budgets": {
      "daily": 10.00,
      "monthly": 100.00
    },
    "actions": {
      "onBudgetExceeded": "warn"
    }
  }
}
```

### Budget Controls

```json5
{
  "usage": {
    "budgets": {
      "daily": 10.00,      // $10/day limit
      "monthly": 100.00,   // $100/month limit
      "perSession": 5.00   // $5 per session limit
    },
    "actions": {
      "onBudgetExceeded": "fallback-to-local",
      "fallbackModel": "ollama/llama3.1:8b"
    }
  }
}
```

### Real Cost Scenarios

#### Personal Assistant (Light Usage)

| Activity | Daily Volume | Model | Daily Cost |
|----------|--------------|-------|------------|
| Quick queries | 30 | Llama 3.1 8B (local) | $0 |
| Complex tasks | 5 | GLM-5 (cloud) | $0 |
| Heartbeats | 48 | Llama 3.1 8B (local) | $0 |
| **Total** | | | **~$0/day** |

#### Developer (Medium Usage)

| Activity | Daily Volume | Model | Daily Cost |
|----------|--------------|-------|------------|
| Code reviews | 10 | Claude Sonnet | $3.00 |
| Debugging | 5 | Claude Sonnet | $1.50 |
| Documentation | 3 | GPT-5.2 | $1.50 |
| Quick tasks | 50 | Llama 3.1 8B (local) | $0 |
| **Total** | | | **~$6/day** |

#### Power User with Optimization

| Activity | Daily Volume | Model | Daily Cost |
|----------|--------------|-------|------------|
| All tasks | 100+ | Mixed strategy | $5-15 |
| With caching enabled | 100+ | Optimized | $2-5 |
| Using local models | 80% | Ollama | $0 |
| **Total (optimized)** | | | **~$3/day** |

### Troubleshooting

#### High Costs

**Problem**: Unexpected API costs
```bash
# Check which model is being used
openclaw status

# Review recent expensive sessions
jq -r 'select(.message.usage.cost.total > 0.5) | "\(.timestamp): $\(.message.usage.cost.total)"' \
  ~/.openclaw/agents/default/sessions/*.jsonl | tail -20

# Switch to local model temporarily
/model llama3.1:8b
```

#### Cache Not Working

**Problem**: Cache hit rate is low
```bash
# Check if system prompts are stable
diff SOUL.md.bak SOUL.md

# Ensure skill ordering is consistent
openclaw config get skills.load.order

# Verify cache configuration
openclaw config get models.providers.anthropic.cache
```

#### Ollama Connection Issues

**Problem**: Cannot connect to Ollama
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
sudo systemctl restart ollama

# Check logs
journalctl -u ollama -f
```

---

**Estimated Setup Time**: 2-3 hours for Ollama + configuration
**Monthly Cost Range**: $0-50 (depending on usage and strategy)
**Break-even for Local Hardware**: 6-18 months vs cloud-only
