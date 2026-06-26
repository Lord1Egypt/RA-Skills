---
name: grantai-memory
description: Persistent memory for OpenClaw agents. Exact recall in milliseconds - your agent remembers everything across sessions.
version: 1.3.0
metadata:
  openclaw:
    requires:
      bins:
        - grantai-mcp
    emoji: "\U0001F9E0"
    homepage: https://solonai.com/grantai/integrations/openclaw
---

# GrantAi Memory

**Persistent memory for your OpenClaw agent. Never hit context limits again.**

Your agent remembers everything - from 1 minute ago to 5 years ago. Exact recall in milliseconds.

## Free for OpenClaw Users

GrantAi Memory is **free** for OpenClaw users - automatic activation, no license key required.

## The Problem

OpenClaw agents hit context window limits mid-task, forget everything, and start from scratch.

## The Solution

GrantAi gives your agent **exact recall in milliseconds**:
- Memory persists across sessions
- Works outside the context window
- 100% local - data never leaves your machine
- AES-256 encrypted at rest

## Installation

Download from [solonai.com/grantai/download](https://solonai.com/grantai/download)

- **macOS**: .pkg installer
- **Windows**: GUI installer (.exe)
- **Linux**: .tar.gz package
- **Docker**: `ghcr.io/solonai-com/grantai-memory:1.8.6`

## Configuration

Add to your OpenClaw config:

```yaml
mcp:
  grantai:
    command: grantai-mcp
```

Or with Docker:

```yaml
mcp:
  grantai:
    command: docker
    args:
      - run
      - -i
      - --rm
      - -v
      - grantai-data:/data
      - ghcr.io/solonai-com/grantai-memory:1.8.6
```

## Tools

| Tool | Description |
|------|-------------|
| `grantai_infer` | Query memory (use FIRST before file searches) |
| `grantai_teach` | Store information for future recall |
| `grantai_learn` | Import files/directories into memory |
| `grantai_summarize` | Save session summaries |
| `grantai_project` | Track project state across sessions |
| `grantai_snippet` | Store code snippets with context |
| `grantai_capture` | Capture conversation turns verbatim |
| `grantai_git` | Import git commit history |
| `grantai_health` | Check memory system status |
| `grantai_savings` | View token savings statistics |

## Usage Examples

**Store a decision:**
```
Remember that we decided to use JWT for authentication
```

**Recall it later:**
```
What did we decide about authentication?
→ Returns exact decision in milliseconds
```

**Import codebase:**
```
Learn the src/ directory
```

## Support

- Docs: [solonai.com/grantai/integrations/openclaw](https://solonai.com/grantai/integrations/openclaw)
- Email: support@solonai.com

---

[SolonAI](https://solonai.com)
