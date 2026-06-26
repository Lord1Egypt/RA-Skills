# PR Creation

Create PRs with structured body, test plan, and optional visual attachments.

## When to Use

- After code-workflow step 4 (implement) to create a PR
- When the user says "create PR", "PR with screenshots"
- After capture step (if visual evidence is needed)

## Options

- `--draft`: Create as Draft PR (`gh pr create --draft`)
- `--skip-review`: Skip CodeRabbit review (`--label coderabbit:ignore`)
- `--no-capture`: Skip visual attachment step
- Options can be combined: `/github-flow pr --draft --skip-review`

## Procedure

### Step 0: Visibility + language decision guard (HARD STOP — run every time, right before PR creation)

**Before writing the PR title and body, always check repository visibility and map the language.**

```bash
gh repo view <owner/repo> --json isPrivate -q '.isPrivate'
```

| `isPrivate` | PR title / body language | When violated |
|------------|--------------------------|---------------|
| `true` (PRIVATE) | **Korean default** | User has previously corrected: "use Korean for Korean-repo PRs" |
| `false` (PUBLIC) | **English required** | Personal-data exposure + rule violation |

| # | Don't | Do |
|---|-------|-----|
| 1 | Reuse the commit message language for the PR title | Decide the PR title language separately from the visibility result. Even if commits are English, a PRIVATE repo still gets a Korean PR title |
| 2 | Inferring "the body is Korean, so the title must also be Korean" | Apply the visibility rule explicitly to both the title and the body |
| 3 | Performing the visibility check only inside the personal-data sanitize step | Step 0: visibility check → language decision → then sanitize |

**Exception**: English only when the project's CLAUDE.md / README explicitly states "write PRs in English", or the user explicitly requests English. Choosing English by inference is forbidden.

Detailed rule: `~/.agents/rules/opensource.md` "PRIVATE repo = Korean default" section.

### Step 1: Pre-flight Checks

```bash
# Detect base branch
BASE=$(git merge-base HEAD master 2>/dev/null && echo master || echo main)

# Check gh CLI
gh --version 2>/dev/null || echo "gh not found"

# Check for existing open PR on this branch
gh pr list --head $(git branch --show-current) --state open
```

- If **gh CLI missing** → proceed with body template only (no creation)
- If **PR already exists** → report to user and stop

#### Step 1.5: GitHub Actions Workflow YAML Verification (HARD STOP — when `.github/workflows/*.yml` was edited)

After modifying or creating a workflow YAML, **verify locally before push**.

##### Permissions matrix verification

If the workflow declares a `permissions:` block, build a matrix of every action/API the jobs use and confirm no permission is missing.

| Action/API | Required permission |
|-----------|---------------------|
| `actions/checkout@v4` | `contents: read` |
| `docker/login-action@v3` + `build-push-action@v6` | `packages: write` |
| `dorny/paths-filter@v3` (PR mode) | `pull-requests: read` |
| `peter-evans/repository-dispatch@v3` | (uses PAT token, no permissions block needed) |
| `softprops/action-gh-release@v2` | `contents: write` |

| # | Don't | Do |
|---|-------|-----|
| 1 | Copy the source workflow's permissions block verbatim into a consolidated workflow | After consolidation, walk every job's actions and **union** the required permissions |
| 2 | Add a new action without updating permissions | Right after adding an action, check the matrix above → append the required permission |
| 3 | Run only `act-check` and then push | Use `act` to validate every executable job. Even lightweight jobs (e.g., `paths-filter`) should pass syntax verification under `act` |

##### `act` local verification

Run `make act-check` or `make act-ci` and confirm **all executable jobs pass** before pushing. Jobs that cannot run under `act` (Tailscale, Semaphore-only paths, etc.) must at least pass YAML syntax verification.

### Step 2: Gather Changes

```bash
git log --oneline origin/$BASE..HEAD   # commits to include
git diff --stat origin/$BASE           # changed files summary
```

### Step 3: Search Related Issues (gh CLI only)

Extract keywords from branch name and changed files, search for related issues:

```bash
gh issue list --limit 100 --state open --search "[keywords]"
```

Present 1-3 candidates via **AskUserQuestion** for confirmation.
If no issues found, skip this section.

### Step 4: Construct PR Body

If `.github/pull_request_template.md` exists, use that template. Otherwise use the default below.

