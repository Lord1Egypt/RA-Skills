# Wiki Knowledge Base - CLAUDE.md

## Overview
This wiki stores research on AI Interpretability and Mechanistic Interpretability, organized following the LLM Wiki pattern (karpathy/442a6bf555914893e9891c11519de94f).

## Directory Structure
```
wiki/
├── entities/              # Entity pages (people, organizations, models)
├── concepts/              # Concept pages (techniques, methods, theories)
├── sources/               # Source summary pages
├── syntheses/            # Cross-source synthesis pages
├── comparisons/          # Comparison analyses
├── overviews/            # Overview/topic pages
├── schema/CLAUDE.md      # This file
├── index.md              # Content catalog
└── log.md                # Operation log

# Source files are stored in the project root's raw/ folder
```

## Conventions

### Page Naming
- Use kebab-case: `circuit-tracing`, `sparse-autoencoder`
- Entities: `claude-35-haiku`, `anthropic`
- Concepts: `attribution-graph`, `feature-steering`
- Sources: Match source filename or use descriptive title

### Frontmatter
All pages should include:
```yaml
---
title: "Page Title"
created: 2026-04-09
tags: [concept, source, entity]
---
```

### Cross-References
Use wiki-style links: `[[wiki/page-name]]`

### Log Format
```
## [YYYY-MM-DD] operation | Title
- Action taken
- Result
```

## Workflows

### Ingest (Adding Sources)
1. Read source document
2. Create source summary in `wiki/sources/`
3. Extract entities → `wiki/entities/`
4. Extract concepts → `wiki/concepts/`
5. Update index.md
6. Log in log.md

### Query
1. Search index.md
2. Read relevant pages
3. Synthesize with citations

### Lint
- Check for broken links
- Find contradictions
- Identify orphan pages