---
name: human-plan-manager
description: |
  Structured plan management for short-term goals and detailed implementation schemes.

  Use when the user needs to create, track, or break down plans into actionable steps.
version: 1.0.0
author: 文轩先师
---

# Human Plan Manager

Manage short-term plans and detailed implementation schemes in a structured, trackable way.

**Who is it for?** Anyone who needs to organize tasks, track progress, or document step-by-step execution plans.

**What makes it different?**

- **Structured**: separates high-level overview from detailed implementation
- **Trackable**: uses tables and checkboxes for clear status visibility
- **Lightweight**: just Markdown files, no external tools needed

## Quick Start

1. Create `plans/plans-overview.md` from the overview template
2. Add your plan items to the table
3. If a plan needs detailed steps, create `plans/detailed/XX-{plan-name}.md`
4. Update `plans/detailed/index.md` to link the new plan
5. Update statuses weekly (or as plans change)

## Directory Structure

```text
plans/
├── plans-overview.md      ← from templates/plans-overview.md
└── detailed/
    ├── index.md           ← from templates/index.md
    └── XX-{plan-name}.md  ← from templates/detailed-plan.md
```

## When to Use

- Creating a new plan or todo list
- Viewing or updating existing plan status
- Breaking a plan into detailed steps
- Recording detailed implementation documentation
- Structured project plan management

## Example: Refactoring the Auth Module

**Step 1** — Add to `plans/plans-overview.md`:

```markdown
| 1 ||***|| Auth module refactor ||***|| In Progress ||***|| High ||***|| TBD ||***|| TBD ||***|| Break into service layer |
```

**Step 2** — Create `plans/detailed/01-auth-refactor.md`:

```markdown
# Detailed Plan - Auth Module Refactor

## Plan ID: #1

## Objective
Extract auth logic into a dedicated service layer with unit tests.

## Schedule
TBD

## Deadline
TBD

## Implementation Steps

### 1. Extract service layer
- [ ] Move auth logic from controllers
- [ ] Define service interfaces

### 2. Add tests
- [ ] Unit tests for login
- [ ] Unit tests for token refresh

## Estimated Time
4-6 hours
```

**Step 3** — Update `plans/detailed/index.md`:

```markdown
| #1 | Auth module refactor | TBD | TBD | [01-auth-refactor.md](./detailed/01-auth-refactor.md) |
```

## Templates

All templates live in `templates/`:

- **`plans-overview.md`** — High-level plan board with status table and priority lists
- **`index.md`** — Index of all detailed plans
- **`detailed-plan.md`** — Step-by-step implementation plan with checkboxes

## Tips

- Keep plan names concise; use kebab-case for filenames (`01-auth-refactor.md`)
- Update `last_updated` in frontmatter whenever the overview changes
- Use checkboxes (`- [ ]`) in detailed plans to track subtask progress
- Archive completed plans by moving them to the "Completed Items" section
