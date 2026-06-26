# PRD_020_CUJ_4: Refactoring SDLC CUJ-4 (Merge Code) for Testability

## 1. Problem Statement
The 4th Core User Journey (CUJ-4) involves the Manager merging approved code into the `master` branch and handling potential deployment triggers. Currently, the `leio-sdlc` skill uses a generic `bash` execution to run `scripts/merge_code.sh <branch_name>`.
This violates our DfT (Design for Testability) principles because:
1. It relies on the unstructured `exec` tool.
2. It lacks a mockable boundary (`TEST_MODE` interception) to prevent actual `git merge` or `git push` operations during automated skill testing.
3. Bash arguments passed from LLMs are brittle.

## 2. Goals
- Refactor CUJ-4 to use the "Limb Stubbing via Dependency Injection" pattern.
- Create a Python wrapper (`merge_code.py`) that strictly handles the branch merge logic.
- Ensure the wrapper intercepts execution when `SDLC_TEST_MODE=true` to provide zero-side-effect automated testing.

## 3. Key Features

### 3.1 The Python Wrapper (`scripts/merge_code.py`)
- **Inputs**: Use `argparse` to accept `--branch <branch_name>`.
- **Test Mode (`SDLC_TEST_MODE=true`)**: 
  - Do NOT execute any `git` commands.
  - Append the exact string to `tests/tool_calls.log`: `{'tool': 'merge_code', 'args': {'branch': <branch_name>}}` (using Python dict to string conversion `str({...})` for single quotes).
  - Print `{"status": "mock_success", "action": "merge"}` to stdout.
  - Exit with code 0.
- **Production Mode**: 
  - Execute the actual `git merge <branch_name>` command securely using `subprocess.run`.
  - Handle potential merge conflicts gracefully (if `git merge` fails, print the error and exit with a non-zero code).

### 3.2 Updating the Skill Brain (`SKILL.md`)
- Locate Command Template 4 (Merge and Deploy) in `SKILL.md`.
- Replace the existing `bash` command with the following exact literal string:
  `To merge approved code, use the \`exec\` tool to run: \`python scripts/merge_code.py --branch <branch_name>\``

### 3.3 The Mock Test (`scripts/test_cuj_4_mock.sh`)
- Create a test script that sets `export SDLC_TEST_MODE=true`.
- Runs the real OpenClaw agent: `openclaw agent -m "Reviewer 已经给了 LGTM，请把 feature/login 分支合并到 master"`
- Asserts that `grep -q "'tool': 'merge_code'" tests/tool_calls.log` succeeds.

## 4. Acceptance Criteria (AC)
- [ ] `scripts/merge_code.py` parses `--branch` and strictly implements `SDLC_TEST_MODE` interception.
- [ ] `SKILL.md` Command Template 4 is replaced with the exact target string.
- [ ] `scripts/test_cuj_4_mock.sh` is created, triggers the native agent, and successfully asserts the mock log.
- [ ] Production logic uses `subprocess.run` to execute git commands securely.