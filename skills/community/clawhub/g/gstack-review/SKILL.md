---
name: review
description: |
  Pre-landing PR review. Analyzes diff against the base branch for SQL safety, LLM trust
  boundary violations, conditional side effects, and other structural issues. Use when
  asked to "review this PR", "code review", "pre-landing review", or "check my diff".
  Proactively suggest when the user is about to merge or land code changes.
---

## AskUserQuestion Format

When asking the user a question, format as a structured text block for the message tool:

1. **Re-ground:** State the project, current branch, and the current plan/task. (1-2 sentences)
2. **Simplify:** Plain English a smart 16-year-old could follow. Concrete examples. Say what it DOES.
3. **Recommend:** `RECOMMENDATION: Choose [X] because [one-line reason]`. Include `Completeness: X/10`.
4. **Options:** `A) ... B) ... C) ...`

## Completeness Principle — Boil the Lake

AI-assisted coding makes marginal cost of completeness near-zero:
- If Option A is complete and Option B saves modest effort — **always recommend A**.
- Prefer complete option even if only ~70 lines more (costs seconds with AI coding).

## Completion Status Protocol
- **DONE** — All steps completed.
- **DONE_WITH_CONCERNS** — Completed with issues to note.
- **BLOCKED** — Cannot proceed.
- **NEEDS_CONTEXT** — Missing info.

## Step 0: Detect base branch
1. `gh pr view --json baseRefName -q .baseRefName`
2. If no PR: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`
3. Fall back to `main`.

---

# Pre-Landing PR Review

Analyze the current branch's diff against the base branch for structural issues that tests don't catch.

## Step 1: Check branch
1. `git branch --show-current` — if on base branch, output "Nothing to review — you're on the base branch" and stop.
2. `git fetch origin <base> --quiet && git diff origin/<base> --stat` — if no diff, stop.

## Step 1.5: Scope Drift Detection
1. Read TODOS.md (if exists). Read PR description: `gh pr view --json body --jq .body 2>/dev/null || true`. Read commit messages: `git log origin/<base>..HEAD --oneline`.
2. Identify stated intent — what was this branch supposed to accomplish?
3. Run `git diff origin/<base> --stat` and compare files changed against stated intent.

Evaluate:
- **SCOPE CREEP:** Files unrelated to intent, new features not in plan, "while I was in there" changes.
- **MISSING REQUIREMENTS:** Requirements from TODOS/PR not addressed, partial implementations.

Output before main review:
```
Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
Intent: <1-line summary of what was requested>
Delivered: <1-line summary of what diff actually does>
[If drift: list each out-of-scope change]
[If missing: list each unaddressed requirement]
```

## Step 2: Read the checklist
Read `.claude/skills/review/checklist.md`. If cannot be read, STOP and report error.

## Step 3: Get the diff
```bash
git fetch origin <base> --quiet
git diff origin/<base>
```

## Step 4: Two-pass review

Apply checklist in two passes:

1. **Pass 1 (CRITICAL):** SQL & Data Safety, Race Conditions & Concurrency, LLM Output Trust Boundary, Enum & Value Completeness
2. **Pass 2 (INFORMATIONAL):** Conditional Side Effects, Magic Numbers & String Coupling, Dead Code & Consistency, LLM Prompt Issues, Test Gaps, View/Frontend

**Enum & Value Completeness requires reading code OUTSIDE the diff.** When the diff introduces a new enum value, grep all files referencing sibling values, then check if new value is handled.

## Step 4.5: Design Review (conditional)
Check if diff touches frontend files using native shell:
```bash
SCOPE_FRONTEND=false
git fetch origin "<base>" --quiet 2>/dev/null
for ext in ts tsx js jsx vue svelte css scss less sass styl pcss postcss png jpg jpeg gif svg webp ico woff woff2 ttf eot; do
  if git diff origin/"<base>" --name-only 2>/dev/null | grep -qiE "\.${ext}$"; then
    SCOPE_FRONTEND=true
    break
  fi
done
```
**If `SCOPE_FRONTEND=false`:** Skip silently.

**If `SCOPE_FRONTEND=true`:**
1. Read `DESIGN.md` or `design-system.md` if exists.
2. Read `.claude/skills/review/design-checklist.md`. If not found, skip with note.
3. Read each changed frontend file (full file, not just diff hunks).
4. Apply design checklist. Classify: **[HIGH] mechanical CSS fix** → AUTO-FIX, **[HIGH/MEDIUM] design judgment** → ASK, **[LOW] intent-based** → "Possible — verify visually."
5. Include findings in review output under "Design Review" header.
6. Log result for Review Readiness Dashboard.

## Step 5: Fix-First Review

Output: `Pre-Landing Review: N issues (X critical, Y informational)`

### 5a: Classify each finding
AUTO-FIX or ASK per Fix-First Heuristic in checklist.md.

### 5b: Auto-fix all AUTO-FIX items
Apply each fix directly. Output one-line summary per fix:
`[AUTO-FIXED] [file:line] Problem → what you did`

### 5c: Batch-ask about ASK items
If ASK items remain, present in ONE question:
- List each with number, severity label, problem, recommended fix
- Options: A) Fix as recommended B) Skip
- Include overall RECOMMENDATION

If 3 or fewer ASK items, individual questions allowed.

### 5d: Apply user-approved fixes
Output what was fixed. If no ASK items, skip question entirely.

### Verification of claims
- If claiming "this pattern is safe" → cite specific line proving safety
- If claiming "handled elsewhere" → read and cite handling code
- If claiming "tests cover this" → name test file and method
- Never say "likely handled" or "probably tested" — verify or flag as unknown.

## Step 5.5: TODOS cross-reference
Read TODOS.md. Cross-reference PR against open TODOs:
- Does this PR close any open TODOs? Note which.
- Does this PR create work that should become a TODO? Flag as informational.
- Are there related TODOs providing context for this review? Reference them.

## Step 5.6: Documentation staleness check
For each `.md` file in repo root:
1. Check if code changes in diff affect features described in that doc.
2. If doc NOT updated but code it describes WAS changed → INFORMATIONAL: "Documentation may be stale: [file] describes [feature] but code changed in this branch."

## Step 5.7: Codex review (optional)
Check if Codex CLI is available:
```bash
which codex 2>/dev/null && echo "CODEX_AVAILABLE" || echo "CODEX_NOT_AVAILABLE"
```

If `CODEX_NOT_AVAILABLE`: skip silently.

If available, **send via message tool:**
> Codex is an independent code review tool from OpenAI. Want an adversarial challenge of this plan?

Options: A) Yes — let Codex critique the plan B) No — proceed without Codex

If user chooses A, use the `browser` tool to open the plan file and describe the approach. Codex can be invoked via `codex exec` if installed locally.

## Important Rules
- Read the FULL diff before commenting.
- Fix-first, not read-only. AUTO-FIX applied directly. ASK items need user approval.
- Be terse. One line problem, one line fix. No preamble.
- Only flag real problems.
