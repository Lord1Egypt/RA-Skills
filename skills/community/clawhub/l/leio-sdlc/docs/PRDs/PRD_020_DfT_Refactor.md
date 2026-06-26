# PRD_020: Refactoring SDLC for Testability (The Tracer Bullet)

## 1. Problem Statement
The current `leio-sdlc` skill directly invokes the generic `sessions_spawn` tool with massive, complex JSON payloads. This violates the principle of "Domain-Specific Tools," leading to:
1. **High Hallucination Risk**: The LLM frequently drops or alters critical system prompt instructions.
2. **Untestability**: We cannot easily mock `sessions_spawn` at the OpenClaw framework level to test the agent's logic without actually creating child sessions (which is slow and costly).

## 2. Goals
- Refactor the skill architecture to support **Limb Stubbing via Dependency Injection**.
- We will execute this refactor iteratively. This PRD focuses *exclusively* on the "Tracer Bullet" (探路弹): **CUJ-1 (Spawning the Planner)**.
- Prove that by shifting from a generic tool to a custom local python wrapper, we can achieve 100% deterministic, zero-side-effect testing.

## 3. Key Features (The CUJ-1 Refactor)

### 3.1 The Python Wrapper (`scripts/spawn_planner.py`)
- **Language**: Must be written in Python to avoid Bash quoting/escaping hell (the ghost of ISSUE-001).
- **Interface**: Instead of taking a massive system prompt string from the CLI, it should take simple arguments: `--prd-file <path>`.
- **Logic (Production Mode)**: The Python script will read the PRD file, assemble the complex `task` prompt string internally, and invoke the OpenClaw API (or CLI) to spawn the sub-agent.
- **Logic (Test Mode)**: If the environment variable `SDLC_TEST_MODE=true` is present, the script MUST NOT call OpenClaw. Instead, it must:
  1. Append the intercepted arguments to a log file (e.g., `tests/tool_calls.log`).
  2. Print a mock success message (e.g., `{"status": "mock_success", "role": "planner"}`).
  3. Exit with code `0`.

### 3.2 Updating the Skill Brain (`SKILL.md`)
- Modify "Command Template 1". 
- Remove the massive `sessions_spawn` JSON template.
- Instruct the Manager: "To spawn a planner, use the `exec` tool to run: `python scripts/spawn_planner.py --prd-file <path_to_prd>`".

### 3.3 The Mock Test (`scripts/test_cuj_1_mock.sh`)
- Create a dedicated test script that sets `export SDLC_TEST_MODE=true`.
- Invokes the global test runner against the modified skill with a CUJ-1 trigger prompt.
- Asserts that the runner completes and that `tests/tool_calls.log` contains the expected mock invocation.

## 4. Acceptance Criteria (AC)
- [ ] `scripts/spawn_planner.py` exists and handles both Production and Test modes.
- [ ] `SKILL.md` is updated to use the new Python script for CUJ-1.
- [ ] `scripts/test_cuj_1_mock.sh` runs successfully in less than 5 seconds (proving it didn't actually spawn a heavy sub-agent).
- [ ] The Python script uses file paths (`--prd-file`) rather than raw text arguments to prevent escaping bugs.

## 5. Anti-Patterns
- **Do not rewrite all 5 CUJs yet**. Focus only on CUJ-1. If the architecture is flawed, we want to fail fast on one component.
- **No Bash Wrappers for Spawn**: Do not use Bash for the `spawn_planner` script. Python only.
