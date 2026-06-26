# git-hooks-manager

## Overview

A Git hooks manager that simplifies installing, configuring, and sharing Git hooks across teams.

## Features

- **One-command install**: Install hooks with a single command
- **Pre-built templates**: lint-and-test, conventional-commits, branch-guard, security-scan, ci-simulation
- **Custom hooks**: Write hooks in Python instead of shell scripts
- **Team sharing**: Export/import hook configurations
- **Conditional execution**: Skip hooks with environment variables or flags
- **Cross-platform**: Works on Linux, macOS, and Windows (with Git Bash)

## Quick Start

```bash
# Install all recommended hooks
python scripts/hooks_manager.py install --all

# Install specific hook with template
python scripts/hooks_manager.py install pre-commit --template lint-and-test

# Validate a commit message
python scripts/hooks_manager.py validate-message "feat: add user authentication"

# List installed hooks
python scripts/hooks_manager.py list
```

## Templates

| Template | Description |
|----------|-------------|
| `lint-and-test` | Run `flake8`/`eslint` + `pytest`/`jest` before commit |
| `conventional-commits` | Enforce `type(scope): message` format |
| `branch-guard` | Block commits to `main`/`master`, enforce naming |
| `security-scan` | Run `bandit`, `npm audit`, or custom security checks |
| `ci-simulation` | Run full CI pipeline locally before push |

## CLI Commands

| Command | Description |
|---------|-------------|
| `install <hook>` | Install a hook |
| `install --all` | Install all recommended hooks |
| `uninstall <hook>` | Remove a hook |
| `list` | List installed hooks |
| `validate-message <msg>` | Validate commit message |
| `validate-branch <name>` | Validate branch name |
| `export <file>` | Export hooks config |
| `import <file>` | Import hooks config |

## Examples

See `examples/basic_usage.py` for programmatic usage.

## Testing

```bash
python -m pytest tests/ -v
```

## 中文说明

Git Hooks管理器，简化团队间Git钩子的安装和配置。

### 快速开始

```bash
python scripts/hooks_manager.py install pre-commit --template lint-and-test
python scripts/hooks_manager.py validate-message "fix: resolve memory leak"
```

## License

MIT License
