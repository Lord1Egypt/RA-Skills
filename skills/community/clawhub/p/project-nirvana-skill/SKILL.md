---
name: project-nirvana-skill
description: Privacy-preserving context stripper for OpenClaw. Strip SOUL/USER/MEMORY before cloud API calls. Assumes you have your own local LLM. Saves 85%+ tokens, protects privacy.
version: "1.0.0"
author: Shiva
compatibility: "OpenClaw 2026.3.24+"
keywords: [privacy, context-stripping, local-llm, cost-reduction, privacy-preserving, context-management]
---

# Nirvana Local: Privacy-Preserving Context Stripper

> **For teams that already have a local inference engine.** Just strip the private data before cloud API calls. Nothing else.

---

## What This Is

Nirvana Local is a lightweight skill for OpenClaw agents that **already have** a local LLM inference engine (Ollama, Llamafile, vLLM, LM Studio, etc.).

It does one thing: **strips private context before cloud API calls.**

- ✅ Removes SOUL.md (agent identity)
- ✅ Removes USER.md (user personal data)
- ✅ Removes MEMORY.md (agent memories)
- ✅ Removes chat history (your actual questions)
- ✅ Leaves only the task at hand
- ✅ Logs every boundary crossing (audit trail)

---

## Why You Need This

### Today: Privacy Leak

When you ask your agent a question, the full system prompt goes to cloud:

```
Your question: "How do I build synbio?"

System prompt sent to OpenAI:
- Agent identity (SOUL.md)
- Your personal info (USER.md)
- Agent memories (MEMORY.md)
- Full chat history
- Everything costs 2,000–5,000 extra tokens
```

### With Nirvana Local: Protected

```
Your question: "How do I build synbio?"

Query to local LLM first:
- Try local inference (free)
- If local fails, ask the cloud

Cloud API call (if needed):
- Original question: [STRIPPED]
- System prompt: [STRIPPED]
- Sanitized query: "How do I build synbio?" (no context)
- Cloud never sees: SOUL, USER, MEMORY, chat history
- Cost: $0.01–$0.03 (no context overhead)
```

---

## Installation

### Prerequisites
- OpenClaw 2026.3.24+
- Your own local LLM running at any endpoint (Ollama, vLLM, LM Studio, etc.)

### Setup (3 minutes)

```bash
# 1. Install skill
clawhub install shivaclaw/nirvana-local

# 2. Configure your local LLM endpoint
openclaw nirvana-local configure \
  --local-endpoint http://localhost:11434 \
  --local-model qwen2.5:7b

# 3. Verify
openclaw nirvana-local status

# Output:
# ✅ Local LLM: qwen2.5:7b @ localhost:11434
# ✅ Privacy audit: enabled
# ✅ Context stripper: active
```

---

## How It Works

### Routing Decision Logic

```
Agent receives your question
    ↓
Try local LLM first
(qwen2.5:7b, Mistral, Llama, whatever you have)
    ↓
┌─────────────────────────────────────────┐
│ Success?                                 │
└─────────────────────────────────────────┘
   ↙ YES (80%)           ↘ NO (20%)
   
Return local answer    Ask cloud for help
                             ↓
                    Strip private context
                    (SOUL, USER, MEMORY)
                             ↓
                    Sanitized query to cloud
                    "How do I build synbio?"
                    (no personal data)
                             ↓
                    Cache response locally
                    Agent learns
                             ↓
                    Return integrated answer
```

### What Gets Stripped

✅ **Always Removed:**
- SOUL.md (agent identity)
- USER.md (personal data)
- MEMORY.md (agent memories)
- Chat history (your actual questions)
- Session context (private workstreams)

✅ **What the Cloud Gets:**
- Sanitized query only
- Task-specific information
- Audit trail (transparent logging)

---

## Configuration

### Basic Setup

Edit `~/.openclaw/workspace/openclaw.json`:

