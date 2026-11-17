<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Peer Input Reading Guide

## Purpose

This document defines HOW AI-DWG reads, locates, and parses its **peer inputs**: Architecture Package (AP from AI-ADLC), Product Backlog Package (PBP from AI-POLC), and UX Design Package (UXP from AI-UXD). It covers detection strategy, file identification, content extraction patterns, and error handling when inputs are incomplete or use non-standard structures.

AI-DWG accepts **any non-empty subset** of {ADLC, POLC, UXD} as a *capability* — each input unlocks its own output cluster, and absence of an input means that cluster is not generated. However, the **default start gate waits for all three** peers (AP + PBP + UXP). Starting with fewer than three is a **user-approved exception with acknowledged reduced coverage**, never the silent default (mirrors the AI-FLO fan-in gate; resolves OI-067).

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS activity, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Read the AP with stakeholder empathy — understand WHY decisions were made, not just WHAT was decided
- Validate completeness from a requirements perspective — are there gaps between stated goals and documented architecture?
- Extract implicit business rules that the architect may have embedded in technical constraints
- Map quality attributes back to business outcomes (e.g., "99.9% uptime" = "customer SLA commitment")
- Question assumptions — if an artifact seems incomplete, frame clarification questions in business terms

### Anti-Patterns for This Activity
- Do NOT invent architecture decisions when the AP is silent — flag as missing, never assume
- Do NOT interpret ambiguous AP content optimistically — ambiguity means "ask the user"
- Do NOT skip validation steps because the AP "looks complete" — verify structure AND content

### Quality Check
A good output from this activity sounds like:
- "AP scan complete — 10/10 required artifacts found. Multi-tenancy document present (conditional generation triggered). Extension `ddd-tactical` active — enrichment mappings will apply."
- "Architecture Vision contains 6 principles but no explicit constraints table — flagging for user: should I proceed with principles-only or do constraints exist elsewhere?"

---

## Step 1: Locate Peer Inputs

AI-DWG scans for **three marker files** simultaneously. At least one MUST be found. If none are found, ask the user to point to their input package(s).

### Detection Strategy (All Three Peers — Parallel Scan)

```
FOR EACH peer marker:
   adlc-state.md  (AP — tech cluster)
   polc-state.md  (PBP — product cluster)
   uxd-state.md   (UXP — UX cluster)

   1. User provides path explicitly → use it
   2. Scan common locations for the marker file:
      → ./architecture/, ./docs/architecture/ (ADLC)
      → ./backlog/, ./product/ (POLC)
      → ./design/, ./ux/ (UXD)
      → ../ (sibling folder for any)
      → ./ (current directory)
   3. Not found → peer is ABSENT for this run (cluster skipped)

AFTER scan:
   IF zero markers found → BLOCK; ask user: "Where are your design packages?"
   IF 1-2 markers found → DEFAULT GATE NOT MET → show peer-status table +
                          reduced-coverage warning → require explicit user
                          approval to proceed (exception), else wait/hold
   IF all 3 found → default gate met → proceed with full generation (all clusters)
```

### Default Start Gate (All Three Peers)

AI-DWG's **default gate waits for all three** peers — AP (AI-ADLC), PBP (AI-POLC), and UXP (AI-UXD). Before generating, DWG displays each peer's status:

```
🔎 PEER READINESS — AI-DWG start gate (default = all three)

| Peer | Marker | Status |
|------|--------|--------|
| AI-POLC (PBP) | polc-state.md | {✅ Complete / ⏳ In Progress / ❌ Absent} |
| AI-UXD (UXP)  | uxd-state.md  | {✅ Complete / ⏳ In Progress / ❌ Absent} |
| AI-ADLC (AP)  | adlc-state.md | {✅ Complete / ⏳ In Progress / ❌ Absent} |

Gate: {✅ ALL READY — proceed | ⚠️ {n}/3 — exception requires approval}
```

