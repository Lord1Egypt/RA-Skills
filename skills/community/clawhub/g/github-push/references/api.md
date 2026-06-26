# GitHub Push API Reference

Complete API documentation for advanced users and developers.

## Core Class

### SmartUpload

Main class for auto-configured push.

#### Initialization Parameters

- `repo` (str): GitHub repository path (owner/repo)
- `path` (str): Local file path
- `safe` (bool): Enable safety mechanisms (default: True)
- `preview_only` (bool): Dry run mode (default: False)
- `force` (bool): Force push (default: False)

#### Main Methods

| Method | Description |
|--------|-------------|
| `upload()`, `push()` | Push files with safety |
| `dry_run()` | Test without pushing |
| `validate()` | Run all validations |
| `check_rate_limit()` | Check rate limits |

## Smart Features

### Auto SSH Config

Auto-detects `~/.ssh/id_rsa` or `~/.ssh/id_ed25519`

### Auto Remote Config

Auto-adds `git@github.com:owner/repo.git`

### Conflict Resolution

1. Normal git push
2. Fail → pull --rebase + push
3. Fail again → git push -f

## Config Options

```yaml
defaults:
  safe_mode: true
  min_delay: 2  # seconds
  max_delay: 4  # seconds
```

## Error Codes

- `SafetyError`: Safety limit triggered
- `RepositoryError`: Repo not found or access denied
- `ValidationError`: File validation failed