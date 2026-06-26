---
name: memory-lancedb-setup
description: Configure OpenClaw's memory-lancedb plugin for semantic vector memory using a local LanceDB database. Use when: (1) setting up vector memory for the first time, (2) memory-lancedb fails with module not found errors, (3) migrating from flat-file MEMORY.md to vector-based recall, (4) configuring an embedding provider (Gemini, OpenAI-compatible). NOT for: general memory_store/memory_recall usage (just use the tools directly).
---

# memory-lancedb Setup

Enables semantic vector memory in OpenClaw: memories stored with `memory_store` are embedded and indexed locally, then recalled on-demand via `memory_recall` — no full-context load.

## Prerequisites

- OpenClaw installed at `/usr/local/lib/node_modules/openclaw`
- An OpenAI-compatible embedding API key (Gemini AI Studio free key works well)

## Setup Steps

### 1. Get a Gemini API Key (free)

Go to [aistudio.google.com](https://aistudio.google.com) → Get API key → Create API key.

### 2. Configure the plugin

```bash
openclaw config set plugins.entries.memory-lancedb.enabled true
openclaw config set plugins.entries.memory-lancedb.config.embedding.baseUrl "https://generativelanguage.googleapis.com/v1beta/openai/"
openclaw config set plugins.entries.memory-lancedb.config.embedding.model "text-embedding-004"
openclaw config set plugins.entries.memory-lancedb.config.embedding.apiKey "YOUR_API_KEY"
openclaw config set plugins.entries.memory-lancedb.config.embedding.dimensions 768
```

### 3. Install dependencies

```bash
# Step 1: install main package in openclaw root
cd /usr/local/lib/node_modules/openclaw
npm install @lancedb/lancedb

# Step 2: install platform-specific native binding in plugin dir
cd /usr/local/lib/node_modules/openclaw/extensions/memory-lancedb
npm install @lancedb/lancedb-darwin-arm64   # Apple Silicon (arm64)
# npm install @lancedb/lancedb-darwin-x64   # Intel Mac
# npm install @lancedb/lancedb-linux-x64-gnu  # Linux x64
```

### 4. Patch native.js (Apple Silicon only)

LanceDB's `native.js` tries x64 first, hits `break` on failure, and never reaches arm64. Run the patch script:

```bash
python3 ~/.openclaw/workspace/skills/memory-lancedb-setup/references/patch_native.py
```

### 5. Restart gateway and verify

```bash
openclaw gateway restart
```

Then test:
```
memory_store → should return: Stored: "..."
memory_recall → should return matching entries with similarity %
```

## Migrating from MEMORY.md

If MEMORY.md is large, migrate key facts to the vector store and shrink MEMORY.md to a 20-30 line index. Group by topic and call `memory_store` for each:

- Identity & permissions
- Execution rules
- Project configurations (cron IDs, doc tokens)
- Technical knowledge (API quirks, field names)
- Workflows and SOPs

Keep only "must-know-every-session" rules in MEMORY.md.

## Troubleshooting

See `references/troubleshooting.md` for common errors and fixes.
