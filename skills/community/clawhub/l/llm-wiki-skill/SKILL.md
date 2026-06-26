---
name: llmwiki
description: >-
  LLM-maintained knowledge wiki for Obsidian vaults. The LLM does the
  bookkeeping, you do the curation. Three sub-skills: ingest sources into
  the wiki, query and synthesize answers, and audit wiki health.
version: 1.0.0
metadata:
  openclaw:
    emoji: 🧠
    homepage: https://github.com/webkong/LLM-Skill
    always: false
---

# /llmwiki — LLM-Maintained Knowledge Wiki

You are a knowledge management assistant. Your job is to route the user's request to the correct sub-skill based on their intent, then execute it.

## Trigger

User invokes `/llmwiki` followed by a sub-command and optional arguments:

```
/llmwiki ingest my-note.md
/llmwiki ingest https://example.com/article
/llmwiki query what do I know about machine learning
/llmwiki health
```

## Routing

Parse the first word of `$ARGUMENTS` and delegate:

| Sub-command | Delegates to | Description |
|---|---|---|
| `ingest <source>` | `skills/llmwiki-ingest/SKILL.md` | Extract insights from a file, URL, or topic into `_wiki/` |
| `query <question>` | `skills/llmwiki-query/SKILL.md` | Search the wiki and synthesize an answer |
| `health` | `skills/llmwiki-health/SKILL.md` | Audit wiki for orphans, stubs, broken links, stale pages |

If no sub-command is given, print this help:

```
Usage:
  /llmwiki ingest <file|url|topic>  — add knowledge to the wiki
  /llmwiki query <question>         — ask the wiki a question
  /llmwiki health                   — audit wiki quality
```

## Use Cases

- Build a compounding personal knowledge base from Obsidian notes
- Capture insights from articles and documentation without losing them
- Retrieve past research without re-reading raw notes
- Keep the wiki well-connected and free of stale content

## References

- [Ingest skill](skills/llmwiki-ingest/SKILL.md)
- [Query skill](skills/llmwiki-query/SKILL.md)
- [Health skill](skills/llmwiki-health/SKILL.md)
- [Wiki page format](skills/llmwiki-ingest/references/wiki-page-format.md)
