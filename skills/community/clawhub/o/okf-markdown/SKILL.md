---
name: okf-markdown
description: >-
  Validate Open Knowledge Format (OKF v0.2) Markdown vaults, convert WebVTT (.vtt)
  and SubRip (.srt) speaker-labeled meeting transcripts into deterministic OKF
  session notes, and build [[wiki-link]] relational knowledge graphs for Obsidian,
  Claude MCP, Cursor, and OneMira local context workflows.
---

# OKF Markdown (`okf-markdown`)

Use this skill whenever working with **Open Knowledge Format (OKF v0.2)** Markdown files, converting meeting/interview `.vtt` or `.srt` transcripts into structured Obsidian/Markdown notes, auditing YAML frontmatter schemas, or detecting broken `[[wiki-links]]` and orphan notes.

## Zero-Dependency CLI Commands (`npx`)

Run directly without global installation:

```bash
# 1. Convert a .vtt or .srt transcript into a speaker-attributed OKF v0.2 Markdown note
npx github:onemira-space/okf-markdown ingest ./meeting.vtt \
  --title "Weekly Engineering Sync" \
  --out ./vault/sessions/weekly-sync.md

# 2. Validate YAML frontmatter and link integrity across an Obsidian / OKF directory
npx github:onemira-space/okf-markdown validate ./vault

# 3. Export nodes, edges, broken links, and orphan notes as JSON for RAG / MCP tools
npx github:onemira-space/okf-markdown graph ./vault --out ./graph.json
```

## Canonical OKF v0.2 Frontmatter Rules

1. Every document MUST begin with `---` YAML frontmatter containing:
   - `okf_version`: `"0.2"`
   - `id`: deterministic `<type>/<slug>` identifier (e.g. `"session/2026-11-16-design-review"`)
   - `type`: one of `session`, `meeting`, `topic`, `person`, `project`, `decision`, `note`
   - `title`: non-empty human-readable title
   - `created_at`: ISO-8601 timestamp (`YYYY-MM-DDTHH:mm:ssZ`)
2. Use deterministic `[[entity-slug]]` wiki-links or relative `.md` links when referencing people, projects, and decisions so `buildKnowledgeGraph()` can verify bidirectional graph edges without a cloud database.

## Reference Architecture

- **OKF Local Wiki Specification**: https://onemira.com/docs/daily-use/local-wiki
- **MCP & CLI Agent Workflow**: https://onemira.com/docs/mcp-integration
- **Standalone Hardware Source (`OneMira C1`)**: https://onemira.com/products/c1
