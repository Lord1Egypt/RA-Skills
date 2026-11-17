<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-POLC — Content Validation Rules

**Purpose:** Quality rules that every AI-POLC output must satisfy. The AI checks these before presenting any artifact to the user.

---

## Universal Rules (Apply to ALL Outputs)

### 1. Source-Driven Content

Every claim, scope item, or backlog entry MUST trace to one of:
- User's stated requirements (verbal or documented)
- PIP content (from AI-PILC)
- Architecture Package decisions (from AI-ADLC)
- UX research findings (from AI-UXD)
- User's explicit approval during this session

**Never fabricate scope.** If something seems needed but wasn't stated by the user or found in upstream input, flag it as a recommendation — don't silently add it to the backlog.

### 2. Generic — No Project-Specific Hardcoding

When working with **templates** (the package source), content must be 100% generic:
- Use `{placeholder}` for values filled during generation
- Use `_[TBD]_` for values the user provides later
- Zero project names, company names, or domain-specific content

When working with **runtime output** (actual project execution), content IS project-specific — that's the point. But still: derive from user input, never invent.

### 3. Value Justification

Every epic and prioritization decision must have explicit value justification:
- **Epic:** "This epic serves Goal X because {reason}. Without it, {consequence}."
- **Priority position:** "Ranked at position N because {model says X}. Rationale: {one sentence}."
- **Backlog admission:** Nothing enters the backlog without answering "why does this serve the product vision?"

Items without justification are flagged for user review, not silently admitted.

### 4. Acceptance Criteria Quality

All acceptance criteria (epic-level in Tier 1, story-level in Tier 2) must be:
- **Testable:** Someone can unambiguously determine pass/fail
- **Specific:** No "the system should work well" — measurable or observable
- **Independent of implementation:** Describe the WHAT, not the HOW

**Tier 1 (epic AC):** May be broader — "All 3 payment providers integrated and passing health checks" is acceptable at epic level.
**Tier 2 (story AC):** Must be Given/When/Then format — "Given a user with valid credentials, When they submit payment via Stripe, Then a confirmation email is sent within 5 seconds."

### 5. Traceability Links

Every artifact must maintain its traceability chain:
- **Epic → Goal:** Which product goal does this epic serve?
- **Epic → Release:** Which release is this epic sliced into?
- **Epic → Priority:** What position in the prioritization register?
- **DoR/DoD → Epic:** Which epics does this quality bar apply to?

If a link is missing, flag it before presenting the artifact.

### 6. Terminology Consistency

Within a single PBP:
- One term for each concept (don't alternate between "user story" and "requirement" and "feature")
- Priority model vocabulary used consistently (if WSJF, always use "cost of delay" and "job duration" — don't switch to MoSCoW terms mid-document)
- Epic naming convention consistent (if using `EPIC-NNN_{name}`, every epic follows that pattern)

### 7. Provenance Front-Matter

Every generated `.md` file must include:

```yaml
---
generatedBy: AI-POLC
generatedVersion: 1.0.0
source: {upstream-doc-path or "user-input"}
generatedOn: {ISO-date}
ownership: generated | hybrid | user
---
```

---

## Per-Artifact Rules

### Product Vision

- [ ] One sentence that passes the "a stranger can understand the product's purpose" test
- [ ] Measurable goals (not aspirational — each goal has a success metric)
- [ ] Time-bounded where appropriate (OKR cadence stated)
- [ ] Aligned to PIP business objectives (if PIP available)

### Epic Definitions

- [ ] Clear name (action-oriented: "Enable multi-currency payments" not "Payments")
- [ ] Goal linkage explicit
- [ ] Epic-level acceptance criteria (testable, boundary-defining)
- [ ] No implementation prescription (says WHAT, not HOW)
- [ ] Estimated complexity tier (S/M/L/XL) if methodology supports it

### Prioritization Register

- [ ] Model stated explicitly (WSJF / MoSCoW / value-effort / custom)
- [ ] Every ranked item has rationale (one sentence minimum)
- [ ] No duplicate rankings (each position is unique)
- [ ] Re-prioritization history visible (previous position, if changed)

### Release Plan

- [ ] Each release has: name/number, goal alignment, epic list, readiness criteria
- [ ] MVP scope clearly bounded (what's IN vs. what's explicitly OUT)
- [ ] Releases are ordered and time-hinted (even if rough: "Q3" / "Sprint 4-6")
- [ ] No orphan epics (every prioritized epic appears in exactly one release)

### DoR / DoD Checklists

- [ ] Each item is a verifiable checkbox (can answer yes/no)
- [ ] No vague items ("adequate" is not verifiable — "reviewed by PO" is)
- [ ] DoR and DoD are distinct (DoR = before dev starts; DoD = before increment ships)
- [ ] Appropriate for stated depth (Minimal DoR has 3-5 items; Comprehensive has 8-12)

### Governance Spine Entries

- [ ] ID follows `POLC-{TYPE}-{NNN}` format
- [ ] Phase column = "POLC" or "AI-POLC"
- [ ] Date in ISO format
- [ ] Status column present (Open / Closed / Superseded)
- [ ] Never edits another phase's entries

---

## Depth-Adapted Quality Bar

| Aspect | Minimal | Standard | Comprehensive |
|--------|---------|----------|---------------|
| Epic count | 3-8 | 5-15 | 10-30+ |
| AC per epic | 2-3 | 3-5 | 5-8 |
| Rationale depth | One sentence | Paragraph with model reference | Full analysis with alternatives considered |
| Risk items | 3-5 | 5-10 | 10-20 with scoring |
| Traceability | Goal→Epic only | Goal→Epic→Release | Goal→Epic→Story→AC→Release→Outcome |
| Stakeholder map | Names + interest level | Full power/interest matrix | Matrix + communication plan + cadence |

---

## Validation Checklist (Run Before Presenting Any Major Artifact)

Before presenting a stage output to the user, verify:

- [ ] Source-driven (nothing fabricated)
- [ ] Value-justified (nothing admitted without rationale)
- [ ] Traceable (links maintained up and down)
- [ ] Terminology consistent (no mixed vocabulary)
- [ ] Depth-appropriate (not over-engineering for minimal, not thin for comprehensive)
- [ ] Provenance header present
- [ ] No implementation prescription (WHAT, not HOW)
- [ ] Acceptance criteria are testable
- [ ] Governance spine entries properly formatted

---

*Reference this file when producing any output. Run the validation checklist at every stage gate.*
