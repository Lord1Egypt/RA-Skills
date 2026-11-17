<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Content Validation

## Purpose

Before creating or saving ANY deliverable file, the AI MUST validate its content against the rules in this document. This ensures all outputs are professional, consistent, complete, and correctly formatted.

---

## Validation Checklist (Apply to Every Deliverable)

### 1. Document Metadata

Every deliverable MUST include:

- [ ] Document title (H1 heading)
- [ ] Project name (generic placeholder `{project_name}` in templates; actual name in generated outputs)
- [ ] Version number
- [ ] Date (ISO format or localized per user preference)
- [ ] Author / Prepared By
- [ ] Status (Draft / Awaiting Approval / Approved / Superseded)
- [ ] Reference to source document or predecessor deliverable

**Validation rule:** If any metadata field is unknown, use `_[TBD]_` or `_[Pending]_` — never leave it blank or omit the field.

---

### 2. Structural Completeness

- [ ] All sections defined in the template are present (even if marked N/A for this project)
- [ ] No orphaned headers (header with no content below it)
- [ ] Tables have consistent column counts (no ragged rows)
- [ ] All numbered lists are sequential (no gaps: 1, 2, 4)
- [ ] Cross-references to other documents use correct file names
- [ ] All placeholder tokens are properly formatted: `_[TBD]_`, `_[Pending]_`, `{variable_name}`

---

### 3. Content Quality

- [ ] No project-specific content in template files (templates must be generic)
- [ ] Generated deliverables reference the source document — never invent scope
- [ ] Recommendations include rationale (never "because it's best practice" without explanation)
- [ ] Quantitative claims have basis stated (even if estimated/assumed)
- [ ] Risk/impact assessments use the defined scoring scales (not ad-hoc language)
- [ ] No contradictions with previously approved deliverables in the same workflow
- [ ] Acronyms defined on first use (or in a glossary section for long documents)

---

### 4. Markdown Formatting

#### Tables

```markdown
<!-- CORRECT: aligned pipes, header separator, consistent columns -->
| Column A | Column B | Column C |
|----------|:--------:|----------|
| Data 1   | Center   | Data 3   |
| Data 2   | Center   | Data 4   |

<!-- INCORRECT: missing separator, ragged columns -->
| Column A | Column B
| Data 1 | Data 2 | Extra |
```

**Rules:**
- Always include the header separator row (`|---|---|`)
- Align pipe characters for readability
- Use `:---:` for center alignment, `---:` for right alignment, only when semantically appropriate
- No empty tables — if no data yet, use a single row with `_[To be populated]_`

#### Headings

- H1 (`#`) — document title only (one per file)
- H2 (`##`) — major sections
- H3 (`###`) — subsections
- H4 (`####`) — sub-subsections (use sparingly)
- Never skip levels (e.g., H1 → H3 with no H2)

#### Lists

- Use `-` for unordered lists (not `*` or `+`)
- Use `1.` for ordered lists (auto-numbered, not manual numbers)
- Nested lists indent by 2 spaces (for Markdown compatibility)
- Lists of 10+ items should be in a table instead

#### Emphasis

- `**bold**` for key terms, field names, and important callouts
- `_italic_` for placeholder values and document references
- `` `code` `` for file paths, technical identifiers, and field values
- Never use ALL CAPS for emphasis

---

### 5. Diagram Validation

If a deliverable includes diagrams (ASCII, Mermaid, or textual):

#### ASCII Diagrams

```
<!-- CORRECT: box-drawing characters, consistent spacing -->
┌──────────────┐     ┌──────────────┐
│   Phase 1    │────►│   Phase 2    │
└──────────────┘     └──────────────┘

<!-- ALSO ACCEPTABLE: simple characters for portability -->
+----------------+     +----------------+
|   Phase 1      |---->|   Phase 2      |
+----------------+     +----------------+
```

