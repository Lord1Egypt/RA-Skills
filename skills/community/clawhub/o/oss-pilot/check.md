---
name: oss-check
description: Morning check-in for pending PRs on any open-source repo. Reads repo
  profile, checks CI/bot/stale status, takes action. Triggers on "oss check",
  "check PRs", "morning check", "PR status", "openclaw check".
user_invocable: true
---

# OSS PR Check-In Skill

Check all pending PRs and handle everything that needs attention. Works on any repo with a profile at `./oss-pilot-data/profiles/<repo-name>.md`.

## Invocation

- `oss-check` -- check all repos with profiles that have active context files
- `oss-check <repo>` -- check a specific repo (e.g., `oss-check openclaw`)

## Step 0: Load Profile

Read the profile from `./oss-pilot-data/profiles/<repo>.md` (schema: see `./oss-pilot-data/profiles/_template.md`) to get:
- `repo` -- owner/repo (e.g., `openclaw/openclaw`)
- `fork` -- our fork (e.g., `Cypherm/openclaw`)
- `username` -- our GitHub username
- `local_path` -- local clone path

If no repo specified, scan `./oss-pilot-data/context/` for context files and infer repos from them.

## Step 1: Load Active PRs

```bash
ls ./oss-pilot-data/context/
```

Read each `pr-*.md` context file. Also check for PRs not in context files:
```bash
gh pr list -R <REPO> --author <USERNAME> --state open --json number,title
```

## Step 2: For Each PR, Check Status

```bash
# CI -- count fails and pending
FAILS=$(gh pr checks <NUMBER> -R <REPO> 2>&1 | grep -c "fail")
PENDING=$(gh pr checks <NUMBER> -R <REPO> 2>&1 | grep -c "pending")

# Unanswered bot comments -- bot root comments with no reply from us
gh api repos/<REPO>/pulls/<NUMBER>/comments --jq '
  [.[] | select(.user.login != "<USERNAME>" and .in_reply_to_id == null) | .id] as $bot_roots |
  [.[] | select(.user.login == "<USERNAME>" and .in_reply_to_id != null) | .in_reply_to_id] as $replied |
  [$bot_roots[] | select(. as $r | $replied | index($r) | not)] | length
'

# Human reviews -- fetch details, not just count (compare with context file Decisions to spot new ones)
gh pr view <NUMBER> -R <REPO> --json reviews --jq '[.reviews[] | select(.author.login != "<USERNAME>" and (.author.login | test("bot"; "i") | not))] | group_by(.author.login) | map({author: .[0].author.login, latest_state: (sort_by(.submittedAt) | last.state), count: length, latest_body: (sort_by(.submittedAt) | last.body[:200])})'

# PR state
gh pr view <NUMBER> -R <REPO> --json state --jq .state

# Stale check -- ping timestamp with no human response after it
gh api repos/<REPO>/issues/<NUMBER>/comments --jq '
  ([.[] | select(.user.login == "<USERNAME>" and (.body | test("^@")))] | last.created_at // empty) as $ping |
  if $ping == "" then "not_pinged"
  else
    ([.[] | select(.created_at > $ping and .user.login != "<USERNAME>" and (.user.login | test("bot"; "i") | not))] | length) as $responses |
    if $responses > 0 then "responded"
    else $ping
    end
  end
'

# Maintainer engagement -- check BOTH the linked issue AND the PR itself
ISSUE=$(grep -oE 'issue: [0-9]+' <CONTEXT_FILE> | grep -oE '[0-9]+')

# 1. Issue-level: maintainer comments + metadata
gh api repos/<REPO>/issues/$ISSUE --jq '{
  author_association: .author_association,
  assignee: (.assignee.login // "none"),
  labels: [.labels[].name],
  milestone: (.milestone.title // "none")
}'
gh api repos/<REPO>/issues/$ISSUE/comments --jq '[.[] | select(.author_association == "MEMBER" or .author_association == "COLLABORATOR" or .author_association == "OWNER")] | length'

# 2. Issue-level: who applied the labels? (auto-applied by reporter/bot != maintainer triage)
gh api repos/<REPO>/issues/$ISSUE/events --jq '.[] | select(.event == "labeled") | {label: .label.name, actor: .actor.login, association: .actor.author_association}' 2>/dev/null

# 3. PR-level: maintainer mentioned/subscribed (they SAW the ping even if they didn't reply)
gh api repos/<REPO>/issues/<NUMBER>/timeline --jq '[.[] | select((.event == "mentioned" or .event == "subscribed") and .actor.login != "<USERNAME>")] | [.[] | {actor: .actor.login, event: .event}] | unique_by(.actor)'

# 4. PR-level: cross-references -- WHO cross-referenced us and are they a maintainer?
#    Domain maintainers may not have MEMBER association but still control an area.
#    Check: cross-reference source PR/issue labels for "maintainer" tag, and actor's profile.
gh api repos/<REPO>/issues/<NUMBER>/timeline --jq '[.[] | select(.event == "cross-referenced")] | .[] | {actor: .actor.login, source_number: .source.issue.number, source_title: .source.issue.title[:80]}' 2>/dev/null
#    For each cross-reference actor, check if they're a known maintainer in the profile
#    or if their source PR/issue has a "maintainer" label.
#    A domain maintainer tracking your PR = [yellow] signal (they're aware, may review)

# Competing PRs -- always run, only report if found
gh pr list -R <REPO> --search "<ISSUE>" --state open --json number,author --jq '[.[] | select(.author.login != "<USERNAME>")] | .[] | {number, author: .author.login}'

# Linked issue state -- always run, flag if closed (supersession check)
gh api repos/<REPO>/issues/<ISSUE> --jq '{state: .state, closed_at: .closed_at[:16]}'
```

