---
name: mlops-industrialization-cn
version: 1.0.0
description: Transform prototypes into distributable Python packages
license: MIT
---

# MLOps Industrialization 🏭

Convert notebooks to production packages.

## Features

### 1. Package Structure Generator 📦

Create `src/` layout:

```bash
./scripts/create-package.sh my_package
```

Creates:
```
src/my_package/
├── __init__.py
├── io/          # I/O operations
├── domain/      # Pure business logic
└── application/ # Orchestration
```

### 2. Three-Layer Architecture 🏗️

**Domain (Pure)**
- No I/O, no side effects
- Feature transformations
- Pure functions or immutable objects

**I/O (Impure)**
- External interactions
- Load data, save models
- Classes for state management

**Application**
- Wire Domain + I/O
- Training loops, inference

## Quick Start

```bash
# Create package structure
./scripts/create-package.sh my_ml_package

# Add CLI entrypoint to pyproject.toml:
# [project.scripts]
# train = "my_ml_package.application.train:main"
```

## Key Files

Generated files:
- `src/my_package/domain/features.py` - Feature engineering
- `src/my_package/io/data.py` - Data loading/saving
- `src/my_package/application/train.py` - Training pipeline

## Author

Converted from [MLOps Coding Course](https://github.com/MLOps-Courses/mlops-coding-skills)

## Changelog

### v1.0.0 (2026-02-18)
- Initial OpenClaw conversion
- Added package generator