When all three are present → proceed. When fewer than three → DWG does **not** start silently; it surfaces the status table, the Quality-Impact Disclosure below, and requires explicit user approval (acknowledged reduced coverage). If AI-FLO is present, this gate is also enforced upstream at the FLO fan-in; if AI-FLO is absent, **AI-DWG enforces the gate itself** at intake.

### Marker Files Summary

| Marker | Producer | Cluster it enables | If absent |
|--------|----------|-------------------|-----------|
| `adlc-state.md` | AI-ADLC | Tech steering + src structure + technical-environment.md | Tech cluster skipped; no src scaffolding |
| `polc-state.md` | AI-POLC | vision.md + DoD + planning + scope-and-risks | Product cluster skipped; no vision document |
| `uxd-state.md` | AI-UXD | design-system.md + frontend-standards + ui-implementation-spec | UX cluster skipped; no design system |

### Quality-Impact Disclosure (Mandatory When <3 Inputs Found)

When fewer than all three peer inputs are detected, the **default gate is not met**. DWG MUST present the following BEFORE proceeding, and proceeding is a user-approved exception (not the default):

```
⚠️ QUALITY-IMPACT DISCLOSURE — default gate (all three) NOT met

Present inputs: {list of found markers + paths}
Absent inputs: {list of missing markers}

Impact of absent inputs:
• {ADLC absent}: Cannot produce tech steering (13+ files), src folder structure,
  or technical-environment.md. AI-DLC v1 will lack technical constraints and module layout.
• {POLC absent}: Cannot produce vision.md, DEFINITION_OF_DONE.md with product acceptance bar,
  or scope-and-risks.md. AI-DLC v1 will lack product context and success metrics.
• {UXD absent}: Cannot produce design-system.md, ui-implementation-spec.md,
  or frontend accessibility baseline. AI-DLC v1 will lack UX governance and design tokens.

Recommended: WAIT for the missing peer(s) — the default gate is all three.
Proceed with {n}/3 inputs anyway? (Acknowledged reduced coverage — user must explicitly approve)
```

**The user MUST explicitly approve** before DWG continues with a partial trio. This is acknowledged degradation (a deliberate exception to the all-three default gate), not silent degradation.

---

## Step 1b: ADLC-Specific State Reading (If ADLC Present)

When `adlc-state.md` is found, ALL other AP files are located relative to its directory. This marker is the anchor for the tech cluster.

**Critical fields to extract from `adlc-state.md`:**

| Field | Used For |
|-------|----------|
| `Output Structure` | Determines naming pattern: `numbered` (01_*.md) or `phase-folder` (foundation/, design/, etc.) |
| `Enabled Extensions` | Triggers extension-enrichment mappings (DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags) |
| `Completed Stages` | Confirms AP completeness — flags if stages are missing |
| `ADR Register` | Inventory of all architecture decisions for cross-referencing |
| `System Name` | Used as default project display name if user doesn't override |
| `Project ID` | Immutable family-wide correlation key; embedded in workspace metadata |

### Standalone/Manual Mode (No `adlc-state.md`)

If ADLC marker is absent but the user explicitly points to architecture documentation:
- Ask user to identify which documents map to which AP artifact
- Proceed without extension detection (no state file to read)
- Tech cluster still generates from the manually-mapped documents

---

## Step 1c: Cross-Input Conflict Surfacing (When 2+ Inputs Present)

When two or more peer inputs are detected, DWG MUST scan for contradictions before proceeding. This is a **hard gate** — generation does not begin until all conflicts are resolved.

**Context:** ADLC, POLC, and UXD are designed to own distinct domains (tech / product / UX). Overlap between them is an **anomaly** — something went wrong upstream. DWG surfaces it with root-cause analysis; the user resolves it.

### What to Check

| Overlap Zone | Sources to Compare | Conflict = |
|---|---|---|
| Frontend framework | ADLC Tech Stack vs. UXD design-system component library | Different frameworks for same UI layer |
| Quality thresholds | ADLC quality attributes vs. POLC DoD metrics | Contradictory performance/coverage targets |
| Accessibility level | UXD a11y baseline vs. ADLC compliance constraints | Different WCAG levels specified |
| User model | UXD personas vs. POLC user segments | Describing different user populations |
| Domain terminology | ADLC bounded contexts vs. POLC product vocabulary | Same concept, different names |

