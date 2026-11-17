# Pattern: Gate Before Transition

**Purpose:** Documents the reusable design pattern where human approval is required before the workflow advances to the next stage — ensuring the user stays in control and mistakes are caught before compounding.

---

## The Pattern

```
STAGE N produces output
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GATE (human decision point)                                         │
│                                                                      │
│  Present: output summary + key decisions + quality indicators        │
│                                                                      │
│  Options:                                                            │
│  ├── ✅ Approve → advance to Stage N+1                               │
│  ├── 🔄 Revise → stay at Stage N, address feedback                   │
│  ├── ⏸️ Pause → save state, resume later                             │
│  └── ❌ Reject → roll back, try different approach                   │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼ (only on Approve)
STATE FILE UPDATED → Stage N+1 begins
```

**One sentence:** No stage transition without human approval — the AI proposes, the human disposes.

---

## Where It's Used

| Package | Gates | Gate Behavior |
|---------|:-----:|--------------|
| **AI-PILC** | 13 (every stage) | Must approve before next stage begins |
| **AI-ADLC** | 13 (every stage) | Must approve; extension opt-in gates at specific stages |
| **AI-ILC** | 6 (every stage) | Must approve; Stage 5 is the DECISION gate (go/no-go) |
| **AI-POLC** | Per-stage | Must approve priority order before release slicing |
| **AI-UXD** | Per-stage | Must approve persona/journey before design system |
| **AI-DWG** | 1 (final review) | Review full generated workspace before activation |
| **AI-GCE** | Strategy stages only | Observation phase is continuous (no gates) |
| **AI-TGE** | Strategy stages only | Same hybrid model as AI-GCE |

---

## Why This Pattern Exists

**The problem it solves:** AI assistants can produce output that LOOKS correct but contains subtle errors — wrong assumptions, misinterpreted constraints, scope drift. Without gates, errors compound across stages until the final output is fundamentally wrong.

**The compounding error effect:**
```
Stage 1: Slight misinterpretation of requirement (unnoticed)
Stage 3: Architecture decision based on misinterpretation
Stage 5: Component design assumes wrong architecture
Stage 8: Generated workspace implements wrong patterns
Stage 10: Governance enforces wrong rules

Cost to fix at Stage 1: 5 minutes (correct the misinterpretation)
Cost to fix at Stage 10: Days (re-derive everything from Stage 1 forward)
```

Gates prevent compounding by catching errors at the EARLIEST possible point.

---

## Gate Anatomy

Every gate presents:

| Element | Purpose |
|---------|---------|
| **Output summary** | What this stage produced (key artifacts, decisions) |
| **Decisions made** | Explicit list of choices the AI made (for user validation) |
| **Assumptions** | What the AI assumed that might be wrong |
| **Quality indicators** | Completeness signals, gap identification |
| **Options** | Approve / Revise / Pause / Reject |

### Gate Options

| Option | Meaning | State Impact |
|--------|---------|:------------:|
| **Approve** | Output is correct, proceed | Stage N → completed, advance to N+1 |
| **Revise** | Output needs changes, stay here | Stage N remains active, iterate |
| **Pause** | Good so far, but I need to stop | State saved, resume later |
| **Reject** | Fundamental problem, go back | May return to earlier stage |

---

## The State-Before-Transition Rule

**Critical:** State file updates happen AFTER gate approval but BEFORE presenting the next stage:

```
1. Stage N output produced
2. Gate presented to user
3. User approves ✅
4. State file updated: Stage N → completed (with timestamp)
5. Current Stage → N+1
6. THEN Stage N+1 begins
```

**Why this order matters:** If the session crashes between stages, the state reflects the last COMPLETED stage — enabling clean resume. The user never loses approved work.

---

## Gate Intensity Varies by Depth

| Depth Level | Gate Behavior |
|-------------|--------------|
| **Minimal** | Lightweight confirmation: "Looks good? [Y/N]" |
| **Standard** | Summary + key decisions + approve/revise |
| **Comprehensive** | Detailed review: all artifacts, all assumptions, explicit sign-off |

The gate always EXISTS (can't be skipped) but its WEIGHT varies with depth.

---

## Gates vs. Continuous Observation

Not all packages use gates for all phases:

| Mode | Gate Behavior | Used By |
|------|--------------|---------|
| **Gated (interactive)** | Every stage requires approval | PILC, ADLC, ILC (all stages) |
| **Hybrid (gate + continuous)** | Strategy gates + continuous observation | GCE, TGE (gate strategy, observe execution) |
| **Single-gate (generator)** | One review at end of generation | DWG (approve full output) |

**Design rule:** Use gates where decisions are being made (strategy, design). Use continuous observation where execution is being monitored (enforcement, test tracking).

---

## Implementation Rules

1. **Gates are non-negotiable** — no workflow ever auto-advances without human confirmation. Even at Minimal depth.

2. **Gate output is self-contained** — the user can make an approval decision from the gate summary alone, without re-reading all prior stages.

3. **Revision loops are unlimited** — a gate can be revised as many times as needed. No "three strikes" limit.

4. **State update is atomic** — either the gate passes and state advances, or it doesn't and state stays. No intermediate states.

5. **Gate approval is timestamped** — audit trail shows who approved what and when. Enables traceability.

6. **Rejection allows navigation** — "go back to Stage 3" is valid at any gate. The workflow supports non-linear correction.

---

## When to Apply This Pattern

Apply when:
- [ ] The workflow produces output that builds on prior stages (compounding risk)
- [ ] AI may misinterpret user intent (all AI-assisted workflows)
- [ ] The cost of error increases with distance from the source
- [ ] Human judgment is required (not just computation)
- [ ] The workflow spans multiple sessions (state must survive)

Don't apply when:
- The operation is fully automated with no human in the loop
- Output is easily reversible (undo is cheaper than review)
- The "gate" would be trivial (auto-approve every time → remove the gate)
- Observation mode (monitoring, not deciding)

---

## Related Documents

| Document | Location |
|----------|----------|
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| Why Spec Before Code Matters | `knowledge_docs/WHY_SPEC_BEFORE_CODE_MATTERS.md` |
| How to Initiate a Project | `knowledge_docs/HOW_TO_INITIATE_A_PROJECT.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
