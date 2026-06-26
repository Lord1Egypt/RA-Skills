---
Affected_Projects: [List the target projects here, e.g., leio-sdlc, AMS]
---

# PRD: ISSUE-1097_HOTFIX_Cleanup_Legacy_Strings_2

## 1. Context & Problem (业务背景与核心痛点)
In ISSUE-1096, we migrated the Reviewer output artifact from `Review_Report.md` to a structured `review_report.json`. While the core parser and prompt templates were updated, a post-execution deep grep revealed that the old string `Review_Report.md` and `Review_Report.md.template` were not completely eradicated from the codebase (e.g., dead code in `spawn_reviewer.py`, stale fallback logs in `orchestrator.py`).
The Coder failed to comprehensively execute the cleanup because there was **no programmatic enforcement mechanism** to catch the omission during the CI phase. We must clean up these residual strings and introduce an automated, physical block to ensure complete eradication.

## 2. Requirements & User Stories (需求定义)
1. **Zero Legacy Artifact Strings**: Global search for `Review_Report.md` must yield zero matches in functional codebase paths.
2. **Programmatic Validation**: We introduce an automated CI guardrail (Architectural TDD) that actively enforces the absence of these strings, ensuring that any future Coder hallucination or laziness is physically blocked by a failing test.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
> **[Instruction to Main Agent/Architect]**
To preserve the "Always Green CI" rule and prevent a RED-state deadlock, the implementation MUST be atomic and contained within a single PR.

**PR 1: Atomic Cleanup & Guardrail Implementation**
- **Action**: Combine the legacy string cleanup and the programmatic test guardrail into a single PR.
- **Cleanup**: 
  - In `scripts/orchestrator.py`, replace legacy fallback references.
  - In `scripts/spawn_reviewer.py`, remove the dead code that attempts to read `TEMPLATES/Review_Report.md.template`.
  - In `scripts/migrate_mocks.py`, ensure the replacement logic is safe.
- **Test Guardrail**: Create a new test file `tests/test_legacy_string_cleanup.sh`.
- **Logic**: This script must execute a recursive search across `scripts/`, `tests/`, `config/`, and `playbooks/`. 
  - **CRITICAL ANTI-SELF-MATCH GUARD**: To prevent the test from failing by finding its own source code, the search string MUST be dynamically constructed (e.g., `SEARCH_STR="Review"_"Report.md"` and `grep -rn "$SEARCH_STR"`), or explicitly exclude its own filename via `--exclude=test_legacy_string_cleanup.sh`.
  - If any matches are found, it must `echo` the violating files and `exit 1`. Otherwise, it must `exit 0`. 
- **Integration**: `preflight.sh` will automatically discover and run this new script. Because the cleanup and the test are committed atomically in this single PR, the test will pass immediately, preserving the GREEN CI pipeline and successfully satisfying the orchestrator's exit condition.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Automated Enforcement Trigger**
  - **Given** The newly created `test_legacy_string_cleanup.sh`
  - **When** Executed via `preflight.sh` with a dirty codebase
  - **Then** The script catches the residual strings and forcefully fails the build with `exit 1`.
- **Scenario 2: Successful Eradication**
  - **Given** The fully modified codebase
  - **When** `preflight.sh` runs the test suite
  - **Then** `test_legacy_string_cleanup.sh` passes successfully, and the orchestrator merges the changes.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Architectural TDD**: We are flipping the script. Instead of manually auditing the Coder's work, we are inserting a permanent `grep` assertion into the CI pipeline. If the Coder misses a file, the `tests/test_legacy_string_cleanup.sh` will fail. The Coder will be trapped in the RED-CI loop until every single string is eliminated.

## 6. Framework Modifications (框架防篡改声明)
- `tests/test_legacy_string_cleanup.sh` (CREATE)
- `scripts/orchestrator.py`
- `scripts/spawn_reviewer.py`
- `scripts/migrate_mocks.py`

## 7. Hardcoded Content (硬编码内容)
- The test script MUST construct the search string safely to avoid self-referencing. Example:
```bash
SEARCH_STR="Review"_"Report.md"
grep -rn --exclude="test_legacy_string_cleanup.sh" "$SEARCH_STR" scripts/ tests/ config/ playbooks/
```
