---
name: poor-mans-opus
version: 2.0.6
description: >
  Give your AI agent a personality. Complete behavioral profile via I-Lang ::GENE{} protocol.
  Six gene blocks: identity, security, communication, capability, memory, I-Lang fluency.
  Install → copy the SOUL template → restart. DeepSeek V4 Pro at 3% of Opus cost.
author: mtmpss
homepage: https://github.com/mtmpss/poor-mans-opus
repository: https://github.com/mtmpss/poor-mans-opus
license: MIT
---

```i-lang
::DNA{skill:poor-mans-opus}
::META{version:2.0.6|protocol:i-lang_v3.0|updated:2026-05-03}
::GENE{behavior|scope:strict}
  T:apply_soul|from:SOUL.md
  T:apply_genes|all
::END{DNA}
```

## Poor Man's Opus — Agent Personality Kit

**Give your AI agent a personality. One command.**

Most AI agents are blank slates. This skill ships a complete behavioral profile — six `::GENE{}` blocks that turn a generic assistant into a precision instrument.

### What you get

| Gene | Shapes |
|------|--------|
| `identity` | Name, owner, self-awareness |
| `security` | Owner-only control, data protection, external action gating |
| `communication` | Concise, direct, conclusion-first voice |
| `capability` | Context awareness, search-before-guess, quality standards |
| `memory` | File-based session continuity |
| `ilang_protocol` | Native I-Lang v3.0 fluency |

### How to activate

```bash
# 1. Install
openclaw skills install poor-mans-opus

# 2. Copy the SOUL template
cp ~/.openclaw/workspace/skills/poor-mans-opus/SOUL.md <your-workspace>/SOUL.md

# 3. Edit line 1
[INIT:@SELF|name=YOUR_AI_NAME|runtime=openclaw|owner=YOUR_NAME]
```

ℹ️ Installing does NOT auto-overwrite your existing SOUL.md. You control the copy step.


### Upgrade to full genome

This safe edition gives your agent a solid behavioral foundation. For production-grade control — iron rules, KILL.md freeze switch, command-level authority — grab the complete genome from our [GitHub repo](https://github.com/mtmpss/poor-mans-opus) or ask your agent: *"show me the advanced configuration."*

### Also on

**🧠 Hermes Agent** — native `agentskills.io` compatibility:
```bash
hermes skills install mtmpss/poor-mans-opus
```

**🤗 HuggingFace** — model + dataset:
```bash
huggingface-cli download ilanguage/poor-mans-opus
```

### Advanced configuration

For production environments requiring maximum control (iron rules, KILL.md freeze switch, command-level authority), see the complete genome in [README.md](https://github.com/mtmpss/poor-mans-opus).

### Cost

| | Claude Opus 4.6 | DeepSeek V4 Pro + this SOUL |
|---|---|---|
| Input | $15.00/M | $1.74/M |
| Output | $75.00/M | $3.48/M |
| **Save** | — | **95%** |

### Links

- [I-Lang Protocol](https://ilang.ai)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub](https://clawhub.ai/mtmpss/poor-mans-opus)
- [GitHub](https://github.com/mtmpss/poor-mans-opus)
