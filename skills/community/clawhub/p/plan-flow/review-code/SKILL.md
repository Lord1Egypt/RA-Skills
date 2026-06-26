---
name: review-code
description: Review local uncommitted code changes
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---

# Review Code

Review local uncommitted changes in the repository.

## What It Does

1. Gets git diff of changes (staged, unstaged, or all)
2. Identifies changed files and their patterns
3. Finds similar implementations in the codebase
4. Reviews against project patterns and rules
5. Provides findings with severity and fix suggestions
6. Generates a review document

## Usage

```
/review-code [path] [scope]
```

**Arguments:**
- `path` (optional): Specific file or directory to review
- `scope` (optional): `staged`, `unstaged`, or `all` (default: all)

## Output

Creates: `flow/reviewed-code/review_<scope>.md`

## Review Categories

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| Critical | Security issues, major bugs | Must fix before commit |
| Major | Significant problems | Should fix |
| Minor | Code quality issues | Consider fixing |
| Suggestion | Improvements | Optional |

## Review Document Structure

```markdown
# Code Review: [Scope]

## Review Information
| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Files Reviewed | N |
| Scope | all/staged/unstaged |

## Changed Files
| File | Status | Lines Changed |
|------|--------|---------------|
| path/to/file | modified | +10/-5 |

## Findings

### Finding 1: [Name]
| Field | Value |
|-------|-------|
| File | path/to/file |
| Line | 42 |
| Severity | Major |
| Fix Complexity | 3/10 |

**Description**: What's wrong
**Suggested Fix**: How to fix it

## Commit Readiness
| Status | Ready to Commit / Needs Changes |
```

## Example

```
/review-code
```

**Scoped review:**
```
/review-code src/components staged
```

## What It Checks

- Pattern consistency with existing codebase
- Error handling completeness
- Type safety (for TypeScript)
- Security concerns (hardcoded secrets, injection risks)
- Performance considerations
- Code organization and naming

## Next Command

After fixing issues, commit your changes or run `/review-pr` after creating a PR.
