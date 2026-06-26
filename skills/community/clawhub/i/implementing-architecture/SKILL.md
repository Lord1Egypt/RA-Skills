---
name: implementing-architecture
description: "Use when: about to write code and docs/architecture/ exists with STATUS: APPROVED in architecture.yaml. Not when: no approved architecture yet (use compiling-architecture first), or architecture.yaml lacks STATUS: APPROVED header."
tags: [architecture, implementation, verification, planning, governance]
version: 1.0.2
homepage: https://github.com/inetgas/arch-compiler
metadata: {"hermes":{"tags":["architecture-as-code-tools","deterministic-execution","architectural-decision-records","software-architecture-patterns","architecture-constraints-enforcement","nfr-enforcement","developer-tools"],"category":"devops","requires_toolsets":["terminal"]},"openclaw":{"homepage":"https://github.com/inetgas/arch-compiler"}}
---

# Architecture Pattern Implementer

## Overview

Translates approved architecture artifacts into working code. The architecture folder is the authoritative source for HOW to build — which services, which config, which constraints. It does NOT replace functional requirements, which tell you WHAT to build (business logic, features, API contracts). You need both.

---

## Repo Structure — Read This First

Treat the compiler repo as having this contract:

```text
arch-compiler/
├── README.md
├── AGENTS.md
├── README-AGENTS.md
├── tools/        <-- read-only for agents
├── schemas/      <-- read-only for agents
├── config/       <-- read-only for agents
├── scripts/      <-- read-only for agents
├── patterns/     <-- read-only for agents
└── skills/
    ├── using-arch-compiler/
    │   └── SKILL.md
    ├── compiling-architecture/
    │   └── SKILL.md
    └── implementing-architecture/
        └── SKILL.md
```

Before acting:

1. Read `AGENTS.md` for repo-wide agent rules and boundaries.
2. Read this `SKILL.md` for the task-specific workflow.
3. Treat `tools/`, `schemas/`, `config/`, and `patterns/` as read-only unless the human explicitly asks for compiler-maintenance work in this repo.
4. Use this skill only when `docs/architecture/` already exists and is approved. If architecture is missing or unapproved, switch to `skills/compiling-architecture/SKILL.md` instead of inventing architecture choices.

The important split is:
- `AGENTS.md` = global agent rules for this repo
- `skills/using-arch-compiler/SKILL.md` = workflow router
- `skills/compiling-architecture/SKILL.md` = how to compile and finalise architecture
- `skills/implementing-architecture/SKILL.md` = how to implement an already-approved architecture

---

## When to Use

- You have a `docs/architecture/` folder with approved artifacts
- You are about to write code and need to know which technology choices are authorised
- You have an existing prototype or codebase and need to refactor it to conform to an approved architecture

## When NOT to Use

- No `docs/architecture/` folder exists — a compiled and approved architecture must be produced first (see `skills/compiling-architecture/SKILL.md` if available)
- The `architecture.yaml` has no `STATUS: APPROVED` header — do not implement an unapproved architecture
- You have architecture artifacts but no functional requirements — ask the human for features, user stories, design doc, or API specs before writing application code. The architecture tells you which database to use; functional requirements tell you what to store in it.
- Planning or pre-flight reveals unresolved provider/runtime/auth-boundary/retention/message-path decisions that would materially change `constraints.*`, `constraints.saas-providers`, `patterns.*`, or accepted risk posture — that is architecture work, not implementation. Stop and return to `skills/compiling-architecture/SKILL.md`.
- Do not treat an existing prototype or codebase as architectural authority. Existing code that conflicts with the approved artifacts must be refactored to match, or raised as an architecture mismatch. Do not silently treat the prototype as the source of truth.
- Do not use this skill if making the existing prototype fit the system would require changing the approved architecture itself. That is architecture work and must return to `skills/compiling-architecture/SKILL.md`.
- If the human explicitly wants existing prototype choices to replace approved providers, boundaries, or selected patterns, treat that as architecture work immediately instead of starting implementation and discovering the stop condition later.

**Brownfield rule:** existing code is still implementation scope when the job is to bring it into compliance with an approved architecture. This skill applies to both greenfield implementation and brownfield refactoring. The stop condition is not "code already exists"; the stop condition is "the approved architecture itself must change."

Example:
> A prototype stores files on local disk and uses ad hoc session auth, but the approved architecture selects object storage and managed OAuth/OIDC. Refactoring the prototype to use the approved storage and auth stack is implementation work, so this skill applies.

---

## What the Artifacts Contain

