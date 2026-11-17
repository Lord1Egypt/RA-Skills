<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-21 | Updated: 2026-04-21 -->

# cards

## Purpose
Extracted knowledge cards in structured JSON format. These are the processed outputs from PDF extraction, used as the source for vector indexing and retrieval.

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `papers/` | Knowledge cards extracted from SCI research papers (11 cards) |
| `experiences/` | Knowledge cards extracted from clinical experience articles (25 cards) |

## For AI Agents

### Working In This Directory
- These files are auto-generated - do not edit manually
- Re-run `../scripts/extract_knowledge_cards.py` to regenerate
- Each card follows the schema in `../../references/knowledge-card-schema.md`

### Card Structure Overview
Each knowledge card contains:
- **Metadata**: `card_id`, `source_type`, `source_file`, `title`, `authors`, `year`, `language`
- **Content**: `abstract`, `conclusions`, `knowledge_points`
- **Relations**: `related_constitutions`, `related_diseases`
- **Evidence**: `evidence_sentences` with source citations

### Card ID Convention
| Pattern | Source | Example |
|---------|--------|---------|
| `WQ-SCI-XXX` | SCI Papers | `WQ-SCI-001`, `WQ-SCI-011` |
| `WQ-EXP-XXX` | Clinical Experience | `WQ-EXP-001`, `WQ-EXP-025` |

### Testing Requirements
- Validate JSON syntax for all cards
- Check required fields are populated
- Verify `card_id` uniqueness

## Dependencies

### Internal
- `../../references/knowledge-card-schema.md` - Schema definition
- `../../scripts/build_local_index.py` - Consumes cards for indexing

### External
- None (JSON data files)

<!-- MANUAL: -->
