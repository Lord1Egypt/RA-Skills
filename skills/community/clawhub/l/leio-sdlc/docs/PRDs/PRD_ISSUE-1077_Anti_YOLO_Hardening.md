---
Affected_Projects: [leio-sdlc]
Status: Completed
---

# PRD: ISSUE-1077 Anti-YOLO Guardrail Hardening

## 1. Context & Problem (业务背景与核心痛点)
The SDLC process is vulnerable to "YOLO" loops where the Main Agent auto-corrects PRDs without human authorization. Additionally, recent attempts to add basic channel parameter validation triggered a catastrophic loop of micro-slicing because of poor testability and Reviewer's rigid scope alignment. We must solve both the YOLO execution issue and the testability blocker (Catch-22 Deadlock).

## 2. Requirements & User Stories (需求定义)
1.  **Shared Notification Infrastructure**: Refactor `notify_channel` out of `orchestrator.py` into a shared library to eliminate duplicated logic and make scripts easily testable via simple mocks.
2.  **Auditor Observability & Interruption**: `spawn_auditor.py` must support a `--channel` argument, use the shared notification infrastructure to post updates, and output JIT prompt injections.
3.  **Hardcoded Content Mandate**: Add a new section to the PRD template to enforce pixel-perfect copying of string literals.
4.  **PM Skill Guardrail**: The `pm-skill/SKILL.md` must be updated with an explicit circuit-breaker instruction.
5.  **Strict Anti-Slicing Directive**: The Planner must NOT slice the functional code and its unit tests into separate atomic PRs. They must be handled as a single cohesive unit to avoid Reviewer deadlocks.
6.  **Pipeline Robustness Upgrades**: Resolve the infinite slicing loop caused by the combination of rigid `Target Working Set` constraints and aggressive escalation rules.
    - Fix the Planner prompt to allow returning a single PR when a task is an indivisible TDD unit.
    - Relax the Reviewer prompt to permit modifications to auxiliary/test files outside the strict Target Working Set as long as CI passes.
    - Modify the Orchestrator to allow 3 retries (with revision feedback) before triggering the Planner split (escalation).

