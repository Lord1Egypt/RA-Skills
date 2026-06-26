---
name: oss-discover
description: Find high-value PR opportunities on any open-source repo. Triggers on
  "oss discover", "find issues", "what should I work on", "next PR",
  "openclaw discover".
user_invocable: true
---

# OSS PR Opportunity Discovery

Surface the highest-value, most-likely-to-merge PR opportunities. Works on any repo with a profile.

## Invocation

- `oss-discover <repo>` -- scan a specific repo
- `oss-discover` -- scan all repos with profiles

## Step 0: Load Profile

Read `./oss-pilot-data/profiles/<repo>.md` for repo, fork, username, local_path, upstream_remote. Profile schema: see `./oss-pilot-data/profiles/_template.md` for expected sections.

**Critical: `upstream_remote` determines which git remote is used for ALL local code verification** (e.g., `git show <UPSTREAM_REMOTE>/main:`). If the local clone has multiple remotes (origin, upstream, fork), using the wrong one produces false positives -- you'll verify against a stale fork instead of the real upstream. Always use the profile's `upstream_remote` value, never hardcode `origin`.

## Step 0.5: Repo Openness Check

Before spending time scanning issues, check if this repo actually merges external contributions:
```bash
# Count recent merged PRs from external contributors vs maintainers
MAINTAINERS=$(gh pr list -R <REPO> --state merged --limit 30 --json mergedBy --jq '[.[].mergedBy.login] | unique | join(",")')
TOTAL=$(gh pr list -R <REPO> --state merged --limit 30 --json number --jq 'length')
EXTERNAL=$(gh pr list -R <REPO> --state merged --limit 30 --json author,mergedBy --jq "[.[] | select(.mergedBy.login as \$m | .author.login != \$m)] | length")
echo "Last 30 merged: $EXTERNAL external out of $TOTAL total"
echo "Active maintainers: $MAINTAINERS"
```

**Interpret the ratio:**
- **>30% external** --> open repo, good for contributions. Proceed normally.
- **10-30% external** --> selective repo, PRs need to be high quality. Proceed but be picky.
- **<10% external** --> closed repo, maintainers do most work themselves. **Warn the user**: "This repo merges very few external contributions. Consider whether the time investment is worth it, or pick a more open repo."

This is NOT a hard blocker -- some closed repos still merge great first PRs. But the user should know the odds before investing hours.

## Step 0.6: Velocity Check

Check how fast issues get claimed in this repo:
```bash
# Sample 5 recent good-first-issue PRs -- how quickly did they get their first competing PR?
for issue in $(gh issue list -R <REPO> --label "good first issue" --state open --limit 5 --json number --jq '.[].number'); do
  prs=$(gh pr list -R <REPO> --search "$issue" --state open --json number --jq 'length')
  echo "#$issue: $prs competing PRs"
done
```

