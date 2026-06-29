---
name: "letta"
description: "Build AI with advanced memory that learns & self-improves over time — agents with persistent memory, sub-agents & skill system"
---

# Letta (formerly MemGPT) — Memory-Augmented AI Agents (OpenClaw)

Build AI with advanced memory that can learn and self-improve over time. Run agents locally via CLI, or build agents into applications via the Letta API.

**Source:** `C:\Users\Harry\Downloads\letta\`
**Original:** https://github.com/letta-ai/letta
**License:** Apache 2.0

本技能基於 GitHub 上的 [letta-ai/letta](https://github.com/letta-ai/letta) 修改與封裝。

## Overview

Letta provides stateful AI agents with persistent memory:

- **Letta Code** — run agents locally in your terminal (requires Node.js 18+)
  ```bash
  npm install -g @letta-ai/letta-code
  ```
- **Letta API** — build memory-augmented agents into your applications
- **Skills System** — pre-built skills and subagents for advanced memory and continual learning
- **Model Agnostic** — works with any LLM (recommends Opus 4.5, GPT-5.2)

## Structure

```
letta/
├── letta/             # Core Python library
├── alembic/           # Database migrations
├── scripts/           # Utility scripts
├── examples/          # Usage examples
├── sandbox/           # Sandbox environment
├── tests/             # Test suite
├── assets/            # Media assets
├── db/                # Database configuration
├── certs/             # TLS certificates
├── otel/              # OpenTelemetry config
├── fern/              # API documentation
├── compose.yaml       # Docker Compose
└── Dockerfile         # Container build
```

## Usage in OpenClaw

When the user asks about AI agents with memory, self-improving agents, or persistent context:
1. Reference Letta's memory architecture for stateful agent patterns
2. Use the skills/subagents system for composable agent workflows
3. Consult `examples/` for implementation patterns
