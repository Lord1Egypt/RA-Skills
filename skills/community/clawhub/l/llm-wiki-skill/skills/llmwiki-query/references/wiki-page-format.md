# Wiki Page Format

All `_wiki/` pages follow this standard format.

## File naming

- Lowercase kebab-case: `machine-learning.md`, `auth-flow.md`
- One concept per file
- Place in `_wiki/` root (subdirectories allowed for large wikis)

## Full template

```markdown
---
title: Concept Name
type: concept
tags: [tag1, tag2]
sources: [origin-file.md or https://url]
updated: YYYY-MM-DD
---

Synthesized explanation in your own words — not a copy of the source.
One to three paragraphs covering the core idea.

## Key Insights
- Insight one
- Insight two

## Related
- [[other wiki page]]
- [[another concept]]
```

## Types

| type | use for |
|---|---|
| `concept` | ideas, patterns, principles |
| `entity` | people, tools, systems, projects |
| `source` | summaries of books, articles, docs |
| `synthesis` | cross-cutting analysis across multiple concepts |

## Rules

- Every page must have at least one `[[wikilink]]` in the Related section
- `sources` must list the origin of the knowledge (file path or URL)
- `updated` must be refreshed whenever the page is edited
- Stubs are allowed — orphans are not
