---
name: mlops-initialization-cn
version: 1.0.0
description: MLOps project initialization with uv/git/VS Code best practices
license: MIT
---

# MLOps 项目初始化 🚀

Setup new MLOps projects with modern Python toolchain.

## Features

### 1. Project Initialization 📦

Create complete project structure:

```bash
./scripts/init-project.sh my-mlops-project
```

Creates:
- `src/` layout
- `pyproject.toml` with uv
- `.gitignore` (Python/MLOps)
- `.vscode/settings.json`
- Git repository

### 2. Configuration Templates 📋

Copy reference configs:

```bash
# pyproject.toml template
cp references/pyproject.toml ../your-project/

# VS Code settings
cp references/vscode-settings.json ../your-project/.vscode/
```

## Quick Start

```bash
# Initialize new project
./scripts/init-project.sh my-project
cd my-project

# Add dependencies
uv add pandas numpy scikit-learn

# Sync environment
uv sync

# Verify
uv run python -c "import sys; print(sys.executable)"
```

## What You Get

- ✅ `src/` package layout
- ✅ Locked dependencies (`uv.lock`)
- ✅ Ruff + MyPy configured
- ✅ VS Code settings
- ✅ Git repository

## References

- `references/pyproject.toml` - Full config example
- `references/vscode-settings.json` - IDE settings

## Author

Converted from [MLOps Coding Course](https://github.com/MLOps-Courses/mlops-coding-skills)

## Changelog

### v1.0.0 (2026-02-18)
- Initial OpenClaw conversion
- Added init script
- Added reference configs
