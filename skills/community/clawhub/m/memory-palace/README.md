# Memory Palace

> Cognitive enhancement layer for OpenClaw agents

[English](README.md) | [简体中文](docs/README.zh-CN.md) | [繁體中文](docs/README.zh-TW.md)

## Overview

Memory Palace is an OpenClaw Skill that provides persistent memory management with semantic search, knowledge graphs, and cognitive enhancement features.

## Features

- 📝 **Persistent Storage** - Memories stored as Markdown files
- 🔍 **Semantic Search** - Vector search with text fallback
- ⏰ **Time Reasoning** - Parse temporal expressions (明天, 下周, 本月, etc.)
- 🧠 **Concept Expansion** - Expand queries with related concepts
- 🏷️ **Tagging System** - Flexible categorization
- 📍 **Locations** - Organize memories by location
- ⭐ **Importance Scoring** - Prioritize important memories
- 🗑️ **Trash & Restore** - Soft delete with recovery
- 🔄 **Background Tasks** - Conflict detection, memory compression

### v1.2.0 New Features

- 🧠 **LLM Integration** - AI-powered summarization, experience extraction, time parsing
- 📚 **Experience Accumulation** - Record, verify, and retrieve experiences
- 💡 **Memory Types** - Classify memories as fact/experience/lesson/preference/decision

## Requirements

### Core Requirements
- **Node.js 18+** (ESM support required)
- **TypeScript 5.3+** (for building from source)

### Optional: Vector Search
- **Python 3.8+** (for semantic search capabilities)
- ~200MB RAM for embedding model
- BGE-small-zh-v1.5 model (auto-downloaded, ~100MB)

> **Note:** Vector search is optional but recommended for better search accuracy. Without it, Memory Palace falls back to text-based keyword matching.

## Installation

### Option 1: Install via ClawHub (Recommended)

```bash
# Install Memory Palace skill from ClawHub
clawhub install memory-palace
```

**ClawHub**: https://clawhub.com/skills/memory-palace

### Option 2: Install from Source

```bash
# Clone and build
git clone https://github.com/Lanzhou3/memory-palace.git
cd memory-palace
npm install
npm run build
```

### Enable Vector Search (Optional but Recommended)

For semantic search capabilities, install the vector search dependencies:

```bash
# Install Python dependencies
pip install sentence-transformers numpy

# Set HuggingFace mirror (China users)
export HF_ENDPOINT=https://hf-mirror.com

# Start the vector service
python scripts/vector-service.py &

# The BGE-small-zh-v1.5 model (~100MB) will be downloaded on first run
```

### Verify Installation

```bash
# Run tests to verify everything works
npm test
```

Expected output:
```
  MemoryPalaceManager
    ✓ should store a memory
    ✓ should get a memory by ID
    ✓ should search memories
    ✓ should list memories with filters
    ✓ should update a memory
    ✓ should delete and restore a memory
    ✓ should get statistics

  7 passing
```

> **Note:** If tests fail, check that Node.js version is 18+ and all dependencies are installed correctly.

## Quick Start

```typescript
import { MemoryPalaceManager } from '@openclaw/memory-palace';

const manager = new MemoryPalaceManager({
  workspaceDir: '/path/to/workspace'
});

// Store a memory
const memory = await manager.store({
  content: 'User prefers dark mode',
  tags: ['preferences', 'ui'],
  importance: 0.8,
  location: 'user-settings'
});

// Search memories
const results = await manager.recall('user preferences');

// List memories
const memories = await manager.list({
  tags: ['preferences'],
  limit: 10
});

// Get statistics
const stats = await manager.stats();
```

## Storage

Memories are stored in `{workspaceDir}/memory/palace/` as Markdown files:

```
workspace/
└── memory/
    └── palace/
        ├── uuid-1.md
        ├── uuid-2.md
        └── .trash/
            └── deleted-uuid.md
```

### File Format

```markdown
---
id: "uuid"
tags: ["tag1", "tag2"]
importance: 0.8
status: "active"
createdAt: "2026-03-18T10:00:00Z"
updatedAt: "2026-03-18T10:00:00Z"
source: "conversation"
location: "projects"
---

Memory content here...

## Summary
Optional summary
```

## API Reference

### MemoryPalaceManager

#### Constructor

```typescript
new MemoryPalaceManager(options: {
  workspaceDir: string;
  vectorSearch?: VectorSearchProvider;  // Optional
})
```

#### Methods

