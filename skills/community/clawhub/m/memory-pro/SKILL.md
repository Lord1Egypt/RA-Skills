---
name: "memory-pro"
description: "This skill provides semantic search over your memory files using a local vector database."
version: "2.5.0"
metadata:
  openclaw:
    requires:
      bins:
        - "bash"
        - "lsof"
        - "openclaw"
        - "python"
        - "python3"
      env:
        - "HOME"
        - "MEMORY_PRO_API_URL"
        - "MEMORY_PRO_BM25_PATH"
        - "MEMORY_PRO_BM25_WEIGHT"
        - "MEMORY_PRO_CANDIDATE_POOL"
        - "MEMORY_PRO_CORE_FILES"
        - "MEMORY_PRO_DAILY_SCOPE"
        - "MEMORY_PRO_DATA_DIR"
        - "MEMORY_PRO_DUAL_HIT_BONUS"
        - "MEMORY_PRO_ENABLE_MMR"
        - "MEMORY_PRO_HARD_MIN_SCORE"
        - "MEMORY_PRO_INDEX_PATH"
        - "MEMORY_PRO_LENGTH_NORM_ALPHA"
        - "MEMORY_PRO_LENGTH_NORM_ANCHOR"
        - "MEMORY_PRO_META_PATH"
        - "MEMORY_PRO_MMR_LAMBDA"
        - "MEMORY_PRO_MMR_SIM_THRESHOLD"
        - "MEMORY_PRO_MODE"
        - "MEMORY_PRO_PORT"
        - "MEMORY_PRO_RECENCY_HALF_LIFE_DAYS"
        - "MEMORY_PRO_RECENCY_WEIGHT"
        - "MEMORY_PRO_RERANK_API_KEY"
        - "MEMORY_PRO_RERANK_BLEND"
        - "MEMORY_PRO_RERANK_ENDPOINT"
        - "MEMORY_PRO_RERANK_MODEL"
        - "MEMORY_PRO_RERANK_PROVIDER"
        - "MEMORY_PRO_RERANK_SAMPLE_PCT"
        - "MEMORY_PRO_RERANK_TIMEOUT_MS"
        - "MEMORY_PRO_RERANK_TOPN"
        - "MEMORY_PRO_SCOPE_STRICT"
        - "MEMORY_PRO_SENTENCES_PATH"
        - "MEMORY_PRO_TIMEOUT"
        - "MEMORY_PRO_VECTOR_WEIGHT"
        - "OPENCLAW_HOME"
        - "OPENCLAW_NETWORK_DRIVE"
        - "OPENCLAW_WORKSPACE"
      config:
        - ".env"
        - "/skills/memory-pro/data/INDEX.json"
        - "/skills/memory-pro/data/state.json"
        - "/skills/memory-pro/v2/eval_queries.json"
        - "/tmp/memory_pro_benchmark.json"
        - "/tmp/memory_pro_hybrid.json"
        - "/tmp/memory_pro_vector.json"
        - "INDEX.json"
        - "args.json"
        - "eval_queries.json"
        - "r.json"
        - "response.json"
        - "state.json"
        - "v2/eval_queries.json"
    primaryEnv: "HOME"
    envVars:
      -
        name: "HOME"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_API_URL"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_BM25_PATH"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_BM25_WEIGHT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_CANDIDATE_POOL"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_CORE_FILES"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_DAILY_SCOPE"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_DATA_DIR"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_DUAL_HIT_BONUS"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_ENABLE_MMR"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_HARD_MIN_SCORE"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_INDEX_PATH"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_LENGTH_NORM_ALPHA"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_LENGTH_NORM_ANCHOR"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_META_PATH"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_MMR_LAMBDA"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_MMR_SIM_THRESHOLD"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_MODE"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_PORT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RECENCY_HALF_LIFE_DAYS"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RECENCY_WEIGHT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_API_KEY"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_BLEND"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_ENDPOINT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_MODEL"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_PROVIDER"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_SAMPLE_PCT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_TIMEOUT_MS"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_TOPN"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_SCOPE_STRICT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_SENTENCES_PATH"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_TIMEOUT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_VECTOR_WEIGHT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "OPENCLAW_HOME"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "OPENCLAW_NETWORK_DRIVE"
        required: false
        description: "Optional network drive/docs root."
      -
        name: "OPENCLAW_WORKSPACE"
        required: true
        description: "Credential used by memory-pro."
---

# Memory Pro (v2)

This skill provides semantic search over your memory files using a local vector database.

## Architecture (v2)

- **Service**: Runs as a `systemd` user service (`memory-pro.service`).
- **Port**: `8001` (hardcoded for stability).
- **Engine**: FAISS + Sentence-Transformers (`all-MiniLM-L6-v2`).
- **Data Source**: 
  - Daily logs: `${OPENCLAW_WORKSPACE}/memory/*.md`
  - Core files: `MEMORY.md`, `SOUL.md`, `STATUS.md`, `AGENTS.md`, `USER.md` (from workspace root).
- **Index**: Stored in `${OPENCLAW_WORKSPACE}/skills/memory-pro/v2/memory.index`.

## Usage

### 1. Semantic Search (Recommended)
Use the python script to query the running service.

```bash
# Basic search
python3 scripts/search_semantic.py "What did I do yesterday?"

# JSON output
python3 scripts/search_semantic.py "project updates" --json
```

### 2. Manual Index Rebuild
The service automatically rebuilds the index on restart. To force an update:

```bash
systemctl --user restart memory-pro.service
```
*Note: Service restart takes ~15-20 seconds to rebuild index and load models. The client script has auto-retry logic.*

### 3. Service Management

```bash
# Check status
systemctl --user status memory-pro.service

# Stop service
systemctl --user stop memory-pro.service

# View logs
journalctl --user -u memory-pro.service -f
```

## Troubleshooting

### "Connection failed"
- The service might be stopped or restarting.
- Check status: `systemctl --user status memory-pro.service`.
- If restarting, wait 15 seconds. The client script retries automatically for up to 20s.

### "Index size mismatch"
- This means `memory.index` and `sentences.txt` are out of sync.
- **Fix**: Restart the service. The startup script `start.sh` automatically runs `build_index.py` to fix this consistency issue before starting the API.

### "Address already in use"
- Port 8001 is taken by a zombie process.
- **Fix**: `kill $(lsof -t -i:8001)` then restart service.
