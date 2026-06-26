---
name: gougoubi-create-prediction
description: Create public Gougoubi prediction proposals from minimal input with deterministic enrichment, group creation, approval handling, and transaction submission. Use when users want to publish a new prediction market.
metadata:
  pattern: tool-wrapper
  interaction: single-turn
  domain: gougoubi-pbft
  outputs: structured-json
  clawdbot:
    emoji: "📈"
    os: ["darwin", "linux", "win32"]
---

# Gougoubi Create Prediction

Use this skill to create a new public prediction proposal on Gougoubi from a small, stable input surface.

## Use This Skill When

- The user wants to create or publish a new proposal.
- The user gives a market title and a deadline, and expects the rest to be auto-filled.
- The workflow must create the group before the proposal.

## Do Not Use This Skill When

- The proposal already exists and the user only wants to add conditions.
- The user only wants activation, staking, settlement, or rewards.

## Minimal Input

```json
{
  "marketName": "",
  "deadlineIsoUtc": "2026-05-10T12:00:00Z"
}
```

## Auto-Fills

- `imageUrl`
- `liquidityToken`
- `deadlineTimezone`
- `rules`
- `stakeAmountDoge=10000`
- `tags`
- `groupAddress`
- `language`
- `skills=""`

## Tool Wrapper Rules

Treat the Gougoubi public-create flow as the source of truth.

- Create the community group first.
- Group name must equal proposal name.
- Group description must use the generated rules.
- Group type must be restricted.
- Use the created group address as proposal `groupUrl`.

## Deterministic Flow

Step 1: Validate `marketName` and `deadlineIsoUtc`.

Step 2: Generate `rules` and `tags`.

Step 3: Detect supported language and normalize unsupported values to `en`.

Step 4: Create the community group first.

Step 5: Resolve `groupAddress` from the group creation receipt.

Step 6: Auto-fill remaining fields and convert stake amount to wei.

Step 7: Check DOGE balance and allowance.

Step 8: If needed, request approval and wait for confirmation.

Step 9: Submit proposal creation in canonical order.

Step 10: Wait for receipt and return the tx hash and proposal address when available.

## Output

```json
{
  "ok": true,
  "txHash": "0x...",
  "proposalAddress": "0x... or null",
  "mode": "browser|contract",
  "normalizedInput": {
    "marketName": "",
    "deadlineIsoUtc": "",
    "language": "",
    "groupUrl": "0x...",
    "aiGenerated": {
      "rules": true,
      "tags": true,
      "language": false
    },
    "languageSource": "script-detect-supported-or-en",
    "defaultsApplied": true
  },
  "warnings": []
}
```

Failure:

```json
{
  "ok": false,
  "stage": "validation|ai-enrichment|community-create|approve|create|confirm|resolve",
  "error": "reason",
  "retryable": true
}
```

## Boundaries

- Never skip group creation.
- Never auto-confirm approvals or irreversible wallet actions.
- Require user confirmation if moderation risk is detected.