### Protocol

1. **Detect:** Compare overlapping fields across present inputs
2. **Classify:** Is it a true contradiction (different answers to same question) or complementary content (different inputs filling different aspects)?
3. **If contradiction:** Surface with root-cause analysis + suggested correction. Present options: fix upstream / override via ADR / cancel.
4. **Hard gate:** DWG does NOT proceed until each contradiction is resolved.
5. **If no contradictions:** Proceed silently — don't report "no conflicts" (noise).

### Anti-Pattern: Over-Detection

Not every shared topic is a conflict. Examples of **complementary** (NOT conflicting) content:
- ADLC specifies "React 18" AND UXD provides React component inventory → complementary
- POLC defines acceptance format AND ADLC defines quality attributes → different granularity, not contradiction
- UXD provides design tokens AND ADLC specifies CSS methodology → different layers

Only flag when two inputs provide **contradictory answers to the same question.**

For full conflict-surfacing protocol including presentation format, see `core-generator.md` → "Input Selection & Conflict Surfacing" section.

---

## Step 2: Identify AP Files (When ADLC Present)

### Two Naming Patterns

AI-ADLC lets users choose between numbered documents and phase folders. AI-DWG must handle both. **This step only executes when `adlc-state.md` was found in Step 1.**

**Pattern A: Numbered Documents (Default)**

| # | File Name Pattern | Maps To |
|---|------------------|---------|
| 01 | `*Architecture_Vision*` | Architecture Vision & Principles |
| 02 | `*System_Context*` or `*C4L1*` | System Context (C4 Level 1) |
| 03 | `*Container*` or `*C4L2*` | Container Diagram (C4 Level 2) |
| 04 | `*Technology_Stack*` | Technology Stack |
| 05 | `*MultiTenancy*` or `*Multi_Tenancy*` | Multi-Tenancy Architecture (conditional) |
| 06 | `*Security*Identity*` or `*Security*` | Security & Identity Architecture |
| 07 | `*Data_Architecture*` | Data Architecture |
| 08 | `*API_Architecture*` | API Architecture |
| 09 | `*Integration*` | Integration Architecture |
| 10 | `*Infrastructure*` or `*Deployment*` | Infrastructure & Deployment |
| 11 | `*Component*` or `*C4L3*` | Component Design (C4 Level 3) |
| — | `Architecture_Workbook*` | Architecture Workbook |
| — | `*PACKAGE_README*` or `*README*` | Package README |
| — | `ADR/` folder | Architecture Decision Records |

**Pattern B: Phase Folders**

| Folder | Contains |
|--------|----------|
| `foundation/` | Architecture Vision, (may include requirements summary) |
| `decomposition/` | System Context (C4 L1), Container Diagram (C4 L2) |
| `decisions/` | Technology Stack, Multi-Tenancy, Security Architecture |
| `design/` | Data Architecture, API Architecture, Integration, Infrastructure, Component Design |
| `ADR/` | Architecture Decision Records |

**Detection logic:**
1. Read `adlc-state.md` → `Output Structure` field
2. If `numbered` → scan for numbered files using Pattern A
3. If `phase-folder` → scan for folders using Pattern B
4. If field missing → try Pattern A first (default), fall back to Pattern B

---

## Step 3: Validate AP Completeness (When ADLC Present)

Before generating the tech cluster, verify all required ADLC artifacts exist:

### Required Artifacts (Generation fails without these)

