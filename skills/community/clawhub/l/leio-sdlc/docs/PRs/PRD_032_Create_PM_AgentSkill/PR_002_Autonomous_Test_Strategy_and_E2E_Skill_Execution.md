status: completed

# PR-002: Autonomous Test Strategy and E2E Skill Execution

## 1. Objective
Implement the Autonomous Test Strategy and TDD Guardrail within the PM AgentSkill, and verify its end-to-end execution using the skill test runner.

## 2. Scope & Implementation Details
- Update `skills/pm-skill/SKILL.md` to add:
  - Autonomous Test Strategy: Autonomously define testing strategy based on project type (AgentSkills, Scripts/CLIs, Web/Services) or use `web_search` for missing practices.
  - TDD Guardrail: Explicitly state implementation and failing test must be delivered in the same PR contract.

## 3. TDD & Acceptance Criteria
- Update `tests/test_032_pm_skill.sh` to execute the skill via `scripts/skill_test_runner.sh`.
- Mock a request: "I want a feature to export reports as PDF in the AMS project. Please generate the PRD."
- Assertion 1 (Artifact Delivery): Verify the test runner spawns the agent and physically creates a PRD file in a mocked workspace.
- Assertion 2 (Scope & Synthesis): Verify the created PRD identifies the project context (AMS).
- Assertion 3 (Autonomous Testing): Verify the PRD contains a comprehensive "Testing Strategy" section defining project-appropriate tests and enforcing the "TDD Guardrail".
- Clean up generated mock files. Test must pass and exit 0.