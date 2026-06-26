# Git Workflows Reference

## Conventional Commits Specification

**Format:**
```
<type>(<scope>): <description>
```

**Optional extensions:**
- Body: Provide context, motivation, trade-offs
- Footer: Breaking changes, issue references

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring, no behavior change
- `test`: Adding or fixing tests
- `chore`: Maintenance, tooling, deps

### Examples

```
feat(auth): add OAuth2 provider support

Implemented Google and GitHub OAuth providers.
Uses PKCE flow for security.

Closes #123
```

```
fix(parser): handle null values in JSON response

Added null checks before parsing nested objects.
Prevents TypeError on malformed API responses.
```

```
chore(deps): update axios to v1.6.0
```

## Branch Strategy

### Main Branches
- `main` / `master` - Production-ready code
- `develop` - Integration branch (optional)

### Feature Branches
```
git checkout -b feat/<feature-name>
# work...
git add -A
git commit -m "feat: implement feature"
git push -u origin feat/<feature-name>
# PR to main
```

### Hotfix Branches
```
git checkout -b hotfix/<issue> main
# fix...
git commit -m "fix: critical production issue"
git push -u origin hotfix/<issue>
# PR to main + develop
```

## Safe Rebase Workflow

1. **Check current state:**
   ```
   git status
   git log --oneline -5
   ```

2. **Backup branch:**
   ```
   git branch backup-<branchname>
   ```

3. **Interactive rebase:**
   ```
   git rebase -i HEAD~N
   ```

4. **Verify:**
   ```
   git log --oneline -5
   git diff HEAD~5
   ```

5. **Force push (only if safe):**
   ```
   git push --force-with-lease
   ```

## Conflict Resolution

1. **During rebase/merge:**
   ```
   git status  # shows conflicted files
   ```

2. **Manual edit:**
   - Open conflicted files
   - Resolve `<<<<<<<`, `=======`, `>>>>>>>` markers

3. **Mark resolved:**
   ```
   git add <resolved-file>
   ```

4. **Continue:**
   ```
   git rebase --continue
   # or
   git merge --continue
   ```

5. **Abort if needed:**
   ```
   git rebase --abort
   git merge --abort
   ```

## Daily Workflow

```bash
# Morning sync
git checkout main
git pull --rebase

# Start feature
git checkout -b feat/your-feature

# Work cycle
git add -p
git commit -m "feat: description"

# End of day
git push -u origin feat/your-feature
```

## Common Patterns

### Undo last commit (keep changes)
```
git reset --soft HEAD~1
```

### Discard last commit and changes
```
git reset --hard HEAD~1
```

### View commit history
```
git log --oneline --graph --all -20
```

### Stash changes
```
git stash
git stash list
git stash pop
```