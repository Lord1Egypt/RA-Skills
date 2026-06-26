# Secrets & Environments

## Secrets
```bash
gh secret list --repo owner/repo                          # names only, values never shown

# ⚠️ CONFIRM WITH USER before running — writes a secret to the repository
gh secret set DATABASE_URL --repo owner/repo              # interactive (safest)

# ⚠️ CONFIRM WITH USER before running — writes a secret scoped to an environment
gh secret set API_KEY --repo owner/repo --env production
```

## Environments
```bash
gh api repos/owner/repo/environments --jq '.environments[].name'

# ⚠️ CONFIRM WITH USER before running — creates or overwrites environment protection rules
gh api --method PUT repos/owner/repo/environments/production \
  --field wait_timer=10 \
  --field reviewers='[{"type":"User","id":USER_ID}]'
```

## Variables (non-secret config)
```bash
gh variable list --repo owner/repo

# ⚠️ CONFIRM WITH USER before running — sets a repository variable
gh variable set APP_ENV --body "production" --repo owner/repo
```
