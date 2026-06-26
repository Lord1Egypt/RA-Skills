---
name: wiki-init
description: |
  Initialize a new LLM-powered wiki knowledge base. Use this skill whenever the user wants to set up a personal wiki following the LLM Wiki pattern (karpathy/442a6bf555914893e9891c11519de94f). This skill creates the two-layer architecture (wiki content, schema), establishes the directory structure, and generates the initial index.md and log.md files. Source files should be stored externally (e.g., in project's raw/ folder), not copied into the wiki. Perfect for: starting a research wiki, creating a personal knowledge base, setting up a reading companion wiki, or building an LLM-maintained team knowledge base. Always use this when user mentions wiki knowledge base, LLM wiki, personal wiki, set up wiki, initialize wiki, or wants to organize accumulated knowledge with an LLM.
compatibility: Write, Read, Glob, Grep, Bash
---

# Wiki Knowledge Base - Initialization Skill

This skill initializes a new LLM-powered wiki knowledge base following the LLM Wiki pattern.

## Core Concept

The LLM Wiki pattern differs from traditional RAG:
- **RAG**: LLM retrieves relevant chunks at query time, rediscovering knowledge from scratch every time
- **Wiki**: LLM incrementally builds and maintains a persistent wiki - cross-references already exist, contradictions are flagged, synthesis reflects everything you have read

## When to Use This Skill

- User wants to set up a new personal or research wiki
- User mentions wiki knowledge base, LLM wiki, or personal wiki
- User wants to organize accumulated knowledge with an LLM

## What This Skill Does

1. Creates the two-layer wiki architecture:
   - **Wiki**: LLM-generated markdown files directory (entities, concepts, sources, etc.)
   - **Schema**: Configuration and conventions document

2. Generates essential files:
   - index.md - Content-oriented catalog of all wiki pages
   - log.md - Chronological record of wiki operations

3. Creates a comprehensive CLAUDE.md schema that tells the LLM how to maintain the wiki

**Note**: Source files should be stored externally (e.g., in project's raw/ folder). The wiki stores summaries, analysis, and generated content - not copies of source documents.

## Directory Structure Created

wiki/
- entities/              - Entity pages (people, places, things)
- concepts/             - Concept pages (ideas, theories)
- sources/               - Source summaries
- syntheses/            - Cross-source syntheses
- comparisons/          - Comparison analyses
- overviews/             - Overview/topic summaries
- schema/CLAUDE.md      - Wiki conventions and workflows
- index.md              - Content catalog (auto-updated)
- log.md                - Operation log (append-only)

## Usage Instructions

### Step 1: Ask User for Wiki Location

Before creating anything, ask the user:
1. Where should the wiki be created?
2. What is the wiki purpose?
3. What types of sources will be added?

### Step 2: Create the Wiki Structure

Create all directories and files following the structure above.

### Step 3: Generate CLAUDE.md Schema

Create a comprehensive schema document that includes:
- Wiki Overview: Purpose and scope
- Architecture: Three-layer explanation
- Page Types: Definitions for each wiki content type
- Naming Conventions: How to name files and links
- Frontmatter Schema: YAML frontmatter for each page type
- Ingest Workflow: Step-by-step for adding new sources
- Query Workflow: How to answer questions
- Lint Workflow: Health check procedures
- Cross-Reference Rules: When and how to link pages

### Step 4: Generate Initial index.md

Create an index.md with proper structure for categorizing pages.

### Step 5: Generate Initial log.md

Create a log.md with timestamped entry format.

### Step 6: Report to User

Summarize what was created and next steps.

## Quality Standards

- All directories must be created
- CLAUDE.md must be comprehensive (2000+ words)
- index.md must have clear structure for categorizing pages
- log.md must have proper entry format with timestamps
- Must ask user for location and purpose before creating
