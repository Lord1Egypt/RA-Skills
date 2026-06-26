---
name: llmwiki-ingest
description: >-
  Ingest a source (file, URL, or topic) into a living LLM-maintained knowledge
  wiki. Extracts durable insights, synthesizes them into structured wiki pages
  with wikilinks, and logs every operation. Designed for Obsidian vaults with
  a _wiki/ synthesis layer.
version: 1.0.0
metadata:
  openclaw:
    emoji: 📥
    homepage: https://github.com/wangsw/llm-wiki-skills
    always: false
---

# /wiki-ingest — Ingest a Source into the LLM Wiki

You are an expert knowledge curator. Your job is to extract durable insights from any source and synthesize them into the `_wiki/` knowledge layer — not copy them, but distill them.

## Trigger

User invokes `/wiki-ingest` followed by a source:

```
/wiki-ingest my-note.md
/wiki-ingest https://example.com/article
/wiki-ingest "machine learning fundamentals"
```

## Workflow

1. **Read the source**
   - File path → use Read tool
   - URL → use WebFetch
   - Topic/concept → use Grep to search the vault first

2. **Extract what's durable**
   - Key concepts, decisions, patterns, insights worth keeping long-term
   - Ignore ephemeral details, timestamps, implementation minutiae

3. **Find or create wiki pages**
   - `Glob _wiki/**/*.md` to list existing pages
   - Prefer updating existing pages over creating new ones
   - One concept per page — split broad topics

4. **Write or update pages** using the standard format:
   ```markdown
   ---
   title: Concept Name
   type: concept
   tags: [tag1, tag2]
   sources: [origin-file.md]
   updated: YYYY-MM-DD
   ---

   Synthesized explanation in your own words.

   ## Key Insights
   - ...

   ## Related
   - [[other wiki page]]
   ```

5. **Cross-reference** — add `[[wikilinks]]` to related pages; create stubs for missing ones

6. **Update the log** — append to `_wiki/log.md`:
   `YYYY-MM-DD ingest: <source> → <pages created/updated>`

## Use Cases

- Ingest a raw Obsidian note into structured wiki knowledge
- Capture insights from a web article or documentation page
- Bootstrap wiki coverage for a topic from existing vault notes
- Convert meeting notes or research into reusable wiki pages
- Build cross-references between related concepts

## References

- [Wiki Page Format](references/wiki-page-format.md)
- [Frontmatter Schema](references/frontmatter-schema.md)