**CI rules:** [pass] = 0 fail + 0 pending. [fail] = any fail. [pending] = 0 fail + some pending. [locked] = all jobs skipping (fork PR -- needs maintainer to trigger CI, this is normal, not a failure).

**Merge rules:** Only show in report when actionable. `MERGEABLE` = [pass] (omit from report). `CONFLICTING` = flag for rebase. `UNKNOWN` = verify before dismissing:
```bash
# When UNKNOWN, check if the branch can actually merge by inspecting the diff against main
gh pr view <NUMBER> -R <REPO> --json baseRefName,headRefOid --jq '{base: .baseRefName, head: .headRefOid}'
# Re-query mergeable up to 2 times (GitHub often resolves UNKNOWN within seconds)
sleep 3 && gh pr view <NUMBER> -R <REPO> --json mergeable --jq .mergeable
```
If still `UNKNOWN` after retry, report as "! mergeable unknown -- verify manually" rather than silently omitting. Multiple PRs all showing `UNKNOWN` simultaneously is unusual and worth flagging.

**Bot rules:** [pass] = 0 unanswered. [fail] = any unanswered --> auto-respond before reporting.

**Cross-reference rules:**
- Filter bot noise before acting. Only count as genuine merge signal if: (a) author is a real user who hit the bug, or (b) maintainer opened/triaged it
- Still add `Closes #XXXX` for bot-opened duplicates (same bug), but don't inflate urgency claims
- Report honestly: e.g., "+2 cross-refs (1 real user, 1 bot duplicate)"

## Step 3: Triage and Act

| State | Action |
|---|---|
| **MERGED** | Celebrate. Run retrospective (Step 3.5). Archive context file. |
| **CLOSED** | Check why. Run retrospective (Step 3.5). Archive context file. |
| **New human review** | Compare Step 2 review details with context file Decisions section. Reviews whose author+state are not already noted in Decisions = new. Report to user with author, state, and body snippet -- needs human judgment. After addressing feedback, run `/oss-pr review` to verify quality before pushing. |
| **Unanswered bot comments** | Auto-respond using context file for approach details |
| **CI fail (our code)** | Read failure, fix, push |
| **CI fail -- needs triage** | Not all red CI means "wait." Triage the failures into 3 buckets (see CI Triage below). |
| **CI green + bots answered + no human review + not pinged** | Find who to ping: CODEOWNERS first, else `git log --since="30 days ago" --format="%an" -- <changed-files>` top result |
| **Stale (<72h since ping, no response)** | Wait. Don't enrich, don't follow up -- any PR activity generates notifications and bothers the maintainer. |
| **Stale (>72h since ping, no response)** | Diagnose WHY (see Stale Diagnosis below). Report diagnosis + merge prospect. Do NOT re-ping -- let user decide. |
| **Everything done, waiting** | Report "waiting for review" |

