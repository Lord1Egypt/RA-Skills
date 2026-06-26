# PRD-1005: Inject Playbook Content Directly into Agent System Prompts

## 1. Problem Statement
Agents (Coder, Reviewer, Planner) are currently acting out of bounds (e.g., Coder modifying PR status to 'closed', Reviewer hallucinating guardrails) because their Role Playbooks (`playbooks/*.md`) are not effectively passed to them. 
- `spawn_coder.py` hardcodes a basic 3-line prompt and completely ignores `coder_playbook.md`.
- `spawn_reviewer.py` instructs the agent to read `playbooks/reviewer_playbook.md`, but the agent is jailed in the target project's `workdir` where the playbook directory does not exist, causing it to operate blind.

## 2. Goal
Ensure every SDLC agent receives its full operational constraints and lifecycle rules before starting its session, drastically reducing 'Reward Hacking' and boundary violations.

## 3. Scope & Implementation Details
- **Target Repository**: `/root/.openclaw/workspace/projects/leio-sdlc`
- **Action Items**:
  1. Refactor `scripts/spawn_coder.py`, `scripts/spawn_reviewer.py`, and `scripts/spawn_planner.py`.
  2. The Python scripts must physically read the corresponding playbook from the `playbooks/` directory (resolving the path relative to the script location, e.g., using `__file__`).
  3. Inject the exact string content of the playbook directly into the `task_string` variable.
  4. Ensure that the prompt explicitly forbids the agent from manually editing the markdown file's `status` field.
  
## 4. Acceptance Criteria
- All three `spawn_*.py` scripts successfully read their corresponding playbook and inject the content into the `task_string`.
- The tests run successfully using `./preflight.sh`.
