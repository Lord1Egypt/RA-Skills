---
name: gougoubi-market-orchestrator
description: Orchestrate end-to-end Gougoubi market operations by routing to the right skill for creation, activation, risk LP, result submission, reward claiming, or recovery. Use when users describe a high-level market task rather than a single low-level action.
metadata:
  pattern: inversion
  interaction: multi-turn
  domain: gougoubi-pbft
  outputs: structured-json
  clawdbot:
    emoji: "🧭"
    os: ["darwin", "linux", "win32"]
---

# Gougoubi Market Orchestrator

Use this skill as the top-level router for Gougoubi PBFT workflows.

## Use This Skill When

- The user describes a complete market workflow.
- The request spans multiple stages such as create, activate, add LP, settle, and claim.
- The agent needs to decide which Gougoubi skill to invoke next.

## Routing Rules

Map the user intent to one or more skills:

- Create proposal: `gougoubi-create-prediction`
- Create condition: `gougoubi-create-condition`
- Activate only: `gougoubi-activate-created-conditions`
- Activate + risk LP: `gougoubi-activate-and-stake-risklp`
- Submit results: `gougoubi-submit-real-results`
- Claim rewards: `gougoubi-claim-all-rewards`
- Repair partial failures: `gougoubi-recovery-ops`

## Inversion Flow

Phase 1: Identify the current market stage:
- proposal creation
- condition creation
- activation
- liquidity staking
- result submission
- reward claiming
- recovery

Phase 2: Detect missing prerequisites:
- proposal exists or not
- condition exists or not
- committee ready or not
- result already submitted or not
- rewards claimable or not

Phase 3: Choose the smallest correct downstream skill and execute it.

Phase 4: Return a compact operation summary:
- selected skill
- why it was selected
- inputs passed through
- outcome
- recommended next action

## Checkpoints

- Do not use this skill to reimplement downstream logic.
- Keep routing explicit and auditable.
- Prefer the smallest skill that fully solves the current stage.

## Output

```json
{
  "ok": true,
  "selectedSkill": "gougoubi-activate-and-stake-risklp",
  "reason": "user asked to activate proposal and add fixed risk LP",
  "stage": "activation-and-liquidity",
  "nextAction": "submit results after deadline",
  "result": {}
}
```
