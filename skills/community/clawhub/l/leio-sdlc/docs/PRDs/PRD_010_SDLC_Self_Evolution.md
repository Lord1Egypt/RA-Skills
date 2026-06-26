# PRD_010: LEIO-SDLC Self-Evolution & Deployment Pipeline

## 1. Problem Statement
The `leio-sdlc` framework currently exists in a "runtime-only" state or relies on informal manual updates between the workspace and the OpenClaw production environment. This lacks version control, design history, and automated safety gates (testing), which is unacceptable for a core infrastructure component.

## 2. Goals
- **Formalize Dev-to-Runtime Lifecycle**: Create a robust mechanism to promote changes from `/workspace/leio-sdlc/` to `~/.openclaw/skills/leio-sdlc/`.
- **Knowledge Retention**: Establish a `docs/` structure to store historical design decisions and PRDs.
- **Safety Gates**: Implement mandatory "Agentic Integration Tests" (sub-agent testing) as a pre-condition for deployment.
- **Self-Hosting**: Use the `leio-sdlc` framework to manage the development of `leio-sdlc` itself.

## 3. Key Features

### 3.1 Project Structure
- `leio-sdlc/STATE.md`: Tracks the project's internal milestones and sprint status.
- `leio-sdlc/docs/PRDs/`: Archives all versioned requirement documents.
- `leio-sdlc/scripts/agentic_smoke_test.sh`: The core testing engine that spawns a sub-agent to verify skill logic.

### 3.2 Shift-Left Testing Strategy (The "Pre-flight" Gate)
- **Dev Gate (preflight.sh)**: For Skill projects, the `preflight.sh` MUST invoke `scripts/agentic_smoke_test.sh`. The Coder is responsible for passing this test in their sandboxed branch BEFORE submitting for review.
- **Review Gate**: The Reviewer verifies that the Coder didn't "hardcode" or cheat the agentic test.

### 3.3 The Deployment Pipeline (`deploy.sh`)
The script acts as the final production gate:
1. **Linting**: Verify `SKILL.md` syntax and metadata.
2. **Final Smoke Test**: Re-run `scripts/agentic_smoke_test.sh` on the merged master code.
3. **Promotion**: Copy validated files to `~/.openclaw/skills/leio-sdlc/`.
4. **Post-deploy**: Auto-restart gateway (if needed) and notify the main channel.

### 3.3 Multi-Agent Lifecycle Integration
- **Planner**: Must now generate PR contracts that include specific test scenarios for the sub-agent pre-check.
- **Coder**: Responsible for maintaining `scripts/` and ensuring `deploy.sh` remains compatible with new logic.

## 4. Acceptance Criteria (AC)
- [ ] A `STATE.md` exists and is updated.
- [ ] `deploy.sh` successfully promotes a version change to the runtime path.
- [ ] A failed sub-agent test successfully blocks the `deploy.sh` process.
- [ ] Git history shows all changes originated from the workspace.

## 5. Anti-Patterns
- **No Hotfixes**: Never edit `~/.openclaw/skills/leio-sdlc/` directly.
- **No Token-Heaving Logging**: `deploy.sh` must follow the "Silent on Success" rule.