```markdown
## Summary
<1-3 bullet points>

## Changes
| File | Change |
|------|--------|
| ... | ... |

## Related Issues
<!-- Relates to #number — Do NOT use "Closes #" or "Fixes #" to prevent auto-close -->

## Visual Changes (optional)
| Before | After |
|--------|-------|
| ![before](url) | ![after](url) |

## Test plan
- [ ] **[general]** Local build passes
- [ ] **[general]** No type errors
- [ ] **[general]** ...

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Checklist inclusion criteria** — only include items relevant to the change. Every item carries the `[general]` / `[UI]` / `[post-merge]` prefix per the "Test Plan category classification" HARD STOP below.

| Item | Prefix | Include when |
|------|--------|-------------|
| Local build passes | `[general]` | Always |
| No type errors | `[general]` | Always |
| Route/sidebar navigation works | `[UI]` | UI page add/change |
| Core feature works | `[general]` or `[UI]` | Functional changes |
| DB/API integration verified | `[general]` | DB/API changes |

For chore/docs/config changes, only build + type check items.

### Test Plan vs BLOCKED separation (HARD STOP)

**Test Plan = "items that validate the PR's essential change". When checked, they are used as a merge-readiness signal.** BLOCKED follow-up work, externally-dependent work, and items destined for a separate PR must NOT be included in the Test Plan.

| Item kind | PR body location |
|-----------|------------------|
| **PR essential validation** (build / type / feature / API / UI) | `## Test plan` section (`- [ ]` checklist) |
| **External-dependency follow-up** (other backend design, awaiting collaborator) | Separate `## Outstanding (BLOCKED)` or `## Follow-up` section |
| **Separate-PR scope** | Exclude from this PR's Test Plan → `fix_plan.md [BLOCKED] [REVIEW_FEEDBACK]` or a separate Issue |
| **Next-session work** | `fix_plan.md` hold section |

**Why separate?**
- merge.md HARD STOP: "Block merge if even one Test Plan `- [ ]` is unchecked"
- Leaving a BLOCKED item as `[ ]` in the Test Plan permanently blocks the merge because of work that cannot autonomously proceed
- A PR with a separate BLOCKED section is fine after Test Plan reaches 5/5 [x] (BLOCKED is tracked via a different medium)

| # | Don't | Do |
|---|-------|-----|
| 1 | Include a BLOCKED item such as `- [ ] hold infra apply` in the Test Plan | Test Plan = essential validation only. BLOCKED goes to a separate `## Outstanding` section or `fix_plan.md` |
| 2 | Mark an "awaiting external response" item as `[ ]` in the Test Plan | Remove it from the Test Plan → `fix_plan.md [BLOCKED]` or a separate Issue |
| 3 | Inline next-session work in the Test Plan | Put it in a separate `## Follow-up` section + sync with `fix_plan.md` |
| 4 | Tack "Outstanding" items at the end of the Test Plan | Split into a distinct header (`## Outstanding`, `## Follow-up`) |

**Self-check (right before writing the Test Plan)**:
1. Is this item **essential validation that must be done to merge** the PR?
2. Is there an external dependency (other-system design, collaborator response)? → Yes → separate section
3. Can it be handled in this session or within 1–2 days? → No → `fix_plan.md` or a separate Issue
4. Can every `[ ]` realistically become `[x]` by merge time? → No → move it out

### Test Plan category classification (HARD STOP)

**Test Plan essential-validation items must be classified with a category prefix.** Each category applies a different merge guard. Automatic verifications (pre-commit / CI / lint) are guaranteed by the workflow itself, so they must NOT be written into the Test Plan (duplication + extra burden on the user).

#### Category matrix

