---
name: smart-router
description: Intelligent task routing between local and cloud Ollama LLM instances. Use when the user wants cost-efficient AI responses by routing simple tasks to a local Ollama model and complex tasks to a more powerful remote/cloud Ollama instance. Automatically classifies task complexity, detects system capabilities, and delegates to the appropriate model tier. Use for any request where you want to balance latency vs capability, or when explicitly asked to use smart routing, local-first routing, or Ollama model selection.
---

# Smart Router

Routes tasks between a local Ollama instance (fast, cheap) and a remote/cloud Ollama instance (more capable) based on task complexity classification and system capabilities.

## Quick Start

```bash
# 1. Profile your system
python scripts/system_profiler.py

# 2. Check endpoints are healthy
python scripts/health_check.py

# 3. Route a task
python scripts/route.py "What is quantum computing?"
```

## How It Works

```
User Request
    ↓
System Profiler (detects compatible models)
    ↓
Health Check (verifies endpoints are up)
    ↓
Classify Task (1-5 complexity score)
    ↓
├─ Score 1-2 → Local Ollama (fast, cheap)
├─ Score 3-5 → Cloud Ollama (powerful)
└─ Match specialist → Dedicated model
    ↓
Verify model available (fallback if not)
    ↓
Stream Response
```

## Classification Scale

| Score | Complexity | Examples | Routed To |
|-------|------------|----------|-----------|
| 1 | Simple | "What is 2+2?", "Define entropy" | Local |
| 2 | Basic | "Write hello world in Python" | Local |
| 3 | Complex | "Debug this error", "Compare X vs Y" | Cloud |
| 4 | Deep | "Design a system", "Research topic" | Cloud |
| 5 | Expert | "Build from scratch", "Multi-file project" | Cloud |

## File Structure

```
smart-router/
├── SKILL.md                          # This file
├── __init__.py                       # Python package interface
├── requirements.txt                    # Dependencies
│
├── config/
│   ├── router.yaml                   # Main configuration
│   └── system_profile.json            # Auto-generated system specs
│
├── scripts/
│   ├── classify.py                   # Task complexity classifier
│   ├── execute.py                    # Ollama API client
│   ├── route.py                      # Main routing logic
│   ├── system_profiler.py            # Hardware detection
│   └── health_check.py               # Endpoint health verification
│
├── tests/
│   └── test_classifier.py            # Test suite
│
└── references/
    └── classifier-prompt.txt         # LLM fallback prompt
```

## Configuration

Edit `config/router.yaml`:

```yaml
# Local Ollama (your machine)
local:
  model: "llama3.2"
  base_url: "http://localhost:11434"

# Cloud Ollama (remote server)
cloud:
  model: "qwen2.5:14b"
  base_url: "http://192.168.1.100:11434"

# Tasks scoring >= this go to cloud
threshold: 3

# Domain specialists (checked first)
specialists:
  code:
    model: "codellama:34b"
    base_url: "http://192.168.1.100:11434"
    triggers: ["code review", "refactor"]

# Performance settings
performance:
  timeout_seconds: 60
  stream_responses: true
  retry_attempts: 2

# Caching
cache:
  enabled: true
  db_path: "cache/router.db"
  ttl_seconds: 86400
```

## Usage

### CLI

```bash
# Basic routing
python scripts/route.py "What is the capital of France?"

# With profiling (updates system profile)
python scripts/route.py "Debug this error" --profile

# Custom config
python scripts/route.py "Design a system" --config config/my-router.yaml

# No streaming (wait for full response)
python scripts/route.py "Summarize this" --no-stream

# Health check all endpoints
python scripts/health_check.py

# Manual classification
python scripts/classify.py "Write a function"
# Output: "2:basic-task"
```

### Python API

```python
from smart_router import SmartRouter

# Initialize
router = SmartRouter()

# Route with streaming
for chunk in router.route("Explain quantum computing"):
    print(chunk, end='')

# Classify only
score, reason = router.classify("Debug this code")
print(f"Complexity: {score}/5, Reason: {reason}")

# Get configuration
config = router.get_config()
print(f"Local model: {config['local']['model']}")
```

