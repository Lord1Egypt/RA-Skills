---
name: markdown-to-summary
description: >
  Use when (1) user provides a long markdown document and asks to summarize, abstract, or condense it. 
  (2) user says "summarize this", "tl;dr", "give me the key points", or "what's the main idea". 
  (3) user pastes a README, article, or doc and wants a short version. 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# Markdown to Summary

Use when (1) user provides a long markdown document and asks to summarize, abstract, or condense it. (2) user says "summarize this", "tl;dr", "give me the key points", or "what's the main idea". (3) user pastes a README, article, or doc and wants a short version.

## Core Position

This skill solves the specific problem of: *long markdown content needs to be distilled into its essential points without losing critical information.*

This skill IS NOT:
- A translation tool — it condenses, it does not translate language
- An analysis tool — it summarizes facts, not opinions or sentiment
- A code documentation tool — for code comments use code-to-mindmap instead

This skill IS activated ONLY when: markdown text + summary/condense intent are both present.

## Modes

### `/markdown-to-summary`

**Default mode.** Produces a concise summary preserving key information structure.

When to use: User provides markdown and wants a shorter version covering main points.

### `/markdown-to-summary/bullet`

Outputs key points as a structured bullet list instead of prose.

When to use: User wants action items, highlights, or a quick-scan list rather than paragraph summary.

### `/markdown-to-summary/tl-dr`

Produces a single-sentence and single-paragraph tl;dr.

When to use: User wants the absolute shortest version possible.

## Execution Steps

### Step 1 — Analyze the Document Structure

1. Receive markdown input (pasted text, file, or path)
2. Detect document type:
   - **Technical doc** (README, API docs, guide): preserve architecture, setup steps, key concepts
   - **Article/post**: preserve main argument, evidence, conclusion
   - **Meeting notes**: preserve decisions, action items, owners
   - **Changelog/release notes**: preserve version, key changes, breaking changes
3. Extract hierarchy: H1/H2/H3 headings define primary sections; body text fills them
4. Identify key content signals:
   - Repeated terms → core topics
   - Numbers/dates → factual claims worth preserving
   - Code blocks → technical detail to keep reference to
   - Tables → structured data to preserve

### Step 2 — Extract Key Points

For each major section (H2 level):

| Section Type | Keep | Discard |
|---|---|---|
| Technical doc | Prerequisites, setup steps, key concepts, examples | Installation chatter, release notes noise |
| Article | Thesis statement, supporting evidence, conclusion | Digressions, tangents, filler examples |
| Meeting notes | Decisions made, action items, owners | Meeting meta (time, attendees unless relevant) |
| Changelog | New features, bug fixes, breaking changes | Version numbers, dates, contributor lists unless significant |

### Step 3 — Compose Summary

Choose output format based on mode:

- **Default**: prose paragraphs, ~20-30% of original length
- **Bullet**: labeled bullet points, one per H2 section
- **Tl;dr**: 1 sentence + 1 paragraph max

Key principles:
- Preserve specific numbers, names, dates, and version numbers
- Keep code examples as references (not full code)
- Use original heading structure as outline
- Maintain logical flow (don't reorder unrelated sections)

### Step 4 — Validate

- Summary length is ≤40% of original (unless user specified a different ratio)
- Every major H2 section has at least one mention
- No new information added that wasn't in the original
- Technical accuracy preserved (version numbers, commands, paths match)

## Mandatory Rules

### Do not

- Do not add opinions, analysis, or commentary not in the original
- Do not reorder sections — keep the original logical flow
- Do not change technical values (version numbers, paths, commands)
- Do not produce a summary longer than the original without explicit permission

### Do

- Preserve exact technical values (version numbers, URLs, paths)
- Keep section structure aligned with original headings
- Flag when a section was condensed significantly vs. kept intact
- Note any sections that were dropped entirely and why

## Quality Bar

**A good output:**
- Every major section appears in the summary
- Technical facts match the original exactly
- Length is 20-40% of original
- Structure mirrors original (sections in same order)

**A bad output:**
- Introduces new information not in source
- Drops an entire H2 section with no mention
- Changes technical specifics (wrong version number, command)
- Summary is longer than original

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| 2000-word README | 200-word summary missing setup steps | Preserves: prerequisites, key commands, architecture |
| Changelog with 20 entries | Lists all 20 | Groups: 3 features, 5 fixes, 1 breaking change |
| Article with digression | Includes the tangent | Skips digression, keeps main argument |
| API doc with code examples | Rewrites code in prose | Keeps code block, summarizes surrounding text |

## References

- `references/` — Document type taxonomies, summary length guidelines by use case