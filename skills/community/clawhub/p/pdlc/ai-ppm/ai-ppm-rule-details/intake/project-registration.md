<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 2: Project Registration

**Phase:** Intake
**Purpose:** Admit a new project into the Portfolio Register. This is how projects enter portfolio governance — from AI-PILC PIPs, AI-ILC Approved Briefs, or manual entry.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (Portfolio Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Extract structured data from unstructured sources (PIPs can be verbose)
- Identify the minimum fields needed for portfolio-level governance (not project-level detail)
- Validate completeness — flag missing data rather than inventing it
- Standardize nomenclature across projects (consistent naming, consistent scales)

### Anti-Patterns for This Stage
- Do NOT copy the entire PIP into the register — extract ONLY portfolio-relevant fields
- Do NOT perform project-level analysis — registration is about ADMISSION, not evaluation

### Quality Check
A good registration sounds like:
- "Project {name} registered as PRJ-{ID}. Budget ROM: $X–Y. Timeline: N months. Strategic alignment: pending (Stage 3)."

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Extract essentials only (ID, name, budget, timeline). Minimal intake card. |
| **Standard** | Full intake card with all fields. Validate against PIP completeness. |
| **Comprehensive** | Full intake card + preliminary risk flags + dependency scan across existing portfolio. |

---

## Step-by-Step Execution

### Step 2.1: Identify Source

Determine how this project enters the portfolio:

| Mode | Source | Detection |
|------|--------|-----------|
| **A: From PIP (AI-PILC)** | `pilc-state.md` → Status: Complete | Same-layer direct read |
| **B: From Idea Brief (AI-ILC)** | `ilc-state.md` → Route: project, Status: Approved | Same-layer direct read |
| **C: Manual entry** | User describes the project verbally or provides a document | Interview mode |
| **D: Batch import** | User has multiple projects (spreadsheet, list) | Batch registration |

If multiple sources detected (Step 1.2 found several), ask:
```
Q-{NN}: Which project would you like to register?

Detected sources:
(a) {Project A from PIP} — {one-line summary}
(b) {Project B from PIP} — {one-line summary}
(c) {Idea Brief C} — {one-line summary}
(d) Register all of the above (batch)
(e) Different project (manual entry)
```

### Step 2.2: Extract Portfolio-Relevant Data

From the source, extract ONLY what portfolio governance needs:

| Field | From PIP | From ILC Brief | From Manual |
|---|---|---|---|
| **Project ID** | `pilc-state.md` → Project ID | Generate new | Generate new |
| **Project Name** | Charter → Project Name | Brief → Idea Name | Ask user |
| **Objective** | Charter → Objectives (first) | Brief → Problem Statement | Ask user |
| **Sponsor** | Charter → Sponsor | Brief → Requestor | Ask user |
| **Budget ROM** | Resource Plan → Total ROM | Brief → Effort Estimate | Ask user |
| **Timeline** | Charter → High-Level Milestones | Brief → Timeline Estimate | Ask user |
| **Risk Level** | Feasibility → Rating (🟢🟡🟠🔴) | Brief → Risk Assessment | Ask user |
| **Priority (initial)** | Prioritization → Rank | Brief → Evaluation Score | Unranked |
| **Source Marker** | `pilc-state.md` path | `ilc-state.md` path | "manual" |
| **Originating Idea** | `pilc-state.md` → Originating Idea | Idea ID | N/A |

### Step 2.3: Validate Completeness

Check extracted data against minimum registration requirements:

| Field | Required? | If Missing |
|---|---|---|
| Project ID | ✅ Mandatory | Generate if not from PIP |
| Project Name | ✅ Mandatory | Ask user |
| Objective | ✅ Mandatory | Ask user (one sentence minimum) |
| Budget ROM | ⚠️ Strongly recommended | Flag as "TBD — affects prioritization" |
| Timeline | ⚠️ Strongly recommended | Flag as "TBD — affects scheduling" |
| Sponsor | 🟡 Standard+ | Skip at Minimal depth |
| Risk Level | 🟡 Standard+ | Default to "Unassessed" |

If critical fields are missing:
```
⚠️ Registration incomplete — the following are needed for portfolio governance:
   • Budget ROM: Not found in PIP. Approximate range? [Provide / Skip for now]
   • Timeline: Not found. Expected duration? [Provide / Skip for now]
```

### Step 2.4: Create Project Intake Card

Generate using template `templates/project-intake-card.md`:

```markdown
# Project Intake Card: {Project Name}

| Field | Value |
|-------|-------|
| **Project ID** | {ID} |
| **Name** | {name} |
| **Objective** | {one-line} |
| **Sponsor** | {name/role} |
| **Budget ROM** | {range} |
| **Timeline** | {duration or dates} |
| **Risk Level** | {🟢🟡🟠🔴 or Unassessed} |
| **Source** | {PIP / ILC Brief / Manual} |
| **Source Path** | {marker file location} |
| **Registered On** | {ISO-date} |
| **Portfolio State** | Registered |
| **Priority Rank** | Pending (Stage 4) |
| **Strategic Alignment** | Pending (Stage 3) |
```

### Step 2.5: Add to Portfolio Register

Append the project as a new row in `portfolio-register.md`:

```markdown
| {ID} | {Name} | Registered | — | — | ⚪ | {date} | {source} |
```

(Priority and alignment are filled in Stages 3-4.)

### Step 2.6: Determine Next Action

```
✅ Project registered: {Project Name} (ID: {Project ID})

Next steps:
(a) Register another project [if more sources available]
(b) Proceed to Strategic Alignment (Stage 3) → score this project against strategy
(c) Batch: register all detected projects first, then prioritize together

Recommended: {based on context}
```

---

## Gate

User confirms registration is correct → proceed to Stage 3 (or register more projects first).

---

## Outputs

| Artifact | Status |
|---|---|
| `project-intake-card-{project-id}.md` | Created in output folder |
| `portfolio-register.md` | Updated (new row) |
| `ppm-state.md` | Updated (project count, session history) |

---

## Management Framework Contribution

Entry: `PPM-D-{NNN}: Project {name} ({ID}) registered in portfolio. Source: {PIP/Brief/Manual}. Budget: {ROM}. Timeline: {est}.`

---

## Batch Registration

When registering multiple projects at once:
1. Extract data for all projects
2. Present summary table for user validation
3. User confirms all / adjusts individual entries
4. Add all to register in one pass
5. Proceed to Stage 3 with the full set

---

*This stage can repeat multiple times as new projects enter the portfolio.*