| File | What to use it for |
|------|--------------------|
| `architecture.yaml` | All decisions explicit at top-level — constraints, NFR targets, pattern configs at `patterns.<id>.*`. No `assumptions` section; every field is intentional. |
| `selected-patterns.yaml` | The approved pattern list — every pattern here must be reflected in the implementation |
| `patterns/<id>.json` | Full pattern detail — read this before implementing each pattern |

Inside each `patterns/<id>.json`:
- `description` — what the pattern is
- `defaultConfig` — the specific services/values chosen; use these directly
- `configSchema` — descriptions and trade-off explanations for each config option; read this to understand why a value was chosen and what the alternatives mean
- `provides` — capabilities the implementation must exhibit
- `requires` — what must be in place before this pattern can work
- `tags` — useful for finding official documentation

> **`docs/architecture/` is read-only.** You may not edit any file in this folder — not `architecture.yaml`, not `selected-patterns.yaml`, not pattern JSONs. These files are compiler output. Their `STATUS: APPROVED` header reflects a human decision made against a specific compiler run. A hand-edited `architecture.yaml` is not an approved architecture — it is drift with an approval header on it.
>
> If you spot a discrepancy between files in `docs/architecture/` (e.g. `architecture.yaml` lists a pattern not in `selected-patterns.yaml`, or has wrong config for a variant): **stop. Do not fix it yourself.** Tell the human what is mismatched. Then: if you have the `compiling-architecture` skill, propose the input spec changes, get human confirmation, apply them, re-run the compiler, and present the output for re-approval. If you do not have that skill, ask the human to update the input spec and re-run the compiler themselves. Either way, human re-approval of the compiler output is required before you continue.
>
> The temptation to "just update the date and fix the field" is the exact failure mode this constraint prevents.

---

## Implementation Workflow

### Step 1 — Read the artifacts

Before writing any code:

1. Read `architecture.yaml` — every field is explicit; note `constraints` (cloud, language, platform), `nfr` targets, and `patterns.<id>.*` for pattern-specific config
2. Read `selected-patterns.yaml` — get the full list of pattern IDs
3. For each pattern ID, read `patterns/<id>.json` — `defaultConfig` gives approved values; `configSchema` explains the trade-offs

### Step 1.5 — Pre-flight check before writing any code

**You MUST perform this check yourself. Do not delegate it to a subagent.** Subagents optimise for "no blocking errors" and resolve flags creatively rather than raising them — which defeats the purpose. A subagent returning "Overall Status: GREEN" is not a substitute for your own verification.

Before the detailed pattern-by-pattern checks below, run the shared workflow preflight helper:

```bash
python3 ~/.codex/arch-compiler/tools/archcompiler_preflight.py --app-repo <app-repo> --mode implement
```

If it fails, stop and fix the reported issue before continuing.

After reading all pattern JSONs in Step 1, and **before writing a single line of code**, go through every pattern and verify:

1. **`requires` is satisfiable** — every capability listed in `requires` is either provided by another selected pattern or already exists in the environment. If a required capability (e.g. `metrics-collection`, `distributed-tracing`, `time-series-database`) has no provider anywhere in the architecture, flag it.

   **Before flagging a gap**, check `schemas/capability-vocabulary.yaml` if it exists in the project. Capabilities with `category: environment` are always satisfied by the deployment environment — skip them entirely, do not raise them as gaps. Examples: `internet-connectivity`, `git-repository`, `compute`, `persistent-storage`, `network-connectivity`, `cloud-infrastructure`, `storage`, `infrastructure`, `data-storage`, `system-architecture`.
2. **`provides` is deliverable** — you can concretely implement every capability listed in `provides` given the current constraints (cloud, language, platform). If delivering a capability would need infrastructure or tooling not present in the architecture, flag it.
3. **Pattern integrity** — if a pattern's `requires` lists a capability that the same pattern's own `supports_nfr`, `provides`, or description explicitly states it cannot deliver, that is a registry bug. Flag it as: "Pattern X requires capability Y but its own NFR section declares it cannot support Y — this looks like a pattern authoring bug."
4. **Runtime semantics are compatible with the selected patterns** — check whether the chosen runtime is stateless, ephemeral, edge-restricted, or otherwise hostile to process-local assumptions. If a pattern implementation would rely on durable in-process state, sticky sessions, local filesystem persistence, or long-lived memory, either bind it to a persistent store or flag it before planning proceeds.

Collect **all** flags across all patterns, then raise them together with the human before proceeding. Do not start implementing and discover blockers mid-way — a partial codebase with unresolved blockers is harder to reason about than a clean pre-implementation conversation.

**A flag means: raise to the human — not find a creative interpretation that allows you to proceed.** The following are NOT resolutions:
- "The platform has logs" is not `monitoring`
- "Deployment logs exist" is not `audit-logging`
- "We can do it manually" is not a provided capability
- "It's close enough" is not satisfiable

