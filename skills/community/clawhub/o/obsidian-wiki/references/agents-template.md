# <Vault Name> — LLM Wiki

Compiled knowledge base maintained by an AI agent, following
[Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Rules

- `raw/` is immutable — drop sources here, never modify existing ones
- `wiki/` is agent-owned — do not edit manually
- `_meta/` is co-owned — propose changes first; edit only after user approval
- `.wiki-meta/` is machine state — do not touch

## Quick Start

1. Drop a file into `raw/`
2. Ask the agent to ingest it
3. Browse `wiki/` in Obsidian (graph view recommended)

## Conventions

- `_meta/schema.md` — page format, naming, wikilink rules
- `_meta/taxonomy.md` — canonical tags

## Agent Workflows

The agent uses scripts from the **obsidian-wiki skill directory** (not the vault).
Refer to the skill's SKILL.md for exact commands and `$VAULT` argument usage.

- **Ingest:** check pending sources → read source → create/update pages → mark ingested → regenerate index
- **Lint:** `wiki-lint.sh "$VAULT"` — run all structural health checks (frontmatter, wikilinks, orphans, stale, tags, wikilink format, markdown structure, unlinked mentions)
- **Fix:** `wiki-lint.sh "$VAULT" --fix` — auto-correct fixable issues (wikilink format, markdown structure, unlinked mentions)
- **Cross-link:** `wiki-crosslink.py "$VAULT"` — find unlinked mentions; `--fix` to auto-add wikilinks
- **Graph:** `wiki-graph.py "$VAULT" --stats` — hub/orphan/articulation point analysis; default exports `.wiki-meta/graph.json`
- **Search:** `wiki-search.sh "$VAULT" "query"` — semantic search via qmd if available, grep fallback
- **Log:** append to `wiki/log.md` after each ingest session
- **Reports:** populate `wiki/reports/` with dashboards during maintenance
