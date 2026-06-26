# Git Safety for Existing Repos

Use this only for `existing-codebase` or `production-qa` mode. Greenfield harnesses may use
simpler auto-checkpointing because they own the generated app.

## Preflight

Before generation:

```bash
git status --short
```

Save the result to:

```text
harness-state/evidence/sprint-N/git/pre-status.txt
```

If the worktree is dirty, the harness must not assume those changes belong to it.

## Commit Strategies

| Strategy | Use When | Behavior |
|---|---|---|
| `disabled` | Production QA, shared worktree, unknown user changes | Never commit; write diff summaries only |
| `path-scoped` | Existing repo with clear allowlist | Stage only allowlisted paths changed by the harness |
| `all` | Greenfield or harness-owned repo | `git add -A` allowed |

Default for existing repos:

```yaml
workspace:
  git:
    enabled: false
    strategy: disabled
```

## Path-Scoped Staging

If enabled, stage only files under `workspace.write_allowlist`. Do not stage protected paths.

```python
def git_commit_scoped(project_dir: Path, message: str, changed_files: list[str], allowlist: list[str]) -> None:
    files = [f for f in changed_files if path_allowed(f, allowlist)]
    if not files:
        return
    subprocess.run(["git", "add", "--", *files], cwd=project_dir, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=project_dir).returncode == 0:
        return
    subprocess.run(["git", "commit", "-m", message], cwd=project_dir, check=True)
```

## Diff Evidence

Always save:

```text
harness-state/evidence/sprint-N/git/post-status.txt
harness-state/evidence/sprint-N/git/diff-name-only.txt
harness-state/evidence/sprint-N/git/diff.patch
```

This lets the user inspect what the harness changed even when commits are disabled.

## Protected Paths

Default protected paths:

```yaml
protected_paths:
  - .git/**
  - .env
  - .env.*
  - node_modules/**
  - .next/**
  - dist/**
  - build/**
  - harness-state/**
  - harness-logs/**
```

Secrets and generated build outputs are never committed by the harness.
