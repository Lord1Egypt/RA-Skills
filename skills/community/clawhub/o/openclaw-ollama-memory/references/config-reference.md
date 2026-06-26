# Configuration Reference

## Minimal Working Config

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama",
        "model": "nomic-embed-text:latest",
        "remote": {
          "baseUrl": "http://127.0.0.1:11434"
        }
      }
    }
  }
}
```

## Full Config with All Options

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama",
        "model": "nomic-embed-text:latest",
        "fallback": "local",
        "enabled": true,
        "remote": {
          "baseUrl": "http://127.0.0.1:11434"
        },
        "query": {
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.7,
            "textWeight": 0.3,
            "mmr": {
              "enabled": false,
              "lambda": 0.7
            },
            "temporalDecay": {
              "enabled": false,
              "halfLifeDays": 30
            }
          }
        },
        "extraPaths": []
      }
    }
  }
}
```

## Alternative Models

| Model | Size | Languages | Notes |
|-------|------|-----------|-------|
| `nomic-embed-text:latest` | 274MB | English | Default recommendation — fast, accurate |
| `nomic-embed-text-v2-moe` | ~300M | 100+ | Multilingual MoE, SoTA for its size, Matryoshka embeddings |
| `embeddinggemma` | ~300M | 100+ | Google Gemma-based, requires Ollama v0.11.10+, state-of-the-art for size |

Pull an alternative:
```bash
ollama pull nomic-embed-text-v2-moe
# or
ollama pull embeddinggemma
```

Then update `openclaw.json`:
```json
{
  "memorySearch": {
    "provider": "ollama",
    "model": "nomic-embed-text-v2-moe",
    "remote": { "baseUrl": "http://127.0.0.1:11434" }
  }
}
```

> **Note for `nomic-embed-text-v2-moe`:** Add query prefixes for best results — `"search_query: your query"` for searches, `"search_document: your text"` for indexed content.

---

## Config Options

### Core

| Key | Default | Description |
|-----|---------|-------------|
| `provider` | auto | Must be `"ollama"` — not auto-detected |
| `model` | provider default | `"nomic-embed-text:latest"` recommended |
| `fallback` | `"none"` | Fallback provider if Ollama fails (e.g. `"local"`) |
| `enabled` | `true` | Set `false` to disable memory search entirely |
| `remote.baseUrl` | — | Ollama API base: `http://127.0.0.1:11434` |

### Hybrid Search (BM25 + Vector)

| Key | Default | Description |
|-----|---------|-------------|
| `query.hybrid.enabled` | `true` | Combine vector + keyword search |
| `query.hybrid.vectorWeight` | `0.7` | Weight for semantic similarity (0–1) |
| `query.hybrid.textWeight` | `0.3` | Weight for BM25 keyword match (0–1) |

### MMR Diversity Re-ranking

Prevents returning near-duplicate results.

| Key | Default | Description |
|-----|---------|-------------|
| `query.hybrid.mmr.enabled` | `false` | Enable MMR re-ranking |
| `query.hybrid.mmr.lambda` | `0.7` | 0 = max diversity, 1 = max relevance |

### Temporal Decay (Recency Boost)

Boosts newer memories in search results. Evergreen files (`MEMORY.md`, non-dated files) are never decayed.

| Key | Default | Description |
|-----|---------|-------------|
| `query.hybrid.temporalDecay.enabled` | `false` | Enable recency boost |
| `query.hybrid.temporalDecay.halfLifeDays` | `30` | Score halves every N days |

### Extra Paths

Index additional directories or files beyond the default workspace:

```json
{
  "memorySearch": {
    "extraPaths": ["../team-docs", "/srv/shared-notes"]
  }
}
```

Paths can be absolute or workspace-relative. Directories are scanned recursively for `.md` files.
