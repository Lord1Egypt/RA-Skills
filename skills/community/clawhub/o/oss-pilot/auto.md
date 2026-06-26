---
name: oss-auto
description: End-to-end PR automation for any open-source repo. From issue number
  to opened PR with CI monitoring. Triggers on "oss auto", "auto PR", "auto fix",
  "openclaw auto".
user_invocable: true
---

# OSS Auto PR Skill

**Role: Workflow orchestrator.** Composes discover --> implement --> pr-review --> check into one end-to-end flow. Not an independent capability -- delegates quality checks to /oss-pr and discovery to /oss-discover.

Take an issue number and drive it to an opened, reviewed, bot-responded, maintainer-pinged PR. Works on any repo with a profile.

## Invocation

- `oss-auto <repo> #XXXXX` -- Fix a specific issue on a repo
- `oss-auto <repo>` -- Run /oss-discover, pick the top candidate, and fix it

## Step 0: Load Profile

Read `./oss-pilot-data/profiles/<repo>.md` to get repo, fork, username, local_path. Also read any "Repo-Specific Rules" and "Lessons Learned" sections -- these are hard-won knowledge from previous contributions. Profile schema: see `./oss-pilot-data/profiles/_template.md` for expected sections.

**Cold start**: If the profile doesn't exist, this is a new repo. Copy `./oss-pilot-data/profiles/_template.md` to `./oss-pilot-data/profiles/<repo>.md`, fill in the 4 required fields (repo, fork, username, local_path), and ask the user to confirm before proceeding.

## Context File Format

Every PR gets a context file at `./oss-pilot-data/context/pr-<repo-short>-<NUMBER>.md`.

**Principle: GitHub is source of truth for live state. Context files only store our reasoning and decisions.**

```markdown
---
repo: <owner/repo>
pr: <PR number>
issue: <Issue number>
branch: <branch name>
linked_issues: <comma-separated>
---

## Approach
<Why we chose this fix. 2-3 sentences.>

## Decisions
- [declined] <bot> <concern>: <why>
- [accepted] <bot> <concern>: <what changed>

## Outcome
<!-- added by oss-check retrospective when PR is merged/closed -->
- **Result**: merged / closed (reason)
- **Reviewed by**: @who -- what they cared about
- **What worked**: ...
- **What surprised us**: ...
- **Lesson**: ...
```

## Phase 1: Issue Selection (skip if issue number provided)

Run /oss-discover for the repo. Present top 3 with honest yes/no answers:

| Question | What it checks |
|---|---|
| **Maintainer cares?** | Filed by maintainer, `help wanted` label, or real user reports |
| **No competition?** | Zero PRs for same issue AND same code area (two-level check) |
| **Small scope?** | <200 lines, <5 files |

Ask user: "Which one? Or 'none' to skip."

## Phase 2: Feasibility Check

1. **Duplicate check -- two levels:**
   - Issue-level: `gh pr list -R <REPO> --search "<issue>" --state open`
   - Code-level: search by function name + context keyword to avoid false positives. Use `"<context> <function>"` not just `"<function>"` alone. Example: `"Anthropic sanitizeToolCallIds"` not just `"sanitizeToolCallIds"` (the latter returns 29 unrelated PRs about other providers).
   - If >2 competing PRs **actually targeting the same fix** --> **stop**. Skim titles/descriptions to filter noise.
2. Active PR count -- check profile for max (default: no limit)
3. Code-level verification -- does the bug still exist on main?
4. Cross-reference discovery -- related issues to link?

If any check fails, report and stop.

## Phase 3: Implement

1. Auto-detect default branch: `DEFAULT_BRANCH=$(gh repo view <REPO> --json defaultBranchRef --jq .defaultBranchRef.name)`
   `cd <LOCAL_PATH> && git fetch <UPSTREAM_REMOTE> $DEFAULT_BRANCH && git checkout -b fix/<branch> <UPSTREAM_REMOTE>/$DEFAULT_BRANCH`
   **Use `upstream_remote` from the profile** -- not hardcoded `upstream` or `origin`. The local clone may have multiple remotes; only the profile's `upstream_remote` is guaranteed to point to the real upstream repo.
