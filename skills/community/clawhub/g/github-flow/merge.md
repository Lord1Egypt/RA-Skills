# Merge

Perform a final quality check on a PR (CI / Review), then merge and clean up the commit message according to the rules.

## When to Use

- On requests like "merge the PR", "confirm reviews and merge", "merge if CI passed"
- When integrating a fully implemented and reviewed PR into the main branch
- Whenever you want a final, pre-merge sanity check on CI success and AI-review actionable status

## Merge condition checks (every condition must pass)

**Even when supervising / reporting, check these first** — never ask "shall we merge?" on a PR that does not satisfy the conditions.

### 1. CI success (real-time)

```bash
gh pr checks <PR_NUMBER>
```
- If any `fail`, stop. If `pending`, wait.
- Required to be confirmed **in real time** — don't rely on a state recorded in fix_plan.

#### CI rerun result verification (MANDATORY when `gh run rerun` / `gh workflow run` was invoked)

After triggering CI (`gh run rerun <run-id> --failed`, `gh workflow run`, etc.) the **final result must be reported** — reporting only "in_progress" is forbidden.

Procedure:
1. Trigger: `gh run rerun <run-id> --failed` or `gh workflow run`
2. Wait for completion: `gh run watch <run-id>` (or poll `gh run view --json status,conclusion` every 30s)
3. Report SUCCESS/FAILURE; on failure, summarize the root cause

If the wait is expected to exceed 2 minutes, launch `gh run watch` with `run_in_background: true` and report on the completion notification.

#### Post-CI followup decision table (MANDATORY after CI SUCCESS)

After confirming CI success, run this table sequentially — do not stop at "CI passed".

| Condition | Action | Command |
|-----------|--------|---------|
| CI SUCCESS | **Check whether the AI Review Summary comment is posted** | `gh pr view <N> --json comments` → search for the user-authored AI Review Summary comment |
| AI Review Summary **missing** | **Run `/consolidate pr-review` FIRST** — consolidate precedes Test Plan verification, which only runs after consolidate completes | `Skill("consolidate", "pr-review")` |
| AI Review Summary **posted** (or consolidate-exempt PR) | Check the PR body Test Plan | `gh pr view <N> --json body` |
| Test Plan has unchecked `- [ ]` items | Verify the unchecked items (deploy, Playwright, API call, etc.) → on pass, mark `- [x]` | `gh pr edit <N> --body` |
| Test Plan fully `[x]` | Record CI success in `fix_plan.md` and check off the entry | Edit `fix_plan.md` |
| Related issue exists | Check off the relevant items in the issue body checklist | `gh issue edit <N> --body` |
| All complete | Move to the next pending item (fix_plan or TaskList) | — |

**CI success ≠ work complete**: every Test Plan item checked + fix_plan reflected + issue body updated is the actual completion criterion.

##### Direct-to-master projects (no PR) — fix_plan reflection still mandatory

For projects pushing directly to master (e.g., infra-provisioning repos), commit + push + CI success **still requires** `fix_plan.md` reflection.

| Condition | Action |
|-----------|--------|
| commit + push + CI passed | Mark the relevant `fix_plan.md` item `[x]` or update its status |
| Related TaskList entry exists | `TaskUpdate(status: "completed")` |
| New infrastructure artifact (deploy, migration, etc.) | Record the result in `fix_plan.md` (commit SHA, environment, status) |

| # | Don't | Do |
|---|-------|-----|
| 1 | Stop at "commit + CI confirmed" without updating `fix_plan.md` | Update the relevant `fix_plan.md` entry to `[x]` + `TaskUpdate completed` |
| 2 | Assume "no PR workflow, so no fix_plan update needed" | Whether PR-based or master-push, `fix_plan` reflection is equally mandatory |

### 2. AI Review Summary — every Actionable item addressed

**Default procedure (HARD STOP — strict order)**:

