---
name: private-knowledge-base
description: Personal knowledge base for PDFs, papers, and documents with cross-document Q&A and concept retrieval. Use when: (1) User asks questions about stored documents ("which doc mentions X?"), (2) Need to summarize concepts across multiple PDFs, (3) User wants to ingest new PDFs/papers into knowledge base, (4) Cross-document linking and association is needed, (5) Fast semantic search over personal document collection.
version: 1.0.0
---

# Private Knowledge Base

Personal document storage and retrieval system for PDFs, papers, and research documents.

## Quick Start

### Ingest Documents

```bash
# Add PDF to knowledge base
./scripts/ingest.sh ~/path/to/document.pdf

# Process entire folder
./scripts/ingest-folder.sh ~/papers/
```

### Query Knowledge Base

```bash
# Search for concept across all documents
./scripts/search.sh "transformer architecture"

# Get summary of concept from relevant docs
./scripts/summarize.sh "attention mechanism"
```

## Core Workflows

### 1. Document Ingestion

When user provides new PDFs or papers:

1. Create document entry in `kb/index.json`
2. Extract text and metadata
3. Generate embeddings for semantic search
4. Store in `kb/docs/` with normalized name

### 2. Cross-Document Q&A

When user asks "which document mentions X?" or "summarize X from my docs":

1. Search embeddings for relevant passages
2. Retrieve source documents
3. Synthesize answer across documents
4. Cite sources with document names and page numbers

### 3. Concept Linking

Build associations between documents:
- Shared concepts
- Citation relationships
- Topic clusters

## File Structure

```
private-knowledge-base/
├── SKILL.md
├── scripts/
│   ├── ingest.sh          # Single document ingestion
│   ├── ingest-folder.sh   # Batch ingestion
│   ├── search.sh          # Semantic search
│   └── summarize.sh       # Cross-document summary
├── references/
│   └── schema.md          # KB index schema
└── kb/                    # Created at runtime
    ├── index.json
    ├── embeddings/
    └── docs/
```

## Usage Examples

**User**: "我之前存的文档里，哪篇提到了 transformer?"
→ Run `./scripts/search.sh "transformer"`

**User**: "总结一下我文档里关于 attention 的内容"
→ Run `./scripts/summarize.sh "attention"`

**User**: "把这篇 PDF 加到知识库"
→ Run `./scripts/ingest.sh <pdf-path>`

## Configuration

Set knowledge base location:
```bash
export KB_ROOT=~/.openclaw/workspace/kb
```

Default: `~/kb` if not set.
