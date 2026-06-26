---
name: gitlab-code-review
description:
  Performs structured code reviews on GitLab Merge Requests. Use when the user provides
  a GitLab MR URL and wants to analyze the diff, generate engineering feedback, and/or
  post inline review comments back to the MR via GitLab API. Triggers on requests like:
  "review this MR", "check this merge request", "post review comments to GitLab",
  "analyze the diff at a gitlab URL", "do a code review for a merge request URL".
  Covers Java/Spring Boot, MongoDB, PostgreSQL, React, and TypeScript codebases.
---

# GitLab MR Code Review

## Workflow

### 1. Read credentials and check token scope

Credentials: `~/.openclaw/credentials/gitlab.json`

```json
{
  "token": "glpat-xxx",
  "host": "https://gitlab.com",
  "ignore_patterns": ["*.min.js", "*.lock", "forms/*.json"]
}
```

Required API scopes:
- `api` — required for posting inline comments
- `read_api` — sufficient for analysis only (no comment posting)

**Always run token check first** to know upfront whether comments can be posted:

```bash
python scripts/gitlab_client.py check-token <mr_url>
```

Output includes `"can_write": true/false`. If `false`, skip step 6 and inform the user that the token needs the `api` scope to post comments. Do NOT proceed to analysis and then fail at step 6.

### 2. Fetch MR metadata and diff

```bash
python scripts/gitlab_client.py fetch-mr   <mr_url>
python scripts/gitlab_client.py fetch-diff <mr_url>
```

`fetch-diff` returns a JSON array. Each entry contains `new_path`, `old_path`, `diff` (unified diff text), and boolean flags `new_file`, `deleted_file`, `renamed_file`.

> **Fallback**: if the `/diffs` endpoint returns HTTP 500 (some self-hosted GitLab instances), the script automatically retries via `/changes`. No manual intervention needed.

### 3. Filter files

Use `ignore_matcher.py` to exclude files before analysis:

```python
from ignore_matcher import filter_diffs
reviewable = filter_diffs(all_diffs)   # merges defaults + credentials ignore_patterns
```

**Default ignore patterns** (always applied, even without credentials file):
`*.min.js`, `*.min.css`, `*.lock`, `package-lock.json`, `pnpm-lock.yaml`, `forms/*.json`

Binary extensions (`.png`, `.jar`, `.class`, `.map`, etc.) are always skipped.

### 4. Analyze the diff

- Analyze only modified lines (added/removed in the diff). Do not comment on unchanged context lines.
- If the total diff is large, process file-by-file and aggregate results.
- Read `references/review-guidelines.md` for all review rules, severity definitions, and comment format.

**Focus areas:**
- Java / Spring Boot — Clean Code, SOLID, transaction boundaries, lazy loading
- MongoDB — query correctness, index coverage, atomicity
- PostgreSQL — SQL correctness, isolation levels, index/schema migrations
- React / TypeScript — hooks correctness, type safety, XSS, stale closures

### 5. Structure the chat summary

Group findings by severity:

```
## Code Review — <MR title> (<source_branch> → <target_branch>)

### Critical
- `UserService.java:42` — Transaction wraps HTTP call; holds DB lock during network I/O.

### Major
- `OrderRepository.java:87` — N+1: `findRolesByUserId` called inside loop. Use batch query.

### Minor
- `PaymentDto.java:15` — Field name `val` is not descriptive.

### Decision: Needs changes
```

Decision options: **Pass** / **Needs changes** / **Reject**
- Pass: no Critical or Major findings
- Needs changes: one or more Major findings, no Critical
- Reject: one or more Critical findings

### 6. Post inline comments to GitLab

Only execute this step if `check-token` (step 1) returned `"can_write": true`.

**Write comments to a temp JSON file, then post via `post_comments.py`.**
Never use `python -c` with inline comment bodies — backticks and special characters break shell escaping.

```bash
# 1. Write all findings to a JSON file
cat > /tmp/mr_comments.json << 'EOF'
[
  {
    "file_path": "src/main/UserService.java",
    "line": 42,
    "body": "[CRITICAL] Transaction wraps HTTP call...\n\nSuggestion:\n```java\n// fix\n```"
  }
]
EOF

# 2. Post via script
python scripts/post_comments.py <mr_url> /tmp/mr_comments.json
```

**How to determine the correct line number** from a diff hunk:

```
@@ -375,6 +375,8 @@       ← new file starts at line 375
     unchanged line          → 375
     unchanged line          → 376
     unchanged line          → 377
+    added line              → 378  ← use this number
+    added line              → 379
```

Count from the `+A` value in `@@ -X,Y +A,B @@` for new-file lines.

Each comment body format (from `references/review-guidelines.md` §8):

```
[SEVERITY] <one-line issue>

<2-4 sentence explanation referencing the diff.>

Suggestion:
```<language>
<corrected snippet>
```
```

**Constraints:**
- Do not auto-approve the MR.
- Do not add labels or trigger pipelines.
- Only post comment-type discussions (no approval API calls).
- If a line is not in the diff, the API returns an error — log it and continue with the next comment.
- On HTTP 403 `insufficient_scope`, the script stops immediately and prints a fix instruction. Do not retry.

## Behavior Rules

- Strict engineering tone. No emotional language. No generic praise.
- Analyze only the modified code in the diff. Do not speculate about code outside the diff.
- Do not log or persist source code content.
- Respect ignore patterns strictly.
- For large diffs: process per file, deduplicate similar findings across files before final output.

## References

- **Review rules, severity table, comment format**: `references/review-guidelines.md`
  - §2 Java & Spring Boot (Clean Code, transactions, N+1, concurrency)
  - §3 MongoDB (queries, indexes, atomicity)
  - §4 PostgreSQL (SQL correctness, isolation, migrations)
  - §5 React & TypeScript (hooks, type safety, security)
  - §6 SOLID & DDD alignment
  - §7 Severity classification table
  - §8 Inline comment format template
