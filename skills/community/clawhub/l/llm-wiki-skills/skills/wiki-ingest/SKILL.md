---
name: wiki-ingest
description: |
  Process and integrate new sources into an existing LLM wiki knowledge base. Use this skill whenever the user adds a new source (article, paper, book chapter, note) to the raw sources directory and wants the LLM to extract key information, update entity pages, revise topic summaries, note contradictions with existing claims, and maintain cross-references. Perfect for: ingesting articles into research wiki, adding book chapters to reading companion, processing meeting notes into team wiki, or updating personal knowledge base with new information. Always use this when user mentions ingest, add source, process document, or update wiki with new content.
compatibility: Write, Read, Glob, Grep, Bash
---

# Wiki Knowledge Base - Ingest Skill

This skill processes and integrates new sources into an existing LLM-powered wiki knowledge base following the LLM Wiki pattern.

## Core Concept

Ingest is the operation where the LLM reads a new source, extracts key information, and integrates it into the existing wiki. A single source might touch 10-15 wiki pages. The LLM updates entity pages, revises topic summaries, notes contradictions, and maintains cross-references.

## When to Use This Skill

- User adds a new source to an external directory (e.g., raw/ folder)
- User mentions ingest, add source, process document
- User wants to update wiki with new information
- User asks to summarize and integrate an article/paper/book chapter

**Note**: Source files are stored externally, not copied into the wiki. The wiki stores summaries and analysis only.

## What This Skill Does

1. **Reads the new source**: Extract text, key concepts, entities, and claims
2. **Creates a source summary page**: Documents the source in wiki/sources/
3. **Updates related entity pages**: Adds new information to existing entity pages
4. **Updates concept pages**: Revises concept pages with new insights
5. **Flags contradictions**: Notes where new data contradicts old claims
6. **Updates index.md**: Adds new pages to the content catalog
7. **Updates log.md**: Appends ingest entry with timestamp

## Ingest Workflow

### Step 1: Identify the Source

Ask the user or find the new source in the external sources directory (e.g., raw/). Determine:
- Source type (article, paper, book, podcast, meeting notes)
- Key entities mentioned
- Key concepts covered
- How it relates to existing wiki content

### Step 2: Read and Analyze the Source

Read the source content and extract:
- Main topic and key takeaways
- Entities (people, places, organizations)
- Concepts (ideas, theories, frameworks)
- Claims and assertions
- Connections to existing wiki content

### Step 3: Create Source Summary Page

Create a new page in wiki/sources/:
`markdown
---
title: [Source Title]
date: [YYYY-MM-DD]
type: [article|paper|book|notes]
tags: [relevant tags]
source_path: [external path to original source]
---

# [Source Title]

## Key Takeaways
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

## Entities Mentioned
- [[wiki/entities/EntityName]]

## Concepts Covered
- [[wiki/concepts/ConceptName]]

## Key Claims
- [Claim 1]
- [Claim 2]

## Cross-References
- Related: [[wiki/concepts/RelatedConcept]]
- Related: [[wiki/entities/RelatedEntity]]
`

**Note**: Do NOT copy the source content into the wiki. Store only the path to the original source.

### Step 4: Update Existing Pages

For each related entity and concept page:
- Add new information from the source
- Update summaries if needed
- Add cross-references to the new source page
- Flag any contradictions with existing claims

### Step 5: Update index.md

Add new pages to the index:
- Add source page to Sources section
- Add new entities to Entities section
- Add new concepts to Concepts section

### Step 6: Update log.md

Append to log.md:
`markdown
## [YYYY-MM-DD] ingest | [Source Title]
- Source: [external path to source file]
- Type: [article|paper|book|notes]
- Key entities: [list]
- Key concepts: [list]
- Pages updated: [list of files]
`

### Step 7: Report to User

Summarize:
- What was created
- What was updated
- Any contradictions flagged
- Cross-references added

## Quality Standards

- Source summary must include key takeaways, entities, concepts
- All related entity and concept pages must be updated
- index.md must reflect new pages
- log.md must have proper timestamp format
- Contradictions must be explicitly flagged with note
- Each ingest should touch 10-15 wiki pages when possible
