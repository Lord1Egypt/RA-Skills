# @primo-studio/memoria-core

**Standalone multi-layer cognitive memory engine** — works with or without OpenClaw.

## Features

- **21-layer cognitive architecture** — selective storage, embeddings, knowledge graph, topics, patterns, observations, procedural memory
- **Zero cloud dependency** — runs 100% local with Ollama, LM Studio, or any OpenAI-compatible API
- **Automatic fallback chain** — Ollama → OpenAI → LM Studio → FTS-only (never fails)
- **SQLite + FTS5** — blazing fast full-text search
- **Vector embeddings** — cosine similarity with nomic-embed-text, text-embedding-3-small, or custom models
- **Knowledge graph** — entity extraction, relations, Hebbian learning
- **Pattern detection** — consolidates recurring facts, 1.5x recall boost
- **Lifecycle management** — fresh → active → settled → dormant (automatic aging)
- **Contradiction detection** — replaces outdated facts with new information
- **Procedural memory** — learns from tool use, reflects on success patterns
- **Markdown sync** — bi-directional sync with .md files

## Installation

```bash
npm install @primo-studio/memoria-core
# or
pnpm add @primo-studio/memoria-core
```

## Quick Start

```typescript
import { Memoria } from '@primo-studio/memoria-core';

// Initialize with Ollama (local, free)
const memoria = await Memoria.init({
  dbPath: './my-app.db',
  provider: 'ollama',
  model: 'qwen3.5:4b',
  embeddingModel: 'nomic-embed-text-v2-moe'
});

// Store facts
await memoria.store('User prefers dark mode', 'preference', 0.95);
await memoria.store('User location: New York', 'savoir', 0.9);

// Recall facts
const results = await memoria.recall('What theme does the user like?');
console.log(results.facts);
// [{ id: 1, fact: 'User prefers dark mode', category: 'preference', confidence: 0.95, ... }]

// Natural language query (future: dialectic reasoning)
const answer = await memoria.query('Tell me about the user preferences');
console.log(answer);

// Stats
const stats = await memoria.stats();
console.log(stats);
// { totalFacts: 42, totalEmbeddings: 38, totalRelations: 15, ... }

// Close
memoria.close();
```

## Configuration

### Local (Ollama)

```typescript
const memoria = await Memoria.init({
  dbPath: './memoria.db',
  provider: 'ollama',
  model: 'qwen3.5:4b',
  embeddingModel: 'nomic-embed-text-v2-moe',
  baseUrl: 'http://localhost:11434'
});
```

### Cloud (OpenAI)

```typescript
const memoria = await Memoria.init({
  dbPath: './memoria.db',
  provider: 'openai',
  model: 'gpt-4o-mini',
  embeddingModel: 'text-embedding-3-small',
  apiKey: process.env.OPENAI_API_KEY
});
```

### LM Studio

```typescript
const memoria = await Memoria.init({
  dbPath: './memoria.db',
  provider: 'lmstudio',
  model: 'auto', // uses loaded model
  baseUrl: 'http://localhost:1234/v1'
});
```

### Custom Fallback Chain

```typescript
const memoria = await Memoria.init({
  dbPath: './memoria.db',
  fallback: [
    { type: 'ollama', model: 'qwen3.5:4b', baseUrl: 'http://localhost:11434' },
    { type: 'openai', model: 'gpt-5.4-nano', apiKey: process.env.OPENAI_API_KEY },
    { type: 'lmstudio', baseUrl: 'http://localhost:1234/v1' }
  ]
});
```

## API Reference

### `Memoria.init(options: MemoriaInitOptions): Promise<Memoria>`

Initialize a new Memoria instance.

**Options:**
- `dbPath` (required): Path to SQLite database file
- `provider`: `'ollama'` | `'openai'` | `'anthropic'` | `'lmstudio'`
- `model`: LLM model name
- `embeddingModel`: Embedding model name
- `embeddingDimensions`: Embedding dimensions (default: 768)
- `baseUrl`: Provider base URL
- `apiKey`: API key for cloud providers
- `language`: `'fr'` | `'en'` (default: 'en')
- `fallback`: Array of fallback providers
- `recallLimit`: Max facts to return (default: 8)
- `workspacePath`: Path for markdown sync (optional)
- `debug`: Enable debug logging

