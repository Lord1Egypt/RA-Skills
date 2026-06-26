---
name: git-conventions
description: Git commit message conventions and workflow rules. Use when making git commits, pushing changes, or performing git operations.
---

# Git Commit Conventions

## Commit Message Format

Use semantic commit format: `<type>(<scope>): <subject>`

### Commit Types

- `feat`: add new feature
- `fix`: correct bug
- `docs`: update documentation
- `style`: format code (no functional changes)
- `refactor`: restructure code
- `test`: add/modify tests
- `chore`: update build tasks

## Workflow Rules

1. **Language**: Use English only for git commit messages.

2. **Force Push**: Always confirm before `git push --force`.

3. **Sign-off**: Include `--signoff` flag with all commits.

4. **Consolidation**: Consolidate changes into meaningful commits.

5. **Push Confirmation**: After making a local commit, ALWAYS prompt the user whether they want to push to the remote repository.

6. **Display URL**: After successfully pushing to remote, display the repository's access URL.
