# Suggestion Patterns

## After code writing/modification

```typescript
options: [
  { label: "Run tests", description: "Verify changes with test suite" },
  { label: "Commit", description: "Git commit the changes" }
]
```

## After feature implementation

```typescript
multiSelect: true,
options: [
  { label: "Write tests", description: "Add tests for new feature" },
  { label: "Document", description: "Update README or JSDoc" },
  { label: "Commit", description: "Git commit the changes" }
]
```

## After bug fix

```typescript
multiSelect: true,
options: [
  { label: "Add regression test", description: "Prevent bug recurrence" },
  { label: "Commit", description: "Git commit the fix" },
  { label: "Close issue", description: "Close related issue" }
]
```

## After configuration change

```typescript
options: [
  { label: "Verify", description: "Source or restart to apply settings" },
  { label: "Backup", description: "Backup config file" }
]
```

## After commit

```typescript
options: [
  { label: "Push", description: "Git push to remote" },
  { label: "Create PR", description: "Create Pull Request" }
]
```

### Branch convention pre-check (HARD STOP — before composing Push / Create PR options)

The generic `Push` option above is only valid when the **current branch is push-ready**. Many repos use **local-only working branches** (`local`, `wip`, `scratch`, `tmp/*`, named after the user) that must NOT be pushed — pushing creates a new branch on the remote, polluting the namespace and bypassing the project's PR / release workflow.

| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|------------------------|
| 1 | Quote the branch name shown in `[<branch> <sha>]` after commit and suggest `git push origin <branch>` | Run `git branch -a` and `git ls-remote --heads origin <branch>` first. If the branch does not exist on origin, do NOT offer a direct `Push` option |
| 2 | Treat every branch as a feature branch ready for `Push` / `Create PR` | Classify the branch first: feature branch (`feat/*`, `fix/*`, `chore/*`) → PR-ready; local-only working branch (`local`, `wip`, names matching user-personal pattern) → NOT pushable as-is |
| 3 | Skip remote-existence check because "the user can pick Other if wrong" | Wrong defaults waste the user's verification budget. Verify branch class before offering options |
| 4 | Offer `Push` to a branch whose remote counterpart does not exist | Offer instead: "Cherry-pick to feature branch + push" or "Reset on feature branch + push" — make the working-branch detour explicit |

### Self-check (every time before composing After-commit options)

1. Run `git branch --show-current` → record the branch name
2. Run `git ls-remote --heads origin <branch>` → if empty, the branch does NOT exist on origin
3. Run `git branch -a | grep -E "(remotes/origin|^\\*)"` → confirm the remote layout pattern (e.g., `origin/main` + feature branches only, no working branch siblings)
4. Classify the current branch:
   - Tracked remote-counterpart exists → push-ready (Push / Create PR options OK)
   - Remote counterpart absent + matches working-branch pattern (`local`, `wip`, `scratch`, `tmp/*`, user-personal name) → NOT pushable. Offer cherry-pick / move-to-feature-branch options instead
   - Remote counterpart absent + looks like a new feature branch (`feat/*`, `fix/*`, `chore/*`) → first push OK, but state "creates new origin branch" in the description
5. Never quote the branch name from `[<branch> <sha>]` commit output alone — that line tells you the commit landed, not whether the branch belongs on the remote

## After push

```typescript
options: [
  { label: "Create PR", description: "Create Pull Request" },
  { label: "Check CI", description: "Verify pipeline status" }
]
```

## After PR fix commit push (after pushing a fix commit to an existing PR)

**Precondition**: A fix commit has just been pushed to an existing PR. CI has been re-triggered.

**Self-check before calling**: Verify AI Review Summary posting status via `gh pr view <N> --json comments`.

### Re-review policy (HARD STOP — first review vs re-review)

| Scenario | Autonomous bot trigger allowed? |
|----------|-------------------------------|
| **First review** (PR initial creation; no prior review from a given bot) | ✅ Allowed — PR creation itself is the user trigger |
| **Re-review** (new commit pushed; a prior review from the same bot exists or was requested) | ❌ Forbidden — AskUserQuestion required before re-requesting |

