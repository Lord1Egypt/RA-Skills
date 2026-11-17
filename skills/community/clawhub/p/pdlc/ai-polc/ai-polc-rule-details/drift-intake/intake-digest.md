<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Drift Intake Digest — AI-POLC (Product Domain)

## Purpose

Defines how AI-POLC **receives, digests, and resolves** drift routed to the product domain. AI-POLC implements the `drift-intake@1.0` interface (see `contracts/DRIFT_INTAKE_CONTRACT.md`); this file carries ONLY the product-specific decision logic. The interface shape, authority matrix, and communication model are the contract's — not repeated here.

**Domain owned:** `product` (acceptance criteria, story/epic scope, features, value & prioritization) — from the `driftRouting` table AI-FLO owns.

**Grounding:** `contracts/DRIFT_INTAKE_CONTRACT.md` (`drift-intake@1.0`) + `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §7 under the baseline-brokered pull model (INV-L4-006).

---

## MANDATORY: Sub-Role — Audit Specialist (governance lens)

Digest under the Product Manager primary + `#persona-subrole-audit-specialist` (the governance/traceability lens that owns DoR/DoD, risk, and the traceability spine). ADDS a lens — never replaces the primary.

### Anti-Patterns
- Do NOT write the drift register or the baseline — disposition goes to POLC's OWN artifacts, then DWG re-baselines (INV-L4-006).
- Do NOT read FLO's routing-log — learn of drift ONLY by querying FLO (address) + reading GCE's register.
- Do NOT hardcode "product is mine" — ask FLO; it returns only what belongs to AI-POLC.
- Do NOT silently change an acceptance criterion — an Amend to scope/AC updates the epic/story AND the traceability matrix (Traceability Contract).

---

## Step 1 — Pull (Contract §3, Direction 1)

```
1. Ask AI-FLO: "Any drift for AI-POLC?"
2. FLO returns ADDRESS(es) only: { driftId, address: "<register>#DRF-NNN" }
3. FOR EACH address: read the drift body DIRECTLY from GCE's register (READ-ONLY):
     driftId · elementId · classification · domainTag · evidence · baselineVersion · elementDescription
4. Confirm domainTag == product (sanity — FLO already resolved ownership)
```

No push arrives; POLC pulls. The body is read from GCE, never relayed by FLO.

---

## Step 2 — Digest: Product-Domain Decision Guidance

Map the drifted element to its product intent, then choose ONE disposition. Guidance by element type:

| Drifted element (`domainTag: product`) | Source of truth (PBP) | Decision lens |
|-----------------------------------------|------------------------|---------------|
| `acceptance-criteria` | `epics/EPIC-*.md` (+ story files) | Was the AC deliberately revised, or did the build satisfy something other than the approved AC? |
| `story-scope` / feature boundary | `epics/`, `prioritization-register.md` | Did scope legitimately change (add/remove), or did the implementation quietly widen/narrow it? |
| `feature` present/absent | `product-vision.md`, `roadmap.md`, `epics/` | Is the built feature an intended addition, or scope creep outside the backlog? |
| `value-metric` / KPI | `product-vision.md` (success metrics) | Did the target change, or is the implementation ignoring an approved metric? |
| DoR/DoD expectation | `definition-of-ready.md`, `definition-of-done.md` | Did the quality bar move, or did work bypass it? |

### Choosing the disposition (authority per contract §5)

- **Conform** — the approved product intent is still correct; the implementation must meet the original acceptance criteria / scope. POLC records the expectation; no backlog change. *Low ceremony.*
- **Amend** — the product intent genuinely changed. Update the source PBP artifact (epic/story AC, scope, roadmap, or metric) **and the `traceability-matrix.md`** so intent→epic→story links stay intact, then let DWG re-baseline. *High ceremony — a scope/AC change is a product decision; PO authority + gate/approval required.*
- **Waive** — a deferred scope change: the divergence is tolerated for now (e.g., a story ships against a relaxed AC this release), with a named owner and mandatory future expiry. *Highest ceremony — time-boxed; auto-reopens on expiry.*

