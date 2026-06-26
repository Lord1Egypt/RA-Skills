---
name: hedgehog-memory
description: Radial memory architecture for AI agents — infinite persistent memory with hierarchical compression. Never deletes, only compresses. Origin always in context. pip install hedgehog-memory.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python
    envVars:
      - name: OPENAI_API_KEY
        required: false
        description: OpenAI API key for quality LLM-based summarization. Falls back to built-in keyword summarizer if not set.
      - name: HEDGEHOG_MEMORY_PATH
        required: false
        description: Directory to store memory files. Defaults to ./memory_store in the working directory.
---

# HedgehogMemory

HedgehogMemory gives AI agents **infinite persistent memory** using a radial compression architecture. Memory is organized as Lines of Nodes — each Node stores the same content at 5 abstraction levels (L0–L4). The L0 one-liner of every node is always loaded at session start (~200 tokens total), so the agent always knows what it knows.

**Key guarantee:** Memory is NEVER deleted. Old context is only compressed into smaller abstractions. The verbatim original is always recoverable at L4.

## Installation

```
pip install hedgehog-memory
pip install "hedgehog-memory[openai]"   # with OpenAI summarizer (recommended)
```

## Abstraction Levels

| Level | Max length | Use case |
|-------|-----------|----------|
| L0 | 80 chars | One-liner, always in context |
| L1 | 200 chars | Navigation preview |
| L2 | 600 chars | Detailed summary |
| L3 | 1800 chars | Full context summary |
| L4 | unlimited | Verbatim original |

## Quick Start

```python
from radial_memory import ContextWindowManager
import os

mgr = ContextWindowManager(
    base_path=os.environ.get("HEDGEHOG_MEMORY_PATH", "./memory_store")
)

# SESSION START: get ~200-token origin overview (all L0 summaries)
overview = mgr.reset()
print(overview)  # inject this into your system prompt

# LOAD: find relevant past context by query
result = mgr.load("Python async patterns")
if result.found:
    print(result.content)   # L1 summary by default
    result = result.drill_deeper()     # go to L2
    full = result.load_full_state()    # get verbatim original (L4)

# COMMIT: save current session to memory
mgr.commit(
    topic="Async Python debugging session",
    full_context="Complete session transcript goes here...",
    tags=["python", "async", "debugging"]
)
```

## With OpenAI Summarizer (recommended for quality)

```python
from radial_memory import ContextWindowManager
from radial_memory.summarizer import OpenAISummarizer
import os

summarizer = OpenAISummarizer(
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-4o-mini"
)
mgr = ContextWindowManager(
    base_path=os.environ.get("HEDGEHOG_MEMORY_PATH", "./memory_store"),
    summarizer=summarizer
)
```

## Agent Workflow Pattern

Apply this pattern every session:

```python
# 1. SESSION START
overview = mgr.reset()
# overview = all L0 one-liners for every stored node (~200 tokens)
# Inject overview into your system prompt / context window

# 2. QUERY - find relevant past context
result = mgr.load(query=user_request)
if result.found:
    context = result.content  # L1 summary, ~200 chars
    # Need more detail?
    result = result.drill_deeper()   # L2, ~600 chars
    result = result.drill_deeper()   # L3, ~1800 chars
    full = result.load_full_state()  # L4, verbatim original

# 3. WORK - perform task with full context available

# 4. COMMIT - persist session to memory
mgr.commit(
    topic="Brief description of this session",
    full_context=full_session_log,
    tags=["topic1", "topic2"]
)
```

## Status Report

```python
report = mgr.status_report()
# Returns: total lines, total nodes, last commit timestamp
print(report)
```

## Design Principles

- **Never deletes** — only compresses. The verbatim original is always recoverable.
- **Origin always in context** — L0 summaries of all nodes load at session start (~200 tokens).
- **Radial navigation** — query finds the most relevant node by keyword overlap, then drill deeper on demand.
- **Pluggable summarizer** — swap OpenAI / LiteLLM / custom backends without changing your workflow code.
- **Zero mandatory dependencies** — pure Python stdlib. Works out-of-the-box with KeywordSummarizer.
- **Single-file storage** — all memory in one `origin.json`. Atomic writes, no corruption.

## Source & Docs

- GitHub: https://github.com/vvxer/HedgehogMemory
- PyPI: `pip install hedgehog-memory`
- Issues: https://github.com/vvxer/HedgehogMemory/issues
