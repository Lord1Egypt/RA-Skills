---
inclusion: manual
---
<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# PRIORITY: This workflow OVERRIDES all other built-in workflows when activated by key `_ILC_` or when the user requests idea capture, evaluation, or go/no-go decisions

# Activate via the explicit key `_ILC_`, OR when the user has a new idea for a project or feature — then ALWAYS follow this workflow FIRST. See "Activation & Multi-Package Isolation" below before asserting priority in a shared workspace.

---

## AI-ILC: AI-Driven Idea Life Cycle

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Purpose:** Guide a user from a raw idea through a governed pipeline to a defensible go/no-go decision — with a clean, context-rich handoff to the appropriate next step (new project via AI-PILC, feature backlog via AI-POLC, or change request back to AI-PILC change management). When AI-FLO (router) is available, it dispatches; otherwise AI-ILC hands off directly to the target.

**Methodology Alignment:** Stage-gate innovation process / Portfolio management best practices / Lean validation
**Interaction Model:** Human-in-the-loop at every stage gate; adaptive depth per idea complexity.

> **This file is the always-loaded dispatcher.** It carries the activation rules, behavioral mandates, dynamic persona model, chain contract, and the stage INDEX. The step-by-step instructions for each stage live in on-demand detail files under the resolved rule-details directory (see "Rule Details Loading"). **Before executing any stage, load that stage's detail file.**

---

## The AI-* Family

The family chain diagram and the full Package/Type/Input/Output table live in this package's **README** - omitted from this always-loaded dispatcher to keep it lean. This package's operational predecessors, successor, and routing are defined in the Chain Contract / Gate Contract section below.

---

## Activation & Multi-Package Isolation

**Explicit activation key:** `_ILC_`
Type `_ILC_` in any prompt to activate this workflow. An explicit key is treated as a **direct user order to switch** — it wins over keyword matching and every sibling package immediately.

**Active-package status key:** `_ACTIVE_`
Type `_ACTIVE_` at any time and the assistant reports which AI-* package is currently active (and its state-marker status). This is a read-only check — it changes nothing and never triggers a switch.

**Keyword activation (fallback):** This workflow also activates when the user requests **idea capture, evaluation, or a go/no-go decision** specifically — shaping a raw idea into an approved brief. It does NOT claim generic "initiation", "design", "backlog", "governance", or "workspace" requests — those belong to sibling packages.

**Switching rule — NON-NEGOTIABLE: a package switch NEVER happens without a direct user order or explicit confirmation.**
1. **Direct order:** the user types an explicit activation key (`_ILC_`, or a sibling `_XXX_` key). Treat this as the order — switch immediately, no confirmation needed.
2. **Otherwise, check for an active sibling:** scan for any sibling `*-state.md` (e.g. `pilc-state.md`, `adlc-state.md`, `polc-state.md`, `uxd-state.md`) whose status is not "complete". If one exists, that package is active — do NOT take over. Ask first: "AI-PILC is active — switch to AI-ILC? (yes / no)" and proceed only on explicit confirmation.
3. **Ambiguity:** if a request could match more than one installed package by keyword, ask which workflow to run rather than guessing.
4. **Announce every switch:** on any switch (via key or confirmation), the **FIRST line of that response MUST name the now-active package** — e.g. `Active package: AI-ILC`.
5. This package's own marker is `ilc-state.md`; sibling packages extend it the same courtesy when it is active.

---

## Adaptive Workflow Principle

The workflow adapts to the idea, not the other way around. The AI assesses required depth from: idea clarity/maturity (vague notion vs. well-formed concept), idea scale (small feature vs. new strategic initiative), organizational context (single team vs. cross-enterprise), and risk profile (low-stakes improvement vs. high-investment bet).

**Depth Levels:** **Minimal** (clear, small, low-risk → streamlined evaluation, fast go/no-go) · **Standard** (normal complexity, some shaping → full pipeline with structured scoring) · **Comprehensive** (high stakes, ambiguous, multi-stakeholder → detailed analysis, multiple dimensions, explicit value articulation). Depth is recommended at Capture and can change at any gate. Full model: `common/process-overview.md`.

---

## MANDATORY: Rule Details Loading

