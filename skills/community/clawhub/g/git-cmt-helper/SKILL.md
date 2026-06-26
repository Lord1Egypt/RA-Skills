---
name: git-commit-helper
description: >
  Generate standardized git commit messages following Conventional Commits format.
  Use this skill when the user asks to commit code, write a commit message,
  or create a git commit. Enforces team conventions for type prefixes,
  scope naming, message length, and breaking change documentation.
---

# Git Commit Message Guide

## Format

Every commit message MUST follow this structure:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Type (required)

| Type | When to use |
|------|-------------|
| feat | New feature or capability |
| fix | Bug fix |
| docs | Documentation only |
| refactor | Code change that neither fixes nor adds |
| test | Adding or updating tests |
| chore | Build, CI, tooling changes |

## Scope (required)

Scope MUST be a real module name from this project.
See [references/modules.md](references/modules.md) for the full list.

If unsure of the scope, check the file paths being changed — the top-level directory is usually the correct scope.

## Subject (required)

- Imperative mood: "add feature" not "added feature"
- No period at the end
- Max 72 characters total (including type and scope prefix)
- Lowercase first letter

## Body (optional)

- Explain WHY, not WHAT (the diff shows what changed)
- Wrap at 72 characters
- Separate from subject with blank line

## Breaking Changes

If the commit introduces a breaking change, add footer:

```
BREAKING CHANGE: <description of what breaks and migration path>
```

## Examples

**Good:**

```
feat(auth): add JWT token refresh endpoint

Tokens now auto-refresh 5 minutes before expiry.
Previously users had to re-login after token expiration.
```

```
fix(parser): handle empty input without crashing
```

```
refactor(db): extract connection pooling to separate module

BREAKING CHANGE: DatabaseClient constructor no longer accepts
pool config. Use PoolConfig.create() instead.
```

**Bad:**

```
updated some stuff          ← no type, no scope, vague
feat: Add new Feature.      ← capitalized, period, missing scope
fix(misc): various fixes    ← "misc" is not a real module
```
