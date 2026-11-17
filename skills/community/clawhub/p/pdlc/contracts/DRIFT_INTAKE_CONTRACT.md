<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-* Family — Drift Intake Contract

**Version:** 1.0.0
**Date:** 2026-07-05
**Author:** Maheri
**Authored under:** `#persona-compliance-governance` (lead) + `#persona-process-designer` (support)
**Status:** ADOPTED
**Governs:** INV-L4-006 (single-writer + baseline-brokered drift)
**Implemented by (disposers):** AI-ADLC · AI-POLC · AI-UXD. *(AI-GCE is the detector/register-writer, not a disposer — its own governance layer isn't a baseline element and can't drift;.)*

---

## 1. Purpose

Define **one** interface, across the whole AI-* family, by which a target package **receives**, **digests**, and **resolves** a drift entry that AI-GCE detected.

The shape is **identical** for every package. Only the **digest logic** — how a package decides Conform / Amend / Waive within its own domain — differs. This contract is the uniform surface; the per-package digest lives in each package's `*-rule-details/` (see §8).

> **This is a shared CONTRACT, not a new package** — same stance as `TRACEABILITY_CONTRACT.md` and `MANAGEMENT_FRAMEWORK_CONTRACT.md`. Drift intake is a cross-cutting discipline every disposing package honors; no package "owns" another's drift.

---

## 2. Governing Principle

> **Intake is a PULL, brokered by address, reconciled through the baseline.**
>
> Nothing is pushed to a package. The package asks AI-FLO "any drift for me?"; FLO returns the **address** of its drift (a pointer, never the body); the package reads the drift **directly from GCE's register** (read-only), digests it, writes its disposition to **its own artifact**, and emits a **"digest ready"** signal. AI-DWG later pulls that signal via FLO and bakes the disposition into the next baseline version. AI-GCE learns the resolution **only** from that new baseline.