**Interpret the competition rate:**
- **<50% of issues have competing PRs** --> LOW velocity. Normal flow (Source 0-8).
- **50-80% have competing PRs** --> MEDIUM velocity. Prioritize Source 0 (maintainer-filed), Source 8 (codebase scan), and stale-PR reclaimable, but still check Source 1-2.
- **>80% have competing PRs** --> HIGH velocity. **Skip Source 1-7** -- issues get claimed within hours, scanning them is a waste of time. Always run Source 0 (maintainer-filed issues don't compete the same way). Then go directly to:
  1. **Source 8** -- codebase scan for safe cleanups (no issue needed, no competition)
  2. **Stale PR reclaimable** -- find issues where competing PR is stale (>1 month no update) and redo the work
  3. **Ecosystem repos** -- check if the project has plugin/extension/docs repos (often mentioned in CONTRIBUTING.md) that are less competitive
  4. **Suggest real-time watch** -- tell the user: "This repo moves too fast for async discovery. Set up GitHub notifications for new `good first issue` labels to claim early."

## Step 1: Gather Exclusion List

```bash
# Issues we already have PRs for
gh pr list -R <REPO> --author <USERNAME> --state open --json body --jq '.[].body' | grep -oE 'Closes #[0-9]+' | grep -oE '[0-9]+' | sort -u

# Files our open PRs touch (for code-level exclusion)
for pr in $(gh pr list -R <REPO> --author <USERNAME> --state open --json number --jq '.[].number'); do
  gh pr diff $pr -R <REPO> --name-only
done | sort -u

# Issues we previously attempted (check archived context files)
grep -l "repo: <REPO>" ./oss-pilot-data/context/_archived/pr-*.md 2>/dev/null | while read f; do
  grep -oE 'issue: [0-9]+' "$f" | grep -oE '[0-9]+'
done | sort -u
```

For each previously attempted issue found in `_archived/`, read the `## Outcome` section. If the PR was **closed** (not merged), check why:
- **Closed for hygiene** (dirty, stale, too-many-prs) --> issue may still be valid, don't auto-exclude but note the prior attempt
- **Closed for technical rejection** (wrong approach, won't fix) --> exclude unless the Outcome suggests a different approach could work
- **Merged** --> exclude (already done)

**Age relevance**: For archived context files older than 6 months, treat exclusions as soft -- maintainers rotate, codebases evolve, and a previously rejected approach may now be welcome. Note the prior attempt but don't auto-exclude.

## Step 2: Search Sources

**IMPORTANT: Search order is by merge signal strength, not source number. Start from Source 0 (strongest signal) and work down. If Source 0-1 yield enough good candidates, don't waste time on weaker sources.**

**Early exit rule:** After Source 1, run competition checks on all high-signal candidates. If every Bounty / Quick Win / good-first-issue candidate already has competing PRs, the repo is too competitive for async discovery. Report this immediately -- don't proceed through Sources 2-7 one by one arriving at the same conclusion. Jump directly to Source 8 (codebase scan) for one quick attempt, and if that also fails, recommend the user either watch for new issues in real-time or focus on a less competitive repo.

**Source 0 -- Maintainer-filed issues (STRONGEST SIGNAL):**
Issues filed by maintainers are the highest-signal candidates -- the person with merge power cares enough to write it up. These are [green] by definition and skip the triage gate.
```bash
# Search issues filed by known maintainers (from profile's Maintainer Review Styles section)
for MAINT in <MAINTAINER_LIST>; do
  gh issue list -R <REPO> --author "$MAINT" --state open --json number,title,createdAt --limit 5 --jq '.[] | {number, title: .title[:70], created: .createdAt[:10], author: "'$MAINT'"}'
done
```
If the profile doesn't list maintainers, derive them from recent merge activity:
```bash
gh pr list -R <REPO> --state merged --limit 20 --json mergedBy --jq '[.[].mergedBy.login] | unique | .[]'
```
**Filter**: skip feature requests, roadmap items, and anything with >10 files in scope. Focus on bugs and build-blockers that a maintainer filed and wants fixed.

**Staleness decay for maintainer-filed issues**: [green] is not permanent. Apply decay based on last maintainer activity on the issue (comment, label, linked PR review -- not just filing date):
- **<14 days since last maintainer activity** --> [green] full signal
- **14-30 days, no endorsed PR was closed** --> [green] but note staleness
- **14-30 days, endorsed PR was closed by maintainer** --> downgrade to [yellow] -- maintainer deprioritized or plans to handle it differently
- **>30 days with zero activity** --> downgrade to [yellow] -- issue may be abandoned, verify it's still relevant before investing

Staleness decay does NOT apply if the maintainer is still active in the repo (merging other PRs). It only matters when the specific issue has gone cold.

**Source 1 -- Maintainer-signal labels (HIGHEST PRIORITY):**
First, scan ALL labels to find high-signal ones -- every repo uses different names:
```bash
gh label list -R <REPO> --json name --jq '[.[].name] | sort | .[:50]'
```
Look for labels that indicate **maintainer intent to accept contributions**:
- Bounty / reward labels (e.g., `[diamond] Bounty`, `bounty`, `$$`)
- Quick win / low-hanging fruit (e.g., `! Quick Wins`, `easy fix`)
- Help wanted / good first issue (e.g., `[hand]help wanted`, `[pass] good first issue`)
- Regression labels (e.g., `[regressing] regressing`, `regression`) -- maintainers want these fixed urgently
- Priority labels (e.g., `High priority`, `Urgent`)

Then search issues with each high-signal label found:
```bash
gh issue list -R <REPO> --label "<HIGH-SIGNAL-LABEL>" --state open --json number,title,createdAt,author --limit 10 --jq '.[] | {number, title: .title[:70], author: .author.login, created: .createdAt[:10]}'
```
**These candidates should be evaluated FIRST** -- a bounty or quick-win issue has 3-5x the merge probability of an unlabeled bug. However, still run **label provenance** in Step 3b -- some repos auto-apply high-signal labels from issue templates. Only labels applied by MEMBER/COLLABORATOR/OWNER are true triage signals.

**Source 2 -- Recent bugs:**
```bash
gh issue list -R <REPO> --label "bug" --state open --json number,title,createdAt,author --limit 20 --jq '.[] | {number, title: .title[:70], author: .author.login, created: .createdAt[:10]}'
```
**Warning**: Do NOT use date string filtering with `--jq 'select(.createdAt > "YYYY-MM-DD")'` -- this returns empty results due to timezone/format mismatches between local time and GitHub's UTC timestamps. Instead, use `--limit 30` and filter manually by recency.

Prefer bugs filed by maintainers or users with reproduction steps. Unlabeled bugs from unknown authors are the weakest signal.

**Source 3 -- CI failures on default branch:**
```bash
# Auto-detect default branch (main, master, develop, etc.)
DEFAULT_BRANCH=$(gh repo view <REPO> --json defaultBranchRef --jq .defaultBranchRef.name)

# Check recent CI runs
gh run list -R <REPO> --branch $DEFAULT_BRANCH --limit 3 --json workflowName,conclusion,createdAt --jq '.[] | {conclusion, workflow: .workflowName, date: .createdAt[:16]}'
```

**Source 4 -- Reclaimable closed PRs** (closed for hygiene, not rejection):
```bash
gh pr list -R <REPO> --state closed --label "good first issue" --limit 10
```

**Source 4b -- Reclaimable from other contributors' closed PRs on maintainer-filed issues:**
High-signal variant of Source 4. Maintainer-filed issues where someone submitted a fix but the PR was closed without merging -- the issue is validated, the fix direction is often known, but no one finished the work.
```bash
# For each Source 0 maintainer-filed issue, check if there were closed (not merged) PRs
for ISSUE in <SOURCE_0_ISSUE_NUMBERS>; do
  closed_prs=$(gh pr list -R <REPO> --search "$ISSUE" --state closed --json number,title,author,mergedAt --jq '.[] | select(.mergedAt == null) | {number, title: .title[:70], author: .author.login}')
  if [ -n "$closed_prs" ]; then
    echo "=== Issue #$ISSUE has closed (unmerged) PRs ==="
    echo "$closed_prs"
  fi
done
```

**Closure reason analysis is CRITICAL for reclaimables.** Check WHO closed the PR and WHY:
```bash
# For each closed PR found above:
gh api repos/<REPO>/issues/<PR_NUMBER>/events --jq '.[] | select(.event == "closed") | {actor: .actor.login}' 2>/dev/null
gh api repos/<REPO>/issues/<PR_NUMBER>/comments --jq '.[-3:] | .[] | {user: .user.login, body: .body[:200]}'
```

Classify the closure:
| Closer | Likely reason | Action |
|---|---|---|
| **openclaw-barnacle[bot]** or stale bot | Hygiene (stale, dirty, too-many-prs) | [pass] Safe to reclaim -- bot doesn't judge quality |
| **PR author** | Author abandoned or submitted a better version | Check if replacement exists; if not, [pass] reclaimable |
| **Maintainer who endorsed the PR** | ! **Ambiguous -- investigate before committing** | Read the last 3 comments. Look for: batch cleanup, deprioritization, "will handle internally", or silence. If no explanation found, treat as [yellow] not [green] |
| **Maintainer who did NOT comment on the PR** | Likely batch cleanup or repo hygiene | [pass] Probably safe to reclaim, but verify issue is still wanted |

**The "maintainer endorsed then closed" pattern deserves extra scrutiny.** When a maintainer says "this is the right fix" and then closes the PR themselves (not stale bot), possible reasons include:
- Batch-closing old PRs during a cleanup sweep
- Decided to handle it internally (will fix themselves)
- Deprioritized the issue entirely
- Wanted a different scope (e.g., fix all `||` vs `??` in one PR, not one at a time)

If you cannot determine the reason from comments/timeline, **do not present as [green]**. Mark as [yellow] with explicit note: "Prior endorsed PR was closed by maintainer without explanation -- reclaim with caution."

**Source 5 -- Merged PR gaps ("What I Did NOT Verify"):**
Recently merged PRs often have explicit gaps the author acknowledged. These are the safest follow-up opportunities -- the work is scoped, the maintainer already approved the direction.
```bash
gh pr list -R <REPO> --state merged --limit 10 --json number,title,body --jq '.[] | select(.body | test("not verif|TODO|follow.up|happy to revisit"; "i")) | {number, title: .title[:70]}'
```
Check for: unverified scenarios, deferred edge cases, declined bot suggestions marked "happy to revisit."

**Yield warning for "maintainer follow-up hints"**: In theory, maintainer comments like "this should be a follow-up" are goldmine opportunities. In practice, many repos' maintainers don't leave textual follow-up hints -- they merge cleanly or push fixes themselves. If you scan maintainer comments for follow-up language, limit to 10 most recent merged PRs and move on quickly if nothing found. The structured "What I Did NOT Verify" approach (above) is much higher yield.

**Source 6 -- Scoped modules** (extensions, plugins, packages):
Repos with modular structure have isolated areas with lower blast radius and faster review.
```bash
# Step 1: Discover module structure from repo directories (if local clone exists)
ls <LOCAL_PATH>/extensions/ <LOCAL_PATH>/plugins/ <LOCAL_PATH>/packages/ <LOCAL_PATH>/apps/ 2>/dev/null | head -20

# Step 2: Discover module labels (every repo uses different labels -- don't hardcode)
gh label list -R <REPO> --json name --jq '[.[].name] | .[:30]'
# Look for labels that name specific components (e.g., "auth", "cli", "edge functions", "extension: telegram", "app")
# Then search issues with those labels
```
Don't hardcode label patterns -- every repo is different. Scan the label list first, then pick relevant ones.

**Source 7 -- Area merge rate signal** (tiebreaker only):
Areas with recent merges = maintainers paying attention = faster review.
```bash
gh pr list -R <REPO> --state merged --limit 30 --json title --jq '[.[].title[:20]] | group_by(.) | map({area: .[0], count: length}) | sort_by(.count) | reverse | .[:5]'
```
Hot area (+1 confidence) vs cold area (-1 confidence). Use as tiebreaker, not primary signal.

**Nuanced usage**: Area merge rate matters because maintainer attention shifts week by week. Check who specifically is merging in the area, not just the count:
```bash
gh pr list -R <REPO> --state merged --limit 20 --json mergedBy,title --jq '.[] | {merger: .mergedBy.login, title: .title[:50]}'
```
A maintainer actively reviewing one area this week will review yours fast -- but if they shift focus next week, your PR may sit.

**Source 8 -- Codebase scan for safe cleanups** (especially good for first PRs):
If local clone exists, scan for known-safe cleanup patterns that don't need an issue:
```bash
# 1. Run the type checker -- catches real errors maintainers want fixed
#    IMPORTANT: run `pnpm install --frozen-lockfile` FIRST to avoid stale node_modules false positives
cd <LOCAL_PATH> && git checkout <UPSTREAM_REMOTE>/main --detach && pnpm install --frozen-lockfile && pnpm tsgo 2>&1 | tail -30

# 2. Truthy coercion bugs: || where ?? is correct (0 treated as falsy)
#    These are real bugs, not style issues -- validated by scoootscooob filing 3 issues for this pattern
grep -rn '|| [0-9]' --include="*.ts" <LOCAL_PATH>/src/ <LOCAL_PATH>/extensions/ 2>/dev/null | grep -v node_modules | grep -v '.test.' | head -10

# 3. Missing test files for recently changed source files
for f in $(git log <UPSTREAM_REMOTE>/main --oneline --name-only -20 -- '*.ts' | grep -v '.test.' | grep -v node_modules | sort -u | head -10); do
  test_file="${f%.ts}.test.ts"
  if [ ! -f "$test_file" ]; then
    echo "MISSING TEST: $f (no $test_file)"
  fi
done

# 4. Duplicate translation keys (JSON)
python3 -c "import json,re; lines=open('<LOCAL_PATH>/packages/i18n/locales/en/common.json' if '<LOCAL_PATH>' else '').readlines(); seen={}; [print(f'L{i+1}: dup \"{m.group(1)}\"') for i,l in enumerate(lines) if (m:=re.match(r'\s*\"([^\"]+)\"\s*:\s*(.*)',l)) and ((seen.setdefault(m.group(1),(i,m.group(2).rstrip().rstrip(',').strip())) and False) or (m.group(1) in seen and seen[m.group(1)][1]==m.group(2).rstrip().rstrip(',').strip()))]" 2>/dev/null

# 5. Images missing alt text (a11y)
grep -rn '<img' --include="*.tsx" --include="*.jsx" <LOCAL_PATH>/packages/ 2>/dev/null | grep -v 'alt=' | grep -v node_modules | head -5

# 6. Inconsistent error handling patterns (e.g., bare catch {})
grep -rn 'catch\s*{' --include="*.ts" <LOCAL_PATH>/src/ <LOCAL_PATH>/extensions/ 2>/dev/null | grep -v node_modules | grep -v '.test.' | head -5
```

**Important for Source 8**: Run `pnpm install --frozen-lockfile` before any local verification. Stale `node_modules` can produce false type errors that waste significant time investigating non-issues. This was validated by experience: tsgo reported 20 errors that all disappeared after a fresh install.

These produce XS PRs (1 file, <10 lines) that match patterns recently merged by maintainers. No issue needed -- the PR itself is the justification.

## Step 3: Filter

- Exclude issues from exclusion list (Step 1)
- Skip issues with >5 comments
- Skip issues with linked PRs: check timeline for cross-references

### Step 3b: Maintainer Interest Gate (MANDATORY for every candidate)

Before investing in competition check and code verification, assess whether a maintainer is likely to review a PR for this issue. This is the #1 predictor of merge -- a perfect PR with zero maintainer interest will sit forever.

```bash
# For each candidate issue:

# 1. Basic metadata + issue author association
gh api repos/<REPO>/issues/<NUMBER> --jq '{
  author_association: .author_association,
  assignee: (.assignee.login // "none"),
  labels: [.labels[].name],
  milestone: (.milestone.title // "none")
}'

# 2. Count maintainer comments (MEMBER, COLLABORATOR, OWNER)
gh api repos/<REPO>/issues/<NUMBER>/comments --jq '[.[] | select(.author_association == "MEMBER" or .author_association == "COLLABORATOR" or .author_association == "OWNER")] | length'

# 3. Label provenance -- WHO applied each label?
#    Labels from issue reporter (template dropdowns) or bots != maintainer triage
gh api repos/<REPO>/issues/<NUMBER>/events --jq '.[] | select(.event == "labeled") | {label: .label.name, actor: .actor.login, association: (.actor.author_association // "UNKNOWN")}' 2>/dev/null

# 4. Area activity -- are maintainers committing to affected files recently?
#    Identify likely affected files from issue title/body, then check recent commits.
#    A maintainer active in the same files = they'll see your PR in their diff review.
gh api "repos/<REPO>/commits?path=<LIKELY_FILE>&since=$(date -v-7d +%Y-%m-%dT%H:%M:%SZ)&per_page=3" --jq '[.[] | .author.login] | unique'
```

Classify each candidate using **verified signals only**:

| Signal | Evidence | Icon |
|---|---|---|
| Maintainer **filed** the issue | `author_association` is MEMBER/COLLABORATOR/OWNER | [green] |
| Maintainer **assigned** the issue | `assignee` is set | [green] |
| Maintainer **commented** on the issue | Maintainer comment count > 0 | [green] |
| Maintainer **labeled** the issue | Label event shows actor with MEMBER/COLLABORATOR/OWNER association | [yellow] |
| Issue has **milestone** | Went through triage and was scheduled | [yellow] |
| Maintainer **active in affected files** (last 7 days) | Recent commits by maintainer to files the issue touches | [yellow] |
| Labels exist but applied by **reporter or bot only** | Label provenance shows non-maintainer actors | [grey] neutral -- NOT triage |
| Zero maintainer interaction of any kind | No maintainer comments, no maintainer-applied labels, no assignee, filed by non-maintainer | [red] |

**Label provenance matters.** Labels applied by the issue reporter (from template dropdowns) or by bots (e.g., barnacle `bug:behavior`) do NOT indicate maintainer triage. Only labels applied by MEMBER/COLLABORATOR/OWNER count as [yellow]. Validated by data: issues with reporter-applied labels and zero maintainer interaction had the same merge outcome as fully unlabeled issues.

**Area activity is a leading indicator.** A maintainer actively committing to the files an issue touches means (a) they'll notice your PR in their review queue and (b) they have recent context on the code. This is [yellow] even without direct issue engagement. However, if a maintainer is active in the area AND ignoring your pinged PR, that's a [orange] signal in oss-check -- meaning they've seen it and chosen not to engage.

**[red] is a soft blocker.** Data shows PRs targeting [red] issues have very low merge rates -- maintainers active in the same files will skip your PR rather than review it. **Skip [red] candidates unless no [green]/[yellow] candidates exist.** If you must report a [red] candidate, it goes last with an explicit warning.

**Ordering rule**: [green] > [yellow] > [grey] > [red]. Within the same tier, use competition and scope as tiebreakers.

**[red] batch early-exit**: In high-volume repos (>20 bugs/day), reporter-filed issues almost never have maintainer triage. When running Step 3b on Source 2 candidates: check the first 5. If all 5 are [red], sample 2 more. If still all [red], **stop checking Source 2** -- report "Source 2: 7/7 sampled bugs are [red] (zero maintainer engagement), skipping remaining" and move to higher-signal sources (Source 0, Source 5, Source 3). Do not spend 45 API calls confirming what the first 5 already told you.

## Step 4: Competition Check (HARD BLOCKER -- mandatory for every candidate)

For each candidate, BOTH checks must be run before reporting:

1. **Issue-level**: `gh pr list -R <REPO> --search "<issue-number>" --state open`
2. **Code-level**: Identify root cause file/function, then search with context keyword + function name to avoid false positives:
   ```bash
   # Good: "Anthropic sanitizeToolCallIds" -- narrow, relevant results
   # Bad:  "sanitizeToolCallIds" alone -- returns 29 unrelated PRs about other providers
   gh pr list -R <REPO> --search "<context-keyword> <function-name>" --state open --json number,title,author --jq '[.[] | select(.author.login != "<USERNAME>")]'
   ```
   Skim returned titles/descriptions to filter noise. Only count PRs **actually targeting the same fix**.
3. Also check against our own PRs' files (from Step 1) -- if candidate touches same files, skip.
4. If either level finds >2 competing PRs actually targeting the same fix --> mark as [fail].

**This is NOT optional.** A candidate falsely reported as "no competition" is worse than no recommendation.

## Step 5: Code-Level Verification

**This is NOT optional.** An open issue does NOT mean the bug still exists. Maintainers push fixes without closing issues. Recommending a "fixed" issue wastes everyone's time.

**VERIFY STALENESS EARLY.** Before deep-diving into competition checks and comment analysis for Source 0 candidates, do a quick existence check: does the specific file/function/pattern mentioned in the issue still exist on current main? This takes 30 seconds and can save 10 minutes of wasted research.

**Prerequisite**: Fetch the correct remote first. Use `upstream_remote` from the profile -- NOT `origin` (which may point to a stale fork):
```bash
cd <LOCAL_PATH> && git fetch <UPSTREAM_REMOTE> main
```

Then verify the EXACT function and EXACT pattern from the issue -- not just a keyword grep:
```bash
# BAD: grep for a keyword that exists in OTHER functions
#   git show <UPSTREAM_REMOTE>/main:<FILE> | grep "isFinite(pid)"  <-- finds hits in wrong function!
# GOOD: verify the specific function contains the specific bug pattern
#   git show <UPSTREAM_REMOTE>/main:<FILE> | sed -n '/function parseLaunchctlPrint/,/^}/p' | grep "isFinite(pid)"
git show <UPSTREAM_REMOTE>/main:<FILE_FROM_ISSUE> 2>&1 | head -3  # does file exist?
git show <UPSTREAM_REMOTE>/main:<FILE_FROM_ISSUE> | sed -n '/function <FUNCTION_NAME>/,/^}/p' | grep "<EXACT_PATTERN>"  # does the SPECIFIC function still have the bug?
```
If the file is gone or the pattern is fixed, mark as STALE immediately and move to the next candidate. Do not spend API calls on competition/interest checks for dead issues.

For each top candidate (top 3-5), verify **the specific pattern described in the issue** still exists on main -- not just that related keywords appear somewhere:
```bash
# Step A: Check git log for fix commits mentioning the issue or keyword
git log upstream/main --oneline --grep="<keyword>" | head -5
gh pr list -R <REPO> --search "<issue-number>" --state merged --json number,title --jq '.[].title' | head -3

# Step B: Verify the EXACT bug pattern still exists in code
# BAD: "server_default exists somewhere" --> too broad, false positive
# GOOD: "server_default=sa.text('uuid_generate_v4()') exists in model files" --> specific pattern from issue
gh search code "<exact-pattern-from-issue>" --repo <REPO> --json path --jq '.[].path' | head -5

# Step C: If no local clone, read the suspected file via API
gh api repos/<REPO>/contents/<file-path> --jq '.content' | base64 -d | grep "<pattern>" | head -5
```

**Common false positive**: A keyword exists in the codebase but the specific bug was already fixed. Always match the **exact pattern** described in the issue, not just related keywords.

Also check for AI-attempted labels (`codex`, `devin`, etc.) -- if a previous AI attempt was closed, read the closure reason. The issue is valid but the approach may need to be different.

### Step 5A: Code Authorship Signal

Once you've identified the buggy file/function, check who wrote that code. If the original author is a known maintainer, this is a strong merge signal -- they understand the context instantly and have no friction deleting/modifying their own code.

```bash
# Identify the original author of the bug pattern
git blame <UPSTREAM_REMOTE>/main -- <FILE_FROM_ISSUE> |
  sed -n '/<BUG_PATTERN>/p' |
  awk '{print $2}' | tr -d '(' | sort | uniq -c | sort -rn | head -3
```

Cross-reference the result with the profile's Maintainer Review Styles section:
- **Author is a known maintainer** --> upgrade candidate to [green] in Step 3b, and note this maintainer as the **primary ping target**. Validated by PR #55922: vincentkoc authored the OAuth guard, we pinged him, merged in 2.1 days with zero review friction.
- **Author is a former contributor (not active)** --> no signal change, but the code may lack an active champion.
- **Author is unknown** --> no signal change.

**Why this works**: A maintainer reviewing a fix to code they wrote has near-zero cognitive load. They already know why the code exists, what edge cases matter, and whether your fix is correct. This is the difference between "please review this unfamiliar code" and "hey, this guard you wrote in #45453 is now stale."

### Step 5B: Version Check

If the issue reports a specific version, check if a newer release exists that might fix it:
```bash
# What version does the issue report?
# Compare against latest release
gh release view -R <REPO> --json tagName,publishedAt --jq '{tag: .tagName, published: .publishedAt[:10]}'

# Scan release notes between reported version and latest for related fixes
gh release view -R <REPO> --json body --jq '.body' | grep -i "<keyword>"
```
If a newer release mentions fixes in the same area (packaging, provider registration, the specific component), **flag the candidate**: "Issue may be version-specific -- check if still reproduces on latest release before investing time."

### Step 5C: Comment Intelligence

**Read the issue comments before committing to work.** Existing comments often contain:
- Root cause analysis that's already done (saves time)
- Signals that the issue is resolved ("fixed in latest", "workaround found")
- Contradictions in the root cause analysis (red flag for scope)
- Maintainer responses ("won't fix", "by design", "duplicate of #X")
```bash
gh api repos/<REPO>/issues/<NUMBER>/comments --jq '.[] | {user: .user.login, body: .body[:200]}' | head -10
```
**Red flags to watch for:**
- Comment says "likely fixed in version X" --> verify before working
- Root cause analysis contradicts itself --> scope risk, needs deeper investigation
- Maintainer says "by design" or "won't fix" --> skip
- Multiple people offering different root causes --> unclear problem, risky

### Step 5D: Fix Feasibility

For each top candidate, quickly assess if the fix is actually doable:
- **Root cause clear?** Is there a consistent, non-contradictory explanation of why the bug happens?
- **Scope bounded?** Can you identify which files/functions need to change without reading the entire codebase?
- **Testable?** Can you verify the fix without special infrastructure (running servers, specific hardware, paid APIs)?
- **Safe?** Does it touch security-sensitive code (auth, exec approval, permissions)?

If any answer is "no" and this is a first-time contribution, **downgrade the candidate** -- save it for after you have trust and codebase familiarity.

Drop any candidate where the fix already landed. Mark remaining candidates as **verified**.

**Verification is NOT optional.** If you cannot verify a candidate (e.g., no local clone, can't access the file), you MUST mark it as `! UNVERIFIED` in Step 6. Never present an unverified candidate without this flag -- the user needs to know verification was skipped so they can decide whether to invest time.

## Step 6: Present Candidates

Answer 3 yes/no questions per candidate:

| Question | Signal |
|---|---|
| **Maintainer interest?** | From Step 3b: [green] (filed/assigned/commented by maintainer), [yellow] (maintainer-applied label, milestone, or active in affected files), [grey] (reporter/bot labels only), [red] (zero maintainer interaction). **#1 merge predictor.** |
| **No competition?** | Zero PRs for same issue AND same code area |
| **Supersession-resistant?** | Fix is at the caller level (self-contained), not callee level (fragile -- someone fixing all callers makes your callee fix redundant). Especially important for high-competition issues. |
| **Small scope?** | <200 lines, <5 files |

```
 #  Issue    Interest               No comp?  Small?  Verified?  Title
 1  #XXXXX   [green] maint. filed        [pass]        [pass]      [pass]          description
 2  #YYYYY   [yellow] maint. labeled      [pass]        [pass]      [pass]          description
 3  #AAAAA   [yellow] area active (7d)    [pass]        [pass]      ! UNVERIFIED  description
 4  #BBBBB   [grey] reporter-labeled     [pass]        [pass]      [pass]          description -- no triage signal
 5  #ZZZZZ   [red] zero engagement     [pass]        [pass]      [pass]          description ! skip unless no [green]/[yellow]
```

**[red] candidates MUST include a warning**: "No maintainer has engaged with this issue. Data shows these PRs have very low merge rates even when technically perfect. Skipping recommended -- only proceed if no [green]/[yellow] candidates are available."

**[grey] candidates note**: "Labels were applied by the issue reporter or bots, not by a maintainer. This does not count as triage -- treat as slightly better than [red] but do not confuse with maintainer interest."

For each include: suggested approach (1 sentence), risk factors.

## First PR on a New Repo

If this is our first contribution to a repo (no merged PRs yet), **prioritize low-risk scope over strong signal**:
- Prefer peripheral code (tests, i18n, a11y, docs tooling, CLI) over core infrastructure (auth, billing, availability, data pipeline)
- A merged small fix builds trust; a rejected core fix builds nothing
- Save high-signal core issues for after we have 1-2 merged PRs and understand the codebase

## What NOT to Work On

- Speculative features without an issue
- Large refactors (>10 files)
- Areas with 5+ competing PRs
- Documentation-only PRs without evidence
- Dependency bumps without security advisory
- **First PR**: core infrastructure changes (availability engine, auth, billing, data pipeline)
