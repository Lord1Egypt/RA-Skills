# PRD_020_CUJ_3: Refactoring SDLC CUJ-3 (Spawn Reviewer) for Testability

## 1. Problem Statement
The 3rd Core User Journey (CUJ-3) involves the Manager spawning a Reviewer agent to verify the Coder's work. Currently, this relies on raw `sessions_spawn` payloads or generic `exec` commands, which violate the "Domain-Specific Tools" (DfT) rule. Furthermore, passing complex `git diff` instructions via natural language is highly susceptible to formatting errors and hallucination.

## 2. Goals
- Extend the "Limb Stubbing" architecture to CUJ-3.
- Create a Python wrapper (`spawn_reviewer.py`) that explicitly takes the PR Contract and the target Git Diff range.
- Guarantee 100% deterministic, zero-side-effect automated testing for the Manager's ability to trigger the Reviewer.

## 3. Key Features

### 3.1 The Python Wrapper (`scripts/spawn_reviewer.py`)
- **Inputs**: Use `argparse` to accept `--pr-file <path>` and `--diff-target <target>` (e.g., `HEAD~1..HEAD` or `base_hash..latest_hash`).
- **Test Mode (`SDLC_TEST_MODE=true`)**: 
  - Do NOT call the OpenClaw API.
  - Append the exact string to `tests/tool_calls.log`: `{'tool': 'spawn_reviewer', 'args': {'pr_file': <path>, 'diff_target': <target>}}` (using Python dict to string conversion `str({...})` for single quotes).
  - Print `{"status": "mock_success", "role": "reviewer"}` to stdout.
  - Exit with code 0.
- **Production Mode**: 
  - Read the content of the `--pr-file`.
  - Construct a `task_string` that explicitly injects the PR Contract text AND instructs the Reviewer to "Execute git diff <diff_target>".
  - Use `subprocess.run(["openclaw", "sessions_spawn", task_string])` to spawn the sub-agent.
  - Handle file-not-found errors gracefully (exit 1).

### 3.2 Updating the Skill Brain (`SKILL.md`)
- Locate Command Template 3 (Spawning the Reviewer) in `SKILL.md`.
- Replace the existing complex command/JSON with the following exact literal string:
  `To spawn a reviewer, use the \`exec\` tool to run: \`python scripts/spawn_reviewer.py --pr-file <path_to_pr> --diff-target <base_hash>..<latest_hash>\``

### 3.3 The Mock Test (`scripts/test_cuj_3_mock.sh`)
- Create a test script that sets `export SDLC_TEST_MODE=true`.
- Runs the real OpenClaw agent: `openclaw agent -m "Coder 已经提交了代码 (Commit: abc1234)，基线是 master (Commit: def5678)，工单在 dummy_pr.md，请拉起 Reviewer 进行审查"`
- Asserts that `grep -q "'tool': 'spawn_reviewer'" tests/tool_calls.log` succeeds.

## 4. Acceptance Criteria (AC)
- [ ] `scripts/spawn_reviewer.py` parses `--pr-file` and `--diff-target` and strictly implements `SDLC_TEST_MODE`.
- [ ] `SKILL.md` Command Template 3 is replaced with the exact target string.
- [ ] `scripts/test_cuj_3_mock.sh` is created, triggers the native agent, and successfully asserts the mock log.
- [ ] Production logic uses `subprocess.run` to spawn the session securely.