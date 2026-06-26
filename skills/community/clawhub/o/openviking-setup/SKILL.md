---
name: openviking-setup
description: Set up OpenViking context database for OpenClaw agents. OpenViking is an open-source context database designed specifically for AI agents with filesystem-based memory management, tiered context loading (L0/L1/L2), and self-evolving memory. Use when asked to set up OpenViking, configure context database for agents, implement persistent memory, or when memory management optimization is needed. Triggers on "install openviking", "setup openviking", "context database", "tiered memory", "L0 L1 L2 context".
---

# OpenViking Setup for OpenClaw

OpenViking brings filesystem-based memory management to AI agents with tiered context loading and self-evolving memory. This skill guides you through installation and configuration.

## What OpenViking Provides

- **Filesystem paradigm**: Unified context management (memories, resources, skills)
- **Tiered loading (L0/L1/L2)**: Load only what's needed, save tokens
- **Self-evolving memory**: Gets smarter with use
- **OpenClaw plugin**: Native integration available

## Prerequisites

- Python 3.10+
- Go 1.22+ (for AGFS components)
- GCC 9+ or Clang 11+ (for core extensions)
- VLM model access (for image/content understanding)
- Embedding model access (for vectorization)

## Quick Start

### Step 1: Install OpenViking

```bash
# Python package
pip install openviking --upgrade --force-reinstall

# CLI tool
curl -fsSL https://raw.githubusercontent.com/volcengine/OpenViking/main/crates/ov_cli/install.sh | bash
```

### Step 2: Create Configuration

Create `~/.openviking/ov.conf`:

```json
{
  "storage": {
    "workspace": "/home/your-name/openviking_workspace"
  },
  "log": {
    "level": "INFO",
    "output": "stdout"
  },
  "embedding": {
    "dense": {
      "api_base": "https://api.openai.com/v1",
      "api_key": "your-openai-api-key",
      "provider": "openai",
      "dimension": 1536,
      "model": "text-embedding-3-small"
    },
    "max_concurrent": 10
  },
  "vlm": {
    "api_base": "https://api.openai.com/v1",
    "api_key": "your-openai-api-key",
    "provider": "openai",
    "model": "gpt-4o",
    "max_concurrent": 100
  }
}
```

### Step 3: Configure Provider

OpenViking supports multiple VLM providers:

| Provider | Model Example | Notes |
|----------|---------------|-------|
| openai | gpt-4o | Official OpenAI API |
| volcengine | doubao-seed-2-0-pro | Volcengine Doubao |
| litellm | claude-3-5-sonnet | Unified access (Anthropic, DeepSeek, Gemini, etc.) |

For LiteLLM (recommended for flexibility):

```json
{
  "vlm": {
    "provider": "litellm",
    "model": "claude-3-5-sonnet-20241022",
    "api_key": "your-anthropic-key"
  }
}
```

For Ollama (local models):

```json
{
  "vlm": {
    "provider": "litellm",
    "model": "ollama/llama3.1",
    "api_base": "http://localhost:11434"
  }
}
```

## OpenClaw Integration

### Plugin Installation

OpenViking has a native OpenClaw plugin for seamless integration:

```bash
# Install OpenClaw plugin
pip install openviking-openclaw

# Or from source
git clone https://github.com/volcengine/OpenViking
cd OpenViking/plugins/openclaw
pip install -e .
```

### Configuration for OpenClaw

Add to your OpenClaw config:

```yaml
# ~/.openclaw/config.yaml
memory:
  provider: openviking
  config:
    workspace: ~/.openviking/workspace
    tiers:
      l0:
        max_tokens: 4000
        auto_flush: true
      l1:
        max_tokens: 16000
        compression: true
      l2:
        max_tokens: 100000
        archive: true
```

## Memory Tiers Explained

| Tier | Purpose | Token Budget | Behavior |
|------|---------|--------------|----------|
| **L0** | Active working memory | 4K tokens | Always loaded, fast access |
| **L1** | Frequently accessed | 16K tokens | Compressed, on-demand |
| **L2** | Archive/cold storage | 100K+ tokens | Semantic search only |

### How Tiers Work

1. New context goes to L0
2. L0 fills → oldest items compressed to L1
3. L1 fills → oldest items archived to L2
4. Retrieval searches all tiers, returns relevant context

## Directory Structure

```
~/.openviking/
├── ov.conf                 # Configuration
└── workspace/
    ├── memories/
    │   ├── sessions/        # L0: Active session memory
    │   ├── compressed/     # L1: Compressed memories
    │   └── archive/        # L2: Long-term storage
    ├── resources/          # Files, documents, assets
    └── skills/             # Skill-specific context
```

## Usage Patterns

### Adding Memory

```python
from openviking import MemoryStore

store = MemoryStore()

# Add to L0
store.add_memory(
    content="User prefers Portuguese language responses",
    metadata={"tier": "l0", "category": "preference"}
)

# Add resource
store.add_resource(
    path="project_spec.md",
    content=open("project_spec.md").read()
)
```

### Retrieving Context

```python
# Semantic search across all tiers
results = store.search(
    query="user preferences",
    tiers=["l0", "l1", "l2"],
    limit=10
)

# Directory-based retrieval (more precise)
results = store.retrieve(
    path="memories/sessions/2026-03-16/",
    recursive=True
)
```

### Compaction

```python
# Trigger manual compaction
store.compact()

# View compaction status
status = store.status()
print(f"L0: {status.l0_tokens}/{status.l0_max}")
print(f"L1: {status.l1_tokens}/{status.l1_max}")
```

## Best Practices

### Memory Hygiene

1. **Categorize entries**: Use metadata tags for better retrieval
2. **Flush L0 regularly**: Let compaction run, don't hoard
3. **Use directory structure**: Organize by project/topic
4. **Review L2 periodically**: Archive stale memories

### Token Efficiency

1. Let OpenViking manage tiers automatically
2. Use semantic search for L2 (don't load entire archive)
3. Compress verbose content before adding to L1
4. Keep L0 under 50% capacity for best performance

### OpenClaw Workflow

1. Session starts → OpenViking loads L0
2. Conversation proceeds → context auto-promoted to L1/L2
3. Long gaps → L2 provides relevant historical context
4. Sessions compound → agent gets smarter over time

## Troubleshooting

### Common Issues

**"No module named 'openviking'"**
- Ensure Python 3.10+ is active
- Try `pip install --user openviking`

**"Embedding model not found"**
- Check `ov.conf` has correct provider and model
- Verify API key is valid

**"L0 overflow"**
- Reduce `l0.max_tokens` in config
- Manually call `store.compact()`

**"Slow retrieval from L2"**
- Consider pre-loading frequently accessed resources to L1
- Use directory-based retrieval for better precision

## Resources

- **GitHub**: https://github.com/volcengine/OpenViking
- **Documentation**: https://github.com/volcengine/OpenViking/tree/main/docs
- **OpenClaw Plugin**: https://github.com/volcengine/OpenViking/tree/main/plugins/openclaw
- **Examples**: https://github.com/volcengine/OpenViking/tree/main/examples

## What Gets Better

After setup, your agent gains:

1. **Persistent memory** across sessions
2. **Smarter retrieval** with semantic + directory search
3. **Token efficiency** with tiered loading
4. **Self-improvement** as context accumulates
5. **Observable context** with retrieval trajectories

The more your agent works, the more context it retains—without token bloat.