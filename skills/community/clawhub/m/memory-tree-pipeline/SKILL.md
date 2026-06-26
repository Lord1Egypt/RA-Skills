---
name: memory-tree-pipeline
version: 1.0.0
description: "Three-scope structured memory for AI agents. Automatically organize, summarize, and index agent memory with sealing workers and topic extraction."
license: MIT
tags: [memory, agent-memory, structured-memory, topic-extraction, summarization, context-management]
source: el-rudo-larios/memory-tree
trigger: "agent memory structured memory topic extraction summarization pipeline"
metadata:
  openclaw:
    emoji: "🌳"
---

# Memory Tree — Three-Scope Structured Memory

A structured memory system with three scopes (source, topic, global) that automatically organizes, summarizes, and indexes agent memory. Never lose context again.

## Architecture

```
Source (raw) → Topic (summarized) → Global (cross-topic knowledge)
   134 files         13 files              6 files
```

## Quick Start

```python
from memory_tools import MemoryTools

tools = MemoryTools(workspace="/path/to/workspace")

# Store a memory
tools.store("User prefers dark mode for all UI", topic_hint="preferences")

# Recall memories
results = tools.recall("dark mode", scope="global")

# Seal source → topic summaries
tools.seal()

# Check status
status = tools.status()
# → {"source_files": 134, "topic_files": 13, "global_files": 6}
```

## Features

- **Three-scope hierarchy**: Source → Topic → Global
- **Automatic sealing**: Raw memories compressed into topic summaries
- **Topic extraction**: Automatic categorization by content
- **Index management**: Full-text search across all scopes
- **Budget enforcement**: Topic files < 2000 tokens, Global < 5000 tokens
- **Idempotent sealing**: Safe to run multiple times

## Testing

```bash
python -m pytest test_memory_tree.py -v
# 15 tests passing
```

## License

MIT
