---
name: gougoubi-create-condition
description: Create a Gougoubi proposal condition from minimal input with deterministic defaults for deadline, trade deadline, normalization, and transaction submission. Use when users want to add conditions to an existing proposal.
metadata:
  pattern: generator
  interaction: single-turn
  domain: gougoubi-pbft
  outputs: structured-json
  clawdbot:
    emoji: "🧩"
    os: ["darwin", "linux", "win32"]
---

# Gougoubi Create Condition

Use this skill to create a condition under an existing Gougoubi proposal from the smallest practical input.

## Use This Skill When

- The user wants to add one or more conditions to an existing proposal.
- The user only provides proposal identifier and condition title.
- The agent should auto-fill default dates and flags.

## Do Not Use This Skill When

- The user wants to create a new proposal. Use `gougoubi-create-prediction`.
- The user wants activation, result submission, or reward claiming.

## Minimal Input

```json
{
  "proposalId": "0x... or proposal identifier",
  "conditionName": "Will Team A win the match?"
}
```

## Defaults

- Resolve `proposalId` to `proposalAddress`.
- `deadlineDateTime`: proposal deadline.
- `deadlineTimezone`: user locale, fallback `UTC`.
- `tradeDeadlineDateTime`: `deadlineDateTime - 1 hour`, clamped to a valid future time.
- `tradeDeadlineTimezone`: same as `deadlineTimezone`.
- `conditionImageUrl`: empty string.
- `conditionRules`: empty string.
- `skills`: empty string.
- `isNormalized`: `true`.

## Generator Flow

Step 1: Validate minimal input.

Step 2: Resolve proposal and load proposal deadline.

Step 3: Generate all default date fields and clamp invalid values.

Step 4: Convert datetimes to unix seconds.

Step 5: Validate final payload:
- `conditionName` non-empty
- `deadline > now`
- `tradeDeadline > now`
- `tradeDeadline <= deadline`

Step 6: Submit the canonical contract call in this order:
1. `conditionName`
2. `deadline`
3. `tradeDeadline`
4. `conditionImageUrl`
5. `conditionRules`
6. `skills`
7. `isNormalized`

Step 7: Wait for confirmation and return the normalized payload.

## Output

```json
{
  "ok": true,
  "mode": "browser|contract",
  "txHash": "0x...",
  "proposalAddress": "0x...",
  "normalizedInput": {
    "proposalId": "",
    "proposalAddress": "",
    "conditionName": "",
    "deadlineDateTime": "",
    "deadlineTimezone": "",
    "tradeDeadlineDateTime": "",
    "tradeDeadlineTimezone": "",
    "defaultsApplied": true,
    "tradeDeadlinePolicy": "deadline-minus-1h-with-valid-clamp"
  },
  "warnings": []
}
```

Failure:

```json
{
  "ok": false,
  "stage": "validation|resolve-proposal|create|confirm",
  "error": "reason",
  "retryable": true
}
```

## Boundaries

- Never bypass wallet confirmation.
- Keep defaults deterministic and explain them in output when relevant.
