---
name: git-hooks-toolkit
description: Generate, install, and manage Git hooks with pre-built templates. Includes hooks for linting staged files, enforcing conventional commits, blocking debug statements, preventing large file commits, auto-formatting code, requiring ticket references, protecting branches, running tests before push, and auto-installing dependencies after merge. Use when setting up git hooks, enforcing commit conventions, or automating pre-commit/pre-push checks.
---

# Git Hooks Toolkit

Install production-ready Git hooks in seconds with pre-built templates.

## Quick Start

```bash
# List all available templates
python3 scripts/git_hooks.py list

# Install a hook
python3 scripts/git_hooks.py install pre-commit lint-staged
python3 scripts/git_hooks.py install commit-msg conventional

# Preview before installing
python3 scripts/git_hooks.py show pre-commit no-debug

# Check what's installed
python3 scripts/git_hooks.py status

# Remove a hook
python3 scripts/git_hooks.py remove pre-commit
```

## Available Templates

### pre-commit
- **lint-staged** — Run ESLint/Ruff/Flake8 on staged files only
- **no-debug** — Block console.log, debugger, pdb, breakpoint()
- **large-files** — Prevent files over 500KB from being committed
- **format-check** — Auto-run Prettier, Black, gofmt on staged files

### commit-msg
- **conventional** — Enforce Conventional Commits (feat/fix/docs/etc.)
- **ticket-ref** — Require ticket reference (#123, PROJ-456)
- **no-wip** — Block WIP commits on main/master/release branches

### pre-push
- **run-tests** — Auto-detect project type and run test suite
- **branch-protect** — Prevent direct push to main/master

### post-merge
- **install-deps** — Auto-install deps when lockfiles change

## Commands

- `list` — Show all templates
- `install <hook> <template> [--repo path] [--force]` — Install a hook
- `show <hook> <template>` — Preview template content
- `status [--repo path]` — Show installed hooks
- `remove <hook> [--repo path]` — Delete a hook
