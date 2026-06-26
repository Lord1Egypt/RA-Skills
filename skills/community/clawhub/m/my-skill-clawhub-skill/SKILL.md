# my_skill_clawhub_skill

## Purpose
A wrapper for `clawhub` to standardize the publishing and installation workflow for agent skills.

## Commands

### 1. Publish (Upload)
Standardize publishing with mandatory versions and changelogs.
```bash
bash scripts/clawhub_helper.sh publish <path> <version> "<changelog>"
```

### 2. Install (Download/Search)
Search and install with optional version specification.
```bash
bash scripts/clawhub_helper.sh install <slug> [version]
```

## Features
- **Auto-versioning**: Ensures every publish has a version.
- **Verification**: Searches for skills before attempting to install.
- **Structure**: Enforces standard ClawHub formatting.
