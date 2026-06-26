# PRD: E2E Test Migration and Preflight Flag

## 1. Context & Problem Definition
Currently, `preflight.sh` relies on an ugly hardcoded `case` statement blacklist to filter out heavy E2E tests and mocks from the automated test discovery glob (`scripts/test_*.sh`). 
These tests have not been executed in a long time and might be broken. We need to physically separate them to avoid glob collision and introduce a dedicated flag to run them on demand.

## 2. Requirements
1. **Atomic Migration Script:** The Coder MUST write a temporary Python or Bash script (e.g., `migrate_e2e.py`) to perform the bulk renaming and moving of the heavy E2E tests from `scripts/` into a new `scripts/e2e/` directory. The scripts MUST be prefixed with `e2e_test_`. (e.g., `scripts/test_blue_green.sh` -> `scripts/e2e/e2e_test_blue_green.sh`). This script MUST also find and replace relative paths (e.g., `cd "$(dirname "$0")/.."`) inside the migrated scripts to account for the new directory depth.
2. **Execute and Delete:** The Coder MUST execute this migration script and then explicitly **delete** it before submitting the PR.
3. **Preflight Flag:** Modify `preflight.sh` to accept an `--e2e-test` flag. 
   - Default (no flag): Run exactly as it does now (discovering and running `scripts/test_*.sh` and unit tests).
   - When `--e2e-test` is provided: ALSO discover and execute the tests in `scripts/e2e/e2e_test_*.sh`.
4. **Silence the Noise (Token-Optimized CI):** When `--e2e-test` is passed and E2E tests are executed, their output MUST NOT be dumped to the console (redirect it to `/dev/null` or a separate log file). If an E2E test fails, ONLY output a single-line warning (e.g., `[E2E WARNING] e2e_test_blue_green.sh failed. Continuing.`) and exit with `0` to keep the build green.
5. **Strict Verification:** Before removing the hardcoded `case` blacklist from `preflight.sh`, the Coder must ensure no E2E scripts remain in the root `scripts/` directory. Once verified, completely remove the `case` blacklist.

## 3. Acceptance Criteria & Redlines
- [ ] `scripts/e2e/` directory exists and contains `e2e_test_*.sh` scripts with fixed relative paths.
- [ ] `preflight.sh` accepts `--e2e-test` and dynamically discovers `scripts/e2e/e2e_test_*.sh`.
- [ ] Hardcoded `case` blacklist is removed from `preflight.sh`.
- [ ] Temporary migration script is deleted.
- **CRITICAL REDLINE (No E2E Pass Guarantee):** The E2E tests have not been run in a long time and will likely fail. The Coder MUST NOT try to fix the E2E tests if they fail. Fixing them is explicitly out of scope for this Issue. The output must be silenced and non-fatal.
