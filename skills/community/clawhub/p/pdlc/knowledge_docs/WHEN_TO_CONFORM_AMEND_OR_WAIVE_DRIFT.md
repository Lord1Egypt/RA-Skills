# When to Conform, Amend, or Waive Drift

**Purpose:** Decision guide for the fork you hit when drift is detected — the design of record and the live workspace disagree, and you must choose one of exactly three dispositions. This explains which option fits your situation, the ceremony each demands, and the consequences of choosing wrong.

---

## The Decision You're Facing

AI-GCE has detected drift: a governed element in your approved baseline (an architecture choice, a data model, a UX rule, a product decision) no longer matches reality in the workspace. It logged the divergence and routed it to whoever owns that domain. Now that package — you, in the disposer's seat — must decide **one** of three things:

- **Conform** — the design is right; fix reality.
- **Amend** — reality is right; change the design.
- **Waive** — neither, for now; tolerate the gap with an owner and an expiry.

There is no fourth option and no "ignore." Every drift becomes a deliberate, recorded decision. The mechanics of how the decision travels back into the baseline are in `HOW_DRIFT_INTAKE_WORKS.md`; this guide is only about *choosing*.

---

## The One-Question Test

Start here:

> **Was the divergence a deliberate design change, or an unsanctioned slip?**

```
Did someone INTEND to change the design?
│
├─ NO  → the design still stands → the code is wrong
│         → CONFORM  (restore reality to the baseline)
│
└─ YES → the design genuinely moved
          │
          ├─ ...and we can adopt it now?
          │     → AMEND  (move the baseline truth, with a decision record)
          │
          └─ ...but we can't act on it this cycle?
                → WAIVE  (time-boxed, owned exception)
```

---

## Conform — The Design Is Still Correct

**Choose Conform when** the approved design is right and reality simply drifted from it — an implementation shortcut, an accidental boundary crossing, a library swap nobody decided on. Nothing about the design should change; the code must come back to it.

- **Ceremony:** Low. The package records the restore expectation; no design change, no sign-off.
- **What you write:** a note in your own artifact that the element should be restored to its baseline definition; emit "digest ready."
- **How it closes:** once reality is corrected, GCE re-measures against the *same* baseline and the drift is gone.

**Example:** a service imports across a module boundary the architecture forbids, and there was no decision to move that boundary. The boundary stands → **Conform**: record the restore expectation; the import gets removed; the entry closes.

**Don't Conform when** the team actually wants the new reality — forcing code back to a design everyone has moved past just creates the same drift again next cycle. That's an Amend.

---

## Amend — The Design Genuinely Changed

**Choose Amend when** the divergence reflects a real, intended evolution — the team decided the new API shape, the new data model, the new stack is correct. The baseline *truth itself* should move to match.

- **Ceremony:** High. This changes the design of record, so it needs a gate/approval and a decision record. In the architecture domain, an Amend to a technology choice, component boundary, or API contract **always** produces an ADR (context → options → decision → consequences) — an architectural change without a decision record isn't allowed.
- **What you write:** update the source design artifact, add/replace the governing decision record, emit "digest ready" with the changed element and rationale.
- **How it closes:** AI-DWG bakes the change into the next baseline version; GCE re-measures against the *new* element and confirms they match.

**Example:** the API design declares path-based versioning, the code uses header-based, and the team confirms header-based is now the intended standard → **Amend**: update the API design doc, write the versioning ADR, signal ready; the baseline moves; the entry closes.

**Don't Amend when** the change was accidental or merely convenient — moving the baseline to bless every slip erodes the design's authority. If nobody deliberately decided it, it's a Conform.

---

## Waive — Tolerated, Owned, and Time-Boxed

**Choose Waive when** the divergence is acknowledged debt: you can't restore the design and can't adopt the change this cycle, but the gap is tolerable for a bounded time.

- **Ceremony:** Highest. A waiver is a signed exception and **must** carry a named owner and a mandatory future expiry, scoped to exactly what's tolerated. A waiver missing an owner or a future expiry is invalid — GCE rejects it and the entry stays open. It **auto-reopens** on expiry, so it can never quietly become permanent.
- **What you write:** the waiver (owner + future expiry + scope) in your own state; emit "digest ready."
- **How it closes:** GCE confirms the annotation (owner present, expiry unexpired) and suppresses the drift until expiry, at which point it resurfaces for a fresh decision.

**Example:** a legacy module still uses the pre-migration library; migrating is out of scope this sprint → **Waive**: owner = the platform lead, expiry = end of the current sprint, scope = that module only. It resurfaces automatically at sprint end.

**Don't Waive when** you simply haven't decided — a waiver is a *decision to tolerate*, not a way to defer deciding. And never leave off the expiry; an open-ended waiver is how silent drift comes back.

---

## Quick Comparison

| | Conform | Amend | Waive |
|---|---------|-------|-------|
| **Design of record** | Unchanged | Changes | Unchanged |
| **What moves** | The code (back to design) | The baseline (to match reality) | Nothing (gap tolerated) |
| **Ceremony** | Low — logged | High — gate + decision record | Highest — signed, owned, expiring |
| **Best when** | Accidental slip | Deliberate, adoptable change | Known debt, can't act yet |
| **Risk if misused** | Re-drifts if team really wanted the change | Erodes design authority if used for slips | Becomes permanent debt if expiry is missing |

---

## The Guiding Principle

Ceremony scales with risk. **Conform** restores an approved truth — the safest move, so the lightest. **Amend** moves the truth — that's a decision, so it's gated and recorded. **Waive** tolerates a known gap — the riskiest, so it demands the most: a name against it and a date it dies. When unsure between Conform and Amend, ask whether a human *decided* to change the design; when unsure between Amend and Waive, ask whether you can *act* on that decision now.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Drift Intake Works | `knowledge_docs/HOW_DRIFT_INTAKE_WORKS.md` |
| When to Trigger Re-Derivation | `knowledge_docs/WHEN_TO_TRIGGER_REDERIVATION.md` |
| What If Architecture Changes Break Governance | `knowledge_docs/WHAT_IF_ARCHITECTURE_CHANGES_BREAK_GOVERNANCE.md` |
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |
| Lifecycle of an Architecture Decision | `knowledge_docs/LIFECYCLE_OF_AN_ARCHITECTURE_DECISION.md` |
| Why Change Management Matters | `knowledge_docs/WHY_CHANGE_MANAGEMENT_MATTERS.md` |

---

*Knowledge Document | Created: 2026-07-05 | Updated: 2026-07-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