| Artifact | How to Verify | If Missing |
|----------|--------------|-----------|
| Architecture Vision | File exists + contains "Principles" section | BLOCK — ask user |
| System Context (C4 L1) | File exists + contains external actors/systems | BLOCK — ask user |
| Container Diagram (C4 L2) | File exists + contains container list | BLOCK — ask user |
| Technology Stack | File exists + contains technology selections table | BLOCK — ask user |
| Security Architecture | File exists + contains authentication/authorization sections | BLOCK — ask user |
| Data Architecture | File exists + contains entity/schema information | BLOCK — ask user |
| API Architecture | File exists + contains REST conventions/standards | BLOCK — ask user |
| Integration Architecture | File exists + contains external system patterns | BLOCK — ask user |
| Infrastructure & Deployment | File exists + contains deployment topology | BLOCK — ask user |
| Component Design (C4 L3) | File exists + contains module decomposition | BLOCK — ask user |
| ADR folder | Folder exists + contains at least 1 ADR | WARN — generate without cross-refs |

### Optional Artifacts (Enrich generation if present)

| Artifact | If Present | If Absent |
|----------|-----------|----------|
| Multi-Tenancy Architecture | Generate `multi-tenancy.md` steering file | Skip — single-tenant assumed |
| Architecture Workbook | Extract open items for `scope-and-risks.md` | Generate scope from other sources |
| Package README | Use as summary reference | Derive summary from individual docs |

### Completeness Report

After scanning, present to user:

```
📋 Architecture Package Scan Results

Location: {path}
Structure: {numbered | phase-folder}
Extensions active: {list or "none"}

Required artifacts:
  ✅ Architecture Vision — found
  ✅ System Context (C4 L1) — found
  ✅ Container Diagram (C4 L2) — found
  ✅ Technology Stack — found
  ✅ Security Architecture — found
  ✅ Data Architecture — found
  ✅ API Architecture — found
  ✅ Integration Architecture — found
  ✅ Infrastructure & Deployment — found
  ✅ Component Design (C4 L3) — found
  ✅ ADR folder — found ({n} ADRs)

Optional artifacts:
  {✅|❌} Multi-Tenancy Architecture
  {✅|❌} Architecture Workbook
  {✅|❌} Package README

Status: {READY TO GENERATE | MISSING REQUIRED: {list}}
```

---

## Step 4: Extract Content from AP Artifacts (When ADLC Present)

### What to Extract Per Artifact

For each AP document, extract these specific elements that drive workspace generation. **This step only executes for the tech cluster (ADLC present).**

#### From Architecture Vision

| Extract | Used In |
|---------|---------|
| Vision statement (1-2 sentences) | `workspace-rules.md` header |
| Guiding Principles (P1-Pn) | `workspace-rules.md` rules, `architecture-principles.md` |
| Architectural Constraints table | `workspace-rules.md` DON'T rules |
| Quality Attributes with priorities | `testing-strategy.md`, `DEFINITION_OF_DONE.md` |

#### From Technology Stack

| Extract | Used In |
|---------|---------|
| Language/runtime per container | `tech-stack.md`, `.gitignore`, `docker-compose.yml` |
| Framework selections | `coding-standards.md`, `naming-conventions.md` |
| Database technology | `database-rules.md`, `docker-compose.yml` |
| Caching layer | `tech-stack.md` |
| Message queue | `tech-stack.md`, `docker-compose.yml` |
| Monitoring/observability stack | `observability-*.md` |
| UI framework (if any) | `frontend-standards.md` |

#### From System Context (C4 L1)

| Extract | Used In |
|---------|---------|
| System boundary definition | `scope-and-risks.md` |
| External actors list | `scope-and-risks.md`, `security-rules.md` |
| External systems list | `scope-and-risks.md`, integration context |
| Communication protocols | `api-standards.md` |

#### From Container Diagram (C4 L2)

| Extract | Used In |
|---------|---------|
| Container list (deployable units) | Top-level folder structure |
| Container technologies | `docker-compose.yml` |
| Data stores | `database-rules.md`, `docker-compose.yml` |
| Inter-container communication | `api-standards.md`, `resilience-standards.md` |
| UI containers (if any) | Triggers `frontend-standards.md` |

#### From Component Design (C4 L3)

