# KV Embed Store

Embedding-based key-value store. Multiple key aliases map to one entry. Built-in dedup prevents duplicates. Optional memory index for `memory_search` discovery.

## Usage Modes

### Plugin Mode (recommended)

Install as an OpenClaw plugin for native tool access:

```bash
openclaw plugins install clawhub:openclaw-plugin-kv-embed-store
```

Registers: `kv_put`, `kv_search`, `kv_get`, `kv_list`, `kv_remove`, `kv_merge`, `kv_dedup`, `kv_refresh_index`.

### Standalone Mode

```bash
python3 scripts/kv_store.py put "my-project" '{"repo":"github.com/example/project","port":3000}'
python3 scripts/kv_store.py search "project reference" -k 5
```

## Plugin Configuration

In `openclaw.json` under `plugins.entries.kv-embed-store.config`:

| Key | Default | Description |
|-----|---------|-------------|
| `storePath` | `data/kv_store.json` | Path to the store JSON file |
| `memoryIndex` | `false` | Generate memory index with aliases and value previews |
| `apiKey` | — | Embedding API key (or `KV_EMBED_API_KEY` env) |
| `baseUrl` | `https://api.siliconflow.cn/v1` | Embedding API base URL (or `KV_EMBED_BASE_URL` env) |
| `model` | `BAAI/bge-m3` | Embedding model (or `KV_EMBED_MODEL` env) |

```json5
{
  plugins: {
    entries: {
      "kv-embed-store": {
        enabled: true,
        config: {
          storePath: "~/.openclaw/workspace/data/kv-store.json",
          apiKey: "sk-xxx",
          baseUrl: "https://api.siliconflow.cn/v1",
          model: "BAAI/bge-m3"
        }
      }
    }
  }
}
```

### Provider Examples

```bash
# SiliconFlow (default)
export KV_EMBED_API_KEY=***
export KV_EMBED_BASE_URL=https://api.siliconflow.cn/v1
export KV_EMBED_MODEL=BAAI/bge-m3

# OpenRouter
export KV_EMBED_API_KEY=***
export KV_EMBED_BASE_URL=https://openrouter.ai/api/v1
export KV_EMBED_MODEL=openai/text-embedding-3-small

# OpenAI
export KV_EMBED_API_KEY=***
export KV_EMBED_BASE_URL=https://api.openai.com/v1
export KV_EMBED_MODEL=text-embedding-3-small
```

## Requirements

- **Plugin**: Node >= 22, `openclaw >=2026.5.17`
- **Standalone**: Python 3, `numpy`, `requests`
- **API**: Any OpenAI-compatible embeddings provider (SiliconFlow, OpenRouter, OpenAI, etc.)

## Put Behavior (anti-duplicate)

When `kv_put` is called:
1. Embed the key text via the configured embedding provider
2. Search existing keys by cosine similarity
3. **cos > 0.95**: auto-merge — add key as alias, update value
4. **cos 0.85-0.95**: return candidates, let caller decide
5. **cos < 0.85**: create new entry
6. `force=true` skips dedup

## Data Format

Store file is human-readable JSON:

```json
{
  "entries": {
    "e1": {
      "aliases": ["my-project", "project-reference"],
      "data": {"repo": "github.com/example/project", "port": 3000},
      "created_at": "2026-07-06T15:30:00",
      "updated_at": "2026-07-06T15:35:00"
    }
  },
  "embeddings": {
    "my-project": [0.1, 0.2, ...],
    "project-reference": [0.15, 0.22, ...]
  }
}
```

## Tips

- Use short, distinctive key texts for best embedding results
- Group related values under one entry with multiple aliases
- Run `kv_dedup --apply` periodically to clean up accidental duplicates
- Enable `memoryIndex` to make entries discoverable via `memory_search`
- Use the standalone Python CLI for ad-hoc queries without installing the plugin
