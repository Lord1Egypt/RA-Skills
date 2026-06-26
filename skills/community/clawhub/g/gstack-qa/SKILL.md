---
name: qa
description: |
  Systematically QA test a web application and fix bugs found. Runs QA testing,
  then iteratively fixes bugs in source code, committing each fix atomically and
  re-verifying. Use when asked to "qa", "test this site", "find bugs",
  "test and fix", or "fix what's broken".
  Proactively suggest when the user says a feature is ready for testing
  or asks "does this work?".
  Three tiers: Quick (critical/high only), Standard (+ medium), Exhaustive (+ cosmetic).
  Produces before/after health scores, fix evidence, and a ship-readiness summary.
---

## AskUserQuestion Format

When asking the user a question, format as a structured text block for the message tool:

1. **Re-ground:** State the project, current branch, and the task.
2. **Simplify:** Plain English. Concrete examples. Say what it DOES.
3. **Recommend:** `RECOMMENDATION: Choose [X]`. Include `Completeness: X/10`.
4. **Options:** `A) ... B) ... C) ...`

## Completeness Principle — Boil the Lake

AI-assisted coding makes marginal cost of completeness near-zero. Always prefer the complete option.

## Completion Status Protocol
- **DONE** — All steps completed.
- **DONE_WITH_CONCERNS** — Completed with issues.
- **BLOCKED** — Cannot proceed.
- **NEEDS_CONTEXT** — Missing info.

---

# QA: Test → Fix → Verify

You are a QA engineer AND a bug-fix engineer. Test web applications like a real user — click everything, fill every form, check every state. When you find bugs, fix them in source code with atomic commits, then re-verify.

## Setup

**Parse parameters:**

| Parameter | Default | Notes |
|-----------|---------|-------|
| Target URL | auto-detect or required | |
| Tier | Standard | `--quick`, `--standard`, `--exhaustive` |
| Output dir | `.qa-reports/` | |
| Scope | Full app or diff-scoped | |
| Auth | None | credentials or cookie file |

**Tiers:**
- **Quick:** Fix critical + high severity only
- **Standard:** + medium severity
- **Exhaustive:** + low/cosmetic severity

**If no URL given and on a feature branch:** Enter **diff-aware mode** — analyze branch diff, test affected pages/routes.

**Clean working tree check:**
```bash
git status --porcelain
```
If dirty: **send via message tool:**
> "Your working tree has uncommitted changes. /qa needs a clean tree so each bug fix gets its own atomic commit."
- A) Commit my changes — commit all with a descriptive message, then start QA
- B) Stash my changes — stash, run QA, pop the stash after
- C) Abort — I'll clean up manually

---

## Modes

### Diff-aware (automatic when on feature branch with no URL)
1. Analyze branch diff to understand what changed:
   ```bash
   git diff main...HEAD --name-only
   git log main..HEAD --oneline
   ```
2. Identify affected pages/routes from changed files.
3. Detect running app on common local ports.
4. Test each affected page/route: navigate, screenshot, console errors, interactions.
5. Report findings scoped to branch changes.

### Full (default when URL provided)
Systematic exploration. Visit every reachable page. Document 5-10 well-evidenced issues. Takes 5-15 min.

### Quick (`--quick`)
30-second smoke test. Homepage + top 5 navigation targets. Check: loads? Console errors? Broken links?

### Regression (`--regression <baseline>`)
Run full mode, diff against baseline.json, report delta.

---

## Workflow

### Phase 1: Initialize
1. Create output directories: `.qa-reports/screenshots/`
2. Start timer.

### Phase 2: Authenticate (if needed)
**If user specified credentials:**
Use browser tool to:
1. Navigate to login URL
2. Find and fill username field
3. Fill password field (never include real passwords — use `[REDACTED]`)
4. Submit
5. Verify login succeeded

**If 2FA/OTP required:** Ask user for code.
**If CAPTCHA blocks:** Tell user to complete CAPTCHA in browser, then continue.

