---
name: memory-governor
slug: memory-governor
version: 0.3.2
homepage: https://github.com/SakenW/memory-governor
description: "Memory governance kernel for AI agents that complements the OpenClaw 2026.6.x memory stack (Dreaming, Active Memory, Memory Wiki, People Wiki, Skill Workshop / Workboard) with explicit correction staging, target-class routing, compiled-surface boundaries, scope/privacy rules, and safer manual hardening rules."
changelog: "Aligns with OpenClaw 2026.6.x; declares all official compiled surfaces (People Wiki, Memory Wiki claims, Memory Palace, Imported Insights, Provenance) downstream of the contract. Adds references/compiled-surfaces.md plus scope/privacy, multi-agent writer, and Skill Workshop versioning rules. 9 target classes unchanged."
metadata: {"clawdbot":{"emoji":"🧭","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["./memory-governor-host.toml"],"configPaths.optional":["./MEMORY.md","./AGENTS.md","./TOOLS.md","./SOUL.md","./memory/"]}}
---

# Memory Governor

Reusable memory-governance core for different host environments.

The OpenClaw integration in this repository is only a reference host profile, not the only host model.

It is not a second-brain system, sync bus, or knowledge manager. It governs what should be remembered, where it should go, when it should be promoted, and what should be excluded.

It is a governance kernel, not an execution-first productivity skill. Its value is highest when a host already has multiple memory layers, multiple memory-writing skills, or adapter drift.

## When to Use

Use this skill when:

- you need to decide whether something should enter memory
- you need to choose the right memory layer or target class
- you need to promote daily, correction, or working state into durable rules
- multiple skills are starting to define memory differently and need governance

## First Reading Path

If this is your first time opening `memory-governor`, start here:

1. `SKILL.md`
2. `references/memory-routing.md`
3. `references/promotion-rules.md`
4. `references/exclusions.md`
5. `references/adapters.md`
6. `references/compiled-surfaces.md`

The remaining reference files are optional on first read.

## What Counts as Memory

Only information that improves future judgment, recovery, execution quality, or coordination consistency counts as memory.

Typical examples:

- stable long-term preferences
- stable long-term facts
- key same-day events
- explicit corrections
- unproven but promising candidate lessons
- reusable lessons
- current progress state
- short-term recovery hints

For content that should stay out of memory, see [references/exclusions.md](references/exclusions.md).

## Core Rule

The thing being standardized is the **memory contract**, not every skill implementation.

That means:

- all skills should follow the same classification, routing, promotion, and exclusion rules
- each skill may keep its own internal logic, downstream tools, interaction style, and directory habits

In short:

**standardize the core, not everything else**

## Target Classes

The kernel defines abstract target classes before it defines any optional skill path.

Recommended standard target classes:

- `long_term_memory`
- `daily_memory`
- `learning_candidates`
- `reusable_lessons`
- `proactive_state`
- `working_buffer`
- `project_facts`
- `system_rules`
- `tool_rules`

Concrete file paths are adapter details, not the contract itself.

Notes:

- `learning_candidates` is a low-commitment staging layer for corrections and emerging lessons
- it exists to prevent single observations from hardening too early
- `proactive_state` and `working_buffer` are stateful targets
- they should not become infinite append-only logs
- they need freshness, replace or merge, and retention rules by default

## Routing Order

When evaluating a candidate memory, reason in this order:

1. Is it worth remembering at all?
2. What memory type is it?
3. Which target class does that type belong to?
4. Which adapter in the current host should store that target class?
5. Is it still short-term, or is it ready for promotion?
6. Does it match any exclusion rule?

See [references/memory-routing.md](references/memory-routing.md) for the routing table.

See [references/routing-precedence.md](references/routing-precedence.md) for ambiguity resolution.

## Promotion Rules

All promotion should extract and refine before it hardens.

Never:

- write raw logs directly into long-term memory
- treat a working buffer as long-term memory
- use system-governance files as temporary capture inboxes

See [references/promotion-rules.md](references/promotion-rules.md) for details.

See [references/correction-pipeline.md](references/correction-pipeline.md) for the correction-to-candidate-to-rule flow.

See [references/candidate-review.md](references/candidate-review.md) for keep/promote/discard review workflow.

See [references/dreaming-integration.md](references/dreaming-integration.md) for how this kernel should coexist with OpenClaw Dreaming without duplicate promotion paths.

See [references/stateful-targets.md](references/stateful-targets.md) for update semantics on stateful targets.

See [references/schema-conventions.md](references/schema-conventions.md) if the host wants stronger structured constraints.

See [references/retention-rules.md](references/retention-rules.md) for lifecycle rules.

See [references/read-order.md](references/read-order.md) for recovery-time read order.

## Compiled Surfaces

OpenClaw keeps adding runtime and compiled memory surfaces: Dreaming artifacts, Active Memory, Memory Wiki, People Wiki, Claim/Evidence, Memory Palace, Imported Insights, and Provenance Views.

None of them is a memory target class. They are downstream of the governance contract.

In short:

- capture into target classes first
- let official engines compile, recall, navigate, and index downstream
- canonical durable truth still lives in the target classes

Two governance rules that the contract adds on top:

- imported content (for example Imported Insights) is unverified and should stage through `learning_candidates`, not jump to canonical truth
- scoped memories (project, chat, agent) should record scope at capture time, so a compiled surface cannot widen them beyond what Active Memory Filters allow

See [references/compiled-surfaces.md](references/compiled-surfaces.md) for the full surface inventory and the capture-vs-compile rule.

See [references/dreaming-integration.md](references/dreaming-integration.md) for the Dreaming-specific boundary.

## Skill Integration

When another skill integrates with this kernel:

- the skill may declare which information types it emits
- the skill may declare where those types usually land
- the skill should not invent a new global memory-layer definition
- the skill should not bypass exclusion rules
- the skill should not confuse downstream storage rules with upstream memory rules

See [references/skill-integration.md](references/skill-integration.md).

## Adapters

`memory-governor` may provide default adapters, but those adapters are not the only truth.

Examples:

- `long_term_memory` -> `MEMORY.md`
- `daily_memory` -> `memory/YYYY-MM-DD.md`
- `reusable_lessons` -> `~/self-improving/...` if `self-improving` is installed
- `reusable_lessons` -> a local fallback file if `self-improving` is absent

See [references/adapters.md](references/adapters.md) for default adapter behavior.

See [references/integration-checklist.md](references/integration-checklist.md) for integration checks.

See [references/installation-integration.md](references/installation-integration.md) for installation and host integration guidance.

See [references/host-profiles.md](references/host-profiles.md) for host differences.

## Never Do

- do not turn this skill into a monolithic personal memory system
- do not embed Obsidian, Notion, or OmniFocus implementation details into the governance kernel
- do not force every skill into the same implementation style
- do not invent a new primary memory directory unless the governance layer explicitly approves it
- do not write secrets, raw long logs, or short-lived noise into memory
- do not model Dreaming, Memory Wiki, People Wiki, Memory Palace, or Imported Insights as target classes
- do not let skills write entity profiles directly into a `people/` surface instead of capturing into target classes
- do not treat imported or cross-platform content as already-verified long-term memory
- do not let a compiled surface widen the scope of a captured memory beyond its intended boundary

## Phase Boundary

The current phase is governance core only.

That means:

- it may define contracts
- it may define references
- it may constrain how other skills write memory
- it may not quietly grow into a unified execution bus at this stage

If the project later wants an orchestration layer or a full personal memory system, that should be scoped separately after the governance layer is stable.
