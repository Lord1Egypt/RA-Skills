---
name: information-extraction
description: Extract structured information from unstructured text through a semi-automatic pipeline. Support entity extraction, relation extraction, attribute extraction, and event extraction from plain text and Markdown. Use when converting raw text into triples, graph-ready records, or normalized structured facts from documents, notes, reports, transcripts, and web content copied as text.
---

# Information Extraction

Extract entity, relation, attribute, and event information from text into a normalized intermediate structure, then export triples in JSON, JSONL, or TSV.

## Core workflow

1. Define extraction scope and output granularity.
2. Segment input text into sentences and paragraphs.
3. Extract entities with evidence.
4. Extract relations, attributes, and events.
5. Normalize aliases, predicates, and duplicated records.
6. Export triples. Default output is JSON.
7. Review ambiguities before treating output as final.

## Input scope

Prefer this skill for:
- Plain text strings
- Markdown text
- Text copied from webpages, notes, reports, transcripts, or documents

If the user provides a file in another format, convert it to text first, then use this skill.

## Output contract

Default output should contain:

```json
{
  "triples": [],
  "entities": [],
  "attributes": [],
  "events": [],
  "ambiguities": []
}
```

Support export formats:
- JSON (default)
- JSONL
- TSV

## Extraction principles

- Extract explicit facts before inference.
- Preserve evidence spans for important records.
- Prefer controlled predicates from `references/relation-taxonomy.md`.
- Keep attributes and events separate internally, even when final output is triples.
- Do not flatten complex events too early.
- Normalize before exporting.
- Record unresolved ambiguity instead of pretending certainty.

## Minimal internal schema

Use these record shapes during extraction.

### Entity

```json
{
  "id": "ent_001",
  "mention": "OpenAI",
  "canonical_name": "OpenAI",
  "type": "Organization",
  "evidence": "OpenAI published the GPT-4 Technical Report.",
  "confidence": 0.95
}
```

### Relation

```json
{
  "subject": "ent_001",
  "predicate": "published",
  "object": "ent_002",
  "evidence": "OpenAI published the GPT-4 Technical Report.",
  "confidence": 0.93
}
```

### Attribute

```json
{
  "entity_id": "ent_002",
  "attribute": "year",
  "value": "2023",
  "evidence": "The report was released in 2023.",
  "confidence": 0.87
}
```

### Event

```json
{
  "id": "ev_001",
  "type": "Publication",
  "trigger": "published",
  "participants": {
    "agent": "ent_001",
    "object": "ent_002"
  },
  "time": "2023",
  "location": null,
  "evidence": "OpenAI published the GPT-4 Technical Report in 2023.",
  "confidence": 0.92
}
```

## How to use references

- Read `references/pipeline.md` for the end-to-end procedure.
- Read `references/schema.md` for types and intermediate record structure.
- Read `references/relation-taxonomy.md` before inventing new predicates.
- Read `references/triple-mapping.md` when exporting final triples.
- Read `references/event-modeling.md` when text describes complex events.
- Read `references/quality-checklist.md` before final delivery.

## Scripts

### Extract

```bash
python3 skills/information-extraction/scripts/extract.py --text "OpenAI published GPT-4." --output out.json
```

Or read from stdin:

```bash
echo "OpenAI published GPT-4." | python3 skills/information-extraction/scripts/extract.py --stdin --output out.json
```

### Normalize

```bash
python3 skills/information-extraction/scripts/normalize.py --input out.json --output normalized.json
```

### Export triples

```bash
python3 skills/information-extraction/scripts/export_triples.py --input normalized.json --format json --output triples.json
python3 skills/information-extraction/scripts/export_triples.py --input normalized.json --format jsonl --output triples.jsonl
python3 skills/information-extraction/scripts/export_triples.py --input normalized.json --format tsv --output triples.tsv
```

## Notes on automation

This is a semi-automatic pipeline, not a claim of perfect extraction. The scripts provide scaffolding, normalization, and export. For high-stakes outputs, keep evidence and perform manual review.
