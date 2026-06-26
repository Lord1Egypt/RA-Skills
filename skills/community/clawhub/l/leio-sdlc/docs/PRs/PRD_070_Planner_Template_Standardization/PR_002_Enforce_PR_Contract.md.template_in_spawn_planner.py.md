status: completed

## 1. Objective
Update the Planner agent script (`spawn_planner.py`) to inject the newly created template into the system prompt and enforce its usage, then write an E2E test.

## 2. Scope & Implementation Details
- Edit `scripts/spawn_planner.py`.
- Read the content of `TEMPLATES/PR_Contract.md.template`.
- Add instruction to the `task_string` prompt: "For EVERY Micro-PR you generate, you MUST strictly use the format defined in the template below. Do NOT alter the `status_open_text` YAML frontmatter." and append the template.

## 3. TDD & Acceptance Criteria
- Create `tests/test_070_planner_template_enforcement.sh`.
- Run `spawn_planner.py` with a mocked PRD.
- Assert that the generated PR contracts in `docs/PRs/` directory strictly start with `status_open_text` and contain headers `## 1. Objective`, `## 2. Scope & Implementation Details`, and `## 3. TDD & Acceptance Criteria`.
