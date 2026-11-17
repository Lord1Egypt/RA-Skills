<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Drift Register — Schema, Writer, Waivers, Thrash Guard

## Purpose

Defines the **Drift Register** — GCE's live state of all drift entries (open / closed / waived) — its schema, the write rules (GCE is the sole writer — no exceptions), waiver management with expiry + auto-reopen, and the thrash guard that prevents detect→dispose→detect loops.

**Location:** `.governance/drift-register.md` (resolved via `manifest.files.driftRegister`).

**Grounding:** Implements `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §5.6, §8.3, §8.4.

---

## MANDATORY: Stage Sub-Role — Audit Specialist

Audit Specialist mindset (immutable trail, one writer, verifiable state). ADDS a dimension.

### Anti-Patterns
- Do NOT let any package other than GCE write the register
- Do NOT delete entries — they transition state (CLOSED/WAIVED/SELF-RESOLVED), never vanish
- Do NOT leave a waiver un-expiring — every waiver is time-boxed

---

## GCE is Sole Writer (No Exceptions)

GCE is the ONLY writer of the Drift Register — **no exceptions** (INV-L4-006). No other component ever writes here:
- **Target packages** emit dispositions via the DWG re-baseline channel (not by writing here). They may only **read** their own entry (read-only).
- **AI-FLO** never writes the register. It reads only the routing **envelope** of each entry (`driftId` + `domainTag` + `status`) to hand a package the **address** of its drift — it never writes routing fields, never reads the drift body. FLO records routing decisions in its own `.flo/routing-log.md`.
- **DWG** never writes the register. It writes the baseline; GCE reconciles by reading the baseline.

**Single reconciliation channel:** GCE learns every resolution ONLY from the arriving baseline version (`vN+1` disposition ledger) — never from FLO, never from a package. This keeps the register a single-writer, tamper-evident audit trail.

---

## Register Schema

```yaml
# .governance/drift-register.md
---
registryVersion: 1.0
baselineVersion: v3            # current baseline this register measures against
lastScanTimestamp: {ISO}
projectId: PRJ-{ABBREV}-{YYYY}-{NNN}
---

entries:
  - driftId: DRF-003
    status: OPEN               # see lifecycle states below
    classification: HARD       # HARD | ADVISORY
    domainTag: architecture    # architecture|data|infrastructure|ux|product (no governance — see engine)
    elementId: ARCH-003
    elementDescription: "REST API versioning: URI path v{N}"
    baselineVersion: v3        # pinned: detected against this version
    detectedAt: {ISO}
    evidence: "src/api/routes.ts uses header-based versioning instead of URI path"
    # NOTE: no routedTo/routedAt on the register — routing state lives in FLO's .flo/routing-log.md

  - driftId: DRF-004
    status: OPEN-ADVISORY
    classification: ADVISORY
    domainTag: ux
    elementId: ADV-001
    elementDescription: "camelCase for variables"
    baselineVersion: v3
    detectedAt: {ISO}
    evidence: "src/utils/helpers.ts uses snake_case in 3 functions"

  - driftId: DRF-001
    status: CLOSED
    classification: HARD
    domainTag: architecture
    elementId: ARCH-002
    baselineVersion: v2
    detectedAt: {ISO}
    closedAt: {ISO}
    disposition: amend
    resolvedInVersion: v3       # closure confirmed by reading v3's ledger

  - driftId: DRF-002
    status: WAIVED
    classification: HARD
    domainTag: ux
    elementId: UX-001
    baselineVersion: v3
    detectedAt: {ISO}
    waivedAt: {ISO}
    waiverExpiry: 2026-09-01
    waiverOwner: "design-lead"
    resolvedInVersion: v4
```

---

## Lifecycle States (Register = GCE-Observable States Only)

The register carries ONLY states GCE can independently determine from its own detection + the arriving baseline. The intermediate routing/digest states are **not** on the register — they live where they are owned (FLO's routing-log; the target package's own state):

```
GCE register view:
  OPEN ─────────────────────────────▶ CLOSED        (GCE verifies via vN+1 ledger)
   │                              └──▶ WAIVED        (GCE reads waiver annotation in vN+1)
   └── (self-resolved) ──────────────▶ SELF-RESOLVED (drift gone without disposition)

Off-register (owned elsewhere, GCE never observes directly):
  ROUTED     — tracked in FLO's .flo/routing-log.md
  IN_DIGEST  — tracked in the target package's own state