A "bot trigger" includes any of:

- `gh api repos/<o>/<r>/pulls/<N>/requested_reviewers -X POST` (re-request)
- `gh pr comment <N> --body "/review"` or `@coderabbitai review` (slash-command trigger)
- `gh pr edit <N> --add-reviewer copilot-pull-request-reviewer` (re-add)

These are external-medium actions (notify the reviewer bot's quota/queue + post user-visible artifacts on the PR). Initiating them autonomously on a fix-commit-push flow steps into user decision territory.

### Pre-trigger self-check (HARD STOP — every time before issuing a re-review trigger)

1. Has the same bot already produced **≥1 review** on this PR (any commit)? — `gh pr view <N> --json reviews --jq '[.reviews[] | select(.author.login | test("<bot>"; "i"))] | length'`. If `>0`, this is a re-review case.
2. Is there a **review currently in progress** (no submitted artifact yet but the bot is known to be working)? — Check the `gh pr checks <N>` output for the bot's status line (e.g., `CodeRabbit\tpending\t0\t\tReview in progress`) and the latest issuecomment timestamp from that bot author within the last **~10 min (600 s)**. The 600-second window is the canonical value set by `consolidate/pr.md` Step 2.6 (`now - 600 | strftime`); keep this file aligned with that source. If in-progress, **do not trigger** — wait.
3. Re-review case ✚ no in-progress signal → **AskUserQuestion required** with explicit options (Re-trigger / Skip Copilot - use 1st review + apply-evidence / Hold).
4. **Inconclusive in-progress detection** (HARD STOP) — if step 2's signals are unavailable (`gh pr checks` empty for the bot, `gh pr view --json comments` query fails, or no bot comment timestamp falls inside the 600 s window AND the bot has no submitted review either), do not interpret silence as "no in-progress" and do not autonomously trigger. Treat the state as **inconclusive** → **AskUserQuestion required** with options (Re-trigger / Skip bot — use prior review evidence / **Hold (Recommended when inconclusive)**). The Hold option lets the user wait for the next polling cycle without burning an external bot-trigger quota on uncertain state.

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | CI passes → jump directly to Test Plan verification (skipping consolidate) | CI passes → check AI Review Summary → if missing, run consolidate first → then Test Plan |
| 2 | "User asked for Test Plan check, so verify only" | Even if user-requested, if consolidate is not posted, guide consolidate first |
| 3 | "User asked for 'wait for Copilot re-review', so auto-trigger the re-request to make it arrive" | "Wait for X" ≠ "trigger X". Polling is allowed; bot re-trigger is not — AskUserQuestion required |
| 4 | Re-request after one missed poll → another /review comment → another `requested_reviewers` POST (cascade) | Single AskUserQuestion at the first missing-arrival decision point. No autonomous cascade |
| 5 | Skip the in-progress check before re-requesting | Always run the in-progress check first (step 2 above). A still-running review must not be re-triggered |

**When AI Review Summary is not posted + this is a re-review case** (multiSelect: false):
```typescript
options: [
  { label: "Re-request <bot> review (Recommended if no in-progress signal)", description: "Issue the re-request only after user explicit OK. Includes /review comment or requested_reviewers POST" },
  { label: "Skip <bot> — proceed with prior review + apply-evidence", description: "Use the 1st <bot> review + Internal Review fallback as Summary basis. Faster but loses follow-up findings" },
  { label: "Hold", description: "Decide later (waiting on external/user signal)" },
]
```

**When AI Review Summary is not posted + first-review case** (multiSelect: false):
```typescript
options: [
  { label: "Wait for CI → consolidate (Recommended)", description: "After CI passes, run /consolidate pr-review <N>. Test Plan verification comes after consolidate" },
  { label: "Wait for CI only", description: "Decide next action after CI result" },
]
```

**When AI Review Summary is posted** (multiSelect: false):
```typescript
options: [
  { label: "Wait for CI → Test Plan verification (Recommended)", description: "After CI passes, verify unchecked Test Plan items" },
  { label: "Wait for CI only", description: "Decide next action after CI result" },
]
```

## After PR creation (BEFORE consolidate — branch on reviewer matrix)

**Precondition**: Passed `github-flow/pr.md` Step 9. Branch on the **reviewer matrix** (CodeRabbit walkthrough + Copilot review request/post state), not just walkthrough.

**Self-check before calling** (HARD STOP — reviewer matrix required, walkthrough alone insufficient):

Run **three** queries per PR (option availability must be verified before composing the option set — never present an option whose action cannot actually execute):

```bash
# 1. CodeRabbit walkthrough
gh pr view <N> -R <repo> --json comments --jq '.comments[] | select(.author.login == "coderabbitai") | {created_at, hasWalkthrough: (.body | contains("<!-- walkthrough_start -->"))}'

# 2. Copilot reviewer request + review post
gh pr view <N> -R <repo> --json reviewRequests,reviews --jq '{
  copilotRequested: ([.reviewRequests[] | select(.login == "copilot-pull-request-reviewer")] | length),
  copilotReviewed:  ([.reviews[]        | select(.author.login == "copilot-pull-request-reviewer")] | length)
}'

# 3. Copilot registration availability (org-level — HARD STOP: skip if owner is a user, not org)
gh api 'orgs/<org>/copilot/billing' --jq '{
  seats: .seat_breakdown.total,
  active: .seat_breakdown.active_this_cycle,
  management: .seat_management_setting
}' 2>/dev/null || echo "Copilot billing query failed (likely user-owned repo or no permission)"
```

**Availability gate (HARD STOP)**: If query 3 returns `active: 0` or `management: "disabled"` or fails with "Not Found", **Copilot reviewer registration is NOT possible for this PR**. The "Request Copilot review" option in the "Copilot absent" branch becomes inactive — skip the option set and self-decide on `consolidate (CodeRabbit only)` instead. Do not present an ask whose Recommended option is impossible to execute.

Then map to a branch:

| CodeRabbit walkthrough | Copilot requested | Copilot reviewed | Branch (option set) |
|------------------------|-------------------|------------------|---------------------|
| ✅ posted | ✅ requested | ✅ reviewed | **Both reviewers complete** — full consolidate |
| ✅ posted | ❌ not requested | ❌ none | **Copilot absent** — branch (a) register + wait, (b) skip Copilot, (c) hold |
| ✅ posted | ✅ requested | ❌ pending | **Copilot pending** — wait for Copilot completion, then consolidate |
| ❌ rate-limited / pending | — | — | **Walkthrough waiting** — same as original "rate limited" branch |

**Branch: Both reviewers complete** (multiSelect: false):
```typescript
options: [
  { label: "Call consolidate pr-review immediately (Recommended)", description: "/consolidate pr-review <N> — CodeRabbit walkthrough ✅ + Copilot review ✅ both present" },
  { label: "Internal Review first", description: "Self-review via superpowers:code-reviewer → then consolidate" },
  { label: "Hold", description: "Push additional commits and wait for re-review" },
]
```

**Branch: Copilot absent (walkthrough only)** — split by Copilot availability (query 3 result):

**Sub-branch A: Copilot registration available** (org `active >= 1` and `management != "disabled"`) (multiSelect: false):
```typescript
options: [
  { label: "Request Copilot review and wait (Recommended)", description: "gh pr edit <N> --add-reviewer copilot-pull-request-reviewer → wait for Copilot review → then /consolidate pr-review <N>. Aligned with consolidate/pr.md Step 2.5 sequential Copilot policy" },
  { label: "Skip Copilot — consolidate with CodeRabbit only", description: "/consolidate pr-review <N> — Internal Review fallback covers Copilot's domain. Faster but loses Copilot's inline suggestions" },
  { label: "Hold", description: "Decide later" },
]
```

**Sub-branch B: Copilot registration unavailable** (org `active: 0`, `management: "disabled"`, or `Not Found`) — **NO ask** (only one option is actually executable, so do not ask):
- Self-decide on `/consolidate pr-review <N>` immediately (CodeRabbit only with Internal Review fallback)
- Briefly report: "Copilot registration unavailable for this org (verified via `gh api orgs/<org>/copilot/billing`); proceeding with CodeRabbit-only consolidate."
- Do not present the "Request Copilot review" option — it cannot execute and asking wastes a user turn

**Branch: Copilot pending** (multiSelect: false):
```typescript
options: [
  { label: "Register task and wait for Copilot (Recommended)", description: "TaskCreate \"Run /consolidate pr-review <N> after Copilot review arrives\" — call when notified" },
  { label: "Skip Copilot — consolidate with CodeRabbit only", description: "/consolidate pr-review <N> now, ignore pending Copilot" },
  { label: "Hold", description: "Decide later" },
]
```

**Branch: Walkthrough rate limited / pending** (multiSelect: false):
```typescript
options: [
  { label: "Register task and move on (Recommended)", description: "TaskCreate \"Run /consolidate pr-review <N> after CodeRabbit review arrives\" — call when notified" },
  { label: "Manual trigger and wait", description: "Force trigger with @coderabbitai review comment and wait for walkthrough arrival" },
  { label: "Skip consolidate (skip-review)", description: "Apply coderabbit:ignore label → proceed with Internal Review only" },
]
```

| # | Don't | Do |
|---|-------|-----|
| 1 | Stop at a "waiting for review" text report without presenting options | Run reviewer matrix queries, then present options per the matching branch |
| 2 | Offer merge options when walkthrough has arrived | consolidate first — consistent with block-merge-without-review.sh guard |
| 3 | Batch-handle multiple PRs as "all waiting for review" | Check reviewer matrix per PR (CodeRabbit and Copilot states may differ per PR) |
| 4 | Branch on walkthrough alone, ignoring Copilot state | Both reviewers form the matrix. Walkthrough ✅ + Copilot ❌ requires its own option set (Copilot register/skip/hold) |
| 5 | Recommend "/consolidate" when Copilot is absent without making the Copilot decision explicit | Make Copilot status an explicit choice in the option description — user must decide register vs skip vs hold |

## After skill/agent creation

```typescript
options: [
  { label: "Test", description: "Verify activation with trigger keywords" },
  { label: "Review integration", description: "Check for duplicates" }
]
```

## After file creation

```typescript
options: [
  { label: "Review content", description: "Verify created file" },
  { label: "Git add", description: "Stage with git add" }
]
```

## After refactoring

```typescript
multiSelect: true,
options: [
  { label: "Run tests", description: "Verify existing tests pass" },
  { label: "Check performance", description: "Run benchmarks (if applicable)" },
  { label: "Commit", description: "Commit refactoring" }
]
```

## After complex workflow completion

```typescript
multiSelect: true,
options: [
  { label: "Agentify", description: "Convert this workflow to an agent/skill" },
  { label: "Serena memory", description: "Save key learnings to Serena memory" }
]
```

## After project exploration/research

```typescript
multiSelect: true,
options: [
  { label: "Serena memory", description: "Store findings in project memory" },
  { label: "Document", description: "Update project documentation" }
]
```

## After session wrap-up with pending tasks (HARD STOP — TaskList based)

**Precondition**: The session's core work is complete and the user signals wrap-up intent (explicit wrap-up keyword such as "wrap up", "cleanup", "end session"), or only asset cleanup (file moves, doc updates) remains. At least one pending/in_progress task remains for carryover.

**Step 0.5 required — Read TaskList directly to identify pending entries**:

```bash
TaskList   # use pending/in_progress entries as the source
```

### Recommended priority — actionable follow-up over "End session" (HARD STOP)

**"End session" must never be the default Recommended option.** It carries no actionable value beyond what the user already implies by stopping responding; suggesting it autonomously is an autonomous proposal of a work-progression decision (branching / session termination / skipping), which is forbidden. If the user wants to end the session, they will say so or simply stop — `next` does not need to nominate it.

Instead, the **Recommended** option is always **the most actionable follow-up** available. In priority order:

1. **A helper skill invocation that adds value at session boundary** (retrospective cleanup, knowledge persistence, weekly report, file cleanup, etc.) — referenced by **purpose, not by skill name**. Example: `"Run session-cleanup retrospective"` or `"Run session wrap-up tooling"` — the user's skill router picks the matching skill. **Never hardcode an external skill name in this skill's body** — published skill names are out-of-tree dependencies and may rename without notice.
2. **Run the highest-priority pending task immediately**
3. **Resume a BLOCKED pending task with newly available preconditions** (e.g., CI just passed, external response just arrived)

"End session" appears **only as a non-Recommended fallback option**, and only when the user has shown signals consistent with wrap-up intent (explicit wrap-up keyword or 2+ consecutive declines of other follow-ups). In that case, the label is plain `"End session"` — never `"End session (Recommended)"`.

### Option composition rules

#### multiSelect — combinability check FIRST (HARD STOP)

**Before applying the layout table below, decide `multiSelect` by whether the follow-up options can be performed *together*, NOT by copying the table's default.** If 2+ options are independent actions the user could reasonably want done in one go (e.g. "commit the changes" + "update the doc" + "deploy"), set **`multiSelect: true`**. The `false` rows below apply ONLY to the mutually-exclusive "pick ONE next action OR end session" model. Recurrence cause (repeated user feedback): blindly applying the table's `false` default without the combinability check on additive follow-ups.

| # | Don't | Do |
|---|-------|-----|
| 1 | Apply `multiSelect: false` from the table without checking combinability | First ask yourself: "could the user want 2+ of these done together?" → Yes ⇒ `multiSelect: true` |
| 2 | Treat every wrap-up ask as single-select because the table says `false` | Combinable follow-ups (commit / doc / deploy / verify) are additive ⇒ `true`. Mutually-exclusive (one path vs end) ⇒ `false` |
| 3 | Include an "End session" option in a `multiSelect: true` ask | With `true`, selecting nothing = end. Drop the "End session" option |

| Pending count | multiSelect | Option layout |
|------------|-------------|----------|
| 0 | — | Skip ask entirely (no actionable follow-up exists). Do not generate a single "End session" option |
| 1 | false | `[Recommended: run helper skill OR run pending task, Defer to next session, Hold]` — quote task subject |
| 2~3 | **combinable ⇒ true** (independent actions doable together; no "End session" option) / false (mutually-exclusive paths) | true: additive options, not-selecting = end. false: `[Recommended, per-task run-now, End session last]` |
| 4+ | **combinable ⇒ true** / false (max 4) | true: top combinable actions, no "End session". false: top 3 (Recommended top) + `End session` last (no marker), note "carryover N items" |

**Helper-skill recommendation phrasing (skill name hidden)**:

```
{ label: "Run session retrospective + cleanup (Recommended)", description: "Invoke the session-cleanup helper to record this session's lessons + tidy temporary tasks. Skill router picks the matching tool." }
```

### Self-check (HARD STOP — before drafting the option array)

For every option you are about to include, answer:

1. **What concrete next-turn action does this option trigger?** If the answer is "the session ends without further action," that option is `End session` and **must not** be Recommended.
2. **Does my Recommended option add value the user could not get by simply not responding?** If no, choose a different option as Recommended.
3. **Is this an autonomous proposal of a work-progression decision (branching / session termination / skipping)?** If the user has not explicitly requested wrap-up, the entire wrap-up pattern may not apply — re-route to a regular next-action ask.
4. **Is my Recommended option referencing a helper by purpose (not skill name)?** Hardcoded skill names break when external skills rename.

### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Recommend only "1-2 immediately actionable" among pending | All pending as candidates. State trigger conditions in description |
| 2 | Quote task names from summary memory | Call TaskList and quote real subjects |
| 3 | Expose TaskList-internal `#NN` IDs in option descriptions | TaskList-internal IDs must not appear in user-visible output — reference via subject keyword |
| 4 | Mark "End session" as `(Recommended)` or place it first | "End session" is a fallback option only — never the default. Place it last with a plain label |
| 5 | Generate a "wrap-up" ask when the user has not signaled wrap-up intent | Only enter this pattern when the user used a wrap-up keyword or 2+ consecutive declines occurred |
| 6 | Hardcode an external skill's name in the option label | Refer to the helper by **purpose** (e.g., "session retrospective tooling") so the user's skill router resolves it; out-of-tree skill renames don't break this skill |
| 7 | Recommend a helper skill invocation that produces no artifact (vague "wrap up") | The helper must produce a concrete artifact (retrospective entry, cleanup report, persistence record). Vague "wrap up" = same as "End session" |
| 8 | Skip TaskList Read before wrap-up ask | TaskList every time per Step 0.5 |
| 9 | Compose the wrap-up ask **inline** without invoking `/next` and skip rows 1–8 because "I know the rule" | The rule is enforced by the skill's Self-check gate. **Inline composition = skill bypass = same gate applies**. Either call `/next` formally OR self-execute every row in this table + the 4-step Self-check before posting. Pattern: writing "Delete X + end session (Recommended)" as option 1 inline ≡ violating row 4 |
| 10 | Generate two end-session-like options ("X + end session" + "End session, leave Y") | At most 1 plain `End session` option, last, no Recommended marker. Multiple end-variants = recurrence signal — re-check Self-check rows 1–2 |

### Example (2 pending, right after asset cleanup)

```typescript
AskUserQuestion({
  questions: [{
    question: "Asset move complete. Next action for this session?",
    header: "Next Action",
    multiSelect: false,
    options: [
      { label: "Run session retrospective + cleanup (Recommended)", description: "Trigger the session-wrap-up helper — records what worked / what did not into the failed-attempts log and prunes completed session tasks. Skill router picks the matching tool." },
      { label: "Run cleanup-RalphExit task now", description: "Note Ralph exit point right before cleanup run.md Phase 2 — ready to start" },
      { label: "Run RalphCB-no_progress task now", description: "Analyze CB OPEN no_progress misclassification — ready to start (analysis task)" },
      { label: "End session", description: "Carry over 2 tasks (cleanup Phase 2 Ralph exit note, CB no_progress misclassification analysis) to next session. Fallback if none of the above fits." },
    ]
  }]
})
```

## After PR consolidate (after AI Review Summary is posted)

**Precondition**: Completed `consolidate/pr-review.md` through Step 7 (Internal Review + AI Review Summary posted).

**Authorship gate (HARD STOP — check FIRST)**: merge options below apply **only when the PR is authored by the current account**. `gh pr view <N> --json author` → if author ≠ current account, you are a reviewer on someone else's PR: **omit all merge options** (merging is the author's domain — branch ownership). Offer review-scoped options only (relay deferred findings to author / hold / done — review complete). Do not present "Squash merge" or "Apply minor then merge" on another's branch.