```json
{
  "plugins": {
    "nirvana-local": {
      "enabled": true,
      "local_llm": {
        "endpoint": "http://localhost:11434",
        "model": "qwen2.5:7b",
        "timeout_ms": 180000,
        "api_format": "openai-compatible"
      },
      "privacy": {
        "strip_soul": true,
        "strip_user": true,
        "strip_memory": true,
        "strip_chat_history": true,
        "audit_logging": true
      },
      "routing": {
        "local_threshold": 0.75,
        "max_local_context_tokens": 8000,
        "cloud_fallback": true
      }
    }
  }
}
```

### Custom API Format

If your local LLM uses a different API:

```json
{
  "plugins": {
    "nirvana-local": {
      "local_llm": {
        "endpoint": "http://your-server:5000",
        "model": "your-model",
        "api_format": "custom",
        "custom_api_handler": "llamafile"  // or "vllm", "lm-studio", etc.
      }
    }
  }
}
```

---

## Privacy Audit Trail

### View What Gets Stripped

```bash
# See every boundary crossing
openclaw nirvana-local audit-log --tail 20

# Output:
# [2026-04-24 14:23:45] LOCAL HANDLING
# Question: "What's my salary range for synbio roles?"
# Handled by: qwen2.5:7b locally
# Private data: None exposed
# Cost: $0

# [2026-04-24 14:25:12] CLOUD FALLBACK (WITH STRIPPING)
# Original question: [STRIPPED]
# Sanitized query sent: "What are typical salary ranges in synthetic biology?"
# Private data stripped: SOUL.md, USER.md, chat history
# Cost: $0.02
```

### Transparency

Every cloud API call is logged with:
- What was stripped
- What was sent
- What was cached
- Cost incurred
- Privacy boundary verified

---

## Supported Local LLMs

| Provider | Endpoint | API Format | Tested |
|----------|----------|-----------|--------|
| **Ollama** | `http://localhost:11434` | openai-compatible | ✅ |
| **Llamafile** | `http://localhost:8000` | openai-compatible | ✅ |
| **vLLM** | `http://localhost:8000` | openai-compatible | ✅ |
| **LM Studio** | `http://localhost:1234` | openai-compatible | ✅ |
| **Text Generation WebUI** | `http://localhost:5000` | custom | ✅ |
| **GPT4All** | `http://localhost:4891` | custom | ✅ |
| **LocalAI** | `http://localhost:8080` | openai-compatible | ✅ |

---

## Philosophy

**You own the learning. The cloud provides intelligence.**

Without Nirvana Local:
- Cloud provider learns from your private data every time you ask a question
- You train their next model
- Your personal information becomes their training corpus
- You pay for the privilege

With Nirvana Local:
- Your local agent learns from cloud responses
- Your private data never leaves your system
- Cloud provider learns nothing about you
- You own all the knowledge

---

## Cost Savings

### Example: 10 Questions/Day

**Today (without Nirvana Local):**
- 2,000 tokens/question (full context sent)
- 20,000 tokens/day
- $0.60/day (OpenAI GPT-4)
- $18/month
- Privacy: Compromised

**With Nirvana Local:**
- 80% local (free, private)
- 20% cloud (sanitized, no context overhead)
- 300 tokens/question average
- 3,000 tokens/day
- $0.09/day
- $2.70/month
- Privacy: Protected

**Savings: $15.30/month + 100% privacy protection**

---

## When to Use

### ✅ Perfect For
- Agents with local LLMs already running
- Privacy-critical deployments (code, healthcare, legal, finance)
- Cost-conscious teams (85% savings)
- Air-gapped environments (local + selective cloud)

### ⚠️ When to Use Full Plugin
- Need automated Ollama + model setup
- No local LLM currently available
- Want out-of-box simplicity

---

## Support

- **GitHub:** [ShivaClaw/nirvana-skill](https://github.com/ShivaClaw/nirvana-skill)
- **Issues:** [GitHub Issues](https://github.com/ShivaClaw/nirvana-skill/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ShivaClaw/nirvana-skill/discussions)

---

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

*Your privacy is yours to keep. Nirvana Local makes it happen.*
