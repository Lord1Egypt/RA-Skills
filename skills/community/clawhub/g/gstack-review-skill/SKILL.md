---
name: gstack-review
version: 1.0.0
description: |
  Garry Tan's gstack-inspired multi-perspective code review for OpenClaw.
  Triggered when user asks to review code, run /review, review a PR/branch/changes,
  or wants a thorough code review with business, engineering, and QA perspectives.
  Analyzes git diffs, runs tests, checks code quality, and provides actionable feedback
  from three viewpoints: CEO (product value), Engineering (architecture), QA (correctness).
---

# gstack-review: Multi-Perspective Code Review

## Review Framework

When asked to review code, follow this three-perspective framework. Run all steps systematically.

### Step 0: Detect What to Review

**Priority order for review scope:**
1. Uncommitted changes (`git diff HEAD`) — if working directory is dirty
2. Specific files mentioned by user
3. Branch diff vs main — if on a feature branch
4. Recent commits — if no clear scope

```bash
# Check working tree status
git status --short

# Get uncommitted changes
git diff HEAD

# Get committed changes on current branch vs origin/main
BRANCH=$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD 2>/dev/null)
MAIN_BRANCH=$(git main-branch 2>/dev/null || echo "main")
git log ${MAIN_BRANCH}..${BRANCH} --oneline 2>/dev/null | head -20
git diff ${MAIN_BRANCH}..${BRANCH} 2>/dev/null | head -500

# List changed files
git diff --name-only ${MAIN_BRANCH}..${BRANCH} 2>/dev/null
```

### Step 1: Gather Context

Before reviewing, collect:

```bash
# Project type and language
ls *.json *.toml *.yaml *.gradle *.xml Makefile package.json 2>/dev/null | head -5
cat package.json 2>/dev/null | grep '"name"\|"scripts"' | head -5

# Run tests (silently, capture exit code)
TEST_OUTPUT=$(npm test 2>&1 || pytest 2>&1 || cargo test 2>&1 || true)
TEST_EXIT=$?

# Type check / lint
LINT_OUTPUT=$(npm run lint 2>&1 || npx tsc --noEmit 2>&1 || true)

# Build check
BUILD_OUTPUT=$(npm run build 2>&1 || cargo build 2>&1 || true)
BUILD_EXIT=$?
```

### Step 2: Read Changed Files

For each changed file, read the full content to understand context. Don't just look at the diff — read the surrounding code.

```
For each file in the diff:
  1. Read the full file (not just changed lines — context matters)
  2. Identify what the code actually does vs. what the diff claims
  3. Note any files that are only binary/generated (skip detailed review)
```

### Step 3: CEO / Product Perspective

**Ask: Does this code serve the business and users?**

Review from a product-thinking perspective:
- **Correctness**: Does this actually solve the stated problem?
- **Complexity**: Is this 10x simpler than the previous approach? Or did we add an abstraction layer that solves nothing?
- **Product signal**: Is this a feature users asked for, or engineer-invented complexity?
- **Scope creep**: Did the diff grow beyond its original purpose?
- **Tech vs business**: Is this engineering for its own sake, or does it genuinely ship value?

**Key question:** "If I had to explain this change to the CEO in 30 seconds, would they be excited or confused?"

### Step 4: Engineering Perspective

**Ask: Is this code sound, maintainable, and safe?**

- **Architecture**: Does this fit the existing patterns? Or did we invent a new framework within a framework?
- **Error handling**: Are all failure modes handled? (network, disk, invalid input, timeouts)
- **Resource management**: Connections closed? Memory leaked? Background tasks cancelled?
- **Dependencies**: Did we add a new heavy dependency when a stdlib call would suffice?
- **Security**: SQL injection, XSS, auth bypass, secrets in code, overly permissive CORS?
- **Performance**: N+1 queries? Unindexed queries in loops? Memory-allocating operations in hot paths?
- **API design**: Are interfaces clean and composable, or did we leak internal state?

**Code quality signals:**
- Functions under 30 lines? Exceptions are allowed but need strong justification.
- Meaningful variable/function names? No `temp2_final_v3` patterns.
- Comments that explain *why*, not *what*? (the code shows *what*)
- Tests that test behavior, not implementation?

### Step 5: QA / Testing Perspective

**Ask: Would this pass a senior engineer's gut check for correctness?**

- **Test coverage**: Are the changed paths actually tested? Not just "tested" but *validated*?
- **Edge cases**: Empty input, max length, null bytes, unicode edge cases, concurrent access
- **Happy path**: Does the main user flow actually work end-to-end?
- **Failure modes**: What breaks when this code is wrong? Can a user detect it?
- **Smoke tests**: Does it at least import/parse/load without crashing?
- **Test quality**: Are tests asserting on behavior or mocking everything and asserting on internals?

### Step 6: Assemble the Review

Present a structured review with three clearly labeled sections.

---

## Review Output Template

```
# Code Review: [BRANCH_NAME] — [DATE]
═══════════════════════════════════════════════

## Summary
[One paragraph: what changed and why. If this were a commit message, is it a good one?]

**Files changed:** N files | **Lines:** +N -N
**Tests:** [PASS/FAIL/NONE] | **Build:** [PASS/FAIL/NONE] | **Lint:** [PASS/FAIL/NONE]

---

## 🏛️ CEO / Product Review
[Bulleted findings. Flag concerns in 🔴, praise good decisions in ✅]

**Verdict:** [Clear statement — ship it, rework it, or discuss with the team]

---

## ⚙️ Engineering Review
[Bulleted findings. Group by category: Architecture, Security, Performance, Code Quality]

**Verdict:** [Clear statement]

---

## 🧪 QA / Testing Review
[Bulleted findings. Group by: Coverage, Edge Cases, Correctness]

**Verdict:** [Clear statement]

---

## Action Items
- [ ] [Priority] [Specific actionable item — who should fix it and how]
- [ ] [Priority] ...

**Overall:** ✅ APPROVED TO SHIP / ⚠️ REVISIONS NEEDED / ❌ BLOCKED
═══════════════════════════════════════════════
```

---

## Review Principles

1. **Be direct.** Don't hedge. "This is wrong" is more useful than "this might be worth considering."
2. **Distinguish severity.** A missing test on a utility function ≠ a SQL injection vulnerability.
3. **Context matters.** Code that looks wrong in isolation might be the right solution for the system.
4. ** Praise good work.** If the code is clean, simple, and well-tested, say so. Reinforce the pattern.
5. **Actionable over academic.** "Consider using a WeakMap" is less useful than "Replace `new Map()` with `new WeakMap()` on line 42 to avoid memory leaks in the closure."
6. **No bikeshedding.** Don't flag style preferences that a linter wouldn't flag. Focus on what matters.

---

## When to Escalate (Don't Review Alone)

Escalate to human review for:
- 🔴 Security vulnerabilities (auth bypass, injection, data exposure)
- 🔴 Breaking changes to external APIs or database schemas
- 🔴 Complex concurrency or distributed systems changes without expert review
- 🔴 Changes to payment, billing, or access control logic
- 🔴 Anything that would require a rollback plan

---

*Inspired by Garry Tan's gstack (github.com/garrytan/gstack) — ported for OpenClaw.*
