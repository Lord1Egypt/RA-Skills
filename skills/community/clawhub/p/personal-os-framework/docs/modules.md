# Modules

## Decision Log

Record important judgments and why they were made.

**Purpose:** Preserve the reasoning behind decisions so it can be reviewed later.

**Template fields:**
- title
- date
- decision
- rationale
- consequences
- follow-up actions

**Storage:**
- Project decisions → `Projects/<name>/DECISIONS.md`
- System decisions → `Chronicle/decisions/`

---

## Review Operator

Generate periodic reviews from project state and recent activity.

**Purpose:** Regular reflection to surface stale projects, blockers, and upcoming work.

**Cadence:** Daily, weekly, monthly

**Inputs:**
- Project states
- Recent decisions
- Task statuses
- Inbox items

**Outputs:**
- Review draft
- Stale project list
- Promotion candidates

---

## Routing Assistant

Classify incoming items by type and destination.

**Categories:**
- Raw capture
- Task
- Decision
- Incident
- Knowledge
- Reference

**Purpose:** Every piece of information has a canonical home.

---

## Task Layer

Define what a "task" is. Provide templates and status conventions.

**Minimal task fields:**
- title
- status (open/in-progress/done/waiting)
- created date
- optional: follow-up, waiting-on, done date

**Purpose:** Consistent task representation across projects.

---

## Execution Layer

Record when work begins. Track started-task staleness.

**Purpose:** Make execution visible to the review system.

**Trigger:** When transitioning `[ ]` → `[p]`

---

## Decision Support Layer

Monitor decision follow-ups and task health.

**Observables:**
- Decision follow-up status
- Task closure rate
- Waiting tasks
- Stale started tasks

**Purpose:** Proactive monitoring without manual recounting.

---

## Memory Distiller

Convert accumulated raw captures into structured knowledge.

**Process:**
1. Raw capture sits in Inbox
2. After 7 days, review for promotion
3. Clean title, extract tags, write summary
4. Move to Knowledge/

**Purpose:** Inbox → Knowledge, one level above raw notes.
