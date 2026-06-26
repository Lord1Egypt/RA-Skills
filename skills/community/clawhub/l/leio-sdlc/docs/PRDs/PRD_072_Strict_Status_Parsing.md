# PRD-072: Robust PR Status Parsing (Fix Deadlock False Positives)

## 1. Objective
Fix the SDLC crawler deadlock where the pipeline infinitely loops on a `completed` PR because the string "status: open" happens to appear in the PR's body markdown text. We must enforce strict regex parsing (anchored to the beginning of lines) across all status-reading and status-writing scripts.

## 2. Scope & Implementation Details
You must modify three Python scripts that handle PR states:

1. **`scripts/get_next_pr.py`**:
   - Replace the loose string check: `if "status: open" in content:`
   - With a strict anchored regex search: `if re.search(r'^status:\s*open\b', content, re.MULTILINE):`
   - Import `re` if not already imported.

2. **`scripts/orchestrator.py`**:
   - Locate the function `def set_pr_status(pr_file, new_status):`.
   - Update the substitution regex from `re.sub(r'status:\s*\S+', ...)` to `re.sub(r'^status:\s*\S+', f'status: {new_status}', content, count=1, flags=re.MULTILINE)`.

3. **`scripts/update_pr_status.py`**:
   - Update the search regex from `re.search(r'status:\s*\S+', content)` to `re.search(r'^status:\s*\S+', content, re.MULTILINE)`.
   - Update the substitution regex from `re.sub(r'status:\s*\S+', ...)` to `re.sub(r'^status:\s*\S+', f'status: {new_status}', content, count=1, flags=re.MULTILINE)`.

## 3. TDD & Acceptance Criteria
Create a test script: `tests/test_072_strict_status_parsing.sh`.

**Test Setup**:
1. Initialize a dummy directory `/tmp/test_072_workspace_$$`.
2. Create a mock PR file `docs/PRs/mock_072/PR_001_Mock.md` with the following content:
```markdown
status: completed

# PR-001
This PR fixes the `status: open` bug.
The previous system falsely detected the text "status: open" in this sentence!
```

**Test Execution & Assertions**:
1. Run `python3 scripts/get_next_pr.py --workdir . --job-dir docs/PRs/mock_072`.
2. **Assertion 1**: The script MUST output `[QUEUE_EMPTY] All PRs in ... are closed or blocked.` (It must NOT output the PR filename, as its true frontmatter status is `completed`).
3. Run `python3 scripts/update_pr_status.py --pr-file docs/PRs/mock_072/PR_001_Mock.md --status in_progress`.
4. **Assertion 2**: Read the modified PR file. The first line MUST be `status: in_progress`. The body text `status: open` MUST NOT be changed to `status: in_progress`.
5. Clean up the dummy directory. If all assertions pass, the script exits `0`.