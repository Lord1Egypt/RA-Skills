---
name: "pull_request_reviewer"
description: "Use when the user wants a local review of a GitHub pull request based on its diff, risks, quality, performance, tests, and security implications."
---


# Pull Request Reviewer

Use this skill for code review of an existing GitHub PR.

## Workflow
1. Resolve the target PR number or list open PRs if needed.
2. Read PR metadata and full diff.
3. Review correctness, conventions, performance, test coverage, and security-sensitive changes.
4. Prioritize concrete findings over generic praise.
5. Return a structured review with suggested follow-up.

## Guardrails
- Base the review on the actual diff, not assumptions.
- Findings first, summary second.
- Keep comments actionable and specific.

## Example Requests
- Review PR #123 for correctness and risk.
- List the biggest problems in this open PR.

## Inputs
- PR number or selection
- GitHub diff
- Repo conventions

## Outputs
- Ordered review findings
- Risk summary
- Improvement suggestions

## Success Criteria
- The review is grounded in the actual diff.
- Findings are actionable.
- Risky changes are prioritized.

## Non-Goals
- Generic praise-only review
- Reviewing without reading the diff

## Source Provenance
Derived from `src/commands/review.ts`.
