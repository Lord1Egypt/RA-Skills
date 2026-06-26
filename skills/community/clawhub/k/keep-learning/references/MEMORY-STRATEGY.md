# Memory Strategy Reference

## Three-Layer Architecture

### L1: Core Memory

Storage: Agent Memory System (via update_memory)

Content:
- Key conclusions and insights from knowledge files
- Core concepts and terminology definitions
- Important decisions and their rationale
- Best practices and recommendations

Purpose:
- Automatically surfaces in memory_overview during conversations
- Enables agent to recall knowledge without explicit file reading
- Provides quick context for related discussions

Category Selection:

| Knowledge Type | Category |
|----------------|----------|
| Domain expertise | expert_experience |
| Best practices | expert_experience |
| Project overviews | project_introduction |
| How-to guides | learned_skill_experience |
| Methodologies | learned_skill_experience |

Title Naming: [Domain] Concise Topic Description

Examples:
- [AI Observability] Product Evolution Three Phases
- [Work Methods] MECE Problem Analysis Framework

### L2: Knowledge Index

Storage: Agent Memory System (single entry per domain/folder)

Content: File path, Theme, Keywords mapping table

Purpose:
- Quick lookup: Which file discusses topic X?
- Enables targeted read_file calls
- Prevents re-reading all files

### L3: Source Files

Storage: Local filesystem (original knowledge base)

Content: Complete, unmodified original files

Purpose:
- Deep-dive access for full context
- Preserves all details, formatting, code examples
- Accessed via read_file when L1/L2 insufficient

## Memory Size Guidelines

L1 Entry: 500-1500 characters target, max ~3000 characters
L2 Index: One entry per major domain, can reference 50-100 files

## Deduplication

Before creating: search_memory with relevant keywords
If exists: update with existing id
If not: create new entry
