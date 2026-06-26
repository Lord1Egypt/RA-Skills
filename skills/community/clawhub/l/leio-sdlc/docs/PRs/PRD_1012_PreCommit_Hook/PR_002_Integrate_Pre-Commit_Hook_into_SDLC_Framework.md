status: closed

# PR-002: Integrate Pre-Commit Hook into SDLC Framework

## 1. Objective
Integrate the newly created pre-commit hook into the SDLC orchestrator, code merge processes, and the AgentSkill deployment template so that it is automatically installed and correctly bypassed during official SDLC operations.

## 2. Scope (Functional & Implementation Freedom)
- Modify the SDLC orchestrator and merge logic to inject the required environment variable (e.g., `SDLC_ORCHESTRATOR_RUNNING=1`) during subprocess calls that perform git commits.
- Update the AgentSkill deployment mechanism to invoke the installation script, ensuring the hook is registered upon deployment.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Automated tests must verify that the orchestrator and merge processes correctly inject the environment variable when executing git commands.
- Automated tests must verify that the deployment template includes the hook installation step.
- The Coder MUST ensure all tests run GREEN before submitting.