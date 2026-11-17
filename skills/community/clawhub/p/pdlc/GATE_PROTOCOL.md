# GATE_PROTOCOL.md — Universal Gate & Seam Protocol

**protocolVersion:** 1.3.0
**Date:** 2026-06-18
**Author:** Maheri
**Authored under:** `#persona-process-designer` (lead) + `#persona-cto-architect` (contracts)
**Status:** ACTIVE
**Distribution:** copied to each family root (like LICENSE/NOTICE) — serves ALL families identically

---

## 1. Purpose

This document defines the **universal gate and seam protocol** for the AIFLC Communication Fabric. It governs:

- What a gate IS (the contract between producer and consumer)
- How gates BEHAVE (the matching algorithm applied at every boundary)
- How capability types are VERSIONED (the semantic surface)
- How compatibility is ASSESSED at build-time

Every package in every family follows this one protocol. Behavior is central (fix once, not 70 times); declaration is local (each package owns its own contract).

---

## 2. Definitions

| Term | Definition |
|------|-----------|
| **Gate** | A validated boundary between a producer package and a consumer package. The producer guarantees fields; the consumer requires them. |
| **Seam** | A gate that crosses a family boundary. Always one-directional; model `A ⇄ B` as two seams. |
| **Seam package** | A package declared in `FAMILY_INTERFACE.md` Tier 1 — the only packages permitted to participate in cross-family communication (P1). |
| **Marker** | A `*-state.md` file emitted by a producer to signal completion. Self-identifying: carries `family`, `emits-type`, `status`, `entityId`, and `payloadRoot` in its front-matter. |
| **Family anchor** | `FAMILY_INTERFACE.md` at a family root — the discovery entry point for cross-family resolution. Self-declares identity and root. |
| **Capability type** | A named, versioned semantic category describing what a producer emits (e.g., `validated-business-case@1`). The shared vocabulary two packages bind on. |
| **Visibility** | An attribute (`internal` or `external`) on each capability in a gate contract. Scopes whether the capability participates in intra-family auto-binding or cross-family declared flows. |
| **Gate contract** | The `§ Gate Contract` section inside a package's core file — declares gate-in and gate-out by capability type. |
| **Fabric** | The unified communication substrate: all packages exchange outputs and verify readiness through the same mechanism regardless of whether they share a family. |

---

## 3. Founding Principles

| # | Principle | Effect |
|---|-----------|--------|
| **P1** | Cross-family communication flows **only through declared seam packages** — never any-package-to-any-package. | Prevents N² coupling across 10+ families. |
| **P2** | Detection is by **marker / anchor file**, never a hardcoded path or central router. | Decoupled discovery; no single point of failure. |
| **P3** | A family **publishes its outbound contract once** (it owns it); the receiver reads and matches. | Single-owner contracts; no drift from dual-declaration. |
| **P4** | Every cross-family input is **optional at the family level** — families always run standalone. | Graceful degradation; no hard inter-family dependency. |
| **P5** | Each family is **self-contained**; no cross-cutting governance overlay. | Any family can be extracted to its own repo and function. |
| **P6** | Gates are **bilateral** (sender guarantees, receiver requires) with a **mandatory floor** + **configurable tolerance**. | Safety without rigidity. |
| **P7** | **Decision approval is internal to the producer, not the seam.** A `status: complete` output has already passed its internal approval. The seam trusts completion. | No new approval mechanism at boundaries; packages must announce their approval step. |

---

## 4. Gate-Contract Structure

Every package that participates in the fabric declares a `§ Gate Contract` in its core file. The schema:

### 4.1 Gate-Out — What the Producer GUARANTEES

```yaml
## Gate-Out
emits-type: {capability-type}@{version}
visibility: internal | external
marker: {package-abbrev}-state.md
payloadRoot: {relative path to output artifacts}
guarantees:
  - status == complete
  - {field-1}
  - {field-2}
  - …
```

| Field | Required | Description |
|-------|:--------:|-------------|
| `emits-type` | ✅ | Capability type name + version the producer emits on completion |
| `visibility` | ✅ | `internal` (family-private, auto-binds within family) or `external` (seam-exposed, may be bound cross-family) |
| `marker` | ✅ | The state file emitted on completion — self-identifying (see §6) |
| `payloadRoot` | ✅ | Relative path where output artifacts live. Declared in the contract (the promise); concrete path emitted in the marker at runtime. |
| `guarantees` | ✅ | Fields the producer promises are present when `status == complete`. These are what consumers match against. |

