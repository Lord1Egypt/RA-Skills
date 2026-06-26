status: closed

# PR-002: Robust PR Status Parsing (Write Side)

## 1. Objective
Fix the write-side PR status parsing to ensure we only update the status frontmatter and do not corrupt the PR body text containing phrases like "status: open".

## 2. Scope & Implementation Details
Modify the Python scripts that handle writing PR states:
1. **`scripts/orchestrator.py`**:
   - Locate the function `def set_pr_status(pr_file, new_status):`.
   - Update the substitution regex to `re.sub(r'^status:\s*\S+', f'status: {new_status}', content, count=1, flags=re.MULTILINE)`.
2. **`scripts/update_pr_status.py`**:
   - Update the search regex to `re.search(r'^status:\s*\S+', content, re.MULTILINE)`.
   - Update the substitution regex to `re.sub(r'^status:\s*\S+', f'status: {new_status}', content, count=1, flags=re.MULTILINE)`.

## 3. TDD & Acceptance Criteria
Extend the test script `tests/test_072_strict_status_parsing.sh` to include write-side assertions.
**Test Execution & Assertions**:
1. Run `python3 scripts/update_pr_status.py --pr-file docs/PRs/mock_072/PR_001_Mock.md --status in_progress`.
2. **Assertion 2**: Read the modified PR file. The first line MUST be `status: in_progress`. The body text `status: open` MUST NOT be changed to `status: in_progress`.