**Rules:**
- Use consistent character set within a single diagram (don't mix box-drawing and ASCII)
- Ensure alignment is preserved (monospace assumption)
- Provide a text description below complex diagrams for accessibility
- Keep diagrams under 80 characters wide for terminal/email compatibility

#### Mermaid Diagrams (if platform supports)

```markdown
```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
```​
```

**Rules:**
- Validate syntax before saving (no orphan nodes, closed brackets)
- Always provide a text alternative below the diagram
- Keep diagrams simple — max 15 nodes for readability

---

### 6. Cross-Reference Integrity

When a deliverable references another document:

- [ ] Referenced file exists (or is planned to exist in a future stage)
- [ ] File name matches exactly (case-sensitive)
- [ ] Referenced section/heading exists within the target document
- [ ] Forward references (to not-yet-created documents) are marked: `_[To be produced in Stage {n}]_`

**Format for cross-references:**
- Same folder: `See Feasibility_Assessment.md §3`
- Different folder: `See ../03_Business_Case/Business_Case.md §2`
- Future document: `See Risk_Register.md _[To be produced in Stage 13]_`

---

### 7. Consistency Checks

Before saving, verify consistency with:

| Check Against | What to Verify |
|---------------|---------------|
| Source document | Scope items match; no invented requirements |
| Requirement Intake Form | Stakeholder names consistent; project name matches |
| Decision Log | Decisions referenced in deliverables match logged decisions |
| Previous deliverables | No contradictions in scope, timeline, budget, or priority |
| State file | Stage status is accurate; project metadata matches |

**If inconsistency found:**
1. Flag to user: "I noticed {deliverable A} says X but {deliverable B} says Y. Which is correct?"
2. Do NOT save until resolved
3. Update all affected documents to be consistent
4. Log the correction in Change Log if it changes a previously approved artifact

---

### 8. Placeholder Hygiene

#### Valid placeholder formats

| Format | Usage |
|--------|-------|
| `_[TBD]_` | Value not yet determined; will be filled later |
| `_[Pending]_` | Awaiting approval or external input |
| `_[To be confirmed]_` | Provisional value needing stakeholder validation |
| `{variable_name}` | Template variable (only in template files) |
| `_[See Action A-{nnn}]_` | Linked to a tracked action for resolution |

#### Placeholder tracking

- Every `_[TBD]_` in a final deliverable MUST have a corresponding Action Item
- At Package Assembly (Stage 16), all remaining placeholders are reported as open items
- Templates may contain unlimited placeholders; generated deliverables should minimize them

---

### 9. File Naming Conventions

| Rule | Example |
|------|---------|
| Use Title_Case with underscores | `Business_Case.md` |
| No spaces in file names | ✅ `Risk_Register.md` ❌ `Risk Register.md` |
| Folder names match phase | `08_Risk_Management/` |
| State file is always `pilc-state.md` | Lowercase, hyphenated |
| Management registers use Title_Case | `Decision_Log.md` |
| Drafts marked with suffix | `Business_Case_DRAFT.md` |
| Archived files with timestamp | `pilc-state-20260603T1430.archived.md` |

---

### 10. Sensitive Content

Before saving any file, verify it does NOT contain:

- [ ] Real passwords, API keys, or credentials
- [ ] Personal data beyond professional role information (no home addresses, personal phone numbers)
- [ ] Financial figures marked as confidential by the user
- [ ] Content from the source document marked as restricted

**If user provides sensitive information during the workflow:**
- Store only the minimum necessary for the deliverable
- Use role references instead of names where possible in templates
- Flag to user if a deliverable would contain information they may not want in a shareable document

---

## Validation Failure Handling

If validation fails on any check:

1. **Do NOT save the file**
2. Identify the specific failure(s)
3. Fix automatically if the fix is unambiguous (e.g., missing separator row in table)
4. Ask user if the fix requires a judgment call (e.g., inconsistency between documents)
5. Re-validate after fix
6. Only save when all checks pass

---

## Template vs. Generated Output Rules

| Rule | Templates | Generated Outputs |
|------|-----------|-------------------|
| Project-specific content | ❌ Never | ✅ Required |
| Placeholder variables `{...}` | ✅ Expected | ❌ Must be resolved |
| `_[TBD]_` markers | ✅ In optional fields | ✅ Only where truly unknown |
| Instructional comments | ✅ Guide the user | ❌ Remove before saving |
| Example data | ✅ Illustrative | ❌ Replace with real data |
| Section markers like `<!-- REMOVE -->` | ✅ For template guidance | ❌ Must be cleaned |
