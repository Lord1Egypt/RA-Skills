---
name: "protea-Self-evolving life agent"
description: >
  Self-evolving artificial life agent. Three-ring architecture: Ring 0 (Sentinel) supervises,
  Ring 1 (Intelligence) drives LLM-powered evolution, Ring 2 (Evolvable Code) is the living program
  that self-restructures, self-reproduces, and self-evolves. Supports Anthropic, OpenAI, DeepSeek,
  and Qwen as LLM providers. Includes fitness scoring, gene pool inheritance, tiered memory,
  skill crystallization, Telegram bot, and web dashboard.
---

# Protea — Self-Evolving Artificial Life Agent

A living program that evolves itself. Three-ring architecture running on a single machine.

## Architecture

- **Ring 0 (Sentinel)** — Immutable physics layer. Heartbeat monitoring, git snapshots, rollback, fitness tracking. Pure Python stdlib.
- **Ring 1 (Intelligence)** — LLM-driven evolution engine, task executor, Telegram bot, skill crystallizer, web dashboard. Multi-LLM support (Anthropic, OpenAI, DeepSeek, Qwen).
- **Ring 2 (Evolvable Code)** — The living code that evolves, managed in its own git repo by Ring 0.

## Prerequisites

- Python 3.11+
- Git
- At least one LLM API key (Anthropic, OpenAI, DeepSeek, or Qwen)

## Quick Start

```bash
curl -sSL https://raw.githubusercontent.com/EdisonChenAI/protea/main/setup.sh | bash
cd protea && .venv/bin/python run.py
```

## Key Features

- **Self-Evolution** — LLM generates code mutations each generation; survivors kept, failures roll back
- **Fitness Scoring** — 6-component scoring (survival, output, diversity, novelty, structure, function)
- **Gene Pool** — Top 100 code patterns stored in SQLite, injected into evolution prompts
- **Tiered Memory** — Hot → Warm → Cold → Forgotten, with LLM-assisted curation
- **Skill Crystallization** — Surviving code patterns extracted as reusable skills
- **Multi-LLM** — Anthropic, OpenAI, DeepSeek, Qwen via unified interface
- **Telegram Bot** — Commands + free-text interaction
- **Web Dashboard** — Local UI at localhost:8899
- **1098 Tests** — Comprehensive coverage

## Source

GitHub: https://github.com/EdisonChenAI/protea
