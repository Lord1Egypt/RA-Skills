# How Drift Intake Works

**Purpose:** Explains how the AI-* Family handles *midflight design drift* — when the code in a live workspace quietly diverges from the approved design baseline — through a single, closed reconciliation loop: AI-GCE detects and logs it, AI-FLO routes it by address, the owning design package digests it into a decision (Conform / Amend / Waive), AI-DWG bakes that decision into a new baseline, and AI-GCE closes it. One writer per step, reconciled through the baseline.

---

## What Drift Intake Solves

Every project starts from an approved design — an architecture, a UX design, a product backlog. That design becomes the **baseline**: the governed truth the workspace is measured against. But as delivery proceeds, reality moves. A team switches a library, a service reaches across a boundary the design forbids, an API changes shape. When those changes happen **without acknowledgment**, the design on paper and the code in the repo silently disagree. That gap is **drift**.

The danger is not the change itself — designs are supposed to evolve. The danger is *silence*: governance keeps enforcing a design that no longer matches reality, and nobody decided that on purpose.

Drift intake is the family's mechanism for making every divergence an explicit, owned decision. Nothing is auto-fixed and nothing is ignored — each drift is routed to whoever owns that design domain, digested into a deliberate disposition, and reconciled back into the baseline so governance and reality re-align.

---

## The Roles: One Job Each

Drift intake is a shared discipline, not a package. Several packages each own exactly one part of the loop:

| Package | Role in the loop | Writes |
|---------|------------------|--------|
| **AI-GCE** | **Detector.** Measures reality against the baseline, classifies and tags each divergence, logs it to the drift register, and later closes it | the drift register |
| **AI-FLO** | **Broker.** Holds the "which domain belongs to which package" map; hands each package the *address* of its drift | the routing log |
| **AI-ADLC / AI-POLC / AI-UXD** | **Disposers.** Digest their domain's drift and decide Conform / Amend / Waive | their own artifacts |
| **AI-DWG** | **Re-baseliner.** Pulls each decision and bakes it into the next baseline version | the baseline |

**Single-writer rule:** each artifact has exactly one writer. GCE writes the register, FLO writes the routing log, each design package writes its own output, DWG writes the baseline. No component ever writes another's artifact. That is what keeps the loop honest.

> Note on GCE: it is the detector and register-writer, never a disposer. Its own governance layer isn't part of the baseline, so it can't "drift" — a stale or edited rule is a re-derivation matter, not drift.

---

## The Governing Principle

> **Intake is a PULL, brokered by address, reconciled through the baseline.**

Nothing is ever *pushed* to a package. A package asks the router "any drift for me?"; the router returns the **address** of the drift (a pointer, never the body); the package reads the drift **directly from the register** (read-only), digests it, writes its decision to **its own artifact**, and emits a "digest ready" signal. AI-DWG later pulls that signal and bakes the decision into the next baseline. AI-GCE learns the resolution **only** from that new baseline — never from the router or the package directly.

---

## The Loop, End to End

```
① Package → FLO:  "Any drift for me?"
② FLO → Package:  ADDRESS only  { driftId, address: "<register>#DRF-NNN" }
③ Package → GCE:  reads the full drift record DIRECTLY from the register (READ-ONLY)
④ Package:        digests → decides Conform / Amend / Waive
⑤ Package:        writes disposition to its OWN artifact + emits "digest ready"
⑥ DWG → FLO:      "Any digested drift ready?" → FLO returns ready addresses
⑦ DWG:            reads each disposition → bakes it into baseline vN+1
⑧ GCE:            reads vN+1 → verifies → CLOSES the register entry
```

The **detection path** adds one read: the package reads the drift body from GCE at the address FLO supplied. The **return path** is `package → FLO → DWG → GCE` — GCE is the *last* actor and learns the outcome only from the baseline DWG wrote.

A package **never** writes the register, writes the baseline, reads the router's private routing log, or pushes to another package. A package **only** reads its drift from the register (read-only), writes its own artifact, and emits its own "digest ready" signal.

---

## Step 1 — Detect (AI-GCE)

GCE is the sole detector. It reads the workspace manifest to locate the baseline and the reality artifacts, then measures every governed element against its approved definition. For each divergence it:

1. **Checks suppression** — skips anything already waived and unexpired, or re-baselined this cycle (a guard against thrashing).
2. **Classifies** — `HARD` (a locked element; blocks the gate) or `ADVISORY` (informs, never blocks).
3. **Tags a domain** — `architecture` · `data` · `infrastructure` · `ux` · `product` — the tag that decides routing.
4. **Logs** a register entry pinned to the current baseline version.

Detection is deliberately **not** continuous — it runs on demand, at session end, and as a gate pre-check. Constant re-measuring would fight the delivery flow, so drift is checked at natural checkpoints. GCE detects and logs; it never fixes.

---

## Step 2 — Route by Address (AI-FLO)

The router alone owns the `domainTag → package` map. Packages do **not** hardcode which domains they own — they ask the router and receive only the addresses that belong to them. Keeping topology in one place means both the detector and the disposers stay free of routing knowledge.

