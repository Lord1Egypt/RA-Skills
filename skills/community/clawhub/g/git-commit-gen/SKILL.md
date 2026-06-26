---
name: commit-message-writer
description: "Generate conventional, descriptive commit messages from git diffs. Analyzes staged changes or branch diffs and produces well-formatted commit messages following the Conventional Commits specification (feat, fix, chore, docs, refactor, test, etc.). Use when the user wants to: (1) Generate a commit message from 'git diff --staged', (2) Write a message for unpushed commits, (3) Rewrite a vague commit message, (4) Generate changelog entries from a range of commits, (5) Ensure team consistency with Conventional Commits. Best for developers, teams using standardized commit conventions, open-source maintainers, and anyone tired of 'fixed stuff' commit messages."
version: 1.0.0
homepage: https://clawhub.ai
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins:
        - git
---

# Commit Message Writer

Generate **conventional, descriptive, and scoped** commit messages from your git diffs — no more "fixed bug" or "updated files".

## When to Use

✅ **USE this skill when:**

- "Write a commit message for my staged changes"
- "Generate a commit message from this diff"
- "Rewrite my last commit message to be conventional"
- "Generate changelog-style messages for commits abc..def"
- "Summarize what changed in this branch"
- "Generate messages for all unpushed commits"
- "Check if my commit message follows conventions"

❌ **DON'T use this skill when:**

- Need sweeping refactors explained → use a code review skill
- Need full changelog generation between releases → use a release tool
- Working on binary-only repos (no meaningful diff)

## How It Works

1. Reads the git diff (staged, branch, or provided inline)
2. Analyzes what files changed, what functions/classes were affected, and the nature of each change
3. Constructs a **Conventional Commits** message:
   ```
   <type>(<scope>): <short summary>

   <body>

   <footer>
   ```
4. Explains the reasoning so you can review before committing

## Available Actions

### `write:staged`
Read `git diff --staged` and generate a commit message.

```
Write a commit message for my staged changes
```
→ Analyzes staged diff, outputs a formatted commit message with type, scope, description, and body.

### `write:diff`
Read changes between the current branch and its base (main/master).

```
Summarize all changes in this branch as a commit message
```

### `write:range`
Generate a changelog or multiple commit messages for a range of commits.

```
Generate conventional commit messages for commits HEAD~5..HEAD
```

### `write:provided`
Given an inline diff or file list, generate a commit message.

```
Here's a diff: [...paste diff...]. Write a commit message.
```

### `rewrite:last`
Improve the last commit message to follow conventions.

```
Rewrite my last commit message in conventional format
```

### `validate`
Check whether a message follows Conventional Commits.

```
Validate this message: "fix(api): handle null pointer in user lookup"
```
→ Confirms it's valid, or explains what to fix.

## Commit Type Reference

| Type       | Usage                                           |
|------------|-------------------------------------------------|
| `feat`     | A new feature                                   |
| `fix`      | A bug fix                                       |
| `docs`     | Documentation only changes                      |
| `style`    | Formatting, missing semicolons, etc. (no logic) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf`     | Code change that improves performance           |
| `test`     | Adding or correcting tests                      |
| `chore`    | Build, CI, dependencies, tooling                |
| `ci`       | CI/CD configuration changes                     |

## Example

> User: "Write a commit message for my staged changes"
>
> Assistant: *(runs `git diff --staged`, analyzes changes)*
>
> ```
> feat(auth): add OAuth2 refresh token rotation
>
> - Implement refresh token rotation on every token refresh
> - Invalidate old refresh tokens immediately after use
> - Add TTL config for refresh tokens (default 30 days)
> - Update token endpoint to return rotated refresh token
>
> Closes: #452
> ```

## Notes

- Always shows you the proposed message before suggesting you run `git commit`.
- Respects `.gitignore` — won't try to diff ignored files.
- For large diffs (>500 lines), summarizes chunk-level changes rather than line-by-line.
