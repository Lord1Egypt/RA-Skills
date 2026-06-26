# PRD_037: The Micro-Slicing Act (Planner Multi-PR Enforcement)

## 1. Problem Statement
The CI pipeline backend is now a continuous Queue Polling Engine capable of processing multiple PR contracts sequentially (ISSUE-028 & ISSUE-034). However, the `leio-sdlc` Planner agent still functions as a monolithic generator. When fed a complex Product Requirements Document (PRD), it tends to compress all requirements into a single, massive `PR_001_xxx.md` file. This overloads the Coder and breaks the core philosophy of iterative Test-Driven Development (TDD). 

We need to enforce a "Micro-Slicing Act" on the Planner: it must slice a PRD into multiple, focused, and independently verifiable PR contracts.

## 2. Solution: Prompt Engineering & Contract Verification

### 2.1 Prompt Upgrade (The Micro-Slicing Act)
We will modify the Planner's system prompt (likely inside `scripts/spawn_planner.py` or its corresponding playbook).
- **Core Instruction**: "You are forbidden from generating a single monolithic PR contract. You must break the PRD down into a sequential, dependency-ordered chain of Micro-PRs (e.g., Database Schema -> Core Logic -> API Endpoints -> UI Integration)."
- **Output Format**: Ensure it uses the OpenClaw `write` tool or file generation instructions to create multiple markdown files in the target directory (e.g., `PR_001_DB.md`, `PR_002_Logic.md`, `PR_003_API.md`).
- **Queue Engine Compatibility**: EVERY generated PR contract must explicitly include `status: open` in its YAML frontmatter or top-level text. Otherwise, the Manager's `get_next_pr.py` engine will ignore it.

### 2.2 E2E Test Verification (`scripts/test_planner_micro_slicing.sh`)
To ensure the Planner actually obeys this prompt, we will write a strict E2E test.
- **Sandbox Setup**: Create a sandbox directory and mock a complex PRD (`dummy_complex_prd.md`). The PRD should explicitly describe a multi-tier feature (e.g., "Build a full-stack login system with DB, API, and UI").
- **Execution**: Run `python3 scripts/spawn_planner.py --prd-file dummy_complex_prd.md --out-dir $SANDBOX/prs`.
- **Assertions**:
  - The `$SANDBOX/prs` directory MUST contain more than one `.md` file.
  - All `.md` files in that directory MUST contain the string `status: open`.
  - The files MUST be numbered/prefixed in a way that allows alphabetical sorting (e.g., `PR_001`, `PR_002`).

### 2.3 Preflight Integration
- Append `bash scripts/test_planner_micro_slicing.sh` to the main `preflight.sh` execution block to ensure this behavior is continuously protected.

## 3. Acceptance Criteria
- [ ] `scripts/test_planner_micro_slicing.sh` is written and correctly asserts that the Planner generates >1 PR file from a complex PRD.
- [ ] The Planner's prompt is updated to enforce Micro-Slicing and the `status: open` requirement.
- [ ] Running `./preflight.sh` passes successfully, proving the Planner natively outputs multiple queue-compatible PRs.