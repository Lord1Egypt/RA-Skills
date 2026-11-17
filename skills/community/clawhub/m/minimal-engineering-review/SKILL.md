---
name: "minimal-engineering-review"
description: "Review coding work for the smallest correct implementation, reuse, stdlib/native features, and dependency restraint."
license: "MIT-0"
---

# Minimal Engineering Review

Use when the user asks to simplify code, avoid overengineering, review a technical plan, choose whether to add a dependency, or before adding shared infrastructure to a project.

This skill is a local lightweight discipline. It must not install global hooks, change model prompts automatically, or override workspace rules.

## Principle

Prefer the smallest implementation that is correct, observable, and maintainable. Minimal means less owned behavior, not fewer safety checks.

## Review Ladder

Before writing or approving new code, stop at the first rung that works:

1. Does this need to exist now? If speculative, skip it or defer it.
2. Does the codebase already have the helper, pattern, script, cron, or state file? Reuse it.
3. Does the language standard library solve it? Prefer stdlib.
4. Does the platform or host tool already provide it? Prefer native behavior.
5. Does an already-installed dependency solve it cleanly? Reuse before adding another.
6. Can the change be a small local patch instead of a new abstraction?
7. Only then write the minimum code that works.

## Workflow

1. Read the touched code, config, or project status before judging.
2. Identify the actual owner and blast radius: which component, service, cron, or external channel is affected.
3. List concrete cuts or simplifications first: delete, reuse, stdlib, native, dependency avoided, abstraction avoided.
4. Preserve non-negotiables: validation at trust boundaries, security, data-loss handling, audit logs, idempotency, recovery after restarts, accessibility, and explicit user requirements.
5. For non-trivial logic, leave one runnable check: targeted test, dry run, self-check, or command output that would fail if the logic breaks.
6. Report the smallest useful change and any deferred fuller version.

## Output Style

For reviews, lead with findings:

- `<path or component>: <issue>. Replace with <simpler option>.`

For implementation summaries, keep it short:

- What changed.
- What was intentionally skipped.
- What verification passed.

## Good Uses

- Trading or automation scripts: prefer deterministic runners, journals, benchmarks, fees, drawdown, and risk gates before model-driven execution.
- Background scripts and crons: prefer idempotent small scripts, state files, and watchdogs over broad orchestrators.
- Dependency requests: check stdlib/native/existing packages first.
- Code review: find abstractions with one implementation, duplicate helpers, dead config, wrappers that only delegate, and custom code that the platform already ships.

## Boundaries

This is not a replacement for correctness, security, or factual review. If the task involves trading decisions, external messaging, auth, schedulers, public posting, or other services' scope, follow the stricter workspace rules first.

Do not apply this skill to prose, creative writing, factual research, or ordinary chat unless the user asks for simplification of a technical workflow.
