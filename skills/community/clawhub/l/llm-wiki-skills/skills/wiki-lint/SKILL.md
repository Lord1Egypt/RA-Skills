---
name: wiki-lint
description: |
  Health check and maintain an LLM wiki knowledge base. Use this skill whenever the user wants to perform routine maintenance on the wiki: check for contradictions between pages, identify stale claims superseded by newer sources, find orphan pages with no inbound links, detect important concepts lacking their own pages, identify missing cross-references, and find data gaps that could be filled with web search. Perfect for: periodic wiki maintenance, quality assurance, finding gaps in knowledge, or cleaning up wiki as it grows. Always use this when user mentions lint, check, health check, maintenance, clean up, or verify wiki quality.
compatibility: Write, Read, Glob, Grep, Bash
---

# Wiki Knowledge Base - Lint Skill

This skill performs health checks on an existing LLM-powered wiki knowledge base following the LLM Wiki pattern.

## Core Concept

Lint is the operation where the LLM performs routine maintenance on the wiki to keep it healthy as it grows. This includes checking for contradictions, stale claims, orphan pages, missing pages, and data gaps.

## When to Use This Skill

- User wants to perform routine wiki maintenance
- User mentions lint, check, health check, maintenance
- User wants to find gaps or issues in the wiki
- Periodic maintenance is due
- User asks to clean up or verify wiki quality

## What This Skill Does

1. **Checks for contradictions**: Find claims that contradict each other across pages
2. **Identifies stale claims**: Find claims that newer sources have superseded
3. **Finds orphan pages**: Identify pages with no inbound links
4. **Detects missing pages**: Find important concepts mentioned but lacking their own page
5. **Identifies missing cross-references**: Find related concepts that should be linked
6. **Finds data gaps**: Identify areas where more information would be valuable
7. **Suggests improvements**: Propose new questions to investigate and sources to find
8. **Logs the lint pass**: Record the health check in log.md

## Lint Workflow

### Step 1: Read index.md

Start by reading index.md to understand the current state of the wiki:
- Total page count
- Categories (entities, concepts, sources, syntheses)
- Recent changes

### Step 2: Scan for Contradictions

Search across pages for contradictory claims:
- Read multiple pages on the same topic
- Compare claims about the same entity or concept
- Note any conflicts or disagreements
- Flag with contradiction note

### Step 3: Check for Stale Claims

Compare recent sources with older pages:
- Look at source dates in frontmatter
- Check if newer sources supersede old claims
- Note when claims need updating

### Step 4: Find Orphan Pages

Identify pages with no inbound links:
- Check each page for backlinks
- Note pages that are never referenced
- Suggest connections to other pages

### Step 5: Detect Missing Pages

Find concepts mentioned but lacking pages:
- Scan for capitalized or defined terms
- Check if each concept has its own page
- Create new pages for important missing concepts

### Step 6: Identify Missing Cross-References

Find related concepts that should be linked:
- Check concept pages for related concepts
- Ensure bidirectional links where appropriate
- Add missing [[wiki/page]] links

### Step 7: Find Data Gaps

Identify areas needing more information:
- Note unanswered questions
- Find topics with sparse coverage
- Suggest sources to search for

### Step 8: Report Findings

Create a lint report:
`markdown
## [YYYY-MM-DD] lint | Health Check

### Contradictions Found
- [Page A] claims X but [Page B] claims Y

### Stale Claims
- [Page] needs updating based on [new source]

### Orphan Pages
- [Page] has no inbound links

### Missing Pages
- Concept [Name] mentioned but no page exists

### Missing Cross-References
- [Page A] should link to [Page B]

### Data Gaps
- [Topic] needs more information

### Suggested Actions
- [Action 1]
- [Action 2]
`

### Step 9: Update log.md

Append lint entry to log.md:
`markdown
## [YYYY-MM-DD] lint | Health Check
- Pages checked: [count]
- Issues found: [count]
- Actions recommended: [list]
`

## Quality Standards

- Must check all pages in the wiki
- Must document all issues found
- Must suggest specific actions for each issue
- Must log lint pass in log.md
- Should prioritize issues by severity
- Should suggest new questions to investigate
