---
Affected_Projects: [leio-sdlc]
---

# PRD: Fix_Planner_Slice_Numbering

## 1. Context & Problem (业务背景与核心痛点)
When the SDLC Planner agent attempts to slice a failed PR into smaller micro-PRs, it exhibits a hallucination regarding the `--insert-after` parameter. For example, if slicing `PR_001_xxx.md`, the Planner correctly uses `--insert-after 001` for the first slice (generating `PR_001_1_xxx.md`). However, for the second slice, it incorrectly infers that it needs to append to the previous slice and uses `--insert-after 001_1` (generating `PR_001_1_1_xxx.md`). This results in overly nested and incorrect sequential numbering. The underlying script (`create_pr_contract.py`) already handles the auto-increment automatically as long as the same base ID is provided.

## 2. Requirements & User Stories (需求定义)
- The `planner_slice` prompt must explicitly forbid the Planner from mutating the `--insert-after` value between slice generations.
- The Planner must be instructed to use the EXACT SAME `--insert-after` value for every slice it generates.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- **Target File**: `config/prompts.json`
- **Design Pattern**: Prompt Engineering / Prompt Hardening.
- We will update the `planner_slice` prompt template by adding a strict constraint right after the mention of `--insert-after`. We will inform the LLM that the script automatically handles sequential numbering.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1:** Slicing a failed PR
  - **Given** A failed PR `PR_001_Failed.md`
  - **When** The `planner_slice` task is executed to split it into two micro-PRs
  - **Then** The resulting PR contracts must be named `PR_001_1_...md` and `PR_001_2_...md` (not `PR_001_1_1_...md`).

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Test Target:** `scripts/test_planner_slice_failed_pr.sh`
- The existing integration tests for slicing should pass without modification, as they already check for `PR_Slice_1.md` and `PR_Slice_2.md` mock outputs based on the provided parameter. The primary change is inside the JSON configuration, and running the `spawn_planner` test in `SDLC_TEST_MODE=true` will verify that the prompt is successfully loaded and used without JSON syntax errors.

## 6. Framework Modifications (框架防篡改声明)
- None. This only targets `config/prompts.json`.

## 7. Hardcoded Content (硬编码内容)

### Exact Text Replacements:
- **In `config/prompts.json`**, under the `planner_slice` key, replace the following sentence:
  `"THEN, use the \`write\` or \`edit\` tool to fill in the contract content. The \`--insert-after\` parameter is MANDATORY for sequential ordering of the new sliced PRs."`
  
  **With the following EXACT TEXT**:
```text
THEN, use the `write` or `edit` tool to fill in the contract content. The `--insert-after` parameter is MANDATORY for sequential ordering of the new sliced PRs. DO NOT change its value between calls. Use the EXACT same `--insert-after` value for EVERY slice. The script will automatically handle the sequential numbering (e.g., 1, 2, 3) based on existing files.
```
