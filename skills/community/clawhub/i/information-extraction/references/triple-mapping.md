# Triple Mapping

Map normalized intermediate records into triples only after extraction and normalization.

## Relation to triple

Direct mapping:

```json
{
  "subject": "OpenAI",
  "predicate": "published",
  "object": "GPT-4 Technical Report"
}
```

## Attribute to triple

Convert an attribute into a predicate-value triple.

Attribute record:

```json
{
  "entity_id": "ent_002",
  "attribute": "year",
  "value": "2023"
}
```

Triple:

```json
{
  "subject": "GPT-4 Technical Report",
  "predicate": "year",
  "object": "2023"
}
```

## Event to triples

Prefer event-centered mapping for complex events.

Event record:

```json
{
  "id": "ev_001",
  "type": "Publication",
  "participants": {
    "agent": "ent_001",
    "object": "ent_002"
  },
  "time": "2023"
}
```

Possible triples:

```json
[
  {"subject": "OpenAI", "predicate": "published", "object": "GPT-4 Technical Report"},
  {"subject": "ev_001", "predicate": "occurs_at", "object": "2023"},
  {"subject": "ev_001", "predicate": "is_a", "object": "Publication"}
]
```

## Evidence and confidence

When possible, carry these fields alongside exported triples:
- `evidence`
- `confidence`

## Deduplication rule

If two triples are identical in subject, predicate, and object, keep one and merge evidence where useful.
