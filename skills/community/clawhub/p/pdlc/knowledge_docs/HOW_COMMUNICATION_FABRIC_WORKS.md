# How the Communication Fabric Works

**Purpose:** Explains how every package in the AI-* Family communicates — intra-family and inter-family — through one unified mechanism: the AIFLC Communication Fabric. Covers how packages discover neighbors, how gates enforce contracts at boundaries, how edges form, how FLO routes over the fabric, and how families stay self-contained.

---

## What the Communication Fabric Is

The Communication Fabric is the single mechanism through which all packages exchange outputs and verify readiness — whether the producer and consumer are in the same family or in different families. The difference between "same family" and "different family" is a visibility attribute on the edge, not a different mechanism.

```
   Producer                                         Consumer
   (any package)                                    (any package)
        │                                                │
        │  gate-out: emits a capability-typed marker     │
        │            with guaranteed fields              │
        └────────────────────┬───────────────────────────┘
                             │
                     THE FABRIC handles:
                     1. discovery (find the anchor)
                     2. type + version match
                     3. gate-in mandatory/optional check
                     4. routing (optional FLO courier)
```

**One principle:** a producer emits a capability-typed output via a marker; a consumer with a matching gate-in consumes it. The fabric validates compatibility and advises readiness. That's it — same algorithm everywhere.

---

## The Five Objects

The fabric is realized as five artifacts, each with a single clear job:

| # | Object | Where it lives | Job |
|---|--------|----------------|-----|
| 1 | `GATE_PROTOCOL.md` | each family root (copied from canonical source) | The universal **schema + behavior**: defines what a gate is, the matching algorithm, versioning rules, the capability-type vocabulary |
| 2 | `FAMILY_INTERFACE.md` | each family root | The family's **public interface**: which packages are seams, what capability types they emit/consume (pointers to gate contracts — no gate detail here) |
| 3 | Package **§ Gate Contract** | inside each package's core file | The package's own gate-in/out **declaration**: capability types + mandatory/optional fields + strictness |
| 4 | `CROSS_FAMILY_FLOWS.md` | build workspace (never published) | The user-defined list of intended **cross-family edges** — each a directed, typed connection |
| 5 | `FAMILY_BINDINGS.md` | each family root (generated, do-not-edit) | The family's **complete topology**: internal edges (auto-derived from gate contracts) + external edges (from cross-family flows) |

---

## How Visibility Scopes the Fabric

Each capability on a gate contract carries a visibility attribute:

| Visibility | Meaning | Edge formation |
|------------|---------|----------------|
| `internal` | Family-private; binds only within this family | Auto-derived from gate contracts (capability match) |
| `external` | Seam-exposed; may be referenced by a declared cross-family flow | Explicitly declared in `CROSS_FAMILY_FLOWS.md` |

Internal edges form automatically (all matching types within the family are wired). External edges form only when the user declares them — this prevents unwanted coupling across 10+ families.

---

## How a Package Gate Works

Every package boundary has the same anatomy:

```
GATE-OUT (producer asserts before declaring done):
  emits-type: project-initiation@1
  marker: pilc-state.md
  guarantees: [status==complete, projectId, charter, scope, riskRegister]

GATE-IN (consumer checks before starting):
  consumes-types: [project-initiation@^1]
  mandatory: [status==complete, id]         ← missing = BLOCK (always, non-configurable)
  optional:  [budgetCeiling, marketSizing]  ← missing = DEGRADE (configurable tolerance)
  on-missing-all: standalone                ← P4: always works without predecessor
```

The **behavior** (the matching algorithm) is universal — defined in `GATE_PROTOCOL.md`. Each package **declares** its own contract; the algorithm validates it.

---

## The Matching Stack (Five Steps)

Every hop — whether internal or across families — runs this same sequence:

| Step | Check | On failure |
|------|-------|------------|
| 1 | **Structure** — can I parse the producer's files? (`interfaceVersion` readable) | HALT + ASK |
| 2 | **Type name** — do we name the same capability? | NO-MATCH (skip this neighbor) |
| 3 | **Type version** — is the producer's version in the consumer's compatible range? | BLOCK / ASK |
| 4 | **Mandatory** — producer guarantees ⊇ the matched type's mandatory fields? | **BLOCK** (non-configurable floor) |
| 5 | **Optional** — any of the matched type's optional fields missing? | DEGRADE (configurable: warn / advisory / silent) |

If all pass → **PROCEED** (enriched input available).

> **Per-type scoping:** Steps 4 and 5 check only the fields scoped to the *matched* capability type. A consumer that accepts several types (a fan-in like the workspace generator) checks each feed against only that feed's type — an architecture feed is never asked for backlog fields, and vice versa. The universal floor (a marker must be `complete` and carry an entity ID) is enforced separately by the marker integrity check.

---

## How Discovery Works (Cross-Family)

Within a family, packages find each other via `*-state.md` markers (the same pattern as before the fabric). Across families, discovery uses the family-level anchor:

1. **Scan** for `FAMILY_INTERFACE.md` files in sibling locations (or user-provided paths)
2. Each anchor **self-declares** its family name and root — no hardcoded neighbor knowledge
3. **Capability match** — keep neighbors where their `emits-type` ∈ the types in my `consumes` list
4. **Locate the marker** — read the producer's state file to confirm status and fields
5. **Run the gate** — matching stack (above)
6. No match / nothing found → **standalone** (the family always works alone)

