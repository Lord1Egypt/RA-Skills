# Mentor Schemas

## Project
```json
{"project_id":"string","goal":"string","constraints":"object","requested_output":"string","status":"string","created_at":"string","updated_at":"string"}
```

## TaskNode
```json
{"task_id":"string","title":"string","description":"string","dependencies":["string"],"candidate_skill":"string","status":"string — pending|ready|running|blocked|failed|complete|archived","retry_count":"number","priority":"number","expected_artifacts":["string"],"blocking_reason":"string|null"}
```

## SkillInvocation
```json
{"task_id":"string","skill_name":"string","skill_version":"string","input_hash":"string","start_time":"string","end_time":"string","success":"boolean","retry_count":"number","artifacts_produced":["string"],"model":"string|null","provider":"string|null"}
```

## VariantProposal
See spec-ocas-shared-schemas.md for the canonical VariantProposal schema.

Written to: `~/openclaw/data/ocas-forge/intake/{proposal_id}.json`

## VariantDecision
See spec-ocas-shared-schemas.md for the canonical VariantDecision schema.

Written to: `~/openclaw/data/ocas-forge/intake/{decision_id}.json`
