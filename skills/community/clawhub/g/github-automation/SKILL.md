---
name: github-automation
description: Automate common GitHub tasks — create issues, check PR status, list repos, manage projects. Use when the user wants to interact with GitHub programmatically without opening the browser.
---

# GitHub Automation

Streamline GitHub workflows from the command line. Create issues, check PRs, manage repos without switching contexts.

## Usage

```
create issue: fix login bug
check my prs
list repos
close issue #123
```

## Features

### Issues
- Create issues with title/body/labels
- List open/closed issues
- Close or comment on issues
- Search issues

### Pull Requests
- Check PR status and reviews
- List open PRs
- Comment on PRs
- Check merge status

### Repositories
- List user/org repos
- Check repo stats
- Get recent commits
- Check branch status

### User
- Check notifications
- Get user profile info
- List starred repos

## Script

```python
# Create issue
python scripts/gh_tool.py issue create "Title" "Body" --repo owner/repo --labels bug

# List PRs
python scripts/gh_tool.py pr list --repo owner/repo

# Check notifications
python scripts/gh_tool.py notifications
```

## Authentication

Uses GITHUB_TOKEN environment variable. Set it in your env:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

## Token Permissions Needed

- `repo` - Repository access
- `issues` - Issue management  
- `pull_requests` - PR access
- `notifications` - Read notifications

## Examples

```
create issue in myrepo: bug - login fails with 500 error
check prs for pollinations/pollinations.ai
list my repos
close issue #42 in cloudgptapi
```

## Output

- Success/failure confirmation
- Issue/PR numbers and URLs
- Formatted lists with key info
- Direct links to GitHub