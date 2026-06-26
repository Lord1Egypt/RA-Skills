---
name: git-workflow
description: >-
  Use this skill for any git commit, pull request, or release task. Invoke
  immediately when the user wants to: stage and commit changes, write a commit
  message, push code, create a PR or MR, tag a release, or update CHANGELOG.
  Triggers on: 「帮我提交」「commit」「提交代码」「创建 PR」「发布版本」「打 tag」
  「推代码」, or English equivalents like "commit my changes", "create a pull
  request", "release v", "write a commit message", "push this branch". Do NOT
  trigger for: bulk repo syncing (use code-sync), general git questions without
  commit/PR intent, or Yunxiao MR creation (use yunxiao skill).
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["git"],"anyBins":["gh"]}}}
---

# Git Workflow

Standardized Git workflow for commits, pull requests, and releases using conventional commits format and semantic versioning.

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| git | cli | Yes | `brew install git` or [git-scm.com](https://git-scm.com/) |
| gh | cli | No | `brew install gh` then `gh auth login` (required for PR and Release) |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## When to Use

- **Creating commits**: Follow conventional commits with concise, imperative messages
- **Creating pull requests**: Generate PR with clear description and test plan
- **Creating releases**: Update versions, CHANGELOG, tags, and GitHub releases

These workflows can be used independently or together as needed.

## Platform Detection

Check `git remote get-url origin` to select workflow:

| Remote URL contains | Commits/Tags/Releases | PR/MR                            |
| ------------------- | --------------------- | -------------------------------- |
| `github.com`        | This skill            | This skill (`gh pr create`)      |
| `codeup.aliyun.com` | This skill            | **Switch to `yunxiao` skill**    |
| `gitlab.com`        | This skill            | This skill (adapt for GitLab CLI) |

## Quick Reference

### Commit Format

```text
type(scope): concise summary

- Optional bullet points (max 3-4)
- Keep short and focused
```

**Types**: feat, fix, refactor, docs, test, chore, style, ci, perf, build, revert

### Branch Naming

- `feature/description`
- `fix/description`
- `docs/description`
- `refactor/description`
- `test/description`

### Release Checklist

1. Update version in project files
2. Update CHANGELOG.md
3. Commit: `chore(release): bump version to x.y.z`
4. Tag: `git tag v{version} && git push upstream v{version}`
5. Create GitHub release with `gh release create`

## Default Behaviors

- **Keep messages concise**: Commit messages and PR titles must be short and to the point. Omit filler words. The diff shows "what" — the message explains "why".
- **No AI signatures**: Never include `Co-Authored-By: Claude`, `Generated with Claude Code`, or any AI markers in commits or PRs.
- **Commit always pushes**: After commit, always push immediately. Do not ask.
  - Has upstream tracking → `git push`
  - No upstream tracking → `git push -u origin <branch>`
- **Single-purpose commits**: Each commit does one thing. If a change spans multiple types or scopes, split into separate commits before pushing.
- **PR/MR description is prose, not template**: subject + 2-3 declarative sentences explaining *why* + one `验证：` / `Verify:` line. No markdown section headings inside the description, no emoji-bullets, no commit-list copy-paste. Full schema and forbidden patterns in [examples-and-templates.md](references/examples-and-templates.md#pr-description).

## Detailed Guides

See [examples-and-templates.md](references/examples-and-templates.md) for commit examples (good/bad), PR body template, and CHANGELOG format.

## Validation

Use `scripts/validate_commit.py` to validate commit messages:

```bash
python3 scripts/validate_commit.py "feat(auth): add OAuth2 support"
python3 scripts/validate_commit.py --file .git/COMMIT_EDITMSG
```

The validator checks:

- Conventional commits format
- Subject line length (< 72 chars)
- Imperative mood usage
- Absence of AI-generated markers
- Body format and bullet point count

## Common Workflows

### Commit (default: commit + push)

```bash
git add <files>
git commit -m "feat(component): add new feature" && git push
```

### Pull Request

```bash
git checkout -b feature/new-feature
# ... make changes, commit (auto-pushes per default behavior) ...
gh pr create --title "feat(component): add new feature" --body "..."
```

### Release

```bash
# Update version files + CHANGELOG.md
git add .
git commit -m "chore(release): bump version to 1.2.0" && git push
git tag v1.2.0 && git push upstream v1.2.0
gh release create v1.2.0 -R owner/repo --title "v1.2.0" --notes "..."
```

## Common Issues

| Issue | Cause | Fix |
| ----- | ----- | --- |
| Subject line > 72 chars | Description too long | Shorten summary, put details in body |
| Multiple types in one commit | Scope too large | Split into single-purpose commits |
| Merge commits appear | Used merge | Use `git pull --rebase` |
| Validator script errors | Format mismatch | Check type(scope): format |
