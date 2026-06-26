# GitHub PR Automation Skill

A skill for automating GitHub open-source contributions - from finding good first issues to submitting PRs.

## Trigger Words

"开源贡献", "GitHub贡献", "find issue", "good first issue", "提交PR", "贡献项目"

## Overview

This skill helps you:
1. Search GitHub for good first issues
2. Analyze project activity and difficulty
3. Fork, clone, and create branches
4. Implement the fix
5. Submit Pull Request
6. Set up daily contribution cron jobs

## Workflow

### Phase 1: Search & Filter

Search for good first issues using GitHub CLI:

```bash
gh search issues "label:good-first-issue language:python created:>2026-01-01"
gh search repos "good first issue" --limit 20
```

Selection criteria:
- Project activity (recent commits in 3 months)
- Language match (Python, JS, Go, etc.)
- Response speed (maintainers active on issues)
- Appropriate difficulty (clear scope, not refactoring entire codebase)

Output: 3-5 candidate issues with links, tech stack, and recommendations.

### Phase 2: Analysis & Planning

1. Read project docs: README.md, CONTRIBUTING.md
2. Clone and explore locally
3. Create implementation plan
4. Draft a comment for the issue (in English)

Example issue comment:
```
Hi! I'd like to work on this issue. I plan to...

My approach:
1. ...
2. ...

Is this direction okay?
```

### Phase 3: Development

1. Fork: `gh repo fork owner/repo`
2. Clone: `gh repo clone yourname/repo`
3. Branch: `git checkout -b fix/issue-xxx`
4. Implement fix
5. Test locally if possible
6. Commit: Follow Conventional Commits

Example commit message:
```
feat: add audio resampling utility

- Add resample_wav() function with linear interpolation
- Add resample CLI command

Assisted development. Original: owner/repo (MIT License)
Ref: https://github.com/owner/repo/issues/123
```

### Phase 4: Submit PR

1. Push: `git push -u origin fix/issue-xxx`
2. Try to create PR via gh:

```bash
# Method 1: gh pr create (if token has repo scope)
gh pr create --title "feat: description" --body "PR description"

# Method 2: Use gh api directly
gh api repos/OWNER/repo/pulls -X POST -f title="PR title" -f body="PR body" -f head="branch-name" -f base="main"

# Method 3: If all above fails, provide manual link
echo "PR creation failed. Create manually at: https://github.com/OWNER/repo/pull/new/branch-name"
```

If token lacks `repo` scope, PR creation will fail. Always provide manual link as fallback.

PR description template:
```markdown
## Summary

Brief description of changes.

## Changes

- Change 1
- Change 2

## Testing

How was this tested?

## Declaration

This is assisted development. Original project: owner/repo (LICENSE)
Reference: https://github.com/owner/repo/issues/123
```

### Phase 5: Daily Cron Job

Set up daily contribution task:

```bash
cron add --name "Daily GitHub Contribution" \
  --schedule "0 8 * * *" \
  --timezone "Asia/Shanghai" \
  --message "Search for good first issues and contribute..." \
  --channel "qqbot"
```

## Important Notes

1. **Respect licenses**: MIT, Apache 2.0, GPL, etc.
2. **Follow CONTRIBUTING.md**: Read and adhere to guidelines
3. **Communicate first**: Comment on issue before writing code
4. **Declare assisted development**: Always credit original authors
5. **Quality over quantity**: Test code, run linters

## Tools Used

- `gh` - GitHub CLI for all GitHub operations (primary tool)
- `git` - Version control
- Web search/fetch - For finding issues
- `gh api` - Direct GitHub API calls as fallback for PR creation

## Constraints

- Token needs `repo` scope for full automation
- Some operations may require manual intervention if token lacks permissions
- Always clean up local files after contribution

---

*Last updated: 2026-03-17*
