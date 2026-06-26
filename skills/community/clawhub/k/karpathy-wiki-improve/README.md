# karpathy-wiki-improve

OpenClaw skill implementing Andrej Karpathy's LLM Wiki pattern — a persistent markdown knowledge wiki with full ingest/query/relink/lint/DeepResearch pipeline.

## What It Does

- **Ingest**: Turn raw bookmarks/links into structured wiki pages with bidirectional links
- **Query**: Answer questions by reading wiki first, then web search to supplement
- **Relink**: Auto-discover and establish page relationships
- **Lint**: Health-check the knowledge graph (orphans, dangling refs, one-way links)
- **Deep Research**: Fill knowledge gaps with targeted search + ingest

## Quick Start

```bash
npx clawhub install zhangmengyang/karpathy-wiki-improve
```

Then in OpenClaw:

```
organize my bookmarks on Go
research MySQL indexing
run lint on my wiki
relink
```

## Wiki Structure

```
wiki/
├── raw/sources/      # immutable original sources
├── wiki/
│   ├── entities/     # people, products, companies, sites
│   ├── concepts/     # tech, theory, methodology
│   ├── comparisons/   # A vs B analysis
│   └── synthesis/    # topic overviews
├── purpose.md        # wiki constitution
├── schema.md         # structure conventions
└── wiki/index.md     # entry point
```

## Source

Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
