---
name: wiki-query
description: |
  Answer questions against an LLM wiki knowledge base. Use this skill whenever the user asks a question that requires searching and synthesizing information from the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms: markdown page, comparison table, slide deck (Marp), chart, or canvas. Important: good answers can be filed back into the wiki as new pages. Perfect for: research questions, comparing concepts, generating summaries, creating analyses, or any question that builds on accumulated wiki knowledge. Always use this when user mentions query, ask, question, compare, analyze, or wants information from the wiki.
compatibility: Write, Read, Glob, Grep, Bash
---

# Wiki Knowledge Base - Query Skill

This skill answers questions against an existing LLM-powered wiki knowledge base following the LLM Wiki pattern.

## Core Concept

Query is the operation where the LLM searches for relevant pages in the wiki, reads them, and synthesizes an answer with citations. The key insight: good answers should be filed back into the wiki as new pages so explorations compound.

## When to Use This Skill

- User asks a question about content in the wiki
- User wants to compare concepts or entities
- User requests a summary or analysis
- User wants to generate output formats (table, slides, chart)
- User mentions query, ask, question, compare, analyze

## What This Skill Does

1. **Reads index.md first**: Find relevant pages from the content catalog
2. **Reads relevant pages**: Drill into specific pages for detailed information
3. **Synthesizes answer**: Combine information from multiple sources
4. **Provides citations**: Link to wiki pages as sources
5. **Creates output**: Format answer as requested (page, table, slides, chart)
6. **Files answer back**: Optionally create a new wiki page from valuable answers
7. **Logs the query**: Append query to log.md

## Query Workflow

### Step 1: Read index.md

Start by reading index.md to find relevant pages. The index provides:
- List of all pages with one-line summaries
- Categorization (entities, concepts, sources, syntheses)
- Metadata (dates, source counts)

### Step 2: Identify Relevant Pages

Based on the question, identify which pages are relevant:
- Entity pages for questions about specific people, places, things
- Concept pages for questions about ideas, theories, frameworks
- Source pages for questions about specific sources
- Synthesis pages for consolidated views

### Step 3: Read Relevant Pages

Read the identified pages to gather information. Note:
- Key facts and claims
- Cross-references to other pages
- Contradictions or debates
- Gaps in knowledge

### Step 4: Synthesize Answer

Combine information from multiple sources:
- Provide a clear answer to the question
- Cite sources using wiki links [[wiki/page]]
- Note any uncertainties or debates
- Highlight connections between concepts

### Step 5: Determine Output Format

Choose appropriate format based on question type:
- **Explanation**: Markdown page with sections
- **Comparison**: Table format
- **Overview**: Summary with bullet points
- **Presentation**: Marp slide deck format
- **Visualization**: Chart or diagram
- **Analysis**: Detailed document with evidence

### Step 6: File Answer Back (Important!)

If the answer is valuable and reusable, create a new wiki page:
- Save to appropriate directory (syntheses/, comparisons/, overviews/)
- Update index.md with the new page
- Add to log.md

Example:
`markdown
## [YYYY-MM-DD] query | [Question Topic]
- Question: [user question]
- Answer format: [page|table|slides|chart]
- Pages consulted: [list]
- Created: [new wiki page if any]
`

### Step 7: Report to User

Present the answer with:
- Clear answer to the question
- Citations to wiki pages
- Note about filing answer back to wiki
- Suggestions for follow-up questions

## Quality Standards

- Must read index.md first before answering
- Must cite wiki pages as sources
- Must consider multiple perspectives from different pages
- Should file valuable answers back to wiki
- Must log query in log.md
- Should suggest follow-up questions

## Output Format Examples

### Markdown Page
`markdown
# [Topic] Overview

## Summary
[2-3 sentence answer]

## Key Points
- [Point 1]
- [Point 2]

## Sources
- [[wiki/sources/SourceName]]
- [[wiki/concepts/ConceptName]]
`

### Comparison Table
`markdown
# [A] vs [B]

| Aspect | [A] | [B] |
|--------|-----|-----|
| [Aspect 1] | [Detail] | [Detail] |
| [Aspect 2] | [Detail] | [Detail] |
`

### Marp Slides
`markdown
---
marp: true
---

# [Topic]

## Slide 1
- [Content]

## Slide 2
- [Content]
`
