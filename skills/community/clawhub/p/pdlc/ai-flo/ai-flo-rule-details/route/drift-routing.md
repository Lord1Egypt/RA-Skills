<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Drift Brokering — Address-Only Broker Between GCE, Packages, and DWG

## Purpose

Defines how AI-FLO **brokers** drift between AI-GCE (detector), the target packages (disposers), and AI-DWG (re-baseliner) — as a pure **address broker**, both directions. FLO carries **pointers, never payloads**: it reads only the routing **envelope** of a drift entry (`driftId` + `domainTag` + `status`), resolves the owning package via the routing table, and hands that package the **address** of its drift. It never reads the drift body, never relays drift detail, and **never writes the drift register**.

FLO does NOT interpret or dispose drift — it brokers addresses (the universal fabric courier role). GCE detects and owns the register; target packages read + dispose; DWG re-baselines; **FLO only points**.

**Grounding:** Implements `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §6 under the **baseline-brokered pull** model (INV-L4-006).

---

## MANDATORY: Stage Sub-Role — (FLO primary — fabric courier)

FLO stays in its courier role: read envelope → resolve owner → hand over address. No domain interpretation, no payload handling.

### Anti-Patterns
- **Do NOT write the drift register** — GCE is the sole writer (INV-L4-006). FLO has NO write access.
- Do NOT read or relay the drift **body** (evidence, elementDescription) — hand over the address only; the package reads the body from GCE.
- Do NOT interpret or dispose drift — brokering only (disposition belongs to the target package).
- Do NOT push work to packages — packages **pull** (they ask FLO); FLO answers.
- Do NOT route advisory drift by default (only on explicit `DFT__ route advisory`).
- Do NOT hardcode the drift register path — resolve via `manifest.files.driftRegister`.

---

## Ownership Model (INV-L4-006)

| Artifact | Writer | FLO's access |
|----------|--------|--------------|
| `.governance/drift-register.md` | **GCE only** | **read-only, envelope fields only** (`driftId`, `domainTag`, `status`) |
| `.flo/routing-log.md` | **FLO** | read/write (its own audit trail) |
| package design artifact | that package | none |
| baseline `vN` + ledger | DWG | none |

FLO holds **no drift content**. It reads the envelope to know *which package owns what*, records the brokering decision in its own routing-log, and hands over an address. Nothing FLO does mutates another component's artifact.

---

## Discovery

FLO resolves the drift register via the workspace manifest: `manifest.files.driftRegister` (typically `.governance/drift-register.md`). Same manifest-driven discovery the whole family uses. FLO opens it **read-only**.

---

## Drift Routing Table (from pdlc-overlay.md)

FLO reads the `driftRouting` map (domain tag → target package) declared in `pdlc-overlay.md`:

```yaml
driftRouting:
  architecture: AI-ADLC
  data: AI-ADLC
  infrastructure: AI-ADLC
  ux: AI-UXD
  product: AI-POLC
# No `governance` route — GCE's own governance layer is not a DWG baseline element and
# cannot drift; stale/edited rules are GCE re-derivation, not drift.
```

**Why domain-tag → package (not GCE naming the package):** keeps GCE free of topology knowledge AND keeps packages free of it too. Only FLO knows the `domainTag → package` mapping. If a future family reshuffles responsibilities, only this table changes — GCE's detection and the packages' intake stay stable.

---

## Broker Direction 1 — Package Inbox Query (Pull)

A target package asks FLO whether any drift is waiting for it. FLO answers with **addresses only**.

```
Package → FLO:  "Any drift for me (AI-{PKG})?"

FLO:
  1. Open drift-register read-only (manifest.files.driftRegister)
  2. FOR EACH entry: read ENVELOPE only (driftId, domainTag, status)
       - skip entries whose status is not OPEN (or OPEN-ADVISORY if advisory requested)
       - resolve domainTag → package via driftRouting
  3. COLLECT driftIds where resolved package == AI-{PKG}
  4. Record the brokering event in.flo/routing-log.md
       (driftId, domainTag, → AI-{PKG}, timestamp)
  5. RETURN the ADDRESS list to the package:
       [ { driftId: DRF-003, address: "<register>#DRF-003" },... ]
     (NO body, NO evidence, NO elementDescription — pointer only)

Package:
  6. Reads each drift record DIRECTLY from GCE's register (read-only) at the address
  7. Digests → produces disposition → writes to its OWN artifact + emits "digest ready"
```

FLO never reads step 6's content. The package fetches the letter; FLO only supplied the envelope address.

---

## Broker Direction 2 — DWG Digest-Ready Pickup (Pull)

Before re-baselining, DWG asks FLO which packages have a completed digest ready to bake in.

```
DWG → FLO:  "Any digested drift ready in packages?"

