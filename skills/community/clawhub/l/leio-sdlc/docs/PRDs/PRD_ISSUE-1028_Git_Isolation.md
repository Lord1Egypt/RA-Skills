# PRD: Git Subprocess Isolation (ISSUE-1028)

## Context
Running Git commands without explicitly specifying the Working Directory (cwd) risks cross-repo contamination if the engine is launched from the wrong directory. This project aims to fix Git Subprocess Isolation in the leio-sdlc project.

## Requirements
- Implement a Preflight Boundary Check in the core Git utility functions (e.g., `git_utils.py`) using `git rev-parse --show-toplevel`.
- Abort with a [FATAL] error if it escapes the workdir.
- Refactor existing Git utility functions to accept and enforce a `workdir` argument.
- Refactor the rest of the engine to utilize the updated utilities and explicitly pass `cwd=workdir` to all Git subprocess calls.

## Architecture
- `git_utils.py`: Contains the updated Git utilities enforcing the workdir boundary.
- Engine components: Core SDLC scripts modified to pass the new argument.

## Acceptance Criteria
- [ ] `git_utils.py` contains a boundary check using `git rev-parse --show-toplevel`.
- [ ] The engine throws a [FATAL] error when execution escapes the specified workdir.
- [ ] All Git utilities accept a `workdir` argument.
- [ ] All framework scripts explicitly pass `cwd=workdir`.

## Framework Modifications
- `orchestrator.py`
- `merge_code.py`
- `spawn_planner.py`
- `spawn_reviewer.py`
- `spawn_arbitrator.py`
- `spawn_coder.py`

## Testing Strategy
Integration tests with mocked Git subdirectories and boundary escape scenarios using `scripts/skill_test_runner.sh`.
