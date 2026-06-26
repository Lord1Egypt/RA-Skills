---
name: git-commit-template
description: >
  Standardized Git commit message templates using changelog-style categories.
  Use when creating Git commits with structured format - Added (new features),
  Changed (existing functionality changes), Deprecated (soon-to-be removed),
  Removed (deleted features), Fixed (bug fixes). Triggers on commit creation,
  git commit messages, or standardizing commit history.
---

# Git Commit Template

Create structured, changelog-style Git commit messages using five standard categories. This ensures consistent, searchable, and maintainable commit history across projects.

## Commit Structure

All commits follow this format:

```
[Type] Short descriptive title (under 72 chars)

Optional body with detailed explanation, implementation notes,
breaking changes, or migration instructions.
```

## Commit Types

### Added
For new features, functionality, or capabilities.

```bash
git commit -m "[Added] user authentication with JWT" -m "Implemented JWT-based auth with login/logout endpoints and token refresh"
```

### Changed
For changes in existing functionality, refactoring, or improvements.

```bash
git commit -m "[Changed] improved database query performance" -m "Added composite indexes, reduced query time from 250ms to 15ms"
```

### Deprecated
For features that will be removed in future releases.

```bash
git commit -m "[Deprecated] legacy API v1 endpoints" -m "Will be removed in v3.0. Migration guide: docs/migration.md"
```

### Removed
For removed features, code, or dependencies.

```bash
git commit -m "[Removed] support for Python 3.7" -m "Minimum version now 3.8. Updated CI/CD and docs."
```

### Fixed
For bug fixes and error corrections.

```bash
git commit -m "[Fixed] memory leak in WebSocket handler" -m "Fixed unclosed connections causing unbounded memory growth. Closes #1234"
```

## Quick Start

### Method 1: Interactive Helper Script (Recommended)

Use the bundled Python script for guided commit creation:

```bash
python scripts/commit.py
```

The script will:
1. Show staged files
2. Prompt for commit type selection
3. Ask for title and optional body
4. Preview and confirm before committing

### Method 2: Direct Command Line

For quick commits:

```bash
# Title only
python scripts/commit.py Added "user profile page"

# Title with body
python scripts/commit.py Fixed "login timeout" "Increased session timeout from 5 to 15 minutes"
```

### Method 3: Manual Git Commands

Standard git workflow with template:

```bash
# Stage changes
git add src/auth.py tests/test_auth.py

# Commit with template
git commit -m "[Added] two-factor authentication" \
  -m "Implemented TOTP-based 2FA with QR code generation and backup codes"
```

## Guidelines

### Title Best Practices
- Keep under 72 characters
- Use imperative mood: "add" not "added"
- Be specific: "[Fixed] null pointer in user parser" not "[Fixed] bug"
- No period at end
- Describe what changed, not how

### Body Best Practices
- Wrap at 72 characters
- Explain *why* the change was made
- Include breaking changes prominently
- Reference issue numbers: "Closes #123", "Fixes #456"
- Add migration instructions for deprecations
- Only add body for complex changes

### When to Use Each Type

**Added**: New endpoints, features, files, tests, documentation sections
**Changed**: Refactoring, performance improvements, API modifications, dependency updates
**Deprecated**: Marking features for future removal, providing migration paths
**Removed**: Deleting features, dropping support, removing dependencies
**Fixed**: Bug fixes, error corrections, security patches

## Common Patterns

### Breaking Changes

Always call out breaking changes:

```
[Changed] restructured API response format

BREAKING CHANGE: Response structure modified.
Old: { "user": {...} }
New: { "data": {...}, "meta": {...} }

Migration: Access response.data instead of response.user
```

### Multiple Related Changes

Group related changes in one commit with bullet points:

```
[Added] comprehensive logging system

- Structured logging with context
- Log rotation and archival
- Monitoring dashboard integration
- Performance metrics collection
```

### Security Fixes

Be cautious with details:

```
[Fixed] authentication bypass vulnerability

Fixed token validation issue. Details withheld per responsible
disclosure. See security advisory SA-2024-001.
```

## Workflow Integration

### Pre-commit Checks

The helper script automatically:
- Verifies staged files exist
- Validates commit type
- Ensures title is non-empty
- Shows file list in confirmation

### Git Hooks

Compatible with standard git hooks (pre-commit, commit-msg, etc.):

```bash
# Use --no-verify to skip hooks if needed
python scripts/commit.py Fixed "urgent hotfix" --no-verify
```

### Searching Commit History

The structured format makes history searchable:

```bash
# Find all new features
git log --oneline --grep="^\[Added\]"

# Find all bug fixes
git log --oneline --grep="^\[Fixed\]"

# Generate changelog
git log --oneline --grep="^\[Added\]\|^\[Changed\]\|^\[Fixed\]"
```

## Examples Reference

For comprehensive examples, best practices, and anti-patterns, see:
- **references/examples.md** - Detailed examples for each commit type with good/bad patterns

## Script Features

The `scripts/commit.py` helper provides:

- **Interactive mode**: Guided commit creation with prompts
- **Direct mode**: Command-line commit creation
- **Validation**: Type checking and staged file verification
- **Preview**: Show commit before creation
- **Multi-line bodies**: Support for detailed descriptions
- **Error handling**: Clear error messages and guidance