### 4.2 Gate-In — What the Consumer REQUIRES

Requirements are **scoped per consumed type** — each capability type the consumer accepts declares its own mandatory/optional fields. This prevents a fan-in consumer from incorrectly requiring (e.g.) architecture fields from a backlog feed.

```yaml
## Gate-In
consumes:
  - type: {capability-type}@{semver-range}
    mandatory: [{field-1}, {field-2}]     # fields THIS type must carry — missing = BLOCK
    optional:  [{field-3}, {field-4}]     # fields THIS type should carry — missing = DEGRADE
  - type: {another-type}@{range}
    optional:  [{field-5}]
on-missing-all: standalone
strictness-default: warn
```

| Field | Required | Description |
|-------|:--------:|-------------|
| `consumes` | ✅ | List of accepted capability types, each with its OWN mandatory/optional fields |
| `consumes[].type` | ✅ | A capability type + semver range this package can consume |
| `consumes[].mandatory` | — | Fields THIS type must carry — missing = BLOCK (non-configurable; see §5.3). Omit if the type has no type-specific mandatory payload. |
| `consumes[].optional` | — | Fields THIS type should carry — missing = DEGRADE at configured strictness |
| `on-missing-all` | ✅ | Behavior when NO matching input exists at all. Always `standalone` (P4). |
| `strictness-default` | ✅ | Default tolerance for optional fields: `block`, `warn`, `advisory`, or `degrade` |

**Universal floor (not re-declared per type):** Every marker MUST carry `status: complete` and a non-empty `entityId` to be eligible for matching at all. These are enforced by the **marker integrity pre-check (§18)** — they are not listed in per-type `mandatory` because they are universal to every feed, not specific to any capability type.

**Wildcard consumers:** A package that consumes ALL types (e.g., AI-FLO the router) declares `consumes: [{ type: "*" }]` — it reads every marker as a routing trigger and declares no type-specific field requirements.

### 4.3 Strictness Override

The `strictness-default` in the gate contract is the package author's recommendation. Teams may override it in the package's install footprint (`<!-- custom -->` section or local manifest). There is NO central `gate-config.yaml` — all package-related configuration lives with the package.

---

## 5. The Matching Stack (Gate Behavior)

Every hop — intra-family or cross-family — runs this five-step sequence. This is the universal behavior; packages declare contracts, this algorithm evaluates them.

### 5.1 The Five Steps

```
Producer:  emits-type: validated-business-case@2
Consumer:  consumes: [{ type: validated-business-case@^1 }]

Step 1 — STRUCTURE CHECK
    Can I parse the producer's files? (interfaceVersion compatibility)
    FAIL → HALT + ASK (unreadable structure; cannot proceed)

Step 2 — TYPE NAME MATCH
    Does the producer emit a capability type the consumer declares in its `consumes` list?
    FAIL → NO-MATCH (skip this neighbor; not an error)

Step 3 — TYPE VERSION MATCH
    Is the producer's capability version compatible with the consumer's declared range?
    FAIL → BLOCK / ASK (incompatible semantic version)

Step 4 — MANDATORY FIELD CHECK
    producer.guarantees ⊇ consumer.consumes[matched-type].mandatory?
    (checks ONLY the mandatory fields scoped to the matched capability type)
    FAIL → BLOCK (the non-configurable floor — always fatal)

Step 5 — OPTIONAL FIELD CHECK
    Any consumer.consumes[matched-type].optional fields missing from producer.guarantees?
    FAIL → DEGRADE at consumer's strictness-default (or team override)
    
→ ALL PASS → PROCEED (enriched)
```

> **Per-type scoping (§4.2):** Steps 4 and 5 evaluate only the mandatory/optional fields declared under the *matched* capability type. A fan-in consumer accepting three types checks each producer against only that producer's type — an architecture feed is never asked for backlog fields, and vice versa.

### 5.2 Step Outcomes

| Step | On failure | Configurable? |
|------|-----------|:-------------:|
| 1 — Structure | HALT + ASK | No |
| 2 — Type name | NO-MATCH (skip) | No |
| 3 — Type version | BLOCK / ASK | No |
| 4 — Mandatory | BLOCK | **Never** — this is the non-configurable floor |
| 5 — Optional | DEGRADE per strictness | **Yes** — team-configurable |

