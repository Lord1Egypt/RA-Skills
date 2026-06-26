# Katelynn — Learned Failure Rules

This file is auto-updated after each run. Katelynn reads it at the start of every new run
and applies all active rules to filter and qualify leads.

Rules are written here when a lead type or signal pattern consistently fails to convert,
or when the user provides feedback that a batch was off-target.

---

## How Rules Work

Each rule has:
- **Rule ID**: Unique identifier for reference
- **Type**: What kind of filter it applies (vertical, size, role, geography, signal, etc.)
- **Description**: What to avoid and why
- **Status**: `active` (enforced) or `archived` (no longer relevant)
- **Added**: Date the rule was learned
- **Source**: What triggered this rule (user feedback, run analysis, low conversion)

---

## Active Rules

*(No rules yet — this file is populated automatically as runs complete and patterns emerge.)*

---

## Rule Template

When adding a new rule after a run, use this format:

```
### RULE-[N]: [Short Title]
- **Type:** [vertical | size | title | geography | signal | competitor | budget]
- **Description:** [What to exclude or filter, and why it doesn't convert]
- **Example:** [Concrete example of what this rule prevents]
- **Status:** active
- **Added:** [YYYY-MM-DD]
- **Source:** [user feedback / run analysis / zero replies / etc.]
```

---

## Example Rules (for reference — not active)

```
### RULE-001: Exclude Pre-Revenue Startups
- Type: budget
- Description: Companies with no revenue or pre-product stage rarely convert —
  they're interested but can't budget right now.
- Example: Excluded 3 Y Combinator W26 companies that had no launched product.
- Status: archived
- Added: 2026-01-10
- Source: Zero replies after 2-week follow-up cadence

### RULE-002: Avoid Regulated Healthcare Verticals
- Type: vertical
- Description: HIPAA/compliance requirements create 6+ month sales cycles
  that don't fit the current motion.
- Example: Removed all hospital system leads from a batch targeting "healthcare ops."
- Status: active
- Added: 2026-02-03
- Source: User feedback after run

### RULE-003: Target VP+ for SaaS, Not Individual Managers
- Type: title
- Description: Manager-level contacts at SaaS companies rarely have budget authority.
  Always target VP, Director, or C-suite for initial outreach.
- Example: Replaced "Marketing Manager" targets with "VP Marketing" or "Head of Growth."
- Status: active
- Added: 2026-02-20
- Source: Run analysis — 0% conversion from manager-level contacts
```

---

## Archiving Rules

When a rule is no longer relevant (e.g., the team now serves that vertical, or the ICP changed),
change its status to `archived` and add a note explaining why it was retired. Do not delete rules —
the history is useful context.
