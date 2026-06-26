---
name: hive-builder
description: Design, scaffold, and carefully activate a Hive-style one-person company inside OpenClaw using an orchestrator pattern. Use when planning or building a multi-agent Hive system with a CEO main session plus specialist subagents, especially when distinguishing fresh-workspace setup from existing-workspace adoption.
---

# Hive Builder

Build Hive as a **controlled architecture project**, not as an automatic workspace takeover.

Treat `hive-builder` as the **complete mother skill** for Hive and the main public product entry point: the user should be able to download this skill and understand how to build the full virtual organization, including CEO, HRM, OPS, and specialist roles such as Collector, Writer, and QA.

Hive uses a **layered orchestrator pattern** built on modern OpenClaw-native primitives:
- **Builder layer** = `hive-builder` for architecture, scaffolding, and activation boundaries
- **Runtime control layer** = `hive-ceo` for task entry, routing, approval, and final synthesis
- **Governance layers** = `hive-hrm` and `hive-ops`
- **Business-role layers** = specialists such as Collector, Writer, and QA
- **Main session** as the user-facing commander/CEO interface
- **`sessions_spawn`** as the preferred execution primitive for bounded specialist work once Hive moves beyond pure contained/manual validation
- **Task Flow / detached work** as the future substrate for durable multi-step Hive chains
- Shared filesystem for artifacts
- Externalized state for tasks and audit trails

## Product Position

For end users, `hive-builder` is the single complete entry point for Hive.
It should evolve with the latest stable OpenClaw runtime primitives instead of preserving unnecessary custom Hive machinery once the platform supports the behavior natively.

That means this skill should:
- explain the full Hive role system
- cover how CEO, HRM, OPS, and specialist roles fit together
- support building the complete virtual organization from one mother skill
- remain usable even if some internal role logic is later modularized into separate `hive-*` skills

The modular `hive-*` skills are implementation helpers and evolution paths, not prerequisites for understanding Hive at the product level.

## Core Rule

Installing this skill is **not** the same as enabling Hive.

Treat Hive setup as four separate phases:
1. **Assess** the environment
2. **Plan** the Hive structure
3. **Scaffold** directories and role templates
4. **Activate** only after explicit confirmation

Do not skip directly from installation to full deployment.

## Operating Modes

### Mode A — Fresh Workspace

Use when the workspace is effectively new and the user wants Hive to become a primary operating structure.

Typical signs:
- Few or no existing workflow files
- No established multi-skill stack yet
- User explicitly wants to build Hive from scratch

Allowed actions in this mode:
- Create full Hive directory structure
- Initialize core roles
- Generate `SETUP.md`
- Create role templates and starter specialist folders
- Prepare document/archive directories

### Mode B — Existing Workspace

Use when the workspace already has established files, behaviors, memory, or active skills.

Typical signs:
- Existing `AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, or mature skill stack
- Existing workflows already operating
- User wants Hive added without disrupting the current system

Default behavior in this mode:
- Plan first
- Scaffold second
- Activate later
- Keep Hive as a parallel subsystem until the user explicitly chooses deeper adoption

In existing-workspace mode, do **not** default to rewriting core workspace files or changing how the main session behaves.

## First Step: Assess Before Building

Before generating anything, determine:

1. Is this a **fresh** or **existing** workspace?
2. Does the user want:
   - a concept/design only,
   - a filesystem scaffold,
   - or a live Hive activation?
3. What should Hive own versus what should remain under the current workspace system?

If the user has not clearly asked for live activation, default to:
- design + scaffold
- not full activation

## Safe Adoption Rules

Especially in existing-workspace mode:

- Do **not** overwrite `AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, or `HEARTBEAT.md`
- Do **not** silently convert the main session into a Hive CEO runtime just because the architecture was scaffolded
- Do **not** spawn a full specialist network just because Hive was requested conceptually
- Do **not** claim Hive is active unless the scaffold exists and activation was explicitly chosen

