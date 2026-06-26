# PRD_027_PM_SDLC_Decoupling: Extract PM Role & Clean Workspace

## 1. Problem Statement & Architecture Vision
The current Agentic SDLC pipeline forces the `leio-sdlc` skill to act as both a **Product Manager (PM)** (absorbing high-context raw user ideas to write a PRD) and an **Engineering Manager** (executing zero-context isolated code generation). This violates the Single Responsibility Principle, pollutes the context for the coding phase, and makes a pure CLI-driven pipeline (`run.sh`) impossible.

**The New Vision: Agentic Microservices (The Two-Stage Rocket)**
1. `leio-pm` (Future): A high-context Main Session skill. Interacts with the Boss. Outputs a physical `PRD_*.md`.
2. `leio-sdlc` (Current): A zero-context, stateless execution engine. Starts execution **ONLY** upon receiving a path to a `PRD_*.md`.

This PRD dictates the massive workspace cleanup required to enforce this new architectural paradigm and satisfy ISSUE-026 (Self-Explaining Architecture).

## 2. Impact Analysis & Refactoring Scope

### 2.1 Top-Level Governance & Documentation
- **`/root/.openclaw/workspace/MEMORY.md`**:
  - Update the "Project Bootstrap Protocol" and "The Ultimate E2E Scenario" (from ISSUE-024). Change "Trigger: User inputs a raw idea -> Manager drafts PRD" to "Trigger: Pre-existing PRD -> Manager spawns Planner".
- **`/root/.openclaw/workspace/TEMPLATES/organization_governance.md`**:
  - In the Agile SDLC section, formally document the "PM-SDLC Decoupling": The PM role operates in the main session to lock the PRD contract; the Manager operates purely as a message bus/executor that consumes the PRD.
  
### 2.2 Skill Runtime & Definition
- **`/root/.openclaw/workspace/projects/leio-sdlc/SKILL.md`**:
  - **Remove** all instructions prompting the Manager to "draft a PRD based on user idea".
  - **Define Entry Point**: "Your input is a physical `PRD.md` file. Your first action is to read it, then spawn the Planner."
  - **Inject Meta-Cognition (ISSUE-026)**: Add a strict rule: "If asked about your internal workings, architecture, or error handling, immediately read `ARCHITECTURE.md` and explain yourself."

### 2.3 E2E Tests Cleanup
- **`/root/.openclaw/workspace/projects/leio-sdlc/scripts/test_manager_e2e.sh`**:
  - The E2E test currently injects a prompt: "Task: Create a simple hello world python script. 1. Create PRD...".
  - **Action**: Refactor the script to *pre-generate* a dummy PRD file inside the sandbox (`tests/e2e_sandbox_xxx/docs/PRDs/dummy_prd.md`).
  - Update the `MANAGER_PROMPT` to: "You are the leio-sdlc Manager. A PRD exists at `docs/PRDs/dummy_prd.md`. Execute the pipeline (Plan -> Code -> Review -> Merge) based on this file."

### 2.4 The Self-Explaining Manifest (ISSUE-026 Fulfillment)
- **`/root/.openclaw/workspace/projects/leio-sdlc/ARCHITECTURE.md`**:
  - **Create this file** as the single source of truth for the skill.
  - Must include:
    1. **The State Machine**: `PRD (Input) -> Planner -> Coder <-> Reviewer -> Merge`.
    2. **The Decoupling**: Explain *why* the PM role is separated from the SDLC engine (Context paradox, hot/cold data).
    3. **Resilience (Green/Yellow/Red Paths)**: Document the 3-attempt API retry lock, the Review-Correction Loop, and the upcoming physical Circuit Breaker (ISSUE-025).

## 3. Acceptance Criteria
- [ ] `MEMORY.md` and `organization_governance.md` are updated to reflect the Two-Stage Rocket architecture.
- [ ] `SKILL.md` is purged of PRD-generation duties and endowed with Introspection (points to `ARCHITECTURE.md`).
- [ ] `ARCHITECTURE.md` is created, detailing the PM-SDLC split and the internal state machine.
- [ ] `test_manager_e2e.sh` is refactored to provision its own dummy PRD and start from Phase 2 (Planner).
- [ ] E2E test passes with the new decoupled flow.
### 2.5 Job Isolation & Concurrency (.sdlc/jobs/)
- **Requirement**: The pipeline MUST NOT use a global `docs/PRs/` directory for active execution. 
- **Mechanism**: When the engine is triggered with a PRD, it must create a dedicated workspace `.sdlc/jobs/<PRD_NAME>/`. All Planner outputs (PR contracts) and state tracking for this specific PRD must occur isolated within this directory.
- **Testing**: Create `scripts/test_concurrency_isolation.sh`. It must spawn two background engine instances with different dummy PRDs and assert that two distinct `.sdlc/jobs/` directories are created and managed without cross-pollution.