### Stale Diagnosis (replacing blind re-ping)

When a PR is stale >72h, don't just re-ping. First understand **why** it's stale using the maintainer engagement data from Step 2:

| Diagnosis | Evidence | Action |
|---|---|---|
| **Maintainer engaged with issue but not PR** | Maintainer commented/labeled the issue, but hasn't reviewed the PR | [yellow] Merge prospect: moderate. They know the problem -- just haven't reached the PR yet. |
| **Maintainer saw our ping but didn't respond** | PR timeline shows `mentioned`/`subscribed` events for a maintainer (they received the notification), but no review or comment followed | [orange] Merge prospect: low. They know about the PR and chose not to act. Possible silent disagreement with approach. |
| **Domain maintainer cross-referenced our PR** | A cross-reference from a user who is a known area maintainer (check profile) or whose source PR has a `maintainer` label. | [yellow] Merge prospect: moderate. They're tracking -- may champion it to core maintainers. |
| **Maintainer never engaged with issue or PR** | Zero maintainer comments on issue, no labels (or labels are auto-applied by reporter/bot), no maintainer activity on PR, AND no domain-maintainer cross-references | [red] Merge prospect: very low. Nobody with merge power has ever engaged. Consider closing to free a PR slot. |
| **Maintainer active in same area but skipping us** | Recent merges in same files/module, but our PR ignored | [orange] Merge prospect: low. They see it but chose not to engage -- may plan to fix differently or disagree with approach. Consider closing. |
| **Maintainer inactive across the board** | No merges from anyone in the last 7 days | [grey] Repo-wide slowdown. Not about our PR -- wait. |

**How to check "active in same area"** -- required for >72h stale PRs, not optional:
```bash
# Recent merges touching same files as our PR (last 7 days)
OUR_FILES=$(gh pr diff <NUMBER> -R <REPO> --name-only | head -5)
for FILE in $OUR_FILES; do
  gh api "repos/<REPO>/commits?path=$FILE&since=$(date -v-7d +%Y-%m-%dT%H:%M:%SZ)&per_page=3" --jq '.[].author.login' 2>/dev/null
done
# Also check recent merges by the pinged maintainer
gh api "repos/<REPO>/commits?author=<PINGED_MAINTAINER>&since=$(date -v-7d +%Y-%m-%dT%H:%M:%SZ)&per_page=5" --jq '.[] | {sha: .sha[:7], message: .commit.message[:80], date: .commit.author.date[:16]}' 2>/dev/null
```

**Label provenance matters.** Labels applied by the issue reporter or by bots (e.g., barnacle) are auto-applied from the issue template -- they do NOT indicate maintainer triage. Check `issues/<N>/events` to see who applied each label. Only count labels applied by MEMBER/COLLABORATOR/OWNER as triage signal.

**Report the diagnosis, not just the timestamp.** "Stale 4 days -- maintainer never engaged with issue [red], merge prospect very low" is actionable. "Stale 4 days" is not.

**Do NOT suggest re-pinging.** Re-pinging (even after 72h, even to a different maintainer) has not been effective in practice. Report the diagnosis and merge prospect so the user can decide. Only re-ping if the user explicitly asks.

### CI Triage (replacing binary green/red)

When CI has failures, don't just report [fail] -- **classify each failure**:

```bash
# Get our PR's changed files
OUR_FILES=$(gh pr diff <NUMBER> -R <REPO> --name-only | tr '\n' '|' | sed 's/|$//')

# For each failed job, check if the failure is in our files or upstream
gh pr checks <NUMBER> -R <REPO> 2>&1 | grep "fail" | while read line; do
  echo "$line"
done
```

**Three buckets:**
1. **Our code failing** -- the failed test/check is in a file we changed --> fix and push
2. **Upstream failing, our area passes** -- failures are in unrelated files, AND checks covering our area (e.g., `extension-fast (telegram)` for telegram changes) all pass --> **PR is ready for review.** Post/update triage comment listing our passing checks.
3. **Upstream failing, can't tell** -- failures are in shared infra (build, lint, type-check) that cover everything --> check if main has same failure. If yes, post triage comment.

**Report CI with nuance:**
- [pass] = all pass
- [pending] = still running
- [yellow] = upstream failures only, our area passes --> **ready for review with triage**
- [fail] = our code failing, or can't determine

