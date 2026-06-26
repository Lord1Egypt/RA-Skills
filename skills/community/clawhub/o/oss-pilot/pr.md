---
name: oss-pr
description: PR preparation and review for any open-source repo. Validates quality,
  checks for duplicates, generates PR description. Triggers on "oss pr", "review PR",
  "prepare PR", "check PR quality", "openclaw PR".
user_invocable: true
---

# OSS PR Preparation & Review

Validate PR quality and maximize merge probability. Works on any repo with a profile.

## Invocation

- `oss-pr review <repo> #XXXXX` -- review a PR

## Step 0: Load Profile

Read `./oss-pilot-data/profiles/<repo>.md` thoroughly. Profile schema: see `./oss-pilot-data/profiles/_template.md` for expected sections. In particular:
- **Repo-Specific Rules** -- mandatory constraints (commit scripts, PR limits, generated files)
- **Architecture Patterns** -- these encode maintainer preferences that are the #1 reason PRs get rejected. Do not skip.
- **Maintainer Review Styles** -- if present, tells you what each reviewer cares about
- **Bot Behavior** -- if present, repo-specific bot names, severity levels, blocking vs informational

## Phase 1: Feasibility Check

1. **Duplicate check (three-level):**
   - Issue-level (open): `gh pr list -R <REPO> --search "<issue>" --state open`
   - Issue-level (merged): `gh pr list -R <REPO> --search "<issue>" --state merged --limit 5` -- if a fix was already merged, our PR is a duplicate. Also search by keywords: `gh pr list -R <REPO> --search "<keywords>" --state merged --limit 5`
   - Code-level (open): `gh pr list -R <REPO> --search "<context> <function>" --state open` -- use context keyword + function name to avoid false positives. Skim titles to filter noise.
   - If >2 competing open PRs actually targeting the same fix --> warn
   - If a merged PR already fixes the same issue --> **stop**. Do not open a duplicate.
   - **Prior art**: If earlier PRs exist for the same issue, acknowledge them in your PR description. Maintainers flag contributors who ignore prior work.
2. **Active PR count**: Check profile for max limit
3. **Branch cleanliness**: No unrelated files staged -- no AI session logs, debug artifacts, `.env` files, PII, or unrelated commits from bad merge/rebase. Some repos auto-close dirty branches.

## Phase 2: Root Cause Analysis (CRITICAL -- #1 rejection reason)

Before writing code, answer these questions:

1. **"Is this fix at the right layer?"** -- Trace the call chain 3-5 levels deep. Does the fix address WHERE the problem originates, or WHERE it surfaces? A fix at the wrong layer will be rejected even if it passes tests.

2. **"Does this change affect code paths beyond the stated scope?"** (Blast radius) -- If you're changing a shared function, check all callers. A fix that's correct for one path but breaks another will be caught in review.

3. **"Does this preserve existing semantic contracts?"** -- Data structure invariants, lifecycle guarantees, API response shapes. Breaking a contract that downstream code relies on is worse than the original bug.

4. **Cross-boundary tracing** -- For fixes where data crosses boundaries (UI --> API, config --> runtime, external input --> internal state), trace BOTH sides:
   - **Producer**: How does the server handler set, parse, and return the fields?
   - **Wire format**: What exact shape does the data have at the API boundary? Check type definitions.
   - **Consumer**: How does the UI/client transform the data? Trace all callers of the function being fixed.
   Only by tracing both sides can you find the right fix point. A guard like `includes("/")` may seem correct at the consumer, but can fail when "/" is part of a vendor prefix rather than a separator -- only tracing producer --> wire --> consumer reveals the correct fix (e.g., `startsWith(provider + "/")` instead).

If the profile has "Architecture Patterns" -- read and follow them.

### Common Mistake Patterns (learn to recognize by sight)

These are universal failure modes that get PRs rejected -- regardless of repo:

**Wrong root cause:**
- Mistaking log noise for a crash --> disabling a feature to "fix" startup failure, when the real issue is verbose retry logging
- Adding a cache TTL to fix stale data --> when the real problem is cache-key divergence across multiple code paths
- Adding a guard at the consumer --> when the producer's wire format makes the guard's assumption invalid (e.g., a "/" in a vendor-prefixed ID is data, not a separator)

**Unintended blast radius:**
- Setting `rejectUnauthorized = false` for one case --> but it silently disables cert validation for ALL connections of that type
- Fixing a shared function for your use case --> but breaking another caller's invariant (buffer lifecycle, compaction boundary, queue semantics)

