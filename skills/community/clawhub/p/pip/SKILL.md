---
name: pip
description: Use pip for Python package install, upgrade, freeze, and dependency file workflows with virtual environments first. Use when handling requirements.txt, pip install errors, pipx vs pip decisions, or reproducible Python dependency setup.
metadata:
  {
    "openclaw":
      {
        "emoji": "🐍",
        "requires": { "bins": ["python3"], "anyBins": ["pip", "pip3"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python + pip (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "python3-pip",
              "bins": ["pip3"],
              "label": "Install pip (apt)",
            },
          ],
      },
  }
---

# pip

Use this skill for Python dependency management with safe defaults and reproducible results.

## Scope

- Create and maintain project-local virtual environments
- Install, upgrade, uninstall, and inspect Python packages
- Manage `requirements.txt` and lock-like pinned outputs (`pip freeze`)
- Troubleshoot common pip failures (`externally-managed-environment`, resolver conflicts, wheel/build failures)

## Safety Defaults

- Prefer isolated installs:
  - project: `python3 -m venv .venv`
  - app CLI: `pipx` (if available)
- Avoid global installs unless user explicitly asks.
- Prefer `python3 -m pip ...` instead of bare `pip` to avoid interpreter mismatch.
- Never run unknown `setup.py` or arbitrary install scripts without explicit user approval.

## Fast Path

```bash
# Initialize venv once per project
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip

# Install deps
python3 -m pip install -r requirements.txt

# Pin exact versions
python3 -m pip freeze > requirements.txt
```

## Common Operations

```bash
# Install one or more packages
python3 -m pip install requests pydantic

# Upgrade specific package(s)
python3 -m pip install --upgrade requests

# Uninstall package
python3 -m pip uninstall -y requests

# Show package details
python3 -m pip show requests

# List outdated packages
python3 -m pip list --outdated
```

## Reproducible Dependency Flows

```bash
# Install from lock-like file
python3 -m pip install -r requirements.txt

# Generate pinned snapshot
python3 -m pip freeze > requirements.txt

# Export JSON metadata for automation
python3 -m pip list --format=json
```

## Troubleshooting

- `externally-managed-environment`:
  - Use a venv (`python3 -m venv .venv`) and retry inside it.
  - If user asked for app CLI install, prefer `pipx install <tool>`.
- `No matching distribution found`:
  - Check Python version compatibility.
  - Check package name/version typo.
  - Try `python3 -m pip index versions <pkg>` when available.
- Build/compile failure:
  - Upgrade build tooling: `python3 -m pip install -U pip setuptools wheel`
  - Install system headers/toolchain if needed, then retry.

## Helper Script

Use the bundled helper for repeatable flows:

```bash
{baseDir}/scripts/pip-safe.sh detect
{baseDir}/scripts/pip-safe.sh ensure-venv .venv
{baseDir}/scripts/pip-safe.sh install --venv .venv -- requests pydantic
{baseDir}/scripts/pip-safe.sh requirements --venv .venv requirements.txt
{baseDir}/scripts/pip-safe.sh freeze --venv .venv > requirements.txt
```

## Decision Rules

- If task is project dependencies: use venv + pip.
- If task is standalone CLI tool install for a user: suggest `pipx` first.
- If system policy blocks global installs: stay in venv and explain why.

