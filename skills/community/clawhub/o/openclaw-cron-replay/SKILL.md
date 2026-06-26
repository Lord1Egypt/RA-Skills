---
name: openclaw-cron-replay
description: Replay OpenClaw cron job formatting and delivery decisions locally using a trusted local openclaw-cron-replay installation. Use when debugging why a cron run produced or suppressed a message, comparing prompt/result changes, or inspecting likely final delivery text. Repository: https://github.com/pfrederiksen/openclaw-cron-replay
---

# OpenClaw Cron Replay

Use this skill to replay an OpenClaw cron job locally from saved config, prompt, payload, result, and metadata files.

This skill is for local debugging and reporting. It does not perform real delivery.

## Repository

Primary source repo:
- https://github.com/pfrederiksen/openclaw-cron-replay

## Prerequisites

Required:
- a trusted local installation of `openclaw-cron-replay`
- local cron config or saved artifacts you want to inspect

Before running:
- verify the local binary or source install is one you trust
- inspect local source if you did not build or install it yourself
- avoid elevated/root execution unless you actually need it
- confirm saved result/config files do not contain secrets you are unwilling to inspect locally

## When to use

Use this when the user asks to:
- replay a cron job locally
- see what message a cron run would have produced
- understand why a cron run suppressed output
- compare before/after prompt behavior
- inspect likely final delivery text from saved artifacts

## Safe source guidance

Prefer one of these:
- a previously installed trusted local binary on `PATH`
- a trusted local source checkout you have already inspected
- a pinned internal/local install workflow you control

Do not instruct users to install directly from a remote GitHub URL inside this skill.

## Recommended commands

Replay a job from local jobs JSON:

```bash
openclaw-cron-replay --job <job-id> --jobs /root/.openclaw/cron/jobs.json
```

Replay with a saved result file:

```bash
openclaw-cron-replay --job <job-id> --jobs /root/.openclaw/cron/jobs.json --result /path/to/result.json
```

Render markdown:

```bash
openclaw-cron-replay --job <job-id> --jobs /root/.openclaw/cron/jobs.json --markdown
```

Emit JSON:

```bash
openclaw-cron-replay --job <job-id> --jobs /root/.openclaw/cron/jobs.json --json
```

Compare two cron configs:

```bash
openclaw-cron-replay --compare before.json after.json
```

If the binary is not on `PATH`, use the trusted local path you already manage.

## Recommended interpretation

Use the replay output to answer:
- which prompt/payload the job would use
- what user-visible text would likely be derived
- whether delivery would likely announce, suppress, or stay silent
- whether `NO_REPLY` conflicts with generated content
- whether a prompt/result/config change explains the observed cron behavior

## Packaging / safety

Keep this skill minimal and transparent:
- plain text only
- no binaries bundled in the skill
- no obfuscation
- no remote install commands in SKILL.md
- prefer already-installed local/auditable tooling
