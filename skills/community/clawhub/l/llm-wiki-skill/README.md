# LLM Wiki Skills

LLM-maintained knowledge wiki skills for [Claude Code](https://claude.ai/code), designed for Obsidian vaults.

Inspired by [Andrej Karpathy's LLM Wiki concept](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [marvec/rock-star-skills](https://github.com/marvec/rock-star-skills).

## The idea

Traditional knowledge bases decay because maintenance is tedious. The LLM Wiki pattern inverts this: **the LLM does the bookkeeping, you do the curation.**

Instead of re-deriving insights from scratch on every query, you build a persistent, synthesized `_wiki/` layer that compounds over time. Every ingest and every query makes it more valuable.

## Skills

| Skill | Command | Description |
|---|---|---|
| `llmwiki-ingest` | `/wiki-ingest <source>` | Extract insights from a file, URL, or topic into the wiki |
| `llmwiki-query` | `/wiki-query <question>` | Search and synthesize an answer; files new insights back |
| `llmwiki-health` | `/wiki-health` | Audit for orphans, stubs, broken links, stale pages |

## Installation

### Via ClawHub

```bash
clawhub skill install llmwiki-ingest
clawhub skill install llmwiki-query
clawhub skill install llmwiki-health
```

Then bootstrap the wiki in your vault:

```bash
cp -r _wiki/ /path/to/vault/_wiki/
```

### Manual

```bash
cp skills/llmwiki-ingest/SKILL.md /path/to/vault/.claude/commands/wiki-ingest.md
cp skills/llmwiki-query/SKILL.md  /path/to/vault/.claude/commands/wiki-query.md
cp skills/llmwiki-health/SKILL.md /path/to/vault/.claude/commands/wiki-health.md
cp -r _wiki/ /path/to/vault/_wiki/
```

Open Claude Code in your vault and start:

```
/wiki-ingest my-most-important-note.md
```

## Wiki page format

```markdown
---
title: Concept Name
type: concept
tags: [tag1, tag2]
sources: [origin-file.md or https://url]
updated: YYYY-MM-DD
---

Synthesized explanation in your own words.

## Key Insights
- ...

## Related
- [[other wiki page]]
```

## Directory structure

```
LLM-Wiki-Skill/
├── skills/
│   ├── llmwiki-ingest/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── wiki-page-format.md
│   │       └── frontmatter-schema.md
│   ├── llmwiki-query/
│   │   ├── SKILL.md
│   │   └── references/
│   └── llmwiki-health/
│       ├── SKILL.md
│       └── references/
├── _wiki/
│   ├── index.md
│   └── log.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Principles

- **Synthesize, don't copy.** Pages contain understanding, not raw quotes.
- **Wikilinks are first-class.** Every page must link to at least one other. Isolated pages are a smell.
- **One concept per page.** Split broad topics into focused pages.
- **Every query compounds.** `/wiki-query` files new insights back automatically.

## Publishing to ClawHub

```bash
clawhub skill publish skills/llmwiki-ingest --version 1.0.0
clawhub skill publish skills/llmwiki-query  --version 1.0.0
clawhub skill publish skills/llmwiki-health --version 1.0.0
```

## License

MIT
