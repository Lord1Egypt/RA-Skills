# Compiled Surfaces

## Goal

Give one canonical place that lists every official OpenClaw runtime / compiled memory artifact and declares that **none of them is a memory target class**.

This file exists because OpenClaw keeps adding memory-related surfaces (Dreaming, Active Memory, Memory Wiki, People Wiki, Memory Palace, Imported Insights, and more). Each of them is useful, but none of them replaces the governance contract.

If this list is not explicit, skills slowly start writing directly to those surfaces, and the contract drifts.

## Core Rule

OpenClaw runtime and compiled artifacts are **downstream** of the memory contract.

They may read from target classes. They may compile, recall, navigate, and index. They do **not** become target classes themselves.

In short:

- capture into target classes first
- let official engines compile / recall / navigate downstream
- canonical durable truth still lives in the target classes defined by this kernel

## Target Classes vs Compiled Surfaces

Target classes (owned by `memory-governor`) are where information is **captured and hardened**:

- `long_term_memory`
- `daily_memory`
- `learning_candidates`
- `reusable_lessons`
- `proactive_state`
- `working_buffer`
- `project_facts`
- `system_rules`
- `tool_rules`

Compiled surfaces (owned by OpenClaw or host plugins) are **derived views** built from those targets. They are not capture layers and not governance primitives.

## Official Compiled / Runtime Surfaces

Treat every item below as a downstream surface, not a target class.

### Background consolidation artifacts

- `DREAMS.md`
- `memory/.dreams/`

These are Dreaming engine artifacts. See [dreaming-integration.md](dreaming-integration.md).

### Runtime recall layer

- Active Memory (pre-reply recall, indexing, boosting)

Active Memory performs runtime recall. It is not a place you write to. See [read-order.md](read-order.md).

### Compiled knowledge surfaces

- Memory Wiki (`WIKI.md`, vault pages, digests)
- Claim / Evidence artifacts (structured assertions with sources, freshness, contradictions)
- Contradiction reports
- Staleness / freshness dashboards
- Obsidian Vault outputs (`~/obsidian-vaults/...`, `00_Index/`, `03_Memories/`, `04_Claims/`, etc.)

These compile existing memory into navigable, machine-readable, or human-readable views. They are not canonical durable memory.

### Entity-compiled surfaces

- People Wiki
- Person Cards
- Relationship Graphs
- Canonical alias maps

These compile entity facts that were already captured into target classes. They do **not** introduce an `entity_memory` or `people` target class.

Entity facts are captured upstream:

- stable facts about a person -> `long_term_memory`
- project-scoped relationships -> `project_facts`
- unverified inferences about a person -> `learning_candidates`

Do not write skills that emit directly into a `people/` directory or a Person Card. Write into target classes and let the wiki compile.

### UI / navigation surfaces

- Memory Palace
- Imported Insights tabs
- Dashboard / Home pages

These are presentation layers. They are not memory layers.

### Provenance surfaces

- Provenance Views
- Source drilldowns
- Evidence-kind reports

Provenance is a property of compiled claims, not a target class. A provenance trail is useful for trust and audit, but it does not promote a candidate into a rule.

## Privacy and Scope Boundary

Newer OpenClaw builds add recall-time access control, for example Active Memory Filters such as `allowedChatIds` / `deniedChatIds`.

Governance implication:

- some target classes may carry a `scope` or `privacy` attribute at capture time
- compiled surfaces must respect that scope when they compile, navigate, or expose
- a project-scoped fact compiled into a global People Wiki page is a leak, even if the source target class was correct

Practical rule:

- when a memory is scoped (project, chat, agent), record the scope on the target class entry
- never let a compiled surface widen the scope of a captured memory
- imported or cross-chat memories are the highest-risk category for scope leaks

## Imports Are Not Promotion

OpenClaw can import external memory (for example ChatGPT conversation history surfaced as Imported Insights).

Governance rule:

- imported content is **unverified** by this host
- it should be treated like `learning_candidates`, not like canonical truth
- it must not jump straight into `long_term_memory`, `reusable_lessons`, or system-level rules
- compilation surfaces may index it, but promotion still requires the manual review path

See [exclusions.md](exclusions.md) and [correction-pipeline.md](correction-pipeline.md).

## Official Behavior That Reinforces This Contract

These official behaviors validate the boundary this kernel already draws:

- stale REM recall previews are filtered, so `DREAMS.md` is not treated as canonical truth
- partial recall on timeout returns compact state, which rewards keeping `working_buffer` short and high-signal
- local models skip guardian review, which does not change what counts as memory
- Memory Wiki state moved to SQLite, so host checkers should not assume wiki output is a plain file tree

## What A Compiled Surface May Do

- read target classes
- compile, summarize, navigate, index
- surface contradictions and staleness as review signals
- provide provenance trails for trust

## What A Compiled Surface May Not Do

- define a new target class
- replace `learning_candidates` or `reusable_lessons`
- auto-promote a candidate into a system rule
- widen the scope or privacy boundary of a captured memory
- become the default startup read layer

## Anti-Patterns

- modeling `DREAMS.md`, `WIKI.md`, People Wiki, or Memory Palace as a target class
- letting skills write Person Cards or `people/` pages directly instead of capturing into target classes
- treating Imported Insights as already-verified long-term memory
- trusting a wiki Claim as a promotion decision without manual review
- reading compiled surfaces during normal startup instead of the minimal target-class read order
- letting a compiled surface expose a project-scoped or chat-scoped memory outside its scope

## Related

- [dreaming-integration.md](dreaming-integration.md)
- [read-order.md](read-order.md)
- [exclusions.md](exclusions.md)
- [correction-pipeline.md](correction-pipeline.md)
- [adapters.md](adapters.md)
