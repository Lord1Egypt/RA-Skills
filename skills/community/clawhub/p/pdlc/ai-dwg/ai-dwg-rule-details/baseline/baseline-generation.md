<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Baseline Generation — Governed Elements, Versioning, Archive

## Purpose

Defines how AI-DWG produces and versions the **baseline** — the DWG-owned snapshot of the workspace truth that drift governance (AI-GCE) measures reality against. DWG is the **sole writer** of the baseline. This file covers governed-element extraction from peer inputs, the `baseline-manifest.yaml` schema, monotonic versioning, and the archive structure.

**Output:**
- `pdlc-ws/projects/{projectId}/baselines/v{N}/baseline-manifest.yaml` — full governed surface at version N
- `pdlc-ws/projects/{projectId}/baselines/v{N}/snapshot-meta.yaml` — version metadata
- `pdlc-ws/projects/{projectId}/baselines/current/` — copy/pointer to latest (deployed to workspace)

**Condition:** Always (every generation produces v1; every re-baseline bumps the version).

**Grounding:** Implements `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §4. DWG generation side.

---

## MANDATORY: Stage Sub-Role — Systems Engineer + Audit Specialist

Systems Engineer (governed-surface modeling) layered with Audit Specialist (version integrity, immutable snapshots). ADDS a dimension — does NOT replace the primary role.

### Behavioral Shifts
- The baseline is the single source of truth reality is measured against — capture what MUST hold, not everything
- Version integrity is sacred — monotonic, immutable snapshots, never rewrite a superseded version
- Distinguish hard-governed (blocks gate) from advisory (informs) deliberately

### Anti-Patterns
- Do NOT let any package other than DWG write the baseline
- Do NOT mutate an archived version
- Do NOT over-govern — not every line is a governed element; pick the structural truths

---

## DWG as Sole Baseline Writer

**Rule: Only DWG writes the baseline.** When POLC/ADLC/UXD change the design, they update their artifacts; DWG detects the delta and re-versions as the sole custodian. One writer, one version counter, immutable prior snapshots.

---

## Governed Element Extraction (at Generation Time)

As DWG maps peer inputs → workspace, it also extracts **governed elements** — addressable design decisions with stable IDs that reality will be measured against.

| Source | Governed Element Type | Example | Locked? |
|--------|----------------------|---------|:-------:|
| AP `component-design.md` | `component-boundary` | Module boundaries from C4 L3 | hard |
| AP `technology-stack.md` | `technology-choice` | Primary language: TypeScript | hard |
| AP `api-architecture.md` | `api-contract` | REST versioning: URI path | hard |
| AP `data-architecture.md` | `data-model` | Schema/table structure | hard |
| AP `security-identity.md` | `security-pattern` | Auth mechanism, encryption | hard |
| AP `quality-attributes.md` | `nfr-threshold` | p95 < 200ms | hard |
| UXP design tokens | `design-token` | Token taxonomy | hard |
| PBP Tier 2 ACs | `acceptance-criteria` | Story ACs (EARS/G-W-T) | hard |
| AP naming conventions | `naming-convention` | camelCase variables | advisory |

**Locked (`hard`)** = drift blocks a gate. **Advisory (`locked: false`)** = drift informs, never blocks.

Element IDs are stable and sequential per category: `ARCH-001`, `UX-001`, `PROD-001`, `ADV-001`.

---

## baseline-manifest.yaml Schema

```yaml
# DWG Baseline vN — Governed Surface
---
baselineVersion: vN
projectId: PRJ-{ABBREV}-{YYYY}-{NNN}
storyStyle: {from polc-state.md — ears | invest | job-story | freestyle | hybrid}
platformTargets: [kiro, claude-code]        # from Config Gate Q2
dwgBuildVersion: {semantic}
peerInputs: [adlc, polc, uxd]               # which inputs present at generation
# buildProfile: PARKED — not populated (build-method-agnostic)