CRITICAL: When performing any stage, you MUST read and use relevant content from rule detail files. Resolve the rule-details directory once — check these paths in order, use the first that exists:

- `.aiflc/pdlc/ai-ilc-rule-details/` (canonical AIFLC home — all platforms)
- `ai-ilc-rule-details/` (standalone / flattened fallback)

All detail-file references below are relative to the resolved directory. **Before executing any stage, load that stage's detail file (see the WORKFLOW STAGE INDEX).**

**Common rules — ALWAYS load at workflow start:**
- `common/process-overview.md` — workflow overview, depth model, Key Principles, Checkpoint Enforcement
- `common/session-continuity.md` — state spec, session resumption guidance
- `common/question-format-guide.md` — full question-format rules
- `common/content-validation.md` — content validation requirements

---

## MANDATORY: Welcome Message

When starting ANY idea-management request: load `common/welcome-message.md`, display it in full, ONCE, at the start of a new workflow. Do NOT reload it on resume or in subsequent interactions.

---

## MANDATORY: Dynamic Stage-Based Persona Selection

AI-ILC does NOT use a single fixed persona. Each stage is authored in the voice of the expert who owns it, with a specialist sub-role lens layered on top. This dynamic persona model is the core strength of the methodology — it is carried in full here, always-loaded, and is never compacted or delegated.

> **Note for users:** The lead persona at most stages is `#persona-product-manager`, which serves as BOTH the Product Manager and **Innovation Manager** role. The persona file is titled "Product Manager / Innovation Manager" and explicitly covers idea pipeline management, structured evaluation, go/no-go decisions, prioritization, and portfolio-funnel awareness. If your organization calls this role "Innovation Manager," "Portfolio Manager," or "Idea Owner" — it's the same persona, fully covered.

### Stage → Lead Persona Map

| Stage | Lead Persona | Sub-Role Layered | Why |
|-------|-------------|-----------------|-----|
| **Capture** | `#persona-product-manager` | — | Fast, low-ceremony — no specialist lens needed |
| **Shape** | `#persona-product-manager` | `#persona-subrole-business-analyst` | Requirements decomposition, ambiguity detection, gap identification |
| **Evaluate** | `#persona-product-manager` | `#persona-subrole-financial-analyst` | Value scoring, cost-of-not-doing, investment framing |
| **Scope** | `#persona-process-designer` | `#persona-subrole-resource-planner` | WBS-like boundary setting, effort estimation, dependencies |
| **Approve** | `#persona-product-manager` | `#persona-subrole-risk-analyst` | Risk-aware go/no-go: challenge assumptions, assess feasibility risks |
| **Route & Handoff** | `#persona-product-manager` | `#persona-subrole-change-manager` | Impact assessment (big vs. small change), stakeholder/adoption lens |

### Domain Detection (Additional Supporting Lens)

When the idea's **subject domain** emerges during shaping, the sub-role above may be supplemented or swapped for a domain-specific sub-role at the Approve and Route stages (capped at primary + one sub-role per the loading guide):

| Idea subject | Sub-role to prefer | Primary fallback |
|---|---|---|
| Architecture, system boundaries, decomposition | `#persona-subrole-systems-engineer` | `#persona-cto-architect` |
| Security, identity, trust boundaries | `#persona-subrole-security-architect` | `#persona-cto-architect` |
| Data modelling, schema, storage | `#persona-subrole-data-architect` | `#persona-cto-architect` |
| API / integration design | `#persona-subrole-api-designer` | `#persona-cto-architect` |
| CI/CD, workspace, repo structure | `#persona-subrole-workspace-architect` | `#persona-devops-platform-engineer` |
| Governance, compliance, hooks | `#persona-subrole-audit-specialist` | `#persona-compliance-governance` |
| Test strategy, QA, validation | _(no sub-role)_ | `#persona-qa-test-engineer` |
| Licensing, IP, commercial strategy | _(no sub-role)_ | `#persona-ip-licensing-counsel` |
| Project management, PMO governance | `#persona-subrole-change-manager` | `#persona-pmo-project-manager` |

**Resolution rule:** Lead = stage default; Sub-role = stage-specific (table above) OR idea's domain (when more relevant at Approve/Route); capped at primary + one sub-role. See `.kiro/steering/persona-loading-guide.md` → "Dynamic / Stage-Based Selection" for full resolution logic.