(Governed by INV-L4-006. Single writer per artifact: GCE→drift-register, FLO→routing-log, package→own artifact, DWG→baseline. No component writes another's artifact.)

---

## 3. The Communication Model (End-to-End)

```
① Package → FLO:   "Any drift for me (AI-{PKG})?"
② FLO → Package:   ADDRESS only — { driftId, address: "<register>#DRF-NNN" }
                   (FLO read the register ENVELOPE — driftId+domainTag+status — to resolve
                    the owner via driftRouting; it never read/relays the drift body)
③ Package → GCE:   reads the full drift record DIRECTLY from the register (READ-ONLY) at the address
④ Package:         digests → decides Conform / Amend / Waive
⑤ Package:         writes disposition to its OWN artifact + emits "digest ready" (own state)
⑥ DWG → FLO:       "Any digested drift ready?" → FLO returns ready addresses (pull)
⑦ DWG:             reads each package's disposition output → bakes into baseline vN+1 + ledger
⑧ GCE:             reads vN+1 ledger → verifies → CLOSES/WAIVES its own register entry
```

**A package never:** writes the drift register · writes the baseline · reads FLO's routing-log · pushes to another package.
**A package only:** reads its drift from GCE (read-only), writes its own artifact, emits its own "digest ready" signal.

> **Reconciliation chain (macro loop):** `GCE (detect) → FLO → package → FLO → DWG → GCE (close via baseline)`.
> The **return path** is `package → FLO → DWG → GCE` — GCE is the LAST actor and learns the resolution ONLY from the baseline DWG wrote. The **intake path** additionally has a `package → GCE` read (the drift body, at the address FLO supplied).

---

## 4. Interface: `drift-intake@1.0`

### 4.1 What the package receives (the address, from FLO)

FLO hands over a pointer only:

```yaml
inbox-response:               # FLO → package (Direction 1)
  - driftId: DRF-003
    address: "<manifest.files.driftRegister>#DRF-003"
  # NO evidence, NO elementDescription, NO body — pointer only
```

### 4.2 What the package reads (the body, from GCE's register — read-only)

At the address, the package reads the standard register entry fields:

```yaml
intake:                       # read by the package from GCE's register (read-only)
  driftId: string             # register entry reference
  elementId: string           # the governed element that drifted
  classification: HARD | ADVISORY
  domainTag: string           # architecture | data | infrastructure | ux | product
  evidence: string            # what GCE observed (the divergence)
  baselineVersion: string     # baseline version the drift was detected against
  elementDescription: string  # human-readable description of what should be true
```

### 4.3 What the package MUST produce (the disposition — to its own artifact)

```yaml
disposition:                  # written to the package's OWN artifact + surfaced as "digest ready"
  driftId: string             # the drift this resolves
  type: conform | amend | waive
  # CONFORM — no extra data; package restores reality to the baseline element
  # AMEND — the design change to absorb the drift:
  amend:
    changedElement: object    # updated governed element definition
    rationale: string         # why the design should change
  # WAIVE — the time-boxed exception:
  waive:
    owner: string             # named owner (mandatory)
    rationale: string         # why divergence is tolerated
    expiry: ISO-date          # mandatory, future date — auto-reopens on expiry
    scope: string             # exactly what is tolerated
```

### 4.4 The feedback channel

```yaml
feedback: via-rebaseline      # package emits "digest ready"; DWG pulls it via FLO and
                              # bakes the disposition into baseline vN+1; GCE reads vN+1 to close.
                              # The package NEVER writes the register or the baseline.
```

### 4.5 The "digest ready" signal

Each package emits a machine-readable signal in **its own state/output** that FLO can poll (read-only) on DWG's behalf:

```yaml
digest-ready:                 # in the package's own state file / output
  - driftId: DRF-003
    dispositionType: amend
    outputAddress: "<package-output>#DRF-003"   # where DWG reads the disposition payload
    readyAt: {ISO}
```

FLO returns these addresses to DWG (Direction 2); DWG reads the payload from `outputAddress`. FLO carries the pointer, not the payload.

---

## 5. Disposition Authority Matrix

Uniform across all packages — who may decide each disposition, and the ceremony required:

| Disposition | Who decides | Ceremony | Why |
|-------------|-------------|----------|-----|
| **Conform** | Package may auto-resolve | Low — logged, no sign-off | Lowest risk — restoring reality to the approved baseline |
| **Amend** | Requires gate / approval | High — design review + sign-off | Changes the baseline truth; the design itself moves |
| **Waive** | Requires explicit signed exception | Highest — named `owner` + mandatory future `expiry`; auto-reopens | Divergence persists by definition; must be time-boxed and owned |

A waiver missing `owner` or a future `expiry` is **invalid** — GCE rejects it and the entry stays `OPEN` (enforced in `ai-gce/.../drift/drift-register.md`).

---

## 6. Domain Ownership (Routing Authority)

The `domainTag → package` mapping is **FLO's authority alone** (declared in `ai-flo/.../pdlc-overlay.md` `driftRouting`). Packages do NOT hardcode which domains they own — they simply ask FLO and receive the addresses that belong to them. This keeps topology in one place (FLO) and both GCE (detection) and the packages (intake) free of it.

Reference mapping (canonical source is FLO's overlay):

| domainTag | Owning package |
|-----------|----------------|
| architecture · data · infrastructure | AI-ADLC |
| ux | AI-UXD |
| product | AI-POLC |

> **No `governance` domain.** GCE's own governance layer is not a DWG baseline element, so it cannot drift; stale/edited rules are GCE re-derivation, not drift. GCE participates only as the detector/register-writer, never as a drift-intake disposer.

---

## 7. Lifecycle & Verification

| State | Owner | Meaning |
|-------|-------|---------|
| `OPEN` / `OPEN-ADVISORY` | GCE register | Detected, unresolved |
| `ROUTED` | FLO routing-log (off-register) | FLO has recorded the owning package |
| `IN_DIGEST` | package state (off-register) | Package is digesting |
| `CLOSED` / `WAIVED` / `SELF-RESOLVED` / `EXPIRED` | GCE register | Reconciled from baseline `vN+1` |

GCE verification per disposition (from the `vN+1` ledger — never from FLO or the package):

| Disposition | GCE confirms by |
|-------------|-----------------|
| Conform | Re-measure element vs same baseline → drift gone |
| Amend | Re-measure element vs new `vN+1` element → matches |
| Waive | Read tolerated-divergence annotation → `owner` + unexpired `expiry` present |

---

## 8. Per-Package Digest (Where Each Implementation Lives)

The digest logic (how each package decides Conform/Amend/Waive) is package-owned:

| Package | Digest file | Domains |
|---------|-------------|---------|
| AI-ADLC | `ai-adlc/ai-adlc-rule-details/drift-intake/intake-digest.md` | architecture · data · infrastructure |
| AI-POLC | `ai-polc/ai-polc-rule-details/drift-intake/intake-digest.md` | product |
| AI-UXD | `ai-uxd/ai-uxd-rule-details/drift-intake/intake-digest.md` | ux |

Each digest file references THIS contract for the interface shape and implements only its domain-specific decision guidance.

---

## 9. Conformance Checklist

Every implementing package MUST:

- [ ] Pull drift by **asking FLO** for its address — never scan/own the `domainTag → package` map itself
- [ ] Read the drift body **directly from GCE's register (read-only)** — never receive it relayed by FLO
- [ ] Write its disposition to **its own artifact** — never to the drift register or the baseline
- [ ] Emit a `digest-ready` signal in its own state for DWG's FLO-brokered pickup
- [ ] Enforce the authority matrix (§5): Conform low-ceremony, Amend gated, Waive owner+expiry
- [ ] Learn of its drift ONLY by querying FLO (address) + reading GCE's register — never by inspecting FLO's internal `.flo/routing-log.md` (that is FLO's private courier record, not a drift source)
- [ ] Reference this contract (`drift-intake@1.0`) from its digest file

---

*Shared contract for the AI-* PDLC Family. Governs the receiving end of the drift-governance loop under the baseline-brokered pull model (INV-L4-006). Detection: AI-GCE. Brokering: AI-FLO (address-only). Re-baseline: AI-DWG. Disposition: the target package.*