**Architecture-binding flags are a stop signal, not plan TODOs.** If pre-flight exposes unresolved choices such as:
- which provider actually satisfies a selected pattern
- where auth is enforced
- which transport implements async delivery semantics
- how retention/deletion is operationalised
- whether an external AI provider changes accepted risk posture

then stop and route back to the compiling skill. Do not keep planning around the ambiguity.

If you catch yourself reasoning that a thin platform feature satisfies a `requires: optional: false` entry, stop. That is a flag.

Example raise:
> "`ops-low-cost-observability` requires `metrics-collection`, `distributed-tracing`, and `time-series-database` — none of these are provided by any other selected pattern. `ops-slo-error-budgets` similarly requires SLO tracking infrastructure. Neither can be fully implemented as the architecture stands. Should I add them to `disallowed-patterns` and recompile, or do you want to add an observability stack first?"

Example integrity flag:
> "`pattern-x` requires `audit-logging` (optional: false) but its own `supports_nfr` declares `audit_logging` must equal `false` because the pattern has no built-in access tracking. This is a contradiction in the pattern registry — should I raise a fix, and how do you want to handle the missing audit trail?"

Example runtime-semantics flag:
> "`resilience-circuit-breaker` is selected, but the target runtime is stateless Lambda-style execution. A module-global circuit breaker will reset across invocations and does not provide durable breaker state. Should I back it with a persistent store, or should we re-evaluate whether this pattern belongs in the approved architecture?"

**Human gate — required even when no flags found.** After completing Steps 1.5, 1.6, and 1.7, present a summary to the human regardless of whether flags were raised:

> "Pre-flight complete. No blocking gaps found. Summary:
> - Requires/provides: all satisfied
> - NFR targets: [list each and whether the selected service meets it]
> - Functional requirements: [list each and the task that covers it]
> - Known limitations accepted: [list any thin implementations]
>
> Ready to proceed to the plan?"

Wait for explicit human confirmation before writing the plan. A clean pre-flight is not implicit approval to proceed.

### Step 1.6 — NFR feasibility check

After Step 1.5, verify that the **selected services** can actually satisfy each NFR target in `architecture.yaml`. The `requires`/`provides` check only confirms pattern compatibility — it does not confirm that real-world services meet real-world targets.

**Do not treat the table below as exhaustive.** After verifying the listed fields, iterate through every field under `nfr.*` in `architecture.yaml` and confirm there is a plan task that delivers it. Any `nfr.*` field with no corresponding task is a gap — flag it. Common examples not in the table: `data.retention_days` requires a cleanup mechanism (scheduled job, TTL policy, or soft-expiry at read time) — a schema comment is not an implementation.

For each NFR field, look up the selected service's actual capability:

| NFR field | What to verify against the actual service |
|-----------|------------------------------------------|
| `nfr.rpo_minutes` | What is the backup frequency of the selected `db-*` provider on the chosen plan? If it exceeds `rpo_minutes`, **flag it** — do not assume it will be fine. |
| `nfr.availability.target` | Does the selected hosting provider's SLA meet or exceed the target on the chosen plan tier? |
| `nfr.latency.p95Milliseconds` | Are function timeout budgets set within this value? Does the selected region minimise latency? |
| `nfr.data.compliance.*` | Does the selected provider offer the required compliance certifications on the chosen plan? |
| `nfr.data.retention_days` | Is there a scheduled cleanup job, TTL policy, or equivalent? A note in a comment is not a plan task. |

**A service limitation is a flag — not a creative interpretation.** Example:
> "`nfr.rpo_minutes: 60` but Neon free tier performs daily backups (1440 min). This NFR cannot be met on the current plan. Should we upgrade the plan, relax the RPO, or accept the gap explicitly?"

### Step 1.7 — Functional requirements cross-check

**Before consulting any heuristic list, locate and read the primary source of functional requirements** — this may be a design doc, user stories, feature specs, a requirements list, or any combination. Extract requirements verbatim from whatever source exists. Also extract anything the source explicitly marks as **out of scope** and record that list alongside requirements.

Only if no source of any kind exists should you fall back to the "common silent misses" heuristics below. A heuristic-based gap that the source material explicitly marks out of scope is not a gap — do not flag it.

For each requirement, confirm a specific plan task will deliver it. Any requirement with no assigned task is a gap — flag it before proceeding.

**Common silent misses** (fallback only — apply when no requirements source exists):
- Navigation/header UI linking between pages
- Sign-in / sign-out flow and unauthenticated landing state
- Error states and retry flows (e.g. retry button on failed jobs)
- Empty states (e.g. "no pets detected", "no history yet")
- Per-user data scoping (history visible only to owner)

