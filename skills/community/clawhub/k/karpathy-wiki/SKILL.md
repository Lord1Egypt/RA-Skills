---
name: karpathy-wiki
description: Build, maintain, query, and lint a persistent markdown knowledge wiki that sits between raw sources and final answers. Use when managing a personal or team wiki, ingesting notes, articles, transcripts, reports, or research into a structured knowledge base, updating index and log pages, creating or revising topic, entity, concept, source, or analysis pages, answering questions from an existing wiki, or checking a wiki for contradictions, stale claims, missing links, orphan pages, duplicate pages, and schema drift. Best for Obsidian-friendly, plain markdown, or git-backed wikis where the agent should incrementally compile knowledge instead of re-deriving it from raw documents on every query.
---

# Karpathy Wiki

Maintain a persistent markdown wiki that compiles knowledge over time. Treat raw sources as immutable, treat the wiki as the maintained artifact, and keep structure and conventions consistent so future sessions can continue the work.

## Core model

Operate with three layers:

1. `raw sources/` or equivalent input area, read-only source material
2. `wiki/` or equivalent markdown knowledge base, editable compiled knowledge
3. `schema` document that defines folder layout, naming, citation style, and workflows

Prefer updating the wiki over answering from scratch. When useful work is produced during analysis or Q&A, file the result back into the wiki as a reusable page.

## Default wiki structure

If the user does not already have a schema, propose a simple markdown-first layout like:

```text
wiki/
  index.md
  log.md
  schema.md
  sources/
  pages/
    topics/
    concepts/
    entities/
    analyses/
```

Adapt to the user's existing layout instead of forcing this one.

## Operating modes

### 1. Ingest

Use when a new source is added.

Workflow:

1. Read the source
2. Identify key topics, entities, concepts, dates, claims, and open questions
3. Create or update a source summary page if the wiki uses source pages
4. Update affected topic, entity, concept, or analysis pages
5. Add or repair internal links
6. Update `index.md`
7. Append a concise entry to `log.md`
8. Record uncertainties, contradictions, or follow-up questions explicitly

During ingest, prefer touching a small number of clearly relevant pages over creating a large number of weak pages.

Create a new page only when at least one of these is true:
- the concept or entity is likely to recur
- the page would receive meaningful links from multiple places
- the content would otherwise make an existing page too broad or noisy

Otherwise, expand an existing page.

### 2. Query

Use when the user asks a question against the wiki.

Workflow:

1. Read `index.md` first when available
2. Identify the most relevant wiki pages
3. Synthesize from the wiki before falling back to raw sources
4. Cite the wiki pages and, when appropriate, the underlying sources
5. If the answer creates durable value, save it as a new or updated analysis page
6. Update `index.md` if a new page is created
7. Append to `log.md` if the wiki treats queries as first-class events

Prefer answers that preserve distinctions between:
- facts directly supported by sources
- synthesis across multiple pages
- speculation or open questions

### 3. Lint

Use when checking wiki health.

Look for:
- orphan pages with few or no inbound references
- duplicate pages with overlapping scope
- stale claims superseded by newer sources
- contradictions between pages
- missing cross-links
- important concepts mentioned repeatedly without their own page
- schema drift, inconsistent titles, inconsistent frontmatter, broken naming
- analysis pages that should have been linked from topic/entity pages but were not

When linting, prefer producing an actionable list of fixes grouped by severity:
- critical consistency issues
- likely quality improvements
- optional structural improvements

## Page conventions

Favor concise pages with clear structure. A useful default shape is:

```markdown
# Page Title

## Summary
Short synthesis of what this page is about.

## Key points
- Bullet points of durable knowledge

## Details
Longer notes, evidence, chronology, or structured sections

## Related
- [[Other Page]]

## Sources
- [[Source Page A]]
- [[Source Page B]]
```
```

If the wiki uses frontmatter, keep it minimal and consistent. Good optional fields include:
- `type`
- `aliases`
- `status`
- `updated`
- `source_count`
- `tags`

Do not invent elaborate metadata unless the user actually benefits from it.

## Naming and linking rules

Use stable, human-readable file names.

Prefer:
- one canonical page per concept/entity/topic
- redirects or aliases only when the wiki supports them
- explicit wiki-links between related pages
- consistent singular vs plural naming

When unsure whether two pages should merge, keep both only if they have clearly different scope. Otherwise merge and leave one canonical page.

## Index and log rules

### `index.md`

Treat `index.md` as the navigational catalog.

Include:
- page link
- one-line summary
- optional grouping by category
- optional source counts or update dates if the wiki uses them

Keep it skimmable. It should help future sessions decide what to read next.

### `log.md`

Treat `log.md` as append-only chronology.

Use a parseable heading style such as:

```markdown
## [2026-04-12] ingest | Source title
```

Keep entries concise:
- what was ingested, queried, or linted
- which pages were created or updated
- any unresolved issues

## Quality bar

A good wiki update should:
- preserve source fidelity
- surface contradictions instead of hiding them
- strengthen cross-links
- reduce future work
- make later questions cheaper to answer

Do not overwrite uncertainty with confident prose. When the evidence is mixed, say so clearly.

## Working with existing wikis

If a wiki already exists:

1. Inspect its schema, folder layout, and naming style
2. Follow the existing conventions unless they are clearly harmful
3. Repair inconsistencies gradually instead of rewriting the whole wiki at once
4. Propose larger schema changes before making them

## Obsidian-friendly guidance

For Obsidian-style vaults:
- prefer markdown files and wiki-links like `[[Page Name]]`
- keep filenames readable
- avoid fragile generated syntax unless the user already uses it
- if frontmatter exists, preserve formatting and field order when practical
- make pages pleasant to browse by humans, not only optimized for machine parsing

## Deliverables by task

### For ingest requests
Deliver:
- source summary or source page update
- updated related pages
- `index.md` update
- `log.md` entry
- short note on contradictions or open questions

### For query requests
Deliver:
- answer with citations
- optional durable analysis page if worth keeping
- any relevant index or log updates

### For lint requests
Deliver:
- prioritized issue list
- concrete proposed edits
- optional patch plan for high-value fixes

## References

- Read `references/getting-started.md` when the user needs a minimal starter schema for a new wiki.
- Read `references/wiki-patterns.md` for core page templates and structural heuristics.
- Read `references/ingest-patterns.md` when ingesting a new source into the wiki.
- Read `references/query-patterns.md` when answering questions from the wiki or deciding whether to save a durable analysis page.
- Read `references/lint-checklist.md` when checking the wiki for contradictions, stale claims, weak links, duplicates, or structural drift.