## Workflow

### 1. System Profiling

Run once (or when hardware changes):
```bash
python scripts/system_profiler.py
```

This creates `config/system_profile.json` with:
- Total/available RAM
- GPU detection (VRAM, name)
- CPU cores
- Compatible model list
- Recommended local model

### 2. Health Check

Verify endpoints before use:
```bash
python scripts/health_check.py
```

Checks:
- Ollama version
- Available models
- Response latency
- Connection status

### 3. Routing

When you submit a task:
1. **Specialist check** — Match against specialist triggers
2. **Classification** — Pattern-based scoring (1-5)
3. **Model selection** — Local (1-2) or Cloud (3-5)
4. **Availability check** — Verify model exists in Ollama
5. **Fallback** — Use compatible model if preferred unavailable
6. **Execution** — Stream response from selected model

## Features

### Pattern-Based Classification

Uses regex patterns (not LLM calls) for speed:
- **30ms** classification time
- **0 tokens** cost
- Handles false positives ("zip code" ≠ code task)

### System-Aware Model Selection

Automatically detects what your system can run:
- No GPU → Filters to CPU-compatible models
- 8GB RAM → Excludes 70B models
- GPU available → Prioritizes GPU-accelerated models

### Health Monitoring

Pre-flight checks prevent routing to dead endpoints:
```bash
✓ local     | Status: healthy | Latency: 45ms | Models: 5
✗ cloud     | Status: unreachable | Error: Connection refused
```

### Automatic Fallbacks

1. **Model fallback** — If configured model unavailable, picks compatible alternative
2. **Endpoint fallback** — If cloud fails, retries with local
3. **Error handling** — Never crashes, always returns something

### Cost Tracking

Even though Ollama is free, logs track latency:
```
[2024-01-15T10:30:00] task: '...' -> local | model: llama3.2 | latency: 0.85s
[2024-01-15T10:30:45] task: '...' -> cloud | model: qwen2.5:14b | latency: 3.2s
```

## Testing

```bash
# Run classifier tests
python tests/test_classifier.py

# Expected output:
# ✓ PASS [1] Simple factual question
# ✓ PASS [1] Zip code (not code)
# ✓ PASS [3] Debugging
# ...
# Results: X passed, Y failed
```

## Troubleshooting

### "Cannot connect to Ollama"
```bash
# Check if Ollama is running
ollama serve

# Verify endpoint
curl http://localhost:11434/api/tags
```

### "Model not found"
```bash
# Pull the model
ollama pull llama3.2

# Or let router auto-fallback to available model
```

### "Classification seems wrong"
Check pattern in `scripts/classify.py`:
```python
# Add new pattern
COMPLEXITY_PATTERNS[2].append(r'your\s+pattern\s+here')
```

### "Cloud endpoint slow"
```yaml
# In config/router.yaml
performance:
  timeout_seconds: 30  # Reduce timeout
```

## Requirements

- Python 3.8+
- Ollama (local or remote)
- `pip install -r requirements.txt`

## Architecture Decision Records

### Why Pattern Matching vs LLM?

| Approach | Latency | Cost | Accuracy | Verdict |
|----------|---------|------|----------|---------|
| Pattern matching | 30ms | 0 tokens | 90% | ✅ Used |
| LLM classification | 500ms | 50 tokens | 95% | Optional (`--llm`) |

Pattern matching wins on speed/cost. Accuracy is good enough for routing.

### Why Not Cloud APIs (Claude, GPT-4)?

Ollama-only keeps everything:
- **Private** — No data leaves your infrastructure
- **Free** — Server costs only, no per-token fees
- **Customizable** — Run fine-tuned models

## Future Enhancements

- [ ] Adaptive threshold learning from feedback
- [ ] Conversation context (multi-turn routing)
- [ ] Cost/latency budget enforcement
- [ ] Automatic model downloading
- [ ] Metrics dashboard
