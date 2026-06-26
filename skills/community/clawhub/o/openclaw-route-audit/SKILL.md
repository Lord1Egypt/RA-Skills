---
name: openclaw-route-audit
description: Use static route analysis plus runtime cron delivery audit to validate OpenClaw cron notification wiring. Use when auditing cron jobs, announce routing, silent notification failures, sessionKey/target mismatches, ambiguous channel:last usage, or when preparing a ClawHub/GitHub-publishable skill around openclaw-route-check. Repository: https://github.com/pfrederiksen/openclaw-route-check
---

# OpenClaw Route Audit

Use this skill when you need to verify that OpenClaw cron jobs are both:
- statically routed correctly
- behaving correctly at runtime

This skill is for auditing and reporting. It does not send test messages.

## Repository

Primary tool repo:
- https://github.com/pfrederiksen/openclaw-route-check

Reference it explicitly when summarizing the static checker or preparing this skill for publishing.

## Prerequisites

Required local files:
- `/root/.openclaw/cron/jobs.json`
- `/root/.openclaw/workspace/tools/cron_delivery_audit.py`

Optional but recommended static checker installation:
- `openclaw-route-check` available on `PATH`
- or a trusted local install you have inspected yourself

Before running:
- verify the referenced local files exist
- inspect local scripts if you did not author them
- avoid elevated/root execution unless you actually need it
- confirm the cron config being read does not contain secrets you are unwilling to inspect locally

## When to use

Use this skill for requests like:
- "audit cron notifications"
- "why didn’t this cron notify me"
- "check announce routing"
- "find silent delivery bugs"
- "review sessionKey / channel / target mismatches"
- "prepare this for ClawHub or GitHub"

## Core workflow

1. Run the local runtime audit:
   - `python3 /root/.openclaw/workspace/tools/cron_delivery_audit.py`
2. Run the static route checker against the real cron config using a trusted `openclaw-route-check` installation.
3. Compare both outputs.
4. Prioritize real bugs in this order:
   - jobs with summary text but not delivered
   - jobs whose prompts say to return user-visible text for cron delivery but use `delivery.mode: none`
   - jobs with ambiguous routing (`channel:last`, implicit target, mismatched sessionKey vs target)
5. Patch the actual failing layer.

## Safe patching guidance

Prefer these fixes:
- set explicit `delivery.channel` and `delivery.to`
- change `delivery.mode` from `none` to `announce` when the prompt explicitly returns user-visible text for cron delivery
- keep `mode: none` for jobs that intentionally use the `message` tool or are explicitly silent-on-success

Do not claim a job is broken just because it is silent. Confirm whether the prompt intends silence.

## Publishing hygiene

If publishing to ClawHub or GitHub:
- keep the skill read-only by default
- avoid embedding secrets, tokens, webhook URLs, cookies, chat ids beyond public examples already present in the user’s config
- avoid curl-to-shell installers in the skill
- avoid auto-download or self-update behavior
- prefer pinned local paths and deterministic commands
- include the upstream repository link in SKILL.md
- list required local paths and prerequisites explicitly

## VirusTotal-friendly posture

To keep this easy to review and low-risk:
- no obfuscated code
- no packed binaries
- no outbound network writes in bundled scripts
- no persistence or daemon setup
- no privilege escalation
- no credential scraping

Bundled script should stay plain text, short, and readable.

## Bundled files

- `scripts/run_route_audit.sh`: runs both audits and prints combined JSON after prerequisite checks
- `references/publish-checklist.md`: lightweight publication checklist for ClawHub/GitHub
- `references/github-publish-notes.md`: GitHub repo positioning notes