### 5.3 The Mandatory Floor (non-configurable)

Mandatory fields represent the minimum viable input without which the consumer **cannot function**. Their absence is always a hard block — no configuration can soften this. This ensures a safety baseline across all deployments regardless of team preferences.

### 5.4 Strictness Levels (optional fields only)

| Level | Behavior |
|-------|----------|
| `block` | Treat missing optional field as fatal — refuse to proceed |
| `warn` | Proceed but emit a visible warning to the user (DEFAULT) |
| `advisory` | Log the gap; no user-facing warning |
| `degrade` | Silently proceed with reduced capability |

### 5.5 On-Missing-All (Standalone)

When NO matching input is found (no neighbor emits a compatible type, or no neighbors exist at all), the consumer enters **standalone mode** (P4). It starts from raw/self-sourced input. This is never an error — it is the designed graceful path.

---

## 6. Marker Specification

The state marker (`*-state.md`) is the runtime signal of completion. It is self-identifying — content is authoritative over filename.

### 6.1 Required Front-Matter

```yaml
---
family: {family-code}
emits-type: {capability-type}@{version}
status: complete | in-progress | blocked
entityId: {entity-identifier}
payloadRoot: {concrete-path-to-artifacts}
---
```

| Field | Description |
|-------|-------------|
| `family` | Which family produced this marker (resolves origin) |
| `emits-type` | Capability type + version (resolves what it IS) |
| `status` | Lifecycle state — gates check for `complete` |
| `entityId` | The specific entity this marker represents (e.g., `projectId: PRJ-ACME-2026-001`). Field name is family-defined; the requirement to have one is universal. Disambiguates when multiple markers of the same type exist. |
| `payloadRoot` | Concrete path to this run's output artifacts (the runtime realization of the contract's declared `payloadRoot`) |

### 6.2 Why Self-Identifying

A consumer never needs to know a foreign marker's filename in advance. It discovers markers through the `FAMILY_INTERFACE.md` anchor → gate-contract pointer → marker name. The marker's front-matter then confirms identity. Filename is convenience; **content is authoritative.**

---

## 7. Discovery Resolution Algorithm

How a consumer finds and validates its inputs at startup:

```
Consumer's gate-in package starts:

  1. ENUMERATE NEIGHBOR FAMILIES
     a. Explicit path(s) the user configured
     b. Scan sibling locations for FAMILY_INTERFACE.md anchors
     c. None found → ASK user → still none → STANDALONE (P4)

  2. READ EACH FAMILY_INTERFACE.md
     Extract: { family, familyRepo, interfaceVersion,
                seam-out[].emits-type, seam-out[].marker,
                seam-out[].gate-contract-ptr }

  3. CAPABILITY MATCH
     Keep neighbors where emits-type ∈ my consumes[].type
     No match → STANDALONE (P4)

  4. LOCATE MARKER
     For each capability match:
       find the emitted marker (relative to neighbor's output)
       read front-matter → confirm { family, emits-type, status, entityId }
       IF status ≠ complete → SKIP (not ready)
       IF multiple markers match same type → ENTITY RESOLUTION (§7.1)

  5. GATE MATCH (run §5 Matching Stack)
     Steps 1–5 against the producer's guarantees vs my requirements

  6. OUTCOME
     All pass → PROCEED (enriched with foreign input)
     Any block → BLOCK / ASK (per step behavior)
     No matches survived → STANDALONE (P4)
```

### 7.1 Entity Resolution (multi-marker disambiguation)

When multiple markers of the same capability type exist from the same or different families:

1. Check `CROSS_FAMILY_FLOWS.md` for an entity-level binding → **resolved** (pre-wired)
2. No binding found → **flag-and-hold**, ask user: "Which entity?"
3. User picks → **record the binding** (learned; reused next time)

---

## 8. Versioning Model — Two Independent Axes

The fabric uses two versioning axes that never collide:

### 8.1 Axis 1 — `interfaceVersion` (structural)

| Aspect | Detail |
|--------|--------|
| **What it tracks** | The file structure of `FAMILY_INTERFACE.md` + the gate-contract format |
| **Bumps when** | A field moves, renames, or disappears such that the file cannot be parsed by older readers |
| **Scope** | Covers both `FAMILY_INTERFACE.md` schema AND the gate-contract structure seam packages use |
| **Content changes** | Content gaps (missing fields) are NEVER version issues — handled by §5 mandatory/optional matching |

