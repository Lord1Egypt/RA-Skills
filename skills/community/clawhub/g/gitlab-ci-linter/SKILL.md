---
name: gitlab-ci-linter
description: Lint and validate GitLab CI/CD pipeline YAML files (.gitlab-ci.yml) for syntax errors, security issues, deprecated patterns, and best practices. Use when asked to lint, validate, audit, or check GitLab CI pipelines, .gitlab-ci.yml files, or CI/CD configurations for GitLab. Triggers on "lint gitlab", "check pipeline", "validate CI", "audit gitlab-ci", "pipeline issues", "gitlab security".
---

# GitLab CI Linter

Lint GitLab CI/CD pipeline files for syntax errors, security issues, deprecated patterns, and best practices violations.

## Commands

All commands use the bundled Python script at `scripts/gitlab_ci_linter.py`.

### 1. Lint a pipeline file

```bash
python3 scripts/gitlab_ci_linter.py lint <file-or-directory> [--strict] [--format text|json|markdown]
```

Runs all lint rules against one or more `.gitlab-ci.yml` files. If given a directory, scans for `*.yml` and `*.yaml` files recursively.

**Flags:**
- `--strict` -- exit code 1 on any warning (not just errors)
- `--format` -- output format: `text` (default), `json`, `markdown`

### 2. Audit for security issues

```bash
python3 scripts/gitlab_ci_linter.py security <file> [--format text|json|markdown]
```

Focused security audit: hardcoded secrets, unprotected variables, privileged runners, insecure Docker image tags, security jobs with `allow_failure`.

### 3. Inspect stages

```bash
python3 scripts/gitlab_ci_linter.py stages <file> [--format text|json|markdown]
```

Show defined stages and which jobs map to each stage. Flags undefined or unused stages.

### 4. Validate pipeline structure

```bash
python3 scripts/gitlab_ci_linter.py validate <file> [--format text|json|markdown]
```

Structural validation only: required keys, stage definitions, job keywords, dependency graph (circular `needs:`, missing refs).

## Lint Rules (24 total)

### Syntax & Structure (8 rules)
1. **missing-stages** -- No `stages:` definition
2. **undefined-stage** -- Job uses stage not in `stages:` list
3. **empty-job** -- Job has no `script:` section
4. **invalid-job-name** -- Job name starts with `.` but is not used as a template
5. **missing-script** -- Job without `script:`, `before_script:`, or `trigger:`
6. **circular-needs** -- Circular dependency in `needs:` graph
7. **duplicate-job** -- Duplicate job names (YAML parser collapses them)
8. **invalid-keyword** -- Unknown top-level or job-level keyword

### Security (6 rules)
9. **hardcoded-secret** -- Passwords, tokens, keys in plain text
10. **unprotected-variable** -- Sensitive-looking variable not using `$CI_*` references
11. **allow-failure-security** -- Security-related job with `allow_failure: true`
12. **privileged-runner** -- `tags:` requesting privileged runners
13. **unmasked-variable** -- Variable looks sensitive but not described as masked
14. **insecure-image** -- Using `:latest` tag for Docker images

### Best Practices (10 rules)
15. **missing-retry** -- No `retry:` on deploy/test jobs
16. **missing-timeout** -- No `timeout:` specified
17. **no-cache-key** -- `cache:` without explicit `key:`
18. **broad-artifacts** -- Overly broad `artifacts: paths:` patterns
19. **missing-rules** -- Job without `rules:` or `only:`/`except:`
20. **deprecated-only-except** -- Using `only:`/`except:` instead of `rules:`
21. **long-script** -- `script:` block exceeds 30 lines
22. **missing-interruptible** -- Long-running job without `interruptible:`
23. **no-coverage-regex** -- Test job without `coverage:` regex
24. **missing-when** -- No `when:` in `rules:` entries

## Output Formats

### Text (default)
```
.gitlab-ci.yml:12 error [missing-script] Job 'deploy' has no script:, before_script:, or trigger:
.gitlab-ci.yml:25 warning [missing-timeout] Job 'test' has no timeout: specified
.gitlab-ci.yml:31 info [deprecated-only-except] Job 'build' uses only:/except: instead of rules:

3 issues (1 error, 2 warnings)
```

### JSON
```json
{
  "file": ".gitlab-ci.yml",
  "issues": [...],
  "summary": {"errors": 1, "warnings": 2, "info": 0}
}
```

### Markdown
Summary table with severity, rule, location, and message.

## CI Integration

```yaml
# .gitlab-ci.yml
lint-pipeline:
  stage: test
  script:
    - python3 scripts/gitlab_ci_linter.py lint .gitlab-ci.yml --strict
```

Exit codes: 0 = clean, 1 = errors found (or warnings in `--strict` mode).