**Functional coverage matrix** — every plan document must include this table:

| Functional requirement | Task that delivers it |
|------------------------|----------------------|
| [requirement from design doc] | Task N: [name] |

If any row has no task, stop and either add the task or flag the gap to the human.

**When the human says "accept the gap":** implement the pattern but add an explicit named comment at the point of implementation — not a silent acceptance. Example:
```
// NOTE: monitoring (requires: optional: false) is not provided by this architecture.
// Kill switches must be triggered manually — no automated alerting will signal when to use them.
```

**When the human says "add a note to the architecture":** you cannot — `docs/architecture/` is read-only for implementing agents. Ask the human to update `architecture.yaml` themselves, then confirm before proceeding.

### When generating a plan with an upfront planning tool (e.g. writing-plans)

**MUST-DO before finalising any plan:**

Every plan document must include a **Pattern Coverage Matrix** in addition to the functional coverage matrix:

| Selected pattern | Task that delivers it | Concrete artifact(s) |
|------------------|-----------------------|----------------------|
| `pattern-id` | Task N: [name] | `path/to/file`, infrastructure resource type/name, config file, migration, named test function, or other concrete artifact |

The artifact column must name something concrete: a source file, infrastructure resource type/name, configuration file, migration, named test function, runbook, or other durable implementation artifact. A pattern mapped only to an area such as "backend", "infra", or "observability" is not coverage. An environment variable reference, a client call that assumes an externally-created resource, or a comment that mentions a resource without defining it is also not coverage.

For EVERY selected pattern, immediately before writing that pattern's task in the plan:

1. Read `patterns/<id>.json` — specifically the `provides` array
2. List every `provides` capability explicitly inside that task's steps
3. Verify each capability has a named, testable step and at least one concrete artifact target — not just a table entry
4. Add or update the Pattern Coverage Matrix row for that pattern
5. Do NOT add a pattern to any "done" or summary table unless its task delivers ALL capabilities in `provides`

**This resolves the planning/coding tension:** "read pattern JSON immediately before writing its code" means immediately before writing that pattern's *task in the plan* — not deferred to implementation time. The plan is the first form of code.

**Red flags during plan writing:**
- Writing a "done" summary table before writing the tasks
- Mapping a pattern to an "area of code" without listing its `provides` capabilities
- Mapping a pattern to a task without naming any concrete artifact it will produce
- Any pattern whose only plan entry is a one-liner in a summary table
- Leaving the Pattern Coverage Matrix incomplete or with vague artifact targets
- Finishing the plan before checking every pattern's `provides` array

**A pattern in a summary table without a task that delivers ALL its `provides` capabilities is a silent skip.**

### After drafting the plan — Adversarial review

Once the plan is drafted and before presenting it to the human, dispatch a subagent with an adversarial mandate. This is the one exception to the "do not delegate verification to a subagent" rule in Step 1.5. The difference: the subagent here is forbidden from producing a pass/fail verdict and must assume the plan is incomplete. Its only output is a gap list.

**Why "forbidden from pass/fail" is the key mechanism:** A reviewer asked "does the plan cover X?" will find creative ways to confirm coverage. A reviewer told "find what's missing" and forbidden from positive statements cannot return green without lying — which forces genuine fault-finding instead of validation theatre.

**Subagent prompt — copy and fill in the bracketed paths:**

