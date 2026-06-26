---
name: llm-wiki
description: Build and maintain a local Markdown knowledge wiki that compounds over time instead of relying on one-shot RAG retrieval. Use when the user wants to turn notes, documents, transcripts, chat logs, research material, or project context into an LLM-maintained wiki/second-brain; when setting up an Obsidian-friendly knowledge base; or when defining ingest, query, reindex, and lint workflows for a personal or team knowledge vault.
---

# LLM Wiki

## Overview

Build a local-first, Markdown-based wiki where the human curates sources and asks questions, while the agent maintains the compiled knowledge pages, links, summaries, and indexes.

Prefer this pattern when the goal is cumulative understanding across many sessions, files, and questions — not just answering one query from raw documents.

## Core Idea

Treat the wiki as a compiled artifact, not the raw archive.

Use three layers:

1. **Raw sources**: immutable inputs such as notes, PDFs, transcripts, copied text, logs, screenshots, and chat exports.
2. **Wiki pages**: curated Markdown pages written and maintained by the agent.
3. **Schema/rules**: lightweight conventions for page layout, naming, linking, and maintenance.

The human focuses on sourcing, exploration, and direction.
The agent handles summarizing, cross-referencing, page updates, consolidation, and bookkeeping.

## Recommended Directory Shape

Adapt the exact layout to the user’s workspace, but prefer a structure like:

```text
knowledge/
  raw/
    inbox/
    docs/
    transcripts/
    web/
  wiki/
    concepts/
    people/
    projects/
    timelines/
    sources/
  logs/
    knowledge-log.md
  INDEX.md
  SCHEMA.md
```

Guidelines:

- Keep `raw/` append-only when practical.
- Keep `wiki/` human-readable and link-heavy.
- Keep `INDEX.md` short and navigational.
- Keep `SCHEMA.md` focused on conventions, not prose.

## Operation Modes

### 1. Ingest

Use when new material arrives.

Goal: convert raw inputs into durable wiki structure.

Steps:

1. Inspect new source material.
2. Decide whether it belongs in `raw/` unchanged.
3. Extract stable entities: concepts, people, projects, decisions, methods, events, open questions.
4. Create or update wiki pages.
5. Add backlinks and related-page links.
6. Update `INDEX.md` if navigation changed.
7. Append a concise entry to the knowledge log.

Prefer updating existing pages over creating near-duplicates.

### 2. Query

Use when the user asks a question about the knowledge base.

Steps:

1. Search the wiki first.
2. Read the most relevant compiled pages.
3. Fall back to raw sources only if the wiki is missing detail.
4. Answer the question.
5. If the answer revealed a gap, update the wiki before finishing when appropriate.

Prefer reading 2–5 good pages over sweeping the entire vault.

### 3. Reindex

Use when the structure has drifted or grown.

Tasks:

- Refresh `INDEX.md`
- Merge overlapping pages
- Rename pages that no longer fit
- Repair broken links
- Normalize tags or page sections
- Split oversized pages when they cover multiple topics

### 4. Lint

Use when the wiki may be internally inconsistent.

Check for:

- duplicate pages for the same concept
- contradictory claims
- stale summaries after new evidence
- orphan pages with no inbound or outbound links
- pages that lack source pointers
- vague claims that should be marked as uncertain or disputed

When high-stakes accuracy matters, preserve disagreement explicitly instead of forcing one synthetic summary.

## Page Design Rules

Prefer simple Markdown that Obsidian and other editors render well.

For most concept pages, use sections like:

```markdown
# Topic Name

## Summary
A short stable summary.

## Key points
- ...

## Relationships
- Related: [[Other Page]]
- Depends on: [[Another Page]]

## Sources
- [[Source - Interview 2026-04-06]]
- raw/transcripts/interview-2026-04-06.md

## Open questions
- ...
```

Rules:

- Put the most reusable summary near the top.
- Prefer explicit links like `[[Page Name]]` when the vault supports wiki links.
- Separate facts, interpretations, and open questions when ambiguity matters.
- Record provenance whenever practical.
- Avoid decorative formatting and long narrative filler.

## Indexing and Logging

Maintain two special files:

### `INDEX.md`

Use as a map of the vault.

Include:

- major sections
- important hub pages
- canonical names for key topics
- pointers to active or recently changed areas

Do not turn it into a giant dump of every page.

### `logs/knowledge-log.md`

Use as a chronological maintenance trail.

Each entry should briefly record:

- what changed
- why it changed
- which pages were added or updated
- any unresolved ambiguity

Example:

```markdown
## 2026-04-06
- Ingested interview transcript on home networking setup.
- Updated [[OpenClaw 微信 channel 插件项目]] and created [[网络规划偏好]].
- Flagged uncertainty around deployment target and auth flow.
```

## Workflow Heuristics

- Prefer modifying a small number of relevant pages over regenerating the whole wiki.
- Create new pages when a concept is likely to recur.
- Merge pages when names differ but the concept is clearly the same.
- Preserve raw material; do not destroy source context unless the user asks.
- If the wiki disagrees with a source, update the wiki and mark the change.
- If evidence is mixed, preserve the disagreement explicitly.
- Use the wiki as the primary retrieval surface; use raw sources as ground truth.

## Obsidian-Friendly Usage

If the user keeps notes in Obsidian:

- write plain Markdown files
- preserve wikilinks where possible
- prefer stable filenames over clever ones
- keep pages short enough to browse comfortably
- use hub pages for dense topics instead of giant monoliths

Obsidian is the browsing interface; the agent is the maintainer.

## Suggested User Requests That Should Trigger This Skill

Examples:

- “把这些零散笔记整理成知识库”
- “帮我做一个 second brain / wiki”
- “把这些聊天记录沉淀成长期知识”
- “给这个 Obsidian 仓库设计 ingest/query/lint 流程”
- “把原始资料编译成可维护的 Markdown wiki”
- “帮我重构这个知识库结构，减少重复页面”

## Quick Start

For a brand-new vault, initialize the scaffold first:

```bash
python3 scripts/init_wiki.py /path/to/knowledge
```

Add `--force` to overwrite existing scaffold files.

After initialization:

1. review `SCHEMA.md`
2. place or copy source material into `raw/`
3. ask the agent to ingest the material into `wiki/`
4. use query / reindex / lint as the vault grows

## References

Read these bundled references only when needed:

- `references/scaffold.md`: example scaffold for `SCHEMA.md`, `INDEX.md`, and page conventions
- `references/operations.md`: practical checklists for ingest, query, reindex, and lint runs
- `references/publish-notes.md`: short external-facing positioning and use-case wording

## Bundled Script

- `scripts/init_wiki.py`: create a starter wiki vault with directories, hub pages, `INDEX.md`, `SCHEMA.md`, and `logs/knowledge-log.md`
