---
name: governed-delegation
description: Policy-guided governed delegation for subagent use. Use when deciding whether to delegate, which model tier is allowed, whether execution must fail closed, or when building an auditable spawn request for critical or deterministic work.
---

# Governed Delegation


> Canonical model-routing source: `docs/MODEL_ROUTING_POLICY.md`
>
> If this file conflicts with routing doctrine, the canonical policy doc wins.

Use this skill when a task may require subagents or governed delegation.

This is the **canonical front door** for delegation-envelope policy in configuration/governance work.
Use it to answer one narrow question well:

> If delegation is needed, what execution envelope is allowed?

Do **not** use this skill as a substitute for:
- live runtime inspection
- persisted config inspection
- config mutation/apply workflows

## Goal

Keep the split clean:
- **GPT** decides whether delegation is needed, how to decompose the work, and whether deterministic execution is better
- **governed delegation** decides the allowed execution envelope
- **OpenClaw runtime** performs the actual spawn/execution through supported surfaces

Do **not** patch OpenClaw core for this.
Do **not** depend on dist internals.
Prefer add-on boundaries.

## Default rule

Before delegating, classify the task on four axes:
- `taskClass`: `A|B|C|D`
- `deterministic`: `true|false`
- `criticalWrite`: `true|false`
- `requiresDeepReasoning`: `true|false`

Then use the helper:
- `node skills/governed-delegation/scripts/request.js '{...json...}'`

For Class C/D or other fail-closed work, include `frontDoor` explicitly (for example `orchestrator:orchestrators/reflect/orchestrator.md`). The helper now rejects strict requests when the requested front door does not match canonical policy.

## Policy intent

- **GPT** for ambiguity, policy interpretation, arbitration, deep synthesis, and critical governance review
- **CODEX** for bounded implementation, deterministic transforms, verification, backup/apply/validate routines
- **MINIMAX** only for bounded low-risk read-only work
- **fail closed** for Class C/D and other unsafe downgrade cases

## When to use

Use this skill when:
- an orchestrator needs subagents
- a cron/delegated task needs model-tier guardrails
- a task mixes planning and implementation and you need a safe split
- a critical write or durable memory/governance task must not silently degrade to a weak model

Use it **after** deciding that delegation is actually on the table.
For ordinary questions like "what is live right now?", "what does the saved config say?", or "apply this config change safely", start with the appropriate inspection/mutation surface instead.

## Output contract

The helper should produce a decision containing:
- chosen model
- failClosed true/false
- policy source
- runner type
- optional auditable spawn request envelope

## Minimal workflow

1. Decide if delegation is actually needed
2. Classify task risk/type
3. Ask governed-delegation helper for decision
4. If safe, pass the resulting request to the supported runtime/tool surface
5. If not safe, refuse or escalate instead of degrading

## Canonical config/governance split

- **live runtime state** → inspect runtime/session/gateway state directly
- **saved config state** → inspect persisted config/schema directly
- **safe mutation** → use supported config patch/apply/restart flows
- **delegation policy** → use this skill

If plain GPT or a direct deterministic runner is enough, do **not** add delegation. This skill reduces unsafe delegation — it is not a reason to turn everything into a subagent workflow.