0. **Verify a real Copilot review error** (explicit error keywords only — beware of false positives):

   ```bash
   gh pr view <PR_NUMBER> --json reviews -q '.reviews[] | select(.author.login == "copilot-pull-request-reviewer") | select(.body | test("encountered an error|unable to review"; "i")) | {state, bodyLen: (.body | length)}'
   ```

   - Result empty → proceed to Step 1 (a short body or the absence of a "Reviewed changes" section may still be a normal review on a simple PR — do NOT flag a false positive)
   - Result matched → real error → re-request Copilot (`gh pr edit <PR_NUMBER> --add-reviewer copilot-pull-request-reviewer`) → wait for the normal review to arrive, then proceed to Step 1

   **Forbidden**: declaring a partial failure just because the `Reviewed changes` section is missing or the bodyLen is short. Copilot does post short reviews to simple PRs (e.g. PR #110 merged, bodyLen 2040, inline comments only, no `Reviewed changes` section).

1. **Check whether the AI Review Summary comment exists**:
   ```bash
   gh api repos/{owner}/{repo}/issues/<PR_NUMBER>/comments --jq '.[] | select(.body | startswith("## AI Review Summary"))'
   ```

2. **No Summary comment → unconditionally auto-invoke `/consolidate pr-review`**:
   - **If any AI review (CodeRabbit / Copilot / etc.) is present, consolidate is the default** — not optional
   - After consolidate, confirm the Summary comment was posted → continue to Step 3
   - **Forbidden**: asking the user a merge / apply option without the Summary. consolidate must run first

3. **Summary comment exists → count 🔴 Critical (HARD STOP)**:

   ```bash
   # Count 🔴 Critical entries in the Summary body
   gh api repos/{owner}/{repo}/issues/<PR_NUMBER>/comments \
     --jq '.[] | select(.body | startswith("## AI Review Summary")) | .body' \
     | grep -c '🔴 Critical'
   ```

   - **🔴 Critical ≥ 1 → merge is absolutely forbidden**. Address the Critical items in code, then refresh the Summary before merging. "deferred" is not allowed — Critical items must be addressed
   - 🔴 Critical 0 + `Actionable > 0` not yet addressed → use AskUserQuestion to confirm the action (apply / deferred / skip)
   - If everything is addressed or explicitly deferred, continue to Step 2.5

**Forbidden patterns**:
- ❌ AI review exists, but you bypass consolidate and ask the user to merge directly
- ❌ Interpreting "if no Summary, run consolidate" as "you can skip it"
- ❌ Looking only at CodeRabbit and missing the Copilot review (both must be consolidated)

### 2.5. Verify deferred Actionable items are registered in a tracking medium (HARD STOP)

**If ≥1 Actionable items are explicitly marked "deferred" on the Summary, before merging, verify they are registered as `[BLOCKED]` in a tracking medium.** If not registered, block the merge.

#### Verification procedure

1. **Identify deferred items**: count items decided as deferred on the Summary body (e.g. "🟡 Minor (optional)", "🟡 Minor (No action)", "🔴 Critical not addressed")
2. **Verify tracking-medium registration** (per environment):

   ```bash
   # fix_plan tracker — workspace-relative path per fix-plan SKILL.md `task-tracker` config
   # (e.g., Ralph wrappers place it at {workspace}/.ralph/fix_plan.md; vanilla workspaces use {workspace}/fix_plan.md)
   # Note: the inner class uses an explicit set (`[A-Za-z0-9:]+`) instead of `[^]]+` —
   # BSD grep (macOS) raises "brackets ([ ]) not balanced" on `[^]]`, so the explicit
   # set is the portable form across GNU + BSD ERE.
   grep -cE '\[BLOCKED(:[A-Za-z0-9:]+)?\].*\[REVIEW_FEEDBACK\].*PR #<N>' <fix_plan tracker path>

   # checklist tracker (non-Ralph workspaces) — same BSD-portable class
   grep -cE '\[BLOCKED(:[A-Za-z0-9:]+)?\].*PR #<N>' {workspace}/checklist.md

   # GitHub Issue tracker
   gh issue list --search "deferred from PR #<N>" --state open --json number
   ```

   The `[BLOCKED(:[^]]+)?\]` pattern matches both the plain `[BLOCKED]` form and the priority-annotated `[BLOCKED:P0-P3:reason]` form (see fix-plan/priority.md).

3. **Compare counts**: deferred-item count ≤ medium-registration count → proceed. deferred-item count > medium-registration count → block the merge

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Treat the "deferred" tag in the Summary table as registration | The Summary is a one-shot GitHub comment. Registration in a medium (fix_plan / checklist / Issue) must be verified separately |
| 2 | Interpret "if deferred is stated, merge is allowed" as "merge regardless of medium registration" | Merge requires BOTH explicit deferred + medium registration |
| 3 | On missing registration, ask the user "shall I register?" via options | `consolidate/pr-review.md` Step 7.6 handles auto-registration. Missing = consolidate-procedure violation → re-invoke consolidate, then re-verify |
| 4 | Treat a "we'll register when the user picks merge" promise as actual registration | A promise ≠ an action. Decide based on actual lines existing in the medium file |

#### Self-check (every time, before merging)

1. Is there ≥1 deferred Actionable item on the AI Review Summary?
2. If yes, did you check medium-registration counts with grep / gh per environment?
3. Did you confirm `deferred count = registered count`? (Block on mismatch)
4. Did you include the registration medium path / Issue number in the merge decision report?

### 3. Test Plan — per-category merge guard

