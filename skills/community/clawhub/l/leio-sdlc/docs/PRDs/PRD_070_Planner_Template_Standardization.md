# PRD-070: Planner PR Contract Template Standardization

## 1. Problem Statement
The Planner (Manager/Architect) agent currently relies on natural language prompts to format the Micro-PR contracts it generates. Because there is no physical template file, the Planner occasionally hallucinates the YAML frontmatter (e.g., omitting `status: open` or using `---` separators incorrectly). This causes the Orchestrator's crawler (`get_next_pr.py`) to silently ignore the generated PRs, stalling the SDLC pipeline (as seen in PRD-069).

## 2. Solution
We must introduce a strict Markdown template and force the Planner to use it as a fill-in-the-blank form, eliminating formatting hallucinations.

### 2.1. Create the PR Contract Template
Create a new file at `TEMPLATES/PR_Contract.md.template` containing the exact structure required:
```markdown
status: open

# PR-[ID]: [Title]

## 1. Objective
[Clearly state the goal of this specific PR]

## 2. Scope & Implementation Details
[List the exact files to modify and the specific logic to implement]

## 3. TDD & Acceptance Criteria
[Define the exact test script to write or extend, and the assertions required to pass this PR]
```

### 2.2. Update Planner Playbook/Prompt
Modify `scripts/spawn_planner.py`:
- Read the contents of `TEMPLATES/PR_Contract.md.template`.
- Inject it into the `task_string` (system prompt) for the Planner.
- Add a strict instruction: "For EVERY Micro-PR you generate, you MUST strictly use the format defined in the template below. Do NOT alter the `status: open` YAML frontmatter."

### 2.3. Update PR Creation Script
Modify `scripts/create_pr_contract.py`:
- Since the Planner will now include `status: open` natively from the template, remove the hardcoded `f.write("status: open\n\n")` injection in `create_pr_contract.py` to prevent duplicate YAML headers.

## 3. Testing Strategy (TDD)
Create `tests/test_070_planner_template_enforcement.sh`.
- Mock a simple PRD.
- Run `spawn_planner.py`.
- Assert that the generated PR files in the `docs/PRs/` directory strictly start with `status: open` (without duplicate status tags) and contain the headers `## 1. Objective`, `## 2. Scope & Implementation Details`, and `## 3. TDD & Acceptance Criteria`.