# ─── Hard-Governed Elements (drift = BLOCK at gate) ───
governedElements:
  architecture:
    - elementId: ARCH-001
      type: component-boundary
      description: "Module boundaries from C4 L3"
      source: ap/component-design.md
      locked: true
  ux:
    - elementId: UX-001
      type: design-token
      description: "Design token taxonomy"
      source: uxp/design-tokens.md
      locked: true
  product:
    - elementId: PROD-001
      type: acceptance-criteria
      description: "ACs for SPEC-001"
      source: pbp/tier2/story-elaboration.md
      locked: true

# ─── Advisory Elements (drift = INFORM, no block) ───
advisoryElements:
  - elementId: ADV-001
    type: naming-convention
    description: "camelCase for variables"
    source: ap/technology-stack.md
    locked: false

# ─── Disposition Ledger (closure + retirement provenance) ───
dispositionLedger:
  - driftId: DRF-001
    disposition: amend            # conform | amend | waive | retire
    fromVersion: v1
    toVersion: v2
    element: ARCH-002
    rationale: "…"
    resolvedBy: AI-ADLC
    timestamp: {ISO}

# ─── Version History ───
previousVersions:
  - v1: { timestamp: "{ISO}", note: "Initial generation" }
---
```

> **`storyStyle` + `platformTargets` are active fields.** `buildProfile` is PARKED — do not populate (build-method-agnostic; GCE defaults to Standard detection when absent, per drift design §5.7).

---

## Versioning Rules

| Rule | Description |
|------|-------------|
| Monotonic | v1, v2, v3, … only increments; never backward |
| Immutable snapshots | Once vN is superseded, it is archived and never mutated |
| Disposition-carrying | Every re-baseline carries a ledger entry (even Conform/Waive/retire) |
| Pin-on-detect | Drift entries pin the baseline version they were detected against |
| Deploy rule | Only the current (latest) version's governed surface is referenced by the deployed workspace |
| Per-document stamp | Every carried file gets a baseline stamp (see `baseline/document-stamping.md`) |

---

## Archive Structure

```
pdlc-ws/projects/{projectId}/
├── baselines/
│   ├── current/                    ← latest vN (governed surface the workspace uses)
│   ├── v1/
│   │   ├── baseline-manifest.yaml
│   │   └── snapshot-meta.yaml      ← { timestamp, note, trigger }
│   ├── v2/ …
│   └── v3/ …
└── {slug}-workspace/               ← generated dev workspace
```

**Note:** The full baseline archive lives on the **planning side** (`pdlc-ws/projects/`). The generated dev workspace carries only the *current* governed surface (referenced via `.governance/`). This keeps version history out of the shipped workspace while preserving it for reconciliation.

---

## What Triggers a Re-Version

(Full detail in `reconciliation/re-baseline.md`.)

| Trigger | Re-version? |
|---------|:-----------:|
| Platform target change | YES |
| Story style change (POLC) | YES |
| AP updated (architecture changed) | YES |
| PBP updated (epics/stories changed) | YES |
| UXP updated (design changed) | YES |
| Drift disposition (Conform/Amend/Waive) | YES |
| File retirement (peer-input drops a file) | YES (retire ledger entry) |

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `baseline/workspace-manifest-generation.md` | Manifest records `baselineVersion`; consumers read it |
| `baseline/document-stamping.md` | Every governed doc carries the version stamp |
| `reconciliation/re-baseline.md` | Handles the version bump on delta |
| (AI-GCE downstream) | Reads baseline governed elements to detect drift |

---

## Output Validation

- [ ] `baseline-manifest.yaml` written to `baselines/v{N}/` with governed + advisory elements
- [ ] Element IDs stable and sequential per category
- [ ] hard vs advisory classification set per element
- [ ] `storyStyle` + `platformTargets` populated; `buildProfile` absent (parked)
- [ ] `current/` points to latest version
- [ ] Prior versions archived immutably
- [ ] `snapshot-meta.yaml` records timestamp + trigger