---

## MANDATORY: State Management

The workflow maintains state across sessions via `pdlc-ws/ideas/ilc-state.md` (the shared marker, kept flat at the fixed output root — one active idea at a time).

At workflow start:
1. Check if `ilc-state.md` exists at `pdlc-ws/ideas/`.
2. If YES → load state, confirm position with the user, resume from the last completed stage.
3. If NO → fresh start; create the state file when the Capture stage begins.

State tracks: current stage, completed stages + timestamps, idea identity (name, Register ID, proposed type, domain), evaluation score (once scored), routing decision (once approved), pending decisions, depth level. **CRITICAL: update the state file immediately after EVERY stage completion.** Full spec: `common/session-continuity.md`.

---

## MANDATORY: Registers

Two registers are created at first use (Capture) and maintained in real-time (not batched), each entry sequentially numbered and never deleted:
**Idea Register** (every idea: status, score, decision, dates) · **Decision Log** (every go/no-go, routing, and park/reject rationale).

The Idea Register lives flat at `pdlc-ws/ideas/Idea_Register.md` (shared across all ideas); the Decision Log lives in the shared governance spine `pdlc-ws/ideas/management_framework/`. Templates: `templates/idea-register.md`, `templates/management-framework.md`.

---

## MANDATORY: Question Format

When asking questions at any stage, use the structured `### Q-{nn}` block: Context → Options (a/b/c) → Recommended option → Rationale → "Your Decision: _[awaiting input]_". Always provide a recommended answer with rationale; the user may accept, choose another, or propose an alternative. Log every confirmed decision in the Decision Log immediately. Full rules + examples: `common/question-format-guide.md`.

---

## MANDATORY: Output Folder Structure

**The output root is ALWAYS `pdlc-ws/ideas/` relative to the workspace root** — a deterministic, non-negotiable path. The user is **NOT** asked where to place output (aligns with `OUTPUT_AND_STATE_CONTRACT.md` §4 and the Always-On Rule). Two principles: **shared artifacts stay flat** (state marker, Idea Register, governance spine — cross-idea, never move, so successors detect them at the fixed root), and **per-idea artifacts live in a per-idea subfolder** keyed by the idea's stable Register ID (never by status).

```
pdlc-ws/ideas/                              ← FIXED output root (workspace-root-relative)
├── ilc-state.md                            ← shared marker (one active idea at a time)
├── Idea_Register.md                        ← shared funnel view (status at a glance)
├── management_framework/                   ← shared governance spine (flat)
│   ├── MANAGEMENT_FRAMEWORK.md
│   ├── Decision_Log.md                     ← all go/no-go + routing decisions
│   └── Lessons_Learned.md
└── {NNN}-{idea-slug}/                      ← per-idea subfolder, keyed by zero-padded Register ID
    ├── Idea_Statement.md                   ← working doc (Shape)
    ├── {NNN}-{idea-slug}_GoNoGo_Decision_Record.md   ← always (approve/park/reject)
    ├── {NNN}-{idea-slug}_Approved_Idea_Brief.md      ← IF route = new-project
    ├── {NNN}-{idea-slug}_Change_Request_Brief.md     ← IF route = change-request
    └── {NNN}-{idea-slug}_Feature_Brief.md            ← IF route = feature
```

