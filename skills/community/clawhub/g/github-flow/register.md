# Issue Registration Strategy

Before creating a new GitHub issue, evaluate the existing issue landscape to decide whether to create a new issue, comment on an existing one, or create a sub-issue.

## When to Use

- When converting a plan/research task into a GitHub issue (Step 0 of `plan-to-issue`)
- When a new finding emerges and you need to decide where to track it
- Use for "issue registration", "duplicate check", "issue strategy"

## Procedure

### Step 1: Duplicate & Related Search

Search for existing issues using keywords from the current task/plan:

```bash
gh issue list --search "<keywords>" --json number,title,state
```

- **Exact Match (OPEN)**: Stop. Report the issue URL to the user.
- **Related/Overlapping Match**: Note the issue number for Step 2.
- **No Match**: Proceed to create a new issue (Step 2).

### Step 2: Registration Strategy Decision

#### Epic vs. Sub-issue Criteria

Before choosing a strategy, evaluate the **density and scope** of existing issues.

| Type | Criterion | Example |
|------|-----------|---------|
| **Issue** | Single task, clear DoD, 1-2 days work | Fix OKLCH color tokens |
| **Epic** | Collection of 3+ related issues, shared strategic goal | Accessibility Audit Remediation |

**Decision Rule (HARD STOP)**:
- If an existing issue is already **detailed (100+ lines of body)**, do NOT add new major topics to it. 
- Instead, create a **New Epic** and link the existing issue as a **Sub-issue**.

#### Principle: Deferred Splitting (Flexible Scope)

For large strategic goals (e.g., Audit Remediation), do not pre-fragment all sub-tasks into empty issues.
- **Rule**: Define sub-tasks as a checklist within the Epic body first.
- **Worker Autonomy**: Allow the assignee to decide whether to bundle tasks in a single PR or create/link dedicated sub-issues during the implementation/analysis phase.
- **Marker**: Use markers like `(Flexible Split)` or `(Worker Discretion)` in the Epic checklist.

#### Strategy Table

| Scenario | Recommendation | Action |
|----------|----------------|--------|
| Topic is a subset of an existing OPEN issue | **Comment** on existing issue | Use `gh issue comment <N> --body "..."` |
| Topic is related but existing issue is bloated | **New Epic + Link Sub-issue** | Create Epic, link #N in checklist |
| Topic is a standalone task but related to an OPEN issue | **New Issue + Blocker** | Create new issue, then use `dependencies` topic to add `blocked-by` |
| Topic is a sub-task of a complex issue | **Sub-issue** | Create sub-issue → create a native relationship via the `addSubIssue` API (body text links alone are not enough) → see the `dependencies` topic's Sub-issue Procedure |
| Topic is entirely new | **New Issue** | Use `plan-to-issue` to create |

### Step 3: Blocker Relationship Analysis (CRITICAL)

Analyze if the new task blocks or is blocked by any existing open issues.

- **Blocked by**: The new task cannot be completed until issue #N is CLOSED.
- **Blocking**: Issue #M cannot be completed until the new task is CLOSED.

**Action**: Use the `dependencies` topic to register these relationships officially on GitHub:
```bash
# Example: new issue blocks #300
Skill("github-flow", "dependencies --blocking 300")
```

## Rules

| # | Don't (Forbidden) | Do (Correct Alternative) |
|---|-------------------|------------------------|
| 1 | Create a new issue for a topic already covered by an open issue | Post a comment with your plan/finding to the existing issue |
| 2 | Forget to link related issues | Always use `Relates to #N` or the `dependencies` topic |
| 3 | Split a coherent change into "micro-issues" | Use the `expand` topic to keep the scope coherent |
| 4 | Choose the Sub-issue strategy and only add a `- #N` text link in the body | Create the native relationship via the `addSubIssue` GraphQL mutation (see the `dependencies` topic's Sub-issue Procedure) |
| 5 | Update only the parent body after `gh issue create` and stop there | `gh issue create` → `addSubIssue` → parent body update (all three steps are required) |

## Topic Dependencies

- `plan-to-issue`: Used to generate the actual issue body/comment content
- `dependencies`: Used to apply `blocked-by` / `blocking` relationships
- `expand`: Used if the new finding should be merged into an in-progress PR/issue
