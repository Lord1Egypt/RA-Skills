status: closed

## 1. Objective
Create the strict Markdown template for Micro-PR contracts and update `create_pr_contract.py` to stop injecting hardcoded YAML frontmatter.

## 2. Scope & Implementation Details
- Create `TEMPLATES/PR_Contract.md.template` with the exact text specified in PRD-070.
- Edit `scripts/create_pr_contract.py` to remove `f.write("status_open_text\n\n")` when generating the PR contract.

## 3. TDD & Acceptance Criteria
- Create a test script `tests/test_070_pr1.sh` that calls `python3 scripts/create_pr_contract.py --workdir ... --job-dir ... --title ... --content-file ...` and verifies that `status_open_text` does not duplicate if the content already has it, or ensure the test verifies the removal of the hardcoded `status_open_text`.
- Assert that `TEMPLATES/PR_Contract.md.template` exists and contains the correct structure.
