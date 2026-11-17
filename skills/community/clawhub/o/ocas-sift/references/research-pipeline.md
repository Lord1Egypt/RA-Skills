# Sift — Research Pipeline

Sift maintains per-domain trust scores based on: cross-source agreement, contradiction frequency, historical accuracy, structured data quality, citation frequency.

## Structured extraction rules

When pages are retrieved, extract: entities (with type from shared ontology), claims, statistics, relationships, citations. Each extraction includes confidence level.

Extracted entities are emitted as enrichment candidates for See references/integration-notes.md for current backend architecture..

## Run completion

After every Sift command that produces results:

1. Persist session, entities, sources, and decisions to local JSONL files
2. For each extracted entity or relationship with confidence >= `med`: write a Signal file to the `signal` payload field in the journal entry. Use Signal schema from `spec-ocas-shared-schemas.md`. Every Signal must include `user_relevance` (see Ontology types section). Set `"user"` if the run was user-initiated or the entity connects to a `user_relevance: "user"` Chronicle entry; otherwise `"agent_only"`.
3. Write journal via `sift.journal`
