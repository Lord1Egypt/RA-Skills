---
Affected_Projects: [leio-sdlc]
Context_Workdir: /root/.openclaw/workspace/projects/leio-sdlc
---

# PRD: ISSUE-1058 Prevent SDLC_TEST_MODE Leakage in Production

## 1. Context & Problem (业务背景与核心痛点)
ISSUE-1058: The `SDLC_TEST_MODE=true` environment variable is used to mock LLM calls during tests. If a developer accidentally exports this variable globally and then starts the production orchestrator, the environment variable leaks into the production pipeline. This causes production agents (like Reviewer) to hallucinate that they are in a test, generating mock approvals for empty diffs, which ultimately crashes the pipeline via guardrail violations.

## 2. Requirements & User Stories (需求定义)
- Implement a context-aware guardrail in `orchestrator.py` to detect `SDLC_TEST_MODE` leakage.
- If `SDLC_TEST_MODE=true` is detected while running from the source workspace (development mode, indicated by `--enable-exec-from-workspace` or `__file__` path), emit a visible WARNING but allow execution.
- If `SDLC_TEST_MODE=true` is detected while running from the production runtime (`~/.openclaw/skills/leio-sdlc` without the bypass flag), emit a FATAL_STARTUP JIT prompt and immediately terminate the pipeline.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- Locate the runtime validation logic in `scripts/orchestrator.py` (likely near early startup checks).
- Add a check for `os.environ.get("SDLC_TEST_MODE") == "true"`.
- Use the existing `args.enable_exec_from_workspace` flag to differentiate between development/test intent and accidental production leakage.
- Add a new `handoff_test_mode_leakage` prompt to `config/prompts.json` for the fatal error.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1:** Developer runs orchestrator in workspace with test mode.
  - **Given** `SDLC_TEST_MODE=true` and orchestrator is run with `--enable-exec-from-workspace`
  - **When** `orchestrator.py` starts
  - **Then** it prints a warning about running in test mode and continues execution.
- **Scenario 2:** User runs production orchestrator with leaked test mode.
  - **Given** `SDLC_TEST_MODE=true` and orchestrator is run without the `--enable-exec-from-workspace` override flag
  - **When** `orchestrator.py` starts
  - **Then** it prints the `handoff_test_mode_leakage` fatal prompt and exits with code 1.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- Create a new e2e test script `scripts/e2e/e2e_test_1058_test_mode_leakage.sh` to verify both the warning scenario and the fatal scenario by invoking `orchestrator.py` with and without `--enable-exec-from-workspace` while `SDLC_TEST_MODE=true`.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/orchestrator.py`
- `config/prompts.json`
- New: `scripts/e2e/e2e_test_1058_test_mode_leakage.sh`

## 7. Hardcoded Content (硬编码内容)
- **`handoff_test_mode_leakage` (For config/prompts.json and Orchestrator)**:
  `"[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nProduction runtime detected but SDLC_TEST_MODE is enabled. This will cause catastrophic mock failures. You MUST run 'unset SDLC_TEST_MODE' before starting the production pipeline."`
- **`test_mode_warning` (For Orchestrator)**:
  `"[WARNING] Running Orchestrator in TEST MODE with mocked LLMs. Production safety checks are bypassed."`

## Appendix: Architecture Evolution Trace (架构演进与审查追踪)
- **v1.0**: Initial PRD drafted to solve the leaky environment variable via context-aware execution guardrails.