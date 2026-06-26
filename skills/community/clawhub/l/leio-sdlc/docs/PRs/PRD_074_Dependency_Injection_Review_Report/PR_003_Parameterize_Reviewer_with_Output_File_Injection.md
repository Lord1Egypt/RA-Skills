status: closed

# PR-001: Parameterize Reviewer with Output File Injection

## 1. Objective
Enable `spawn_reviewer.py` to accept a dynamically injected output file path via a new command-line argument, replacing the hardcoded `Review_Report.md`.

## 2. Scope & Implementation Details
- **Target File:** `scripts/spawn_reviewer.py`
- **Implementation:** 
  - Add an `--out-file` argument (e.g., using `argparse`).
  - Default to `Review_Report.md` if not provided (for backward compatibility).
  - Inject this `out_file` path into the LLM system prompt/instructions so the model knows exactly where to write its output.

## 3. TDD & Acceptance Criteria
- **Target File:** `tests/test_074_reviewer_injection.sh` (New)
- **Assertions:**
  - Test that running `python3 scripts/spawn_reviewer.py --out-file custom_report.md` parses the argument correctly.
  - Assert that the script instructs the mock/LLM to write to the specified injected path.