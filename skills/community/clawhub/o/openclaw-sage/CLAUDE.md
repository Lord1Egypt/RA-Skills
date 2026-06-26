# CLAUDE.md

openclaw-sage is an OpenClaw skill that gives AI agents access to OpenClaw documentation via shell scripts and a Python BM25 search engine.

## Key files

| File | Role |
|---|---|
| `scripts/lib.sh` | Shared constants and functions — sourced by every script |
| `scripts/bm25_search.py` | BM25 ranking engine — called by `build-index.sh` and `search.sh` |
| `SKILL.md` | Agent-facing tool reference |
| `AGENTS.md` | Quick-reference guide for AI agents using this skill |
| `docs/coding-conventions.md` | Full coding conventions — read before adding or modifying code |

## Critical rules

- **Always source `lib.sh`** — never redefine `is_cache_fresh`, `fetch_markdown`, `parse_version_flag`, `CACHE_DIR`, `VERSION_CACHE_DIR`, or `DOCS_BASE_URL` in a script.
- **Never hardcode** `~/.cache/...` or `https://docs.openclaw.ai` — use `$CACHE_DIR` and `$DOCS_BASE_URL`.
- **Every `curl` call must write to `$CACHE_DIR`** — no uncached network requests.
- **stdout is data, stderr is diagnostics** — progress/warning messages go to `>&2`.
- **Use Python for JSON** — never build JSON with bash string concatenation.
- **No new required dependencies** — `bash` and `curl` are the only hard requirements.
- **Use `VERSION_CACHE_DIR` for doc/index paths** — never use `$CACHE_DIR` directly for doc files; always call `parse_version_flag` first so `VERSION_CACHE_DIR` is set.

## Full conventions

See [`docs/coding-conventions.md`](docs/coding-conventions.md).
