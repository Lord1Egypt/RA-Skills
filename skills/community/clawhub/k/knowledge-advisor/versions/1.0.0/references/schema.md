# Knowledge Base Schema

File format and structure specification for the knowledge-advisor knowledge base.

## Directory Structure

```
knowledge-base/
├── _index.md              # Master index (always loaded first)
├── _health.json           # Health metrics
├── _cross-references.md   # Inter-book connections
├── _domains.json          # Domain tag registry
├── [book-slug]/           # One directory per book (kebab-case)
│   ├── meta.json          # Book metadata
│   ├── frameworks.md      # Extracted frameworks
│   ├── principles.md      # Extracted principles
│   ├── mental-models.md   # Extracted mental models
│   ├── anti-patterns.md   # Extracted anti-patterns
│   └── case-studies.md    # Extracted case studies
└── [book-slug]/
    └── ...
```

## Naming Convention

Book directory names use kebab-case derived from the book title:
- "Crucial Conversations" → `crucial-conversations/`
- "Good to Great" → `good-to-great/`
- "從A到A+" → `from-a-to-a-plus/` (romanized)

## File Specifications

### `_index.md`
- Always loaded first for any query
- Contains book list table and application trigger index
- Must stay under 3,000 estimated tokens (word count * 1.3)
- Updated after every ingestion

### `_health.json`
- Updated after every ingestion
- Contains metrics for self-monitoring
- See templates/_health.json for field definitions

### `_cross-references.md`
- Maps related frameworks across different books
- Updated after every ingestion
- Only loaded when cross-referencing

### `_domains.json`
- Registry of all domain tags with descriptions
- Updated when new domains are added

### `meta.json`
- One per book directory
- Contains metadata, not extracted knowledge
- Used for filtering and listing

### `frameworks.md`, `principles.md`, etc.
- Contain the actual extracted knowledge
- Loaded on demand only
- Follow the templates in `templates/` directory

## File Size Guidelines

| File | Target Size | Max Size |
|------|------------|----------|
| `_index.md` (30 books) | ~600 words | ~2,300 words (3,000 tokens) |
| `meta.json` | ~200 words | ~400 words |
| `frameworks.md` | ~800 words | ~2,000 words |
| `principles.md` | ~500 words | ~1,200 words |
| `mental-models.md` | ~300 words | ~800 words |
| `anti-patterns.md` | ~300 words | ~800 words |
| `case-studies.md` | ~400 words | ~1,000 words |
| **Total per book** | ~2,500 words | ~6,200 words (~8,000 tokens) |

## Encoding

All files must be UTF-8 encoded to support English, Traditional Chinese, and Simplified Chinese.
