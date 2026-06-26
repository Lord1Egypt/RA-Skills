# PR Review Assistant

Automated pull request review with structured feedback on code quality, security, performance, and best practices. Use when reviewing PRs, preparing code for review, or setting up automated review workflows.

## Usage

```bash
# Review current branch changes against main
python3 scripts/pr_review.py

# Review specific PR (requires gh CLI)
python3 scripts/pr_review.py --pr 42

# Review staged changes only
python3 scripts/pr_review.py --staged

# Review with specific focus areas
python3 scripts/pr_review.py --focus security,performance
```

## Review Categories

The assistant evaluates code across 6 dimensions:

### 1. Correctness
- Logic errors, off-by-one, null handling
- Missing edge cases
- Incorrect type usage

### 2. Security
- Injection vulnerabilities (SQL, XSS, command)
- Hardcoded secrets or credentials
- Insecure deserialization
- Missing input validation

### 3. Performance
- N+1 queries, unnecessary loops
- Memory leaks, unbounded growth
- Missing indexes on queried fields
- Inefficient algorithms

### 4. Maintainability
- Dead code, unused imports
- Functions doing too much
- Unclear naming
- Missing or excessive comments

### 5. Testing
- Are new code paths covered?
- Missing edge case tests
- Test quality (assertions, mocking)

### 6. Best Practices
- Framework-specific patterns
- Error handling conventions
- API design consistency
- Documentation updates needed

## Output Format

```markdown
## PR Review Summary

**Risk Level:** 🟢 Low / 🟡 Medium / 🔴 High

### Must Fix (blocking)
- [file:line] Description of critical issue

### Should Fix (non-blocking)
- [file:line] Description of improvement

### Consider (optional)
- [file:line] Suggestion for better approach

### Positive Notes
- What was done well
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--pr` | GitHub PR number | None (uses diff) |
| `--base` | Base branch to compare | `main` |
| `--staged` | Review staged changes only | false |
| `--focus` | Comma-separated focus areas | All |
| `--severity` | Minimum severity to report | `low` |
| `--format` | Output format: `markdown`, `json`, `github-comment` | `markdown` |
| `--max-files` | Max files to review | 50 |

## AI Enhancement

When used as an agent skill, the AI reviewer:
- Understands project context from surrounding code, not just the diff
- Identifies patterns across multiple changed files
- Suggests specific code fixes, not just descriptions of problems
- Learns from repository conventions and applies them consistently
- Generates review comments in the project's preferred style
