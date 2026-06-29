# Bug Or Regression Issue Shape

Use this shape when a feature behaves incorrectly, a regression is suspected, or users can reproduce a failure. Bug issues should prioritize reproduction closure over broad design discussion.

## Required Sections

```markdown
# <Observed broken behavior>

## Description

One sentence describing what fails and in what scenario.

## Steps To Reproduce

1. ...
2. ...
3. ...

## Current Behavior

What actually happens. Include error messages, logs, screenshots, response status/body, or UI state when available.

## Expected Behavior

What should happen instead.

## Impact

Who is affected, how often, and whether there is data loss, workflow blockage, degraded UX, or operational risk.

## Initial Diagnosis

Optional. Include suspected code paths, recent changes, or likely cause. Mark uncertain facts as `Needs verification`.

## Suggested Fix

Optional and lightweight unless the fix is obvious.

## Acceptance Criteria

- [ ] Repro steps no longer fail.
- [ ] Regression test or verification command added when practical.
- [ ] Existing related behavior remains intact.
```

## Bug-Specific Rules

1. Do not overuse security-style evidence chains for ordinary bugs.
2. The most important evidence is a reproducible path from input/action to wrong output.
3. Suggested fixes do not need `reason` and `options` unless they change compatibility, defaults, data shape, or architecture.
4. If the bug is hard to reproduce, include environment, version, branch, config, and observed frequency.
5. If the issue is a regression, identify last-known-good and suspected bad version/commit/branch when available.

## Suggested Fix Examples

Simple:

```markdown
- Validate `namespace` before saving the config.
- Return a structured 400 instead of sending an empty value to the Kubernetes API.
- Add a regression test for empty namespace.
```

With reason/options because behavior changes:

```markdown
- Recommendation: Treat empty `namespace` as invalid input.
  - Reason: Empty namespace currently reaches the Kubernetes API and fails late with an unclear dependency error.
  - Options: Reject at the HTTP boundary with 400, or normalize to a documented default namespace before persistence.
```