| Category | Prefix | Meaning | When validated | Merge guard |
|----------|--------|---------|----------------|-------------|
| **Automatic** | (none — excluded from Test Plan) | pre-commit hook / GitHub Actions / lint run automatically | At push time | Workflow itself (no Test Plan entry needed) |
| **General test** | `[general]` | Run local code / CLI / Make / scripts and check the result | Before merge | `[x]` required (merge.md HARD STOP) |
| **UI test** | `[UI]` | Browser scenario (Playwright / wmux browser / direct clicks) | Before merge | `[x]` required (merge.md HARD STOP) |
| **Post-merge test** | `[post-merge]` | Verification after deploy / CD trigger (production-environment behavior, integrated deploy result) | After merge | Does NOT block merge; must be registered in a tracking medium (issue / fix_plan) |

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Put a pre-commit/CI/lint item as `[ ]` in the Test Plan (e.g. "lint passes", "type check passes", "terraform fmt passes") | Exclude — the workflow guarantees it. No need to report it in the PR body either |
| 2 | List everything as a flat single list | Use category prefixes (`[general]` / `[UI]` / `[post-merge]`) so authors, reviewers, and the merge guard can see verification method / timing clearly |
| 3 | Force `[x]` verification of `[post-merge]` items before merge | `[post-merge]` does not block merge. Register a tracking record (issue or `fix_plan.md [BLOCKED]`) and proceed to merge |
| 4 | Mark an item `[post-merge]` without registering a tracking medium (post-merge verification gets lost) | `[post-merge]` items require `gh issue create` or `fix_plan` registration. Inline the tracking link in the item description |
| 5 | Omit the category prefix and only write notes | Prefix is required — both the merge.md guard automation and human triage classify by prefix matching |
| 6 | Wrap the category in backtick + bracket in the PR body (`` `[post-merge]` ``) — backtick renders an inline-code chip stacked on the brackets = redundant double-highlight | **PR-body output format = `**[category]**`** (bold + bracket, a single highlight): `**[general]**` / `**[UI]**` / `**[post-merge]**`. (Inline-code `[category]` references in *this doc's* prose/tables are fine — the rule applies only to the **PR body** the reader sees.) |

#### Test Plan example

```markdown
## Test Plan

- [ ] **[general]** `make plan ENV=dev-A` → backend switch confirmed + plan output 1 add / 2 change
- [ ] **[general]** `make plan ENV=integration` → environment switch confirmed
- [ ] **[UI]** Entry to service-A → `service-A-source-auto-redirect` flow exposed (Playwright)
- [ ] **[UI]** After service-B logout, entry to service-A re-exposes the service-B login screen (Playwright, regression guard for case C-1)
- [ ] **[post-merge]** After integration deploy, app logout → verify post-logout redirect (tracking: [#39-followup](url))
- [ ] **[post-merge]** Self-hosted runner picks up at least one workflow run (tracking: workflow_dispatch or next PR's CI)
```

#### Self-check (right before writing the Test Plan, every time)

1. Is the item run automatically by pre-commit / CI / lint? → Yes → exclude from Test Plan
2. Can the item be verified in this session before merge? → `[general]` or `[UI]`
3. Is the item a deploy / production-environment behavior verifiable only after merge? → `[post-merge]` + tracking-medium registration required
4. Does every `[ ]` have a category prefix? → Re-review any item missing one

### Step 5: Sanitize Internal Paths

Before posting, strip all internal paths per SKILL.md Core Rules:
- Internal workflow-generated doc paths (e.g., `.ralph/docs/`, `.omc/plans/`) → remove or inline the content
- Session IDs → remove
- Other internal working directories (`~/.claude/`, `~/.ralph/`, `~/.omc/`, etc.) → remove

### Step 6: Suggest Milestone

Before creating the PR, check for a milestone on the related issue:

```bash
# If related issue exists, inherit its milestone
gh issue view <ISSUE_NUMBER> --json milestone --jq '.milestone.title'
```

- **Issue has milestone** → apply the same milestone to the PR after creation (`gh pr edit <NUMBER> --milestone "<title>"`)
- **Issue has no milestone** → query open milestones and suggest via **AskUserQuestion**:
  ```bash
  gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.state=="open") | "\(.title)\t\(.description)"'
  ```
- **No related issue** → suggest milestone based on change scope (patch/minor/feature)

### Step 7: Review and Create PR

Show the drafted title and body to the user via **AskUserQuestion** for confirmation.

**With gh CLI:**

```bash
gh pr create \
  --title "..." \
  --body "$(cat <<'EOF'
...
EOF
)" \
  --base $BASE \
  --head $(git branch --show-current) \
  --label [label] \
  --milestone "<milestone>" \
  --add-assignee @me
```

- `--draft` option → add `--draft` flag
- `--skip-review` option → add `--label coderabbit:ignore` (in addition to classification label)
- **At least 1 classification label required**: enhancement, bug, documentation, test, chore, etc.
- **Milestone from Step 6** → add `--milestone "<title>"` flag

Report the PR URL after creation.

**Without gh CLI:** output the body in a code block for manual use.

### Step 8: Attach Visual Evidence

**UI-change PRs — MANDATORY (HARD STOP)**. Non-UI PRs — optional.

#### UI-change PR detection (HARD STOP)

If any of the following applies, the PR is a UI-change PR — capture attachment is required:

| Changed-file pattern | Verdict |
|----------------------|---------|
| `*.tsx`, `*.jsx`, `*.svelte`, `*.vue` (component code) | UI change |
| `*.css`, `*.scss`, `*.module.css`, Tailwind class add / change | UI change |
| Screen-entry directories such as `app/`, `pages/`, `routes/` | UI change |
| API route only (no UI change) | Non-UI |
| Rules / docs / CI / config | Non-UI |

#### Capture count guidance

- **At least 1**: one shot of the main screen (after)
- **One per Test Plan item recommended**: one screen per verification item
- **Before / after pair**: when modifying an existing UI (visual comparison needed)
- **GIF / MP4**: for interaction changes (hover, animation, drag, modal open, etc.)

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Create a UI-change PR without captures | Attach at least one capture in the PR body or a comment |
| 2 | Skip captures with the rationale "the reviewer can check it themselves" | The author attaches captures — removing the reviewer's burden of going from code → browser to verify |
| 3 | Capture automation (web-browser / Playwright) is available, but skipped due to "manual effort" | Use `Skill("web-browser")` or `wmux browser screenshot` |
| 4 | Use `--no-capture` opt-out by default | `--no-capture` is forbidden on UI-change PRs. Allowed only on non-UI PRs |

#### Attachment method

| Method | When |
|--------|------|
| GitHub image upload (preferred) | PR-only visual evidence — drag-drop into the body or a comment, or `![](URL)` |
| `.github/assets/` directory | Permanent documentation (when a live demo or README reference is needed) |

**Do not commit screenshots** unless they serve as permanent docs.

### Image Format Priority

| Format | Use Case |
|--------|----------|
| WebP | Static screenshots (smallest, GitHub supported) |
| PNG | When WebP unavailable or transparency needed |
| GIF | Short animations, hover effects |
| MP4/WebM | Complex interactions |

### Capture Naming

```text
.github/assets/<issue-number>-<description>-before.webp
.github/assets/<issue-number>-<description>-after.webp
```

### Step 9: Schedule Consolidate Follow-up (MANDATORY)

Right after PR creation, **do not stop there** — explicitly handle the follow-up for AI review consolidation (CodeRabbit / Copilot). Leaving a gap between PR creation and consolidate causes the flow to end at "review pending" with no further action.

#### 0. Copilot reviewer handling (HARD STOP — automated step)

**Handle the Copilot reviewer first, right after PR creation.** The `next.md` "After PR creation" matrix only triggers via the turn-end stop hook, so any work between PR creation and turn end will skip it. Therefore handle it **automatically in this step**, immediately after PR creation.

**Identifier caveat (HARD STOP — corrected 2026-05-24)**: the Copilot bot identifier differs by usage. The login used for registration is not the same as the login used for verification:

| Usage | Identifier | Notes |
|-------|-----------|-------|
| `gh pr edit --add-reviewer <login>` | **`copilot-pull-request-reviewer`** | Works. Generates a `review_requested` event in the timeline (PR #13 verified) |
| `gh pr edit --add-reviewer Copilot` / `copilot[bot]` | Fails with "Could not resolve user with login" | gh CLI requires the exact bot login |
| REST `POST .../requested_reviewers -F "reviewers[]=copilot[bot]"` | 200 + empty `requested_reviewers` response (silent fail) | Bot users cannot be added via the regular reviewers array |
| REST `reviewers[]=Copilot` (capitalized) | silent fail (200 + empty response) | Same |
| GraphQL `requestReviews(input: { userIds: [bot_node_id] })` | "Could not resolve to User node with the global id of '...'" | GraphQL cannot resolve a Bot ID as a User |
| Timeline `review_requested` event's `requested_reviewer.login` | `Copilot` (capitalized, type=Bot, node_id=`BOT_...`) | Primary source for registration confirmation |
| `reviews[].author.login` (auto-review after registration) | `copilot-pull-request-reviewer` | Auto-review appears 5 sec to tens of sec later |
| `pullRequest.reviewRequests` GraphQL field | **empty array** (Bot reviewers not exposed) | Known GraphQL limitation. Do NOT trust for Bot registration confirmation — use timeline or reviews |

**Key conclusions**:
- **Primary registration method: `gh pr edit --add-reviewer copilot-pull-request-reviewer`** (silent success, timeline event is generated)
- **For confirmation, use timeline `review_requested` events or `reviews(author=copilot-pull-request-reviewer)` — not `reviewRequests`**
- `gh search prs --review-requested <id>` only supports Users — for in-progress searches use GraphQL `viewer.pullRequests` + `reviewRequests` (Bot filter), or the `reviews` matrix, or map REST `/issues/{N}/timeline` `review_requested` events

**Procedure**:

```bash
# Step 0-1: Pre-check whether this PR has already had Copilot registered as a reviewer
# - reviewRequests does not expose Bots → check the timeline review_requested event
# - reviews(author=copilot-pull-request-reviewer) appears after the auto-review arrives
TIMELINE_HAS_COPILOT=$(gh api repos/<owner>/<repo>/issues/<N>/timeline --jq '[.[] | select(.event=="review_requested" and .requested_reviewer.login=="Copilot")] | length')
REVIEW_HAS_COPILOT=$(gh pr view <N> -R <repo> --json reviews --jq '[.reviews[] | select(.author.login=="copilot-pull-request-reviewer")] | length')
if [[ "$TIMELINE_HAS_COPILOT" -gt 0 || "$REVIEW_HAS_COPILOT" -gt 0 ]]; then echo SKIP; else echo PROCEED; fi
```

`PROCEED` → continue to Step 0-2. `SKIP` → already registered / reviewed.

```bash
# Step 0-2: Search across the account for open PRs with Copilot review_requested in flight
# Iterate open PRs you are author/assignee/reviewer on, and look for a review_requested(Copilot) event in the timeline
gh api graphql -f query='
query {
  viewer {
    pullRequests(states: OPEN, first: 50, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        number
        title
        url
        repository { nameWithOwner }
        reviewRequests(first: 10) {
          nodes { requestedReviewer { __typename ... on Bot { login } } }
        }
        reviews(first: 50) {
          nodes { author { login } }
        }
      }
    }
  }
}' \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
prs=d.get('data',{}).get('viewer',{}).get('pullRequests',{}).get('nodes',[])
pending=[]
for pr in prs:
    req=any(r.get('requestedReviewer',{}).get('login')=='Copilot' for r in pr.get('reviewRequests',{}).get('nodes',[]) if r.get('requestedReviewer',{}).get('__typename')=='Bot')
    rev=any(r.get('author',{}).get('login')=='copilot-pull-request-reviewer' for r in pr.get('reviews',{}).get('nodes',[]))
    if req and not rev:
        pending.append((pr['repository']['nameWithOwner'], pr['number'], pr['url']))
print('pending:', pending)
print('count:', len(pending))
"
```

Copilot has a limited concurrent-review queue, so **if reviews are already in flight, new requests pile up in the backlog**. Requesting a new PR while reviews are in flight may delay walkthrough arrival indefinitely or drop it silently.

| Search result (count) | Action |
|-----------------------|--------|
| 0 (none in flight) | Register immediately (Step 0-3 below) |
| 1–2 (small backlog) | Ask the user via AskUserQuestion: "N Copilot reviews in flight — request this PR now / request after the in-flight ones complete / skip Copilot" |
| 3+ (large backlog) | TaskCreate "Register Copilot reviewer for PR #N (after the N in-flight ones drain)" + BLOCKED. Also record in `fix_plan.md` hold section |
| This PR already registered (Step 0-1 SKIP) | skip |

```bash
# Step 0-3: Register Copilot reviewer (gh pr edit — use the copilot-pull-request-reviewer login)
gh pr edit <N> -R <owner>/<repo> --add-reviewer copilot-pull-request-reviewer
# Verification 1 (immediate): confirm a review_requested event appears in the timeline
gh api repos/<owner>/<repo>/issues/<N>/timeline --jq '[.[] | select(.event=="review_requested") | {requested_user: .requested_reviewer.login}]'
# Verification 2 (~5 sec to tens of sec later): confirm copilot-pull-request-reviewer appears in reviews (auto-review)
gh pr view <N> -R <owner>/<repo> --json reviews \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print([r.get('author',{}).get('login') for r in d.get('reviews',[])])"
# Note: pullRequest.reviewRequests GraphQL field does not expose Bot reviewers — do not use it to confirm registration
```

#### Step 0-4: Detect rate-limit failure after registration (HARD STOP)

Registration silent-success and a review body posted by `copilot-pull-request-reviewer` are NOT sufficient evidence that Copilot reviewed the PR. The auto-triggered Action run can fail with `429 rate_limit` while still leaving a placeholder review on the PR ("Copilot encountered an error and was unable to review this pull request"). Treat that placeholder as a failure, extract the reset time, and hold further Copilot ops until the reset.

```bash
# 1. Locate the auto-triggered "Running Copilot Code Review" run on this branch (most recent)
RUN_ID=$(gh run list -R <owner>/<repo> --branch <head-branch> \
  --workflow "Running Copilot Code Review" --limit 1 \
  --json databaseId,status,conclusion --jq '.[0].databaseId')

# 2. Inspect conclusion. failure -> rate-limit suspect.
gh run view "$RUN_ID" -R <owner>/<repo> --json conclusion --jq '.conclusion'

# 3. On failure, scan logs for the canonical message and pull the reset window.
gh run view "$RUN_ID" -R <owner>/<repo> --log 2>&1 \
  | grep -oE "Please wait for your limit to reset in [0-9]+ hours? [0-9]+ minutes?" \
  | head -1

# 4. Cross-check via review body — placeholder string is the user-visible failure mode.
gh pr view <N> -R <owner>/<repo> --json reviews --jq \
  '.reviews[] | select(.author.login=="copilot-pull-request-reviewer")
   | {state, isPlaceholder: (.body | contains("encountered an error and was unable to review"))}'
```

| Signal combination | Interpretation | Required action |
|---|---|---|
| Run conclusion `success` + review body has actionable content | Real review posted | Proceed to Step 1 (CodeRabbit walkthrough) |
| Run conclusion `failure` + log matches `reset in N hours M minutes` | **Weekly rate limit hit** | Compute reset timestamp (run failure time + N hours M minutes), see "Hold procedure" below |
| Run conclusion `failure` + log has no rate-limit phrase | Other Copilot failure (network / config / permissions) | Report run URL to the user via AskUserQuestion; do NOT retry blindly |
| Review body == placeholder + run not found | API consistency lag — re-run Step 0-4 after 10s | If still missing, treat as failure |

##### Hold procedure when rate-limit detected

1. Compute reset timestamp: take the run's `createdAt` (or the failing log line's timestamp), add the parsed `N hours M minutes`, in UTC. **Immediately write this reset time to the shared global cache file `~/.claude/copilot-rate-limit.json`** in the format `{"reset_at": "ISO_TIMESTAMP_IN_UTC"}` (e.g. `{"reset_at": "2026-05-31T08:08:29Z"}`) to share the rate limit status across all sessions.
2. Do **not** re-register Copilot reviewer. The bot self-removes from `requested_reviewers` after the failed attempt, so no manual removal needed.
3. Update the consolidate follow-up task with the reset time so the next session can act on the deadline:
   ```text
   TaskUpdate <consolidate-task-id> description:
     "PR #<N> — Copilot rate-limit until <ISO timestamp>.
      After reset, re-run Step 0 (Copilot reviewer) then proceed to Step 1."
   ```
4. If the reset is more than 60 minutes out, register it in `fix_plan.md` `## Hold` section (workflow.md medium separation). Less than 60 minutes: `ScheduleWakeup` with a delay near the reset (use the cache-window guidance — pick 270s if reset is under 5 minutes, else round up to 1200s+).
5. Report to the user with one line: run URL + reset time + chosen hold medium.

##### Don't / Do (Step 0-4)

| # | Don't | Do |
|---|-------|-----|
| 1 | Treat `reviews[].author.login == "copilot-pull-request-reviewer"` count as proof Copilot reviewed | Inspect `body` for the placeholder string; cross-check the run conclusion |
| 2 | Re-register Copilot after the placeholder appears | Bot self-removes from `requested_reviewers` after the failed run. Re-registering inside the rate-limit window triggers another `429` immediately |
| 3 | Skip log parsing because "the API didn't return a structured error" | `gh run view --log` is the canonical surface for the reset-window string. Without parsing it, the deadline is lost |
| 4 | Proceed to Step 1 (CodeRabbit) on a rate-limited Copilot run | Step 1 still runs (CodeRabbit and Copilot are independent), but consolidate must wait — record the Copilot deadline in the consolidate task before moving on |
| 5 | Report "Copilot review pending" without the reset timestamp | Always cite the reset timestamp + the run URL the user can click |

##### Self-check (every time after Step 0-3 registration)

1. Did the Action run for "Running Copilot Code Review" complete on this branch? If the status is still `in_progress` after 30s, wait another 30s before deciding.
2. Is the conclusion `failure`? Pull the log and grep the reset phrase.
3. Is the review body the placeholder string? Same as conclusion=failure path.
4. Recorded the reset timestamp on the consolidate task? Confirm before reporting "registration done".

##### Violation case (run conclusion=failure missed by presence-only check)

A PR registered the Copilot reviewer via `gh pr edit --add-reviewer copilot-pull-request-reviewer`. `requested_reviewers` and `reviews[].author.login` were inspected and "registered + reviewed" was reported. The auto-triggered "Running Copilot Code Review" Action run actually completed with conclusion `failure`; its log contained `Please wait for your limit to reset in N hours M minutes` and the review body was the placeholder string. The failure was missed entirely until the user supplied the run URL. Root cause: Step 0-3 verification stopped at presence checks (login + body posted) without inspecting the run conclusion or the body content. This Step 0-4 was added to close that gap.

**Don't / Do table**:

| # | Don't | Do |
|---|-------|-----|
| 1 | Skip the Copilot-reviewer step after PR creation and only check the CodeRabbit walkthrough | Step 0 first → handle Copilot → then Step 1 CodeRabbit walkthrough |
| 2 | Register Copilot reviewer unconditionally, without checking account-wide in-flight state | Run Step 0-2 GraphQL `viewer.pullRequests` + `reviewRequests` matrix first — if backlogged, drain the backlog first |
| 3 | Delegate Copilot handling to the consolidate skill (trusting only the next.md matrix) | The next.md matrix triggers via the stop hook — easy to miss. Handle it automatically in pr.md Step 9 |
| 4 | Stay silent after detecting a Copilot backlog | TaskCreate + fix_plan hold + AskUserQuestion for the user to decide |
| 5 | Skip in-flight checks because "I already checked once" during silent-fail / retry | **Re-run the Step 0-2 in-flight check every time Copilot registration is attempted.** Do not trust cached results — between checks, Copilot may have been registered on another PR |
| 6 | When an AskUserQuestion option mentions "re-register Copilot then consolidate", omit the in-flight check from the description | Spell out the **"in-flight check → 0 → register → 1+ → backlog notice"** procedure inline in the option description. Promise that it will re-run at fire time |
| 7 | After one passing in-flight check, auto-generate a registration option without checking again | **Re-run Step 0-2 every time AskUserQuestion options are authored.** Check again at the action step after firing (double guard) |

**Self-check (right after PR creation + every Copilot registration attempt)**:
1. Step 0-1: `gh pr view <N> --json reviewRequests,reviews` to check whether Copilot is already registered for this PR — SKIP if `Copilot` (Bot) is in reviewRequests OR `copilot-pull-request-reviewer` is in reviews
2. Step 0-2: on PROCEED, search for in-flight Copilot reviews via the GraphQL `viewer.pullRequests` matrix
3. Branch by count using the table above
4. Step 0-3: when 0, register via `gh pr edit <N> --add-reviewer copilot-pull-request-reviewer` + 5s wait + reviews verification
5. **State the Copilot-handling outcome in the report before moving on to Step 1 (CodeRabbit walkthrough)**
6. **On retry / silent-fail recovery**: **re-run** Step 0-1 + Step 0-2 (do not trust earlier results)
7. **When AskUserQuestion options include a Copilot-registration option**: inline the "in-flight check → branch by result" procedure in the description + re-check at fire time

#### In-flight check obligation on Copilot retry / silent-fail / option authoring (HARD STOP)

**A Copilot-reviewer registration attempt is not a one-shot event.** The same procedure (Step 0-1 + Step 0-2 + branch-by-result) is required at every one of the following moments:

| Moment | In-flight check required? | Why |
|--------|---------------------------|-----|
| Right after PR creation (entering Step 9-0) | Yes | Determines whether Copilot can be registered on the new PR |
| Silent-fail recovery (POST 200 + empty `requested_reviewers`) | Yes | Between retries, another PR may have grabbed Copilot |
| Alternative registration attempt (GitHub UI, GraphQL `requestReviews` mutation, etc.) | Yes | Different timing → different in-flight state |
| Authoring an AskUserQuestion option that includes "register Copilot" | Yes | The user's fire moment can lag by minutes |
| Right before actually registering, after an option has fired | Yes | Time elapses between option-fire and registration — new in-flight requests may appear |

**Self-check procedure**:
1. If any of "Copilot registration / retry / option inclusion" applies, re-run Step 0-2
2. Reflect the re-run result in the option description (e.g. "0 in-flight confirmed — can register immediately")
3. Re-run Step 0-2 **once more** right before actually registering, after the option fires (double guard)
4. If the result has changed (e.g. 0 → 1+), abort registration and report back to the user

**1. Check whether the CodeRabbit walkthrough has been posted** (~30 seconds after PR creation):

```bash
gh pr view <N> -R <repo> --json comments --jq '[.comments[] | select(.author.login=="coderabbitai") | .body] | .[0]'
```

Check the result for one of the following patterns:

| Result | Next action |
|--------|-------------|
| Walkthrough / Summary by CodeRabbit body (posting complete) | `/consolidate pr-review <N>` **invoked immediately** |
| `Rate limit exceeded` / `wait N minutes` / `Refill in N minutes M seconds` | **Compute the absolute reset timestamp** (procedure below). If reset has not passed: TaskCreate + ScheduleWakeup. If reset has passed: post `@coderabbitai review` as a PR comment (with user approval) to trigger a fresh walkthrough |
| No comment yet (immediately after creation, pending) | Wait another 30 seconds and re-check; if still missing, register a task |
| `coderabbit:ignore` label applied | Skip consolidate — proceed with Internal Code Review only (`superpowers:code-reviewer` or `coderabbit:code-review` direct invocation) |

#### CodeRabbit rate-limit body — absolute reset timestamp procedure (HARD STOP)

The walkthrough body's "Refill in N minutes M seconds" / "wait N minutes" notice is **static at posting time**. The body itself never updates as time passes. Quoting that notice verbatim on every check is a violation. Convert "body posting time + remaining notice" into an **absolute reset timestamp** and compare against the current time.

##### Procedure

1. **Read body posting time**: `gh api repos/<owner>/<repo>/issues/<N>/comments --jq '.[] | select(.user.login=="coderabbitai[bot]") | {created_at, body_first200: (.body[:200])}'`
2. **Parse remaining duration**: extract "N minutes M seconds" / "wait N minutes" from the body
3. **Compute absolute reset**: `created_at` (UTC ISO 8601) + the remaining duration = reset timestamp (UTC)
4. **Compare with current time**: `date -u +%Y-%m-%dT%H:%M:%SZ` versus the reset timestamp
   - **Now >= reset**: refill complete. Post `gh pr comment <N> -R <owner>/<repo> --body "@coderabbitai review"` to trigger a fresh walkthrough (only after explicit user approval)
   - **Now < reset**: actual remaining = reset - now. Register `ScheduleWakeup(delaySeconds=remaining + 60)` or a follow-up task and wait

##### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Quote the body's "N minutes M seconds" notice verbatim on each follow-up | Compute absolute reset = body `created_at` + remaining notice → compare against the current time |
| 2 | Conclude "rate-limited" just because the body is still present | The body is a static snapshot. Use the timestamp arithmetic only — "still posted" does not mean "still rate-limited" |
| 3 | After a wakeup fires, requote the same body notice without re-computing | Wakeup fired = a new now-timestamp. Recompute reset vs now every time |
| 4 | Post `@coderabbitai review` before reset has passed | Posting inside the window triggers another rate-limit failure. Only post once reset has clearly passed |
| 5 | Estimate "tens of minutes have passed, must be refilled" without arithmetic | Reset passage is decided only by explicit comparison: `date -u` against the computed reset timestamp |

##### Self-check (every time a rate-limit body is encountered)

1. Did you read body `created_at`?
2. Did you parse the remaining minutes/seconds from the body?
3. Did you compute absolute reset = created_at + remaining?
4. Did you compare against the current time (`date -u`)?
5. When reporting to the user, did you say "reset @<timestamp> UTC — remaining Y minutes as of now" instead of quoting the body's static "X minutes M seconds"?

##### Violation case (reset countdown quoted verbatim past expiry)

A walkthrough body advertised a rate-limit reset as "N minutes M seconds remaining" at body-publication time. By the time consolidate re-checked, the absolute reset (`created_at + remaining`) had already passed, yet the prior response quoted the body's static "N minutes M seconds" verbatim and reported "about X minutes remaining after the wakeup." User correction: the time had already passed. Fix: every report MUST recompute `absolute_reset - now()` against the current `date -u`, never the static body string.

**2. No automatic trigger between PR and consolidate — registration is mandatory**:

PR creation is stateless. There is no automation that detects review arrival. So at PR-creation time you **must** do exactly one of: task registration, or immediate invocation. Reporting and stopping = procedural violation.

| # | Don't | Do |
|---|-------|-----|
| 1 | Report "waiting on CodeRabbit review" and stop | Confirm walkthrough posting → invoke consolidate immediately or register a task |
| 2 | Stay silent after detecting a rate limit | TaskCreate for the follow-up — task subject must include the PR number + "consolidate after CodeRabbit arrives" |
| 3 | Bulk-report "review pending" for multiple PRs at once | Check walkthrough status per PR — one PR may have arrived while another is rate-limited |
| 4 | Skip consolidate and present merge options via the next-action AskUserQuestion | Run consolidate first (Internal Review + AI Review Summary posting) → then the next action |

**3. Consolidate-invocation timing decision table**:

| PR state | When | How to invoke |
|----------|------|---------------|
| Walkthrough posted | Immediately (same session as PR creation) | `/consolidate pr-review <N>` directly |
| Rate limited (wait time stated) | At the stated time + 1 minute | Register a task + invoke when the time arrives |
| Reviewer not registered (e.g. Copilot not set up) | Handled in consolidate Step 1 | Invoke immediately — consolidate branches the fallback |
| `coderabbit:ignore` label | No walkthrough — Internal Review only | `superpowers:code-reviewer` or `coderabbit:code-review` directly |

## Rules

- **`Closes #` / `Fixes #` keyword forbidden** — use `Relates to #` to prevent auto-close of linked issues
- **At least 1 classification label** required on every PR
- **Sanitize internal paths** before posting (Step 5)
- **Step 9 mandatory** — after PR creation, either register a consolidate follow-up task or invoke it immediately. Reporting and stopping is forbidden.

## PR Creation Explicit Authorization (HARD STOP)

**PR creation after implement is a separate decision point.** Do not chain push and PR creation as a single flow. PRs are permanently recorded on GitHub; closing them leaves "history garbage" so recovery cost is high.

| # | Don't | Do |
|---|-------|-----|
| 1 | "Start implementation" option selected → implement + commit + push + `gh pr create` auto-chain | "Start implementation" = implement + commit only. push/PR requires separate explicit instruction |
| 2 | Plan says "submit Phase 1 as PR" → interpret plan approval as PR creation approval | Plan is a procedure spec. Each publish point requires explicit user instruction |
| 3 | code-workflow Step 4 (implement) → auto-trigger github-flow/pr | After implement completion, report → wait for user "create PR" instruction |
| 4 | Just before `gh pr create`, ask AskUserQuestion "title/body OK as is?" and proceed | Ask "Should I create the PR?" first — title/body confirmation comes after |
| 5 | AskUserQuestion option description does not mention PR creation, but PR is created anyway | Publish actions not explicitly stated in option description require separate ask |
| 6 | **Open PR(s) already in flight, but a new axis (new branch + push + PR) is added as an option, imposing simultaneous-handling burden** | **Before composing options, run `gh pr list --state open` as primary source. If 1+ open PRs exist, ask "handle existing PR first vs start new axis" as a separate question first** — including the new axis in option description is itself a burden |
| 7 | "User selected option whose description mentions 'PR creation', so OK" — ignoring other in-flight PRs | Option description coverage is the single-PR-context rule (#5). Adding a multi-PR axis is a separate decision point **before options are even presented**. Option description inclusion ≠ multi-PR axis agreement |

**Self-check (every time before `gh pr create` / new branch push)**:
1. Did the user **explicitly** say "create PR", "register PR", "open PR", etc.?
2. Or does the AskUserQuestion option description selected by the user **explicitly** mention PR creation?
3. **Confirm via `gh pr list --state open` as primary source** — is there 1+ open PR in flight?
   - **If yes**: regardless of #2 passing, axis split is required. "Handle existing PR (#N) first vs start new axis" must be asked separately. Option description must mark "existing PR in flight" + indicate this is a separate axis
   - **If no**: passing #2 alone is OK
4. If neither holds, or axis was not split → block `gh pr create` / new branch push

**Why multi-PR axis split?**:
- 2+ concurrent PRs = N× user burden for review/merge/CI monitoring decisions
- Even if option description mentions "PR creation", the user may intend "existing PR must be processed first" — the option itself was composed wrong
- 1+ in-flight PR = signal that user is focused on processing that PR. Adding a new axis disrupts the work flow

Violation case history: see `~/.claude/skills/cleanup/data/failed-attempts.md` "PR creation explicit authorization" entries (2026-05-16 + 2026-06-05 recurrences).
