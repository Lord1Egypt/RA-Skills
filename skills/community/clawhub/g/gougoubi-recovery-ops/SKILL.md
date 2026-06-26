---
name: gougoubi-recovery-ops
description: Detect and repair partial failures in Gougoubi PBFT operations, including missing activation, missing risk LP, missing results, and pending reward claims. Use when earlier batch workflows only partially succeeded.
metadata:
  pattern: reviewer
  interaction: single-turn
  domain: gougoubi-pbft
  outputs: structured-json
  clawdbot:
    emoji: "🛠️"
    os: ["darwin", "linux", "win32"]
---

# Gougoubi Recovery Ops

Use this skill to scan a proposal, identify gaps, and repair only the missing parts.

## Use This Skill When

- A batch activation or LP workflow partially failed.
- Some conditions still have `result=0`.
- Rewards may be claimable but have not been claimed.
- The user wants targeted repair instead of rerunning everything.

## Do Not Use This Skill When

- The user wants a fresh proposal creation flow.
- The user already knows the exact missing condition and only wants one isolated action.

## Input

```json
{
  "proposalAddress": "0x...",
  "repair": [
    "activate-missing",
    "risklp-missing",
    "submit-result-missing",
    "claim-pending"
  ],
  "riskLpPerCondition": "optional",
  "forcedResultForPending": "yes|no|optional"
}
```

## Reviewer + Repair Flow

Step 1: Scan all proposal conditions and classify gaps.

Step 2: Report detections by repair class:
- `activateMissing`
- `riskLpMissing`
- `resultMissing`
- `claimPending`

Step 3: Build the smallest possible repair plan.

Step 4: Execute only the requested repair modules.

Step 5: Re-scan and return the final report.

## Checkpoints

- Do not rerun healthy conditions.
- Prefer single-condition or smallest-scope repair first.
- Keep detection counts separate from repaired counts.

## Output

```json
{
  "ok": true,
  "proposalAddress": "0x...",
  "detected": {
    "activateMissing": 0,
    "riskLpMissing": 0,
    "resultMissing": 0,
    "claimPending": 0
  },
  "repaired": {
    "activate": 0,
    "riskLp": 0,
    "result": 0,
    "claim": 0
  },
  "txHashes": [],
  "failed": [],
  "warnings": []
}
```

Failure:

```json
{
  "ok": false,
  "stage": "scan|repair|confirm",
  "error": "reason",
  "retryable": true
}
```

## Project Scripts

- `scripts/pbft-activate-and-add-risklp.mjs`
- `scripts/pbft-submit-all-condition-results.mjs`
- `scripts/pbft-submit-real-results-ba0c-resolved-only.mjs`
- `scripts/pbft-submit-remaining-no-ba0c.mjs`
- `scripts/pbft-claim-rewards-profile-method.mjs`

## Boundaries

- Recovery runs must stay idempotent where possible.
- Do not widen scope beyond the user's requested repair set.