FLO:
  1. Poll each target package's "digest ready" signal (its own state/output) — read-only
  2. COLLECT the ready items: { driftId, package, dispositionType, address-of-package-output }
     (only items with a completed digest — no matter the disposition type)
  3. Record the pickup event in.flo/routing-log.md
  4. RETURN the ready list (addresses) to DWG

DWG:
  5. Reads each package's disposition output → bakes into baseline vN+1 ledger + marks
  6. (GCE later reads vN+1 → verifies → closes its own register entries)
```

Again FLO carries addresses, not the disposition payload — DWG reads the payload from the package's own output.

---

## Advisory Drift — Not Brokered by Default

Advisory drift (`OPEN-ADVISORY`) is NOT included in inbox answers automatically (reduces noise for target packages). Operator can request: `DFT__ route advisory` — FLO includes advisory addresses too, but with no gate-blocking consequence.

---

## Conflict C10 — Drift Gate Block

FLO enforces gates from the register (read-only) + its own brokering log — never by writing the register:

| # | Type | Description | Severity | Resolution |
|---|------|-------------|----------|------------|
| C10 | Drift Gate Block | Entity cannot advance — unresolved HARD drift (`status == OPEN`) | Critical (hold) | Broker address → package disposes → DWG re-baseline → GCE re-scan closes → release |

Integrates with FLO's existing **flag-and-hold**: the entity holds until drift resolves, then FLO re-evaluates the gate. Lifecycle mirrors other conflicts: `DETECTED → FLAGGED → HOLDING → RESOLVED → CLOSED`.

**Resolution path for C10:**
```
1. FLO answers the owning package's inbox query with the drift address (envelope → driftRouting)
2. Target package reads the drift from GCE, disposes (Conform / Amend / Waive) — its own drift-intake flow
3. Target package emits "digest ready"; DWG picks it up via FLO → re-baselines vN → vN+1 (disposition in ledger)
4. GCE re-scans vN+1 → confirms closure → register entry CLOSED (GCE writes this, not FLO)
5. FLO re-evaluates the gate → hold released → entity advances
```

---

## Advance Pre-Check Integration

FLO's `advance` command gains a drift pre-check (before the GATE_PROTOCOL 5-step stack):

```
advance [entity]:
  Step 0 (NEW): DRIFT PRE-CHECK
    - Read drift-register read-only (manifest.files.driftRegister)
    - Count HARD entries WHERE status == OPEN
    - IF count > 0:
        - Ensure each is brokered (envelope → driftRouting → routing-log; owning package can pull it)
        - BLOCK advance (C10 — flag-and-hold)
    - IF count == 0: proceed to Step 1 (structure/type/version/mandatory)
```

This mirrors GCE's gate Step 0 (`drift/gate-integration.md`) — FLO enforces it at the brokering/advance layer, reading the register but never writing it.

---

## Command Surface

| Command | Mode | Action |
|---------|------|--------|
| `DFT__ route` | broker | Broker all OPEN (hard) entries: envelope → driftRouting → routing-log; answers pending inbox queries with addresses |
| `DFT__ route advisory` | broker | Also broker advisory entries (no gate block) |
| `conflicts` | report | Shows C10 drift-blocks alongside C1–C9 |

> "broker" mode writes ONLY `.flo/routing-log.md` (FLO's own artifact). It never writes the drift register.

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `ai-flo-rules/pdlc-overlay.md` | Declares the `driftRouting` table FLO reads |
| `monitor/health-conflicts-alerts.md` | C10 detection + drift counts in status |
| `route/handoff-execution.md` | Standard routing FLO extends with the drift pre-check |
| (AI-GCE `drift/drift-register.md`) | The register FLO reads (envelope only, read-only); GCE is sole writer |
| (AI-GCE `drift/gate-integration.md`) | GCE's gate Step 0 — same block, GCE side |
| (target packages) | Pull drift addresses from FLO, read bodies from GCE, dispose (Phase P7) |
| (AI-DWG re-baseline) | Pulls digest-ready list from FLO before baking vN+1 |

---

## Output Validation

- [ ] Drift register resolved via `manifest.files.driftRegister` (not hardcoded), opened **read-only**
- [ ] FLO reads ONLY the envelope (`driftId`/`domainTag`/`status`) — never the drift body
- [ ] FLO **never writes** the register (no `routedTo`/`routedAt`/status writes) — INV-L4-006
- [ ] Brokering decisions recorded only in `.flo/routing-log.md`
- [ ] Inbox query returns **addresses only**; packages read bodies from GCE
- [ ] DWG pickup returns ready-digest **addresses only**; DWG reads payload from package output
- [ ] Advisory drift not brokered unless `DFT__ route advisory`
- [ ] C10 flag-and-hold blocks advance on unresolved HARD drift (`status == OPEN`), computed read-only
