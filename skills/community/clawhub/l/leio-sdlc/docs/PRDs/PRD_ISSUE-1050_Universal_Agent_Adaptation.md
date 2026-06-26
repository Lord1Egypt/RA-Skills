---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1050 Universal Agent Adaptation (v9 Final)

**Status**: Completed

## 1. Context & Problem Definition (核心问题与前因后果)
The `leio-sdlc` project currently hardcodes Anthropics Claude as the primary LLM driver. To ensure vendor neutrality and resilience, we must implement a Universal Agent Adaptation layer that natively supports other models, specifically starting with Google Gemini via the `openclaw` CLI. Previous iterations successfully established strong architectural defenses, but the 8th round of Red Team auditing flagged a critical flaw: embedding real, costly LLM network calls directly into the `preflight.sh` CI hook, which violates the token-optimized CI principle. Boss has mandated a final v9 architecture that preserves all prior defenses while strictly isolating real LLM integration tests into a parameterized script.

## 2. Requirements (需求说明)
1. **Universal LLM Driver Abstraction**: Implement an `agent_driver` layer to route prompts to the correct LLM backend based on configuration (e.g., `LLM_DRIVER=gemini`).
2. **Environment Robustness**: Support dynamic path resolution with `$AGENT_SKILLS_DIR` fallback.
3. **Safety Guardrails**: Implement JIT (Just-In-Time) Prompt guardrails enforcing the File System API.
4. **Communication Channel**: Utilize a pure `stdio` terminal stealth channel to interact with `openclaw` without native plugin dependencies.
6. **Triad Integration**: Ensure the Planner, Coder, and Reviewer scripts and their playbooks are fully updated to utilize the new `agent_driver`.
7. **Isolated E2E Integration Testing**: Create a standalone script `scripts/test_agent_driver_gemini.sh` to test the real Gemini driver invocation. **Absolutely NO real network/LLM calls in `preflight.sh`**.
8. **Parameterized Test Models**: The independent testing script must allow specifying the LLM model via an environment variable or parameter (e.g., `gemini-2.0-flash`) to allow cheap probe testing and save tokens.

## 3. Architecture (架构设计)
- **agent_driver Abstraction**: The core router that dynamically selects the `openclaw` command flags based on the active `LLM_DRIVER`.
- **config/prompts.json**: Centralized dictionary of role-based prompts (Planner, Coder, Reviewer, Auditor).
- **Stealth Integration**: Uses `subprocess` and `stdio` to shell out to `gemini run --model <MODEL> (or appropriate CLI flags based on LLM_DRIVER)`, intercepting the output.
- **Isolated Testing Pipeline**: 
  - `preflight.sh` remains completely offline, fast, and token-optimized (strictly syntax/lint checks).
  - `scripts/test_agent_driver_gemini.sh` is the dedicated E2E test harness. It accepts dynamic parameters (e.g., `TEST_MODEL=google/gemini-2.0-flash` or via command-line args) to validate the real connection without incurring heavy costs during routine CI loops.

## 4. Acceptance Criteria (验收标准)
- [ ] `agent_driver` successfully routes to Gemini when `LLM_DRIVER=gemini`.
- [ ] `$AGENT_SKILLS_DIR` path fallback logic is implemented.
- [ ] JIT File System API Prompt guardrails are active and injected into context.
- [ ] `preflight.sh` contains ZERO real LLM network calls (offline checks only).
- [ ] `scripts/test_agent_driver_gemini.sh` exists, runs completely isolated from CI, and supports model parameterization.
- [ ] Triad scripts (Planner/Coder/Reviewer) successfully read from `prompts.json` and invoke the new `agent_driver`.

## 5. Framework Modifications (框架修改声明)
**Allowed Modifications:**
- `scripts/spawn_planner.py`
- `scripts/spawn_coder.py`
- `scripts/spawn_reviewer.py`
- `scripts/spawn_arbitrator.py`
- `scripts/spawn_manager.py`
- `scripts/orchestrator.py`
- `scripts/pm.py`
- `scripts/handoff_prompter.py`
- `deploy.sh`
- `scripts/agent_driver.py` (New File)
- `config/prompts.json` (New File)
- `scripts/test_agent_driver_gemini.sh` (New File)
- `playbooks/*` (Updates to Triad prompts/playbooks)

**Explicitly UN-AFFECTED Files (DO NOT MODIFY):**
- `scripts/create_pr_contract.py`
- `scripts/merge_code.py`
- `scripts/update_issue.py`
- `preflight.sh` (Only add linter/offline checks, NO LLM calls)

---

## Appendix: Architecture Evolution Trace (架构演进与审查追踪)
> **[CRITICAL INSTRUCTION FOR PLANNER & CODER]** 
> IGNORING THIS SECTION IS MANDATORY. This section is strictly for historical tracking of the PM-Auditor-Boss discussion loop. Do NOT read, reference, or implement any logic from this appendix into the SDLC pipeline.

- **v8.0**: Attempted to integrate real LLM network calls into `preflight.sh` for E2E validation.
- **Audit Rejection (v8.0)**: Red Team Auditor flagged `preflight.sh` changes as a critical violation of Token-Optimized CI (Lobster Architecture). CI must remain silent, fast, and offline.
- **v9.0 Revision Rationale**: Boss directive. Removed LLM calls from `preflight.sh`. Created `scripts/test_agent_driver_gemini.sh` as an isolated, parameterized test script (supporting cheap models like `gemini-2.0-flash`) for manual probe testing without polluting the automated CI loop.