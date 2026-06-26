---
name: openclaw-cron-standard
version: 0.2.0
description: Standardize OpenClaw cron wrappers, prompt contracts, and delivery-mode expectations. Use when auditing or fixing cron jobs that rely on ClankerHive claims, result JSON artifacts, cron delivery status, wrapper scripts, or reply-vs-message delivery behavior. Prevent stale result files, duplicate-run confusion, claim-string drift, and silent not-delivered runs caused by mismatched delivery.mode settings.
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3"] }
    }
  }
---

# openclaw-cron-standard

Use this skill when cleaning up or designing OpenClaw cron jobs.

## Standard contract

For cron wrappers:

1. Clear the old result artifact before a new run.
2. Claim through one shared helper.
3. If the claim reports `ALREADY_CLAIMED`, print that sentinel, exit 0, and do not write a result artifact.
4. Only write a result JSON for a real execution or a real failure.
5. Keep result artifacts as the source of truth for real runs, not duplicate-run guards.

For cron prompts:

1. Run the wrapper first.
2. If it prints `ALREADY_CLAIMED`, reply only with `NO_REPLY`.
3. Only then read the result JSON.
4. Never read a stale artifact after a duplicate-claim guard path.
5. Match the prompt's delivery contract to the cron job's `delivery.mode`.

## Delivery-mode contract

This is the easy place to break a healthy cron job.

### Use `delivery.mode: announce` when:

- the job returns user-visible text as its final assistant reply
- the prompt says things like `return summary_text exactly`, `return the alert text`, or `return the formatted message`
- the job explicitly says `Do not use the message tool`

### Use `delivery.mode: none` when:

- the job is intentionally silent on success
- the job sends alerts explicitly via the `message` tool
- the job is maintenance-only and should never rely on reply-text fallback delivery

### Common failure mode

If you set `delivery.mode: none` on a cron that still relies on reply-text delivery, the job can:

- run successfully
- generate valid summary text
- update freshness facts
- still never notify the user

That is not a wrapper failure. It is a delivery-contract mismatch.

## Why this matters

The fragile failure mode is usually contract drift across three places:

- wrapper behavior
- prompt behavior
- claim string expectations such as `already claimed` vs `already-claimed`

That drift can turn a healthy duplicate-run guard into a fake failure or a silent not-delivered run. Delivery-mode drift can do the same thing even when the wrapper itself is fine.

## Preferred implementation shape

Use a small shared helper module for:

- `prepare_result_path(...)`
- `claim_or_exit(...)`
- `run(...)`

Keep wrapper-specific business logic outside the shared helper.

## Audit checklist

- no result artifact written on `ALREADY_CLAIMED`
- stale result file is removed before each run
- prompts check the sentinel before reading the artifact
- `delivery.mode` matches the actual delivery contract (`announce` for reply delivery, `none` for explicit message-tool or silent jobs)
- validator passes after edits
- dead scratch wrappers and tmp scripts are removed if unreferenced

## Good migration order

1. Patch the wrapper contract first.
2. Patch the live cron prompt second.
3. Patch `delivery.mode` to match the prompt's real delivery behavior.
4. Validate with the cron validator and any runtime snapshot tools.
5. Remove dead one-off scripts after reference checks.

## Scope guidance

This skill is for cron wrapper standardization, not for changing the business logic of a cron job unless that logic is required to fit the contract.