Hive should begin as a **contained subsystem** under `{WORKSPACE}/hive/`.

## Architecture

```text
User request
    ↓
Commander / CEO (main session)
    ├── classify task
    ├── keep in main session when Hive adds no real value
    ├── run contained/manual validation when testing a chain
    └── dispatch bounded specialist work when appropriate
         via sessions_spawn
              ↓
         isolated specialist runs / governance roles
              ↓
         artifacts → {WORKSPACE}/hive/artifacts/
         task state → {WORKSPACE}/hive/state/tasks/
         checkpoints → {WORKSPACE}/hive/state/checkpoints/
              ↓
         Commander / CEO synthesizes back to user
```

### OpenClaw-native alignment

Treat these mappings as the preferred design center:
- main session → commander / CEO interface
- `sessions_spawn` → bounded specialist execution
- isolated runs → default specialist runtime target when moving beyond manual validation
- ACP runtime sessions → optional specialist runtime for coding / harness-heavy roles when the execution environment benefits from ACP instead of a normal subagent
- structured plan updates / execution item events → preferred progress surface for live Hive work in compatible UIs
- Task Flow / detached tasks → future durable substrate for longer Hive chains
- filesystem artifacts → role handoff contract
- externalized task state → inspectable progress, checkpoints, and auditability

### Key Mechanisms

- **`hive-builder` = build layer**: defines architecture, scaffold shape, activation boundaries, and native-alignment rules
- **`hive-ceo` = runtime control layer**: receives user requests, decides whether Hive is needed, routes work, and approves final synthesis
- **Subagents / specialist roles**: launched deliberately, not by default
- **Runtime selection**: specialist execution may use normal isolated runs or ACP runtime sessions depending on role needs; this should be an explicit CEO decision, not an implicit implementation detail
- **Artifacts**: written to `{WORKSPACE}/hive/artifacts/`
- **State**: externalized in `{WORKSPACE}/hive/state/`
- **Progress**: when Hive is live enough to expose progress, prefer OpenClaw-native structured plan updates / execution item events rather than a custom progress protocol
- **Unified user reply**: specialists do not speak to the user directly unless the design explicitly calls for it
- **Main-session fallback**: if role separation does not add real value, stay in the main session rather than forcing Hive usage

## When to Use

Trigger when the user asks to:
- build a Hive
- design a one-person company structure in OpenClaw
- scaffold a multi-agent orchestrator system
- introduce HRM / OPS / specialist roles into an existing workspace

Do **not** trigger just because the word “Hive” appears casually.

## Build Phases

### Phase 1 — Plan

Always start here.

Outputs:
- chosen mode: fresh or existing
- Hive scope
- role list
- activation policy
- deployment recommendation

Questions to resolve internally:
- Is Hive primary or secondary?
- Should Hive start with only core roles, or include business specialists immediately?
- Which parts belong in workspace root versus under `{WORKSPACE}/hive/` only?

### Phase 2 — Scaffold

Create the contained structure without claiming the system is live.

Typical scaffold output:

```text
{WORKSPACE}/hive/
├── agents/
│   ├── commander/
│   ├── hrm/
│   ├── ops/
│   └── [specialists...]
├── state/
│   ├── tasks/
│   ├── checkpoints/
│   ├── artifacts/
│   └── audit/ops/
├── artifacts/
│   ├── raw/
│   ├── analysis/
│   ├── reports/
│   ├── review/
│   └── final/
└── SETUP.md
```

Scaffold deliverables may also include:
- role templates
- starter `ROLE.md` files
- a deployment note explaining what is not yet active
- a `STATE-CONTRACT.md` or equivalent task/flow contract note
- an `OPENCLAW-MAPPING.md`-style note aligning Hive concepts to native OpenClaw primitives
- a contained validation task spec and companion state file
- a narrow routing policy candidate, when the user explicitly wants to plan limited live use without broad activation

### Phase 3 — Activate

