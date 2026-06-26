# Corvus Schemas

## Hypothesis

```json
{
  "hypothesis_id": "string",
  "graph_region": "string — area of the graph being investigated",
  "hypothesis_text": "string — what the hypothesis proposes",
  "drive_source": "string — novelty|uncertainty|prediction_error",
  "evidence_refs": ["string — signal or entity IDs supporting the hypothesis"],
  "confidence": "string — high|med|low",
  "status": "string — active|validated|rejected|promoted",
  "created_at": "string — ISO 8601",
  "updated_at": "string — ISO 8601"
}
```

## Pattern

```json
{
  "pattern_id": "string",
  "pattern_type": "string — routine|thread|interest|anomaly|opportunity",
  "description": "string",
  "signal_refs": ["string — signal IDs that support the pattern"],
  "confidence": "string — high|med|low",
  "validation_status": "string — pending|validated|rejected",
  "temporal_data": {
    "first_observed": "string — ISO 8601",
    "last_observed": "string — ISO 8601",
    "interval_estimate": "string|null — estimated recurrence interval"
  }
}
```

## InsightProposal

```json
{
  "proposal_id": "string",
  "proposal_type": "string — routine_prediction|thread_continuation|opportunity_discovery|anomaly_alert",
  "description": "string",
  "confidence_score": "number — 0.0 to 1.0",
  "supporting_entities": ["string — entity IDs"],
  "supporting_relationships": ["string — relationship IDs"],
  "predicted_outcome": "string|null",
  "suggested_follow_up": "string|null"
}
```

## CuriositySignal

```json
{
  "signal_id": "string",
  "drive_type": "string — novelty|uncertainty|prediction_error",
  "target_region": "string — graph region identifier",
  "priority_score": "number — 0.0 to 1.0",
  "timestamp": "string — ISO 8601"
}
```

## DecisionRecord

Extends the shared DecisionRecord schema from spec-ocas-shared-schemas.md

Additional Corvus-specific decision types: pattern_validated, pattern_rejected, hypothesis_promoted, proposal_generated.
