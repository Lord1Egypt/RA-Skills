# Harness Mode Selection

Choose the mode before writing any harness code. The mode controls cwd, write boundaries,
artifact paths, git behavior, and evaluator probes.

## Modes

| Mode | Use When | Generator CWD | Default Git | Artifact Policy |
|---|---|---|---|---|
| `greenfield` | Building a new app from scratch | `PROJECT_DIR / "src"` | Auto checkpoints allowed | All non-app output under `harness-state/` + `harness-logs/` |
| `existing-codebase` | Modifying an established repo | Repo root or service root | Path-scoped or disabled | Same; never scatter artifacts into app/public/docs |
| `production-qa` | Mostly evaluating, building, testing, and proposing/fixing production issues | Repo root, often read-heavy | Disabled by default | Same; evidence collector is primary |

## Required Questions

Ask before implementation:

1. Is the harness creating a new app or maintaining an existing repo?
2. What paths may the Generator edit?
3. What paths must never be edited?
4. Should the harness auto-commit, create path-scoped checkpoints, or avoid commits?
5. Where should generated evidence, screenshots, logs, reports, and temp files go?

Defaults:

```yaml
workspace:
  mode: greenfield
  app_root: src
  artifact_root: harness-state
  log_root: harness-logs
  evidence_root: harness-state/evidence
  tmp_root: harness-state/tmp
  write_allowlist:
    - src/**
    - package.json
    - package-lock.json
  protected_paths:
    - .env*
    - .git/**
    - harness-state/**
    - harness-logs/**
  git:
    enabled: true
    strategy: path-scoped   # path-scoped | all | disabled
```

For `existing-codebase`, do not use `git add -A` unless the user explicitly says the harness
owns the whole repo.

## Existing Codebase Rules

Use repo-root cwd only when the sprint can require cross-cutting changes such as:

- API routes, auth, middleware, Prisma, migrations, package files
- production env/readiness checks
- CMS schemas, scripts, or admin tooling
- tests and CI config

If repo-root cwd is used, the prompt must include:

```text
You may edit only these paths:
<write_allowlist>

You must never edit these paths:
<protected_paths>

All generated evidence/logs/screenshots/reports/temp files must go under:
<evidence_root> or <log_root>
```

## Production QA Rules

Production QA harnesses usually run commands more than they generate code. Include explicit
probes in sprint contracts:

- build commands
- health/readiness endpoints
- auth/session endpoints
- API negative tests
- env missing/invalid cases
- browser workflows
- log redaction checks

Store every command output under `harness-state/evidence/sprint-N/commands/`.