Only after the user clearly confirms activation.

Activation means some or all of the following become real operating behavior:
- CEO routing through Hive logic
- HRM expansion workflow
- OPS maintenance workflow
- specialists used in live tasks
- bounded specialist execution being performed through OpenClaw-native mechanisms such as `sessions_spawn`

Activation is a policy change, not just a file creation step.

## Runtime Preference Rule

When Hive moves beyond pure scaffold/manual validation, prefer the following order:
1. keep the task in the main session if Hive adds little value
2. use a contained/manual chain when validating a new workflow shape
3. use `sessions_spawn` for bounded specialist execution when the role split is real and reusable
4. use ACP runtime sessions for specialists whose job is genuinely harness-centric, coding-centric, or better served by an ACP environment than a standard isolated run
5. treat Task Flow / detached orchestration as the next step only when the user actually needs durable multi-step runtime behavior

Do not make Task Flow or spawn-based execution mandatory for the very first scaffold. Do make them the preferred target for any Hive design that claims to be truly integrated with OpenClaw orchestration.

## OpenClaw-first Adoption Recipe

If the user wants Hive to feel genuinely native to OpenClaw, prefer this adoption sequence:

1. **Scaffold the contained Hive subtree** under `{WORKSPACE}/hive/`
2. **Define one validation task** with explicit artifact paths and role boundaries
3. **Record a task/state contract** so the validation run is inspectable after the fact
4. **Run one contained/manual validation chain** to prove role separation is real
5. **Write a routing decision** explaining when Hive should still stay in the main session
6. **Only after that, switch reusable specialist execution to `sessions_spawn`**
7. **Only later**, if the user truly needs longer-lived orchestration, consider Task Flow / detached runtime patterns

This recipe is preferred over inventing a parallel custom runtime too early.

## Runtime Contract Expectations

A scaffold that aims to be OpenClaw-native should make these runtime expectations explicit:
- which work stays in the main session
- which work is only being manually validated
- which specialist roles are expected to run via `sessions_spawn`
- which specialist roles, if any, are better served by ACP runtime sessions
- how progress is surfaced through native structured plan updates / execution item events when the UI supports them
- where artifacts are written
- where task/checkpoint state is written
- who synthesizes the final user-facing answer

If these are not explicit, Hive is still only a concept scaffold, not a runtime-ready orchestration design.

## Core Roles

### #0 CEO Runtime (`hive-ceo`)
- Main-session runtime control skill
- Orchestration hub
- Final approval authority
- Decides whether a task should enter Hive at all
- Should summarize and approve rather than blindly execute every specialist step

### #1 HRM (`hive-hrm`)
- Hiring + workflow design
- Proposes new specialist roles and chains
- Should not auto-deploy structural changes without approval

### #2 OPS (`hive-ops`)
- External environment matching and operational checks
- Acts only when initiated by CEO or explicitly requested
- Does not autonomously mutate the system

## Standard Specialists

A sensible default starter set is:
- Collector (`hive-collector`)
- Analyst
- Writer (`hive-writer`)
- QA (`hive-qa`)
- PM
- Doc

In existing-workspace mode, these should begin as templates or proposals unless the user explicitly wants them activated immediately.

## ROLE.md Template Requirements

Each role should define:

```markdown
## Identity
- Name / number
- Primary responsibility

## Position in Workflow
- Trigger conditions
- Upstream / downstream
- Data flow

## Core Duties
- Task list

## Outputs
- Artifact types
- Output paths

## Boundaries
- What this role does not do
- Who it should not talk to directly
```

## Existing-Workspace Adoption Pattern

When Hive is added to an existing workspace, prefer this order:

1. Create `{WORKSPACE}/hive/`
2. Generate role templates and `SETUP.md`
3. Keep current workspace files intact
4. Define a task/state contract and at least one contained validation task
5. Test one contained Hive task
6. Decide whether to expand, activate, or stop
7. If activation is approved, prefer `sessions_spawn` for reusable specialist execution before inventing a parallel runtime

