# PRD-032: Create PM (Product Manager) AgentSkill to Standardize PRD Generation

## 1. Objective
Establish a dedicated `pm-skill` (Product Manager AgentSkill) to standardize the PRD generation process. This skill will act as a "Requirement Engineer", synthesizing conversational context into structured PRDs, autonomously defining project-appropriate TDD testing strategies (dogfooding its own principles), and physically delivering the PRD to the orchestrator's queue.

## 2. Scope & Implementation Details
**Location**: The skill will be built inside the `skills/pm-skill` directory within the `leio-sdlc` repository.

1. **Scaffolding (`skills/pm-skill/`)**:
   - Create `skills/pm-skill/` directory.
   - Create the core playbook `SKILL.md`.
   - Create a deployment script `deploy.sh` that symlinks the skill to `~/.openclaw/skills/pm-skill`.

2. **The PM Playbook (`skills/pm-skill/SKILL.md`)**:
   - **Role Definition**: The PM is a Summarizer, NOT an Inventor. It must synthesize the Problem Statement, Solution, and Scope strictly from the user conversation. It must NOT hallucinate technical pseudo-code or specific files to modify unless explicitly discussed.
   - **Scope Locking**: The PM must explicitly identify the target project's absolute directory (e.g., `/root/.openclaw/workspace/projects/leio-sdlc` vs `/root/.openclaw/workspace/AMS`) to prevent downstream agents from wandering into the wrong repository.
   - **Autonomous Test Strategy (Core Value)**: The PM MUST autonomously define the optimal testing strategy based on the project type. 
     - *AgentSkills*: Define testing via `scripts/skill_test_runner.sh` or Conversation Replay Testing.
     - *Scripts/CLIs*: Define Unit/Integration testing with mocks.
     - *Web/Services*: Define Probe/API or UI tests.
     - If local best practices are missing, the PM must use the `web_search` tool to find industry standards for the project type.
   - **TDD Guardrail**: The PM must explicitly state in the PRD that the implementation and its failing test MUST be delivered in the same PR contract.
   - **Artifact Delivery**: The PM must use the `write` tool to physically save the PRD into the target project's `docs/PRDs/` directory (e.g., `/root/.openclaw/workspace/projects/leio-sdlc/docs/PRDs/PRD_XXX_Example.md`). It must verify the file exists.

## 3. TDD & Acceptance Criteria
**Test Script**: Create `tests/test_032_pm_skill.sh`.

We must test this AgentSkill using our established best practice (`scripts/skill_test_runner.sh`).

**Execution & Assertions**:
1. Within the test script, execute the skill test runner against the new PM skill:
   `bash scripts/skill_test_runner.sh skills/pm-skill "I want a feature to export reports as PDF in the AMS project. Please generate the PRD."`
2. **Assertion 1 (Artifact Delivery)**: Verify that the test runner successfully spawned the agent and the agent physically created a PRD file (e.g., `docs/PRDs/PRD_*_PDF.md` or similar) in the mocked workspace.
3. **Assertion 2 (Scope & Synthesis)**: Read the created PRD file and verify it correctly identified the project context (AMS).
4. **Assertion 3 (Autonomous Testing)**: Verify the PRD contains a comprehensive "Testing Strategy" section that defines a project-appropriate test (since it's a feature, a CLI or unit test) and enforces the "TDD Guardrail".
5. **Assertion 4 (Playbook Constraints)**: Read `skills/pm-skill/SKILL.md` and verify it contains the mandatory rules: "Summarizer, NOT an Inventor", "Scope Locking", "Autonomous Test Strategy", and "Artifact Delivery".
6. Clean up any generated mock PRD files. If all assertions pass, the script exits `0`.