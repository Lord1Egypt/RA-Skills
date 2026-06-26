# Model Info Skill ??

Get **100% accurate, real-time** AI model information directly from OpenClaw's session status. Never guess which model you're using - this skill tells you exactly what's running.

---

## ? Features

- ? **Real-time Model Detection** - Current model name (full ID)
- ? **Provider Identification** - Know exactly which API (Nvidia, OpenRouter, etc.)
- ? **Session Status** - Active session info, runtime details
- ? **Token Usage** - Input/output tokens, cost tracking
- ? **Configuration** - Think mode, elevated status, queue depth
- ? **Zero Dependencies** - Uses built-in `session_status` command
- ? **100% Accurate** - Pulls from system's official status

---

## ?? Usage

Simply ask me:

- `"model info"` ? Full details
- `"what model"` ? Quick model name
- `"model status"` ? Session status
- `"which AI"` ? Provider info

---

## ?? What You Get

```
Model: stepfun-ai/step-3.5-flash
Provider: Nvidia (custom__ceacf5ff)
API: nvapi-… (from models.json)
Tokens: 154k in / 3.4k out
Cost: $0.0000
Context: 56k/200k (28%)
Runtime: Direct · Think: off
Queue: collect (depth 0)
```

---

## ??? Installation

Automatic discovery - just place in `skills/model-info/` folder. No external dependencies.

---

## ?? Accuracy Guarantee

This skill uses OpenClaw's **official `session_status`** command - the same system that tracks your runtime. It's not guessing or inferring; it's reporting what the system knows. **Zero chance of error.**

---

**Skill Name:** model-info  
**Version:** 1.0.0  
**Author:** AutoClaw  
**License:** MIT
