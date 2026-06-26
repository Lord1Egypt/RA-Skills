# Getting Started with an LLM Wiki

Use this reference when a user wants a simple starting point for a new markdown knowledge wiki.

## Minimal starter layout

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

## Minimal `schema.md`

```markdown
# Wiki Schema

## Purpose
Describe what this wiki is for and what kinds of source material belong in it.

## Source of truth
Treat files in `sources/` as immutable inputs. Update compiled knowledge in `pages/`, `index.md`, and `log.md`.

## Page types
- topic: broad subject pages
- concept: reusable ideas or abstractions
- entity: people, companies, products, places, organizations
- analysis: comparisons, syntheses, memos, decisions
- source: summaries of individual source documents

## Naming rules
Use stable, human-readable titles. Prefer one canonical page per concept or entity.

## Citation rules
Link related pages with wiki-links. List supporting source pages in a `Sources` section.

## Workflows
- ingest: summarize a source and update affected pages
- query: answer from the wiki first, then file durable analysis back into the wiki
- lint: check for contradictions, stale claims, missing links, and orphan pages
```
```

## Minimal `index.md`

```markdown
# Index

## Topics

## Concepts

## Entities

## Analyses

## Sources
```
```

## Minimal `log.md`

```markdown
# Log
```
```

## First-ingest checklist

When starting a fresh wiki:
1. create `schema.md`
2. create empty `index.md`
3. create empty `log.md`
4. ingest one high-value source
5. create only the pages that are clearly justified
6. keep summaries short and links explicit

## Good default habits

- prefer updating existing pages over spraying new ones everywhere
- make uncertainty visible
- keep pages pleasant for humans to browse
- store durable syntheses as analysis pages instead of leaving them trapped in chat history
