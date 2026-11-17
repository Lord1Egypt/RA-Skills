# Changelog

## v1.0.0

Initial release.

- Read-only mirror of OneNote notebooks into local Markdown + git snapshots (`graph_sync.py` + `html2md.py`)
- Query CLI: `list` / `since` / `week` / `grep` / `fetch` / `diff` (purely local, zero network, zero LLM cost)
- Change detection based on ETag by default, with a `--mode timestamp` fallback
- Periodic reporting flow driven by git history (`references/weekly-report.md`)
- One-time OAuth authorization code flow: `auth_code.py`, token stored under `.auth/` (0600, never committed)