Apply the PR-body Test Plan category classification rule (pr.md "Test Plan category classification" section) at merge time. Guards differ by category prefix (`[general]` / `[UI]` / `[post-merge]`).

```bash
gh pr view <PR_NUMBER> --json body
# Or chain a project-local verification script:
gh pr view <PR_NUMBER> --json body --jq '.body' | node scripts/check-test-plan.js
```

| Category prefix | Guard when unchecked |
|-----------------|----------------------|
| `[general]` | **Cannot merge** (HARD STOP, no exception) |
| `[UI]` | **Cannot merge** (HARD STOP, no exception) |
| `[post-merge]` | **Merge allowed** (but tracking-medium registration must be verified — procedure below) |
| No prefix (legacy) | Treated as `[general]` or `[UI]` — **cannot merge** |

#### `[post-merge]` items — verify tracking-medium registration (HARD STOP)

If ≥1 `[post-merge]` items exist, confirm they are registered in a tracking medium before merging:

```bash
# Extract [post-merge] items from the PR body
# Category prefix output format is **[post-merge]** (bold bracket); tolerate legacy `[post-merge]` (backtick) too.
gh pr view <PR_NUMBER> --json body --jq '.body' | grep -E '^- \[.\] (\*\*\[post-merge\]\*\*|`\[post-merge\]`)'

# Verify each item names a tracking link (issue # or fix_plan path)
# 0 items without a tracking link is required to merge
```

| # | Don't | Do |
|---|-------|-----|
| 1 | `[post-merge]` item without a tracking medium → post-merge verification gets dropped | Inline `(tracking: gh issue #N)` or `(tracking: fix_plan.md [BLOCKED])` in the item description before merging |
| 2 | Misclassify essential validation as `[post-merge]` to bypass the merge guard | Apply the "essential vs adjacent follow-up" self-check — essential validation belongs to `[general]` / `[UI]` |

#### Runtime-verification → PR-body sync (HARD STOP)

After verifying a Test Plan item at runtime (API call, Playwright, `curl`, etc.), immediately mark the corresponding `- [ ]` in the **PR body** to `- [x]`. Checking only `fix_plan.md` is insufficient — the PR body is the primary tracking medium.

| # | Don't | Do |
|---|-------|-----|
| 1 | Check off `fix_plan.md` `[x]` but skip updating the PR body | `fix_plan` `[x]` + `gh pr edit --body` so the PR body also shows `[x]` |
| 2 | Conclude "the PR is MERGED, so updating the body is pointless" | A MERGED PR body can still be edited — record the verification trail for auditability |

#### "Check the Test Plan" command handling (HARD STOP)

When the user issues "check the PR Test Plan", "verify tests", "check it for me", etc., **all items must be re-run + results reported + then [x]/[ ] decided**. A simple grep that keeps existing `[x]` rows untouched and PATCHes only unchecked rows is a violation. Per-item workflow: **(a) execute → (b) report result → (c) decide [x]/[ ]**.

##### Per-item handling

| Item type | Execution medium | Treatment |
|-----------|-----------------|-----------|
| `pnpm test` / `pnpm check-types` / unit-test command | Run directly on the PR head commit (or a worktree) | Pass → `[x]` + result meta (e.g., "313/313 PASS, YYYY-MM-DD") / Fail → `[ ]` + reason |
| `CI E2E` / `Playwright` / other CI-run items | Query latest CI run result (`gh run view <ID>`) | `conclusion=success` → `[x]` + run ID + date / unrun or failed → `[ ]` |
| `curl <URL>` / `[runtime] <service> behavior` | Call directly (or via Playwright) | Verified response → `[x]` + response status + date / Fail → `[ ]` + response body |
| `[post-merge]` / `[deploy]` prefix | Out of this cycle (separate post-merge cycle) | Keep `[ ]` + note "out of this cycle — follow-up work" |
| **Existing `[x]` items (already checked)** | Re-run if visibility is in doubt (env drift, time passed) | Re-verified → keep `[x]` + add re-check meta / Re-fail → flip to `[ ]` + report |

##### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | "Already `[x]`, so skip" — only PATCH the unchecked items | **Re-run every item**. After environment changes (drift, time), re-verification is the 1st-priority outcome |
| 2 | PATCH PR-body Test Plan `[x]` based only on overall CI status | Map each Test Plan item to the specific CI job that verified it → state job conclusion + run ID + date |
| 3 | Mark `[x]` from a code Read / `package.json` script inspection ("it could run, so I declare pass") | **Actually execute the command + capture output**. Reading code is not a verification medium |
| 4 | One command (`pnpm --filter dt test`) produces N `[x]` marks at once | Map each Test Plan item to the command executed 1:1 in the report. Unmapped items stay `[ ]` |
| 5 | Report only the unchecked items PATCHed; skip re-verifying existing `[x]` | Re-verify the existing `[x]` in this same cycle and report the result (add "re-verified pass" meta) |
| 6 | Omit result meta (run ID / date / response status / N/M PASS) | Each `[x]` carries verification medium + result + date so future readers can trace "when, by what, verified" |

