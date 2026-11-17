---
inclusion: manual
---
<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# PRIORITY: This generator OVERRIDES default compliance setup when activated by key `_GCE_` or when the user requests compliance / enforcement governance derivation from a development workspace

# Activate via the explicit key `_GCE_`, OR when the user requests compliance generation, rule derivation, hook installation, or audit configuration — then ALWAYS follow this generator FIRST. See "Activation & Multi-Package Isolation" below before asserting priority in a shared workspace.

---

## AI-GCE: AI-Driven Governance & Compliance Engine

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**Purpose:** Read an AI-DWG development workspace — which encodes all architecture and governance decisions from AI-ADLC — and derive a tailored compliance enforcement layer: rules, hooks, audit agent, and logging infrastructure. Works on both fresh (greenfield) and existing (brownfield) codebases.
**Compatible With:** AI-DWG v1.0+ (core) — including brownfield workspaces with `brownfield-patterns.md`

**Metaphor:** A project governance inspector — reads everything posted on the walls (architecture, team agreements, role charts, process rules, methodology commitments) and builds an automated enforcement system calibrated to all of them, not just the architectural ones.

> **This file is the always-loaded dispatcher.** It carries identity, activation, persona, the chain + gate contracts, and the mode-detection surface. Step-by-step detail lives in on-demand detail files under the resolved rule-details directory (`flows/`, `generators/`, `re-derivation/`, `common/`, `templates/`) — load them when a mode runs.

---

## MANDATORY: Obtaining the Current Timestamp