### 8.2 Axis 2 — Capability-Type Version (semantic)

| Aspect | Detail |
|--------|--------|
| **What it tracks** | The semantic meaning of one capability type |
| **Bumps when** | The capability's semantic contract changes incompatibly (breaking change to what the type MEANS) |
| **Field additions** | NOT a version bump — handled by gate matching (new field in guarantees; consumer ignores fields it doesn't declare) |
| **Backward compat** | A newer version CAN be backward-compatible with older (matching is field-based, not version-number-based) |

### 8.3 The Relationship

- **Within** a capability-type version: missing content = degrade (optional fields) or block (mandatory fields). Normal operation.
- **Across** capability-type versions: the bump signals a breaking semantic change that degrade was never meant to swallow.
- Structure versioning is orthogonal to capability versioning. A structural change doesn't imply a semantic one, and vice versa.

---

## 9. Capability-Type Vocabulary

The vocabulary is the shared semantic surface two packages bind on. It is governed at **build-time** (never at runtime).

### 9.1 What the Vocabulary Contains

For each capability type:

| Field | Description |
|-------|-------------|
| `name` | The type identifier (e.g., `validated-business-case`) |
| `version` | Current version (e.g., `@1`) |
| `description` | What this type semantically represents — one sentence |

**What it does NOT contain:** field lists. Fields live exclusively in gate contracts (guarantees[] and mandatory[]/optional[]). This eliminates double-definition drift — the gate contract is the single source of truth for fields.

### 9.2 Governance Rules

1. New types are allocated at **build-time** by the package builder
2. The vocabulary is canonical in this file's `§ Appendix A` and propagated with the protocol
3. A type name, once allocated, is never reused for a different meaning (deprecate instead)
4. Version bumps require a justification note in the vocabulary entry
5. FLO warns on **mandatory field mismatch** (consumer requires what producer doesn't guarantee) — NOT on version number alone

### 9.3 Compatibility Assessment (build-time)

For each flow in `CROSS_FAMILY_FLOWS.md`, the package builder runs:

```
FOR each declared flow (producer → consumer):
  1. Compare producer.emits-type@version vs consumer.consumes[].type@range
     → incompatible? WARN + register correction action
  2. Compare producer.guarantees vs consumer.mandatory
     → mandatory not covered? WARN + register correction action
  3. Check interfaceVersion structural compatibility
     → mismatch? WARN + register correction action
  4. Check for cycles in the flow graph
     → cycle detected? ERROR + register correction action
```

Results are logged in a **compatibility assessment log** — a correction-action register that tracks what was found, what was fixed, and what remains open.

---

## 10. Seam Rules

| Rule | Source | Effect |
|------|--------|--------|
| Seam-packages-only (P1) | Anti-N² coupling | Only packages declared in `FAMILY_INTERFACE.md` Tier 1 may participate in cross-family gates |
| Always-optional (P4) | Standalone law | A family never requires another to function; cross-family = enrichment, never dependency |
| One-directional | Design decision Q1 | Model bidirectional flows as two seams, each with its own owner. Preserves single-owner contracts (P3) + clean gate split |
| Bilateral validation (P6) | Design decision D2 | Sender guarantees, receiver requires. Both sides have skin in the game |
| No central router (P2) | Design decision D1=C | Discovery by anchor/marker file; no umbrella orchestrator |
| Self-contained families (P5) | Design decision D4 | No cross-cutting governance overlay; governance families connect only through declared seams |

---

## 11. Cross-Family Lineage

The fabric reuses the existing `TRACEABILITY_CONTRACT.md` provenance stamp. Cross-family lineage is the same mechanism — the edge simply crosses a family boundary:

```yaml
# Receiver's state after consuming foreign input
derivedFrom: BVLC-VEN-2026-001   # foreign origin — lineage crosses families
projectId:  PRJ-ACME-2026-001    # receiver mints its own
originType: project
```

Each family mints IDs internally; the provenance edge links them at the seam. `projectId` propagation rules (per `TRACEABILITY_CONTRACT.md`) extend unchanged across the fabric.

---

## 12. Edge Formation — Internal vs External

| Scope | How edges form | Governed by |
|-------|----------------|-------------|
| **Intra-family** (visibility: `internal`) | **Auto-derived** from package gate contracts. All matching types within the family are wired. | Package gate contracts + generated `FAMILY_BINDINGS.md` (internal section) |
| **Inter-family** (visibility: `external`) | **Explicitly declared** in `CROSS_FAMILY_FLOWS.md`. Never auto-binds. | User-defined flows + generated `FAMILY_BINDINGS.md` (external section) |

The matching stack (§5) is identical for both. Only edge *creation* differs — intra is open/auto-wired, inter is curated/declared.

---

## 13. Approval at Boundaries (P7)

A gate does NOT introduce a new approval step. The protocol trusts that:

1. A producer that emits `status: complete` has **already run its internal approval**
2. The producing package MUST announce its approval step to the user (transparency requirement)
3. If the user bypasses the approval informally, resulting system drift is the user's responsibility

The gate's role is **validation** (are the guaranteed fields present and compatible?), not **authorization** (should this output be allowed to proceed?). Authorization is internal to each package's own lifecycle.

---

## 14. Relationship to Existing Contracts

| Contract | Relationship to this protocol |
|----------|-------------------------------|
| `TRACEABILITY_CONTRACT.md` | Lineage mechanism (§11) reuses the provenance stamp unchanged |
| `PACKAGE_UPDATE_CONTRACT.md` | Versioning discipline extends to `interfaceVersion` + capability-type versioning |
| `AGENT_GOVERNANCE_CONTRACT.md` | Same decoupling philosophy (marker-fenced, self-sufficient, no runtime coupling) |
| `HOW_CHAIN_HANDOFF_WORKS.md` | Intra-family marker handoff — this protocol formalizes + extends it with gate validation |
| `PATTERN_MARKER_FILE_DETECTION.md` | Three-step detection reused for cross-family with `FAMILY_INTERFACE.md` as the anchor |

---

## 15. Capability-Type & Seam Lifecycle (G-E)

> **CFA-17.** Types and seams are not permanent — they may be deprecated, sunset, or superseded.

### 15.1 Lifecycle States

| State | Meaning | Consumer impact |
|-------|---------|-----------------|
| `active` | Current, recommended | Normal matching |
| `deprecated` | Still functional; replacement available | FLO warns on match; log advisory; consumers should migrate |
| `sunset` | Removed after migration window | BLOCK — type no longer satisfies gate matching |

### 15.2 Deprecation Process

1. **Declare deprecation** — add `status: deprecated` + `supersededBy: {new-type}@{version}` + `sunsetDate: {ISO date}` to the vocabulary entry in Appendix A
2. **Migration window** — consumers have until `sunsetDate` to update their `consumes` entries to the replacement type
3. **Build-time warning** — `assess-fabric-compatibility.ps1` flags any flow using a deprecated type
4. **Runtime advisory** — FLO logs a warning when routing through a deprecated edge but does NOT block
5. **Sunset** — after `sunsetDate`, the type moves to `sunset` state; gate matching step 2 (type name) returns NO-MATCH; the edge is dead

### 15.3 Seam Deprecation

Seams (cross-family flows in `CROSS_FAMILY_FLOWS.md`) follow the same lifecycle:

```yaml
- id: FLOW-001
  status: deprecated          # was: active
  supersededBy: FLOW-007      # replacement flow
  sunsetDate: 2027-03-01      # consumers migrate by this date
```

### 15.4 Rules

- A type CANNOT be sunset without a `supersededBy` replacement declared
- The migration window MUST be at least 90 days from deprecation to sunset
- Sunset types are never deleted from Appendix A — they remain with `status: sunset` for audit

---

## 16. Fabric Audit Log (G-F)

> **CFA-18.** Every cross-family handoff is a significant governance event. The fabric audit log records them.

### 16.1 What Is Logged

Every time an entity crosses a family boundary (advances on an `external` edge):

```yaml
- timestamp: {ISO datetime}
  flow: {FLOW-ID}
  entity: {entityId}
  from: {family.package}
  to: {family.package}
  type: {capability-type@version}
  gateResult: {PASS / DEGRADE(fields) / BLOCK(step)}
  actorScope: {central-flo / manual}
```

### 16.2 Where It Lives

- **Central FLO active:** appended to `_FLO_/fabric-audit-log.md` (workspace root)
- **No central FLO:** each family's resident FLO logs to its own `_FLO_/fabric-audit-log.md` (scoped to what it can see — inbound external edges only)

### 16.3 Intra-Family Hops

Intra-family hops (`internal` edges) are logged in FLO's `routing-log.md` — NOT the fabric audit log. The audit log is reserved for cross-family boundary crossings only.

---

## 17. Migration & Coexistence (G-H)

> **CFA-19.** The 10 PDLC packages chain informally today (marker detection without formal gate contracts). The fabric introduces formal gates. Both must coexist during transition.

### 17.1 Coexistence Model

| Mechanism | Status during transition | Long-term |
|-----------|--------------------------|-----------|
| **Informal chain** (direct marker detection, completeness-only readiness) | Still works — packages continue to detect `*-state.md` and proceed if `status: complete` | Retired once all packages run gate matching |
| **Formal gates** (GATE_PROTOCOL matching stack) | Additive — FLO applies gate matching in addition to completeness check | The only mechanism |

### 17.2 Transition Rules

1. **Gate matching is advisory during transition.** FLO logs gate results but does NOT block on Step 4/5 failures until the operator explicitly enables strict mode.
2. **Strict mode activation** — per family: the operator sets `gateEnforcement: strict` in `flo-state.md`. Until then, `gateEnforcement: advisory` (log + warn, never block).
3. **No big-bang cutover.** Each family transitions independently. PDLC can go strict while BVLC remains advisory.
4. **Informal detection preserved.** Even in strict mode, packages continue to detect markers. The gate adds validation ON TOP of detection — it doesn't replace it.

### 17.3 Completion Criteria

A family's transition is complete when:
- All packages have `§ Gate Contract` sections (done for PDLC)
- `FAMILY_BINDINGS.md` is generated and validated (done for PDLC)
- FLO `gateEnforcement` is set to `strict`
- No gate failures remain unresolved

---

## 18. Malformed-Marker Handling (G-I)

> **CFA-20.** A marker that parses but is internally inconsistent (distinct from missing or unreadable).

### 18.1 Integrity Checks

Before running the 5-step matching stack, FLO performs a **marker integrity pre-check**:

| Check | Failure condition | Action |
|-------|-------------------|--------|
| Required fields present | `family`, `emits-type`, `status`, `entityId` — any missing | Quarantine + alert |
| `status` value valid | Not one of: `complete`, `in-progress`, `blocked` | Quarantine + alert |
| `emits-type` in vocabulary | Type name not found in GATE_PROTOCOL Appendix A | Warn (may be a newer type from an updated family) |
| `entityId` non-empty | Field present but blank | Quarantine + alert |
| `family` matches context | Marker claims family X but found in family Y's folder | Warn (may be a cross-family output placed locally) |

### 18.2 Quarantine Path

When a marker fails integrity:

1. **Do NOT route** — the entity is held at its current position
2. **Log** — `routing-log.md` entry with failure reason
3. **Alert** — surface to operator: "Marker {filename} failed integrity: {reason}. Fix and retry, or dismiss."
4. **Operator actions:** `force` (accept the marker as-is), `dismiss` (ignore it), or fix the marker and re-scan

### 18.3 Distinction from Gate Matching

- **Integrity check** = "is this marker structurally valid?" (pre-step, before matching)
- **Gate matching** = "does this valid marker satisfy the consumer's requirements?" (the 5 steps)

A marker can pass integrity but fail gate matching (valid but incompatible). A marker that fails integrity never reaches gate matching.

---

## 19. Static Bindings vs Runtime State (G-J)

> **CFA-21.** Explicit statement of the relationship between the bindings graph and runtime activation.

### 19.1 The Two Layers

| Layer | Artifact | Meaning | Mutability |
|-------|----------|---------|:----------:|
| **Topology** (static) | `FAMILY_BINDINGS.md` | The *possible* edges — what CAN route | Build-time only (generated; never edited at runtime) |
| **Activation** (dynamic) | FLO state + operator commands | The *active* subset — what IS routing for each entity | Runtime (operator decisions per entity) |

### 19.2 Rules

1. **Bindings = possible.** Every edge in `FAMILY_BINDINGS.md` is a potential route. Not all are active for every entity.
2. **FLO state = actual.** Per-entity positions, holds, overrides, and skip lists determine what's active.
3. **Operator commands never edit bindings.** `hold`, `override`, `force` change runtime state only. To change topology, regenerate `FAMILY_BINDINGS.md`.
4. **Topology changes require rebuild.** Add/remove a gate contract → re-run `generate-family-bindings.ps1` → new topology. Runtime state adapts (new edges become available; removed edges cause stale-edge warnings).
5. **No implicit edges.** An edge not in `FAMILY_BINDINGS.md` cannot be routed, even via `override`. The operator must first add the gate contract + regenerate bindings.

---


## 20. Minor Gap Resolutions (G-K…G-P)

> **CFA-25.** Each minor gap from the design review is given an explicit stance: resolved now, or deferred with a clear trigger.

| Gap | Topic | Resolution |
|-----|-------|-----------|
| **G-K** | Trust/security boundary for cross-repo reads | **Resolved (stance):** Foreign markers and payloads are **untrusted input** — the marker integrity pre-check (§18) applies to every foreign marker, and no family ever executes code from another family (markers + artifacts are read-only data). All families are first-party today. **Deferred trigger:** hardening (signature/provenance verification) is added only if families begin shipping from different/untrusted sources. |
| **G-L** | One-to-many lineage (one entity → N descendants) | **Resolved:** Modeled by N markers, each carrying `derivedFrom: {parent}` (per `TRACEABILITY_CONTRACT.md`). FLO's lineage resolution reports all branches; each branch routes independently (see FLO "Entity Lineage Resolution — Fork handling"). |
| **G-M** | Glossary / shared terms | **Resolved:** §2 Definitions is the canonical glossary (gate, seam, seam package, marker, family anchor, capability type, visibility, gate contract, fabric). The user-facing knowledge doc mirrors these terms. |
| **G-N** | Standalone-package (no family) case | **Resolved:** A package always carries its own `§ Gate Contract`. With no `FAMILY_INTERFACE.md` present, discovery finds no neighbors → `on-missing-all: standalone` (P4). The gate contract is self-sufficient; a family anchor is not required for a package to run. |
| **G-O** | Fabric testing strategy (one family present) | **Deferred (trigger: family #2):** Intra-family is validated by `assess-fabric-compatibility.ps1` + `generate-family-bindings.ps1` (build-time) on PDLC. A full cross-family seam test (mock foreign markers, bilateral validation) is exercised when family #2 (BVLC) exists. |
| **G-P** | `protocolVersion` cross-version interop | **Resolved (stance):** Each `FAMILY_INTERFACE.md` carries its `interfaceVersion`; markers/contracts conform to a `protocolVersion`. A consumer reading a producer on a different protocol version relies on **structural compatibility (§5 Step 1)** — if the interface structure is parseable, proceed; if not, structural block (C8). A detailed cross-version interop matrix is authored only if two live families actually diverge in protocol version. |

---


## Appendix A — Capability-Type Vocabulary (Global)

> Canonical registry of ALL capability types across ALL families. New types are allocated here at build-time. Field definitions live in each package's gate contract (never duplicated here). This appendix is global — when copied to a family root it carries the full vocabulary so any family can resolve any type it encounters.
>
> **Visibility is NOT a property of the type** — it is declared per gate contract. The same type can be emitted with `internal` visibility (for intra-family consumers) AND `external` visibility (for cross-family seams). The "Seam-Capable" column flags types that at least one package exposes externally.

| # | Type Name | Version | Description | Emitted by | Family | Seam-Capable |
|---|-----------|:-------:|-------------|-----------|:------:|:------------:|
| CT-01 | `idea-decision` | @1 | A validated idea with a go/no-go decision and lifecycle disposition | AI-ILC | PDLC | — |
| CT-02 | `project-initiation` | @1 | A fully initiated project with charter, scope, risk register, and governance structure | AI-PILC | PDLC | — |
| CT-03 | `architecture-design` | @1 | A complete architecture package (C4, ADRs, NFRs, component decomposition) | AI-ADLC | PDLC | — |
| CT-04 | `product-backlog` | @1 | A prioritized, governance-ready product backlog with acceptance criteria | AI-POLC | PDLC | — |
| CT-05 | `ux-design` | @1 | UX research findings, flows, wireframes, and design specifications | AI-UXD | PDLC | — |
| CT-06 | `development-workspace` | @1 | A scaffolded workspace with CI/CD, steering, hooks, and project structure | AI-DWG | PDLC | ✅ external |
| CT-07 | `governance-engine` | @1 | Governance hooks, compliance checks, audit scoring, and drift detection rules | AI-GCE | PDLC | — |
| CT-08 | `test-strategy` | @1 | Test strategy, coverage matrix, test cases, and quality gates | AI-TGE | PDLC | — |
| CT-09 | `portfolio-state` | @1 | Adaptive portfolio positions, health scores, and intervention recommendations | AI-PPM | PDLC | ✅ external |
| CT-10 | `orchestration-state` | @1 | Routing positions, conflict flags, readiness assessments, and handoff coordination | AI-FLO | (shared infra) | — |
| CT-11 | `data-surface` | @1 | Structured per-package + demand-shaped JSON data surface (`{family}-ws/data/`) with registry, schemas, and history — the family's machine-readable data layer | AI-DFE | PDLC | — |
| CT-E01 | `validated-business-case` | @1 | A validated business case with financial model and market sizing | AI-BPLC | BVLC | ✅ external |
| CT-E02 | `capability-input` | @1 | Enterprise capability context (roadmap, capability map) that enriches idea shaping | AI-TRM | EAFLC | ✅ external |

> **Seam-Capable** = at least one producing package declares this type with `visibility: external` in its gate contract, making it eligible for cross-family flows (`CROSS_FAMILY_FLOWS.md`). A type without a seam-capable flag is intra-family only. `CT-E*` prefixes mark types whose producing family is not yet built (BVLC, EAFLC) — they are registered ahead of the family so PDLC's seam-in contracts can reference them.

> **Allocation rules:** (1) One package may emit multiple types (e.g., AI-DWG with internal + external visibility). (2) A type name, once allocated, is never reused. (3) Version bumps require a justification note below. (4) Types with `external` visibility may appear in `FAMILY_INTERFACE.md` Tier 1 and be bound cross-family.

### Version History

| Type | Version | Date | Justification |
|------|:-------:|------|---------------|
| _(none yet — all types seeded at @1)_ | | | |

---

## Appendix B — Protocol Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-18 | Initial protocol — schema, behavior, matching stack, two versioning axes, capability-type vocabulary (PDLC seed), seam rules, lineage, approval model. Filed under CFA-04. |
| 1.1.0 | 2026-06-18 | Operational hardening (Phase 5): added §15 capability-type & seam lifecycle (CFA-17/G-E), §16 fabric audit log (CFA-18/G-F), §17 migration & coexistence (CFA-19/G-H), §18 malformed-marker handling (CFA-20/G-I), §19 static bindings vs runtime state (CFA-21/G-J). |
| 1.2.0 | 2026-06-18 | **Per-type scoped gate-in (§4.2 rework).** Gate-in requirements now scope mandatory/optional fields UNDER each consumed type (`consumes: - type / mandatory / optional`), replacing the flat `consumes-types` + global `mandatory`/`optional` lists. Fixes fan-in consumers incorrectly requiring fields from feeds that don't provide them (e.g. AI-DWG asking POLC/UXD for architecture fields). Universal floor (status==complete + entityId) moved to marker integrity (§18). Unified Appendix A vocabulary into one global table with a Seam-Capable flag (visibility is per-contract, not per-type). All 10 PDLC gate contracts + assessment/generator parsers updated. Assessment: PASS, 0 issues. |
| 1.3.0 | 2026-06-18 | **Minor gap resolutions (Phase 6, CFA-25): added §20** giving an explicit stance for G-K (trust boundary — untrusted foreign input + integrity check), G-L (one-to-many lineage — N markers via derivedFrom), G-M (glossary = §2), G-N (standalone-package — gate contract self-sufficient), G-O (fabric testing — deferred to family #2), G-P (protocolVersion interop — structural compatibility via §5 Step 1). |
| 1.3.1 | 2026-06-27 | **Vocabulary addition (no protocol-mechanic change): +CT-11 `data-surface@1`** (AI-DFE, PDLC, internal visibility — not seam-capable). Registered for the AI-DFE build (Phase E fabric registration). Like CT-10 (`orchestration-state`/AI-FLO), AI-DFE is a wildcard observer that consumes `"*"` and forms no capability edge; `data-surface` is its emitted type, consumed by internal tools/dashboards via `REGISTRY.json`, not by sibling packages. Packages may keep pinning protocolVersion 1.2.0 (additive change, §5 Step 1 / G-P tolerance). |

---

*Copied to each family root per the LICENSE/NOTICE bootstrap pattern | Authored under #persona-process-designer + #persona-cto-architect | CFA-04*
