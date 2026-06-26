# CI / GitHub Actions

## Runs
```bash
gh run list --repo owner/repo --limit 10
gh run watch --repo owner/repo
gh run view <id> --repo owner/repo --log-failed
gh run rerun <id> --repo owner/repo --failed-only
gh run rerun <id> --repo owner/repo

# ⚠️ CONFIRM WITH USER before running — cancels an active run
gh run cancel <id> --repo owner/repo
```

## Workflows
```bash
gh workflow list --repo owner/repo

# ⚠️ CONFIRM WITH USER before running — triggers a workflow run (may deploy or modify infra)
gh workflow run deploy.yml --repo owner/repo --field environment=staging

# ⚠️ CONFIRM WITH USER before running — enables a workflow (it will start running on triggers)
gh workflow enable deploy.yml --repo owner/repo

# ⚠️ CONFIRM WITH USER before running — disables a workflow (stops all future runs)
gh workflow disable deploy.yml --repo owner/repo
```

## Checklist for .github/workflows/
- Pin actions to SHA (not `@latest`)
- Use `${{ secrets.GITHUB_TOKEN }}` — never hardcode
- Cache deps: `actions/cache`
- Tests on every PR; deploy only on merge to main
- Use `environments:` with required reviewers for production
- Always declare `permissions:` explicitly — default is too broad

```yaml
# Minimal safe permissions example
permissions:
  contents: read
  pull-requests: write
```
