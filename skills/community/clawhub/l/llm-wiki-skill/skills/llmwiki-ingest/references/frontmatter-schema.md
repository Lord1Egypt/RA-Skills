# Frontmatter Schema

Required YAML frontmatter for all `_wiki/` pages.

## Fields

| Field | Required | Type | Description |
|---|---|---|---|
| `title` | yes | string | Human-readable concept name |
| `type` | yes | enum | `concept`, `entity`, `source`, `synthesis` |
| `tags` | yes | list | Relevant keywords for search and grouping |
| `sources` | yes | list | Origin files or URLs this page was derived from |
| `updated` | yes | ISO date | Last edit date (`YYYY-MM-DD`) |

## Example

```yaml
---
title: Retrieval-Augmented Generation
type: concept
tags: [llm, rag, knowledge-retrieval]
sources: [https://arxiv.org/abs/2005.11401]
updated: 2026-04-07
---
```

## Validation rules

- `title` must match the page's primary concept (not the filename)
- `type` must be one of the four allowed values
- `tags` must have at least one entry
- `sources` must have at least one entry (use `[]` only for the index page)
- `updated` must be refreshed on every edit
