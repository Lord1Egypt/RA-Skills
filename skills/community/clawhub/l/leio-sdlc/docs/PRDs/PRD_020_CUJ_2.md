# PRD_020_CUJ_2: Refactoring SDLC CUJ-2 (Spawn Coder) for Testability

## 1. Problem Statement
Following the successful "Tracer Bullet" refactor of CUJ-1 (Spawn Planner), we must apply the exact same "Limb Stubbing" architecture to CUJ-2 (Spawn Coder). Currently, the Manager uses raw `sessions_spawn` JSON payloads or brittle Bash scripts to spawn the Coder. This is untestable, prone to hallucination, and vulnerable to Bash quoting bugs.

## 2. Goals
- Implement the "Limb Stubbing via Dependency Injection" pattern for CUJ-2.
- Provide a Python wrapper (`spawn_coder.py`) that handles dual file-path inputs (`--pr-file` and `--prd-file`) for Direct Context Injection.
- Ensure zero-side-effect automated testing for the Manager's ability to trigger the Coder.

## 3. Key Features

### 3.1 The Python Wrapper (`scripts/spawn_coder.py`)
- **Inputs**: Use `argparse` to accept `--pr-file <path>` and `--prd-file <path>`.
- **Test Mode (`SDLC_TEST_MODE=true`)**: 
  - Do NOT call the OpenClaw API.
  - Append the following exact string to `tests/tool_calls.log`: `{'tool': 'spawn_coder', 'args': {'pr_file': <path>, 'prd_file': <path>}}` (Note: use Python dict to string conversion `str({...})` to ensure single quotes).
  - Print `{"status": "mock_success", "role": "coder"}` to stdout.
  - Exit with code 0.
- **Production Mode**: 
  - Read the contents of BOTH files.
  - Construct a `task_string` that explicitly injects both the PR Contract and the PRD text to ensure the Coder has full context.
  - Use `subprocess.run(["openclaw", "sessions_spawn", task_string])` to spawn the sub-agent.
  - Handle file-not-found errors gracefully (exit 1).

### 3.2 Updating the Skill Brain (`SKILL.md`)
- Locate Command Template 2 (Spawning the Coder) in `SKILL.md`.
- Replace the existing complex command/JSON with the following exact literal string:
  `To spawn a coder, use the \`exec\` tool to run: \`python scripts/spawn_coder.py --pr-file <path_to_pr> --prd-file <path_to_prd>\``

### 3.3 The Mock Test (`scripts/test_cuj_2_mock.sh`)
- Create a test script that sets `export SDLC_TEST_MODE=true`.
- Runs the real OpenClaw agent: `openclaw agent -m "PR合约已就绪在 dummy_pr.md，技术字典在 dummy_prd.md，请安排 Coder 开始开发"`
- Asserts that `grep -q "'tool': 'spawn_coder'" tests/tool_calls.log` succeeds.

## 4. Acceptance Criteria (AC)
- [ ] `scripts/spawn_coder.py` exists, handles dual file inputs, and implements the `SDLC_TEST_MODE` block perfectly.
- [ ] `SKILL.md` is updated with the exact target string for Command Template 2.
- [ ] `scripts/test_cuj_2_mock.sh` runs successfully in less than 10 seconds.
- [ ] Production logic uses `subprocess.run` instead of just printing placeholders.