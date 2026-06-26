# Changelog

## v1.2.0 — 2026-03-03

### Added

- **`api_key` field in config** — store the embedding API key directly in `pgmemory.json` so scripts work with zero env var setup. Setup wizard prompts to paste the key; it's stored as `embeddings.api_key`. Resolves in order: config `api_key` → env var → error.
- **Setup wizard prompts for API key** — if key isn't in env or config, wizard asks "Paste your API key or leave blank". Key is stored in config for all future queries automatically.
- **No more `VOYAGE_API_KEY=...` prefixes** — startup commands in generated AGENTS.md blocks no longer require env var prefixes; key comes from config transparently.

### Changed

- All scripts (`query_memory.py`, `write_memory.py`, `setup.py`) resolve API key from config first, env var second

## v1.1.0 — 2026-03-03

### Changed

- **pgmemory replaces markdown file reads at startup** — loading MEMORY.md + daily files dumps thousands of lines into context; pgmemory returns the 20 most relevant memories via semantic search, far faster and more focused. AGENTS.md startup now says "query pgmemory instead of reading markdown files"
- **AGENTS.md integration is now startup-mandatory** — setup and `--sync-agents` inject pgmemory startup steps directly into the "Every Session" numbered list in AGENTS.md, so agents run memory queries before every task (not just when they remember to)
- **Smarter injection** — `inject_startup_into_agents_md()` finds the last numbered startup list in AGENTS.md and appends pgmemory as the next step in-place, rather than only appending to end of file
- **Section marker** — pgmemory blocks in AGENTS.md are tagged with `<!-- pgmemory:section -->` and `<!-- pgmemory:startup -->` so re-runs are idempotent and the section is easy to find/update
- **Clearer instructions** — startup block now explicitly states "This is not optional" and explains why (decisions, constraints, infrastructure facts)
- **`scaffold_agents_md` generates reference + startup separately** — `startup_steps()` for injection, `scaffold_agents_md()` for the full reference section

### Philosophy

- **pgmemory is the default** — used by default for all reads and writes
- **Markdown is the automatic backup** — always also write a brief note to `memory/YYYY-MM-DD.md`; this ensures memories survive if the DB is unavailable. Full detail in pgmemory, brief backup in markdown.

### Added

- **`--check` flag** on `query_memory.py` — fast connectivity check (exit 0=ok, 2=unreachable). Prints a clear `⚠️ pgmemory UNREACHABLE` warning with host, error, and fallback instructions. 5-second connect timeout prevents hanging on unreachable hosts.
- **Startup step now runs `--check` first** — if it fails with exit 2, agent warns the user and falls back to markdown files rather than silently continuing

### Fixed

- DB connection now uses `connect_timeout=5` to fail fast instead of hanging on unreachable hosts
- Install no longer checks `if "pgmemory" in content` (too broad — matches comments); now checks for `<!-- pgmemory:section -->` marker

## v1.0.0 — 2026-03-02

Initial release.

### Features

- **Persistent semantic memory** — PostgreSQL + pgvector backend; memories survive session compaction
- **Three scripts** — `setup.py`, `write_memory.py`, `query_memory.py`
- **Wizard** — interactive setup with Docker detection/install, DB provisioning, embedding provider config, AGENTS.md scaffolding, cron setup
- **Migrations** — versioned SQL files with checksum verification, rollback support, idempotent on existing schemas
- **Decay + reinforcement** — relevance scores decay by category/importance, boosted by access frequency; archive not delete
- **Doctor** — full system health check including dimension mismatch detection, index health, cap warnings
- **Validate** — config pre-flight, no DB connection needed
- **`--sync-agents`** — auto-scaffold pgmemory into all OpenClaw agent workspaces from `openclaw.json`
- **Harvest** — pull important findings from sub-agent namespaces into primary namespace
- **Embedding providers** — Voyage AI (default), OpenAI, Ollama (local)
- **Archive table** — expired/evicted/decayed memories move to `archived_memories`, never hard deleted; `restore_on_access` brings them back automatically
- **Sane defaults** — minimal config is 3 fields; all options configurable