2. Read the relevant code. Understand before changing. Also read `CLAUDE.md`, `CONTRIBUTING.md`, and `.github/CONTRIBUTING.md` if they exist -- these contain repo-specific conventions (commit format, required checks, formatting tools) that override defaults.
3. **Root cause analysis** (follow /oss-pr Phase 2): Is the fix at the right layer? Trace call chain 3-5 levels. Check blast radius across all callers. Verify it preserves existing contracts.
   - **Caller vs callee**: In high-competition issues, prefer fixing callers over callees. A callee fix is fragile -- someone else can fix all callers and make your callee fix redundant. A caller fix is self-contained and harder to supersede.
4. **Scope checkpoint** (MANDATORY): After reading the code and identifying the fix, if it requires >5 files or >200 lines --> **stop and ask the user** whether to continue. Do NOT silently commit to a large change. This prevents wasted effort on PRs that will be labeled `dirty` or rejected for scope creep.
5. **Auto-detect build tooling:**
   - If `package.json` exists --> detect package manager from lock file (pnpm-lock.yaml --> pnpm, yarn.lock --> yarn, package-lock.json --> npm), then read scripts
   - If `Cargo.toml` exists --> `cargo fmt`, `cargo clippy`, `cargo test`
   - If `go.mod` exists --> `go fmt`, `go vet`, `go test`
   - If `Makefile` exists --> check for `make lint`, `make test`
   - Check profile "Repo-Specific Rules" for overrides (e.g., custom commit scripts)
6. Write the minimal fix. Follow profile "Architecture Patterns" if present.
7. Write or update tests.
8. Run detected format + lint + test commands.
9. **Generated files check**: Read the profile's "Repo-Specific Rules" for generated file commands (e.g., schema generation, config docs). If any config or schema files were changed, run the relevant commands and commit generated output SEPARATELY from the feature commit. Failing to regenerate is a common CI failure after rebase.
10. Commit (use repo's commit script if specified in profile, else standard git commit).
11. Push to fork remote.

## Phase 4: Open PR

1. Follow /oss-pr Phase 5 for PR description -- auto-detect template, include "What did NOT change" and "What I Did NOT Verify" sections.
2. Auto-detect default branch: `DEFAULT_BRANCH=$(gh repo view <REPO> --json defaultBranchRef --jq .defaultBranchRef.name)`
3. `gh pr create -R <REPO> --head <FORK>:<BRANCH> --base $DEFAULT_BRANCH`

## Phase 5: Save Context

Write context file. Only store approach and decisions.

## Phase 6: First Review Cycle

Wait 5 minutes, then check once. If no bot reviews yet, proceed to Phase 7 -- /oss-check handles them in the next session.

Follow /oss-pr Phase 6 for bot response strategy:
- Every comment MUST be responded to. Reply format: `Addressed in [hash]. What changed: [1 sentence]. Validation: <test> is green.`
- Accept real bugs --> fix, push, reply with commit hash
- Decline with evidence --> explain WHY, not just disagree
- Repeat concern --> progressively shorter replies referencing prior answer

## Phase 6.5: Mark Ready for Review

After Phase 6 (bot comments addressed) and before pinging:
- If PR was created as draft --> `gh pr ready <NUMBER> -R <REPO>`
- Fork PRs often need maintainer to trigger CI -- marking ready makes the PR visible to maintainers
- Do NOT leave PRs in draft indefinitely -- draft PRs are invisible to reviewers

## Phase 7: Ping Maintainer

When ready (CI fully green + all bot comments answered + description-diff alignment verified):
1. `cat CODEOWNERS 2>/dev/null` -- if exists, skip manual ping
2. If no CODEOWNERS: `git log --since="30 days ago" --format="%an" -- <changed-files> | sort | uniq -c | sort -rn | head -1`
3. Post: `@maintainer -- [problem] -> [fix]. [N] files, +X/-Y. Closes #XXXX.`

## Phase 8: Report

```
+===========================================================+
|            OSS Auto PR Complete: <repo>                   |
+===========================================================+
| Issue:       #XXXXX                                       |
| PR:          #YYYYY                                       |
| CI:          green / N upstream fails                     |
| Bot comments: N addressed                                 |
| Pinged:      @maintainer                                  |
+===========================================================+
| Next: run /oss-check tomorrow                             |
+===========================================================+
```

## Error Handling

- Implementation fails after 3 attempts --> stop, report
- CI upstream failures --> post triage, continue
- Bot P1 we can't resolve --> stop, report to user
- PR limit exceeded --> hard stop
