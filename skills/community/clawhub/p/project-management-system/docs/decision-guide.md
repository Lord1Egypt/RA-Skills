# Decision and Writing Guide

> Dispatchers need to make various judgments during the process: when to return, when to switch person, how to write feedback, how to adjust the big picture.
> This file is the meta-guidance on "how to make decisions" and "how to write files".

---

## I. Review Decision Guide

### When to Pass

- Acceptance criteria item by item met
- Output file at specified location
- Format meets requirements
- No obvious omissions

### When to Return

- Acceptance criteria have unmet items
- Output missing or wrong location
- Quality clearly below expectation

**How to write feedback when returning:**
```markdown
## Review Feedback

**Unpassed items:**
1. [Which specific acceptance criteria] — [Where is the gap] — [What is expected]
2. ...

**Passed items:** (Let Executor know what doesn't need changing)
1. ...

**Modification instructions:**
- [Clearly tell Executor what modifications to make]
```

**Principle: Feedback must be specific enough to say "where the gap is + what is expected". Don't say "not good enough", say "missing error handling, need try-catch covering X and Y exceptions".**

### When to Switch Person/Approach

| Situation | Judgment Criteria | Action |
|-----------|------------------|--------|
| 3 rounds of rework still not meeting standard | Is the problem within Executor's capability range | Switch Executor or switch approach |
| Executor reports "infeasible" | Evaluate if feedback is reasonable | Reasonable→switch approach, unreasonable→add explanation |
| Executor timeout no response | Wait time exceeds expiration time | Re-dispatch |
| Output direction completely wrong | Does Executor understand the task | Clarify→redo, understanding insufficient→switch person |

### When to Escalate to Decision Maker

- Subjective problems you can't judge yourself
- Changes involving project goals or scope
- Cost or time exceeding expectation
- 3 rounds of rework with no progress
- Multiple approaches each with pros and cons, need a decision

## II. File Writing Guide

### How to Write task-spec

**Good task-spec standard: Executor can start work just by reading this one document.**

| Element | Good | Bad |
|---------|------|-----|
| Task goal | "Implement GitHub Actions auto-tagging" | "Do CI well" |
| Acceptance criteria | "After push to main, auto-create vX.Y.Z tag" | "Works normally" |
| Output location | "`.github/workflows/release.yml`" | "Put in an appropriate location" |
| Notes | "Don't use deprecated actions/create-release" | _(empty)_ |

**Checklist (self-check after writing):**
- [ ] Can Executor start without asking me?
- [ ] Are acceptance criteria items that can be checked off one by one?
- [ ] Is output location and format clear?
- [ ] Information pointers only provide needed context? (Don't stuff irrelevant info)

### How to Write Review Record

- Check item by item against acceptance criteria
- Mark each item ✅ Pass / ❌ Not passed
- For unpassed items, write the gap and expectation
- Overall conclusion: Pass / Rework / Escalate
- If rework, write specific modification instructions

### How to Write Change Request

- What was the original requirement (cite brief.md or task-spec)
- What is changing
- Why the change
- Impact analysis: Which tasks are affected, how much extra work needed
- Proposed approach

### How to Write brief Adjustment (Big Picture Change)

Big picture adjustment = new entry in brief.md requirements confirmation record:

```markdown
| Round | Time | Adjustment | Reason | Decision Maker Confirmation |
|-------|------|------------|--------|----------------------------|
| 3 | YYYY-MM-DD | Scope adjustment: remove feature | Insufficient time | Pending confirmation |
```

Also check:
- Which existing task-specs are affected? → Update or cancel
- Which new tasks need creation? → Create new task-spec
- Has risk changed? → Update risk-register

## III. Runtime Content Writing Guide

Various real-time content is generated during project execution, not copied from templates, but written on the spot. How to write:

### How to Write Heartbeat Check Items

```markdown
## [Project name]
- [Current most urgent todo] ← Only write next step, no history
- [If there's a second todo]
```

**Principles:**
- Maximum 3 check items per project
- Only write "what to do next", not completed items
- Project complete → delete entire entry
- Update immediately after each phase completion

### How to Write Communication Log Entry

```markdown
| Time | Direction | Content Summary | Communication ID / Tool |
|------|-----------|-----------------|-------------------------|
| 03-21 10:00 | Dispatcher→Executor | [One sentence summary: what was done/said] | [identifier] |
```

**Principle:** One sentence summary is sufficient. Purpose is to know "who was talked to about what" when resuming, not to record full text.

### How to Write Status Tracking Entry

```markdown
| Time | Status Change | Explanation |
|------|---------------|-------------|
| 03-21 10:00 | Pending→In Progress | [reason/trigger event] |
```

### How to Write Public Message Board Entry

```markdown
| Time | Author | Content |
|------|--------|---------|
| 03-21 10:00 | [role/task ID] | [information content] |
```

**When to use message board vs communication log:**
- Only relevant to one Executor → communication log
- Multiple people need to know → message board

## IV. Recording and Linking New Files

**Whenever creating a new file in project directory, must complete two steps:**

1. **Add reference in corresponding parent document**
   - New task-spec → Confirm brief.md task list mentions it
   - New review-record → Confirm task-spec status tracking references it
   - New change-request → Confirm brief.md or affected task-spec references it

2. **Check index consistency**
   - If system-level file (under system/) → update data_structure.md
   - If project file (under /path/to/projects-data/) → no system index update needed, project self-links

**Principle: Every file must be referenced by at least one other file, otherwise it's an orphan.**