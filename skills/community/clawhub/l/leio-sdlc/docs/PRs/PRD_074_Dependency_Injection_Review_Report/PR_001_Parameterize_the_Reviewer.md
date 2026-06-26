status: completed

# PR-001: Parameterize the Reviewer

## 1. Objective
Enable the AI Reviewer to accept a dynamic output file path via dependency injection.

## 2. Scope & Implementation Details
- **File**: `scripts/spawn_reviewer.py`
- **Logic**: Add an `--out-file` CLI argument. Modify the AI prompt instructions to explicitly tell the model to write its final review artifact to the path specified by `--out-file` (defaulting to `Review_Report.md` if not provided). Ensure the reviewer script correctly passes this to the LLM.

## 3. TDD & Acceptance Criteria
- **Test**: Create `tests/test_074_reviewer_injection.sh`.
- **Criteria**: The test must invoke `spawn_reviewer.py --out-file custom_report.md` with a mocked LLM response, verifying that the output is written exactly to `custom_report.md`. The test must fail before the implementation and pass after.
