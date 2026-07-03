---
name: parallel-code-review
description: >
  Use when reviewing PRs, diffs, or completed work—covers both runtime bugs (resource leaks, edge cases, race conditions) and architecture concerns (design alignment, API contracts, consistency). Triggers when user says "review", "code review", "PR review", "审查", or after completing a feature. NOT for linter-only checks or quick syntax scans.
---

# Reviewing Code

Three-phase review that catches orthogonal bug classes: **runtime failures** most reviewers miss (resource leaks, null paths, idempotency gaps) AND **architecture drift** terse reviews skip (interface contract violations, subclass obligations, design-plan mismatches).

## When to Use

After completing a feature, before merge, or on any diff. Not for linting, formatting, or type-checking—those are tool jobs.

## Output Structure

Every review produces exactly four sections, in this order:

```
## Overview
[2-3 sentences: what changed, design alignment, overall quality signal]

## Issues
[One line per finding. Format: <file>:L<line>: <severity> <problem>. <fix>.
 No throat-clearing, no restating what the line does.]

## Recommendations
[0-3 actionable next steps—only if non-obvious]

## Verdict
**Ready to merge?** [Yes | With fixes | No]
**Why:** [one sentence]
```

### Severity Prefixes

| Prefix | Meaning | Examples |
|--------|---------|----------|
| `🔴 bug:` | Broken—will cause incident | null deref, zombie state, data loss |
| `🟡 risk:` | Works but fragile | missing guard, race window, swallowed error |
| `⚠️ arch:` | Design/API contract violation | interface breach, subclass contract mismatch, wiring inconsistency |
| `🔵 nit:` | Style/naming/duplicate, optional | dead code, old class name, unused import |
| `❓ q:` | Genuine question, not a suggestion | "Why is this check inverted?" |

## Determining Review Scope

**Default: review the current branch.** When no range is specified, review all commits on the current branch that are not yet on its upstream tracking branch.

Before starting, resolve what to review:

1. **User provided explicit range** → use as-is (e.g. `"review origin/main..HEAD"`)
2. **No range specified** → review current branch by default:
   ```bash
   UPSTREAM=$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null)
   if [ -n "$UPSTREAM" ]; then
     BASE=$(echo "$UPSTREAM" | sed 's|/|/|')  # origin/main
     git diff --stat "$UPSTREAM..HEAD"
   else
     # No upstream — fall back to origin/main or ask user
     git diff --stat origin/main..HEAD 2>/dev/null || echo "No range found, ask user"
   fi
   ```
   If the branch has no new commits vs upstream → fall back to staged/unstaged diffs:
   - `git diff --cached` (staged)
   - `git diff` (unstaged)
   - if all empty → ask: "No changes to review. Specify a range?"
3. Always report the resolved range in Overview so the user can confirm.

## Three-Phase Process

### Phase 1: Rapid Scan (read diff surface → Overview)

Read the diff summary for the resolved range, scan key files. Form an opinion on:
- **What actually changed** vs what was planned
- **Design alignment**: do class hierarchies make sense? does DI flow consistently?
- Any obvious red flags from the diff alone

Output: the Overview section. This is the ONLY place for praise or narrative summary.

### Phase 2: Deep Issues — Parallel Lenses

**MUST dispatch two subagents in parallel.** Lens A and Lens B are orthogonal and share no state. Sequential execution doubles wall-clock time for no gain.

#### Subagent A — Runtime Safety (caveman lens)

Dispatch a subagent with this focus checklist:
- Resource lifecycle: acquire/release, open/close, connect/disconnect patterns—any leak?
- Null/empty paths: what happens when input is null, empty, zero-length, or oversized?
- Idempotency: is setup/init/start safe to call twice? does a partial failure leave unrecoverable state?
- Lock discipline: are locks/semaphores held during blocking operations?
- Exception paths: does a throw in one cleanup path starve others?
- Behavior changes: silently removed constraints, changed defaults, altered semantics

Output format for this subagent: one line per finding. `<file>:L<line>: 🔴/🟡/🔵/❓ <problem>. <fix>.`

#### Subagent B — Architecture Consistency (design lens)

Dispatch a subagent with this focus checklist:
- Subclass obligations: override/implementation annotations, interface contract correctness
- Static vs instance method contracts: are abstract signatures consistent with implementations?
- Configuration access: string-keyed vs typed—any key typos or default-value dead code?
- Dependency wiring: consistent injection patterns across all entry points (routers, controllers, handlers)
- Plan/design doc deviations (if design docs exist)
- Naming consistency, dead code, merge conflict residues

Output format for this subagent: one line per finding. `<file>:L<line>: ⚠️/🔵 <problem>. <fix>.`

Both subagents run **read-only**—never mutate the working tree. Use `git diff`, `git show`, `read`.

After both return, deduplicate and merge into a single Issues list sorted by severity (🔴 → 🟡 → ⚠️ → 🔵 → ❓). For each finding, write ONE terse line. If a finding needs more than 3 lines to explain (security vulns, architectural disagreements), write a full paragraph then resume terse.

### Phase 3: Synthesis → Recommendations + Verdict

Merge Phase 1+2 into a forward-looking assessment. Recommendations are tactical next steps, not vague "improve X."

## Calibration

**Every issue gets exactly one severity.** If unsure between two, pick the higher.

**🔴 bug is rare.** Reserved for things that will break in production. Not for "this could be better."

**⚠️ arch is for design contracts, not opinions.** Interface contract violation = arch. "I'd use a different pattern" = not an issue.

**🔵 nit can be skipped entirely** if the review is already long. Prioritize 🔴 and 🟡.

## Boundaries

Reviews only. Does not write fixes, does not approve/request-changes in GitHub, does not run linters. Does not discuss testing strategy unless there's a clear coverage gap tied to a bug.

## Red Flags (Self-Check)

- "I noticed that..." → delete, write the finding directly
- "You might want to consider..." → delete, pick a severity and state the fix
- Restating what a line does → delete, the reviewer can read the diff
- "Great work!" in the Issues section → move to Overview or delete
- More than 3 🔵 nits in a small diff → stop nitpicking
- No 🔴 or 🟡 findings → re-scan with Lens A before concluding
