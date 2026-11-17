# How Gates and Approvals Work

**Purpose:** Explains the human-in-the-loop gate mechanism used across all AI-* lifecycle packages — how gates enforce user authority, prevent auto-progression, and maintain governance discipline at every decision point.

---

## What Gates Are

A gate is a structured approval point at the end of every stage in an AI-* lifecycle workflow. The AI presents its work, the user reviews it, and the workflow only advances with explicit user approval. Gates are non-negotiable — no package ever auto-progresses past a gate.

```
┌──────────────────────────────────┐
│  STAGE N EXECUTION                │
│                                   │
│  AI produces the deliverable      │
│  following stage detail rules     │
│                                   │
└───────────────┬──────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│  GATE                             │
│                                   │
│  Summary of what was produced     │
│  Key decisions made               │
│  Items logged to registers        │
│                                   │
│  Options:                         │
│  (a) Approve → proceed            │
│  (b) Revise → iterate             │
│  (c) Reject → backtrack           │
│                                   │
│  ⏸️ WORKFLOW PAUSED               │
│  (awaiting user decision)         │
│                                   │
└───────────────┬──────────────────┘
                │ User chooses
                ▼
┌──────────────────────────────────┐
│  (a) → Advance to Stage N+1      │
│  (b) → Iterate on current stage  │
│  (c) → Return to earlier stage   │
└──────────────────────────────────┘
```

**Key principle:** Gates ensure human authority. The AI proposes, the human decides. No governance artifact is finalized without explicit user confirmation.

---

## Why Gates Exist

| Reason | What It Prevents |
|--------|-----------------|
| Human authority | AI making irreversible decisions without oversight |
| Quality assurance | Catching errors before they compound downstream |
| Audit trail | Every advance is a traceable, approved decision |
| Course correction | Allowing the user to redirect before investment deepens |
| Governance discipline | Ensuring PMO/Architecture rigor at every step |

---

## Gate Types

### Stage Gate (Every Stage)

The default gate — present after every stage completes:

```
✅ Stage {N} — {Stage Name} complete.

📄 Produced: {artifact name}
📋 Decisions logged: {count}
📊 Key findings: {summary}

Options:
(a) Approve — proceed to {next stage name}
(b) Revise — provide feedback for this deliverable
(c) Reject — return to {previous stage} with new direction
```

### Phase Gate (Between Phases)

A heavier gate marking the boundary between major workflow phases. Includes a phase completion summary:

```
✅ {PHASE NAME} PHASE COMPLETE

📊 Summary:
   • Documents produced: {n}
   • Decisions logged: {n}
   • Assumptions registered: {n}
   • Open items: {n}

Ready to proceed to {NEXT PHASE NAME}?
  [Yes / Revisit {current phase} / Stop here]
```

### Adaptive Gates (Depth-Dependent)

For simple projects (Minimal depth), some stage gates are lighter:
- Auto-proceed after brief confirmation ("Looks good? [Yes/No]")
- No formal options presentation
- Reduced summary

For complex projects (Comprehensive depth):
- Full formal gate with checklist
- Extended review period
- May require multiple stakeholders

---

## Gate Behavior Rules

| Rule | Enforcement |
|------|-------------|
| Never auto-progress | AI MUST pause and wait for user input at every gate |
| Always present options | User always has Approve / Revise / Reject available |
| Log every gate decision | Gate passage logged in Decision Register with timestamp |
| Update state after approval | State file updated ONLY after user approves |
| Iteration is unlimited | User can request revisions as many times as needed |
| Reject enables backtracking | User can return to any previous stage |

---

## What Happens at Each Option

### (a) Approve

1. Gate decision logged in Decision Register
2. State file updated: stage marked complete with timestamp
3. Deliverable finalized (saved to output folder)
4. Workflow advances to next stage
5. Next stage's detail file loaded

### (b) Revise

1. AI asks for specific feedback: "What would you like changed?"
2. User provides feedback (text, specific corrections, direction)
3. AI iterates on the deliverable
4. Re-presents the updated version
5. Gate is presented again (same options)
6. Change logged in Change Register (if scope changed) or Decision Register (if approach changed)

### (c) Reject

1. AI asks: "Which stage should we return to?"
2. User specifies target stage (or "start this phase over")
3. State file updated: stages beyond target marked as "needs redo"
4. Issue logged in Issue Register (what went wrong)
5. Workflow returns to the specified stage

---

## Gate Granularity by Package Type

| Package Type | Gate Frequency | Rationale |
|-------------|---------------|-----------|
| Lifecycle (AI-PILC, AI-ADLC) | Every stage + phase boundaries | Interactive; user makes decisions throughout |
| Generator (AI-DWG) | Before generation + after generation | One-shot; user confirms input and reviews output |
| Engine (AI-GCE) | Before derivation + after derivation | One-shot; user reviews impact and output |

Generators and engines have fewer gates because they don't have multi-stage linear progression — they read input, transform, and output in one pass.

---

## Gates in the Question Format

During stage execution, structured decisions also use a gate-like pattern:

```markdown
### Q-{nn}: {Question Title}

**Context:** {Why this question matters}

**Options:**
- (a) {Option A}
- (b) {Option B}
- (c) {Option C}

**Recommended:** Option {x}
**Rationale:** {Why recommended}

**Your Decision:** _[awaiting input]_
```

These are micro-gates within a stage — the workflow pauses at each decision point until the user responds.

---

## Phase Gates as Governance Checkpoints

Phase boundaries serve as natural checkpoints for governance reporting:

| Checkpoint | What's Reported |
|-----------|-----------------|
| Inception → Assessment | Source validated, requirements structured |
| Assessment → Justification | Feasibility confirmed, priority set |
| Justification → Authorization | Business case approved, investment justified |
| Authorization → Planning | Charter approved, authority granted |
| Planning → Mobilization | All plans complete, resources confirmed |
| Mobilization → Complete | Package assembled, handoff ready |

These map directly to AI-GCE's phase gate rules (PG-* category) when governance enforcement is active.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Auto-approving to "go faster" | Compounds errors; defeats governance purpose |
| Skipping phase gates | Loses the governance checkpoint; audit trail breaks |
| Presenting gates without summaries | User can't make informed decisions |
| Making gates blocking without escape | User must always have Reject/backtrack option |
| Different gate formats per package | Breaks user expectation; learning doesn't transfer |

---

## Related Documents

| Document | Location |
|----------|----------|
| AI-PILC gates (in core workflow) | `ai-pilc/ai-pilc-rules/core-workflow.md` |
| AI-ADLC gates (in core workflow) | `ai-adlc/ai-adlc-rules/core-workflow.md` |
| Question format guide (AI-PILC) | `ai-pilc/ai-pilc-rule-details/common/question-format-guide.md` |
| AI-GCE phase gate rules | `ai-gce/ai-gce-rule-details/generators/phase-gates-generator.md` |
| Depth Levels (gate adaptation) | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