---

## How FLO Routes Over the Fabric

FLO is an **optional runtime courier**. It reads the fabric objects and carries routing — it never authors artifacts or makes decisions. Without FLO, the user orchestrates manually (packages still work via marker detection).

### What FLO reads

| Object | What FLO extracts |
|--------|-------------------|
| `FAMILY_BINDINGS.md` (internal edges) | The routing graph — THIS is the routing table |
| `FAMILY_BINDINGS.md` (fan-in gates section) | Fan-in rules and ordering (e.g. "workspace generator waits for all three feeds") |
| Each package's `§ Gate Contract` | Gate-out guarantees + gate-in requirements |
| Each package's `*-state.md` | Current positions (status, emits-type) |
| `GATE_PROTOCOL.md` | The matching algorithm it executes |

### What FLO does on each hop

```
detect state change → read the edge from FAMILY_BINDINGS → read gate-out + gate-in
  → execute GATE_PROTOCOL matching stack → check routing-policy (fan-in/hold)
  → advise the operator → record the result in flo-state.md
```

### What FLO writes

One file only: `flo-state.md` (positions, routing log, conflict state). Packages write their own state.

### The FLO visibility model (two tiers)

| Tier | Scope | Role |
|------|-------|------|
| **Family FLO** (resident) | `internal` — always | Routes that family's internal graph only; ships with the family |
| **Central FLO** (workspace root, optional) | external + internal-by-proxy | Routes cross-family edges; also takes over internal routing for registered families |

Key rules:
- A family FLO is **always `internal`-scoped** — it never does cross-family routing
- When a central FLO **registers** a family, the family's resident FLO **auto-dormants**; the central FLO plays its role — writing the family's local `flo-state.md` and routing its internal graph
- **No state merge** — each family's state stays in its own folder; migration is lossless
- **Deregister** → the resident FLO reactivates from its current local state; the central FLO never touches it again

---

## Two Versioning Axes

The fabric uses two independent version numbers:

| Axis | What it versions | Bumps when |
|------|------------------|------------|
| `interfaceVersion` | The **structure** of the files (`FAMILY_INTERFACE.md` schema + gate-contract format) | A field moves/renames/disappears (so the file can't be parsed) |
| Capability-type `@version` | The **meaning** of one capability (its semantic contract) | The capability's expected behavior or field set changes incompatibly |

Within a capability-type version, content gaps are handled by degrade (not version bumps). A version bump signals a breaking *semantic* change that degrade shouldn't swallow.

---

## Standing Principles

| # | Principle |
|---|-----------|
| P1 | Cross-family flows only through **declared seam packages** (anti-coupling) |
| P2 | Detection by **marker / anchor file**, never hardcoded paths |
| P3 | A family publishes its contract **once** (sender owns it; receiver matches) |
| P4 | Every cross-family input is **optional** — families always run standalone |
| P5 | Each family is **self-contained** — no cross-cutting governance overlay |
| P6 | Gates are **bilateral** (sender guarantees, receiver requires) with a **mandatory floor** + configurable tolerance |
| P7 | **Decision approval is internal to the producer, not the seam.** A `complete` output has already passed its producing package's own approval — the seam trusts completion |

---

## Operational Behaviors

Beyond the core matching, the fabric defines how it behaves under real-world conditions:

| Behavior | What it does |
|----------|--------------|
| **Type & seam lifecycle** | Capability types and seams can be `active` → `deprecated` → `sunset`, with a migration window so consumers have time to move to a replacement |
| **Fabric audit log** | Every cross-family handoff is recorded (which entity, which flow, which version, gate result) — intra-family hops stay in the routing log |
| **Migration & coexistence** | Gate matching runs in `advisory` mode (log + warn, never block) during transition and switches to `strict` per family when ready — informal marker detection keeps working throughout |
| **Marker integrity** | A marker that parses but is internally inconsistent (missing required fields, blank entity ID) is quarantined and surfaced, never silently routed |
| **Bindings vs. activation** | The bindings graph is the *possible* topology (changed only by regeneration); runtime holds/overrides change what's *active* per entity, never the topology |

---

## Residual Inter-Family Dependency

| Layer | Dependency |
|-------|------------|
| **Runtime** | **None.** Every family works alone; cross-family input is optional; no shared registry or router |
| **Build-time** | **One — intentional.** Two families joined by a seam share a compatible **capability-type definition** (name + version + field schema). This is the irreducible interface — analogous to two services agreeing on a shared API schema |

---

## Related Documents

| Document | Location |
|----------|----------|
| Universal Gate & Seam Protocol | `GATE_PROTOCOL.md` (family root) |
| Family Interface (seam surface) | `FAMILY_INTERFACE.md` (family root) |
| Family Bindings (generated topology) | `FAMILY_BINDINGS.md` (family root) |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How Flow Orchestrator Works | `knowledge_docs/HOW_FLOW_ORCHESTRATOR_WORKS.md` |
| Pattern: Marker File Detection | `knowledge_docs/PATTERN_MARKER_FILE_DETECTION.md` |

*Knowledge Document | Created: 2026-06-18 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