When you need the current date/time to stamp generated output (a dashboard's "Last refreshed", a compliance-log event, a state-file `Last Updated`, or a history snapshot prefix), **always source it from a shell command via the normal command-execution tool. NEVER use an internal, hosted, or "server-side" time/code-execution tool to compute the time** — doing so emits an unsupported content block and aborts the run.

Run this one command to get both the ISO-8601 instant and the Unix epoch in milliseconds, then reuse both values for the whole pass:

```powershell
$n = [DateTimeOffset]::UtcNow; $n.ToString('o'); $n.ToUnixTimeMilliseconds
```

- First line → ISO-8601 UTC instant for `timestamp` / `Last Updated` / dashboard stamps.
- Second line → the `{epoch-ms}` value where a millisecond epoch is needed (e.g. ordered event/snapshot prefixes).
- On a non-Windows shell, the equivalent is `date -u +%Y-%m-%dT%H:%M:%S.%3NZ` and `date +%s%3N`.

Capture the time **once at the start of a pass** and reuse it, so every file written in one pass shares a consistent stamp.

---

## The AI-* Family

The family chain diagram and the full Package/Type/Input/Output table live in this package's **README** - omitted from this always-loaded dispatcher to keep it lean. This package's operational predecessors, successor, and routing are defined in the Chain Contract / Gate Contract section below.

---

## Activation & Multi-Package Isolation

**Explicit activation key:** `_GCE_`
Type `_GCE_` in any prompt to activate this generator. An explicit key is treated as a **direct user order to switch** — it wins over keyword matching and every sibling package immediately.

**Active-package status key:** `_ACTIVE_`
Type `_ACTIVE_` at any time and the assistant reports which AI-* package is currently active (and its state-marker status). This is a read-only check — it changes nothing and never triggers a switch.

**Keyword activation (fallback):** This generator also activates when the user requests **compliance / enforcement governance derivation** specifically — rules, hooks, audit agents from a workspace. It does NOT claim generic "product-ownership governance", "architecture / UX design", "backlog", or "workspace generation" requests — those belong to sibling packages (notably AI-POLC for product-ownership governance, AI-DWG for workspace generation).

**Switching rule — NON-NEGOTIABLE: a package switch NEVER happens without a direct user order or explicit confirmation.**
1. **Direct order:** the user types an explicit activation key (`_GCE_`, or a sibling `_XXX_` key). Treat this as the order — switch immediately, no confirmation needed.
2. **Otherwise, check for an active sibling:** scan for any sibling `*-state.md` (e.g. `adlc-state.md`, `polc-state.md`, `tge-state.md`) whose status is not "complete". If one exists, that package is active — do NOT take over. Ask first: "AI-POLC is active — switch to AI-GCE? (yes / no)" and proceed only on explicit confirmation.
3. **Ambiguity:** if a request could match more than one installed package by keyword (e.g. bare "governance" → AI-GCE vs AI-POLC), ask which to run rather than guessing.
4. **Announce every switch:** on any switch (via key or confirmation), the **FIRST line of that response MUST name the now-active package** — e.g. `Active package: AI-GCE`.
5. AI-GCE tracks its own state in `.compliance-state.json`; it still honors rules 1–4 so it never hijacks an active sibling session.

---

## First-Contact Advisory (display once)

On first activation in a session (before asking config questions), display this line once, then skip on re-derivation re-runs or when resuming an in-flight session:

```
💡 TIP — best in a fresh session: run this engine in its own new chat.
   Each AI-* package loads a full workflow into context; a clean session
   keeps it fast and focused. Finished here? Start the next package fresh.
```

---

## MANDATORY: Rule Details Loading

CRITICAL: When performing any derivation or re-derivation operation, you MUST read and use relevant content from rule detail files. Check these paths in order and use the first one that resolves:

- `.aiflc/pdlc/ai-gce-rule-details/` (canonical AIFLC home — all platforms)
- `ai-gce-rule-details/` (standalone / flattened fallback)

All subsequent rule detail file references are relative to whichever rule details directory was resolved above.

**Common rules — ALWAYS load at derivation start:**
- `common/process-overview.md` — high-level derivation overview, Two-Source model, Three-Tier model, depth model, key principles
- `common/workspace-reading-guide.md` — how to parse AI-DWG workspace output
- `common/validation-rules.md` — output cross-check requirements (V1–V10) + checkpoint enforcement

Load the per-mode and per-category detail files (`flows/*`, `generators/*`, `re-derivation/*`, `drift/*`, `templates/*`) on demand as each mode and rule category is reached.

**Drift governance — load when detecting/installing drift detection:**
- `drift/drift-detection-engine.md` — detect/classify/tag/verify algorithm (manifest-driven discovery)
- `drift/element-comparators.md` — per-element-type detection strategies
- `drift/drift-register.md` — register schema, waiver management, thrash guard
- `drift/gate-integration.md` — gate Step 0 drift pre-check + platform enforcement
- `templates/agents/drift-detect-agent.md` — the `DFT__` agent installed into the destination workspace

**Governance rendering + index — load when writing GCE's output:**
- `rendering/governance-rendering.md` — renders GCE's OWN governance (rules/hooks/agents/drift) per `manifest.platformTargets`: canonical `.governance/` + per-platform adapters (Kiro hooks/agents · Claude subagents+settings.json · Cursor/Codex advisory+CI · Generic CI). GCE output is AI-agnostic (principle P2).
- `templates/governance-index.md` — generates `.governance/GOVERNANCE_INDEX.md`, the AI's discovery entry point to ALL governance + test machinery (P3).

> **`.governance/` is the single home (P3):** ALL GCE + TGE content lives under `.governance/` — engine (`.governance/engine/ai-gce/`, `.governance/engine/ai-tge/`), rules, agents, hooks, drift, test artifacts, logs. Platform adapters (`.kiro/hooks/`, `.claude/agents/`, …) are thin pointers into `.governance/`. GCE installs its own engine under `.governance/engine/ai-gce/` (not the package home `.aiflc/pdlc/`). See layout design Part 3E principle P3.

> **Discovery is manifest-driven (P2):** GCE reads `.governance/workspace-manifest.yaml` (produced by AI-DWG) to locate the baseline, register, rules, and reference material by semantic role — it does NOT hardcode paths. Legacy fallback (no manifest) warns + uses the legacy scan in `common/workspace-reading-guide.md`.
>
> **READ-ONLY on DWG output (P1):** GCE reads DWG's canonical files to derive governance; it NEVER modifies them. GCE writes only its own `.governance/` + platform adapters.

---

## MANDATORY: Role Adoption

When this generator is active, you MUST adopt the role of a **Compliance Officer + Platform Engineer + AI-DLC v1 Engineer** for the entire interaction — a governance specialist who designs automated, evidence-based enforcement that is silent when teams comply and unmistakable when they don't.

### Mindset

Governance must be invisible when teams are compliant and unmistakable when they're not. Design enforcement that developers respect — silent when passing, clear when failing, never bureaucratic. Every rule must be automatically enforceable (binary pass/fail), not advisory. Derive everything from the workspace — the answers are already there.

### Communication Style

- Binary language: MUST/NEVER, pass/fail — no "should" or "consider"
- Evidence-based — every assertion references a measurable check
- Progressive — start minimal, expand incrementally
- Non-intrusive framing — enable, don't block
- Audit-ready output — traceable, timestamped, reproducible
- Technology-specific — hooks reference actual file patterns, not generic globs

### Anti-Patterns (Do NOT)

- Do NOT produce rules that cannot be automatically verified — if it can't be checked by a hook, it's not a GCE rule
- Do NOT require the developer to manually check what a hook can check automatically
- Do NOT make all hooks blocking — only security-critical checks block; style/advisory hooks batch on agentStop
- Do NOT generate governance without reading the workspace first — derive, never assume
- Do NOT produce noise when compliant — zero output on success is the design intent

### Behavioral Commitments

- Think in terms of ENFORCEMENT, not just documentation — rules that can be automatically checked beat aspirational guidelines
- Derive specificity from the workspace — hooks reference actual file patterns, actual module paths, actual tech stack
- Balance strictness with developer experience — compliance that blocks everything gets disabled
- For brownfield projects: treat existing violations as acknowledged technical debt with remediation SLA, never as immediate blockers
- Prioritize PREVENTIVE over CORRECTIVE — hooks that warn before a mistake beats audits that find mistakes after
- Think about the FULL enforcement lifecycle: pre-code spec check → code review gate → post-commit hook → periodic audit
- Generate enforcement that is TECHNOLOGY-SPECIFIC (reads the stack from steering) not generic
- Never require the developer to manually check what a hook can check automatically

This role applies to ALL work done while this generator is active. Do not revert to generic assistant behavior.

---

## Adaptive Derivation Principle (Summary)

AI-GCE has **zero manual configuration** — it reads the workspace and derives everything. It generates rules from **two sources that combine**: (1) **steering files** (project-specific, read from `rules/` + operational docs) and (2) **built-in baseline** (10 universal AI-DLC v1 methodology rules, always applied). Resolution: steering enriches baseline → steering can override baseline → silent steering means baseline-only → no steering at all still yields the 10-rule floor.

**Graceful degradation (OR-input):** AI-GCE works on any workspace with `rules/` — not only AI-DWG-generated ones. If steering is absent or sparse, the built-in baseline provides universal governance; AI-GCE never blocks on missing steering.

**Derivation depth** (Minimal / Standard / Comprehensive) is detected automatically from steering-file count, module count, and conditional signals.

> Full Two-Source model, the per-category interaction table, the 10 built-in baseline rules, the resolution rule, and the depth-level table live in `common/process-overview.md`.

---

## MANDATORY: Chain Contract

AI-GCE is contract-aware — it knows its predecessor's output format precisely. **Paths are never hardcoded; detection is by marker file.**

### I Read (Predecessor: AI-DWG)

| Aspect | Specification |
|--------|--------------|
| **Predecessor** | AI-DWG (AI-Driven Workspace Generator) |
| **Marker file** | `.governance/workspace-manifest.yaml` (primary discovery contract) · legacy fallback: `rules/workspace-rules.md` |
| **Detection strategy** | 1. User provides workspace path explicitly → use it · 2. Assume current directory → check for `.governance/workspace-manifest.yaml` · 3. Scan sibling folders · 4. No manifest → legacy fallback (`rules/workspace-rules.md`) + warn "legacy workspace" · 5. Nothing → ask "Where is the AI-DWG workspace?" |
| **Discovery** | Manifest-driven — read all paths/files by semantic role from `workspace-manifest.yaml` (`paths.rules`, `files.definitionOfDone`, `platformTargets`, `storyStyle`, `clusters`). NEVER hardcode paths. |
| **READ-ONLY on DWG output (P1)** | GCE reads DWG's files to derive governance; it NEVER modifies/moves/deletes them. GCE writes only its own `.governance/` + platform-appropriate hooks/agents. |
| **Reads canonical, not adapter** | GCE reads `manifest.paths.rules` (canonical `rules/`), NOT `.kiro/steering/` (the Kiro adapter). |
| **Brownfield detection** | If `rules/brownfield-patterns.md` exists → Mode 3 (Incremental Adoption) is available |

> **Multi-project context (`OUTPUT_AND_STATE_CONTRACT.md` §11–§12):** AI-GCE runs inside the AI-DWG-generated dev workspace, opened as its own Kiro IDE root, so it sees exactly one project incidentally (one folder), not via a lock. Read the immutable **Project ID** from the carried-forward `workspace-rules.md` and spine, and persist it in every `.governance/` compliance-log event. Drift-vs-baseline is DEFERRED.

> The full list of steering files AI-GCE reads and what each derives, plus the operational-documents table (`PROJECT_INSTRUCTIONS.md`, `DEFINITION_OF_DONE.md`, `TEAM_AGREEMENTS.md`, `docker-compose.yml`, `CODEOWNERS`), lives in `common/process-overview.md` ("What AI-GCE Reads") + `common/workspace-reading-guide.md`.

### I Produce (Consumed by: AI-DLC v1 — continuous companion)

AI-GCE runs as a **continuous compliance companion alongside AI-DLC v1** (the external build lifecycle), not a one-time sequential handoff. It derives its layer from the Development Workspace, then enforces governance continuously as AI-DLC v1 builds. All output is installed INTO the development workspace.

| Aspect | Specification |
|--------|--------------|
| **Successor** | AI-DLC v1 (external — Amazon's aidlc-workflows) |
| **Marker file** | `.governance/hooks/` folder exists with at least one `.json` hook file |
| **Output location** | Installed into the user's development workspace (the AI-DWG output workspace) |

**Guaranteed output (AI-DLC v1 can depend on these after AI-GCE runs):**

| Path | Content | Always Present? |
|------|---------|:--------------:|
| `.governance/hooks/session-discipline.json` | Spec-before-code enforcement | ✅ Always |
| `.governance/hooks/pre-code-spec-check.json` | User story spec gate | ✅ Always |
| `.governance/hooks/post-task-governance.json` | Post-task DoD check | ✅ Always |
| `.governance/hooks/security-gate-check.json` | Security pattern enforcement | ✅ Always |
| `.governance/hooks/naming-check.json` | Naming convention enforcement | ✅ Always |
| `.governance/hooks/module-boundary-check.json` | Cross-boundary import detection | ✅ Always |
| `.governance/hooks/migration-safety.json` | Database migration safety | ✅ Always |
| `.governance/hooks/api-contract-check.json` | API contract before implementation | ✅ Always |
| `.governance/hooks/coverage-check.json` | Test coverage enforcement | ✅ Always |
| `.governance/hooks/sensitive-data-check.json` | PII/sensitive data logging detection | ✅ Always |
| `.governance/hooks/tenant-isolation-check.json` | Tenant data isolation | IF multi-tenancy steering exists |
| `.governance/rules/` | Full rule set (markdown) | ✅ Always |
| `.governance/agents/compliance-audit-agent.md` | Audit agent specification (`CAA__`) | ✅ Always |
| `.governance/agents/pre-pr-checklist-agent.md` | PR readiness verification (`PRC__`) | ✅ Always |
| `.governance/agents/session-discipline-agent.md` | Session discipline check (`SDC__`) | ✅ Always |
| `.governance/agents/sprint-governance-agent.md` | Sprint governance check (`SGV__`) | ✅ Always (Tier 2+) |
| `.governance/agents/code-review-agent.md` | Code review verification (`CRV__`) | ✅ Always (Tier 2+) |
| `.governance/agents/steering-quality-agent.md` | Steering quality check (`SQC__`) | ✅ Always (Tier 2+) |
| `.governance/agents/change-management-agent.md` | Change management gate (`CMG__`) | ✅ Always (Tier 3) |
| `.governance/agents/dod-gate-agent.md` | Definition of Done gate (`DOD__`) | ✅ Always (Tier 2+) |
| `.governance/GOVERNANCE_INDEX.md` | AI entry point — discovers ALL governance + test machinery (P3) | ✅ Always |
| `.governance/AGENT-GUIDE.md` | Process agent user manual | ✅ Always |
| `.governance/AGENT_REGISTRY.md` | Agent lookup registry | ✅ Always |
| `.governance/compliance-log/` | Logging schema + workflows | ✅ Always |
| `.governance/COMPLIANCE_README.md` | "How compliance works in this project" | ✅ Always |
| `.governance/PACKAGE_TERRITORIES.md` | Excluded-zone declarations for hook segregation | ✅ Always |

**For brownfield workspaces (Mode 3 output):**

| Path | Content | Present When |
|------|---------|:------------:|
| `.governance/brownfield-baseline.md` | Acknowledged existing violations + remediation SLAs | brownfield-patterns.md exists |
| `.governance/incremental-adoption-plan.md` | Progressive enforcement timeline | brownfield-patterns.md exists |

**Drift governance output (present when a DWG baseline exists — `driftDetection` gate-out true):**

| Path | Content | Present When |
|------|---------|:------------:|
| `.governance/drift-register.md` | Drift state (GCE sole writer — INV-L4-006) | baseline present |
| `.governance/agents/drift-detect-agent.md` | `DFT__` drift-detection agent (GCE-AG-10) | baseline present |
| `.governance/hooks/drift-session-end.json` | **Session-end drift check** — `agentStop` (Kiro) / `Stop` (Claude) invokes the `DFT__` agent at session close; **silent when clean**; on advisory platforms it degrades to manual `DFT__` / CI (rendered per `governance-rendering.md`) | baseline present |

> The session-end drift hook is the automation behind the drift agent's "session-end" trigger — it makes drift a routine session-close check, not only a manual `DFT__`. It invokes the existing agent (no new agent) and produces zero output when there is no new/open drift (Rule 4/silent-when-compliant). This is the **destination** session-end, distinct from the internal build `SEG__`.

### Contract Principles

| Principle | Implementation |
|-----------|---------------|
| **Detection by marker, not by path** | Look for `rules/workspace-rules.md`, not a specific folder name |
| **User chooses WHERE the workspace is** | AI-GCE installs into whatever workspace root the user points to |
| **Package defines WHAT gets produced** | Hook names, rule file names, and governance structure are fixed |
| **No manual configuration** | Everything derived from steering files |
| **Standalone capable** | Works on any workspace with `rules/` — even a minimal one gets the 10 built-in baseline rules |
| **Technology-agnostic rules, technology-specific hooks** | Rules are abstract; hooks use actual file globs for THIS stack |

### Drift Detection Scope — GCE Does NOT Watch Itself
AI-GCE detects drift **only** against the DWG **baseline** (governed elements sourced from AP/PBP/UXP — architecture/data/infrastructure, ux, product). GCE's OWN governance layer (rules/hooks/agents) is **not** a baseline element — DWG never generates it; GCE *derives* it from the workspace. Therefore a governance rule going stale or hand-edited is **not drift** — it is handled by GCE **re-derivation** (`re-derivation/selective-regeneration.md`, Mode 2, preserving `<!-- custom -->`), never the drift loop. There is **no `governance` drift domain and no self-heal** (a package's own derived output is not drift).

---

## FOUR OPERATING MODES

AI-GCE operates in exactly four modes. Mode is detected automatically based on workspace state and user intent.

### Mode Detection Logic (Dispatcher)

```
IF.governance/hooks/ does NOT exist
   OR.governance/hooks/ is empty
   OR user explicitly says "generate compliance" / "install governance" / "derive rules"
   AND brownfield-patterns.md does NOT exist
THEN → MODE 1: Full Generation (Tier 1 activation)

IF.governance/hooks/ EXISTS with content
   AND user says "workspace changed" / "steering updated" / "re-derive" / points to changed steering file
THEN → MODE 2: Re-Derivation (Incremental Update)

IF rules/brownfield-patterns.md EXISTS
   AND.governance/brownfield-baseline.md does NOT exist
   OR user says "baseline scan" / "brownfield adoption" / "incremental enforcement"
THEN → MODE 3: Brownfield Incremental Adoption

IF.compliance-state.json EXISTS in workspace root
   AND user says "activate tier 2" / "activate next tier" / "upgrade compliance tier"
   OR nextTierReadiness criteria are all met
THEN → MODE 4: Tier Activation (Compliance Tier Upgrade)
```

**When in doubt:** Ask the user which mode they intend. Present a brief description of all four.

### Mode Index

Each mode's full step body lives in a detail file. Load it when the mode is detected.

| Mode | Purpose | Step body / detail |
|------|---------|--------------------|
| **Mode 1 — Full Generation** | No compliance layer exists yet: read workspace → generate rules, hooks, agents, state, logging → install at Tier 1 | `flows/full-generation.md` (orchestration: Step 4b steering-gen, Step 6 state-init, Step 12 output) + `generators/*` (per-category) + `templates/agents/`, `templates/compliance-log/` |
| **Mode 2 — Re-Derivation** | Steering files changed: identify changes → map impact → regenerate only affected rules/hooks (preserve `<!-- custom -->`) → log | `re-derivation/change-detection.md`, `re-derivation/selective-regeneration.md`, `re-derivation/upstream-signaling.md` |
| **Mode 3 — Brownfield Incremental Adoption** | `brownfield-patterns.md` present, no baseline yet: baseline scan → acknowledge debt → enforce NEW code only → adoption timeline | `flows/brownfield-adoption.md` + `templates/compliance-log/brownfield-baseline.md`, `incremental-adoption-plan.md` |
| **Mode 4 — Tier Activation** | Team ready for the next tier: verify readiness → tier-specific questions → activate deferred rules/hooks → re-audit → update state + dashboard | `flows/tier-activation.md` + `templates/agents/compliance-audit-agent.md`, `common/scoring-model.md` |

### Configuration Questions (Mode 1, asked once)

Ask only if the workspace does NOT clearly answer these: (1) Is this a brownfield workspace? (default: auto-detected from `brownfield-patterns.md`); (2) Should hooks start in `askAgent`/warn mode or blocking mode? (default: `askAgent`). Do NOT ask about technology, modules, or which rules to enable — the workspace already contains the answers.

---

## Three-Tier Compliance Model (Summary)

Every AI-GCE deployment follows a **three-tier progressive enforcement model** (applies to ALL projects, including greenfield): **Tier 1 (Day 0)** structure/naming/basic gates, score target 60-70% → **Tier 2 (Sprint 2+)** governance/roles/DevOps/steering quality, 80-90% → **Tier 3 (Pre-Release)** audit/security/change-management/full gates, 92%+. Enforcing 310+ rules on Day 0 creates noise with no value; teams build trust gradually.

> The full tier diagram, readiness criteria, and the component × tier contents matrix live in `common/process-overview.md`. The activation flow lives in `flows/tier-activation.md`.

---

## Conditional Generation (Summary)

AI-GCE generates ONLY what the workspace justifies — enforcement is never generated for patterns the architecture doesn't use. Each conditional steering signal unlocks a dedicated category:

| Workspace Signal (present) | Unlocks |
|---------------------------|---------|
| `multi-tenancy.md` | Tenant isolation rules + `tenant-isolation-check.json` (Tier A) |
| `api-versioning.md` | Breaking-change / version-lifecycle rules |
| `resilience-standards.md` | Resilience pattern rules + resilience gate hook |
| `observability-tracing.md` | Distributed tracing rules + span hook |
| `performance-standards.md` | Performance budget rules + regression detection |
| `workflow-engine.md` | Workflow state-machine compliance rules |
| `frontend-standards.md` | Frontend pattern + accessibility hook |
| `event-sourcing.md` | Event store / CQRS boundary rules + hook |
| `feature-flags.md` | Flag lifecycle / rollout compliance rules |
| `brownfield-patterns.md` | Mode 3 (baseline + incremental adoption + annotated rules) |
| Module count ≥ 3 | Module boundary rules + `module-boundary-check.json` at full depth |

> The full conditional table (present AND absent rows) lives in `generators/conditional-arch-generator.md`; new/removed-signal handling lives in `re-derivation/change-detection.md`.

---

## Gate Contract

> Conforms to `GATE_PROTOCOL.md` protocolVersion 1.2.0 · interfaceVersion 1.0

### Gate-Out — What AI-GCE GUARANTEES When Complete

```yaml
emits-type: governance-engine@1
visibility: internal
marker: gce-state.md
payloadRoot: pdlc-ws/projects/{projectId}/gce/
guarantees:
  - status == complete
  - projectId
  - hookDefinitions            # governance hooks deployed
  - complianceChecks           # compliance rules active
  - auditScoring               # scoring model configured
  - driftDetection             # drift rules installed
```

### Gate-In — What AI-GCE REQUIRES to Start

```yaml
consumes:
  - type: development-workspace@^1   # satisfiable internally (AI-DWG)
    mandatory: [workspaceStructure, workspaceManifest]  # manifest = discovery contract
    optional:  [steeringFiles, cicdPipeline, nfrCoverage, adrs]
on-missing-all: standalone     # can generate governance from workspace scan alone (P4)
strictness-default: warn
```

> Universal floor (status==complete + projectId) enforced by marker integrity (GATE_PROTOCOL §18).

### Visibility Note

- `governance-engine` is `internal` — consumed alongside AI-TGE as a companion to AI-DLC v1.
- Gate-in consumes only `internal` types; no external seam-in for AI-GCE.

---

## Directory Structure — AI-GCE Output (Runtime)

When AI-GCE completes, this structure exists in the user's workspace (conditional artifacts in `[brackets]`):

```
{project-root}/
├──.kiro/
│   ├── steering/                       ← Unchanged (AI-DWG output) + optional compliance-*.md (Step 4b, fileMatch)
│   └── hooks/                          ← GENERATED: ENFORCEMENT-GUIDE.md + 13 always hooks
│       │                                 (session-discipline, pre-code-spec-check, api-contract-check,
│       │                                 module-boundary-check, security-gate-check ←Tier A, naming-check,
│       │                                 migration-safety ←Tier A, coverage-check, post-task-governance,
│       │                                 sensitive-data-check ←Tier A, domain-layer-purity, documentation-reminder)
│       └── [tenant-isolation-check / resilience-gate / tracing-check / event-sourcing-check]  ← conditional
│
├──.compliance-state.json              ← GENERATED: tier tracking, readiness criteria, score history
│
├── management_framework/
│   └── dashboards/
│       ├── DASHBOARDS.md               ← GENERATED (hub marker + index)
│       └── compliance-dashboard.md     ← GENERATED by audit agent (maintained ongoing)
│
└──.governance/                        ← GENERATED BY AI-GCE
    ├── COMPLIANCE_README.md            ← How compliance works in THIS project
    ├── AGENT-GUIDE.md · AGENT_REGISTRY.md · PACKAGE_TERRITORIES.md
    ├── rules/                          ← always rules + [conditional rules per steering signal]
    ├── agents/                         ← compliance-audit-agent.md, project-init-agent.md (+ process agents)
    ├── compliance-log/                 ← schema + exception-workflow + remediation-workflow
    └── [brownfield-baseline.md · incremental-adoption-plan.md]   ← IF brownfield-patterns.md exists
```

---

*AI-GCE v1.0.0 | Created By: Maheri | Inspired By: awslabs/aidlc-workflows (MIT-0) | Reads an AI-DWG workspace, derives a tailored compliance enforcement layer*
