---
name: knowledge-lib
displayName: Knowledge Lib
description: >
  Personal knowledge wiki manager. Organizes notes into structured .md wiki
  with concept pages, summaries, and cross-references.
  Activate when user says "add to wiki", asks to query knowledge base,
  or mentions "knowledge base".
version: 1.2.0
metadata:
  permissions:
    - file:read
    - file:write
  behavior:
    network: none
    telemetry: none
    credentials: none
---

# Knowledge Lib

Personal knowledge wiki at `~/.openclaw/workspace/knowledge/`.

## Quick Start

1. User says **"add to wiki"** with a link or file → agent saves + summarizes it
2. User says **"look up X"** → agent searches wiki pages and answers with citations
3. User says **"wiki status"** → agent reports wiki health stats

## Directory Structure

```
knowledge/
├── raw/<category>/        # Source documents (read-only)
├── wiki/
│   ├── index.md           # Content catalog (refreshed on every write)
│   ├── log.md             # Chronological operation log (append-only)
│   ├── concepts/          # Concept pages (PascalCase: Self-Distillation.md)
│   ├── summaries/         # Document summaries (date-slug.md)
│   └── analyses/          # Query writeback results (date-query-slug.md)
└── output/                # Generated outputs (slides, charts)
```

Categories: `ai-llm`, `engineering`, `products`, `startups`

## Schema Conventions

### Frontmatter (all wiki pages)

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
related: [[Concept-A]], [[Concept-B]]
sources: N
tags: [tag1, tag2]
status: active        # active | superseded | disputed
---
```

### Naming Rules
- **Concepts**: PascalCase → `Self-Distillation.md`, `RAG.md`
- **Summaries**: `YYYY-MM-DD-<slug>.md`
- **Analyses**: `YYYY-MM-DD-query-<slug>.md`

### Cross-references
- Wiki-links: `[[ConceptName]]` (Obsidian compatible)
- Source citation: `[[YYYY-MM-DD-summary-slug]]`
- Dispute mark: `⚠️ [[ConceptName#disputed]]` when new data challenges old claims

### Status Lifecycle
- `active` → current knowledge
- `superseded` → newer source proved this wrong (keep with link to replacement)
- `disputed` → conflicting evidence, needs resolution

## Content Type Guide

When user sends a link or document, classify by content type:

| Type | Indicators |
|------|-----------|
| Paper | arxiv.org, paperswithcode.com, huggingface.co/papers |
| Project | github.com repos |
| Blog | medium.com, substack.com, tech blogs |
| Company post | openai.com/blog, anthropic.com/news, deepmind.google |
| Product | producthunt.com, techcrunch.com |

Action: save to `raw/<category>/`, then summarize and link concepts.

## Workflow

### Save (trigger: user command "add to wiki")

1. Read the provided content or link
2. Save to `raw/<category>/YYYY-MM-DD-<slug>.md` with frontmatter
3. Log in `log.md`: `## [YYYY-MM-DD] save | <Title> | <category>`
4. Proceed to Summarize step

### Summarize (trigger: after save)

1. Read the raw document, identify key points
2. Write summary to `wiki/summaries/YYYY-MM-DD-<slug>.md`
3. **Contradiction check**: Compare new claims against existing `active` concepts
   - If conflict: mark old as `disputed`, link both pages
   - If reinforcement: update existing page, increment `sources`
4. Create or update `wiki/concepts/<Concept>.md`
5. Add `[[backlinks]]` between related concept pages
6. Refresh `index.md`
7. Log: `## [YYYY-MM-DD] summarize | <Title> | touched N pages`

### Query (trigger: user asks "look up X")

1. Search `wiki/concepts/` and `wiki/summaries/` for matches
2. Answer with source citations
3. If the answer is substantial → write to `wiki/analyses/` and update links
4. Log: `## [YYYY-MM-DD] query | <Topic> | sources: N`

### Health Check (trigger: user says "wiki status")

1. Count unprocessed raw docs, orphan pages, missing frontmatter
2. Report stats summary
3. Optionally do deep-lint: contradiction scan, stale claims, missing concepts

## Quick Commands

| User says | Action |
|-----------|--------|
| "add to wiki" + link/file | save → summarize |
| "look up X" | query wiki |
| "wiki status" | health check |
| "deep check" | full lint |

## Templates

### Concept Page

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
related: [[Concept-A]], [[Concept-B]]
sources: N
tags: [category]
status: active
---
# Concept Name

## Definition
One sentence.

## Key Points
- ...

## Contradictions
- ⚠️ [[YYYY-MM-DD-summary-slug]] challenges: <brief>

## Sources
- [[YYYY-MM-DD-summary-slug]]
```

### Summary Page

```markdown
---
source: <URL>
category: <category>
concepts: [[Concept-A]], [[Concept-B]]
imported: YYYY-MM-DD
---
# Title

## Core Points
- ...

## Key Data
- ...
```

### Analysis Page

```markdown
---
created: YYYY-MM-DD
query: <Original question>
concepts: [[Concept-A]], [[Concept-B]]
sources: N
---
# <Question Summary>

## Answer
...

## Key Insights
- ...
```
