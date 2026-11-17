# Router contract

The router is a constrained classifier, not a general-purpose agent.

## Input

```json
{
  "request": "natural-language request from the current session",
  "candidate_groups": {
    "branch_a": "short description",
    "branch_b": "short description"
  }
}
```

Do not include private history, secrets, or user-supplied internal IDs unless the local policy explicitly requires a redacted identifier for disambiguation.

## Output

```json
{
  "group_key": "branch_a",
  "group_id": "value resolved from the local allowlist",
  "confidence": 0.0,
  "needs_confirmation": false,
  "query": "normalized retrieval query",
  "decision_source": "jev"
}
```

The host must independently verify every field. A valid-looking response is not permission by itself: `group_key` and `group_id` must agree with the local allowlist, confidence must meet policy, and the result must be bound to the current request and tool.
