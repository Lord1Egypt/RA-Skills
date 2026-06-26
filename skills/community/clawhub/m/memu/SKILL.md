---
name: memu
description: >
  Persistent memory infrastructure for 24/7 agents. Replaces flat-file memory
  with a three-layer architecture (Resource → Memory Item → Memory Category)
  that reduces token costs by 70-90% and enables proactive context retrieval.
  Built on NevaMind AI's open-source memU framework (v1.4.0).
  92.09% accuracy on LoCoMo benchmark.
version: 1.0.0
author: ProjectSnowWork
homepage: https://github.com/NevaMind-AI/memU
license: AGPL-3.0
tags:
  - agent-memory
  - long-term-context
  - proactive-agents
  - token-optimization
  - memory-infrastructure
  - pgvector
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
      bins:
        - python3
      primaryEnv: OPENAI_API_KEY
---

# memU: Persistent Memory for 24/7 Agents

You are integrating memU, an open-source memory framework by NevaMind AI, into an agent that needs to remember, learn, and act proactively across long-running sessions.

## When to Use This Skill

Use memU when the agent needs to:

- Retain and retrieve information across sessions spanning days, weeks, or months
- Reduce token costs from injecting raw conversation history into context (70-90% reduction)
- Act proactively — surface relevant context before the user explicitly asks
- Process multi-modal inputs (conversations, documents, images, logs) into structured memory
- Distinguish between current and outdated information with temporal awareness

Do NOT use memU for:

- Single-session chatbots that don't need persistence
- Simple key-value storage (use a database directly)
- Real-time streaming memory (not yet supported)

## Core Concepts

memU organizes memory in three layers:

1. **Resources** — Raw, immutable inputs (conversations, documents, images). The ground truth.
2. **Memory Items** — Extracted atomic facts with timestamps, provenance, and confidence scores. Queryable and versioned.
3. **Memory Categories** — Emergent clusters that self-organize as items accumulate. Enable broad context retrieval.

Two retrieval strategies are available:

- **Embedding (RAG)** — Vector similarity search. Fast (50-150ms). Best for factual recall.
- **LLM** — Deep semantic reasoning over memory files. Slower (500-2000ms). Best for nuanced, cross-category queries.

## Installation

```bash
pip install memu-py
```

Optional persistent storage:

```bash
docker run -d --name memu-postgres \
  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=memu -p 5432:5432 pgvector/pgvector:pg16
```

## Minimal Integration

```python
import asyncio
from memu import MemoryService

service = MemoryService(
    llm_profiles={
        "default": {
            "provider": "openai",
            "base_url": "https://api.openai.com/v1",
            "api_key": "sk-your-key",
            "chat_model": "gpt-4o-mini",
            "embed_model": "text-embedding-3-small",
        }
    }
)

# Store
await service.memorize(
    resource_payload=[{"role": "user", "content": "I deploy on Tuesdays."}],
    modality="conversation",
)

# Retrieve
results = await service.retrieve(
    query=[{"role": "user", "content": "When should we deploy?"}],
    method="embedding",
)
```

## Included Files

- **README.md** — Full architecture explanation, 3 real-world scenarios, cost/performance tables, integration guides, troubleshooting
- **FAQ.md** — 10 high-frequency questions with detailed answers
- **RELEASE.md** — Release announcement
- **METADATA.yaml** — ClawHub form metadata
- **examples/** — 4 complete, runnable Python scripts:
  - `example_1_minimal.py` — In-memory mode, no database
  - `example_2_openclaw_integration.py` — Replace OpenClaw default memory
  - `example_3_production.py` — Logging, retries, metrics
  - `example_4_scenarios.py` — Research assistant, email triage, system monitoring

## Attribution

This is a community Skill packaging the official [memU](https://github.com/NevaMind-AI/memU) project by [NevaMind AI](https://github.com/NevaMind-AI). It does not modify or extend memU's code.
