---
name: wiki-knowledge-base
description: |
  LLM-powered personal wiki knowledge base system. Use this when user wants to build and maintain a persistent wiki using LLMs following the LLM Wiki pattern (karpathy/442a6bf555914893e9891c11519de94f). This system implements: wiki initialization (two-layer architecture - wiki content and schema), source ingestion with cross-reference maintenance, querying with synthesis and citations, health checking (lint), and schema management. Source files are stored externally (e.g., in project's raw/ folder), not copied into the wiki. Perfect for: personal knowledge management, research wikis, reading companions, team knowledge bases. Triggers on: wiki knowledge base, LLM wiki, personal wiki, build wiki, knowledge management, or any mention of organizing accumulated knowledge with an LLM.
compatibility: Write, Read, Glob, Grep, Bash
---

# Wiki Knowledge Base - Master Skill

This is a comprehensive system for building and maintaining a personal wiki knowledge base using LLMs.

## What This System Does

The LLM Wiki pattern differs from traditional RAG:
- **RAG**: LLM retrieves relevant chunks at query time, rediscovering knowledge from scratch
- **Wiki**: LLM incrementally builds and maintains a persistent wiki with cross-references already in place

## Core Operations

This system provides 5 skills for wiki management:

### 1. wiki-init
Initialize a new wiki with:
- Two-layer architecture (wiki content, schema)
- Directory structure for entities, concepts, sources, syntheses
- Initial index.md and log.md
- CLAUDE.md schema with conventions

**Note**: Source files should be stored externally (e.g., in project's raw/ folder) - the wiki stores summaries and analysis, not copies of source documents.

**Trigger**: User wants to set up a new wiki

### 2. wiki-ingest
Process new sources:
- Read and analyze source documents
- Create source summary pages
- Update entity and concept pages
- Flag contradictions with existing claims
- Update index.md and log.md

**Trigger**: User adds a new source or wants to process a document

### 3. wiki-query
Answer questions against the wiki:
- Search index.md first
- Read relevant pages
- Synthesize answers with citations
- Support multiple output formats (markdown, tables, slides)
- File valuable answers back to wiki

**Trigger**: User asks questions about wiki content

### 4. wiki-lint
Health check the wiki:
- Find contradictions between pages
- Identify stale claims superseded by new sources
- Find orphan pages with no inbound links
- Detect missing pages for important concepts
- Identify missing cross-references
- Suggest data gaps to fill

**Trigger**: User wants to maintain or clean up the wiki

### 5. wiki-maintain
Manage wiki schema:
- Update CLAUDE.md conventions
- Modify page templates
- Refine workflows
- Add new page types

**Trigger**: User wants to update wiki rules or structure

## Usage

Select the appropriate sub-skill based on the operation:
- **New wiki?** → wiki-init
- **Adding content?** → wiki-ingest
- **Asking questions?** → wiki-query
- **Checking quality?** → wiki-lint
- **Updating rules?** → wiki-maintain

## Directory Structure

When initialized, the wiki follows this structure:
```
wiki/
├── entities/              # Entity pages
├── concepts/              # Concept pages
├── sources/              # Source summaries
├── syntheses/            # Cross-source syntheses
├── comparisons/          # Comparison analyses
├── overviews/            # Overview pages
├── schema/CLAUDE.md      # Wiki conventions
├── index.md              # Content catalog
└── log.md                # Operation log

# Source files should be stored in the project root's raw/ folder (or similar external location)
```

## Key Concepts

- **index.md**: Content-oriented catalog, updated on every ingest
- **log.md**: Chronological record with format `## [YYYY-MM-DD] operation | Title`
- **CLAUDE.md**: Schema defining conventions and workflows
- **Cross-references**: Always use [[wiki/page]] link format