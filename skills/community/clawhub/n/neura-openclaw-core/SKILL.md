---
name: neura-openclaw-core
description: Use when an OpenClaw-style or local autonomous computer-use agent needs a single Neura Relay preflight workflow for messages, file changes, browser submits, shell commands, package or publisher changes, workflow state, memory writes, or data exports before execution.
---

# Neura Relay Core For OpenClaw-Style Agents

Use this skill before a local autonomous agent takes a consequential action. The goal is one governed checkpoint:

```text
proposed action -> refs-only Action Card -> Relay Decision Receipt -> runtime-owned execution
```

This is a community example skill pack. It is not an official OpenClaw or ClawHub integration, approval, endorsement, or partnership.

## Current Package Truth

- Canonical npm package: `@neurarelay/openclaw-preflight-adapter@0.1.1`
- Canonical ClawHub community package: `@neurarelay/openclaw-preflight-adapter@0.1.4`
- Historical ClawHub community fallback: `@rpelevin/neura-relay-preflight-adapter@0.1.1`
- ClawHub history thread: `openclaw/clawhub#2190`
- Execution owner: developer or local runtime, not Neura

Prefer the canonical npm package for JavaScript imports. Use the canonical ClawHub community package for OpenClaw installs when ClawHub audits and local policy allow it. The `@rpelevin` package remains a historical fallback only; neither package creates an official OpenClaw or ClawHub approval, listing, endorsement, integration, or partnership claim.

## Workflow

1. Classify the action family: message, file, browser, shell, package/publisher, workflow, memory, or data export.
2. Build a refs-only Action Card. Include action refs, target refs, authority refs, evidence refs, rule refs, risk category, and requested outcome.
3. Reject raw payloads. Do not include message bodies, file contents, form values, raw command strings, package credentials, customer data, secrets, tokens, passwords, or private payloads.
4. Route the card through Relay or the preflight adapter. Use dry-run mode when only shaping the card.
5. Interpret the Decision Receipt before execution:
   - `proceed`: execute only if authority is Registry-backed or the local policy explicitly accepts the receipt route.
   - `human_review`: stop and collect a named human review ref.
   - `revise`: update the Action Card with missing evidence, policy, target, or authority refs.
   - `stop` or `blocked`: do not execute; record the blocking reason and readiness path.
6. Preserve the trace, transaction ref, receipt id, and developer-owned next step.

## High-Risk Triggers

Always require a Decision Receipt before:

- sending external messages or public comments
- deleting, overwriting, or moving files
- submitting browser forms or changing account state
- running shell commands, package scripts, deploys, or release operations
- publishing packages, changing package metadata, or changing publisher namespace ownership
- writing persistent memory
- exporting customer, account, browser, or workspace data

For package and publisher actions, require source repo, source commit, package identity, owner/publisher ref, artifact digest or pack ref, and no-official-claim boundary refs.

## Output

Return:

- action family and one-sentence proposed action summary
- refs-only Action Card draft or adapter `preflightAction`
- missing authority, policy, evidence, artifact, or target refs
- Decision Receipt interpretation when a receipt is available
- next step for the developer-owned runtime
- reminder that no local execution should happen until the receipt path is accepted

Read `references/scenario-corpus.md` when the action is package/publisher related, involves customer data, or needs examples for receipt interpretation.
