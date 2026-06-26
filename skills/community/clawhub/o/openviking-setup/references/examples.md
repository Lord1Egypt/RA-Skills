# OpenViking Examples

This file contains practical examples for common OpenViking operations.

## Basic Usage

### Initialize MemoryStore

```python
from openviking import MemoryStore

# Create store with default config (~/.openviking/ov.conf)
store = MemoryStore()

# Or specify custom config path
store = MemoryStore(config_path="/path/to/custom/config.json")
```

### Adding Memories

```python
# Add to L0 (active working memory)
store.add_memory(
    content="User prefers concise responses in Portuguese",
    metadata={
        "tier": "l0",
        "category": "preference",
        "importance": "high"
    }
)

# Add with auto-tier assignment
store.add_memory(
    content="Project deadline is March 30, 2026",
    metadata={"category": "project"}
)

# Add resource (file, document, etc.)
store.add_resource(
    path="specs/requirements.md",
    content=open("requirements.md").read(),
    metadata={"type": "markdown", "project": "openviking-setup"}
)
```

### Searching Memory

```python
# Semantic search across all tiers
results = store.search(
    query="user preferences",
    limit=10
)

# Search in specific tier
results = store.search(
    query="project deadlines",
    tiers=["l0", "l1"],
    limit=5
)

# Directory-based retrieval (more precise)
results = store.retrieve(
    path="memories/sessions/2026-03-16/",
    recursive=True
)
```

## OpenClaw Integration

### Session Memory Pattern

```python
# At session start - load relevant context
context = store.search(
    query="recent work and decisions",
    tiers=["l0", "l1"],
    limit=20
)

# During session - add important context
store.add_memory(
    content=f"Decision: Use OpenViking for context management",
    metadata={
        "tier": "l0",
        "category": "decision",
        "session": "2026-03-16"
    }
)

# At session end - promote important items
store.promote(
    from_tier="l0",
    to_tier="l1",
    criteria={"importance": "high"}
)
```

### Working with Resources

```python
# Store a project spec for future reference
with open("project_spec.md") as f:
    spec_content = f.read()

store.add_resource(
    path="project/openviking-setup/spec.md",
    content=spec_content,
    metadata={
        "type": "specification",
        "version": "1.0",
        "created": "2026-03-16"
    }
)

# Later, retrieve it
spec = store.retrieve("project/openviking-setup/spec.md")
```

## Tier Management

### Manual Promotion

```python
# Promote important L0 items to L1
store.promote(
    from_tier="l0",
    to_tier="l1",
    criteria={"importance": "high"}
)

# Archive old L1 items to L2
store.archive(
    older_than_days=30
)
```

### Compaction

```python
# Trigger manual compaction
result = store.compact()

print(f"Compacted {result.items_moved} items")
print(f"Tokens saved: {result.tokens_saved}")

# View compaction status
status = store.status()
print(f"L0: {status.l0_tokens}/{status.l0_max} tokens")
print(f"L1: {status.l1_tokens}/{status.l1_max} tokens")
```

## Advanced Patterns

### Context-Aware Retrieval

```python
def get_relevant_context(query: str, session_id: str):
    """Get context prioritizing recent session and semantic relevance."""
    
    # First, check current session
    session_context = store.retrieve(
        path=f"memories/sessions/{session_id}/",
        recursive=True
    )
    
    # Then semantic search across tiers
    semantic_context = store.search(
        query=query,
        tiers=["l1", "l2"],
        limit=10
    )
    
    # Combine with session priority
    return session_context + semantic_context
```

### Memory Categories

```python
# Categorized memory storage
categories = {
    "preference": "User preferences and settings",
    "decision": "Important decisions made",
    "project": "Project-specific context",
    "learning": "Things learned and improved",
    "error": "Errors encountered and solutions"
}

for cat, desc in categories.items():
    store.add_memory(
        content=f"Category initialized: {desc}",
        metadata={"category": cat, "type": "meta"}
    )
```

### Bulk Import

```python
# Import existing memories from file
import json

with open("memories_export.json") as f:
    memories = json.load(f)

for mem in memories:
    store.add_memory(
        content=mem["content"],
        metadata=mem.get("metadata", {})
    )
    
print(f"Imported {len(memories)} memories")
```

## Cleanup and Maintenance

```python
# View storage stats
stats = store.stats()
print(f"Total memories: {stats.total_memories}")
print(f"Total resources: {stats.total_resources}")
print(f"L0 size: {stats.l0_size}")
print(f"L1 size: {stats.l1_size}")
print(f"L2 size: {stats.l2_size}")

# Clean up duplicates
removed = store.deduplicate()
print(f"Removed {removed} duplicates")

# Prune stale entries
pruned = store.prune(older_than_days=90)
print(f"Pruned {pruned} stale entries")
```