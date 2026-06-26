---
name: smart-commit
description: "Analyze staged git changes and generate high-quality commit messages following Conventional Commits format. Use when: (1) user asks to commit changes, (2) user wants a commit message generated, (3) user says 'smart commit' or 'auto commit', (4) user asks to describe staged changes. Supports feat/fix/refactor/docs/chore/test/style/perf/ci/build types with optional scope and breaking change detection."
---

# Smart Commit

Generate precise, conventional commit messages from staged git changes and optionally commit in one step.

## Workflow

1. Run `git diff --cached --stat` to see what's staged. If nothing is staged, check `git diff --stat` and ask the user if they want to stage all changes first.
2. Run `git diff --cached` to get the full diff (if very large, use `--stat` summary + sample key hunks).
3. Analyze the diff and generate a commit message following the rules below.
4. Present the message to the user. If approved, run `git commit -m "<message>"`.

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Rules

- **type**: One of `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `style`, `perf`, `ci`, `build`
- **scope**: Optional. Infer from changed files (e.g., `auth`, `api`, `ui`, `db`). Omit if changes span too many areas.
- **subject**: Imperative mood, lowercase, no period, max 72 chars. Be specific — not "update files" but "add retry logic to HTTP client".
- **body**: Add only when the "why" isn't obvious from the subject. Wrap at 72 chars.
- **breaking changes**: Add `!` after type/scope and `BREAKING CHANGE:` footer.
- **Multiple logical changes**: If the diff contains clearly unrelated changes, suggest splitting into multiple commits with `git add -p`.

### Type Selection Guide

| Signal | Type |
|--------|------|
| New feature, new endpoint, new UI element | `feat` |
| Bug fix, error correction, patch | `fix` |
| Code restructure, no behavior change | `refactor` |
| Comments, README, docs, JSDoc | `docs` |
| Dependencies, configs, tooling | `chore` |
| Test files added/modified | `test` |
| Formatting, whitespace, linting | `style` |
| Performance improvement | `perf` |
| CI/CD pipeline changes | `ci` |
| Build system, compilation | `build` |

### Quality Checklist

Before presenting the message, verify:

- [ ] Subject is specific and descriptive (someone reading `git log --oneline` can understand the change)
- [ ] Type accurately reflects the change
- [ ] Scope is correct or intentionally omitted
- [ ] No vague words: "update", "change", "modify", "fix stuff", "misc"
- [ ] Breaking changes are flagged if applicable

## Examples

**Single file fix:**
```
fix(auth): handle expired JWT tokens in refresh flow
```

**Multi-file feature:**
```
feat(api): add pagination support to list endpoints

Implement cursor-based pagination for /users, /posts, and /comments.
Default page size is 20, max 100.
```

**Breaking change:**
```
feat(config)!: migrate from YAML to TOML configuration

BREAKING CHANGE: config.yaml is no longer supported.
Run `migrate-config` to convert existing configs.
```

**Chore:**
```
chore(deps): bump express from 4.18.2 to 4.19.0
```

## Large Diffs

For diffs exceeding ~4000 lines:

1. Use `git diff --cached --stat` for overview
2. Read key files with `git diff --cached -- <important-file>` 
3. Summarize the overall change from the stat + sampled hunks
4. If changes are too diverse, recommend splitting the commit

## Options

The user may specify preferences:

- **`--no-body`**: Skip the body, subject only
- **`--scope <name>`**: Force a specific scope
- **`--type <type>`**: Force a specific type
- **`--amend`**: Amend the previous commit instead
- **`--dry-run`**: Generate message without committing