##### Self-check (every time the user issues "check Test Plan")

1. Enumerate **every** Test Plan item in the PR body (`[x]` and `[ ]`). Reporting only the unchecked rows is forbidden
2. Identify each item's execution medium (match the table above)
3. Re-run **every item** (including existing `[x]`). Map results 1:1 per item in the report
4. After reporting, decide `[x]`/`[ ]` → `gh pr edit --body` or `gh api PATCH .../pulls/<N>` (multi-line bodies go via a JSON file per `git.md`)
5. `[post-merge]` / `[deploy]` items: stay `[ ]` and note "out of this cycle"
6. Summarize the report as "Test Plan re-run: X/Y passing, Z out of cycle"

##### Exceptions

- User explicitly says "only the unchecked items" / "verify only the unchecked" → skipping re-verification of existing `[x]` is allowed
- Without an explicit instruction, default = re-run all

Legacy PRs (Test Plan without category prefix): the existing HARD STOP applies — if even one `- [ ]` is unchecked, you cannot merge. For items not executable before merge, change to a tracking annotation like `- [x] (verify post-deploy — tracked in issue #N)` + AskUserQuestion approval (but NEVER use the tracking annotation to bypass essential validation).

A PR with no Test Plan is unaffected by this condition.

### 3.5. Blocked by — all predecessor issues CLOSED (HARD STOP)

If the issue this PR closes (or the PR itself) has GitHub Issue Dependencies (`blockedBy`) set, **every predecessor issue must be CLOSED** to merge. See [dependencies.md](./dependencies.md) for details.

```bash
# Extract issues the PR closes (Closes/Fixes keywords + linked issues)
gh pr view <PR_NUMBER> --json closingIssuesReferences -q '.closingIssuesReferences[].number'

# For each soon-to-close issue, query blockedBy
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql -f query='
  query { repository(owner:"<owner>", name:"<repo>") {
    issue(number:<N>) {
      blockedBy(first:10) { nodes { number state title } }
      issueDependenciesSummary { totalBlockedBy }
    }
  } }
'
```

**Decision rule**:

| `blockedBy` node state | Action |
|------------------------|--------|
| All `CLOSED` | OK — can merge |
| ≥1 `OPEN` | **Cannot merge** — report the OPEN predecessor's number + title, ask via AskUserQuestion (e.g. "predecessor issue #N is unresolved. How shall we proceed?") |
| `blockedBy` empty | OK — no dependencies |

**Forbidden patterns**:
- ❌ Merging on your own judgment "it's unrelated" when `blockedBy` has an OPEN issue
- ❌ Force-closing the predecessor at the last minute then merging (actual work incomplete)

**If the predecessor will soon be closed by another PR**: re-order so this PR merges after that PR. Use AskUserQuestion to get the user's decision.

#### Distinguish PR essential validation vs adjacent follow-up validation (HARD STOP)

When marking an unchecked Test Plan item as `[x] (post-merge verification — tracked separately)`, **always self-check the essential vs adjacent classification**. Do not use the tracking annotation to bypass essential validation.

**Classification rule**:

| Class | Definition | Handling |
|-------|------------|----------|
| **PR essential validation** | The goal stated in the PR title / body. This validation must SUCCEED for the PR to truly solve the problem | **Must verify before or immediately after merge.** Tracking annotation `[x]` is forbidden |
| Adjacent follow-up | A byproduct of the PR change. Environment impact, regression monitoring, etc. | Tracking annotation `[x]` is allowed |

**Self-check procedure (right before marking a Test Plan item as `[x]` tracking)**:
1. Extract the PR's core goal in one sentence ("the essence of this PR is solving X")
2. Determine whether the unchecked item is a direct verification of X:
   - "X workflow SUCCESS check" / "X behavior verified" / "X passed" → **essential validation**
   - "environment impact monitoring" / "regression tracking" / "follow-up PR work" → adjacent follow-up
3. If essential → do NOT mark `[x]`. Consider triggers that can be executed before or immediately after merge:
   - manual `workflow_dispatch`
   - cross-repo trigger (e.g. PAT-authenticated `repository_dispatch`)
   - real user-scenario reproduction (curl, Playwright)
4. If no immediately-executable trigger → **do not merge**. Use AskUserQuestion only to decide "how to verify". Merging while unchecked is absolutely forbidden

