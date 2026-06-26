---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1093_Global_Dir_Decoupling

## 1. Context & Problem (业务背景与核心痛点)
The `--global-dir` parameter is intended to dictate where the `.sdlc_runs` artifacts and data are stored for the target project. However, the child scripts (`spawn_coder.py`, `spawn_planner.py`, `spawn_reviewer.py`) are erroneously using this same `global_dir` variable to resolve the paths for static assets like `playbooks/` and `TEMPLATES/`. 

When the SDLC runs on an external repository and a custom `--global-dir` is provided, these scripts fail to find the playbooks (which only exist in the leio-sdlc installation directory). They silently swallow the `FileNotFoundError` and inject empty playbooks into the LLM context, causing the agents to lose their rules and behave erratically.

## 2. Requirements & User Stories (需求定义)
- **Asset Independence**: All static assets (`playbooks/`, `TEMPLATES/`) must be resolved using the physical location of the script itself, completely independent of the `--global-dir` CLI argument.
- **State Data Routing**: The `--global-dir` argument must remain solely responsible for determining where the `.sdlc_runs` folder is created for the given project's execution artifacts.
- **Silent Fail Prevention**: (Optional but recommended) If a playbook or template cannot be found at the hardcoded static asset path, the system should raise an error or log a severe warning rather than silently proceeding with empty rules.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
Refactor the affected scripts (`scripts/spawn_coder.py`, `scripts/spawn_planner.py`, `scripts/spawn_reviewer.py`) to resolve static assets strictly relative to the script's physical location.

The logic should be updated from using `global_dir` to:
```python
RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
SDLC_ROOT = os.path.dirname(RUNTIME_DIR) # Points to the leio-sdlc root
playbook_path = os.path.join(SDLC_ROOT, "playbooks", "<agent>_playbook.md")
# And similarly for TEMPLATES
```
The `--global-dir` CLI parameter must remain intact in `argparse` across all scripts, as it is still used by the orchestrator for state directories, but its variable must not be used for asset resolution.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Custom Global-Dir with External Project**
  - **Given** the orchestrator runs with `--workdir /external/project` and `--global-dir /tmp/fake_global`
  - **When** `spawn_coder.py` (or planner/reviewer) is executed
  - **Then** the script successfully loads `coder_playbook.md` from the `leio-sdlc/playbooks/` directory instead of `/tmp/fake_global/playbooks/`.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Layer 1: Unit Test (Fast Feedback)**: Create `scripts/test_spawn_scripts_paths.py`.
  - Use `unittest.mock.patch` on `builtins.open` to monitor file reads.
  - Mock `sys.argv` to inject a fake `--global-dir`.
  - Assert that the scripts attempt to `open()` the playbook from the actual installation root (`SDLC_ROOT`), not from the fake `global-dir`.
  - Mock `openclaw_agent_call` to intercept the generated `task_string` payload and assert the payload is not empty.
- **Layer 2: E2E Mock Test (Integration)**: Create `scripts/e2e/e2e_test_1093_global_dir_decoupling.sh`.
  - Set up a fake external `workdir` and a fake empty `global_dir`.
  - Prepend a mock `openclaw` executable to `$PATH` to intercept the prompt payload instead of calling the actual LLM.
  - Assert that the intercepted prompt contains the actual playbook text.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/spawn_coder.py` (Update `playbooks` resolution)
- `scripts/spawn_planner.py` (Update `playbooks` and `TEMPLATES` resolution)
- `scripts/spawn_reviewer.py` (Update `playbooks` and `TEMPLATES` resolution)
- `scripts/test_spawn_scripts_paths.py` (New python unit test)
- `scripts/e2e/e2e_test_1093_global_dir_decoupling.sh` (New E2E test)

## 7. Hardcoded Content (硬编码内容)
### Exact Text Replacements:

**For the Python Unit Test `scripts/test_spawn_scripts_paths.py`**:
```python
import unittest
from unittest.mock import patch
import sys
import os

class TestSpawnScriptsPaths(unittest.TestCase):
    @patch('builtins.open')
    @patch('scripts.spawn_coder.openclaw_agent_call')
    def test_spawn_coder_playbook_path(self, mock_agent_call, mock_open):
        from scripts import spawn_coder
        
        # Inject fake arguments
        test_args = ["spawn_coder.py", "--pr-file", "dummy.md", "--prd-file", "dummy.md", "--workdir", "/tmp/fake_workdir", "--global-dir", "/tmp/fake_global_dir"]
        with patch.object(sys, 'argv', test_args):
            try:
                spawn_coder.main()
            except Exception:
                pass # Ignore exit or side effects, we only care about the open() calls
                
        # Assert that builtins.open was NOT called with the fake global dir for playbooks
        for call in mock_open.call_args_list:
            path = call[0][0]
            if "playbook" in path:
                self.assertNotIn("/tmp/fake_global_dir", path, f"Red Status: Attempted to read playbook from fake global dir: {path}")

if __name__ == '__main__':
    unittest.main()
```

**For the E2E test `scripts/e2e/e2e_test_1093_global_dir_decoupling.sh`**:
```bash
#!/bin/bash
set -e

# Setup mock directories
TEST_DIR=$(mktemp -d)
mkdir -p "$TEST_DIR/fake_global_dir"
mkdir -p "$TEST_DIR/fake_workdir"

# Interceptor setup
mkdir -p "$TEST_DIR/bin"
cat << 'EOF' > "$TEST_DIR/bin/openclaw"
#!/bin/bash
echo "$@" > /tmp/intercepted_prompt.log
EOF
chmod +x "$TEST_DIR/bin/openclaw"

# Execution
export PATH="$TEST_DIR/bin:$PATH"
python3 scripts/spawn_coder.py --workdir "$TEST_DIR/fake_workdir" --global-dir "$TEST_DIR/fake_global_dir" --pr-file "dummy.md" --prd-file "dummy_prd.md" || true

# Assertion
if grep -q "You are an autonomous" /tmp/intercepted_prompt.log; then
  echo "PASS: Playbook successfully injected despite fake global-dir."
else
  echo "FAIL: Playbook was empty or not injected."
  exit 1
fi
```
