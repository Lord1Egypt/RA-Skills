---
name: memory-persistence
description: Multi-backend memory system with optional embedding, private/shared memories, conversation summarization, and maintenance tools. For AI agents to store and retrieve persistent memories.
metadata:
  {
    "memory_system":
      {
        "version": "1.5.0",
        "author": "assistant",
        "tags": ["memory", "embedding", "shared-memory", "storage"],
        "requires": {
          "python_packages": ["sentence-transformers", "scikit-learn", "pyyaml", "numpy"]
        }
      }
  }
---

# 🧠 Memory System

A flexible memory system for AI agents with optional embedding support and multiple storage backends.

## Features

- **Private & Shared Memories** - Private by default, shared memories for multi-agent collaboration
- **Embedding Search** - Semantic search using sentence-transformers
- **Multiple Backends** - Local file / SQLite / GitHub / Gitee
- **LLM Summarization** - Auto-extract key info from conversations
- **Memory Maintenance** - Review, consolidate, tag suggestions
- **Templates** - Quick memory creation with templates

## Installation

```bash
pip install sentence-transformers scikit-learn pyyaml numpy
```

## Quick Start

### Python API

```python
from memory_system import MemoryManager

# Initialize (local storage)
mm = MemoryManager(backend='local')

# Add 
mm.add("User prefers dark theme", tags=["preference"])

# Search
results = mm.search("dark theme preference")

# List
entries = mm.list(tags=["preference"])
```

### CLI

```bash
# Add 
python3 memory_cli.py add "User feedback: slow page load" --tags "bug,performance"

# List
python3 memory_cli.py list

# Search
python3 memory_cli.py -e search "performance issue"

# Semantic search (with embedding)
python3 memory_cli.py -e search "dark mode"
```

## Private vs Shared Memory

| Type | Storage | Access | Use Case |
|------|---------|--------|----------|
| **Private** | `./memory_data/` | Current agent only | User preferences, personal notes |
| **Shared** | `./shared_memory/` | All agents | Team decisions, collaboration |

**Default**: All memories are private. Use `shared add` only when other agents need to know.

```python
# Private memory - user says "remember..."
mm.add("User name is Zhang San")

# Shared memory - user says "tell other agents..."
smm.add("Team decision: use React", agent_id="agent_a")
```

## Storage Backends

### Local (Default)
```python
mm = MemoryManager(backend='local')
```

### SQLite (High Performance)
```python
mm = MemoryManager(backend='sqlite', base_path='./memory.db')
```

### GitHub
```bash
export GITHUB_TOKEN="your_token"
```
```python
mm = MemoryManager(
    backend='github',
    repo='owner/repo',
    branch='main'
)
```

### Gitee
```bash
export GITEE_TOKEN="your_token"
```
```python
mm = MemoryManager(
    backend='gitee',
    repo='owner/repo',
    branch='master'
)
```

## Embedding & Semantic Search

Embedding is optional and auto-downloads on first use.

```python
# Enable embedding
mm = MemoryManager(backend='local', use_embedding=True)

# Add (auto-generates vector)
mm.add("User works from 9am to 6pm")

# Semantic search - finds similar content
results = mm.search("what time does user work")
```

CLI with embedding:
```bash
python3 memory_cli.py -e search "working hours"
```

## Shared Memory (Multi-Agent)

```python
from memory_system import SharedMemoryManager

# Initialize
smm = SharedMemoryManager(backend='local', shared_path='./shared_memory')

# Add shared memory (from an agent)
smm.add("Bug #123 fixed", agent_id='agent_b')

# List shared memories
shared = smm.list()

# By agent
by_agent = smm.get_by_agent('agent_b')
```

CLI:
```bash
# Add shared 
python3 memory_cli.py shared add "Team decision: use Vue" --agent "agent_a"

# List
python3 memory_cli.py shared list

# Search
python3 memory_cli.py -e shared search "Vue decision"
```

## Conversation Summarization

Auto-extract key information from conversation history.

```python
from memory_system import MemoryManager, MemorySummarizer, ConversationMemoryProcessor

mm = MemoryManager(use_embedding=True)
summarizer = MemorySummarizer()  # Auto-detects OpenClaw model
processor = ConversationMemoryProcessor(mm, summarizer, auto_save=True)

conversation = """
User: I prefer dark theme
Assistant: Changed to dark theme
User: Page loads slowly
Assistant: Optimized images
"""

memories = processor.process(conversation)
```

CLI:
```bash
python3 memory_cli.py summarize --file conversation.txt --save
```

## Memory Maintenance

```bash
# Generate report
python3 memory_cli.py maintenance report

# Review old memories
python3 memory_cli.py maintenance review --days 7

# Find similar memories
python3 memory_cli.py maintenance consolidate

# Suggest tags for untagged memories
python3 memory_cli.py maintenance suggest-tags

# Mark as outdated
python3 memory_cli.py maintenance outdated --mark <id> --reason "expired"
```

## Templates

Predefined formats for quick memory creation.

```bash
# List templates
python3 memory_cli.py template list

# Show template
python3 memory_cli.py template show task

# Use template
python3 memory_cli.py template use task \
  --field title="Complete report" \
  --field priority="high"
```

## Memory Groups

Organize memories into groups.

```bash
# Add to group
python3 memory_cli.py add "work task" --tags "work" --group "work"

# List groups
python3 memory_cli.py group list

# Show group
python3 memory_cli.py group show "work"
```

## Batch Operations

```bash
# Batch add tags
python3 memory_cli.py batch-add-tags id1,id2 --tags "important,priority"

# Batch delete (requires confirmation)
python3 memory_cli.py batch-delete id1,id2 --force
```

## API Reference

### MemoryManager

| Method | Description |
|--------|-------------|
| `add(content, tags, metadata, group)` | Add memory |
| `get(id)` | Get by ID |
| `delete(id)` | Delete |
| `list(tags, limit, offset)` | List with pagination |
| `search(query, tags, top_k, threshold)` | Search |
| `batch_delete(ids)` | Batch delete |
| `list_groups()` | List groups |
| `export_json(filepath)` | Export JSON |

### SharedMemoryManager

| Method | Description |
|--------|-------------|
| `add(content, agent_id, tags)` | Add shared memory |
| `list(tags)` | List shared |
| `get_by_agent(agent_id)` | By agent |
| `search(query)` | Search shared |

## Files Structure

```
memory_system/
├── memory_manager.py   # Core manager
├── shared_memory.py    # Shared 
├── summarizer.py      # LLM summarization
├── maintenance.py      # Maintenance tools
├── templates.py       # Templates
├── embedding.py       # Embedding handler
├── storage/           # Storage backends
│   ├── local.py
│   ├── sqlite.py
│   ├── github.py
│   └── gitee.py
└── memory_cli.py         # CLI entry (run with python3)
```

## Configuration

`config.yaml`:
```yaml
STORAGE_BACKEND: "local"

USE_EMBEDDING: false
EMBEDDING_MODEL: "sentence-transformers/all-MiniLM-L6-v2"

storage:
  local:
    base_path: "./memory_data"
  sqlite:
    base_path: "./memory.db"
  github:
    repo: "owner/repo"
    token_env: "GITHUB_TOKEN"
  gitee:
    repo: "owner/repo"
    token_env: "GITEE_TOKEN"
```

## License

MIT
