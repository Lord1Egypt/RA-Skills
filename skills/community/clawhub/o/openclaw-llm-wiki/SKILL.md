---
name: llm-wiki
description: Create and maintain a persistent LLM-maintained knowledge base (wiki) following Andrej Karpathy's pattern. The LLM actively builds and maintains interconnected markdown files that compound knowledge over time.
---

# LLM Wiki Skill

Create and maintain a persistent LLM-maintained knowledge base (wiki) following Andrej Karpathy's pattern. Instead of traditional RAG where LLMs rediscover knowledge from scratch, this skill enables the LLM to actively build and maintain interconnected markdown files that serve as a growing, searchable knowledge base.

## Overview

This skill implements Andrej Karpathy's LLM Wiki concept:
- **Raw sources** → Immutable collection of source documents
- **The wiki** → LLM-generated, interconnected markdown files owned entirely by the LLM
- **The schema** → Configuration file that tells the LLM how to structure and maintain the wiki

The LLM becomes a disciplined wiki maintainer rather than a generic chatbot, handling all the bookkeeping, cross-referencing, and knowledge synthesis.

## Folder Structure

When initialized, this skill creates:
```
llm-wiki/
├── raw/                  # Your source documents (immutable)
├── wiki/
│   ├── entities/         # Person, model, organization pages
│   ├── concepts/         # Techniques, theories, methods
│   ├── sources/          # Source summaries and analyses
│   └── logs/             # Activity logs (optional)
├── index.md              # Auto-generated catalog of all wiki pages
├── log.md                # Chronological record of activities
└── SCHEMA.md             # Configuration for LLM wiki maintainer
```

## Core Workflows

### 1. Ingesting Sources
When new sources are added to `raw/`:
- LLM reads and discusses key takeaways with human
- Creates/updates summary page in `wiki/sources/`
- Updates relevant entity pages in `wiki/entities/`
- Updates relevant concept pages in `wiki/concepts/`
- Updates `index.md` and appends to `log.md`

### 2. Querying Knowledge
When answering questions:
- Consults `index.md` to find relevant pages
- Reads and synthesizes from wiki pages with citations
- Suggests filing valuable answers back as new wiki knowledge
- Logs the query interaction

### 3. Wiki Maintenance (Lint)
Periodic health checks:
- Identifies contradictions between pages
- Finds stale claims superseded by newer sources
- Detects orphan pages (no inbound links)
- Notes missing concepts that need their own page
- Highlights missing cross-references
- Suggests new questions to investigate and sources to seek
- Reports findings and asks for confirmation before changes

## Human-LLM Collaboration

### Human Responsibilities:
- Curate and add sources to `raw/`
- Direct analysis and ask probing questions
- Resolve conflicts and provide context
- Think about implications and meaning

### LLM Responsibilities:
- Read and comprehend source materials
- Extract and integrate knowledge into wiki
- Maintain cross-references and consistency
- Update summaries when new information arrives
- Flag contradictions and uncertainties
- Handle all bookkeeping and maintenance
- Never modify raw source documents

## Usage

### Initial Setup
The skill automatically creates the folder structure and base files when first used.

### Adding a Source
1. Place document(s) in `llm-wiki/raw/`
2. Tell the agent: "Please process the new source I added"
3. Agent will ingest and integrate the knowledge

### Asking Questions
- Ask questions naturally about your knowledge base
- Agent will consult the wiki and provide cited answers
- Agent may suggest filing insights back as wiki pages

### Maintenance
- Agent will periodically suggest running wiki health checks
- Or you can request: "Please run a lint check on the wiki"

## Configuration

The `SCHEMA.md` file in the wiki root contains detailed configuration for:
- Naming conventions
- Optional frontmatter format
- Specific workflow details
- Output format guidelines
- Tool integration hints (Obsidian, qmd, git, etc.)

## Example Interaction Flow

**Human:** "I've added a new paper about LLM quantization techniques to raw/"

**Agent:** 
1. Reads the paper
2. Discovers key points: quantization reduces model size, improves inference speed, techniques like GPTQ, AWQ
3. Creates/updates `wiki/sources/paper-title.md` with summary
4. Updates/concept page `wiki/concepts/quantization.md` 
5. Updates entity pages for any mentioned models/researchers
6. Updates `index.md` and appends to `log.md`
7. Reports: "I've processed the paper and updated the quantization concept page. Would you like to discuss any specific findings?"

**Human:** "What's the difference between GPTQ and AWQ?"

**Agent:**
1. Checks index for relevant pages
2. Reads `wiki/concepts/quantization.md` and related entity pages
3. Synthesizes answer comparing the two techniques with citations
4. Suggests: "This comparison could be filed as a new wiki page. Would you like me to create `wiki/concepts/gptq-vs-awq.md`?"
5. Logs the query

## Benefits Over Traditional RAG

- **Compounding knowledge**: Each source makes the wiki more valuable, not just adds to retrieval corpus
- **Zero maintenance cost**: LLM handles all bookkeeping, cross-referencing, consistency
- **Persistent synthesis**: Knowledge is compiled once and kept current, not re-derived per query
- **Exploration value**: Answers can become new wiki pages, making explorations permanent
- **Transparent organization**: Human-navigable structure with clear categories and links

## Requirements

- Basic file system access to create/modify the wiki directory structure
- Compatible with any LLM that can read/write files and follow structured instructions
- Works best with agents that can maintain context over multiple interactions

## Getting Started

1. Use this skill to initialize your LLM wiki
2. Add your first source document to the `raw/` folder
3. Ask the agent to process it
4. Begin building your knowledge base through ingestion and questioning