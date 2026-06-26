# GitHub Actions Integration

## Overview

Automatically remediate code issues in your CI/CD pipeline.

## Quick Start

Add to `.github/workflows/remediate.yml`:

```yaml
name: Gomboc Remediation

on:
  pull_request:
  push:
    branches: [main]

jobs:
  remediate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Gomboc scan
        env:
          GOMBOC_PAT: ${{ secrets.GOMBOC_PAT }}
        run: |
          python scripts/cli-wrapper.py scan --path ./src --format markdown

      - name: Generate fixes
        env:
          GOMBOC_PAT: ${{ secrets.GOMBOC_PAT }}
        run: |
          python scripts/cli-wrapper.py fix --path ./src

      - name: Auto-remediate
        env:
          GOMBOC_PAT: ${{ secrets.GOMBOC_PAT }}
        run: |
          python scripts/cli-wrapper.py remediate \
            --path ./src \
            --commit \
            --push
```

## Setup

### 1. Add Secret

1. Go to Settings → Secrets and variables → Actions
2. Create new secret: `GOMBOC_PAT`
3. Paste your token (from https://app.gomboc.ai/settings/tokens)

### 2. Create Workflow File

Create `.github/workflows/remediate.yml` with the workflow above.

### 3. Test

Push or open a PR to trigger the workflow.

## Advanced Workflows

### Scan Only (No Auto-Fix)

```yaml
- name: Scan for issues
  env:
    GOMBOC_PAT: ${{ secrets.GOMBOC_PAT }}
  run: |
    python scripts/cli-wrapper.py scan --path ./src --format markdown > scan.md
    cat scan.md >> $GITHUB_STEP_SUMMARY
```

### Create PR with Fixes

```yaml
- name: Generate fixes
  env:
    GOMBOC_PAT: ${{ secrets.GOMBOC_PAT }}
  run: |
    python scripts/cli-wrapper.py fix --path ./src

- name: Create Pull Request
  uses: peter-evans/create-pull-request@v5
  with:
    commit-message: "fix: Auto-remediate code issues"
    title: "Gomboc Auto-Remediation"
    branch: gomboc-fixes
```

### Scheduled Remediation

```yaml
name: Scheduled Gomboc Remediation

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC

jobs:
  remediate:
    runs-on: ubuntu-latest
    steps:
      # ... workflow steps ...
```

## Environment Variables

Set additional options:

```yaml
env:
  GOMBOC_PAT: ${{ secrets.GOMBOC_PAT }}
  GOMBOC_POLICY: aws-cis
  GOMBOC_MCP_URL: http://localhost:3100
```

## Troubleshooting

### "GOMBOC_PAT not set"
- Check secret is in Settings → Secrets
- Verify secret name matches: `secrets.GOMBOC_PAT`

### "API error 401"
- Check token is valid
- Generate new token at https://app.gomboc.ai/settings/tokens

### Workflow doesn't run
- Check `.github/workflows/remediate.yml` syntax
- Verify workflow is enabled in Actions tab

## Best Practices

- ✅ Require PR reviews before merge
- ✅ Use branch protection rules
- ✅ Run scans on every PR
- ✅ Schedule daily full scans
- ✅ Monitor Gomboc dashboard for quota

## Support

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **GitHub Issues:** https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions
