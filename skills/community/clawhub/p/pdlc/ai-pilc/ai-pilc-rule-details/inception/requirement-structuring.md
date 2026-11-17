<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Requirement Structuring

## Stage: 3 of 16
## Phase: 🔵 INCEPTION
## Execution: ALWAYS

---

## Purpose

Transform the raw source material into a professional, structured Requirement Intake Form — the standard entry point for any project in a PMO pipeline. This form becomes the canonical reference for all subsequent stages.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Separate concerns cleanly — functional, non-functional, constraints, and assumptions go in distinct categories
- For every field, cite the source statement that supports it; mark unsupported fields as `_[TBD]_`
- Convert vague phrasing ("fast", "scalable", "user-friendly") into specific, testable statements — or flag for clarification if you can't
- Identify dependencies between requirements as you structure them

### Anti-Patterns for This Stage
- Do NOT merge functional and non-functional requirements into one bucket
- Do NOT fill a field with plausible-sounding content the source doesn't support

### Quality Check
A good output at this stage sounds like:
- "Each intake field traces to a source line; 3 fields marked `_[TBD]_` with Action Items created; 'fast' rewritten as 'P95 < 500ms'..."

---

## Step-by-Step Execution

### Step 1: Extract Information from Source

Read the source document (ingested in Stage 2) and extract content into these categories:

| Category | What to Extract | If Missing |
|----------|----------------|------------|
| **Requestor** | Who is asking for this? Name, role, department, contact | Mark `_[TBD]_`; create Action Item |
| **Business Need** | Problem statement, current pain, impact of inaction | Synthesize from context if implied |
| **Expected Outcome** | What success looks like; desired end-state | Infer from stated requirements |
| **Functional Requirements** | Specific capabilities the solution must have | List what's stated; flag gaps |
| **Non-Functional Requirements** | Quality attributes: performance, security, scalability, etc. | Note absence; flag for Stage 4 |
| **Constraints** | Hard limits: technology, budget, timeline, regulatory | List stated; note assumed |
| **Assumptions** | What the source takes for granted | Make implicit assumptions explicit |
| **Stakeholders** | Named people, roles, departments, decision authority | List all mentioned |
| **Preliminary Estimates** | Any budget, timeline, or team size indicators | Mark `_[TBD]_` if absent |
| **Attachments/References** | Other documents referenced by the source | List with availability status |

---

### Step 2: Classify and Organize Requirements

#### Functional Requirements Organization

Group functional requirements by logical domain or capability area:

```markdown
### Functional Requirements

#### {Domain 1 — e.g., "User Management"}
1. {Requirement — concise, testable statement}
2. {Requirement}

#### {Domain 2 — e.g., "Reporting & Analytics"}
3. {Requirement}
4. {Requirement}
```

**Rules for requirement statements:**
- Each requirement should be a single, testable capability
- Use active voice: "The system shall..." or "Users can..."
- Avoid compound requirements (split "X and Y" into two items)
- Number sequentially across all domains
- If source uses different numbering, maintain a cross-reference

#### Non-Functional Requirements Organization

Organize by quality attribute:

| Category | NFR Statement | Target/Metric | Priority |
|----------|--------------|---------------|:--------:|
| Performance | {statement} | {measurable target} | {H/M/L} |
| Security | {statement} | {standard/certification} | {H/M/L} |
| Scalability | {statement} | {capacity target} | {H/M/L} |
| Availability | {statement} | {uptime %} | {H/M/L} |
| Accessibility | {statement} | {standard level} | {H/M/L} |
| Compliance | {statement} | {regulation/standard} | {H/M/L} |
| Usability | {statement} | {metric if available} | {H/M/L} |
| Maintainability | {statement} | {constraint} | {H/M/L} |

---

### Step 3: Identify Scope Boundaries

From the source, explicitly separate:

**In Scope:**
| # | Item | Description | Source Reference |
|---|------|-------------|:---------------:|
| 1 | {capability} | {brief description} | §{section} |

**Out of Scope (if stated):**
| # | Item | Reason for Exclusion | Source Reference |
|---|------|---------------------|:---------------:|
| 1 | {excluded item} | {reason — deferred, not needed, separate project} | §{section} |

**Unclear / Not Addressed:**
| # | Item | Why It's Ambiguous | Resolution Needed |
|---|------|-------------------|:-----------------:|
| 1 | {item} | {source says X in one place and Y in another} | Stage 4/5 |

---

### Step 4: Produce the Requirement Intake Form

Using the template `templates/requirement-intake-form.md`, populate all sections:

**Section 1: General Information**
- Request ID: Derive from the `Project ID` minted at Stage 1 (read from `pilc-state.md`) — reuse the same `{ABBREV}-{YEAR}-{NNN}` with a `REQ-` prefix (e.g., Project ID `PRJ-CRM-2026-001` → Request ID `REQ-CRM-2026-001`). It is the intake-time handle for the **same identity thread** — do not generate an independent sequence.
- Date, requestor details, department, contact