**Correct flow** (essential validation):
1. If the unchecked item is essential → attempt a trigger before merge (e.g. manual workflow_dispatch + watch, infra dry-run, curl)
2. After SUCCESS, check `[x]` → merge
3. If a trigger is impossible → **do not merge**. Decide a verification approach with the user, execute it, check `[x]`, then merge

**Absolutely forbidden (2nd recurrence — HARD STOP strengthened)**:
- The "merge with unchecked items after user consent" path is closed. Even if the user says "go ahead", do not run `gh pr merge` while any `- [ ]` remains
- "Record and proceed" = "record this fact" + "proceed to the next step (verification / deploy)", NOT "approval to merge unchecked"

#### HARD STOP — Self-check for the merge-option AskUserQuestion (five conditions)

Before recommending merge (AskUserQuestion option includes "proceed merge" / "squash merge"), **self-check all five conditions**:

| # | Condition | How to verify | If not satisfied |
|---|-----------|---------------|------------------|
| 1 | All CI PASS | `gh pr checks <N>` → confirm bucket=pass | Exclude "merge" from options |
| 2 | All Test Plan `[x]` | `gh pr view <N> --json body --jq '.body' \| node scripts/check-test-plan.js` → exit 0 | Exclude "merge" from options |
| 3 | AI Review Summary comment posted | `gh pr view <N> --json comments` → confirm a user-authored "AI Review Summary" body | consolidate invocation required |
| 4 | Mergeable | `gh pr view <N> --json mergeable` → MERGEABLE | Resolve conflicts first |
| 5 | Cross-repo infrastructure dependency | Inspect PR body / code for cross-repo env-var or infrastructure changes | Block merge until the dependent repo's change is merged + deployed |

**Condition 5 in detail — cross-repo dependency (HARD STOP)**:
- The code references a new env var (`process.env.X`, `lookup('env', 'X')`) that is supplied by an infra repo's inventory / template
- **The infra-repo PR must be merged + deployed first** before the app code can merge
- Order: infra variable-addition PR merged → infra deploy → app code PR merged → app deploy
- **Forbidden**: merging the app code first and deferring the infra as a "follow-up PR" — at deploy time the missing env var breaks the feature

**If even one condition is unsatisfied, ALL of the following are forbidden**:
- Including "proceed merge" / "squash merge" / "merge recommended" in AskUserQuestion options
- Bypassing unsatisfied conditions with phrases like "Playwright will run separately", "ZAP will follow", while still recommending merge
- Concluding "the core passed, so merge is fine" on your own judgment
- Concluding "AI bot comments exist, so OK" on your own (the consolidate Summary is separate)

#### CI fail — analyze the essence + state the merge value (HARD STOP)

Before recommending merge on a PR with CI fails, **state both**:

1. **Essence analysis of each CI fail (self-check per fail entry)**:
   - **Is the fail resolved by this PR?** → if so, wait until it passes, then merge
   - **Is the fail unrelated to this PR?** → register a separate issue + name the issue in the PR body + guarantee the fail is not permanently masked by this PR
   - **Is the fail intentional `continue-on-error`?** → record the GUARD reason in the PR body + name a separate tracking issue

2. **Merge value (diff with merging vs not merging)**:
   - What changes between pre-merge and post-merge? (code coherence, regression prevention, unblocking subsequent work — concretely)
   - If merging is not strictly required, deferral may be a better option — if the value is unclear, offer a defer option

