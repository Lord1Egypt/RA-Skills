# PRD: Automated Test Discovery in Preflight

## 1. Context & Problem Definition
Currently, preflight.sh hardcodes the list of test scripts. If a developer adds a test but forgets to update preflight.sh, the test is bypassed in CI. This is a generic pattern problem originating from `standard_preflight.template.sh`.

## 2. Requirements
- **Polyglot Test Discovery:** Refactor `preflight.sh` to dynamically find and execute tests across languages.
  - Bash: Discover all `scripts/test_*.sh`.
  - Python: Execute `python3 -m unittest discover -s tests -p "test_*.py"` (if `tests/` exists) AND `scripts/test_*.py`.
  - Node.js: Execute `scripts/test_*.js` or `npm test` if `package.json` exists.
- **Extreme Restraint CI (Anti-Explosion):** 
  - **Aggregated Success:** MUST NOT print individual "Pass" lines for each test script. Maintain a counter and print a single aggregate success message (e.g., `✅ 38 Bash tests passed.`).
  - **Hard-Capped Error Output:** When a test fails, MUST output ONLY the error trace, hard-capped to a maximum of 50 lines (e.g., `tail -n 50 "$TMP_TEST_LOG"` or `grep | head -n 50`). Never use `cat "$TMP_TEST_LOG"` directly.
  - **Exclude Heavy E2E Tests:** Ensure heavy external tests (like `test_agent_driver_gemini.sh` or non-unit tests) are explicitly excluded from automated bash discovery to prevent API rate limit explosions. Rename them to `e2e_*.sh` or filter them out.
- **Fail-Fast:** Stop immediately upon the first test failure.
- **Retroactive Patching:** Apply these changes to the global template `/root/.openclaw/workspace/projects/docs/TEMPLATES/standard_preflight.template.sh` and ALL existing `preflight.sh` scripts in the workspace (e.g., `leio-sdlc/preflight.sh`, `skills/pm-skill/preflight.sh`, `skills/leio-auditor/preflight.sh`).

## 3. Framework Modifications
- `projects/docs/TEMPLATES/standard_preflight.template.sh` (modified)
- `preflight.sh` (modified)
- `skills/pm-skill/preflight.sh` (modified)
- `skills/leio-auditor/preflight.sh` (modified)

## 4. Auditor Constraints (Red Team)
- **Empty Test Sets:** MUST use `shopt -s nullglob` in Bash to gracefully handle cases where no test files exist for a specific language (preventing glob errors).
- **Execution Context:** All dynamic test executions MUST occur from the project root directory.
- **Redirection Safety:** Redirect output to a temporary log file, ensuring clean teardown via `trap`.
