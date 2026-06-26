---
name: gougoubi-activate-created-conditions
description: Activate all CREATED conditions under a Gougoubi proposal with deterministic committee checks, optional auto-stake joining, and structured voting results. Use when users want to activate proposal conditions by proposal id or proposal address.
metadata:
  pattern: pipeline
  interaction: single-turn
  domain: gougoubi-pbft
  outputs: structured-json
  clawdbot:
    emoji: "🗳️"
    os: ["darwin", "linux", "win32"]
---

# Gougoubi Activate Created Conditions

Use this skill when the user wants to activate all currently `CREATED` conditions under a proposal.

## Use This Skill When

- The user asks to activate a proposal.
- The user asks to vote on all created conditions.
- The workflow should auto-join the committee when needed.

## Do Not Use This Skill When

- The user also wants risk LP added in the same run. Use `gougoubi-activate-and-stake-risklp`.
- The user wants result submission or reward claiming.

## Input

```json
{
  "proposalId": "number|string",
  "bnbAddress": "0x...",
  "approve": true,
  "minBnbForGas": "0.001"
}
```

## Pipeline

Step 1: Validate `proposalId` and `bnbAddress`.

Step 2: Check wallet, chain, and gas balance.

Step 3: Resolve `proposalAddress` from `proposalId`.

Step 4: Check committee membership.

Step 5: If not a member, auto-stake the minimum required amount and confirm membership.

Step 6: Enumerate all `CREATED` conditions.

Step 7: Vote `true` on each `CREATED` condition, one transaction at a time.

Step 8: Return structured success and failure details.

## Checkpoints

- Only vote on `CREATED` conditions.
- If one condition fails, continue and report it.
- If no `CREATED` conditions exist, return success with warning `no-created-conditions`.
- Load [references/CONTRACT_METHODS.md](references/CONTRACT_METHODS.md) when contract method details are needed.

## Output

```json
{
  "ok": true,
  "proposalId": 0,
  "proposalAddress": "0x...",
  "bnbAddress": "0x...",
  "committeeJoinedByStake": false,
  "stakeTxHash": "0x... or null",
  "createdConditionCount": 0,
  "attemptedConditionCount": 0,
  "successCount": 0,
  "failedCount": 0,
  "successes": [
    {
      "conditionAddress": "0x...",
      "txHash": "0x..."
    }
  ],
  "failures": [
    {
      "conditionAddress": "0x...",
      "error": "human readable reason"
    }
  ],
  "warnings": [],
  "nextActions": []
}
```

Failure:

```json
{
  "ok": false,
  "stage": "validation|wallet|gas-check|resolve-proposal|stake-committee|approve|activate-vote|confirm",
  "error": "human readable reason",
  "retryable": true
}
```

## Boundaries

- Do not bypass wallet confirmation.
- Do not widen scope beyond `CREATED` conditions.
- Keep Chinese user-facing errors concise and actionable.
