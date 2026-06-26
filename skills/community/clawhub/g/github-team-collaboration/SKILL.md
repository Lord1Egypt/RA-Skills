---
name: github-team-collaboration
description: GitHub team collaboration toolkit for managing team workflows, code reviews, issue tracking, sprint planning, and team metrics. Supports PR automation, issue triage, milestone management, and team productivity analytics. Use when teams need to coordinate development workflows, automate code review processes, track sprint progress, or analyze team collaboration metrics on GitHub.
---

# GitHub Team Collaboration

A comprehensive toolkit for managing GitHub team workflows, code reviews, and project coordination.

## Features

- **Pull Request Automation**: Auto-assign reviewers, check PR status, merge strategies
- **Issue Management**: Triage, label, assign, and track issues
- **Sprint Planning**: Milestone management, burndown charts, velocity tracking
- **Team Metrics**: PR review time, issue resolution time, contributor stats
- **Workflow Automation**: Branch protection, status checks, release management

## Usage

### Manage Pull Requests

```python
from scripts.github_team import list_open_prs, assign_reviewers

# List open PRs
prs = list_open_prs("myorg", "myrepo")

# Auto-assign reviewers
assign_reviewers("myorg", "myrepo", 123, ["alice", "bob"])
```

### Track Sprint Progress

```python
from scripts.github_team import get_milestone_progress

# Get sprint progress
progress = get_milestone_progress("myorg", "myrepo", "Sprint-15")
print(f"Closed: {progress['closed_issues']}/{progress['total_issues']}")
```

### Team Metrics

```python
from scripts.github_team import get_team_metrics

# Analyze team metrics
metrics = get_team_metrics("myorg", "myrepo", days=30)
print(f"Avg review time: {metrics['avg_review_time']} hours")
```

## GitHub API Authentication

Set your GitHub token as an environment variable:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

## Supported Operations

- Repository management
- Pull request lifecycle
- Issue tracking and triage
- Milestone and project management
- Team member activity
- Release management
- Webhook configuration