**Anti-patterns in the diff:**
- Multiple boolean flags tracking related state --> should be a single enum or ordered array
- Nested try/catch with duplicated recovery --> should be a data-driven loop over an attempts array
- Adding new exports for each variant --> should extend existing types with optional fields
- Separate code paths for similar operations --> should be a unified chain
- Hardcoded values that belong in config/constants
- Adding special-case `if` branches --> should extend existing data structures
- Channel/module-specific fix where a shared fix is possible --> fix the root cause in shared infrastructure

## Phase 3: Diff Analysis

```bash
DEFAULT_BRANCH=$(gh repo view <REPO> --json defaultBranchRef --jq .defaultBranchRef.name)
git diff --stat upstream/$DEFAULT_BRANCH...HEAD
```

- XS: <50 lines --> ideal
- S: 50-200 --> good
- M: 200-500 --> warn "consider splitting"
- L: >500 --> fail "split this PR"

Scope check: all changed files in one domain? Mixing feature + refactor + fix --> warn "one concern per PR."

## Phase 4: Build & Test

**Auto-detect tooling from repo:**
- `package.json` --> read scripts for format, lint, test commands. Check for lock file to determine package manager (pnpm-lock.yaml --> pnpm, yarn.lock --> yarn, package-lock.json --> npm).
- `Cargo.toml` --> `cargo fmt && cargo clippy && cargo test`
- `go.mod` --> `go fmt && go vet && go test ./...`
- `Makefile` --> `make lint && make test`
- Profile overrides take precedence (e.g., custom commit scripts)

Run: format --> lint --> type-check --> test (in that order).

### Live Verification (when available)

Beyond static tests, consider whether runtime verification is available for the repo:
- **Browser automation** (Playwright, Cypress, Selenium) -- verify UI rendering, form behavior, live data display
- **Local dev server** -- verify config changes take effect, API responses are correct
- **REPL/CLI testing** -- for CLI tools, run the actual command and capture output

Check the profile's "Live Verification" section for repo-specific tools and URLs. Capture runtime evidence for the PR description's "Evidence" section -- visual proof dramatically increases merge probability, especially for UI changes.

## Phase 5: PR Description

### Step 1: Fetch the repo's PR template (MANDATORY)

```bash
gh api repos/<REPO>/contents/.github/pull_request_template.md -H "Accept: application/vnd.github.raw+json" 2>/dev/null
```

If the command succeeds --> use that template verbatim as the skeleton. Fill in **every section** -- do not skip sections, do not collapse them, do not reorder them. If a section is not applicable, write `N/A` rather than omitting it.

If the command fails (404 / permissions) --> try the local clone:
```bash
cat <LOCAL_PATH>/.github/pull_request_template.md 2>/dev/null
```

**Only if both fail** --> learn the format from the repo's own merged PRs (Step 1b).

### Step 1b: Learn format from merged PRs (ONLY when no template)

When the repo has no PR template, do NOT immediately use the fallback. Instead, learn what format this repo actually uses:

```bash
# 1. Read the 5 most recently merged PRs
for PR in $(gh pr list -R <REPO> --state merged --limit 5 --json number --jq '.[].number'); do
  echo "=== PR #$PR ==="
  gh pr view $PR -R <REPO> --json body --jq '.body[:500]'
done
```

Extract the common pattern: which sections appear? What level of detail? Checkboxes or free text? Formal or informal?

If the recent 5 PRs don't include a PR similar to yours (e.g., yours is a bug fix but all 5 are features), search for similar changes:

```bash
# 2. Find 3 merged PRs with similar change type or area
gh pr list -R <REPO> --state merged --search "<change-type> <area-keyword>" --limit 3 --json number --jq '.[].number'
# Read their bodies the same way
```

**Use the observed pattern as your skeleton.** Match the section structure, heading style, and level of detail from the merged PRs. If merged PRs are minimal (just a summary + test output), write a minimal description. If they use structured sections, match that structure.

**Fall back to the fallback template below only if**: the repo has <5 merged PRs total, or the merged PR descriptions are empty/one-liners with no discernible pattern.

### Step 2: Fill the template

Whether using the repo template, a learned pattern, or the fallback, follow these rules:

- **Use the exact section headings, checkbox formats, and ordering from the template.** Do not rename sections, merge sections, or use free text where checkboxes are expected.
- **"What did NOT change"** is the most important content. Maintainers check scope boundaries first.
- **"What I Did NOT Verify"** -- be honest about gaps. Listing unverified scenarios is valued, not penalized.
- Include actual test output as evidence, not just claims.
- For bug fixes: fill Root Cause with sub-bullets (root cause, missing guardrail, prior context, why now) and Regression Test Plan (coverage level, target test, scenario, why smallest guardrail).
- For all PRs: fill Repro + Verification with environment details and numbered steps (adapt from the linked issue if available).

### Fallback template (ONLY when repo has no template)

