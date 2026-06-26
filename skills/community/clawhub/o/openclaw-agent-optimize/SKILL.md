---
name: openclaw-agent-optimize
slug: openclaw-agent-optimize
version: 1.2.1
license: MIT
description: |
  Use when: you want a structured audit -> options -> recommended plan to improve an OpenClaw workspace
  (cost, model routing, context discipline, delegation, reliability).
  Don't use when: you want immediate config/cron mutations without review, or the question is unrelated to OpenClaw ops.
  Output: a prioritized plan with exact change proposals, expected impact, and rollback steps. No persistent changes without explicit approval.
triggers:
  - optimize agent
  - optimizing agent
  - improve OpenClaw setup
  - agent best practices
  - OpenClaw optimization
metadata:
  openclaw:
    emoji: "🧰"
---

# OpenClaw Agent Optimization

Use this skill to tune an OpenClaw workspace for **cost-aware routing**, **parallel-first delegation**, and **lean context**.

## Default posture

This skill is **advisory first**.
It should produce:
- audit,
- options,
- recommended plan,
- exact patch proposal,
- rollback,
- verification plan.

No persistent mutations without explicit approval.

## Quick start

1) **Full audit (safe, no changes)**
> Audit my OpenClaw setup for cost, reliability, and context bloat. Output a prioritized plan with rollback notes. Do NOT apply changes.

2) **Context bloat / transcript noise**
> My OpenClaw context is bloating (slow replies / high cost / lots of transcript noise). Identify the top offenders (tools, crons, bootstrap files, skills) and propose the smallest reversible fixes first. Do NOT apply changes.

3) **Model routing / delegation posture**
> Propose a model routing plan for (a) coding/engineering, (b) short notifications/reminders, (c) reasoning-heavy research/writing. Include an exact config patch + rollback plan, but do NOT apply changes.

## What good output looks like

- **Executive summary**
- **Top drivers**
  - cost
  - context
  - reliability
  - operator friction
- **Options A/B/C** with tradeoffs
- **Recommended plan** (smallest safe change first)
- **Exact proposals** + **rollback** + **verify**

## Safety contract

- Do not mutate persistent settings without explicit approval.
- Do not create/update/remove cron jobs without explicit approval.
- If an optimization reduces monitoring coverage, present options and require choice.
- Before any approved change, show:
  1. exact change,
  2. expected impact,
  3. rollback plan,
  4. post-change verification.

## High-ROI optimization levers

### 1) Output discipline for automation
Make maintenance loops truly silent on success.

### 2) Separate work from notification
If you want alerts but want interactive context lean:
- do the work quietly
- notify out-of-band with a short human receipt

### 3) Bootstrap discipline
Keep always-injected files short and load-bearing only.
Move long runbooks into `references/` or adjacent notes.

### 4) Ambient specialist surface reduction
A common hidden tax is **too many always-visible specialist skills**.
If a workflow is low-frequency or specialist:
- prefer on-demand worker/subagent usage,
- do not keep it permanently ambient in main-chat prompt surface.

### 5) Measure optimizations authoritatively
Prefer fresh-session `/context json` or equivalent receipts over “feels better”.
High-signal fields include:
- `eligible skills`
- `skills.promptChars`
- `projectContextChars`
- `systemPrompt.chars`
- `promptTokens`

### 6) Verification-first ops hygiene
After any approved optimization, verify:
- core chat still works
- recall/behavior did not degrade
- new session actually picks up the change
- rollback path is proven, not theoretical

## Workflow (concise)

1. Audit rules + memory: keep restart-critical facts only.
2. Audit skill surface: trim ambient specialists before touching tool surface.
3. Audit transcripts/noise: silence cron and heartbeat success paths.
4. Audit model routing and delegation posture.
5. Recommend the smallest viable change first.
6. Verify on a **new session** when skill/bootstrap snapshotting exists.

## Notes

- Some runtimes snapshot skills/config per session. If you install/update skills and do not see changes, start a new session.
- Prefer short `SKILL.md` + `references/` for long runbooks.
- If context bloat is the main complaint, pair this skill with `context-clean-up` (audit-only).

## References

- `references/optimization-playbook.md`
- `references/model-selection.md`
- `references/context-management.md`
- `references/agent-orchestration.md`
- `references/cron-optimization.md`
- `references/heartbeat-optimization.md`
- `references/memory-patterns.md`
- `references/continuous-learning.md`
- `references/safeguards.md`
