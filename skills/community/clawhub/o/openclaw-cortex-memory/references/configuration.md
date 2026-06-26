# Configuration Reference

## Minimum OpenClaw Config

Use this as the baseline in `openclaw.json`.

```json
{
  "plugins": {
    "allow": ["openclaw-cortex-memory"],
    "slots": {
      "memory": "none"
    },
    "entries": {
      "memory-core": {
        "enabled": false
      },
      "memory-lancedb": {
        "enabled": false
      },
      "openclaw-cortex-memory": {
        "enabled": true,
        "config": {
          "autoSync": true,
          "autoReflect": false,
          "graphQualityMode": "warn",
          "wikiProjection": {
            "enabled": true,
            "mode": "incremental",
            "maxBatch": 100
          },
          "embedding": {
            "provider": "api",
            "model": "text-embedding-3-small",
            "apiKey": "${EMBEDDING_API_KEY}",
            "baseURL": "https://your-embedding-endpoint/v1",
            "dimensions": 1536
          },
          "llm": {
            "provider": "api",
            "model": "gpt-4",
            "apiKey": "${LLM_API_KEY}",
            "baseURL": "https://your-llm-endpoint/v1"
          },
          "reranker": {
            "provider": "api",
            "model": "BAAI/bge-reranker-v2-m3",
            "apiKey": "${RERANKER_API_KEY}",
            "baseURL": "https://your-reranker-endpoint/v1/rerank"
          }
        }
      }
    }
  }
}
```

## Exclusive Mode Rules

- Do not set `plugins.slots.memory` to `openclaw-cortex-memory`.
- Keep `plugins.entries.memory-core.enabled = false`.
- Keep `plugins.entries.memory-lancedb.enabled = false`.

## Required Environment Variables

- `EMBEDDING_API_KEY`
- `LLM_API_KEY`
- `RERANKER_API_KEY`

## Required Endpoints

- Embedding: OpenAI-compatible `/embeddings`
- LLM: OpenAI-compatible `/chat/completions`
- Reranker: `/rerank`

## Troubleshooting: memory backend requirement

If `openclaw plugins install/enable` reports `memory-core` or `memory-lancedb` requirement errors, keep both disabled under `plugins.entries`.  
If your host still requires a `memory-lancedb` shape check even when disabled, use:

```json
"memory-lancedb": {
  "enabled": false,
  "config": {
    "embedding": {
      "apiKey": "${MEMORY_LANCEDB_API_KEY}",
      "model": "text-embedding-3-small"
    },
    "dbPath": "~/.openclaw/memory/lancedb",
    "autoRecall": true,
    "autoCapture": false,
    "captureMaxChars": 500
  }
}
```

## Recommended Validation Commands

```bash
openclaw plugins list
openclaw plugins inspect openclaw-cortex-memory
openclaw skills list
openclaw skills info cortex-memory
openclaw skills check
```