### `memoria.store(fact: string, category?: string, confidence?: number): Promise<StoreResult>`

Store a new fact in memory.

**Categories:**
- `savoir` — knowledge, facts
- `preference` — user preferences
- `erreur` — errors, mistakes
- `chronologie` — events, timeline
- `outil` — tools, configs
- `client` — client info
- `rh` — team, HR
- `pattern` — detected patterns (auto-generated)

**Returns:**
- `factId`: Database ID (-1 if not stored)
- `stored`: Boolean
- `reason`: Why not stored (if applicable)

### `memoria.recall(query: string, options?: RecallOptions): Promise<RecallResult>`

Recall facts based on a query.

**Options:**
- `limit`: Max facts to return
- `minConfidence`: Minimum confidence threshold
- `categories`: Filter by categories

**Returns:**
- `facts`: Array of facts with scores
- `totalFound`: Number of results

### `memoria.query(question: string): Promise<string>`

Natural language query with formatted context (future: dialectic reasoning).

### `memoria.stats(): Promise<MemoriaStats>`

Get memory statistics.

**Returns:**
- `totalFacts`, `totalEmbeddings`, `totalRelations`, `totalTopics`, `totalPatterns`, `totalObservations`
- `lifecycleDistribution`: Facts by lifecycle state
- `categoryCounts`: Facts by category

### `memoria.close(): void`

Close database connection.

## Advanced Usage

### Direct Manager Access

```typescript
// Access low-level managers for advanced use
const entities = memoria.graph.getEntitiesByType('person');
const strongRelations = memoria.hebbian.getStrong(5);
const topTopics = memoria.topics.getTopics(10);
const patterns = memoria.patterns.getAll();
```

### Custom Providers

```typescript
import { type LLMProvider, type EmbedProvider } from '@primo-studio/memoria-core';

const customLLM: LLMProvider = {
  async generate(prompt: string): Promise<string> {
    // Your custom implementation
    return 'response';
  }
};

const customEmbed: EmbedProvider = {
  async embed(text: string): Promise<number[]> {
    // Your custom implementation
    return [/* 768-dim vector */];
  }
};
```

## Architecture

Memoria uses a **21-layer cognitive architecture**:

1. **Layer 1** — Capture (fact extraction from conversations)
2. **Layer 2** — Deduplication (Levenshtein + Jaccard)
3. **Layer 3** — Contradiction detection (semantic similarity + LLM)
4. **Layer 4** — Enrichment (merge related facts)
5. **Layer 5** — Embedding (vector search)
6. **Layer 6** — Recall (retrieval pipeline)
7. **Layer 7** — Scoring (FTS5 + cosine + context boost)
8. **Layer 8** — Knowledge graph (entity/relation extraction)
9. **Layer 9** — Topics (emergent clustering)
10. **Layer 10** — Lifecycle (aging, state transitions)
11. **Layer 11** — Hebbian (co-occurrence learning)
12. **Layer 12** — Expertise (skill tracking)
13. **Layer 13** — Feedback (usefulness tracking)
14. **Layer 14** — Patterns (behavioral consolidation)
15. **Layer 15** — Observations (hypothesis testing)
16. **Layer 16** — Fact clusters (semantic grouping)
17. **Layer 17** — Revision (content updates)
18. **Layer 18** — Context tree (hierarchical boost)
19. **Layer 19** — Budget (adaptive limits)
20. **Layer 20** — Procedural (tool patterns)
21. **Layer 21** — Continuous (live extraction)

## Performance

- **Recall**: ~50-150ms (FTS5 + embeddings + reranking)
- **Store**: ~200-500ms (with embedding + graph extraction)
- **Memory**: ~50MB base + ~1KB per fact
- **Database**: SQLite (portable, zero-config)

## License

Apache-2.0

## Contributing

PRs welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md)

## Credits

Built by [Primo Studio](https://primo-studio.fr) for OpenClaw and standalone use.
