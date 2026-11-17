<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Drift Intake Digest — AI-ADLC (Architecture Domain)

## Purpose

Defines how AI-ADLC **receives, digests, and resolves** drift routed to the architecture domains. AI-ADLC implements the `drift-intake@1.0` interface (see `contracts/DRIFT_INTAKE_CONTRACT.md`); this file carries ONLY the architecture-specific decision logic. The interface shape, authority matrix, and communication model are the contract's — not repeated here.

**Domains owned:** `architecture` · `data` · `infrastructure` (from the `driftRouting` table AI-FLO owns).

**Grounding:** `contracts/DRIFT_INTAKE_CONTRACT.md` (`drift-intake@1.0`) + `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §7 under the baseline-brokered pull model (INV-L4-006).

---

## MANDATORY: Sub-Role — Systems Engineer (+ Security/Data/API as the drift dictates)

Digest under the CTO/Architect primary + the sub-role matching the drifted element: `#persona-subrole-systems-engineer` (boundaries/containers/components), `#persona-subrole-security-architect` (auth/identity), `#persona-subrole-data-architect` (data/schema), `#persona-subrole-api-designer` (API/integration). ADDS a lens — never replaces the primary.

### Anti-Patterns
- Do NOT write the drift register or the baseline — disposition goes to ADLC's OWN artifacts, then DWG re-baselines (INV-L4-006).
- Do NOT read FLO's routing-log — learn of drift ONLY by querying FLO (address) + reading GCE's register.
- Do NOT hardcode "which domains are mine" — ask FLO; it returns only what belongs to AI-ADLC.
- Do NOT Amend without a formal ADR — an architectural change to absorb drift is a decision, not an edit.

---

## Step 1 — Pull (Contract §3, Direction 1)

```
1. Ask AI-FLO: "Any drift for AI-ADLC?"
2. FLO returns ADDRESS(es) only: { driftId, address: "<register>#DRF-NNN" }
3. FOR EACH address: read the drift body DIRECTLY from GCE's register (READ-ONLY):
     driftId · elementId · classification · domainTag · evidence · baselineVersion · elementDescription
4. Confirm domainTag ∈ {architecture, data, infrastructure} (sanity — FLO already resolved ownership)
```

No push arrives; ADLC pulls. The body is read from GCE, never relayed by FLO.

---

## Step 2 — Digest: Architecture-Domain Decision Guidance

Map the drifted element to its architectural intent, then choose ONE disposition. Guidance by element type:

| Drifted element (`domainTag`) | Typical source of truth (AP) | Decision lens |
|-------------------------------|------------------------------|---------------|
| `technology-choice` (architecture) | `04_Technology_Stack.md` + ADR | Was the stack decision deliberately changed, or did an implementation shortcut diverge? |
| `component-boundary` (architecture) | `11_Component_Diagram_C4L3.md`, `03_Container_Diagram_C4L2.md` | Did the module/boundary genuinely need to move, or is code crossing a boundary it shouldn't? |
| `api-contract` (architecture) | `08_API_Architecture.md` + ADR | Is the new API shape the intended evolution, or an unsanctioned break? |
| `data-model` / schema (data) | `07_Data_Architecture.md` + ADR | Did the data design evolve, or did the implementation drift from the approved schema? |
| `integration` / topology (infrastructure) | `09_Integration_Architecture.md`, `10_Infrastructure_Deployment.md` | Is the deployment/integration change adopted, or accidental? |

### Choosing the disposition (authority per contract §5)

- **Conform** — the approved architecture is still correct; reality is wrong. The implementation must be brought back to the baseline element. ADLC records the expectation; no design change. *Low ceremony.*
- **Amend** — the architectural intent genuinely changed. Update the source AP artifact **and write/replace the governing ADR** (context → options → decision → consequences), then let DWG re-baseline. *High ceremony — this is an architecture decision (Rule 3), gate/approval required.*
- **Waive** — acknowledged technical debt: the divergence is tolerated for now, with a named owner and a mandatory future expiry. *Highest ceremony — time-boxed; auto-reopens on expiry.*

