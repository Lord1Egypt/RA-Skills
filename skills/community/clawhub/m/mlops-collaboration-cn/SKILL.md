---
name: mlops-collaboration-cn
version: 1.0.0
description: Prepare projects for sharing, collaboration, and community
license: MIT
---

# MLOps Collaboration 🤝

Make projects collaborative and community-ready.

## Features

### 1. README Template 📖

Professional documentation:

```bash
cp references/README-template.md ../your-project/README.md
# Edit with your project details
```

Includes:
- Badges (PyPI, CI, License)
- Quick start guide
- Installation steps
- Usage examples
- Contributing guide

### 2. Required Files Checklist ✅

Community files:
- `LICENSE` - MIT/Apache/GPL
- `CODE_OF_CONDUCT.md` - Contributor Covenant
- `CONTRIBUTING.md` - How to contribute
- `CHANGELOG.md` - Version history

### 3. Dev Container 📦

VS Code Dev Container:

```json
// .devcontainer/devcontainer.json
{
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/astral-sh/uv:latest": {}
  }
}
```

## Quick Start

```bash
# Copy README template
cp references/README-template.md ./README.md

# Create required files
touch LICENSE CODE_OF_CONDUCT.md CONTRIBUTING.md CHANGELOG.md

# Setup dev container
mkdir -p .devcontainer
# Add devcontainer.json

# Protect main branch (GitHub UI)
# Settings → Branches → Add rule
```

## Release Checklist

1. Bump version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Git tag: `git tag v1.0.0`
4. Push: `git push --tags`
5. GitHub Release

## Semantic Versioning

- `1.0.0` → `1.0.1` - Bug fix (PATCH)
- `1.0.0` → `1.1.0` - New feature (MINOR)
- `1.0.0` → `2.0.0` - Breaking change (MAJOR)

## Author

Converted from [MLOps Coding Course](https://github.com/MLOps-Courses/mlops-coding-skills)

## Changelog

### v1.0.0 (2026-02-18)
- Initial OpenClaw conversion
- Added README template