> You are an adversarial plan reviewer. Your job is to find gaps — not to validate. You are explicitly forbidden from producing a pass/fail verdict or any positive summary statement.
>
> Read:
> 1. Functional requirements source: `[path or inline content — design doc, user stories, feature specs, or any combination]`
> 2. `docs/architecture/architecture.yaml`
> 3. The drafted plan: `[path/to/plan.md]`
>
> For each area below, produce a numbered list of questions and concerns. If you find nothing to question in an area, look harder — do not leave an area blank.
>
> **Area 1 — Functional requirements:** For each requirement in the source, ask: "Where exactly in the plan is this implemented — which file, function, and test?" If the answer is not obvious from the plan text, flag it. Also extract any items the source explicitly marks out of scope — do not flag those.
>
> **Area 2 — NFR completeness:** For every field under `nfr.*` in `architecture.yaml`, ask: "Where in the plan is this enforced with code?" A comment, a note, or a documentation file is not an implementation. Pay attention to fields outside the common set: `data.retention_days`, `data.pii`, `consistency.*`, `durability.*`, `throughput.*`.
>
> **Area 3 — Pattern provides delivery:** For each selected pattern, read its `provides` array in `docs/architecture/patterns/<id>.json`. For each capability, ask: "Which specific step in which task delivers this?" If a pattern appears only in a summary table with no task that walks through its `provides` capabilities, flag it.
>
> **Area 3.5 — Concrete artifact coverage:** For each selected pattern, ask: "What concrete artifact will exist after implementation?" Acceptable answers include a code file, infrastructure resource type/name, migration, configuration file, named test function, or runbook. If the plan only names a subsystem or workstream and not an artifact, flag it. If the answer is only an environment variable reference, a client call that assumes an externally-created resource, or a comment, flag it as non-implementation.
>
> **Area 4 — Runtime and API compatibility:** For each pattern with runtime-specific `defaultConfig` values (`function_runtime`, `edge_functions`, `compute_type`), ask: "Do the packages and APIs chosen in the plan actually work in this runtime?" Name the specific API or package you are questioning.
>
> **Area 5 — Error and edge cases:** For each main user-facing flow in the requirements source, ask: "Where does the plan handle the failure scenario?" Look for: upload failures, external API timeouts, empty results, retry flows, unauthenticated access attempts. Additionally, for any state that persists across page reloads (poll results, uploaded image URLs, job status), ask: "Does the plan preserve or re-fetch this state from a durable source — or does it survive only in-memory or in a URL parameter that is unavailable after a reload?"
>
> Output ONLY this structure — no preamble, no verdict, no positive statements:
>
> ```
> ## Adversarial Review — Gaps and Questions
>
> ### Area 1: Functional requirements
> 1. [Requirement text]: [Specific question]. Not visible in plan because: [what's absent].
>
> ### Area 2: NFR completeness
> 1. nfr.[field]: [Specific question]. Not visible in plan because: [what's absent].
>
> ### Area 3: Pattern provides delivery
> 1. [pattern-id] provides [capability]: [Specific question].
>
> ### Area 3.5: Concrete artifact coverage
> 1. [pattern-id]: [Specific question about missing concrete artifact].
>
> ### Area 4: Runtime and API compatibility
> 1. [pattern-id] sets [config key]: [value]. Plan uses [package/API]. Question: [compatibility concern].
>
> ### Area 5: Error and edge cases
> 1. Flow [name], failure scenario [x]: [Specific question].
> ```
>
> If you find yourself writing a positive statement, delete it and find another gap instead.

**Resolving the gap list:**

For each item the reviewer raises, respond with exactly one of:

- **Covered — cite it:** "Covered at Task N, Step M, file `path/to/file.ts`." If you cannot cite a specific location, the item is a real gap.
- **Gap confirmed:** add the missing task or step to the plan before presenting to the human.

Do not dismiss items with vague reassurances ("handled by the framework", "implied by the pattern", "standard practice"). If it is not explicitly in the plan, it is a gap.

After resolving, note in the human-facing summary what the adversarial review found and what was added.

**Final Verification must be structured as numbered tasks, not prose.** After resolving adversarial-review gaps, write a `Final Verification` section in the plan as explicitly numbered tasks with exact commands and expected output. A prose appendix is not a task and will not be tracked by plan executors.

At minimum, `Final Verification` must include:
1. A smoke-test task that starts the service (or nearest equivalent), performs at least one real call, and verifies a valid response
2. A post-implementation adversarial-review task matching Step 5 below

**Rewrite vs patch:** If more than 3 gaps are confirmed, rewrite the full plan rather than patching individual tasks. Patching accumulates on top of the original blindspots — the same mental model that produced the gaps is now editing its own output. A full rewrite forces you to trace every task from scratch with the gap list in hand, which surfaces secondary issues invisible in a diff. (Example: fixing a retry flow reveals a polling cleanup bug that only shows up when reading the whole `JobPoller` spec in one pass — not when diffing the retry step in isolation.)

**Re-review trigger:** If the architecture is recompiled or re-approved after the plan was drafted, the plan is stale by default. Re-run the adversarial review against the new `docs/architecture/` before presenting or executing the plan. If the pattern set or top-level constraints changed materially, rewrite the plan instead of carrying the old one forward.

### Step 2 — Establish implementation order

**Primary: derive sequencing from `requires`/`provides`.** For each selected pattern, read its `requires` list and find which other selected patterns `provides` those capabilities — those providers must be implemented first. Build the full dependency order before writing any code. Do not skip this: the category table below is a manually authored approximation and can diverge from actual dependencies.

**Secondary: use this table only when the dependency graph leaves order ambiguous** (e.g. two patterns with no dependency on each other). It is a scaffold, not a substitute for the `requires`/`provides` check.

