# Memory Pro 

## Included
- Core skill instructions
- Search client scripts
- V2 semantic search API/server code
- Hybrid retrieval / BM25 / rerank helpers
- Example env file and requirements
- Validation and benchmark helpers

## Removed / Excluded
- Personal memory content
- Generated FAISS indexes
- `sentences.txt`
- `memory_meta.jsonl`
- Runtime logs / caches / `__pycache__`
- Real user ids, emails, paths, and secret values

## Placeholder conventions
- `${OPENCLAW_HOME}` = user OpenClaw home
- `${OPENCLAW_WORKSPACE}` = workspace root
- `${OPENCLAW_NETWORK_DRIVE}` = optional network drive/docs root
- `${HOME}` = user home
- `<REDACTED>` / `<API_KEY>` / `<TOKEN>` = secrets removed

## Notes for adopters
1. Review all paths before running.
2. Create your own `.env` using the environment variable list in `SKILL.md`.
3. Rebuild the index from your own memory/docs corpus.
4. Do not reuse any bundled state from another user.

## Export manifest
- `SKILL.md`
- `scripts/search_semantic.py`
- `scripts/index.py`
- `scripts/search.py`
- `v2/main.py`
- `v2/start.sh`
- `v2/build_index.py`
- `v2/preprocess.py`
- `v2/retrieval_hybrid.py`
- `v2/rerank.py`
- `v2/validate_phase1.sh`
- `v2/eval_queries.json`
- `v2/benchmark.py`
