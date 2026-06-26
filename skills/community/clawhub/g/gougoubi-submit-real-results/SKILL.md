---
name: gougoubi-submit-real-results
description: Submit real-world outcomes for Gougoubi conditions using deterministic evidence from condition skills and public market data. Use when users want resolved-only submission, full settlement checks, or forced fallback submission for pending conditions.
metadata:
  pattern: pipeline
  interaction: single-turn
  domain: gougoubi-pbft
  outputs: structured-json
  clawdbot:
    emoji: "✅"
    os: ["darwin", "linux", "win32"]
---

# Gougoubi Submit Real Results

Use this skill to map external evidence to on-chain condition results and submit one result per condition.

## Use This Skill When

- The user wants to submit real outcomes for all conditions in a proposal.
- The user wants to submit only officially resolved conditions first.
- The user wants a forced fallback such as `No` for remaining unresolved conditions.

## Do Not Use This Skill When

- The user only wants to inspect missing results without submitting. Use `gougoubi-recovery-ops`.
- The user only wants activation or LP staking.

## Input

```json
{
  "proposalAddress": "0x...",
  "mode": "resolved-only|all|force",
  "forceResult": "yes|no",
  "evidenceNote": "optional"
}
```

Defaults:

- `mode=resolved-only`
- `evidenceNote` should be auto-generated when missing

## Pipeline

Step 1: Validate proposal address and target chain.

Step 2: Enumerate all conditions under the proposal.

Step 3: Read each condition `skills` payload and extract evidence locators such as event slug or market id.

Step 4: Fetch public evidence and build a result map:
- `resolved-only`: only officially resolved markets
- `all`: all markets with clear final outcomes
- `force`: use the same forced side for still-pending conditions

Step 5: For each target condition:
- Skip if `result != 0`
- Skip if the condition is not ready for submission
- Submit exactly one result vote

Step 6: Return submitted, skipped, failed, and tx hashes.

## Checkpoints

- Prefer `resolved-only` unless the user explicitly asks for `all` or `force`.
- Never duplicate a submission for a condition that already has `result != 0`.
- Keep evidence mapping and tx results together in the output.

## Output

```json
{
  "ok": true,
  "proposalAddress": "0x...",
  "mode": "resolved-only|all|force",
  "submittedCount": 0,
  "skippedCount": 0,
  "failedCount": 0,
  "submitted": [
    {
      "index": 0,
      "conditionAddress": "0x...",
      "conditionName": "",
      "result": 1,
      "txHash": "0x..."
    }
  ],
  "skipped": [],
  "failed": [],
  "warnings": []
}
```

Failure:

```json
{
  "ok": false,
  "stage": "validation|fetch-evidence|submit|confirm",
  "error": "reason",
  "retryable": true
}
```

## Project Scripts

- `scripts/pbft-submit-all-condition-results.mjs`
- `scripts/pbft-submit-results-from-skills-once.mjs`
- `scripts/pbft-submit-real-results-1605.mjs`
- `scripts/pbft-submit-real-results-c427-confirmed.mjs`
- `scripts/pbft-submit-real-results-ba0c-resolved-only.mjs`
- `scripts/pbft-submit-remaining-no-ba0c.mjs`

## Script Entry Points

- Generic fixed-side submission: `scripts/pbft-submit-all-condition-results.mjs`
- Generic skills-derived submission: `scripts/pbft-submit-results-from-skills-once.mjs`
- `node scripts/pbft-submit-all-condition-results.mjs --help`
- `node scripts/pbft-submit-all-condition-results.mjs <proposalAddress> --result yes --dry-run`
- `node scripts/pbft-submit-results-from-skills-once.mjs --help`
- `node scripts/pbft-submit-results-from-skills-once.mjs <proposalAddress>`
- Specialized scripts also support `--help` for their fixed proposal mappings.

## Boundaries

- Do not infer unresolved results unless the user explicitly asks for `all` or `force`.
- Preserve an auditable mapping from evidence to submitted result.
