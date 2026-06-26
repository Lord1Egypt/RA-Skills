---
name: github-actions-linter
description: Lint and validate GitHub Actions workflow YAML files for common mistakes, security issues, deprecated actions, and best practices. Use when asked to lint, validate, audit, or check GitHub Actions workflows, CI/CD pipelines on GitHub, or .github/workflows/*.yml files. Triggers on "lint actions", "check workflow", "validate CI", "audit GitHub Actions", "workflow issues", "actions security".
---

# GitHub Actions Linter

Lint GitHub Actions workflow files for syntax errors, security issues, deprecated actions, and best practices violations.

## Commands

All commands use the bundled Python script at `scripts/gha_linter.py`.

### 1. Lint a workflow file

```bash
python3 scripts/gha_linter.py lint <file-or-directory> [--strict] [--format text|json|markdown]
```

Runs all lint rules against one or more workflow files. If given a directory, scans for `*.yml` and `*.yaml` files recursively.

**Flags:**
- `--strict` — exit code 1 on any warning (not just errors)
- `--format` — output format: `text` (default), `json`, `markdown`

### 2. Audit for security issues

```bash
python3 scripts/gha_linter.py security <file> [--format text|json|markdown]
```

Focused security audit: shell injection via `${{ }}` in `run:`, hardcoded secrets, overly permissive `permissions`, untrusted event contexts in expressions.

### 3. Check for deprecated actions

```bash
python3 scripts/gha_linter.py deprecated <file> [--format text|json|markdown]
```

Detect outdated action versions (e.g., `actions/checkout@v2`, `actions/setup-node@v3` when v4 exists) and suggest upgrades.

### 4. Validate workflow structure

```bash
python3 scripts/gha_linter.py validate <file> [--format text|json|markdown]
```

Structural validation only: required keys (`on`, `jobs`), valid trigger events, valid `runs-on` labels, job dependency graph (circular deps, missing refs).

## Lint Rules (28 total)

### Syntax & Structure (8 rules)
1. **missing-on** — Workflow missing `on` trigger
2. **missing-jobs** — Workflow missing `jobs` section
3. **empty-jobs** — Jobs section is empty
4. **missing-runs-on** — Job missing `runs-on`
5. **missing-steps** — Job missing `steps`
6. **empty-steps** — Steps list is empty
7. **invalid-trigger** — Unknown trigger event name
8. **circular-deps** — Circular job dependency via `needs`

### Security (8 rules)
9. **shell-injection** — `${{ }}` expression in `run:` (potential injection)
10. **hardcoded-secret** — Hardcoded password/token/key patterns in workflow
11. **permissive-permissions** — `permissions: write-all` or no permissions block
12. **untrusted-context** — Dangerous contexts in expressions (`github.event.issue.title`, `github.event.pull_request.body`, etc.)
13. **pull-request-target** — `pull_request_target` with checkout of PR head (known attack vector)
14. **third-party-action** — Non-verified third party action without pinned SHA
15. **env-in-run** — Secret used directly in `run:` instead of via `env:`
16. **excessive-permissions** — Job requests more permissions than needed

### Deprecated & Outdated (4 rules)
17. **deprecated-action** — Action version is outdated (v1/v2 when v4 exists)
18. **deprecated-runner** — Using deprecated runner labels (ubuntu-18.04, macos-10.15)
19. **set-output-deprecated** — Using deprecated `::set-output::` command
20. **save-state-deprecated** — Using deprecated `::save-state::` command

### Best Practices (8 rules)
21. **missing-timeout** — Job without `timeout-minutes` (default 6h is dangerous)
22. **missing-name** — Step without `name` (harder to debug)
23. **latest-tag** — Action pinned to `@main` or `@master` (unstable)
24. **no-concurrency** — Workflow without `concurrency` (can waste resources)
25. **hardcoded-runner** — Hardcoded runner version instead of `-latest`
26. **long-run-command** — `run:` block exceeds 50 lines (should be a script)
27. **duplicate-step-id** — Duplicate `id` in steps within same job
28. **missing-if-continue** — `continue-on-error: true` without explanation comment

## Output Formats

### Text (default)
```
workflow.yml:12:3 error [shell-injection] Expression ${{ github.event.issue.title }} in run: is vulnerable to injection
workflow.yml:25:5 warning [missing-timeout] Job 'build' has no timeout-minutes (default: 360 min)
workflow.yml:31:7 warning [missing-name] Step at index 2 has no name

3 issues (1 error, 2 warnings)
```

### JSON
```json
{
  "file": "workflow.yml",
  "issues": [...],
  "summary": {"errors": 1, "warnings": 2, "info": 0}
}
```

### Markdown
Summary table with severity, rule, location, and message.

## CI Integration

```yaml
# .github/workflows/lint-actions.yml
name: Lint Workflows
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/gha_linter.py lint .github/workflows/ --strict
```

Exit codes: 0 = clean, 1 = errors found (or warnings in `--strict` mode).
