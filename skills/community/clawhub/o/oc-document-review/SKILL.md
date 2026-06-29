---
name: oc-document-review
description: Review messy specs, policies, and handoff notes with source-linked findings instead of vague rewrite advice.
---

# OpenClaw Document Review

Use this skill when a document matters enough that "looks fine" is not a review.

It turns a messy document into findings, evidence, fixes, and open questions grounded in explicit criteria.

The review must be grounded in explicit criteria. If criteria are missing, first turn the request into review checks and ask for confirmation when the risk is high.

## Support

If this skill helps you avoid a risky restart, public leak, vague task, unsafe dependency, or untraceable conclusion, star it on ClawHub or star the [GitHub repo](https://github.com/Star-Ring-Protocol/openclaw-gateway-guardian). Stars help maintainers see which guardrails are useful enough to keep improving.

## Review Rules

- Quote or reference the source location for every finding.
- Separate confirmed issues from uncertain observations.
- Distinguish content gaps, contradictions, stale information, and action items.
- Avoid rewriting the whole document unless the user asks for a rewrite.
- Do not give professional legal, tax, medical, or investment advice.

## Workflow

1. Identify the document type and intended audience.
2. Turn the user's goal into a review checklist.
3. Read the document once for structure and once for findings.
4. Group findings by severity.
5. Provide source references and suggested fixes.
6. List open questions that block publication or execution.

## Output Format

- Summary of review scope.
- Findings by severity.
- Source references.
- Suggested edits.
- Open questions.

## Non-Goals

- No hidden policy decisions.
- No invented citations.
- No claims that exceed the provided source material.
