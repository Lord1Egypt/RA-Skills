# Requesting Code Review — keelwright

This document defines the machine-checkable code review process for keelwright
and for projects that use keelwright's review methodology.

## Review Types

- **R3 review** — mandatory before any commit touches security-gates, circuit-breaker,
  web-guard, import/export, or auth-adjacent code. Reviewer must be a different role
  than the author.
- **Ad-hoc review** — optional for docs, tests, and trivial fixes.

## Findings Taxonomy

| Severity | Meaning | Action |
|----------|---------|--------|
| CRIT | Breaks a security gate, leaks secrets, or corrupts data | Block merge; fix required |
| MAJ | Violates a documented rule, weakens a gate, or breaks a binding | Block merge; fix or waiver |
| MIN | Style, docs, or minor robustness | Record; merge allowed after owner OK |
| OK | Compliant | No action |

## Severity Rules

- The reviewer MUST cite the exact rule violated (file:line or gate ID).
- A finding without a rule citation is not a finding — it is opinion.
- CRIT and MAJ findings must be resolved (fix, revert, or explicit owner waiver)
  before merge.
- MIN findings may be deferred but must be recorded in the review report.

## Auto-fix Boundaries

The reviewer MAY auto-fix:
- Whitespace, formatting, and import ordering
- Typo fixes in comments and docs
- Test renames that match an existing pattern

The reviewer MUST NOT auto-fix:
- Business logic
- Security gate implementations
- Circuit-breaker thresholds
- Web-guard regexes or classifier code
- License headers or attribution

## Request-Changes vs Approve

- **Request Changes** — at least one CRIT/MAJ finding is unresolved.
- **Approve** — no unresolved CRIT/MAJ findings; all MIN findings recorded.
- **Comment** — informational only; no blocking findings.

## Review Report Format

Use `templates/r3-review-report.md`. The report MUST include:
1. Reviewer role + model
2. Files reviewed (glob or explicit list)
3. Findings table: Severity | Rule | File:Line | Evidence | Fix
4. Verdict: Approve / Request Changes / Comment
5. Waiver record (if any MAJ waived by owner)

## Pre-commit Enforcement

`validate_run.py` gates:
- GATE 7 — review-request record integrity: a review report exists for every R3 commit
- GATE 8 — verification checklist: report matches diff, tests red→green, discriminating tests present

If GATE 7 or GATE 8 fails, the commit is rejected.

## Escalation

If reviewer and author disagree on severity:
1. Record both positions in the review report.
2. Escalate to project owner.
3. Owner decision is final and must be documented.