### Phase 3: Orient
```bash
browser goto <target-url>
browser snapshot
browser screenshot
```
Detect framework (note in report): `__next` → Next.js, `csrf-token` → Rails, `wp-content` → WordPress.

### Phase 4: Explore
Visit pages systematically. At each page:
```
browser goto <page-url>
browser snapshot
browser screenshot
browser console --errors
```

Per-page checklist:
1. **Visual scan** — layout issues
2. **Interactive elements** — do buttons/links work?
3. **Forms** — fill and submit. Test empty, invalid, edge cases.
4. **Navigation** — all paths in and out
5. **States** — empty state, loading, error, overflow
6. **Console** — JS errors after interactions
7. **Responsiveness** — mobile viewport (375x812)

**Quick mode:** Only homepage + top 5 nav targets. Just: loads? Console errors? Broken links?

### Phase 5: Document
Document each issue immediately when found.

**Interactive bugs:**
1. Screenshot before action
2. Perform action
3. Screenshot showing result
4. Write repro steps referencing screenshots

**Static bugs:**
1. Annotated screenshot showing the problem
2. Description of what's wrong

### Phase 6: Wrap Up
1. **Compute health score** (see rubric below)
2. **Write "Top 3 Things to Fix"**
3. **Console health summary**
4. **Fill in report metadata**

---

## Health Score Rubric

### Per-category (0-100 each):
- **Console (15%):** 0 errors → 100, 1-3 → 70, 4-10 → 40, 10+ → 10
- **Links (10%):** 0 broken → 100, each broken → -15 (min 0)
- **Visual (10%):** 100 - (critical×25 + high×15 + medium×8 + low×3)
- **Functional (20%):** same deduction scale
- **UX (15%):** same deduction scale
- **Content (5%):** same deduction scale
- **Accessibility (15%):** same deduction scale

### Final: weighted average of all categories.

---

## Phase 7: Triage
Sort by severity. Fix based on tier:
- **Quick:** Fix critical + high only
- **Standard:** + medium
- **Exhaustive:** Fix all

Mark unfixable issues (third-party, infrastructure) as "deferred" regardless of tier.

---

## Phase 8: Fix Loop
For each fixable issue, in severity order:

### 8a. Locate source
```bash
grep -r "<error-message-or-component-name>" --include="*.js" --include="*.ts" --include="*.rb" --include="*.py" .
glob: **/*.jsx, **/*.tsx, **/*.vue
```

### 8b. Fix
Read source. Make **minimal fix** — smallest change resolving the issue. Do NOT refactor or expand.

### 8c. Commit
```bash
git add <only-changed-files>
git commit -m "fix(qa): ISSUE-NNN — short description"
```

### 8d. Re-test
```bash
browser goto <affected-url>
browser screenshot
browser console --errors
```

### 8e. Classification
- **verified:** re-test confirms fix works, no new errors
- **best-effort:** fix applied but couldn't fully verify
- **reverted:** regression detected → `git revert HEAD` → mark as deferred

---

## Phase 9: Final QA
1. Re-run QA on all affected pages
2. Compute final health score
3. If final score WORSE than baseline: WARN prominently

---

## Phase 10: Report
Write report to `.qa-reports/qa-report-{domain}-{YYYY-MM-DD}.md`.

Include:
- Health score: baseline → final
- Total issues found
- Fixes applied: verified X, best-effort Y, reverted Z
- Deferred issues
- Per-issue: status, commit SHA, files changed, before/after screenshots

---

## Important Rules
1. **Repro is everything.** Every issue needs at least one screenshot.
2. **Verify before documenting.** Retry once to confirm reproducible.
3. **Never include credentials.** Use `[REDACTED]` for passwords.
4. **Write incrementally.** Append each issue to report as found.
5. **Never read source code during QA.** Test as user, not developer.
6. **Check console after every interaction.**
7. **Test like a user.** Use realistic data. Walk complete workflows end-to-end.
8. **Depth over breadth.** 5-10 well-documented issues > 20 vague descriptions.
9. **Never delete output files.**
10. **Never refuse to use the browser.** Backend changes affect app behavior — always open the browser and test.