| Extract | Used In |
|---------|---------|
| Module list per container | Folder structure (src-level) |
| Module responsibilities | `module-structure.md` |
| Module dependencies/rules | `module-structure.md` |
| Bounded contexts | `domain-context.md` |
| Core entities per context | `domain-context.md`, `naming-conventions.md` |
| Cross-cutting concerns | `error-handling.md`, `observability-logging.md` |
| Component ownership | `CODEOWNERS` |

#### From Security Architecture

| Extract | Used In |
|---------|---------|
| Authentication methods | `security-rules.md` |
| Token strategy | `security-rules.md` |
| RBAC model | `security-rules.md` |
| Encryption approach | `security-rules.md`, `observability-sensitive.md` |
| Audit logging strategy | `observability-logging.md` |
| OWASP mitigations | `security-rules.md` |
| Sensitive data categories | `observability-sensitive.md` |

#### From API Architecture

| Extract | Used In |
|---------|---------|
| REST conventions | `api-standards.md` |
| URL patterns | `api-standards.md`, `naming-conventions.md` |
| Error response format | `api-standards.md`, `error-handling.md` |
| Versioning strategy | `api-versioning.md` (conditional) |
| Pagination approach | `api-standards.md` |
| Rate limiting | `api-standards.md` |

#### From Data Architecture

| Extract | Used In |
|---------|---------|
| Data model strategy (DDD/ERD) | `database-rules.md` |
| Schema management approach | `database-rules.md` |
| Multi-tenant scoping method | `database-rules.md`, `multi-tenancy.md` |
| Caching strategy | `database-rules.md` |
| Search index approach | `database-rules.md` |

#### From Integration Architecture

| Extract | Used In |
|---------|---------|
| Integration patterns per external system | `resilience-standards.md` |
| Failure handling (retry, circuit breaker) | `resilience-standards.md` |
| Event-driven patterns | `module-structure.md` |
| Integration count (triggers conditional) | Conditional: `resilience-standards.md` |

#### From Infrastructure & Deployment

| Extract | Used In |
|---------|---------|
| Container/orchestration strategy | `docker-compose.yml` |
| Observability stack (metrics, logging, tracing) | `observability-*.md` |
| Branching/CI strategy | `git-workflow.md` |
| Scaling approach | `performance-standards.md` |
| HA/DR approach | `scope-and-risks.md` |

#### From ADRs

| Extract | Used In |
|---------|---------|
| ADR titles and decisions | Cross-referenced in relevant steering files |
| Technology choices with rationale | `tech-stack.md` rationale sections |
| Pattern decisions | Relevant steering files (e.g., ADR about event-driven → module-structure) |

---

## Step 5: Detect Active Extensions (When ADLC Present — AI-ADLC v1.1+)

### Reading Extension State

From `adlc-state.md`, locate the `Enabled Extensions` field:

```markdown
## Enabled Extensions
- ddd-tactical (activated at Stage 12)
- microservices (activated at Stage 5)
- resilience-patterns (activated at Stage 11)
```

### Extension Impact on Reading

When an extension is active, the AP contains ADDITIONAL content that normal (non-extension) APs don't have:

| Extension Active | Look For (additional AP content) |
|-----------------|----------------------------------|
| **DDD Tactical** | Aggregate boundary definitions in C4 L3; Domain Events catalog; ACL specifications; Value Object identification |
| **Microservices** | Service mesh configuration in Infrastructure; Distributed tracing design; Saga/choreography patterns in Integration; Schema registry in API |
| **BFF Pattern** | BFF container in C4 L2; Aggregation rules; Client-specific shaping rules |
| **Event Sourcing/CQRS** | Event store design in Data Architecture; Projection definitions; Read model specifications; Snapshot strategy |
| **Resilience Patterns** | Extended failure handling in Integration (bulkhead, graceful degradation); Circuit breaker configuration per integration |
| **Feature Flags** | Flag architecture in Component Design or Technology Stack; Rollout strategy; Flag lifecycle rules |

### What to Do with Extension Content

1. Extract the extension-specific content from the AP documents where it appears
2. Load the corresponding extension-enrichment mapping file (`mapping/extension-{name}-enrichment.md`)
3. Follow enrichment rules to add extension-specific content to relevant steering files
4. Override conditional triggers where the extension demands it (e.g., Microservices → always generate `resilience-standards.md`)

