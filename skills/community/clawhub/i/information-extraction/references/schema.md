# Intermediate Schema

## Entity types

Use a compact default type inventory:
- Person
- Organization
- Location
- Time
- Product
- Document
- Concept
- Object
- Quantity
- Event

## Entity record

```json
{
  "id": "ent_001",
  "mention": "OpenAI",
  "canonical_name": "OpenAI",
  "type": "Organization",
  "evidence": "OpenAI published the GPT-4 Technical Report.",
  "confidence": 0.95,
  "metadata": {}
}
```

## Relation record

```json
{
  "subject": "ent_001",
  "predicate": "published",
  "object": "ent_002",
  "evidence": "OpenAI published the GPT-4 Technical Report.",
  "confidence": 0.93,
  "metadata": {}
}
```

## Attribute record

```json
{
  "entity_id": "ent_002",
  "attribute": "year",
  "value": "2023",
  "evidence": "The report was released in 2023.",
  "confidence": 0.87,
  "metadata": {}
}
```

## Event record

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
  "confidence": 0.92,
  "metadata": {}
}
```

## Ambiguity record

```json
{
  "kind": "coreference",
  "text": "it",
  "candidates": ["ent_001", "ent_003"],
  "evidence": "It later expanded globally.",
  "note": "Insufficient evidence to resolve confidently."
}
```

## Top-level output

```json
{
  "triples": [],
  "entities": [],
  "attributes": [],
  "events": [],
  "ambiguities": []
}
```
