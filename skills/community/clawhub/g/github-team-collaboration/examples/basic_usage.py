"""
Basic usage example for GitHub Team Collaboration
"""

from scripts.github_team import (
    list_open_prs,
    assign_reviewers,
    get_milestone_progress,
    get_team_metrics,
    list_issues,
    create_issue
)

# Example 1: List open pull requests
print("=" * 50)
print("Example 1: List Open Pull Requests")
print("=" * 50)
# prs = list_open_prs("octocat", "Hello-World")
# print(f"Found {len(prs)} open PRs")
print("Note: Replace 'octocat' and 'Hello-World' with your org/repo")
print()

# Example 2: Assign reviewers to a PR
print("=" * 50)
print("Example 2: Assign Reviewers")
print("=" * 50)
# result = assign_reviewers("octocat", "Hello-World", 42, ["alice", "bob"])
# print(f"Result: {result}")
print("Note: Set GITHUB_TOKEN environment variable first")
print()

# Example 3: Get milestone progress
print("=" * 50)
print("Example 3: Sprint/Milestone Progress")
print("=" * 50)
# progress = get_milestone_progress("octocat", "Hello-World", "Sprint-15")
# print(f"Progress: {progress['closed_issues']}/{progress['total_issues']}")
print("Note: Replace with your actual milestone title")
print()

# Example 4: Get team metrics
print("=" * 50)
print("Example 4: Team Metrics")
print("=" * 50)
# metrics = get_team_metrics("octocat", "Hello-World", days=30)
# print(f"Avg review time: {metrics['avg_review_time_hours']} hours")
# print(f"Contributors: {metrics['contributors']}")
print("Note: Requires valid GITHUB_TOKEN")
print()

# Example 5: List and create issues
print("=" * 50)
print("Example 5: Issue Management")
print("=" * 50)
# issues = list_issues("octocat", "Hello-World", state="open")
# print(f"Open issues: {len(issues)}")
# 
# new_issue = create_issue(
#     "octocat", "Hello-World",
#     title="Bug: Something is broken",
#     body="Detailed description here",
#     labels=["bug", "priority:high"]
# )
print("Note: Uncomment and customize for your repository")
