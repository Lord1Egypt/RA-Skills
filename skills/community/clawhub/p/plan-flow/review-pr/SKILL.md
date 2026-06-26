---
name: review-pr
description: Review a Pull Request
metadata: {"openclaw":{"requires":{"bins":["git","gh"]}}}
user-invocable: true
---

# Review PR

Review a Pull Request by its number using the GitHub CLI.

## What It Does

1. Fetches PR information using `gh pr view`
2. Gets PR diff using `gh pr diff`
3. Analyzes changes against project patterns
4. Checks for security and performance issues
5. Provides detailed findings and recommendations
6. Generates a review document

## Usage

```
/review-pr <pr_number>
```

**Arguments:**
- `pr_number` (required): The PR number to review

## Prerequisites

- `gh` CLI must be installed and authenticated
- Run `gh auth login` if not authenticated

## Output

Creates: `flow/reviewed-pr/pr_<number>.md`

## Review Focus Areas

| Area | What's Checked |
|------|----------------|
| Code Quality | Pattern consistency, naming, organization |
| Security | Secrets, injection, authentication |
| Performance | N+1 queries, unnecessary loops, caching |
| Testing | Test coverage, edge cases |
| Documentation | Comments, README updates |

## Review Document Structure

```markdown
# PR Review: #<number>

## PR Information
| Field | Value |
|-------|-------|
| Title | PR title |
| Author | username |
| Branch | feature -> main |
| Files Changed | N |

## Summary
What this PR does

## Findings

### Finding 1: [Name]
| Field | Value |
|-------|-------|
| File | path/to/file |
| Severity | Major |

**Description**: What's wrong
**Suggested Fix**: How to fix it

## Security Considerations
Any security concerns

## Performance Considerations
Any performance concerns

## Recommendation
| Status | Approve / Request Changes / Comment |
```

## Example

```
/review-pr 123
```

**Output:**
```
Reviewing PR #123...

Fetching PR information...
Fetching PR diff...
Analyzing changes...

PR #123 Review Complete!

Summary: Adds user authentication with OAuth
Files Changed: 12
Findings: 2 Major, 3 Minor

Review saved to: flow/reviewed-pr/pr_123.md

Recommendation: Request Changes
- Fix the 2 major issues before merging
```

## Authentication

If you get authentication errors:

```bash
# Authenticate with GitHub
gh auth login

# Verify authentication
gh auth status
```
