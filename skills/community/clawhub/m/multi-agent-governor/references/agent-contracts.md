# Agent Contracts

## Contents

1. Context capsule
2. Explorer output
3. Worker output
4. QA output

## Context Capsule

Every agent receives only:

- `run_id`, `lane_id`, `role`, and current `build_id`;
- one concrete objective;
- absolute input paths;
- explicit ownership;
- exclusions and information boundaries;
- one deliverable description;
- acceptance checks and deadline;
- artifact hashes when reviewing a mutable deliverable.

Do not include the expected answer in a QA capsule. Do not include conclusions from another reviewer unless the lane explicitly adjudicates them.

## Explorer Output

Return structured findings:

```json
{
  "lane_id": "evidence-qa",
  "build_id": "run-b01",
  "status": "complete",
  "findings": [
    {
      "severity": "blocker|high|medium|low",
      "claim": "Concise finding",
      "evidence": ["absolute path or URL with location"],
      "confidence": "high|medium|low",
      "recommended_action": "Specific action"
    }
  ],
  "unresolved": []
}
```

## Worker Output

Return:

- files changed;
- tests or commands run;
- concise behavior summary;
- unresolved blockers;
- build/source hashes used.

Workers must not revert unrelated changes and must stay inside assigned ownership.

## QA Output

Review only the supplied artifact hash. Lead with blockers and high-severity findings. Separate objective defects from preferences. A valid QA finding must include evidence and a concrete correction.

Return `no_blockers` explicitly when appropriate. Do not continue searching merely to produce more findings.