| Order | Categories | Examples |
|-------|-----------|---------|
| 1 | Foundation | `arch-*`, `platform-*`, `hosting-*`, `iac-*`, `onprem-*` |
| 2 | Secrets, Security, Identity | `secrets-*`, `sec-*`, `policy-*`, `idp-*`, `pki-*` |
| 3 | Compliance | `compliance-*` |
| 4 | Storage | `db-*`, `data-*` |
| 5 | Caching | `cache-*`, `caching-*`, `write-*` |
| 6 | Communication | `api-*`, `sync-*`, `async-*`, `queue-*` |
| 7 | Reliability | `resilience-*`, `consistency-*`, `distributed-*`, `exactly-*`, `saga-*` |
| 8 | Application/Feature patterns | `cqrs-*`, `event-*`, `crud-*`, `multi-*`, `tenancy-*`, `batch-*`, `genai-*` |
| 9 | Front-end | `ui-*` |
| 10 | Observability | `obs-*`, `ops-*`, `finops-*` |
| 11 | Delivery | `deploy-*`, `release-*`, `build-*`, `dev-*`, `test-*`, `gof-*` |
| 12 | Governance | `gov-*` |

If the table order conflicts with a `requires`/`provides` dependency, the dependency wins.

### Step 3 — Implement each pattern

**Do this for each pattern individually, immediately before writing its code — not as a bulk upfront exercise.** Reading `compiled-spec.yaml` or a prior subagent summary is not a substitute for reading the pattern JSON itself.

For each pattern:

1. **Read `patterns/<id>.json` now** — even if you read it earlier, re-read it immediately before writing this pattern's code
2. Read `defaultConfig` — use these values directly; they are the approved choices
3. Read `configSchema` descriptions — understand the trade-offs and wire config into environment variables or config files accordingly
4. **Check `defaultConfig` for runtime-specific values** (e.g. `function_runtime`, `edge_functions`, `compute_type`) and verify that the packages and APIs in your implementation are compatible with that runtime. `function_runtime: nodejs` means Edge-only APIs are unavailable — use Node.js equivalents. `edge_functions: true` means Node.js built-ins are unavailable — use Web APIs. Mismatches compile and deploy silently but fail at runtime.
5. Check whether the pattern relies on process-local state, sticky sessions, local filesystem persistence, or long-lived memory. If the selected runtime is stateless or ephemeral, do not implement a thin in-process approximation and call it done — either bind it to a durable backing service or flag the mismatch.
6. Check `requires` as a pre-implementation checklist — confirm each required capability is already in place before starting. If a required capability (e.g. a metrics backend, CI/CD integration, SLO tracking tool) does not exist anywhere in the current architecture, **stop — do not write code for this pattern.** Follow the unimplementable pattern workflow below.
7. After implementing, verify your implementation delivers **every** capability listed in `provides`. If any capability is undelivered, **stop — do not move to the next pattern.** Follow the unimplementable pattern workflow below.

**Do not deviate from `defaultConfig` values without human approval.** If a value is unachievable or breaks NFR targets and/or compliance requirements, surface it to the human — do not substitute silently. Ask human to review and recompile architecture if needed.

### Step 4 — Verify against NFR targets

After implementing each pattern, verify configuration correctness against `architecture.yaml`. Agents verify that config values are set appropriately for each target — live performance testing against actual workloads is a human-run step done outside this workflow.

| NFR field | What to verify (configuration, not live measurement) |
|-----------|------------------------------------------------------|
| `nfr.availability.target` | Replication factor, health check intervals, and failover config set to values compatible with the target |
| `nfr.latency.p95Milliseconds` / `p99Milliseconds` | Connection pool sizes, cache TTLs, and timeout budgets wired to values compatible with the target — flag to human for load testing before go-live |
| `nfr.rpo_minutes` / `nfr.rto_minutes` | Backup schedule interval ≤ RPO target; recovery procedure documented; failover config present |
| `nfr.data.compliance.*` | Required controls active: encryption at rest/in-transit enabled, audit log destination configured, data retention policies set |
| `nfr.security.auth` | Exactly the specified auth mechanism implemented — not a different one |

### Step 5 — Post-implementation verification

After all patterns are implemented, complete two verification tasks before declaring implementation done. Both must appear in the plan as explicit numbered tasks inside `Final Verification`.

#### 5a. Smoke test (mandatory)

Start the service and verify at least one real call succeeds end-to-end.

| Type | Owner | Scope |
|------|-------|-------|
| Configuration correctness | Implementing agent (Step 4) | Are the approved values wired correctly? |
| Integration smoke test | Implementing agent (Step 5a) | Does the service start and respond correctly to one real call? |
| Load/performance testing | Human, out-of-band | Does the system hold under traffic? |