**Section 2: Requirement Summary**
- Project/initiative name
- Requirement title (concise)
- Category: New Capability / Enhancement / Replacement / Compliance / Infrastructure
- Priority (requestor's view): Critical / High / Medium / Low
- Desired dates (if known)

**Section 3: Business Need**
- Problem statement (from extraction)
- Expected business outcome (bulleted)
- Impact if NOT addressed (consequences of inaction)

**Section 4: Requirements Description**
- Functional requirements (organized by domain)
- Non-functional requirements (table format)
- Constraints & assumptions (bulleted)

**Section 5: Stakeholders & Approvals**
- Table of known stakeholders with role and department

**Section 6: Preliminary Estimates**
- Budget range, duration, team size (if known; `_[TBD]_` if not)
- Systems/tools impacted

**Section 7: Attachments & References**
- Checklist of available reference documents

**Section 8: PMO Use Only**
- Received date
- Assigned analyst: `_[To be assigned]_`
- Screening decision: `_[Pending — Phase 2]_`

---

### Step 5: Quality Check

Before presenting to user, validate the intake form:

- [ ] All sections present (even if some contain `_[TBD]_`)
- [ ] No invented requirements — every item traceable to source
- [ ] Requirement statements are singular, testable, and clear
- [ ] No duplicate requirements (same thing stated differently)
- [ ] Constraint vs. requirement distinction is correct (constraints limit; requirements demand)
- [ ] Stakeholder names match any names in the source
- [ ] Request ID derived from the Stage-1 Project ID (same `{ABBREV}-{YEAR}-{NNN}`, `REQ-` prefix) — not an independent sequence
- [ ] Cross-references to source document are correct

---

### Step 6: Present for Review

Display to the user:

```markdown
## Review: Requirement Intake Form

I've structured your source material into a formal Requirement Intake Form.

**Key highlights:**
- {n} functional requirements identified across {m} domains
- {n} non-functional requirements captured
- {n} constraints documented
- {n} stakeholders identified
- Scope boundaries: {n} in-scope items, {n} explicitly excluded, {n} unclear

**Notable observations:**
- {Any significant gap, ambiguity, or concern — 1-3 bullets}
- {Items that required interpretation — what was assumed}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Intake form captures my intent; proceed to Assessment
- (b) **Request changes** — Adjustments needed (tell me what)
- (c) **Add more** — I have additional requirements not in the source
- (d) **Major issues** — Significant misunderstanding; let's discuss
```

---

### Step 7: Iterate (if needed)

If user requests changes:
1. Ask specifically what to add, remove, or modify
2. Apply changes
3. Re-validate (Step 5)
4. Re-present summary
5. Repeat until approved

If user adds new requirements not in the source:
1. Accept and integrate
2. Note in the form: "Added by {user} during structuring — not in original source document"
3. These additions have equal standing going forward

---

### Step 8: Finalize and Transition

Upon approval:

1. Save final version to output folder:
   - Numbered: `{output_root}/01_Requirement_Submission/Requirement_Intake_Form.md`
   - Flat: `{output_root}/pilc-docs/inception/Requirement_Intake_Form.md`
2. Update state file:
   - Stage 3: ✅ Done
   - Current Phase: ASSESSMENT
   - Current Stage: 4
3. Log in Decision Log:
   - D-003: "Requirement Intake Form approved. {n} functional reqs, {m} NFRs, {p} constraints captured."
4. Log lesson (if applicable):
   - LL-001 (if source was unclear): "Source document required significant interpretation — recommend stakeholder review of intake form before proceeding."

Display transition:

```
✅ Stage 3: Requirement Structuring — Complete

📋 Intake Form: {n} functional + {m} non-functional requirements
📄 Saved to: {file_path}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ INCEPTION PHASE COMPLETE (Stages 1-3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next → ASSESSMENT PHASE
Stage 4: Requirements Analysis — I'll analyze the structured requirements
for gaps, ambiguities, and inconsistencies.

Proceeding...
```

---

## Handling Different Source Qualities

### High-Quality Source (Completeness >80%)

- Extraction is mostly direct mapping
- Few interpretations needed
- Intake form will be comprehensive
- Note: "Source document is well-structured; intake form closely mirrors source organization"

### Medium-Quality Source (Completeness 40-79%)

- Extraction requires inference for some categories
- Clearly mark inferred items: "_[Inferred from §X — confirm]_"
- Flag gaps for Stage 4 analysis
- More questions likely in the review step

### Low-Quality Source (Completeness <40%)

- Heavy structuring work — source provides direction, not detail
- Use Mode C follow-up questions to enrich
- Many items will be `_[TBD]_` — this is acceptable
- Workflow depth should be Standard or Comprehensive
- Note: "Source is early-stage; significant elicitation needed in Assessment phase"

---

## Traceability

Every requirement in the Intake Form should be traceable:

| Requirement | Source Location | Confidence |
|-------------|:---------------:|:----------:|
| FR-001 | Source §3.2 | High (direct quote) |
| FR-002 | Source §3.2 | Medium (paraphrased) |
| FR-003 | User addition (Stage 3) | High (directly stated) |
| NFR-001 | Source §5 | High (direct) |
| NFR-002 | Inferred from Source §2 context | Low (needs confirmation) |

**Confidence levels:**
- **High** — directly stated in source or by user
- **Medium** — paraphrased or reorganized from source
- **Low** — inferred or implied; needs confirmation in Clarification Cycle

---

## Do NOT Do

- ❌ Restructure the source in a way that changes meaning
- ❌ Combine two distinct requirements into one (split, don't merge)
- ❌ Add requirements the AI thinks are "best practice" but aren't in the source (flag as observations instead)
- ❌ Remove requirements because they seem difficult or unrealistic (flag as concerns)
- ❌ Change the priority stated by the user/source without explicit agreement
- ❌ Produce the intake form without presenting it for review
