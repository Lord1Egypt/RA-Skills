# Sift Schemas

## SearchQuery
```json
{
  "query_id": "string",
  "original_query": "string",
  "rewritten_queries": ["string"],
  "tier": "number — 1|2|3",
  "context": "string|null — conversation or Chronicle context used for rewriting"
}
```

## SearchSession
```json
{
  "session_id": "string",
  "query": "SearchQuery",
  "provider_telemetry": {
    "provider": "string",
    "latency_ms": "number",
    "results_returned": "number",
    "results_used": "number"
  },
  "entities_extracted": ["ExtractedEntity"],
  "sources_used": ["string — URLs"],
  "timestamp": "string — ISO 8601"
}
```

## ResearchThread
```json
{
  "thread_id": "string",
  "topic": "string",
  "entity_overlap": ["string — entity IDs appearing across sessions"],
  "session_ids": ["string"],
  "status": "string — active|complete|stale"
}
```

## ExtractedEntity
```json
{
  "entity_id": "string",
  "name": "string",
  "type": "string — Entity|Place|Concept|Thing (from shared ontology)",
  "relationships": [{"target": "string", "type": "string"}],
  "confidence": "string — high|med|low",
  "source_refs": [{"url": "string", "quote": "string"}]
}
```

## SourceReputation
```json
{
  "domain": "string",
  "trust_score": "number — 0.0 to 1.0",
  "agreement_rate": "number",
  "contradiction_rate": "number",
  "last_updated": "string — ISO 8601"
}
```

## EnrichmentCandidate
```json
{
  "candidate_entity": "ExtractedEntity",
  "proposed_type": "string — from shared ontology",
  "confidence": "string — high|med|low",
  "source_refs": ["object"]
}
```

## DecisionRecord
Extends shared DecisionRecord. Sift-specific types: tier_escalation, entity_extraction, thread_merge, source_reputation_update.