- `{NNN}` = zero-padded Register ID (`001`, …) — a **stable** domain key; the subfolder is created at Capture and **never renamed** for status changes (status lives in the Register + each artifact's `Status` field, not the folder name).
- **Successor detection is preserved:** successors scan for `ilc-state.md` at `pdlc-ws/ideas/`; the state file's `Brief File` field carries the relative path to the brief, and the Idea Register stores each idea's `Folder` path — consumers resolve the brief from the marker, never guessing the folder.
- **Brownfield exception:** if AI-ILC output already exists in a non-standard (older flat) location, detect it on first run, inform the user, continue in `pdlc-ws/ideas/`, and never force-move existing files.
- **Provenance:** per `NAMING_AND_OWNERSHIP.md` §5.2, per-idea artifacts carry front-matter (`generatedBy: AI-ILC`, `ownership: user`) and a `Status` field — classification lives in metadata, not the path.

---

## MANDATORY: Two-Source Evaluation Model

The Evaluate stage scores against a **two-source model**: a **default baseline rubric** (built in — 7 universal criteria that work for any idea in any domain; functional even with no customization) plus optional **enterprise customization** (the org can override criteria, weights, or thresholds on a per-criterion basis). Resolution: enterprise custom overrides baseline per-criterion; baseline stands where the enterprise is silent; full baseline applies when there is no customization at all. Full rubric, criteria, and scoring bands: `idea-lifecycle/evaluate.md`.

---

## MANDATORY: Chain Contract

AI-ILC is contract-aware — it is the optional pre-stage (front door) of the AI-* chain.

### I Read (Predecessor: None)
AI-ILC is the optional first entry point. It accepts raw ideas in any format — verbal description, one-liner/subject line, document (brief/proposal/email/feature request), or an existing backlog item to elevate. No input marker file; no predecessor package.

### I Produce (Successors: AI-PILC / AI-POLC / AI-FLO / AI-DLC v1 / AI-PPM)
- **Marker:** `ilc-state.md`. **Output:** `pdlc-ws/ideas/` (fixed; shared artifacts flat, per-idea artifacts under `{NNN}-{idea-slug}/`).
- **Guaranteed output** (relative to marker): `ilc-state.md` (✅ always), Idea Register entry (✅ always), Decision Log entry (✅ always), `{NNN}-{slug}/*_GoNoGo_Decision_Record.md` (✅ always). **Conditional briefs:** `*_Approved_Idea_Brief.md` when `Route = new-project`; `*_Change_Request_Brief.md` when `Route = change-request`; `*_Feature_Brief.md` when `Route = feature`. Exactly one brief is produced per approved idea, keyed off the route.
- **State fields successors read:** `Status` (must be `Routed` for handoff — terminal success), `Route` (`new-project` / `change-request` / `feature` / `portfolio-inform`), `Brief File` (relative path to the brief in the per-idea subfolder), `Depth Level`, `Idea Name`, `Project ID` (if targeting an existing project — for AI-PPM correlation).

### Successor detection (forward-compatible)
- **`new-project`:** AI-FLO dispatches to AI-PILC (if available) → fallback: AI-PILC directly reads `ilc-state.md` and consumes the Approved Idea Brief via Mode E intake.
- **`change-request`:** AI-PILC consumes the Change Request Brief through its change management registers.
- **`feature`:** AI-POLC consumes the Feature Brief (if available) → fallback: AI-DLC v1 backlog.
- **`portfolio-inform`:** AI-PPM is notified for portfolio awareness (if available) → fallback: informational no-op.

> **Forward-compatibility:** the `Route` field carries the *intent*; the consuming package resolves the *target* based on what's installed. Routing never breaks if AI-FLO/AI-POLC/AI-PPM are absent — it falls through to the direct successor.

### Contract Principles
Detection by marker (not folder name) · fixed output root (`pdlc-ws/ideas/`) · graceful standalone (every successor works without AI-ILC) · **additive to AI-PILC** (the AI-ILC brief is an additional optional intake mode, OR-input) · **forward-compatible routing** (routes may target packages that don't exist yet; fallback always succeeds) · single-project context (v1.0) · **AI-ADLC is never a direct target** (architecture rework flows THROUGH AI-PILC change management) · **AI-POLC preferred for features** (AI-DLC v1 is the fallback OR-input).

### Portfolio Connector & Downstream Signal
On `new-project`, AI-ILC may also set `portfolio-inform` so AI-PPM (if present) registers the project; absent AI-PPM, it is a no-op. Multi-project routing is a v1.1+ capability (will consume AI-FLO). **Downstream signal:** none — the brief is a one-time handoff. If the user modifies the idea after the successor starts, they re-initiate from the updated brief.

---

# WORKFLOW STAGE INDEX

Six stages, one governed pipeline. Each stage produces its primary artifact behind an approval gate. **Load the stage's detail file before executing it** — the detail file holds the full step-by-step instructions, depth adaptation, gate, transition message, and edge cases.

| # | Stage | Exec | Lead persona · sub-role | Primary output / gate | Detail file |
|:-:|-------|------|-------------------------|-----------------------|-------------|
| 1 | **Capture** | ALWAYS | Product/Innovation Mgr | Idea registered + state file · gate: capture summary confirmed | `idea-lifecycle/capture.md` |
| 2 | **Shape** | ALWAYS (adaptive) | PM · business-analyst | Idea Statement (working doc) · gate: shaped idea approved | `idea-lifecycle/shape.md` |
| 3 | **Evaluate** | ALWAYS (adaptive) | PM · financial-analyst | Score /35 + Value Analysis · gate: Proceed/Park/Reject confirmed | `idea-lifecycle/evaluate.md` |
| 4 | **Scope** | CONDITIONAL (if Proceed) | process-designer · resource-planner | In/out + effort estimate · gate: scope agreed | `idea-lifecycle/scope.md` |
| 5 | **Approve** | CONDITIONAL (if Scoped) | PM · risk-analyst | Go/No-Go Decision Record · gate: explicit APPROVE/PARK/REJECT | `idea-lifecycle/approve.md` |
| 6 | **Route & Handoff** | CONDITIONAL (if Approved) | PM · change-manager | Brief (Approved Idea / Change Request / Feature) · no forward gate (final) | `idea-lifecycle/route-handoff.md` |

**Stage gates:** never auto-progress past a gate without explicit user approval. Park/Reject at Evaluate or Approve is a valid, governed early exit (clean close with audit trail). Depth changes are user-controllable at any gate — see `common/session-continuity.md`.

---

## Post-Workflow: Agent Installation (ALWAYS — automatic, first run only ·)

After the AI-ILC workflow completes its first full run in a workspace, install the governance agent so the user can validate future idea briefs independently — automatic, no user interaction. This installs `idea-quality-agent` (ILC-AG-01) and activates the `IQC__` shortcut. Full installation logic (agent file, shortcut block, registry, guide, when-to-install, self-sufficiency rule): `idea-lifecycle/agent-installation.md`.

---

## Key Principles & Checkpoint Enforcement

The behavioral principles (every idea gets a fair hearing · go/no-go always explicit · context carries forward · the user decides and the AI advises · audit trail from day one · standalone is first-class · dynamic expertise · parked is not dead) and the checkpoint rules (never pass a gate without approval · update `ilc-state.md` after every stage · log every decision in real-time with ISO-8601 timestamps) are defined in `common/process-overview.md`. Apply them throughout. Provenance front-matter (`generatedBy: AI-ILC`, `ownership: user`) on all output artifacts per `NAMING_AND_OWNERSHIP.md` §5.2.

---

## Gate Contract

> Conforms to `GATE_PROTOCOL.md` protocolVersion 1.2.0 · interfaceVersion 1.0

### Gate-Out — What AI-ILC GUARANTEES When Complete

```yaml
emits-type: idea-decision@1
visibility: internal
marker: ilc-state.md
payloadRoot: pdlc-ws/projects/{projectId}/ilc/
guarantees:
  - status == complete
  - ideaId
  - projectId
  - decisionOutcome           # approved | rejected | deferred | merged
  - ideaBrief                 # Approved Idea Brief / Feature Brief / CR Brief present
  - lifecycleDisposition      # new-project | feature | change-request
```

### Gate-In — What AI-ILC REQUIRES to Start

```yaml
consumes:
  - type: capability-input@^1       # satisfiable externally (e.g., EAFLC capability roadmap)
    optional:  [capabilityContext, strategicAlignment]
on-missing-all: standalone    # accepts raw idea from user (P4)
strictness-default: warn
```

> No type-specific mandatory payload — AI-ILC starts from a raw idea. Universal floor (status==complete + id) enforced by marker integrity (GATE_PROTOCOL §18).

### Visibility Note

- `idea-decision` is `internal` — consumed only by AI-PILC, AI-POLC, and AI-PPM within PDLC.
- `capability-input` is the **external seam-in** — declared in `FAMILY_INTERFACE.md` Tier 1.

---

*AI-ILC v1.0.0 | Created: 2026-06-12 | Author: Maheri | From raw idea to a defensible, routed go/no-go decision.*
