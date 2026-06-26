# PRD-031: Agentic Orchestration Infrastructure Stabilization & Guardrails

## Context
This project addresses three critical issues in the LEIO SDLC infrastructure to ensure reliable autonomous operation, transparent communication, and strict requirement-first discipline. Currently, the system suffers from:
1.  **Deadlock/Locking**: Orchestrator tasks in SKILL.md use legacy shell backgrounding (`&`), which prevents the OpenClaw agent loop from receiving completion events, causing the Main Agent to hang.
2.  **Notification Failures**: Slack channel IDs with the `slack:channel:CXXX` protocol are improperly parsed by the Orchestrator, resulting in silent failures of progress updates.
3.  **Requirements Discipline**: There is no enforcement that a PRD (the source of truth) is committed to Git before the Orchestrator begins execution, leading to "untracked" logic and poor traceability.
4.  **Base Drift/Branch Collision**: Stale branches from failed runs are reused without rebasing, causing "reversion" diffs that trigger security alarms.

## Requirements
### Functional Requirements
*   **Native Backgrounding**: All execution commands in `SKILL.md` must use the OpenClaw `exec(background: true)` parameter.
*   **Robust Channel Parsing**: The Orchestrator's notification module must support full-qualified OpenClaw routing keys (e.g., `slack:channel:<ID>`, `channel:<ID>`, or just `<ID>`) without splitting or truncation.
*   **PRD Commit Guardrail**: The Orchestrator MUST verify that the target PRD file (passed via `--prd`) is tracked by Git and has no uncommitted changes before proceeding.
*   **Atomic Branch Isolation**: The Orchestrator MUST generate unique branch names for every PR execution attempt (e.g., by appending a timestamp or UUID) to prevent stale code reuse from previous failed runs.

### Non-Functional Requirements
*   **Multi-Repo Awareness**: All scripts must resolve paths relative to the project's root or the global workspace correctly.
*   **Token Efficiency**: Prevent unnecessary polling by using native event-driven completion notifications.

## Architecture
- **Skill Templates**: Refactor `leio-sdlc/SKILL.md` and related skills to remove `nohup` and `&`.
- **Orchestrator Logic**: 
    - Update `notify_channel` in `scripts/orchestrator.py` to handle raw routing keys.
    - Add a `validate_prd_is_committed()` check in the Orchestrator startup sequence.
- **Archetypes**: Update the global `AgentSkill_Archetype` in `projects/docs/TEMPLATES/` to propagate these best practices to future skills.

## Framework Modifications
The Coder is explicitly authorized to modify the following core SDLC framework files:
- `projects/leio-sdlc/scripts/orchestrator.py` (Notification logic, PRD guardrail)
- `projects/leio-sdlc/SKILL.md` (Command templates)
- `projects/leio-sdlc/skills/pm-skill/SKILL.md` (Command templates)
- `projects/leio-sdlc/skills/issue_tracker/SKILL.md` (Command templates)
- `projects/docs/TEMPLATES/AgentSkill_Archetype/SKILL.md.template` (Template fix)

## Autonomous Test Strategy
*   **Integration Tests**: Use `scripts/test_orchestrator_cli.py` to verify:
    - Channel parsing with various routing key formats.
    - PRD commit guardrail (test with untracked vs committed PRD).
*   **Smoke Tests**: Trigger a mock SDLC run and verify the Main Agent receives the `Exec completed` notification and Slack notifications are received in a test channel.

## Acceptance Criteria
- [ ] Main Agent can start an Orchestrator run and reply with `NO_REPLY` (Agent Loop is not blocked).
- [ ] Orchestrator sends a "Processing PRD..." notification to Slack successfully using a full routing key.
- [ ] Orchestrator exits with a clear error message if a PRD is modified but not committed.
- [ ] Orchestrator generates a unique branch name (with timestamp/suffix) for each PR run, avoiding stale branch reuse.
- [ ] All `SKILL.md` files in `leio-sdlc` are free of `nohup` and `&`.