**Key insight:** In repos with flaky CI (>20% failure rate on main), waiting for fully green CI is a losing strategy. The goal is giving the maintainer enough evidence that our code is clean -- not achieving a green badge that may never come.

To verify main CI, check the actual CI workflow -- NOT `gh run list` which includes non-CI workflows (Labeler etc.) that are always green.

**Conditional actions** -- data already collected in Step 2, act only when triggered:
- **Merge conflict**: Only act on `CONFLICTING` (not `UNKNOWN`). Rebase if main CI green.
- **Competing PR found** (Step 2 query returned results): Alert in report. Check if competing PR covers the same fix -- if so, compare approaches and assess supersession risk.
- **Linked issue closed** (Step 2 query returned `state: "closed"`): Determine supersession:
  ```bash
  # Find which PR closed it
  gh api repos/<REPO>/issues/<ISSUE>/comments --jq '.[] | select(.user.login != "<USERNAME>") | {date: .created_at[:16], body: .body[:200]}' | tail -3
  # Compare the competing PR's diff with ours
  gh pr diff <COMPETING_PR> -R <REPO> --name-only
  gh pr diff <OUR_PR> -R <REPO> --name-only
  # If same files: read both diffs and compare approaches
  ```
  Report one of three conclusions:
  - **Fully superseded** -- competing PR covers all our changes --> recommend closing our PR
  - **Partially overlapping** -- competing PR fixes some cases but not ours --> report which cases remain, PR is still needed
  - **Different approach, same issue** -- both valid but competing PR already merged --> recommend closing unless ours is strictly better
- **New cross-references**: Only report if new ones found since last check. Filter bot noise per cross-reference rules above.

## Step 3.5: Retrospective (on MERGED/CLOSED PRs)

For each PR that was MERGED or CLOSED this check, before removing the context file:

1. **Collect data** -- run ALL of these, not just issue comments:
   ```bash
   # Timeline
   gh pr view <NUMBER> -R <REPO> --json createdAt,mergedAt,closedAt,mergedBy --jq '{created: .createdAt[:16], merged: .mergedAt[:16], closed: .closedAt[:16], mergedBy: .mergedBy.login}'

   # Human reviews (what did the reviewer actually say?)
   gh api repos/<REPO>/pulls/<NUMBER>/reviews --jq '.[] | select(.state == "APPROVED" or .state == "CHANGES_REQUESTED") | {author: .author.login, state: .state, body: .body[:300]}'

   # Bot review scores (e.g., Greptile confidence)
   gh api repos/<REPO>/issues/<NUMBER>/comments --jq '.[] | select(.user.login | test("bot"; "i")) | {user: .user.login, body: .body[:200]}'

   # Inline review comments (what specific code did bots/reviewers flag?)
   gh api repos/<REPO>/pulls/<NUMBER>/comments --jq '[.[] | .user.login] | group_by(.) | map({user: .[0], count: length})'

   # Our ping --> first response time
   gh api repos/<REPO>/issues/<NUMBER>/comments --jq '[.[] | {user: .user.login, date: .created_at[:16]}] | .[-5:]'
   ```

2. **Calculate timeline**: opened --> pinged --> first human response --> merged/closed. How many days at each stage?

3. **Write retrospective into the context file** -- append an `## Outcome` section:
   ```markdown
   ## Outcome
   - **Result**: merged / closed (reason)
   - **Timeline**: opened [date] --> pinged [date] --> reviewed [date] --> merged [date] ([N] days total)
   - **Reviewed by**: @who -- what they specifically cared about (quote their review comment)
   - **Bot scores**: Greptile [N]/5, Codex [N] rounds ([summary of key concerns])
   - **What worked**: (fast merge? clean review? good approach? what specifically made this succeed/fail?)
   - **What surprised us**: (unexpected rejection? bot concern we missed? maintainer preference we didn't know?)
   - **Lesson**: (one actionable takeaway -- not "clean merge, no lessons" unless truly nothing was learned)
   ```
3. **Route the lesson** (if any):
   - **Repo-specific** (maintainer name, bot quirk, label, convention) --> also append to profile's Lessons Learned section
   - **Universal** (methodology improvement, new technique) --> flag to user: "This lesson may be universal -- consider updating oss-* skill"