## 3. Architecture & Technical Strategy (架构设计与技术路线)
-   **`scripts/agent_driver.py`**: Extract the `notify_channel` function from `orchestrator.py` and place it here. Ensure `format_notification` is imported or handled properly if used by `notify_channel`.
-   **`scripts/orchestrator.py`**: Import `notify_channel` from `agent_driver.py` and remove the local definition.
-   **`scripts/spawn_auditor.py`**: Add `--channel` argument parsing (using standard `argparse` best practices, ensuring it doesn't break when called via other means). Add a fail-fast handshake if `--channel` is missing. Use `agent_driver.notify_channel` for Slack messages. Output `[ACTION REQUIRED FOR MANAGER]` JIT prompt injections to stdout upon completion or failure.
-   **`skills/pm-skill/TEMPLATES/PRD.md.template`**: Add a `## 7. HARDCODED CONTENT (CODER MUST COPY EXACTLY)` section.
-   **`skills/pm-skill/SKILL.md`**: Append the `End of Task & Circuit Breaker` guardrail section. (Note: Modifying this is safe because it is a local internal replica within the `leio-sdlc` repository. It does not violate cross-project boundaries).
-   **`config/prompts.json`**: Update the "auditor" prompt to explicitly specify the PRD file path to fix prompt blindness. Update "planner_slice" to stop forcing at least 2 micro-PRs, allowing it to output a single PR or refine the current contract if splitting breaks atomicity. Update "reviewer" to relax the Target Working Set boundaries.
-   **`scripts/orchestrator.py`**: Import `notify_channel` from `agent_driver.py` and remove the local definition. Increase the escalation `reset_count` limit from 1 to 3, giving the Coder more chances to fix tests before triggering the `planner_slice` logic.
-   **Deployment Strategy**: Changes made to `skills/pm-skill/SKILL.md` within the workspace source will be synchronized to the global runtime skill directory post-merge via the `kit-deploy.sh` pipeline, mitigating any path isolation risks.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
-   **Scenario 1: Shared Infrastructure Refactoring**
    -   **Given** A test script invokes `orchestrator.py` or `spawn_auditor.py`
    -   **When** A notification is sent
    -   **Then** Both scripts successfully route the call through `agent_driver.notify_channel`.
-   **Scenario 2: Auditor Reject/Approve Flow with JIT**
    -   **Given** `spawn_auditor.py` is run with a valid `--channel`
    -   **When** the auditor rejects or approves the PRD
    -   **Then** The target Slack channel receives status updates via the shared function.
    -   **And** `stdout` ends with the correct REJECT or APPROVE JIT prompt.
-   **Scenario 3: Handshake Fail**
    -   **Given** `spawn_auditor.py` is run without a valid `--channel`
    -   **Then** The script terminates immediately (fail-fast) and prints the Handshake Fail JIT prompt.
-   **Scenario 4: Template and Skill Updates**
    -   **Given** The SDLC pipeline completes
    -   **Then** `skills/pm-skill/TEMPLATES/PRD.md.template` contains the exact Hardcoded Content block for PRDs.
    -   **And** `skills/pm-skill/SKILL.md` contains the exact Circuit Breaker block.
-   **Scenario 5: Escalation Robustness**
    -   **Given** The orchestrator triggers the state 5 escalation block
    -   **When** The retry counter is evaluated
    -   **Then** It should allow up to 3 resets (reset_count < 3) before shifting to `spawn_planner.py --slice-failed-pr`.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
-   **Unit Tests for `spawn_auditor.py`**: MUST use `@patch("agent_driver.notify_channel")` to intercept and assert channel calls. **DO NOT** use `subprocess.run` to execute the script in a black box or inject test-only environment variables (`os.environ.get("SDLC_TEST_MODE")`) into production code.
-   **Unit Tests for `orchestrator.py`**: Existing tests for `orchestrator.py` must be updated to mock `agent_driver.notify_channel` instead of `subprocess.run`.
-   **ATOMICITY MANDATE**: Planner is forbidden from slicing the functional modifications and test modifications of `spawn_auditor.py` across multiple PRs. They must be merged in one step to prevent Reviewer format truncation and Scope Creep violations.
-   **Rollback Plan**: If this PRD execution causes CI/CD deadlock or orchestrator crash, immediately execute `git checkout master && git reset --hard && git clean -fd` to rollback safely to the pre-PRD state.

## 6. Framework Modifications (框架防篡改声明)
> **[CRITICAL GUARDRAIL FOR CODER]**: The file paths listed below are relative to the current project's working directory (`/root/.openclaw/workspace/projects/leio-sdlc`). When using OpenClaw native file tools (`read`, `write`, `edit`), you **MUST use their absolute paths** (e.g., `/root/.openclaw/workspace/projects/leio-sdlc/skills/pm-skill/SKILL.md`) because native tools resolve relative paths against the global OpenClaw root, not the `cwd`.
-   `scripts/agent_driver.py`
-   `scripts/orchestrator.py`
-   `scripts/spawn_auditor.py`
-   `tests/test_spawn_auditor.py` (New file)
-   `tests/test_orchestrator_cli.py` (Modify imports/mocks)
-   `skills/pm-skill/SKILL.md`
-   `skills/pm-skill/TEMPLATES/PRD.md.template`
-   `config/prompts.json`

---
## 7. HARDCODED CONTENT (CODER MUST COPY EXACTLY)

**1. Content for `skills/pm-skill/TEMPLATES/PRD.md.template`:**
(Append the following section to the end of the file)
```markdown
---

## 7. HARDCODED CONTENT (CODER MUST COPY EXACTLY)
> [CRITICAL INSTRUCTION TO CODER] For any modifications involving specific string literals (e.g., SKILL.md content, Playbook rules, JIT prompts, error messages), you MUST NOT generate them yourself. You are required to copy the exact content provided below in this section.
```

**2. Content for `skills/pm-skill/SKILL.md`:**
(Append the following section to the end of the file)
```markdown
## End of Task & Circuit Breaker (CRITICAL)
Once you have written and saved the PRD file, your active role as PM is **100% COMPLETE**.
1. **Trigger Auditor**: You must immediately call `spawn_auditor.py` to check your work.
2. **Circuit Breaker (NO YOLO)**: If the Auditor returns `{"status": "REJECTED"}`, Report the rejection reasons to the Boss, then you MUST immediately halt all further operations and WAIT for explicit instructions. DO NOT ATTEMPT TO AUTO-CORRECT.
3. **Wait for Launch**: If the Auditor returns `{"status": "APPROVED"}`, Notify the Boss of the successful audit, then you MUST immediately halt all further operations and WAIT for explicit authorization to execute.
```

**3. Content for JIT Prompts in `scripts/spawn_auditor.py`:**
- **On Handshake Fail**: `[ACTION REQUIRED FOR MANAGER] [FATAL] Channel handshake failed. You MUST provide a valid --channel parameter (e.g., slack:#XXXX) and retry.`
- **On REJECT**: `[ACTION REQUIRED FOR MANAGER] The Auditor REJECTED the PRD. Report the rejection reasons to the Boss, then you MUST immediately halt all further operations and WAIT for explicit instructions.`
- **On APPROVE**: `[ACTION REQUIRED FOR MANAGER] The Auditor APPROVED the PRD. Notify the Boss of the successful audit, then you MUST immediately halt all further operations and WAIT for explicit authorization to deploy.`

**4. Content for `config/prompts.json`:**

*(Update "auditor" key)*:
```json
"You are the deterministic Red Team Auditor. Read your strict auditing guidelines from {base_dir}/playbooks/auditor_playbook.md. The PRD you must audit is located at {prd_file}. You MUST use the `read` tool to read this PRD file before generating your verdict. You MUST output ONLY valid JSON without Markdown wrappers."
```

*(Update "planner_slice" key - Replace the end of the prompt to stop forcing 2 PRs)*:
Find the sentence: `You MUST generate at least 2 Micro-PRs for this feature. Ensure you define a Target Working Set for each sliced Micro-PR. Start now.`
Replace it EXACTLY with:
```json
"You are encouraged to refine the scope or architecture of the failed PR. If the feature can be safely divided into smaller TDD-compliant steps, generate 2 or more Micro-PRs. If the feature is an indivisible atomic unit (like extracting a shared function and updating its tests), you MAY output exactly 1 refined Micro-PR. Ensure you define a Target Working Set for each PR. Start now."
```

*(Update "reviewer" key - Relax the strict Working Set rule)*:
Find the sentence: `All security checks, redlines, and logic validations MUST be strictly applied ONLY to this file.`
Add this sentence immediately after it:
```json
"You MUST NOT reject the PR solely because the Coder modified auxiliary/test files outside the Target Working Set, provided those modifications are logically required to make the CI pipeline pass and do not introduce Scope Creep."
```