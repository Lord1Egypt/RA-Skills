---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1098_UAT_Verifier

## 1. Context & Problem (业务背景与核心痛点)
Currently, our SDLC pipeline ends at State 5 (Merge to Master). However, a merged PR does not guarantee that 100% of the PRD requirements (e.g., legacy string cleanups, exact hardcoded strings) were perfectly translated into code. As seen in previous hotfixes, we lack a final Post-Merge acceptance validation step (User Acceptance Testing / UAT). 
We need a "Ticket-Level" Verifier Agent that acts as an independent QA. It will read all PRDs associated with an Issue (including hotfixes), inspect the final codebase, and generate a structured JSON Acceptance Report. This provides the Manager/Boss with a clear, data-driven summary to decide whether to close the Issue or spawn a hotfix.

## 2. Requirements & User Stories (需求定义)
1. **Agentic QA Simulator**: A standalone script (`spawn_verifier.py`) that assumes a read-only QA persona to cross-check PRD requirements against the codebase.
2. **Ticket-Level Context**: The Verifier must accept multiple PRDs as input (e.g., initial PRD + hotfix PRDs) to understand the complete requirement baseline.
3. **Structured JSON Outcome**: The Verifier must output its findings strictly as a JSON artifact (`uat_report.json`), avoiding unstructured markdown chatter.
4. **Pipeline Handoff**: The Orchestrator must automatically trigger this Verifier at the very end of the pipeline (when all PRs are merged), broadcast the JSON results to Slack, and halt for Manager approval.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
> **[Instruction to Main Agent/Architect]**
To preserve system stability, implement this in two distinct PRs:

**PR 1: UAT Verifier Core Engine**
- **Action**: Create `scripts/spawn_verifier.py` leveraging the existing `agent_driver.py` mechanism.
- **Input**: `--prd-files` (comma-separated paths to PRDs), `--workdir`, and `--out-file` (default `uat_report.json`).
- **Playbook**: Create `playbooks/verifier_playbook.md`. The persona must be defined as a read-only QA. It must be instructed to extract all requirements from the provided PRD(s) and use file-reading tools to verify their existence in the code.
- **Prompt Config**: Add a `"verifier"` template to `config/prompts.json` enforcing the JSON output schema (defined in Section 7).

**PR 2: Orchestrator Integration (State 6 UAT & JIT Handoff)**
- **Action**: Modify `scripts/orchestrator.py`.
- **Logic & File Storage**: After the job queue is completely empty (all PRs merged), introduce a final step. The Orchestrator collects all PRD files in the current job directory, calls `spawn_verifier.py`, and reads the resulting `uat_report.json` physically saved in the run directory.
- **Notification**: Format a concise summary into a readable Slack message (e.g., "UAT Verification completed. Status: [PASS/NEEDS_FIX]. Manager is reviewing...") and broadcast it.
- **JIT Prompt & Exit Codes (CRITICAL)**: The Orchestrator must parse the JSON status and explicitly hand control back to the Manager Agent via standard output:
  - If `PASS`: Print `[SUCCESS_HANDOFF] UAT Passed. You are authorized to close the ticket using issues.py.` and call `sys.exit(0)`.
  - If `NEEDS_FIX`: Print `[ACTION REQUIRED FOR MANAGER] UAT Failed. Read uat_report.json, summarize the MISSING items to the Boss, and ask whether to append a hotfix or redo.` and call `sys.exit(1)`.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Complete Implementation Verification**
  - **Given** A codebase perfectly matching the PRDs
  - **When** `spawn_verifier.py` is executed with the PRD files
  - **Then** It outputs a `uat_report.json` with `"status": "PASS"` and all requirements marked as `IMPLEMENTED`.
- **Scenario 2: Flawed Implementation Detection**
  - **Given** A codebase where a hardcoded string from the PRD was missed
  - **When** `spawn_verifier.py` is executed
  - **Then** It outputs a `uat_report.json` with `"status": "NEEDS_FIX"` and explicitly flags the missed requirement as `MISSING`.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **E2E Mock Testing**: Create `scripts/e2e/e2e_test_verifier_mock.sh`. Mock the agent's LLM response to output a valid `uat_report.json`. Ensure `spawn_verifier.py` successfully writes the artifact and exits with 0.
- **Orchestrator Resilience**: Ensure the Orchestrator safely handles cases where the Verifier hallucinated invalid JSON (fallback to raw text notification or a safe error message) instead of crashing.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/spawn_verifier.py` (CREATE)
- `playbooks/verifier_playbook.md` (CREATE)
- `scripts/orchestrator.py`
- `config/prompts.json`

## 7. Hardcoded Content (硬编码内容)
- **`verifier_json_schema` (For `config/prompts.json` -> "verifier")**:
```json
{
  "status": "(PASS|NEEDS_FIX)",
  "executive_summary": "A concise summary of the UAT outcome.",
  "verification_details": [
    {
      "requirement": "Description of the requirement extracted from the PRD(s).",
      "status": "(IMPLEMENTED|MISSING|PARTIAL)",
      "evidence": "File paths, code snippets, or tool output proving the status.",
      "comments": "Any notes or suggestions for hotfixes if applicable."
    }
  ]
}
```

- **`uat_pass_jit_prompt` (For `scripts/orchestrator.py` stdout)**:
```text
[SUCCESS_HANDOFF] UAT Passed. You are authorized to close the ticket using issues.py.
```

- **`uat_fail_jit_prompt` (For `scripts/orchestrator.py` stdout)**:
```text
[ACTION REQUIRED FOR MANAGER] UAT Failed. Read uat_report.json, summarize the MISSING items to the Boss, and ask whether to append a hotfix or redo.
```

- **`uat_slack_notification_template` (For `scripts/orchestrator.py` channel broadcast)**:
```text
UAT Verification completed. Status: {status}. Manager is reviewing...
```