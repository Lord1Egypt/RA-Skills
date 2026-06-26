# GitHub Push Configuration Guide

Configure and customize github-push behavior.

## Config File

Create `config.yaml` in project root:

```yaml
defaults:
  safe_mode: true
  min_delay: 2  # seconds - min delay
  max_delay: 4  # seconds - max delay
  batch_commits: true
  enable_validation: true
```

## Safety Thresholds

| Metric | Default | Description |
|--------|---------|-------------|
| Push cooldown | 180s | Min push interval |
| Pushes/hour | 50 | Rate limit |
| Commits/hour | 100 | Rate limit |

## Exclusion Patterns

Auto-excludes:
- `.git/` directory
- `.DS_Store`, `Thumbs.db`
- SSH keys (`id_rsa`, `id_ed25519`)
- Key files (`*.pem`, `*.key`)
- Large files (`*.zip`, `*.exe`, `*.dll`)

## Environment Variables

No required environment variables. SSH keys auto-loaded.

## Pre-commit Integration

```bash
# Add to .pre-commit-config.yaml
- repo: local
  hooks:
    - id: github-push
      name: GitHub Push
      entry: python scripts/github_upload.py
      language: system
```