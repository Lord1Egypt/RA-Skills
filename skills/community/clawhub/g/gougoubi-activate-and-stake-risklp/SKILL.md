---
name: gougoubi-activate-and-stake-risklp
description: Activate Gougoubi proposal conditions and stake risk LP per condition in one deterministic workflow. Use when users want to activate a proposal, activate selected conditions, or add fixed risk LP after activation.
metadata:
  pattern: pipeline
  interaction: single-turn
  domain: gougoubi-pbft
  outputs: structured-json
  clawdbot:
    emoji: "⚡"
    os: ["darwin", "linux", "win32"]
---

# Gougoubi Activate And Stake Risk LP

Use this skill for the combined execution flow: activate first, then add risk LP.

## Use This Skill When

- The user wants to activate a proposal and add risk LP in one run.
- The user wants fixed risk LP per condition.
- The user wants to repair missing activation or missing LP on a small scope.

## Do Not Use This Skill When

- The user only wants result submission. Use `gougoubi-submit-real-results`.
- The user only wants reward claiming. Use `gougoubi-claim-all-rewards`.
- The user only wants condition creation. Use `gougoubi-create-condition`.

## Input

```json
{
  "proposalAddress": "0x...",
  "riskLpPerCondition": "100",
  "scope": "all|only-created|single",
  "conditionIndex": 0
}
```

Defaults:

- `scope=all`
- `riskLpPerCondition=100`

## Pipeline

Step 1: Validate input and resolve proposal.

Step 2: Ensure there are enough usable committee voters. Auto-join committee with minimum stake when required.

Step 3: Enumerate conditions by `scope`.

Step 4: For each selected condition:
- If status is `CREATED`, vote to activate.
- Wait until the condition is `ACTIVE`.
- Add risk LP exactly once unless the user explicitly asked to top up.

Step 5: Return per-condition activation and LP results.

## Checkpoints

- Do not add LP before the condition is `ACTIVE`.
- Keep activation failures and LP failures separate.
- Continue past single-condition failures and report them.

## Output

```json
{
  "ok": true,
  "proposalAddress": "0x...",
  "activatedCount": 0,
  "riskLpAddedCount": 0,
  "activated": [],
  "riskLpAdded": [],
  "activationFailed": [],
  "riskLpFailed": [],
  "warnings": [],
  "nextActions": []
}
```

Failure:

```json
{
  "ok": false,
  "stage": "validation|resolve-proposal|join-committee|activate|add-risklp|confirm",
  "error": "reason",
  "retryable": true
}
```

## Project Scripts

- `scripts/pbft-activate-and-add-risklp.mjs`
- `scripts/pbft-join-and-activate-all-conditions.mjs`
- `scripts/pbft-add-risk-lp-to-proposal.mjs`

## Script Entry Points

- Preferred combined entry: `scripts/pbft-activate-and-add-risklp.mjs`
- `node scripts/pbft-activate-and-add-risklp.mjs --help`
- `node scripts/pbft-activate-and-add-risklp.mjs <proposalAddress> <riskLpAmount> --dry-run`
- Use `--dry-run` before execution when installing or validating this skill in a new environment.

## Boundaries

- Never add LP to an inactive condition.
- Do not top up existing LP unless the user explicitly asks.
- Keep the workflow idempotent where possible.