---

## Step 6: Build the Generation Context

After reading all **present** peer inputs, compile a **generation context** — a mental model of what's available and what can be produced:

```
GENERATION CONTEXT:
├── Peer Input Inventory
│   ├── ADLC: {present/absent} → {path if present}
│   ├── POLC: {present/absent} → {path if present}
│   ├── UXD:  {present/absent} → {path if present}
│   └── Quality-impact: {disclosed and approved / full coverage}
│
├── System Identity (assembled from whatever is present)
│   ├── Name: {from adlc-state, or polc project name, or user config}
│   ├── Vision: {Architecture Vision if ADLC | Product Vision if POLC | deferred if UXD-only}
│   └── Type: {monolith | modular-monolith | microservices | hybrid — if ADLC present}
│
├── Technology Profile (IF ADLC present)
│   ├── Primary language: {e.g., TypeScript}
│   ├── Framework: {e.g., NestJS}
│   ├── Database: {e.g., PostgreSQL}
│   ├── Cache: {e.g., Redis}
│   ├── Queue: {e.g., BullMQ}
│   └── Frontend: {e.g., React / none}
│
├── Product Profile (IF POLC present)
│   ├── Product vision statement: {1-2 sentences}
│   ├── Success metrics: {key KPIs}
│   ├── MVP scope: {IN / OUT boundaries}
│   └── Prioritization model: {WSJF / MoSCoW / etc.}
│
├── UX Profile (IF UXD present)
│   ├── Design system: {token set + component inventory}
│   ├── Accessibility target: {WCAG level}
│   ├── Personas: {list — also feeds Vision if POLC present}
│   └── User journeys: {key flows}
│
├── Complexity Indicators (IF ADLC present)
│   ├── Module count: {n}
│   ├── Integration count: {n}
│   ├── Multi-tenant: {yes/no}
│   ├── Extensions active: {list}
│   └── Depth level: {minimal / standard / comprehensive}
│
├── Principles (Rules to Encode — IF ADLC present)
│   ├── P1: {name} — {statement}
│   ├── P2: {name} — {statement}
│   └── ...
│
├── Constraints (DON'T Rules — IF ADLC present)
│   ├── C1: {constraint} — source: {where it came from}
│   └── ...
│
├── Modules (Folder Structure — IF ADLC present)
│   ├── {module-1}: {responsibility}
│   ├── {module-2}: {responsibility}
│   └── ...
│
└── Cluster Generation Plan
    ├── Tech cluster: {yes/no — ADLC present?}
    ├── Product cluster: {yes/no — POLC present?}
    ├── UX cluster: {yes/no — UXD present?}
    └── Conditional Triggers (IF ADLC):
        ├── multi-tenancy.md: {yes/no — reason}
        ├── resilience-standards.md: {yes/no — reason}
        ├── observability-tracing.md: {yes/no — reason}
        ├── performance-standards.md: {yes/no — reason}
        ├── workflow-engine.md: {yes/no — reason}
        ├── frontend-standards.md: {yes/no — reason}
        ├── api-versioning.md: {yes/no — reason}
        ├── event-sourcing.md: {yes/no — reason}
        └── feature-flags.md: {yes/no — reason}
```

This context drives ALL subsequent mapping and generation. It's the "compiled understanding" of the project from whichever inputs are present.

---

## Error Handling

| Situation | Response |
|-----------|----------|
| `adlc-state.md` not found | Ask user for AP location. If still not found → manual mode (user maps docs) |
| Required artifact missing | Present completeness report. Ask: "Generate with assumptions?" or "Wait for artifact?" |
| Artifact exists but has unexpected format | Attempt to extract what's available. Mark sections with `<!-- partial: could not extract {what} -->` |
| `adlc-state.md` shows incomplete stages | Warn user: "AP appears incomplete (stages {list} not completed). Generate anyway?" |
| Conflicting information between AP docs | Flag conflict to user: "Technology Stack says X but Infrastructure says Y. Which is correct?" |
| Unknown technology (not in template library) | Generate generic patterns. Mark with `<!-- customize: {technology}-specific rules needed -->` |
| Extension listed in state but no extension content in AP | Warn: "Extension {name} was active but its expected content wasn't found in AP. Generating without enrichment." |

