# Voyage Journal Format

## Journal Outputs

**Action Journal** — all planning, recommendation, and reservation runs.

## Journal Path

`{agent_root}/commons/journals/ocas-voyage/YYYY-MM-DD/{run_id}.json`

## Journal Payload

Every Voyage journal entry includes:

```json
{
  "skill_id": "ocas-voyage",
  "run_id": "uuid",
  "timestamp": "ISO8601",
  "command": "voyage.plan.trip|voyage.recommend.lodging|...",
  "outcome": "success|partial|error",
  "entities_observed": [
    {
      "type": "Place|Concept/Event|Concept/Action|Entity/Person",
      "name": "string",
      "context": "string",
      "user_relevance": "user|agent_only|unknown"
    }
  ],
  "relationships_observed": ["string"],
  "preferences_observed": ["string"],
  "decision": {
    "summary": "string",
    "items_evaluated": 0,
    "items_recommended": 0
  }
}
```

## Entity Relevance

- `user` — entity directly related to the user's world (destinations, hotels, companions, reservations)
- `agent_only` — entity encountered incidentally (landmark mentioned only as routing waypoint)
- `unknown` — relevance is unclear

Most Voyage entities are `user`-relevant since they represent the user's actual travel plans and destinations.
