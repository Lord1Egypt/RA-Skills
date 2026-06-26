# Setup & Environment Reference

## Service Requirements

| Service | Default URL | Purpose |
|---------|------------|---------|
| FalkorDB | `172.18.0.1:6379` | Graph database (temporal KG storage) |
| NVIDIA Ollama | `172.18.0.1:11436` | Embedding models (nomic-embed-text, mxbai-embed-large) |
| AMD Ollama | `172.18.0.1:11437` | LLM for entity extraction (gemma4:e4b) |

**Minimum viable**: FalkorDB + one Ollama instance with `nomic-embed-text` loaded.
The AMD/LLM endpoint is only needed for write path (entity extraction). Reads work with embeddings only.

## Python Dependencies

```bash
pip install graphiti-core falkordb sentence-transformers httpx
```

The container's `/home/node/.local` layer is ephemeral — reinstall after restart:
```bash
export PATH=$PATH:/home/node/.local/bin
curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python3 /tmp/get-pip.py --user --break-system-packages
pip3 install --user --break-system-packages graphiti-core falkordb sentence-transformers
```

## Ollama Models

Pull these before first use:

```bash
# Embeddings (NVIDIA Ollama)
docker exec ollama-modern-gpu ollama pull nomic-embed-text
docker exec ollama-modern-gpu ollama pull mxbai-embed-large

# LLM for entity extraction (AMD Ollama — or NVIDIA if no AMD)
docker exec ollama-amd-rx6800 ollama pull gemma4:e4b

# Verify
curl -s http://172.18.0.1:11436/api/tags  # should show nomic + mxbai
curl -s http://172.18.0.1:11437/api/tags  # should show gemma4:e4b
```

If you only have one Ollama instance, set both `OLLAMA_URL` and `AMD_OLLAMA_URL`
to the same endpoint in `config.py`, and use any capable instruction-following model
for `LLM_MODEL` (e.g., `llama3.2`, `mistral`, `gemma3`).

## FalkorDB Setup

Using Docker:
```bash
docker run -d --name falkordb -p 6379:6379 falkordb/falkordb
```

Or use an existing Redis-compatible FalkorDB instance.

## First-Time Initialization

```bash
# 1. Check config.py matches your endpoints
cat memory-upgrade/config.py

# 2. Run smoke test
python3 memory-upgrade/smoke_test.py

# 3. Seed initial memories
python3 memory-upgrade/phase3_ingest.py      # MEMORY.md + daily notes
python3 memory-upgrade/phase6_full_ingest.py  # broader workspace docs

# 4. Validate read path
python3 memory-upgrade/phase4_query_test.py

# 5. Create vector index (only needed once per graph)
python3 memory-upgrade/phase5_vector_index.py
```

## Graph Names

The FalkorDB graph name equals the `group_id` passed during ingestion.
Default: `workspace`. Always use consistent `group_id` and `init_graphiti("workspace")`.

To list all graphs:
```python
import falkordb
r = falkordb.FalkorDB(host='172.18.0.1', port=6379)
print(r.list_graphs())
```

## Adapting to Different Environments

| Setting | Where to change |
|---------|----------------|
| Ollama URLs | `config.py` → `OLLAMA_URL`, `AMD_OLLAMA_URL` |
| LLM model | `config.py` → `LLM_MODEL` |
| Embedding model | `config.py` → `EMBED_GENERAL` |
| FalkorDB host/port | `config.py` → `FALKORDB_HOST`, `FALKORDB_PORT` |
| Graph name | `setup_graphiti.py` → `LIVE_GRAPH` |
| Routing threshold | `router.py` → `CONFIDENCE_THRESHOLD` |
| Domain centroids | `checkpoints/centroids.json` (auto-generated) |