---

---

## Step 7: Accessibility Baseline Extraction & Relay (When UXD Present)

When `uxd-state.md` is found, extract the accessibility baseline and prepare it for two consumers:

### What to Extract

From UXP Accessibility Baseline document:
- WCAG target level (e.g., 2.1 AA, 2.2 AAA)
- Specific contrast ratio requirements
- Touch target minimums
- Keyboard navigation requirements
- Screen reader testing expectations
- Motion/animation policy (prefers-reduced-motion)
- Focus indicator requirements
- ARIA usage guidelines

### Where It Goes (Two Destinations)

| Destination | What Gets Relayed | How |
|---|---|---|
| **`design-system.md`** (DS-A11Y rules) | Full accessibility governance rules — every specific requirement becomes a DS-A11Y-NN rule | Via `mapping/uxd-to-design-system.md` — Accessibility Governance section |
| **`frontend-standards.md`** (FE-A11Y rules) | Enriched/overridden accessibility rules — specific WCAG requirements replace generic AP-derived rules | Via `mapping/containers-to-frontend.md` — UXD enrichment of FE-A11Y section |
| **AI-GCE downstream signal** | Accessibility baseline availability — AI-GCE derives `accessibility-compliance` enforcement hooks from DS-A11Y rules | Via downstream signal: `accessibility-baseline-available` event |

### Signal to AI-GCE

After generation (if UXD present), include accessibility baseline in the downstream signal:

```
⚡ DOWNSTREAM SIGNAL (ACCESSIBILITY BASELINE)
   From: AI-DWG
   To: AI-GCE
   Event: accessibility-baseline-available
   Source: AI-UXD Accessibility Baseline (relayed via DWG)
   WCAG Target: {level}
   Steering file: rules/design-system.md (DS-A11Y-* rules)
   Action required: Derive accessibility-compliance hooks from DS-A11Y rules
```

### Relay Logic

DWG does NOT enforce accessibility — it **relays** the baseline into enforceable steering rules. Enforcement is AI-GCE's responsibility. DWG's job:
1. Extract the baseline from UXP (verbatim requirements)
2. Transform into prescriptive steering rules (MUST/MUST NOT)
3. Place in `design-system.md` (primary) and `frontend-standards.md` (cross-reference)
4. Signal AI-GCE that the baseline is available for hook derivation

### If UXD Absent But ADLC Has Quality Attributes

When UXD is not present but ADLC has accessibility mentioned in Quality Attributes, DWG produces a **basic** accessibility section in `frontend-standards.md` (FE-A11Y-01 through FE-A11Y-08) from the generic Quality Attributes. This is less specific than a UXP baseline but ensures the workspace isn't accessibility-blind.

---

## Key Rules

1. **NEVER invent content absent inputs don't provide.** If a peer input is absent, its cluster is simply not generated. Don't assume or synthesize what's missing.
2. **Extract VERBATIM where possible.** Principle statements, constraint definitions, technology names, vision statements, and design tokens should be copied exactly — not paraphrased.
3. **Trace every extraction.** Know which peer input + artifact + section provided which piece of generated content (for provenance tracking).
4. **Respect conditional triggers.** Don't generate files the present inputs don't justify. Don't skip files the inputs demand.
5. **Extension content is authoritative.** If an extension was active (ADLC present), its additional AP content takes precedence over normal conditional logic.
6. **Peer inputs are non-overlapping by design.** Each owns a distinct domain (tech / product / UX). Conflict between them is an anomaly — flag, analyze root cause, present correction suggestion. Do NOT resolve conflicts — user decides.
7. **Quality-impact disclosure is mandatory.** When fewer than 3 inputs are present, disclose what's missing and get explicit user approval before proceeding.
