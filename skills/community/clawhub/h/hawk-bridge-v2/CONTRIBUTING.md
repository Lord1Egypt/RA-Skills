# Contributing to Auto-Evolve

Thank you for your interest in contributing to Auto-Evolve!

---

## Development Environment Setup

### Prerequisites

- Python 3.10+
- Git
- `gh` CLI (for PR creation and GitHub interactions)

### Clone and Install

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/auto-evolve.git
cd auto-evolve

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies (if any)
pip install -e .
```

### Verify Installation

```bash
python3 scripts/auto-evolve.py --help
```

---

## Code Standards

### Language

- Python 3.10+
- English comments (following [CODE-STYLE.md v2](https://github.com/relunctance/gql-openclaw/blob/main/knowledge/standards/CODE-STYLE.md))
- All code must be type-annotated

### Code Style

We follow PEP 8 with these rules:

- Line length: max 120 characters
- Indentation: 4 spaces (no tabs)
- Docstrings: Google style

```python
def example_function(param: str, options: dict) -> bool:
    """
    Brief one-line description.

    Longer description if needed.

    Args:
        param: Description of the parameter.
        options: Description of options dict.

    Returns:
        Description of return value.

    Raises:
        ValueError: When something is wrong.
    """
    if not param:
        raise ValueError("param cannot be empty")
    return True
```

### File Header

Every Python file must include:

```python
#!/usr/bin/env python3
# ===========================================================
# File:    <file_name>
# Description: <One-line English description>
# Description (中文): <One-line Chinese description>
#
# Author: <Author>
# Date:   <YYYY-MM-DD>
# License: MIT
# ===========================================================
```

---

## Branch Strategy

```
main           — stable, production-ready
├── develop    — integration branch (if needed)
├── feature/* — new features
├── fix/*      — bug fixes
├── docs/*    — documentation only
└── refactor/* — code refactoring
```

### Creating a Branch

```bash
# Feature branch
git checkout -b feature/my-new-feature

# Bug fix branch
git checkout -b fix/some-bug

# Documentation branch
git checkout -b docs/improve-readme
```

---

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, missing semicolons, etc. |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

### Examples

```bash
git commit -m "feat(scan): add multi-language TODO detection"
git commit -m "fix(conflict): handle rebase conflicts gracefully"
git commit -m "docs: update README with Chinese translation"
git commit -m "refactor(priority): simplify priority calculation"
```

---

## Testing

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run with coverage
python3 -m pytest tests/ --cov=. --cov-report=term-missing

# Run specific test file
python3 -m pytest tests/test_auto_evolve.py -v
```

### Writing Tests

```python
import pytest
from auto_evolve import calculate_priority

def test_priority_high_value_low_risk():
    """High value with low risk should give high priority."""
    item = {
        "value_score": 8,
        "risk_score": 2,
        "cost_score": 3
    }
    priority = calculate_priority(item)
    assert priority > 0.5

def test_priority_zero_division():
    """Zero risk or cost should not cause division error."""
    item = {"value_score": 5, "risk_score": 0, "cost_score": 5}
    priority = calculate_priority(item)
    assert priority == 0
```

### Test Requirements

- All new features must have tests
- All bug fixes must have a test that would have caught the bug
- Test coverage should not decrease

---

## Pull Request Process

### Before Opening a PR

1. **Sync with latest main**
   ```bash
   git fetch origin main
   git rebase origin/main
   ```

2. **Run tests**
   ```bash
   python3 -m pytest tests/ -v
   ```

3. **Check code style**
   ```bash
   python3 -m flake8 scripts/auto-evolve.py
   ```

4. **Verify documentation updated**
   - SKILL.md reflects new commands
   - README.md updated if needed
   - CHANGELOG.md updated

### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] No sensitive information leaked
```

### PR Title

Follow Conventional Commits:
```
feat: add new command
fix: resolve conflict handling
docs: update README
```

---

## Opening Issues

### Bug Reports

```markdown
## Bug Description
Clear description of the bug.

## Steps to Reproduce
1. Run `...`
2. Click on `...`
3. See error

## Expected Behavior
What should happen.

## Environment
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.10.12]
- Auto-Evolve version: [e.g. 3.0.0]

## Relevant Log Output
Paste any error messages or logs.
```

### Feature Requests

```markdown
## Feature Description
Clear description of the feature.

## Problem It Solves
What problem does this solve?

## Proposed Solution
How would you implement this?

## Alternatives Considered
What other approaches did you consider?
```

---

## Code of Conduct

### Our Standards

Examples of behavior that contributes to a positive environment:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project maintainers. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate.

---

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be patient — we try to respond within 48 hours

---

## License

By contributing to Auto-Evolve, you agree that your contributions will be licensed under the MIT License.