> Amend on any `acceptance-criteria`, `story-scope`, or `feature` element ALWAYS updates the traceability matrix — a product change that breaks intent→epic→story lineage violates the Traceability Contract.

---

## Step 3 — Emit (Contract §4.3–4.5)

Write the disposition to AI-POLC's OWN artifacts, then signal readiness:

| Disposition | POLC writes (own artifacts) | Then |
|-------------|-----------------------------|------|
| Conform | Note the restore expectation against the epic/story (element unchanged) | emit `digest-ready` (type: conform) |
| Amend | Update `epics/EPIC-*.md` (AC/scope) + `traceability-matrix.md` (+ `roadmap.md`/`product-vision.md` if the change reaches them) + log a `POLC-C-NNN` change in the spine | emit `digest-ready` (type: amend, `changedElement` + rationale) |
| Waive | Record the waiver (owner + future expiry + scope) in `polc-state.md` / `product-risk-register.md` | emit `digest-ready` (type: waive, owner+expiry+scope) |

```yaml
digest-ready:                 # in polc-state.md (POLC's own state)
  - driftId: DRF-011
    dispositionType: amend
    outputAddress: "polc-state.md#DRF-011"   # where DWG reads the disposition payload
    readyAt: {ISO}
```

DWG later pulls this via FLO (Contract §3, Direction 2), reads the payload from `outputAddress`, and bakes it into baseline `vN+1`. GCE then reads `vN+1` and closes the register entry. **AI-POLC never writes the register or the baseline.**

---

## Step 4 — Examples

**Example A — `acceptance-criteria` drift → Conform.**
`DRF-011`: `EPIC-002`'s story AC requires MFA on login; the build ships password-only, with no decision to drop MFA. → **Conform**: the AC stands; record the restore expectation; emit `digest-ready(conform)`. DWG carries a ledger entry (backlog unchanged); GCE re-measures vs the same AC and closes when MFA is implemented.

**Example B — `story-scope` drift → Amend.**
`DRF-014`: the built feature includes bulk-export, which isn't in any story, and the PO confirms bulk-export is now in scope. → **Amend**: add/adjust the story in `epics/EPIC-*.md`, update `traceability-matrix.md`, log `POLC-C-023` in the spine; emit `digest-ready(amend)`. DWG re-baselines; the new governed element matches reality; GCE closes.

**Example C — `acceptance-criteria` drift → Waive.**
`DRF-018`: a story ships against a relaxed AC (deferred i18n) to hit the release date. → **Waive**: owner = `product-owner`, expiry = next release, scope = that story's i18n AC only; record in `polc-state.md` + `product-risk-register.md`; emit `digest-ready(waive)`. GCE confirms the annotation (owner + unexpired expiry); the waiver auto-reopens at expiry.

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `contracts/DRIFT_INTAKE_CONTRACT.md` | The `drift-intake@1.0` interface + authority matrix this file implements |
| (AI-FLO `route/drift-routing.md`) | Answers POLC's inbox query with drift addresses; polls POLC's `digest-ready` for DWG |
| (AI-GCE `drift/drift-register.md`) | The register POLC reads (read-only) for the drift body; GCE closes entries from the baseline |
| (AI-DWG `reconciliation/re-baseline.md`) | Pulls POLC's disposition via FLO; bakes into `vN+1` |
| `strategy/epic-decomposition.md` · `governance/traceability.md` · `governance/definition-of-ready-done.md` | The PBP artifacts an Amend updates |
| `assembly/pbp-assembly.md` | Spine (`POLC-C-*`) logging conventions an Amend follows |

---

## Output Validation

- [ ] Drift pulled by querying FLO (address) + reading GCE register (read-only) — never scanned/pushed
- [ ] Disposition written to POLC's OWN artifacts (epics / traceability / `polc-state.md`) — never the register or baseline
- [ ] Every Amend to AC/scope/feature updates `traceability-matrix.md` (Traceability Contract)
- [ ] Waivers carry named owner + mandatory future expiry
- [ ] `digest-ready` signal emitted in `polc-state.md` with `driftId` + `dispositionType` + `outputAddress`
- [ ] No read of FLO's routing-log; drift state learned only from GCE register + own digest
