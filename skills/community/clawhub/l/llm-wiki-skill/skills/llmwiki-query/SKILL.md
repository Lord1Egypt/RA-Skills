---
name: llmwiki-query
description: >-
  Query the LLM-maintained knowledge wiki and synthesize a focused answer.
  Searches _wiki/ pages first, falls back to raw vault notes, and files new
  insights back into the wiki automatically — so every query compounds the
  knowledge base.
version: 1.0.0
metadata:
  openclaw:
    emoji: 🔍
    homepage: https://github.com/wangsw/llm-wiki-skills
    always: false
---

# /wiki-query — Query the LLM Wiki

You are an expert knowledge synthesizer. Your job is to answer questions by leveraging the accumulated `_wiki/` knowledge layer — not re-deriving everything from scratch — and to file new insights back so the wiki compounds over time.

## Trigger

User invokes `/wiki-query` followed by a question or topic:

```
/wiki-query what is the difference between X and Y
/wiki-query how does the authentication flow work
/wiki-query summarize everything I know about machine learning
```

## Workflow

1. **Search the wiki**
   - `Grep _wiki/` for keywords from the question
   - Try synonyms and related terms if first search is sparse

2. **Read relevant pages**
   - Read the most relevant pages found
   - Follow `[[wikilinks]]` to related pages for additional context

3. **Fall back to the vault if needed**
   - If wiki coverage is thin, `Grep` the full vault for raw notes
   - Raw notes are secondary — the wiki is the primary source

4. **Synthesize an answer**
   - Combine findings into a clear, direct response
   - Cite sources as `_wiki/page-name.md` or vault file paths

5. **File new insights back**
   - If you derived something new not already in the wiki, update or create the relevant page
   - This is how the wiki compounds over time

6. **Report gaps**
   - State explicitly what the wiki is missing
   - Suggest which sources to run `/wiki-ingest` on

## Output Format

```
<direct answer>

Sources: _wiki/page-name.md, _wiki/other-page.md

Wiki updated: yes — added [what] to [page] / no
Gaps: [missing coverage, if any]
```

## Use Cases

- Answer questions using accumulated personal knowledge
- Summarize everything known about a topic
- Find connections between concepts across the vault
- Identify gaps in the knowledge base
- Retrieve past decisions or research without re-reading raw notes

## References

- [Wiki Page Format](references/wiki-page-format.md)
- [Frontmatter Schema](references/frontmatter-schema.md)
