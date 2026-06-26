---
name: gougoubi-claim-all-rewards
description: Claim all Gougoubi rewards for one or more addresses, including winner rewards, governance rewards, and LP rewards. Use when users want one-click claiming without scanning every condition.
metadata:
  pattern: pipeline
  interaction: single-turn
  domain: gougoubi-pbft
  outputs: structured-json
  clawdbot:
    emoji: "💰"
    os: ["darwin", "linux", "win32"]
---

# Gougoubi Claim All Rewards

Use this skill for one-click reward claiming across one or multiple addresses.

## Use This Skill When

- The user wants to claim all rewards for one address or multiple addresses.
- The user explicitly wants the profile-style fast path.
- The user wants winner, governance, and LP rewards claimed together.

## Do Not Use This Skill When

- The user wants to inspect missing results before claiming. Use `gougoubi-recovery-ops`.
- The user wants proposal activation or LP staking. Use activation skills instead.

## Input

```json
{
  "addresses": ["0x...", "0x...", "0x..."],
  "method": "profile|quick|full-scan"
}
```

Defaults:

- `method=profile`

## Pipeline

Step 1: Validate all addresses.

Step 2: Pick claim method:
- `profile`: match the reward-detail modal behavior.
- `quick`: fast direct claim path.
- `full-scan`: exhaustive fallback only when needed.

Step 3: Run claim for each address.

Step 4: Record all tx hashes and per-type claim status when available.

Step 5: Return a full summary.

## Checkpoints

- Prefer `profile` unless the user explicitly asks otherwise.
- Do not force slow condition scanning when the user asked for one-click claim.
- Safe re-run behavior is required.

## Output

```json
{
  "ok": true,
  "method": "profile",
  "addresses": ["0x..."],
  "claimedTxCount": 0,
  "results": [
    {
      "address": "0x...",
      "winnerRewardClaimed": true,
      "governanceRewardClaimed": true,
      "lpRewardClaimed": true,
      "txHashes": ["0x..."]
    }
  ],
  "warnings": []
}
```

Failure:

```json
{
  "ok": false,
  "stage": "validation|claim|confirm",
  "error": "reason",
  "retryable": true
}
```

## Project Scripts

- `scripts/pbft-claim-rewards-profile-method.mjs`
- `scripts/pbft-claim-rewards-quick.mjs`
- `scripts/pbft-claim-three-address-rewards.mjs`

## Script Entry Points

- Preferred profile path: `scripts/pbft-claim-rewards-profile-method.mjs`
- Fast one-click path: `scripts/pbft-claim-rewards-quick.mjs`
- Deep scan path: `scripts/pbft-claim-three-address-rewards.mjs`
- `node scripts/pbft-claim-rewards-profile-method.mjs --help`
- `node scripts/pbft-claim-rewards-profile-method.mjs --dry-run`
- `node scripts/pbft-claim-rewards-quick.mjs --dry-run`
- `node scripts/pbft-claim-three-address-rewards.mjs --dry-run`

## Boundaries

- Claim all three reward classes together when available.
- Keep the method explicit in the output.