Step 4 covers configuration correctness. Step 5a covers whether the implementation actually runs. The carve-out in Step 4 for human-run live testing applies to load/performance testing only — not to the smoke test.

If the smoke test hits a runtime environment blocker (for example SDK incompatibility, missing cloud access, expired credentials, or unavailable external infrastructure), make one reasonable workaround attempt. If it still fails, surface the blocker to the human and stop iterating around it. An environment blocker is not the same thing as an implementation bug.

#### 5b. Post-implementation adversarial review

Run an adversarial review of the actual implementation against `docs/architecture/` — not just the plan. The plan adversarial review asks "does the plan cover the architecture?" This review asks "does the implementation in the working tree or commit candidate deliver what the plan said?"

The reviewer must be forbidden from producing a pass/fail verdict or positive summary. Its only output is a gap list. Prefer a reviewer with no prior implementation context so it is less likely to rationalize gaps away.

Focus areas:
- Does each selected pattern's `provides` capability appear in actual code, infrastructure, config, or tests — not stubs, comments, or log lines?
- Are NFR targets wired in running code, not only in config or documentation files?
- Do any implementation details contradict the approved `defaultConfig` values?
- Are cross-task integration points correct?

Resolve findings the same way as the plan adversarial review: cite the exact file and line, or confirm the gap and fix it.

---

## When a Pattern Can't Be Implemented or Human Asks to Skip It

If a pattern is unachievable, over-engineered for the scope, or the human explicitly says to skip it — **do not skip it silently in code.**

**A partial implementation is a silent skip.** Writing a log line, a comment, or a stub that references a pattern's `defaultConfig` values without delivering the capabilities in `provides` is not implementation — it is a silent skip with extra steps. It is worse than a clean skip because it creates the illusion of compliance. Treat it identically: stop and follow the workflow below.

The approved `docs/architecture/` folder is the source of truth. A pattern listed there but not fully implemented creates drift between what was decided and what was built — defeating the purpose of having an approved architecture.

**The correct response in all cases:**

1. **Confirm with the human** that the pattern should be removed and that this requires a recompile:
   > "`ops-low-cost-observability` and `ops-slo-error-budgets` are in the approved architecture. To keep things simple I'd suggest removing them — that means recompiling and re-approving the spec. Should I proceed?"
2. **Do not recompile yourself** — the human or a compiler agent adds the pattern IDs to `disallowed-patterns` in the spec, recompiles, and re-approves the output (see `skills/compiling-architecture/SKILL.md` if available)
3. **Only implement once the updated architecture is re-approved** — the refreshed `docs/architecture/` is your new source of truth

---

## Binding Constraints

`architecture.yaml` constraints are not suggestions:

