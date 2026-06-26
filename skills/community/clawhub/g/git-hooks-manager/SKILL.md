# git-hooks-manager - Git Hooks管理器

## Metadata

| Field | Value |
|-------|-------|
| **Name** | git-hooks-manager |
| **Slug** | git-hooks-manager |
| **Version** | 1.0.0 |
| **Homepage** | https://github.com/openclaw/git-hooks-manager |
| **Category** | development |
| **Tags** | git, hooks, pre-commit, pre-push, lint, test, automation, devops |

## Description

### English
A Git hooks manager that simplifies installing, configuring, and sharing Git hooks across teams. Includes pre-built templates for linting, testing, branch naming validation, commit message validation, and custom hook orchestration.

### 中文
Git Hooks管理器，简化团队间Git钩子的安装、配置和共享。包含预置模板：代码检查、测试运行、分支名验证、提交信息验证和自定义钩子编排。

## Requirements

- Python 3.8+
- Git >= 2.30
- click >= 8.0.0
- colorama >= 0.4.6

## Configuration

### Environment Variables
```bash
HOOKS_MANAGER_STRICT=true
HOOKS_MANAGER_SKIP_LINT=false
```

## Usage

### Install Hooks

```bash
# Install all recommended hooks
python scripts/hooks_manager.py install --all

# Install specific hook
python scripts/hooks_manager.py install pre-commit

# Install from template
python scripts/hooks_manager.py install pre-commit --template lint-and-test
```

### Create Custom Hook

```python
from git_hooks_manager import HookManager

manager = HookManager()

# Define a custom pre-commit hook
@manager.hook("pre-commit")
def my_pre_commit():
    # Run custom checks
    result = manager.run_command("pytest", ["tests/smoke/"])
    if result.returncode != 0:
        print("Smoke tests failed!")
        return False
    return True

manager.install()
```

### Validate Commit Messages

```bash
python scripts/hooks_manager.py validate-message "feat: add user login"
```

## API Reference

### HookManager
- `install(hook_name, template=None)` - Install a hook
- `uninstall(hook_name)` - Remove a hook
- `list_hooks()` - List installed hooks
- `validate_commit_message(msg)` - Validate conventional commits format
- `validate_branch_name(name)` - Validate branch naming convention
- `run_command(cmd, args)` - Run a shell command and return result

### Built-in Templates
- `lint-and-test` - Run linters and unit tests
- `conventional-commits` - Validate commit messages
- `branch-guard` - Enforce branch naming rules
- `security-scan` - Run basic security checks
- `ci-simulation` - Simulate CI pipeline locally

## Examples

See `examples/` directory for complete examples.

## Testing

```bash
cd /root/.openclaw/workspace/skills/git-hooks-manager
python -m pytest tests/ -v
```

## License

MIT License
