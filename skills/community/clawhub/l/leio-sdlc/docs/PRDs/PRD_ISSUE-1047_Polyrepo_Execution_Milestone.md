---
Affected_Projects: [leio-sdlc, AMS]
Context_Workdir: /root/.openclaw/workspace/projects/leio-sdlc
---

# PRD: ISSUE-1047 Polyrepo Execution Milestone

> ⚠️ **STATUS: BLOCKED / PAUSED (2026-04-09)** ⚠️
> This PRD was rejected by the Auditor and the architectural feasibility was assessed as **FATAL** under the current SDLC engine. 
> **Why it failed:** 
> 1. `orchestrator.py` currently enforces a single, global `--workdir` and assumes all git commands (quarantine, state checking, merges) apply to this one repo. It cannot natively switch context to `../AMS/`.
> 2. The `prompts.json` contains a `[CRITICAL REDLINE]` explicitly forbidding the Coder from touching any file outside the absolute path of `workdir`. Bypassing this via `../AMS/` triggers a hard violation.
> 3. The newly introduced `commit_state.py` requires the PRD itself to be cleanly committed in the target workdir, causing a chicken-and-egg problem for cross-repo PRDs.
> **Next Steps before resuming:** The Orchestrator must be heavily refactored to support dynamic `workdir` binding per Micro-PR (or per target file set) rather than a global workspace constraint.

## 1. Context & Problem (业务背景与核心痛点)
Currently, `leio-sdlc` is primarily used in a self-hosting mode. To prove its maturity as a general-purpose orchestrator, we must demonstrate its ability to coordinate changes across multiple independent git repositories (Polyrepo) within a single task. This PRD targets two real-world issues in different projects to verify cross-project scheduling, testing, and merging.

## 2. Requirements & User Stories (需求定义)
- **Target 1: [leio-sdlc] Parameterize Reviewer History Depth (ISSUE-1057)**:
    - Instead of a hardcoded `max(5, pr_num)`, the history window for the exemption clause must be a CLI parameter `--history-depth` in `spawn_reviewer.py`.
    - Default value must remain `5` to maintain backward compatibility.
- **Target 2: [AMS] Decouple AMS from Direct Notifications (ISSUE-1086)**:
    - Eliminate the hardcoded `send_telegram` logic and the deprecated `telegram_notifier.py`.
    - Refactor `weekly_audit.py` and `push_arb_daily.py` to only output report text to `stdout`.
    - Remove all Telegram-specific channel IDs from the source code.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- **Multi-Project Orchestration**: The orchestrator will parse the `Affected_Projects` frontmatter and acquire locks for both `leio-sdlc` and `AMS`.
- **Atomic Modification**: 
    - Coder must modify `scripts/spawn_reviewer.py` (within `leio-sdlc`) to add the `--history-depth` argument.
    - Coder must modify `../AMS/scripts/weekly_audit.py` and `../AMS/scripts/push_arb_daily.py` (relative to the orchestrator workspace) to remove `openclaw message send` subprocess calls and replace them with `print()`.
- **Cleanup**: Delete `../AMS/scripts/telegram_notifier.py` if it exists.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: SDLC History Depth is Configurable**
    - **Given** `spawn_reviewer.py` is called with `--history-depth 10`
    - **When** generating `recent_history.diff`
    - **Then** the generated file must contain content from the last 10 commits.
- **Scenario 2: AMS Report Output via Stdout**
    - **Given** `weekly_audit.py` is executed
    - **When** the script finishes its analysis
    - **Then** it must print the report to the terminal instead of attempting to call the `openclaw` CLI for delivery.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Preflight Integration**: Both projects' `preflight.sh` must pass.
- **Polyrepo Smoke Test**: Verify that the Coder successfully switches between directories and stages files in both repositories.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/spawn_reviewer.py`
- `../AMS/scripts/weekly_audit.py`
- `../AMS/scripts/push_arb_daily.py`
- `../AMS/scripts/telegram_notifier.py` (Delete)

## 7. Hardcoded Content (硬编码内容)
- **`history_depth_help` (For spawn_reviewer.py)**: `"Number of recent commits to include in the history diff for the exemption clause (default: 5)"`

## Appendix: Architecture Evolution Trace (架构演进与审查追踪)
- **v1.0**: Consolidated 1057 and 1086 into a single polyrepo verification task. Removed the "configurable target" middle-ground for 1086 in favor of complete stdout decoupling.
