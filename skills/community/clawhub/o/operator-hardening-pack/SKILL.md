---
name: operator-hardening-pack
description: A unified operating workflow for hardening agent setups and running complex tasks reliably by combining bootstrap hardening, role orchestration, and handoff discipline.
---

# Operator Hardening Pack

Use this skill as the top-level entry point when you need a reliable, safety-first agent operating system.

## Includes

- **agent-bootstrap-hardening**: tighten AGENTS/SOUL/USER/HEARTBEAT/memory structure
- **team-agents-orchestrator**: role-separated execution (operator/researcher/builder/editor)
- **team-role-launchkit**: reusable role prompts + handoff contract templates

## When to use

- New workspace setup
- Existing workspace feels inconsistent/noisy
- Complex multi-step tasks with quality drift
- Need repeatable role handoffs across long tasks

## Workflow (recommended)

1. **Harden foundation**
   - Run bootstrap hardening on core files.
2. **Enable role mode for complex work**
   - Activate orchestrator with explicit role boundaries.
3. **Enforce handoff contract**
   - Use template from `references/pack-runbook.md`.
4. **Deliver + log**
   - Final output + decisions/follow-ups in memory.

## Guardrails

- External/public actions require explicit approval policy.
- Keep instructions concise and enforceable.
- Promote only durable, useful memory.
- Prefer no-change over low-value churn.

## Output contract

Return:
- hardening/operation summary
- files/artifacts changed
- unresolved risks
- next best step
