---
name: llmwiki-health
description: >-
  Audit the LLM-maintained knowledge wiki for quality issues: orphan pages,
  broken wikilinks, stubs, stale content, and missing frontmatter. Generates
  a severity-tiered health report and auto-fixes what it can.
version: 1.0.0
metadata:
  openclaw:
    emoji: 🩺
    homepage: https://github.com/wangsw/llm-wiki-skills
    always: false
---

# /wiki-health — Audit the LLM Wiki

You are an expert knowledge base auditor. Your job is to inspect `_wiki/`, surface quality issues, and fix what can be fixed automatically — keeping the wiki well-connected and trustworthy over time.

## Trigger

User invokes `/wiki-health` with no arguments:

```
/wiki-health
```

## Workflow

1. **Inventory**
   - `Glob _wiki/**/*.md` to list all pages
   - Count total pages; group by `type` tag in frontmatter if present

2. **Check for stubs**
   - Pages with fewer than 5 lines of content (excluding frontmatter)
   - List them by filename

3. **Check for orphans**
   - Pages with no outgoing `[[wikilinks]]`
   - Isolated nodes are the most critical issue

4. **Check for broken links**
   - Find all `[[Page Name]]` references across `_wiki/`
   - Verify each target page exists
   - List broken links with the page that contains them

5. **Check for stale pages**
   - Pages whose `updated` frontmatter date is more than 90 days old
   - Flag for review, not auto-deletion

6. **Check for missing frontmatter**
   - Pages missing any of: `title`, `type`, `tags`, `sources`, `updated`

7. **Auto-fix what's easy**
   - Orphans: add at least one `[[wikilink]]` to a related page
   - Missing frontmatter fields: fill in from page content

8. **Generate report**

## Output Format

```markdown
## Wiki Health Report — YYYY-MM-DD

Total pages: N

### Issues Found
- Stubs (N): [list]
- Orphans (N): [list]
- Broken links (N): [list]
- Stale pages (N): [list]
- Missing frontmatter (N): [list]

### Fixed
- [what was auto-fixed]

### Needs Attention
- [what requires human review or /wiki-ingest]
```

## Use Cases

- Regular maintenance to keep the wiki well-connected
- Before sharing or publishing the wiki
- After a large batch of `/wiki-ingest` runs
- When the wiki feels "stale" or hard to navigate
- Onboarding check before a new project phase

## References

- [Wiki Page Format](references/wiki-page-format.md)
- [Frontmatter Schema](references/frontmatter-schema.md)
