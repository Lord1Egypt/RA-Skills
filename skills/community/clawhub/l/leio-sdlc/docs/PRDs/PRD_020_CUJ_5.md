# PRD_020_CUJ_5: Refactoring SDLC CUJ-5 (Update Issue Tracking) for Testability

## 1. Problem Statement
The final Core User Journey (CUJ-5) involves updating internal `.issues/*.md` files, or tracking project state. Currently, `SKILL.md` instructs the Manager to use the generic `edit` or `write` tools. This presents a massive testing problem: we cannot easily intercept and assert the payload of a native file-edit operation without executing it and altering the local file system. This breaks our "Zero Side-Effect Automated Testing" paradigm.

## 2. Goals
- Refactor CUJ-5 using the "Limb Stubbing" architecture.
- Instead of using the generic `edit` tool, create a dedicated Python wrapper (`update_issue.py`) to manage issue updates.
- Ensure the `SDLC_TEST_MODE=true` mechanism successfully intercepts the execution, logs the intent, and protects the real files from modification during tests.

## 3. Key Features

### 3.1 The Python Wrapper (`scripts/update_issue.py`)
- **Inputs**: Use `argparse` to accept `--issue-id <ID>` (e.g., `ISSUE-012`) and `--status <status>` (e.g., `closed`, `in-progress`).
- **Test Mode (`SDLC_TEST_MODE=true`)**: 
  - Do NOT modify any `.issues/*.md` files.
  - Append the exact string to `tests/tool_calls.log`: `{'tool': 'update_issue', 'args': {'issue_id': <ID>, 'status': <status>}}` (using Python dict to string conversion `str({...})` for single quotes).
  - Print `{"status": "mock_success", "action": "update_issue"}` to stdout.
  - Exit with code 0.
- **Production Mode**: 
  - Locate the file `.issues/<ID>.md`.
  - Open the file, find the line starting with `status:`, and replace the status with the new `<status>`.
  - If the file does not exist, print an error and exit with code 1.
  - Save the file and print a success message.

### 3.2 Updating the Skill Brain (`SKILL.md`)
- Locate Command Template 5 (Issue Tracking) in `SKILL.md`.
- Replace the instructions that tell the agent to "use the edit tool" with the following exact literal string:
  `To update an issue status, use the \`exec\` tool to run: \`python scripts/update_issue.py --issue-id <ID> --status <new_status>\``

### 3.3 The Mock Test (`scripts/test_cuj_5_mock.sh`)
- Create a test script that sets `export SDLC_TEST_MODE=true`.
- Runs the real OpenClaw agent: `openclaw agent -m "功能已经开发完了并且合并到 master 了，请把 ISSUE-999 的状态更新为 closed"`
- Asserts that `grep -q "'tool': 'update_issue'" tests/tool_calls.log` succeeds.

## 4. Acceptance Criteria (AC)
- [ ] `scripts/update_issue.py` is implemented with proper `argparse` and dual-mode functionality.
- [ ] `SKILL.md` Command Template 5 is cleanly replaced with the exact target string.
- [ ] `scripts/test_cuj_5_mock.sh` is created, sets the environment, triggers the native agent, and successfully asserts the log.
- [ ] Production logic correctly parses and replaces the `status:` line in the target markdown file without corrupting other content.