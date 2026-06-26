# Publishing to ClawHub

## Packaging the Skill

From the workspace root:
```bash
python3 /app/skills/skill-creator/scripts/package_skill.py \
  skills/public/graph-rag-memory \
  skills/dist/
```

This creates `skills/dist/graph-rag-memory.skill` — a validated zip archive ready for distribution.

## ClawHub Submission

1. Go to https://clawhub.ai
2. Create an account / log in
3. Upload `graph-rag-memory.skill`
4. Fill in the listing:

**Name:** `graph-rag-memory`

**Tagline:** Persistent temporal knowledge graph memory for OpenClaw agents

**Description:**
> Gives your OpenClaw agent persistent, queryable long-term memory using a Graphiti temporal
> knowledge graph backed by FalkorDB. Facts are extracted from conversations and documents via
> a local LLM (Ollama), stored as typed entities and relationships, and retrieved via hybrid
> BM25 + cosine similarity search with domain-expert routing.
>
> Inspired by RouterRetriever (AAAI 2025): routes queries to domain-specialized embedding
> models (personal, technical, research, project, episodic) for better retrieval precision
> than single-model RAG systems.

**Tags:** `memory`, `rag`, `graphiti`, `falkordb`, `ollama`, `knowledge-graph`, `local-llm`

**Requirements:**
- FalkorDB instance (Docker: `docker run -d -p 6379:6379 falkordb/falkordb`)
- Ollama with `nomic-embed-text` loaded
- Ollama with an instruction model for entity extraction (gemma4:e4b recommended)
- Python 3.11+

**GitHub:** https://github.com/jebadiahgreenwood/openclaw-workspace

## Versioning

Follow semver: `MAJOR.MINOR.PATCH`
- **0.1.0** — Initial release (BM25 + vector hybrid, 6-domain routing, FalkorDB backend)
- **0.2.0** — When Graphiti fork adds multi-vector storage (mxbai-embed-large full support)
- **0.3.0** — When live write hook is integrated into OpenClaw session pipeline
- **1.0.0** — Stable API, tested on multiple deployments, ClawHub featured

## User Configuration Guide (for ClawHub README)

After installing the skill, users need to:

1. **Start FalkorDB:**
   ```bash
   docker run -d --name falkordb -p 6379:6379 falkordb/falkordb
   ```

2. **Pull embedding model:**
   ```bash
   ollama pull nomic-embed-text
   ```

3. **Pull extraction LLM** (any capable model works):
   ```bash
   ollama pull gemma4:e4b   # recommended — fast, good JSON
   # or: ollama pull llama3.2, mistral, qwen2.5, etc.
   ```

4. **Edit `memory-upgrade/config.py`** with your Ollama URL(s)

5. **First-time setup:**
   ```bash
   python3 memory-upgrade/phase3_ingest.py      # seed from your memory files
   python3 memory-upgrade/phase5_vector_index.py # create vector index
   python3 memory-upgrade/phase4_query_test.py   # validate it works
   ```

6. **Start using it** via the convenience scripts or the Python API.
