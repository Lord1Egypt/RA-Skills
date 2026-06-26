# Project Scaffold Reference

How to initialize the methodology in a new project or restructure a bloated one.

## For New Projects: init-project-structure

When starting a fresh project, the methodology needs:

### 1. Project memory file (CLAUDE.md)

A slim router containing:
- Project name and description
- Hard rules (non-negotiable)
- Branch → environment topology
- Where to find things (pointer index)
- Common commands
- Today's state
- Housekeeping protocol

### 2. Local env file (CLAUDE.local.md)

Gitignored, contains:
- Connection strings for all environments
- API keys and credentials (never commit)
- Railway service names
- Cross-env discrepancies and gotchas

### 3. Docs tree

```
docs/
├── recaps/           # Session recaps
├── plans/            # Feature plans
├── architecture/     # Architecture docs (overview, database, auth, etc.)
├── features/         # Feature-specific docs
├── operations/       # Operations guides, pipeline docs
└── scripts/          # Script catalog
```

### 4. Contract docs

- `TECHNICAL-DOCUMENTATION.md` — architecture decisions, schema, API reference
- `FUNCTIONAL-SPECIFICATIONS.md` — user-facing feature descriptions, flows

### 5. Housekeeping protocol

Rules for keeping the docs tree from rotting over time. The protocol is embedded in CLAUDE.md and covers:
- When to update which doc
- How stat tables work (STATE-SNAPSHOT.md, replace don't append)
- Drift checks before session end
- Quarterly hygiene pass

### Topology question

Ask the user: **2 environments (staging + production) or 3 (staging + canary + production)?**
Default to 2. Canary is only needed for large migrations.

## For Existing Projects: slim-claude-md

When CLAUDE.md has grown past ~300 lines:

1. Extract topical content into `docs/architecture/*.md`, `docs/features/*.md`
2. Move credentials and URLs to `CLAUDE.local.md` (gitignored)
3. Strip CLAUDE.md down to: hard rules, topology, pointer index, today's state
4. Add housekeeping protocol to prevent re-bloating

### When to slim

- CLAUDE.md > 300 lines
- User reports "Claude pointed at the wrong environment"
- User asks "where do I find X?"
- Session starts showing credential-asking patterns

### When NOT to slim

- Project is in active development (slipstream is fine)
- Project is a temporary experiment
- Only one person works on it and they're comfortable with the verbosity