**Merge option guard** (`block-merge-without-review.sh` pass-through conditions):
- Description must include "AI Review Summary posted (\<URL\>)" or "AI Review Summary ✅"
- Or replace with a non-merge option such as "consolidate pr-review first"

**When all 4 merge conditions are met** (multiSelect: false):
```typescript
options: [
  { label: "Squash merge (Recommended)", description: "AI Review Summary posted (<comment-URL>) | CI ✅ | Test Plan ✅ | Mergeable ✅" },
  { label: "Apply minor findings, then merge", description: "Apply N Minor findings → CI pass → merge" },
  { label: "Hold", description: "Decide after further review" },
]
```

**When Test Plan has unchecked items** (multiSelect: false):
```typescript
options: [
  { label: "Verify unchecked items (Recommended)", description: "Verify N items via web-browser / curl → mark [x] → merge" },
  { label: "Move to separate issue, then merge", description: "Register the unchecked items as a follow-up issue and remove from this PR's Test Plan" },
  { label: "Hold", description: "Decide after verification" },
]
```

**When CI fails (unrelated to PR)**:
```typescript
options: [
  { label: "Report CI failure cause + register separate issue", description: "Register an issue noting unrelatedness to PR changes + assess mergeability" },
  { label: "Self-approve + merge (if confirmed unrelated)", description: "AI Review Summary posted (<URL>) | E2E confirmed unrelated to PR | Squash merge" },
  { label: "Hold", description: "Wait for CI to pass" },
]
```

**Actual merge is executed only via the `/github-flow merge` skill** — register as a follow-up task after option selection.

