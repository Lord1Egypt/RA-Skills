# Review Apply

Collect `[REVIEW_FEEDBACK]` deferred items from fix_plan, apply them to the code, and update the PR body/Summary.

This is the **dedicated follow-up entry point** for items that were not applied immediately during consolidate Step 6.

## When to Use

- On requests like "apply review feedback", "review apply", "address feedback", "apply deferred items"
- When `[REVIEW_FEEDBACK]` items in fix_plan still require code changes
- When applying Actionable items that were classified as deferred after consolidate
- On a `[REVIEW_FEEDBACK] processing` instruction

## Workflow

### Step 1: Collect deferred items

Collect every unchecked (`[ ]`) item tagged `[REVIEW_FEEDBACK]` from `fix_plan.md` or `checklist.md` (whichever is present in the workspace — collect from both if both exist):

```bash
Grep("[REVIEW_FEEDBACK]", path="{workspace}/.ralph/fix_plan.md")
Grep("[REVIEW_FEEDBACK]", path="{workspace}/checklist.md")
```

**Information to collect** (per item):

| Field | Example |
|-------|---------|
| PR number | `PR #317` |
| Severity | `🔴 Critical`, `🟡 Minor` |
| File:line | `route.ts:25` |
| Summary | `findMany has no take, risks bulk reads` |
| Original reviewer | `code-reviewer`, `CodeRabbit`, `Copilot` |
| Owner | `teammate in progress`, unassigned, etc. |

### Step 2: Filter the apply targets

| Condition | Action |
|-----------|--------|
| `[ ]` + PR assigned to / authored by me | Apply |
| `[ ]` + marked **teammate in progress** | Skip — do not modify a teammate's PR |
| `[x]` already completed | Skip |
| `[BLOCKED]` tag | Skip — external dependency |

If zero items remain, report and stop.

### Step 3: AskUserQuestion for apply scope

Show the apply targets to the user and confirm scope.

```javascript
AskUserQuestion({
  questions: [{
    question: "Apply scope for N [REVIEW_FEEDBACK] items?",
    header: "Review apply",
    multiSelect: true,
    options: [
      { label: "Apply Critical only", description: "🔴 Critical N items" },
      { label: "Apply Critical + Minor", description: "🔴 N items + 🟡 M items" },
      { label: "Pick individually", description: "Decide apply/skip per item" }
    ]
  }]
})
```

### Step 4: Apply to code

Process the approved items sequentially:

1. **Edit code**: change the code to address the review point
2. **Verify**: confirm the build/tests pass after the change (`pnpm typecheck`, `pnpm test`, etc.)
3. **Commit**: review-application commit
   ```text
   fix: address [REVIEW_FEEDBACK] — {summary}
   ```
4. **Update fix_plan**: check `[ ]` → `[x]` for completed items

### Step 5: Update the PR body / Summary

Update the AI Review Summary status line on the PR that was just addressed:

```bash
# Update the status line on the existing Summary comment
# Status: 4/10 actionable addressed → 7/10 actionable addressed
```

**Update targets**:
- The `status-line` on the AI Review Summary comment (refresh addressed count)
- The PR body Test Plan (check `[x]` for related items)

### Step 6: Push + CI confirmation

```bash
git push origin <branch>
gh pr checks <N>  # wait for CI to pass
```

## Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Check `[REVIEW_FEEDBACK]` items as `[x]` without applying the code change | Edit code → build/tests pass → then `[x]` |
| 2 | Apply `[REVIEW_FEEDBACK]` items belonging to a teammate's PR yourself | Skip teammate-PR items. Relay via a PR comment if necessary |
| 3 | Apply everything without asking the user for scope | Use the Step 3 AskUserQuestion to confirm scope |
| 4 | Apply code without updating Summary / fix_plan | Three-piece set: code apply + fix_plan `[x]` + Summary status-line update |

## Relationship with consolidate

```text
consolidate pr-review
  Step 4: classify (Actionable / Non-blocking)
  Step 6: immediate apply (with user approval)
  Step 7: post Summary + register deferred items into fix_plan
           ↓
github-flow review-apply  ← follow-up entry point
  Step 1: collect [REVIEW_FEEDBACK] from fix_plan
  Step 4: apply to code
  Step 5: refresh Summary status line
```

consolidate owns **classification + registration**; review-apply owns **follow-up apply + refresh**.