The reference mapping (the router's overlay is the canonical source):

| domainTag | Owning package |
|-----------|----------------|
| architecture · data · infrastructure | AI-ADLC |
| ux | AI-UXD |
| product | AI-POLC |

Crucially, the router carries **only the pointer**, never the drift body. It reads just enough of the register envelope (id, domain tag, status) to resolve the owner, then hands back an address. The package fetches the body itself. There is no `governance` domain — governance can't drift, so GCE never appears as a routing target.

---

## Step 3 — Digest into a Disposition (the owning package)

Having read the drift body, the owning package maps the drifted element to its design intent and chooses exactly one disposition. What differs between packages is only the *decision logic* — the interface is identical family-wide.

| Disposition | Meaning | Who decides / ceremony |
|-------------|---------|------------------------|
| **Conform** | The approved design is still correct; reality is wrong and must be brought back. No design change. | Package may auto-resolve — **low ceremony**, logged |
| **Amend** | The design intent genuinely changed; the baseline truth itself should move. | Requires a gate / approval — **high ceremony**, design review + sign-off |
| **Waive** | The divergence is tolerated for now as acknowledged debt. | Requires a signed exception — **highest ceremony**: named owner + mandatory future expiry; auto-reopens on expiry |

The ceremony scales with risk: Conform restores the approved truth (safest), Amend moves the truth (needs a decision), Waive tolerates a known gap (must be time-boxed and owned). A waiver missing an owner or a future expiry is **invalid** — the detector rejects it and the entry stays open.

**Example (architecture domain):** an API element is declared with path-based versioning, but the code uses header-based versioning and the team confirms header-based is now intended → **Amend**: update the API design artifact, record a decision (an architectural change is a decision, not an edit), and signal ready. Had there been no decision to change it → **Conform**: the design stands, restore the code. Were migration simply out of scope this sprint → **Waive**: named owner, expiry at sprint end, scoped to that module.

---

## Step 4 — Emit "Digest Ready" (the owning package)

The package writes its disposition to **its own artifacts** and emits a machine-readable "digest ready" signal in its own state:

```yaml
digest-ready:                 # in the package's own state file
  - driftId: DRF-003
    dispositionType: amend
    outputAddress: "<package-output>#DRF-003"   # where DWG reads the payload
    readyAt: {ISO}
```

The router later returns these addresses to AI-DWG; DWG reads the payload from `outputAddress`. Again, the router carries the pointer, not the payload — and the package has written only its own artifact, never the register or the baseline.

---

## Step 5 — Re-baseline (AI-DWG) and Close (AI-GCE)

AI-DWG pulls each ready disposition (via the router) and bakes it into baseline `vN+1` with a ledger entry. Only then does AI-GCE act again: it reads the new baseline and verifies the outcome — never trusting the disposition blindly, always re-measuring.

| Disposition | GCE confirms by |
|-------------|-----------------|
| **Conform** | Re-measure the element vs the same baseline → drift is gone |
| **Amend** | Re-measure the element vs the new `vN+1` element → they match |
| **Waive** | Read the tolerated-divergence annotation → owner present + expiry unexpired |

The register entry then moves to its final state. GCE is the last actor and learns the resolution **only** from the baseline DWG produced — closing the loop that GCE opened.

---

## The Lifecycle of One Drift Entry

| State | Owned by | Meaning |
|-------|----------|---------|
| `OPEN` / `OPEN-ADVISORY` | GCE register | Detected, unresolved |
| `ROUTED` | FLO routing log | Owning package resolved |
| `IN_DIGEST` | package state | Package is deciding |
| `CLOSED` / `WAIVED` / `SELF-RESOLVED` / `EXPIRED` | GCE register | Reconciled from the new baseline |

The full reconciliation chain is a macro loop: **GCE (detect) → FLO → package → FLO → DWG → GCE (close via baseline)**.

---

## Why It Works This Way

| Design choice | Why it matters |
|---------------|----------------|
| **Pull, never push** | Each package controls when it digests drift; nothing interrupts it uninvited |
| **Address-only routing** | The body has exactly one home (the register); the router can't become a second, drifting copy |
| **Single writer per artifact** | No component can corrupt another's data — the loop's integrity is structural, not a matter of discipline |
| **Reconcile through the baseline** | GCE learns outcomes only from the baseline, so the design of record and enforcement can never silently disagree |
| **Ceremony scales with risk** | Restoring truth is cheap; moving truth needs a decision; tolerating a gap must be owned and time-boxed |
| **Detect at checkpoints, not continuously** | Drift checks happen at natural pauses, so governance never fights the delivery flow |

---

## Related Documents

| Document | Location |
|----------|----------|
| How the Flow Orchestrator Works | `knowledge_docs/HOW_FLOW_ORCHESTRATOR_WORKS.md` |
| How GCE Compliance Audit Works | `knowledge_docs/HOW_GCE_COMPLIANCE_AUDIT_WORKS.md` |
| How GCE Re-Derivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| Pattern: Non-Destructive Reconciliation | `knowledge_docs/PATTERN_NON_DESTRUCTIVE_RECONCILIATION.md` |
| Pattern: Downstream Signaling | `knowledge_docs/PATTERN_DOWNSTREAM_SIGNALING.md` |
| When to Trigger Re-Derivation | `knowledge_docs/WHEN_TO_TRIGGER_REDERIVATION.md` |
| What If Architecture Changes Break Governance | `knowledge_docs/WHAT_IF_ARCHITECTURE_CHANGES_BREAK_GOVERNANCE.md` |
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |

---

*Knowledge Document | Created: 2026-07-05 | Updated: 2026-07-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