> Amend on any `technology-choice`, `component-boundary`, or `api-contract` element ALWAYS produces an ADR — an architectural change without an ADR violates ADLC Rule 3.

---

## Step 3 — Emit (Contract §4.3–4.5)

Write the disposition to AI-ADLC's OWN artifacts, then signal readiness:

| Disposition | ADLC writes (own artifacts) | Then |
|-------------|-----------------------------|------|
| Conform | Note the restore expectation in the Workbook / relevant AP section (element unchanged) | emit `digest-ready` (type: conform) |
| Amend | Update the source AP doc (`04`/`07`/`08`/`11`/…) + add/replace `ADR/ADR-{NNN}_*.md` + log a `Decision_*` spine entry | emit `digest-ready` (type: amend, `changedElement` + rationale) |
| Waive | Record the waiver (owner + future expiry + scope) in `adlc-state.md` / Workbook | emit `digest-ready` (type: waive, owner+expiry+scope) |

```yaml
digest-ready:                 # in adlc-state.md (ADLC's own state)
  - driftId: DRF-003
    dispositionType: amend
    outputAddress: "adlc-state.md#DRF-003"   # where DWG reads the disposition payload
    readyAt: {ISO}
```

DWG later pulls this via FLO (Contract §3, Direction 2), reads the payload from `outputAddress`, and bakes it into baseline `vN+1`. GCE then reads `vN+1` and closes the register entry. **AI-ADLC never writes the register or the baseline.**

---

## Step 4 — Examples

**Example A — `api-contract` drift → Amend.**
`DRF-003`: `08_API_Architecture.md` declares URI-path versioning; code uses header-based versioning, and the team confirms header-based is now intended. → **Amend**: update `08_API_Architecture.md`, write `ADR-014_API_Versioning_Strategy.md` (context/options/decision/consequences), log a Decision spine entry, emit `digest-ready(amend)`. DWG re-baselines; the new governed element matches reality; GCE closes.

**Example B — `component-boundary` drift → Conform.**
`DRF-007`: a service imports across a module boundary the C4 L3 design forbids, with no decision to change the boundary. → **Conform**: the boundary stands; record the restore expectation; emit `digest-ready(conform)`. DWG carries a ledger entry (design unchanged); GCE re-measures vs the same element and closes when the import is removed.

**Example C — `technology-choice` drift → Waive.**
`DRF-011`: a legacy module still uses the pre-migration library. Migrating now is out of scope this sprint. → **Waive**: owner = `platform-lead`, expiry = end of Sprint 8, scope = that module only; record in `adlc-state.md`; emit `digest-ready(waive)`. GCE confirms the annotation (owner + unexpired expiry); the waiver auto-reopens at expiry.

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `contracts/DRIFT_INTAKE_CONTRACT.md` | The `drift-intake@1.0` interface + authority matrix this file implements |
| (AI-FLO `route/drift-routing.md`) | Answers ADLC's inbox query with drift addresses; polls ADLC's `digest-ready` for DWG |
| (AI-GCE `drift/drift-register.md`) | The register ADLC reads (read-only) for the drift body; GCE closes entries from the baseline |
| (AI-DWG `reconciliation/re-baseline.md`) | Pulls ADLC's disposition via FLO; bakes into `vN+1` |
| `decisions/technology-stack.md` · `design/api-architecture.md` · `design/data-architecture.md` · `design/component-design.md` | The AP artifacts an Amend updates |
| `assembly/package-assembly.md` | ADR + spine logging conventions an Amend follows |

---

## Output Validation

- [ ] Drift pulled by querying FLO (address) + reading GCE register (read-only) — never scanned/pushed
- [ ] Disposition written to ADLC's OWN artifacts (AP docs / ADR / `adlc-state.md`) — never the register or baseline
- [ ] Every Amend on a tech-choice / boundary / API element produces an ADR (Rule 3)
- [ ] Waivers carry named owner + mandatory future expiry
- [ ] `digest-ready` signal emitted in `adlc-state.md` with `driftId` + `dispositionType` + `outputAddress`
- [ ] No read of FLO's routing-log; drift state learned only from GCE register + own digest