- `constraints.cloud` — use only services from this provider
- `constraints.language` — implement in this language only
- `constraints.platform` — shapes deployment target and code structure (e.g. `data-pipeline` means batch jobs, not an HTTP server)
- `constraints.features.*` — only features set to `true` are in scope; do not implement features that aren't enabled

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting to code without functional requirements | Stop — architecture tells you HOW, not WHAT. Get feature specs from the human first. |
| Assuming a pattern is irrelevant without checking the full picture | e.g. `hosting-static-frontend--netlify` looks irrelevant for a mobile app until you check `ui-cross-platform` defaultConfig — Flutter targets web too. Cross-check pattern `provides`/`requires` before dismissing any selected pattern. If you confirm it genuinely can't be implemented in the current context, raise it with the human — do not skip silently. |
| Writing token code to satisfy a pattern (log line, comment, stub) | This is a silent skip. If you cannot deliver every capability in `provides`, follow the unimplementable pattern workflow — stop, raise with human, add to `disallowed-patterns` if agreed. |
| Reading compiled-spec.yaml or a prior summary instead of the pattern JSON | `compiled-spec.yaml` has `defaultConfig` but not `provides` or `requires`. Read `patterns/<id>.json` directly, immediately before implementing each pattern. |
| Choosing a service not in `defaultConfig` | Check `configSchema` — if it's not in the enum, it wasn't approved |
| Implementing patterns in arbitrary order | Derive order from `requires`/`provides` dependencies first |
| Ignoring NFR targets | Check each NFR field and verify your implementation meets it |
| Implementing a feature not in `constraints.features` | Only implement features explicitly enabled |
| Modifying files in `docs/architecture/` | Read-only for implementing agents; changes require re-compilation and human re-approval |
| Treating provider binding as an implementation detail | AWS vs agnostic, Auth0 vs Cognito, SQS vs generic queue, or OpenAI vs self-hosted model all change the architecture contract. Route back to the compiling skill instead of coding through it. |
| Self-resolving a `requires` gap with a thin justification | "Platform has logs" ≠ `monitoring`. "Deployment records exist" ≠ `audit-logging`. If no selected pattern provides the capability, it is an unresolved gap — flag it to the human, do not decide it is fine. |
| Ignoring a pattern's internal contradiction between `requires` and `supports_nfr` | If a pattern requires a capability its own `supports_nfr` says it cannot support, that is a registry bug — raise it explicitly rather than quietly accepting both claims. |
| Delegating the pre-flight check to a subagent | Subagents return "green" by finding creative resolutions. You must do Step 1.5–1.7 yourself. A subagent's "no issues found" verdict is not pre-flight completion. |
| Skipping the human gate when pre-flight returns clean | No flags does not mean implicit approval. Present the summary and wait for explicit confirmation before writing the plan. |
| Not checking whether selected services actually meet NFR targets | Pattern `requires`/`provides` compatibility does not mean the chosen provider's plan tier meets `rpo_minutes`, `availability.target`, or compliance requirements. Verify against actual service specs. |
| Treating the Step 1.6 NFR table as exhaustive | The table covers common fields — iterate every `nfr.*` field in `architecture.yaml` and confirm each has a plan task. `data.retention_days` with no cleanup job is a gap even if the field isn't in the table. |
| Applying generic heuristics before reading the requirements source | Read the actual source (design doc, user stories, feature specs) first and extract requirements verbatim. The "common silent misses" list is a fallback for when no source exists — not a first check. Flag an item from the heuristic list only if the source does not explicitly mark it out of scope. |
| Dismissing adversarial reviewer items with vague reassurances | "Handled by the framework" or "implied by the pattern" are not resolutions. For every reviewer item, cite the exact task, step, and file — or confirm the gap and add a task. |
| Using the adversarial reviewer as a validator instead of a fault-finder | If you prompt the reviewer to confirm coverage rather than find gaps, it will return green. The reviewer's mandate is to assume incompleteness. Never ask it "does the plan cover X?" — only "what is missing?" |
| Treating the smoke test as load testing and therefore out of scope | A smoke test is mandatory before declaring the work done: start the service, make one real call, and verify a valid response. Load/performance testing remains human-owned. |
| Writing `Final Verification` as a prose appendix instead of numbered tasks | Prose is not tracked as work. `Final Verification` must be numbered tasks with exact commands and expected output, including smoke test and post-implementation adversarial review. |
| Iterating through multiple workarounds for a runtime environment blocker | Make one reasonable workaround attempt. If the blocker persists, raise it to the human instead of continuing to churn on environment issues. |
| Treating per-task reviews as a substitute for post-implementation adversarial review | Per-task review catches isolated issues. Post-implementation adversarial review catches cross-task integration mistakes and implementation-vs-architecture drift. Both are required. |
| Referencing a resource by name without defining it | An env var like `FIREHOSE_STREAM_NAME` and a `put_record()` call do not create a Firehose stream. Every required resource needs a real definition: cloud resource, Terraform block, provisioning script, config, or explicit externally-managed dependency noted in the plan. |
| Using a runtime-incompatible API because `defaultConfig` wasn't checked | `function_runtime: nodejs` and `edge_functions: false` mean Edge-only APIs (e.g. `globalThis.waitUntil`) are unavailable. Check `defaultConfig` runtime values before choosing packages and APIs — mismatches compile silently and fail at runtime. |
| Missing functional requirements with no plan task | Error/retry/empty states and other UX flows are functional requirements not derivable from pattern `provides`. Cross-check the requirements source explicitly — they will not appear in any pattern JSON. |
| Patching the plan after an adversarial review instead of rewriting | Patches layer on top of the original blindspots. When the confirmed gap count exceeds 3, rewrite from scratch — a full rewrite traces every task and surfaces secondary issues invisible when diffing individual steps. |
| Continuing with an old plan after architecture re-approval | Recompilation changes the contract. Re-run adversarial review against the new architecture, and rewrite the plan if constraints or pattern set changed materially. |
| Writing approved architecture.yaml with assumptions block still present | Finalisation requires promoting every field under `assumptions.*` to its top-level path and removing the block entirely. An approved file with `assumptions:` still in it is compiler output, not a finalised architecture — implementing agents cannot distinguish decided fields from defaulted ones. |
| Assuming page-reload survival without tracing state to a durable source | State held in `URL.createObjectURL`, a query param, or in-memory React state is lost on reload. For any state a user might reload into, trace it to a durable read (database, Blob URL, cookie) — not a locally-constructed value. |