**Forbidden pattern** (no statement of "what got better" from the user's POV):
- ❌ 2 CI fails → "continue-on-error / tracked separately" → recommend merge. No value statement
- ❌ Abstract phrasing like "merging restores env coherence with the master fixture". State concrete changes
- ❌ Treating fails as "deferred" without a separate tracking issue and merging — tracking lost

**Correct flow** (PR with CI fails):
1. Report the essence-analysis result text per fail
2. On detecting "fails this PR does not resolve" → **prefer reusing an existing tracking issue** (Step 2-A) → if none, register a new issue (Step 2-B)
3. State the merge value in one line (concrete): "Merging makes the master fixture use `service-A-source` → prevents regressions in the next PR + guarantees coherence at dev-A/integration/production rollout"
4. Then issue AskUserQuestion or auto-merge

**Step 2-A: prefer reusing an existing issue (HARD STOP)**

Before suggesting a new issue, search:

```bash
# 1. PR trigger issue (look at Resolves / Relates to / Closes keywords in the PR body)
gh pr view <PR> --json body -q '.body' | grep -iE 'Resolves|Relates to|Closes|Fixes' | head

# 2. Open issues with the same label / area
gh issue list -R <owner>/<repo> --state open --label <label> --json number,title

# 3. Existing issues by fail keyword
gh search issues "<fail keyword>" --repo <owner>/<repo> --state open
```

**Decision**:
- If a trigger issue exists and the fail falls in its scope → **add the unresolved item to the trigger-issue body** (do not close; reopen or leave as-is)
- If an open issue in the same area is found → **add the fail item to that issue body**
- If no search hits → register a new issue (Step 2-B)

**Forbidden pattern**:
- ❌ Suggesting a new issue without checking the trigger issue. The same environment inconsistency ends up split across issues with fragmented tracking
- ❌ When `Resolves #N` is stated in the PR, suggesting a new issue after solving only part of it → adding the unresolved item to `#N`'s body is the canonical fix

**Step 2-B: register a new issue (only when no existing issue applies)**

Use `/github-flow plan-to-issue` or `gh issue create`.

**Correct flow** (on any unsatisfied condition):
1. Test Plan unchecked → run verification directly → check `[x]`
2. AI Review Summary missing → invoke the consolidate skill → Summary posted → actionable addressed
3. CI failure → root-cause analysis + fix
4. Conflicts → resolve conflicts
5. Only after all four are satisfied may you offer a merge option. Merge only when the user explicitly says "merge now" (auto-recommendation is forbidden)

#### Pre-approved context — skip AskUserQuestion (auto-merge)

When all four merge conditions are satisfied AND **the user pre-approved a workflow that includes merging**, skip AskUserQuestion and run squash merge immediately. Asking again is redundant and delays progress.

**Pre-approval patterns** (the user's answer / instruction contains expressions like):
- "wait for the predecessor PR to merge" / "proceed after the PR merges" / "next step after merge"
- "merge if conditions are satisfied" / "merge once CI passes" / "squash once it passes"
- "handle the preliminary work" + the workflow includes a merge step
- "run it through to the end" / "do it all in one go" + the workflow is named

**❌ Non-pre-approval patterns (HARD STOP — do not auto-recommend the merge option)**:

The following expressions mean "inspect / review / check" — NOT permission to merge. Even if a merge keyword appears in the option description, auto-recommending merge is a violation:

- "review merge conditions" / "check merge conditions"
- "see if mergeable" / "look into whether it can merge"
- "inspect conditions" / "review" / "check" / "inspect" (when used alone)
- A merge word in the option description, when the verb is "review / check / inspect / look", is not approval
- The user must add an explicit **action verb** like "then merge" / "merge once it passes" / "proceed when conditions hold"

**Decision rule (option self-check)**:

| User answer / option phrasing | Intent | Auto-recommend the merge option |
|-------------------------------|--------|---------------------------------|
| "merge if conditions are satisfied" | Approval (conditional action) | ✅ auto-merge or recommend the option |
| "merge after CI passes" | Approval | ✅ |
| "review merge conditions" | Non-approval (inspect) | ❌ exclude merge from options; offer "report conditions only" |
| "check if mergeable" | Non-approval (inspect) | ❌ |
| "inspect conditions" | Non-approval (inspect) | ❌ |
| "run it through to the end" + workflow names merge | Approval | ✅ |

**Correct flow** (non-approval pattern + conditions satisfied):
1. Report the five-condition self-check result as text ("CI ✅, AI Review ✅, Test Plan ✅, Mergeable ✅")
2. Use AskUserQuestion to **confirm merge intent separately** — "All conditions satisfied. Proceed with merge?" (options: "merge now" / "defer" / "additional review")
3. Run `gh pr merge --squash` only when the user picks "merge now"

**Auto-merge procedure**:
1. Self-check the five conditions (CI / Test Plan / AI Review Summary / Mergeable)
2. If all satisfied → skip AskUserQuestion, run `gh pr merge --squash`
3. If any unsatisfied → AskUserQuestion explaining the blocker + suggesting how to clear it (independent of pre-approval)

**Forbidden patterns**:
- "Wait for the predecessor PR to merge" answer → after the PR is created + five conditions satisfied → asking "shall I merge?" again (redundant)
- Mis-interpreting a pre-approval answer as "inspect intent" instead of "merge intent"

### 4. Mergeable status

```bash
gh pr view <PR_NUMBER> --json mergeable
```
- If `CONFLICTING`, resolve conflicts first.

### Per-repository Formal Review policy

| Repository profile | Self-approve | Formal Review |
|--------------------|--------------|---------------|
| Org-protected app repo | Not allowed | **Skip** — replaced by CI + AI Review + Test Plan |
| Solo-maintained infra repo | Allowed (solo) | Replaced by AI Review APPROVE |

- For an org-protected app repository where self-approve is not allowed, the formal-review condition is skipped.
- If all five conditions above pass, the PR can be merged.

## Merge Execution

### Squash Merge (recommended)

Most feature work / bug fixes use squash merge. Clean up the commit message per the rules:

1. **Subject**: start from the PR title with redundant tags (e.g. `[WIP]`, `[DRAFT]`) removed. **Subject MUST end with ` (#<PR_NUMBER>)` suffix** (HARD STOP) — matches GitHub's native squash default format. Enforced by `~/.claude/hooks/block-squash-subject-without-pr.sh` (PreToolUse:Bash): blocks `gh pr merge --squash` when (a) `--subject` is absent or (b) `--subject` value does not end with `(#<digits>)`.
2. **Body**:
   - Distill the key content from the PR body's "Changes" or "Key changes" section.
   - Include `Closes #issue` or `Fixes #issue`.
   - On a PRIVATE repo you MAY add a non-sensitive trace reference (e.g. a short workspace identifier) if your team relies on one. On a PUBLIC repo, **do not embed session identifiers / personal handles / internal IDs** — they survive in `git log` forever and violate the sanitize HARD STOP introduced elsewhere in this skill.

```bash
# Example (PUBLIC repo — subject ends with (#<PR_NUMBER>), no internal identifiers in body)
gh pr merge <PR_NUMBER> --squash --subject "feat: add user session countdown UI (#<PR_NUMBER>)" --body "- JWT-exp-based countdown hook and header UI\n- Closes #253"
```

### Regular Merge (merge commit)

Use only when preserving commit history matters (e.g. merging large deploy branches).

```bash
gh pr merge <PR_NUMBER> --merge
```

## Rules

- **Always confirm**: `gh pr checks` right before merging is non-optional.
- **Message quality**: at squash time, write a message that actually reveals the work — not GitHub's default "Merge pull request #..." text.
- **Post-merge cleanup**: after a successful merge, delete the local branch and check the corresponding `fix_plan.md` item as `[x]`. **Worktree removal requires AskUserQuestion (HARD STOP)** — `git worktree remove` is a destructive action and the `git-repo` skill recommends reusing worktrees for the next PR rather than removing them. After merge, the worktree must be left in place by default; only remove on explicit user instruction. Listing "remove worktree" as a default cleanup step (or executing it autonomously) is forbidden.
- **Post-merge AI Review Summary sync (HARD STOP)**: after a successful merge, immediately PATCH the AI Review Summary comment (the one posted in `consolidate/post.md` Step 7) to reflect the merged state — do NOT leave the Summary frozen at its pre-merge snapshot. The Summary is the user-facing record of the PR's final disposition; if it still says "⏳ Actionable PENDING" or shows an incomplete Test Plan after merge, anyone reading the PR later will see a contradictory record.
  - **What to update**: (a) verdict line: `⏳ Actionable PENDING fix.` → `✅ MERGED <YYYY-MM-DD>` + merge commit SHA + `(#<PR>)` suffix. (b) findings table `Status` column: each "⏳ Pending decision" → either `🟢 Applied (commit <sha>)` or `🟢 Deferred (<tracking-medium reference>)` per the actual outcome. (c) any inline "Test Plan N/M items checked" → "Test Plan M/M ✅" if CI re-pass confirmed.
  - **How**: `gh api repos/{owner}/{repo}/issues/comments/{comment_id} -X PATCH --input <(jq -n --rawfile body <updated-summary-file> '{body: $body}')` — find the comment id via `gh api repos/{owner}/{repo}/issues/{N}/comments --jq '.[] | select(.body | startswith("## AI Review Summary")) | .id'`. Reuse the same id (PATCH, not new POST) — `consolidate/post.md` "Single Summary preservation guard" applies post-merge too.
  - **Forbidden**: leaving the Summary at its pre-merge state because "the PR is MERGED so the comment is read-only". A MERGED PR's comment body is still PATCH-able and the audit trail benefits from the merged-state record.
  - **Order vs Issue body checklist update (next bullet)**: Summary PATCH runs first (PR-scoped), then issue body checklist update (issue-scoped). Both run before `Deploy follow-up`.
- **Update related issue body checklists (HARD STOP)**: if the PR referenced an issue via `Relates to #N` / `Resolves #N` / `Fixes #N` / `Refs #N`, immediately after merge update that issue body's checklist (`- [ ]`) to `- [x]` for items covered by the PR scope, and append a reference to the merged PR number. Especially for **epic-style issues** (multiple Phase 1/2/3 checkboxes), batch-update every Phase item completed by the PR merge.
  - Update format: `- [x] item description (merged in PR #N)` or `- [x] item description — PR #N`
  - Search: `gh pr view <PR> --json body -q '.body' | grep -iE 'Resolves|Relates to|Closes|Fixes|Refs'` → extract referenced issues
  - **Cross-repo issues apply equally**: if the PR references another repository's issue, update that repository's issue body too (e.g. when an app-repo PR includes work tracked in the infra repo, update both issue bodies)
  - Consequence of skipping: the epic body stays stale; on the next planning pass, "already implemented items" appear unfinished and cause duplicate work / confusion
- **Deploy follow-up**: after merge, confirm with the user whether to run the related deploy workflow (infra automation, ArgoCD sync, etc.).
- **`gh pr merge` direct invocation is absolutely forbidden** — merging must always go through this skill (`/github-flow merge`). Trying to merge without surfacing the five conditions to the user is a procedural violation.
- **Post-hoc review for PRs merged without review** — run `/consolidate pr-review` for a post-hoc review, and if actionable items appear, ask via AskUserQuestion whether to register them in a follow-up PR or an existing issue.

## Recording evidence of merge-condition satisfaction (CRITICAL)

**When you add the PR entry to the "Completed" or "Merged / Closed" section of fix_plan.md right after merging, also record the evidence for all five conditions.**

A bare `✅` leaves no basis to verify "the conditions were really satisfied" after the fact. Format:

```markdown
### PR #N (branch-name) — ✅ MERGED YYYY-MM-DD
- CI: 4/4 SUCCESS (test ubuntu, test windows, e2e, CodeRabbit)
- AI Review: CodeRabbit ✅ addressed (3 actionable), Copilot ✅ addressed (1 comment)
- Test Plan: 5/5 checked
- Formal Review: APPROVED by @user (or "not required by repo policy")
```

**Forbidden pattern**: `### PR #N — ✅ MERGED YYYY-MM-DD` alone (no condition evidence)

**For post-hoc verifiability**: a post-hoc supervision flow (e.g., a Ralph wrapper's improve 5-A2 step, or the workflow.md supervision checklist Step 7) reads this information for verification. Without evidence, `✅`-only entries are classified as "merged without checking conditions" suspects during supervision.

## Merge-recommendation AskUserQuestion format (CRITICAL — HARD STOP)

**When recommending PR merge via AskUserQuestion, every option's description must include evidence for the five conditions.**

```typescript
{
  label: "PR #N squash merge",
  description: "CI: 4/4 ✅ | AI Review: CodeRabbit ✅ Copilot ✅ | Test Plan: 5/5 ✅ | Formal Review: APPROVED (or 'not required by repo policy')"
}
```

**Forbidden patterns (insufficient description)**:
- `"merge conditions satisfied"` (which conditions are unclear)
- `"CI passed"` (Test Plan, AI Review missing)
- A label with no description

**Verification procedure (HARD STOP)**:

Right before authoring the merge-recommendation AskUserQuestion, verify all five conditions:

```bash
# 1. CI status
gh pr checks <N> --json bucket -q '[.[] | .bucket] | group_by(.) | map({(.[0]): length}) | add'

# 2. AI Review Summary — count of 🔴 Critical (forbid merge if ≥ 1)
gh api repos/{owner}/{repo}/issues/<N>/comments \
  --jq '.[] | select(.body | startswith("## AI Review Summary")) | .body' \
  | grep -c '🔴 Critical' && echo "BLOCKED: Critical unresolved"

# 2b. AI Review actionable status
gh pr view <N> --json comments -q '.comments[] | select(.body | contains("actionable")) | .body' | head

# 3. Unchecked Test Plan items
gh pr view <N> --json body -q '.body' | node scripts/check-test-plan.js || echo "BLOCKED: Test Plan unchecked"

# 4. Formal Review (per repo policy)
gh pr view <N> --json reviews -q '[.reviews[] | select(.state == "APPROVED") | .author.login]'
```

**Any one of the four unsatisfied = the AskUserQuestion options must NOT include "merge"**. Offer "address <missing condition> then merge" instead.

## Merging requires explicit user instruction — no autonomous push (HARD STOP)

**"All Test Plan items [x]" = mergeable**, not "proceed with merge". Merging is a separate decision.

| # | Don't | Do |
|---|-------|-----|
| 1 | Verification complete → auto-check 4 merge conditions + present a merge option AskUserQuestion | Report verification complete and end. Enter the merge flow only when the user explicitly says "merge" |
| 2 | Treat "Test Plan all [x]" as a merge trigger | "Test Plan all [x]" is a verification-complete marker only. The merge decision belongs to the user |
| 3 | Auto-offer "AI Review Summary post" right after verification | Summary posting comes after the merge decision. Without merge intent, hold the Summary too |
| 4 | Auto-map "next unfinished item" = "merge or follow-up PR" | "Next unfinished item" is only an explicit fix_plan / TaskList entry. The merge is excluded unless explicitly listed |

**Self-check (every time after verification completes)**:
1. Did the user use the explicit words "merge" / "proceed with merge" / "ship it"? → If no, do NOT present a merge option
2. Verification work and merge work are separate. End with the verification-complete report
3. Including a merge option in the AskUserQuestion = rule violation (pressures the user into the merge decision)
