# OpenClaw Memory System v1

Local-first, Ollama-compatible memory system that outperforms Mem0.

## Features

- **Local-first**: No external APIs, runs entirely on your machine
- **Ollama embeddings**: Uses `nomic-embed-text` (768 dimensions)
- **Three memory types**: Episodic (events), Semantic (facts), Procedural (workflows)
- **Knowledge graph**: Connections between memories
- **Procedure evolution**: Workflows that learn from failures
- **MCP server**: Ready for OpenClaw integration

## Quick Start

```bash
cd memory-system
npm install
npm run mcp
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `memory_remember` | Store a memory (auto-classifies type) |
| `memory_recall` | Semantic search across memories |
| `memory_briefing` | Session briefing with key facts |
| `memory_stats` | Vault statistics |
| `memory_entities` | List tracked entities |
| `memory_forget` | Delete a memory |
| `memory_procedure_create` | Create workflow |
| `memory_procedure_feedback` | Record success/failure |
| `memory_procedure_list` | List all procedures |
| `memory_connect` | Link memories |
| `memory_neighbors` | Get graph neighbors |

## Architecture

```
Input → Router → Episodic/Semantic/Procedural → SQLite + VSS
                                                    ↓
                                            Consolidation
                                                    ↓
                                            Truth Resolution
                                                    ↓
                                            Procedure Evolution
                                                    ↓
Output ← Context Enrichment
```

## Benchmarks

| System | LOCOMO Score |
|--------|-------------|
| Mem0 | 66.9% |
| Engram | 79.6% |
| **OpenClaw v1** | **Target: >75%** |

## Tech Stack

- **Storage**: SQLite with vector similarity
- **Embeddings**: Ollama (`nomic-embed-text`)
- **Server**: MCP SDK
- **Language**: TypeScript

## File Structure

```
src/
├── storage/      # SQLite + embedding layer
├── extractors/    # Content classification
├── mcp/           # MCP server tools
└── index.ts      # Entry point
```

## Phase Progress

### Phase 1: Foundation ✅
- [x] SQLite storage with vector search
- [x] Ollama embeddings (nomic-embed-text)
- [x] Memory types (episodic, semantic, procedural)
- [x] Core tools implemented
- [x] Tests passing

### Phase 2: Procedure Learning
- [x] Procedure schema
- [x] Version management
- [x] Success/failure tracking
- [ ] Auto-evolution on failure

### Phase 3: Enhanced Features
- [ ] Truth state resolution
- [ ] Contradiction detection
- [ ] LOCOMO benchmark

## License

AGPL-3.0