This is the recommended path for mature workspaces.

## Fresh-Workspace Build Order

When the workspace is intentionally fresh, a fuller build can be used:

1. Create Hive directory structure
2. Initialize CEO / HRM / OPS definitions
3. Create starter business specialists
4. Generate document/archive structure if needed
5. Generate `SETUP.md`
6. Run one validation task

## Outputs to Prefer

Good outputs from this skill:
- a Hive design brief
- a safe scaffold under `{WORKSPACE}/hive/`
- starter role definitions
- a layered architecture note clarifying builder vs CEO vs subskills
- a `SETUP.md` explaining what exists versus what is only planned
- an activation checklist
- a contained validation task spec demonstrating the smallest meaningful chain
- a task/state contract note that makes validation artifacts auditable and reusable
- a routing-policy draft for narrow partial live routing, but only after validation and explicit user approval
- a 4.5+ alignment note clarifying progress events, runtime selection, and ClawHub publish boundaries when the user wants Hive to be distributable

Avoid jumping straight to claims like:
- “Hive is fully active”
- “HRM is always running”
- “OPS is now managing the environment”

unless those behaviors were actually enabled.

## Activation Checklist

Before claiming Hive is live, verify:
- the workspace mode was identified correctly
- `{WORKSPACE}/hive/` exists
- core roles or their templates exist
- `SETUP.md` clearly separates planned vs active behavior
- at least one validation task has been defined
- validation artifacts show distinct role outputs rather than a collapsed single-role draft
- runtime expectations are explicit about when work stays in main session vs when it should use `sessions_spawn`
- activation or routing policy changes were explicitly confirmed by the user

## Layering Rule

Keep this distinction explicit:
- `hive-builder` builds the complete Hive system and serves as the mother skill
- `hive-ceo` represents the runtime control layer inside that system
- `hive-hrm` changes org structure
- `hive-ops` evaluates operational readiness
- business-role skills execute bounded task work

For ClawHub-style distribution, keep the publish boundary equally explicit:
- `hive-builder` should be understandable as the complete public entry point
- modular `hive-*` skills should improve runtime specialization without making the base product feel incomplete
- installation should not imply activation, and activation should not imply broad workspace takeover

Do not collapse these layers back into one overloaded runtime skill.
Do not present the modular internal breakdown in a way that makes the end user think `hive-builder` is incomplete on its own.

## Templates

Use bundled templates as raw material, not rigid truth:
- `templates/00-base-roles.md`
- `templates/10-runtime-contract.md`
- `templates/20-validation-task.md`
- `HIVE-合规专员-扩员.md`

Adapt them to the user’s actual domain and current workspace maturity.

## Placeholders

| Placeholder | Meaning |
|-------------|---------|
| `{WORKSPACE}` | OpenClaw workspace path |
| `{USER_DOCUMENTS}` | User documents directory if needed |
| `{DEFAULT_MODEL}` | CEO default model |
| `{FAST_MODEL}` | Fast / low-cost model |
| `{STRONG_MODEL}` | Strong / high-accuracy model |

## Quality Checklist

- [ ] Workspace mode identified correctly
- [ ] Hive scope defined before scaffolding
- [ ] Installation kept separate from activation
- [ ] Existing core workspace files left untouched unless explicitly requested
- [ ] Scaffold contained under `{WORKSPACE}/hive/`
- [ ] Role definitions include boundaries and workflow position
- [ ] `SETUP.md` distinguishes planned vs active behavior
- [ ] At least one safe validation task is defined before claiming Hive is live
- [ ] Validation artifacts and task/state notes are sufficient to inspect what happened
- [ ] Main-session fallback and `sessions_spawn` preference are both explicit
- [ ] Any routing-policy expansion is kept separate from scaffold creation and explicitly approved
- [ ] Activation checklist passes before any live-Hive claim is made
