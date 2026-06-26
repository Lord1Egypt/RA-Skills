# openclaw-cron-standard

A small OpenClaw skill for standardizing cron wrappers, cron prompt contracts, and delivery-mode expectations.

## What it does

This skill captures a hardened pattern for OpenClaw cron jobs that use:

- ClankerHive task claims
- wrapper scripts
- result JSON artifacts
- cron-delivered text responses

It helps prevent common cron breakage modes such as:

- stale result files being read after duplicate claims
- `already claimed` vs `already-claimed` string drift
- prompts reading result artifacts unconditionally
- silent `not-delivered` runs caused by wrapper/prompt contract mismatch
- silent notification failures caused by wrong `delivery.mode` for the job's actual delivery pattern

## Standard contract

### Wrapper rules

1. Remove stale result artifacts before each run.
2. Claim through one shared helper.
3. On duplicate claim, print `ALREADY_CLAIMED`, exit successfully, and do not write a result artifact.
4. Write result artifacts only for real execution or real failure.
5. Keep business logic separate from claim/result lifecycle helpers.

### Prompt rules

1. Run the wrapper first.
2. If it prints `ALREADY_CLAIMED`, reply with `NO_REPLY`.
3. Only then read the result JSON.
4. Use the result artifact as the source of truth only for real runs.
5. Make sure the cron `delivery.mode` matches the prompt's actual delivery contract.

### Delivery-mode rules

Use `delivery.mode: announce` when the cron returns user-visible text as its final reply.

Use `delivery.mode: none` when the cron is intentionally silent or sends alerts explicitly through the `message` tool.

If you bulk-flip reply-delivery jobs to `none`, they can still run and finalize successfully while never actually notifying the user.

## Why publish this as a skill

Cron systems tend to become fragile through small contract drift across scripts, prompts, and delivery settings. This skill packages the safe pattern so it can be applied consistently instead of rediscovered in production.

## Safety / scanner friendliness

This repository is intentionally plain and transparent:

- text files only
- no binaries
- no obfuscated payloads
- no encoded blobs
- no bundled installers
- no auto-update behavior

That makes it friendlier for human review and reputation scanning.

## Files

- `SKILL.md` - the actual OpenClaw skill definition

## Publish

Use the ClawHub CLI to publish the skill folder.

## License

MIT
