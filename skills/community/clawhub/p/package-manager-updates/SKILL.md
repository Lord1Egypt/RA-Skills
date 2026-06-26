---
name: package-manager-updates
description: Check, summarize, and update packages across all installed package managers (npm, pip, brew, cargo, go, etc.). Use when user wants to (1) check for outdated packages, (2) see a summary of outdated packages, or (3) update all/select packages. Excludes OpenClaw packages.
---

# Package Manager Updates

This skill automates package update workflows: check → summarize → update (on demand).

## Workflow

### Step 1: Check for Updates

Run these commands to check outdated packages for each package manager:

```bash
# npm global packages
npm outdated -g --depth=0 2>/dev/null || echo "npm: no global packages"

# pip
pip list --outdated 2>/dev/null || pip3 list --outdated 2>/dev/null

# Homebrew
brew outdated

# Cargo (Rust)
cargo outdated 2>/dev/null || echo "cargo: not installed or no projects"

# Go modules
go list -m -u all 2>/dev/null || echo "go: no modules"
```

### Step 2: Present Summary

Format the results in a clear table:

| Package Manager | Outdated Count |
|----------------|----------------|
| npm | X |
| pip | X |
| brew | X |
| cargo | X |

For detailed output, show per-package tables with Current vs Latest versions.

### Step 3: Update (On Demand)

Only update when user explicitly confirms. Run:

```bash
# npm - update all globals
npm update -g

# npm - update specific package
npm install -g <package-name>@latest

# pip
pip install --upgrade <package-name>

# pip (Homebrew-managed)
brew upgrade pip 2>/dev/null || pip install --upgrade <package-name>

# Homebrew
brew update && brew upgrade

# Homebrew (Post Update/Upgrade)
brew cleanup 
brew doctor

# Homebrew - specific package
brew upgrade <package-name>

# Cargo
cargo update

# Go
go get -u <module>
```

## Exclusions

- Always exclude OpenClaw packages (check if package name starts with `openclaw` or is in the OpenClaw ecosystem)
- Skip system-critical packages unless user explicitly asks

## Output Format

Keep output concise. Use markdown tables for summaries. Present update commands only when user confirms.