4. **Then** archive context file: `mv pr-<REPO>-<N>.md` --> `./oss-pilot-data/context/_archived/`

**Why write retrospective into the context file**: The archived file becomes a complete record -- approach --> decisions --> outcome --> lesson. When oss-discover encounters a similar issue in the future, checking `_archived/` reveals not just "we tried this" but "we tried this and here's what happened."

### Maintenance Check (after retrospective)

After archiving, check if accumulated knowledge needs pruning. Skip if no PRs were merged/closed this run.

**Profile Lessons Learned (trigger: >15 entries)**:
1. Read all entries in Lessons Learned section
2. For each entry: has this lesson been absorbed into a more structured section?
   - Encoded in Architecture Patterns --> remove from Lessons Learned
   - Encoded in Maintainer Styles --> remove from Lessons Learned
   - Encoded in Bot Behavior --> remove from Lessons Learned
3. For remaining entries: is the lesson still accurate?
   - Stale (references a bot that no longer exists, a maintainer who left, a process that changed) --> remove or update
4. Report: "Pruned N lessons (M absorbed, K stale). Lessons Learned now has X entries."

**Archived context files (trigger: >30 files for this repo)**:
1. Count files matching `pr-<REPO>-*.md` in `_archived/`
2. If >30, identify cleanup candidates:
   - Older than 6 months AND Outcome is "clean merge, no new lessons" --> delete
   - Older than 6 months AND Outcome has lessons --> keep (valuable reference)
   - Any age AND Outcome is "closed for technical rejection" --> keep (prevents re-attempts)
3. Report: "Pruned N archived context files. X remain."

**Profile total size (trigger: >200 lines)**:
1. `wc -l` the profile
2. If >200: flag to user which sections are largest, suggest review
3. Do NOT auto-prune structured sections (Architecture Patterns, Maintainer Styles) -- these require human judgment

## Step 4: Report

### Diff-only repeat checks

If this is a repeat check within the same conversation, only report **what changed** since the last check. Skip the full table if nothing changed. Example:

```
Since last check (2h ago): no changes. All 4 PRs waiting for review.
```

If something changed:
```
Since last check (6h ago):
 - #52644 crossed 72h --> [orange] agents area active but skipping us, merge prospect low
 - #51384 mergeable resolved --> MERGEABLE [pass]
 Rest unchanged (3 PRs waiting).
```

### Full report (first check or significant changes)

```
+===============================================================+
|              OSS Check-In: <repo>                             |
+===============================================================+

 PR       CI   Bot  Stale Diagnosis                  Merge Prospect
 #123     [pass]   [pass]   [yellow] maint. knows issue (2d)        moderate
 #456     [fail]   [pass]   --                                 blocked (CI)
 #789     [pass]   [pass]   [red] no maint. engagement (5d)      very low
 #012     [merged]   -    --                                 merged --> archived

+===============================================================+
```

### Portfolio Health (always include on first check)

After the PR table, add a portfolio summary:

```
Portfolio: 4 open PRs (of 10 max). Total wait: 17 days across all PRs.
Slot pressure: low / medium / high (based on proximity to barnacle's 10-PR limit)
Merge outlook:
 - 1 moderate prospect (#51384)
 - 1 moderate prospect (#52053 -- domain maint. tracking)
 - 1 low prospect (#52644 -- being skipped)
 - 1 very low prospect (#52137 -- zero engagement)
Recommendation: [only if actionable, e.g., "Consider closing #52137 to free a slot for higher-value work"]
```

**Slot pressure levels:**
- **Low** (<=5 open): plenty of room
- **Medium** (6-8 open): be selective about new PRs
- **High** (9-10 open): barnacle will auto-close at 11 -- close low-prospect PRs before opening new ones

## Step 5: Update Context Files

For each PR where action was taken, update the context file Decisions section.

## Context Files

Live at `./oss-pilot-data/context/pr-<REPO-SHORT>-<NUMBER>.md` (e.g., `pr-openclaw-52644.md`). See `/oss-auto` for format.

## Error Handling

- Missing context file for open PR --> create from GitHub data
- Merged/closed PR --> archive context file to `./oss-pilot-data/context/_archived/`
- GitHub API failure --> report error, skip that PR
