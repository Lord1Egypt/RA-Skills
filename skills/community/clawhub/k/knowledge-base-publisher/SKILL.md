---
name: knowledge-base-publisher
description: "Organize, format, and publish knowledge-base articles and documentation. Use when you need to convert raw notes, meeting transcripts, or scattered content into structured, publication-ready knowledge base entries with proper metadata, cross-references, and version tracking."
version: 1.0.0
author: openclaw-user
metadata:
  openclaw:
    emoji: "📚"
    category: "knowledge-management"
---

# Knowledge Base Publisher

A skill for turning raw content into structured, publication-ready knowledge base articles.

## When to Use

- Converting meeting notes into structured documentation
- Organizing scattered content into a knowledge base
- Adding metadata, tags, and cross-references to documentation
- Batch-processing multiple articles for publication
- Versioning knowledge base entries with changelog tracking

## Prerequisites

- A source directory containing raw content (markdown, text, or transcript files)
- A target directory or platform for published output
- Optional: a taxonomy file for consistent tagging

## Basic Steps

### 1. Ingest Raw Content

Read source files from the input directory. Supports:
- `.md` / `.markdown` files
- `.txt` plain text files
- Transcript formats (JSON with speaker/timestamp)

### 2. Structure & Enrich

For each document:
1. **Extract or generate title** — from H1, filename, or AI summary
2. **Add metadata block** — date, author, tags, related articles
3. **Normalize formatting** — consistent headings, code blocks, lists
4. **Add cross-references** — link to related articles by tag/topic matching
5. **Generate summary** — one-paragraph abstract if none exists

### 3. Quality Gate

Check each article for:
- Minimum length (recommend ≥ 200 words)
- Has a clear title and at least one section
- No broken internal links
- Tags match the taxonomy (if provided)

### 4. Publish

Write structured articles to the output directory with:
- Consistent filename slugification
- `index.json` catalog with all article metadata
- `CHANGELOG.md` tracking version history
- Per-article `meta.json` for machine-readable metadata

## Example Output Structure

```
knowledge-base/
├── index.json              # Full catalog of all articles
├── CHANGELOG.md            # Version history
├── articles/
│   ├── getting-started.md
│   ├── getting-started.meta.json
│   ├── api-reference.md
│   ├── api-reference.meta.json
│   └── ...
└── taxonomy.json           # Tag/category definitions
```

## Taxonomy Format (Optional)

```json
{
  "categories": ["tutorial", "reference", "guide", "faq"],
  "tags": ["api", "setup", "configuration", "troubleshooting"],
  "related": {
    "api": ["getting-started", "authentication"],
    "setup": ["configuration"]
  }
}
```

## Integration with TaskFlow

This skill works well as a TaskFlow child task:
1. Parent flow defines the source directory and taxonomy
2. Spawn this skill as a detached child task for batch processing
3. Flow waits on child completion, then validates the output catalog
4. Flow finishes with a summary of articles published

## Integration with ClawHub

Published knowledge bases can be packaged as ClawHub skills:
1. Structure the knowledge base as a skill folder with SKILL.md
2. Use `clawhub publish` to register it in the ClawHub registry
3. Others can discover and install via `clawhub search` + `clawhub install`
