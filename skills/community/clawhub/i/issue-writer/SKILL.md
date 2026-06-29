---
name: issue-writer
description: Use when drafting, restructuring, reviewing, or submitting GitHub issues from investigation findings, bugs, security reviews, regressions, feature requests, or technical debt; selects the right issue shape and keeps evidence, impact, recommendations, and acceptance criteria appropriate to the issue type.
---

# Issue Writer

## Purpose

Turn findings, review notes, bugs, security concerns, or implementation gaps into actionable GitHub issues. Match the issue structure to the issue type instead of forcing one generic template.

## Use When

Use this skill when the user asks to:

1. Draft or polish a GitHub issue.
2. Convert review/debug/security findings into an issue.
3. Create an epic issue or linked child issues.
4. Submit an issue with `gh`.
5. Compare whether an issue has enough evidence, reproduction detail, impact, recommendations, and acceptance criteria.

## Core Workflow

1. Identify the issue type before drafting:
   - `security`
   - `bug` or `regression`
   - `epic` or `tech-debt`
   - `feature` or product request
2. Load only the matching reference file:
   - Security: `references/security-issue.md`
   - Bug or regression: `references/bug-issue.md`
   - Epic or technical debt: `references/epic-issue.md`
3. Gather concrete evidence:
   - Code paths and line numbers.
   - Logs, screenshots, responses, or repro steps.
   - Config/deployment facts.
   - Current versus expected behavior.
4. Draft in the user's language unless they ask otherwise.
5. Keep the issue actionable:
   - Findings must be reviewable from evidence.
   - Recommendations must explain why when they change security boundaries, defaults, compatibility, or architecture.
   - Acceptance criteria must be verifiable.
6. If the user asks to submit, confirm the target repository if ambiguous, then submit with `gh issue create` or the GitHub REST API fallback when `gh issue create` fails.

## Type Selection Rules

### Security

Use the security issue shape when the issue is about auth, authorization, tokens, secrets, SSRF, CORS, origin isolation, injection, data exposure, privilege, sandboxing, DoS, supply chain, or deployment hardening. Security issues need evidence chains and risk reasoning because the fix usually changes a boundary or default.

### Bug Or Regression

Use the bug shape when the user-visible behavior is wrong, broken, unexpected, or regressed. Bug issues need reproduction closure more than broad risk reasoning.

### Epic Or Tech Debt

Use the epic shape when multiple related findings should be grouped into one coordination issue, or when the work will likely split into child issues. Epic issues need scope, grouping, priorities, child issue candidates, and acceptance criteria.

### Feature

For feature requests, use a lightweight product issue shape:

1. Problem / need.
2. Target users and workflows.
3. Proposed behavior.
4. Non-goals.
5. Open questions.
6. Acceptance criteria.

## Recommendation Rules

Use plain recommendations for simple bugs. Add `reason` and `option` fields when a recommendation:

1. Rejects an input/config/default.
2. Tightens security or permissions.
3. Changes compatibility or existing behavior.
4. Introduces a new required configuration.
5. Has multiple viable implementation paths.

Preferred wording:

```markdown
- Recommendation:
  - Reason:
  - Options:
```

## Evidence Rules

1. Security evidence should be a chain: entrypoint -> behavior -> missing control -> exposure/impact context.
2. Bug evidence should be reproduction-oriented: steps -> observed behavior -> expected behavior -> logs/screenshots.
3. Epic evidence can summarize and link child facts, but each high-risk item still needs enough evidence to be independently reviewable.
4. If a fact is suspected but not verified, mark it as `Needs verification` instead of stating it as confirmed.

## Submission Rules

Before submitting:

1. Ensure the title is concise and action-oriented.
2. Check the issue body does not include secrets, tokens, private credentials, or excessive exploit detail.
3. If labels are requested, avoid guessing labels that may not exist unless `gh label list` was checked.
4. If `gh issue create` fails with GraphQL auth issues but `gh auth status` is valid, try GitHub REST:

```sh
gh api --method POST repos/OWNER/REPO/issues -f title='TITLE' -F body=@BODY_FILE --jq '.html_url'
```

Report the created URL or the exact blocker.
