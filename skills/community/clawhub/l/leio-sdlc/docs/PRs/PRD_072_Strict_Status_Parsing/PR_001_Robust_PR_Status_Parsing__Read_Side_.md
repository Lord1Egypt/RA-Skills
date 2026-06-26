status: completed

# PR-001: Robust PR Status Parsing (Read Side)

## 1. Objective
Fix the SDLC crawler deadlock where the pipeline infinitely loops on a `completed` PR because the string "status: open" happens to appear in the PR's body markdown text. This PR focuses strictly on the read-side status parsing.

## 2. Scope & Implementation Details
Modify the Python script that reads PR states:
1. **`scripts/get_next_pr.py`**:
   - Replace the loose string check: `if "status: open" in content:`
   - With a strict anchored regex search: `if re.search(r'^status:\s*open\b', content, re.MULTILINE):`
   - Import `re` if not already imported.

## 3. TDD & Acceptance Criteria
Create the read-side portion of the test script: `tests/test_072_strict_status_parsing.sh`.
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
2. **Assertion 1**: The script MUST output `[QUEUE_EMPTY] All PRs in ... are closed or blocked.` (It must NOT output the PR filename).
3. Clean up the dummy directory and exit 0 if assertions pass.