```

**Register states:**
| State | Meaning |
|-------|---------|
| `OPEN` | Hard drift, awaiting resolution |
| `OPEN-ADVISORY` | Advisory drift; never blocks |
| `WAIVED` | Hard drift with active unexpired waiver (suppressed) |
| `CLOSED` | Resolved — confirmed via the `vN+1` disposition ledger |
| `SELF-RESOLVED` | Drift disappeared without explicit disposition (logged) |
| `EXPIRED` | Waiver expired → auto-reopened as `OPEN` |

> GCE transitions an OPEN entry only when a **new baseline version arrives** (it reads the ledger, re-measures, then CLOSES/WAIVES) or when re-measurement shows the drift is gone (SELF-RESOLVED). GCE never learns routing/digest progress — that is not its concern.

---

## Write Rules (GCE Only)

Every write below is performed by **GCE and GCE alone**. FLO and packages never write here.

1. **New drift** → append entry, status `OPEN` (hard) or `OPEN-ADVISORY`, pinned to current `baselineVersion`, with evidence.
2. **Closure** (after reading `vN+1` ledger + re-measuring) → status → `CLOSED`, set `disposition`, `closedAt`, `resolvedInVersion`.
3. **Waiver** (from `vN+1` waiver annotation) → status → `WAIVED`, set `waiverOwner`, `waiverExpiry`, `resolvedInVersion`.
4. **Self-resolved** → status → `SELF-RESOLVED` (drift gone without disposition).
5. **Never delete** — entries transition; the register is an immutable audit trail.

> There is deliberately **no "routing" write rule**. Routing does not touch the register — FLO records it in `.flo/routing-log.md`.

---

## Waiver Management (Expiry + Auto-Reopen)

Every waiver is time-boxed. Nothing stays waived silently forever.

```
WAIVED entry with waiverExpiry: {date}

On each DFT__ scan:
  IF current_date > waiverExpiry:
    1. status → EXPIRED → DETECTED (re-opened)
    2. Re-measure the element:
       → still drifted? → fresh HARD drift, must be resolved again
       → not drifted?   → SELF-RESOLVED (fixed during the waiver window)
    3. Alert: "⚠️ Waiver expired for DRF-{NNN}. Drift re-opened."
```

**Waiver requirements (enforced):** `waiverOwner` (named) + `waiverExpiry` (mandatory, future date). A waiver without both is invalid — GCE rejects it and keeps the entry OPEN.

---

## Thrash Guard (Loop Prevention)

Prevents Amend → re-baseline → re-measure → new drift on the just-changed element → another Amend → infinite loop.

```
WHEN DWG re-baselines vN → vN+1:
  FOR EACH element changed in vN+1 (via dispositionLedger):
    SUPPRESS drift detection on that element for ONE scan cycle
    (the first DFT__ after re-baseline skips these elements)
  AFTER one scan cycle: suppression lifts; element measured normally
```

GCE reads the ledger's `toVersion == current` entries to know which elements to suppress this cycle. Combined with waiver expiry, the system always converges (settles in at most one extra cycle).

---

## Scan Summary Output

After each scan, GCE reports (console + register `lastScanTimestamp` update):

```
Drift scan vs baseline v{N}:
  🆕 {new} new ({H} hard, {A} advisory)
  ✅ {resolved} resolved (closed/self-resolved)
  ⏳ {open} still open ({openHard} hard)
  🔕 {waived} waived ({expiringSoon} expiring within 7 days)
  {IF openHard > 0}: ⛔ Gate blocked — {openHard} unresolved hard drift(s)
  {IF openHard == 0}: ✅ Gate clear
```

Silent when fully compliant (zero drift → minimal "✅ All governed elements pass").

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `drift/drift-detection-engine.md` | Writes entries; checks waiver + thrash guard here |
| `drift/gate-integration.md` | Reads `OPEN` HARD counts to block gates |
| (AI-FLO) | Reads the routing **envelope** (`driftId`+`domainTag`+`status`) read-only to hand packages an address; never writes the register |
| (target packages) | Read their own entry (read-only) after FLO hands them the address; never write the register |
| (DWG re-baseline) | GCE reads `vN+1` ledger → closes entries + applies thrash suppression |

---

## Output Validation

- [ ] `.governance/drift-register.md` written by **GCE only** — no FLO/package/DWG writes (INV-L4-006)
- [ ] No `routedTo`/`routedAt` fields on the register (routing lives in FLO's routing-log)
- [ ] Register carries only GCE-observable states (`OPEN`/`OPEN-ADVISORY`/`WAIVED`/`CLOSED`/`SELF-RESOLVED`/`EXPIRED`)
- [ ] Closure/waiver set only after reading the `vN+1` baseline ledger
- [ ] Every entry pinned to the baseline version it was detected against
- [ ] Entries transition state; never deleted
- [ ] Every waiver has owner + future expiry (else rejected)
- [ ] Expired waivers auto-reopen + re-measure on next scan
- [ ] Thrash guard suppresses just-changed elements for one cycle
- [ ] Scan summary produced; silent when compliant