| Method | Description |
|--------|-------------|
| `store(params)` | Store a new memory |
| `get(id)` | Get memory by ID |
| `update(params)` | Update a memory |
| `delete(id, permanent?)` | Delete memory (soft by default) |
| `recall(query, options?)` | Search memories |
| `list(options?)` | List with filters |
| `stats()` | Get statistics |
| `restore(id)` | Restore from trash |
| `listTrash()` | List deleted memories |
| `emptyTrash()` | Clear trash |
| `storeBatch(items)` | Store multiple |
| `getBatch(ids)` | Get multiple |

### Experience Management (v1.2.0)

| Method | Description |
|--------|-------------|
| `recordExperience(params)` | Record a reusable experience |
| `getExperiences(options?)` | Query experiences by criteria |
| `verifyExperience(id, effective)` | Mark experience as effective/ineffective |
| `getRelevantExperiences(context)` | Get experiences relevant to context |

### LLM-Enhanced Methods (v1.1.0)

| Method | Description |
|--------|-------------|
| `summarize(id)` | AI-powered memory summarization |
| `extractExperience(memoryIds)` | Extract lessons from memories |
| `parseTimeLLM(expression)` | Complex time parsing via LLM |
| `expandConceptsLLM(query)` | Dynamic concept expansion |
| `compress(memoryIds)` | Intelligent memory compression |

### Cognitive Modules

```typescript
import {
  TopicCluster,
  EntityTracker,
  KnowledgeGraphBuilder
} from '@openclaw/memory-palace';

// Topic clustering
const cluster = new TopicCluster();
const clusters = await cluster.cluster(memories);

// Entity tracking
const tracker = new EntityTracker();
const { entities, coOccurrences } = await tracker.track(memories);

// Knowledge graph
const graphBuilder = new KnowledgeGraphBuilder();
const graph = await graphBuilder.build(memories);
```

### Background Tasks

```typescript
import {
  ConflictDetector,
  MemoryCompressor
} from '@openclaw/memory-palace';

// Conflict detection
const detector = new ConflictDetector();
const conflicts = await detector.detect(memories);

// Memory compression
const compressor = new MemoryCompressor();
const results = await compressor.compress(memories);
```

### Time Reasoning

```typescript
import { TimeReasoningEngine } from '@openclaw/memory-palace';

const engine = new TimeReasoningEngine();

// Parse temporal expressions
const context = engine.parseTimeQuery('下周有什么重要事项？');
// {
//   relativeTime: 'next_week',
//   timeRange: { start: Date, end: Date },
//   keywords: ['3月24日-3月30日', '重要', '截止', ...],
//   hasTimeReasoning: true
// }

// Resolve conditional queries
const conditional = engine.resolveConditionalTime('如果明天是周三，我需要准备什么？');
// {
//   isConditional: true,
//   targetDay: '周三',
//   keywords: ['周三', '准备']
// }
```

### Concept Expansion

```typescript
import { ConceptExpander } from '@openclaw/memory-palace';

const expander = new ConceptExpander();

// Expand query concepts
const expansion = await expander.expandQuery('健康和运动');
// {
//   expandedKeywords: ['健康', '运动', '健身', '体检', '爬山', '跑步', ...],
//   relatedConcepts: ['医疗', '锻炼', ...],
//   method: 'mapping'
// }

// Discover related concepts
const related = await expander.discoverRelated('编程');
// ['代码', '开发', 'TypeScript', 'Python', ...]

// Check domain category
const domain = expander.getDomainCategory('健康');  // '健康与运动'
```

## Integration with OpenClaw

Memory Palace is designed to wrap OpenClaw's `MemoryIndexManager` for vector search capabilities.

### With Vector Search

```typescript
import { MemoryPalaceManager } from '@openclaw/memory-palace';
import { MemoryIndexManager } from '@openclaw/memory';

const vectorSearch = new MemoryIndexManager({
  // OpenClaw config
});

const manager = new MemoryPalaceManager({
  workspaceDir: '/workspace',
  vectorSearch: {
    search: (query, topK, filter) => vectorSearch.search(query, topK, filter),
    index: (id, content, metadata) => vectorSearch.index(id, content, metadata),
    remove: (id) => vectorSearch.remove(id)
  }
});
```

### Without Vector Search

Memory Palace works without vector search, using text-based matching as fallback.

## Testing

```bash
npm test
```

## Architecture Principles

1. **No MCP Protocol** - Direct function calls, no external protocol
2. **Interface Isolation** - Vector search is optional interface
3. **File-based Storage** - Simple, portable, human-readable
4. **Graceful Degradation** - Works without advanced features

## License

MIT

---

Built with 🔥 by the Chaos Team