```markdown
## Summary
- **Problem**: [what's broken and who it affects]
- **Why it matters**: [impact]
- **What changed**: [2-3 bullets]
- **What did NOT change** (scope boundary): [explicit boundaries]

## Change Type
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Refactor (no behavior change)

Closes #XXXX

## Security Impact
- New permissions requested: [none / list]
- Secrets handling changes: [none / describe]
- New network calls: [none / describe]
- Data access changes: [none / describe]

## Verification
- [x] [specific test scenario with actual steps]
- [x] [edge case tested]

## Evidence
[Paste actual test output, not just "tests pass"]

## What I Did NOT Verify
[Be honest. Maintainers value transparency over false confidence.]
- [e.g., "Not verified: live API call with real credentials"]

## Failure Recovery
If this breaks in production:
- **Detection**: [how you'd notice]
- **Rollback**: [steps to revert]
- **Blast radius**: [what's affected]
```

**Description-Diff alignment check (CRITICAL for iterated PRs):**
**This is a formal gate.** Do NOT request human review until description-diff alignment is verified. Stale descriptions are the most common mistake after iterating on bot feedback.

After multiple rounds of bot feedback and code changes, descriptions go stale. Before requesting human review:
1. Function names in description match actual diff?
2. Test counts match?
3. Approach description matches final code, not first draft?
4. "What changed" bullets map to actual changes?

## Phase 6: Bot Response Strategy

Bot usernames auto-detected (login contains `bot` or ends in `[bot]`).

**Every bot comment MUST be responded to before requesting human review.** Unanswered bot comments signal carelessness to maintainers.

**Response format:**
```
Addressed in [commit-hash]. What changed: [1 sentence]. Validation: `<test command>` is green.
```

**When to accept vs decline:**
- **Accept** when: bot found real bug, dead code, missing edge case, or correctness issue. Fix it, push, reply with commit hash.
- **Decline** when: suggestion adds complexity without meaningful regression signal. But you MUST explain why with evidence, not just disagree.

**Handling repeat concerns across pushes:**
Bots re-review on every push and often raise the same concern again.
1. First occurrence --> address substantively
2. Second occurrence --> "This was addressed in the prior reply (see above). [1-sentence restatement]."
3. Third+ occurrence --> "Same concern as above -- see prior replies."

Never ignore even duplicate concerns -- unanswered comments look bad when maintainers scan the thread.

## Phase 7: Who to Ping

```bash
# 1. CODEOWNERS? Don't ping manually -- auto-assignment handles it.
cat CODEOWNERS 2>/dev/null

# 2. No CODEOWNERS? Who touched these files recently?
git log --since="30 days ago" --format="%an" -- <changed-files> | sort | uniq -c | sort -rn | head -1
```

Ping format:
```
@maintainer -- [problem] -> [fix]. [N] files, +X/-Y. Closes #XXXX.
```

Do NOT ping until: all bot comments answered + description-diff alignment verified + one of:
- CI fully green, OR
- CI has upstream-only failures, our area-specific checks pass, and triage comment is posted (see oss-check CI Triage -- [yellow] status means ready to ping)

**Adapting to the reviewer you get:** Don't guess reviewer style in advance. Once someone reviews, read 2-3 of their recent reviews on other PRs to calibrate your responses. Check the profile's "Maintainer Review Styles" section if available.

### When Maintainers Rewrite Your Approach

This is NOT rejection -- it's a compliment. The maintainer values your idea enough to invest time rewriting it. When this happens:
1. The maintainer typically thanks you for the diagnosis/idea
2. Explains why the approach changed (often architectural preference)
3. Pushes the rewrite to same branch or opens a new PR
4. Credits the original contributor

Don't be discouraged. This means your issue selection and root cause analysis were correct -- only the implementation style changed.

## Phase 8: CI Failure Triage

When CI fails for upstream reasons, post a triage comment -- don't just wait silently:
```
CI failure in `<job>` is unrelated to this PR:
- Failed: <test/error description>
- Our changes: exclusively in <area>
- Same failure on main: confirmed ([link or evidence])
- Our area's checks all pass: <list passing checks>

Happy to rebase when main stabilizes.
```

This dramatically increases merge probability -- maintainers see you understand CI and aren't just ignoring red.

## Report

```
+==========================================+
|       OSS PR Readiness: <repo>          |
+==========================================+
| Duplicates:    [none/found]   [pass/fail]
| Root cause:    [right layer]  [pass/warn]
| Size:          [XS/S/M/L]    [pass/warn]
| Scope:         [clean/dirty] [pass/warn]
| Tests:         [pass/fail]
| PR Description: [complete/gaps] [pass/warn]
+==========================================+
| Overall:       [READY / NEEDS WORK]      |
+==========================================+
```
