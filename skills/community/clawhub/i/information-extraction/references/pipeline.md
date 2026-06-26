# Extraction Pipeline

## 1. Define scope

Before extracting, decide:
- which entity types matter
- whether attributes should stay as properties or become triples
- whether the text contains real events or only static facts
- whether uncertain statements should be excluded or flagged

## 2. Segment the text

Split by paragraphs and then by sentences. Preserve original sentence text for evidence.

Recommended fields:
- `paragraph_index`
- `sentence_index`
- `sentence_text`

## 3. Extract entities

For each candidate entity mention:
- capture mention text
- assign canonical name
- assign type
- attach evidence sentence
- estimate confidence

Use conservative typing. If type is unclear, prefer `Object` or `Concept` over hallucinating a fine-grained type.

## 4. Extract relations

Identify directional relations between resolved entities.

Guidelines:
- use controlled predicates when possible
- keep predicate names stable across records
- record evidence per relation
- avoid creating relations whose arguments are unresolved

## 5. Extract attributes

Treat descriptive values as attributes when they belong to one entity.

Examples:
- size
- color
- title
- year
- quantity
- role

If the final requested format is triples, map attributes after extraction.

## 6. Extract events

Create an event record when the text describes:
- an action
- a change of state
- a publication or creation
- participation
- an occurrence in time or space

Record:
- event type
- trigger
- participants
- time
- location
- evidence

## 7. Normalize

Perform normalization after initial extraction:
- merge aliases and repeated mentions
- standardize predicate names
- deduplicate repeated triples
- resolve simple pronouns only when evidence is strong
- keep an ambiguity list for unresolved cases

## 8. Export

Export triples only after normalization. Default output is JSON, but JSONL and TSV should also be available.

## 9. Review

Before final delivery, check:
- missing core entities
- relation direction
- event flattening errors
- unsupported inferences
- evidence coverage
