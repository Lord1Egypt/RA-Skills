---
name: helm-chart-linter
description: Lint and validate Helm charts for structure, security, dependencies, and best practices. Use when asked to lint, validate, check, or audit Helm charts, verify Chart.yaml, values.yaml, templates, or ensure Helm chart quality. Triggers on "lint helm", "validate chart", "check helm chart", "helm best practices".
---
# Helm Chart Linter

A pure Python 3 (stdlib only) linter and validator for Helm chart directories. Checks structure, security, dependencies, and best practices across 22 rules.

## Commands

```
python3 scripts/helm_chart_linter.py <command> <chart-dir> [options]
```

| Command        | Description                                                   |
|----------------|---------------------------------------------------------------|
| `lint`         | Lint chart structure and best practices (all rules)           |
| `security`     | Run security-focused checks only                              |
| `dependencies` | Validate Chart.yaml/Chart.lock dependencies                   |
| `validate`     | Full validation: structure + security + dependencies          |

## Options

| Option                          | Description                                      |
|---------------------------------|--------------------------------------------------|
| `--format text\|json\|markdown` | Output format (default: text)                  |
| `--strict`                      | Exit 1 on warnings as well as errors (CI mode)   |

## Examples

```bash
# Basic lint
python3 scripts/helm_chart_linter.py lint ./my-chart

# Full validation with JSON output
python3 scripts/helm_chart_linter.py validate ./my-chart --format json

# Security audit, strict mode for CI
python3 scripts/helm_chart_linter.py security ./my-chart --strict

# Dependency check with Markdown report
python3 scripts/helm_chart_linter.py dependencies ./my-chart --format markdown
```

## Rules

### Structure (6 rules)
1. `CHART001` — Chart.yaml exists and has required fields (apiVersion, name, version, description)
2. `CHART002` — Version is valid semver
3. `CHART003` — values.yaml exists
4. `CHART004` — templates/ directory exists
5. `CHART005` — NOTES.txt exists in templates/ (warning)
6. `CHART006` — .helmignore exists (warning)

### Security (6 rules)
7. `SEC001` — No hardcoded secrets in values.yaml (passwords, tokens, keys)
8. `SEC002` — No privileged containers (securityContext.privileged: true)
9. `SEC003` — No hostNetwork, hostPID, or hostIPC enabled
10. `SEC004` — Resource limits defined in templates
11. `SEC005` — No runAsRoot without explicit runAsNonRoot
12. `SEC006` — Image tags not "latest"

### Dependencies (4 rules)
13. `DEP001` — Chart.lock present and matches Chart.yaml dependencies
14. `DEP002` — No wildcard version constraints
15. `DEP003` — Repository URLs use HTTPS
16. `DEP004` — No duplicate dependency names

### Best Practices (6 rules)
17. `BP001` — Labels include app.kubernetes.io/name, version, managed-by
18. `BP002` — Liveness and readiness probes defined
19. `BP003` — Service account name configured
20. `BP004` — Namespace not hardcoded in templates
21. `BP005` — No deprecated API versions (extensions/v1beta1, apps/v1beta1, etc.)
22. `BP006` — Values documented with comments

## Exit Codes

| Code | Meaning                                      |
|------|----------------------------------------------|
| `0`  | No issues (or only warnings in normal mode)  |
| `1`  | Errors found (or warnings found in --strict) |
| `2`  | Script/usage error                           |
