---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1057_Cross_PRD_History_Exemption

## 1. Context & Problem (业务背景与核心痛点)
Currently, the `recent_history.diff` passed to the Reviewer for the 'exemption clause' (to avoid rejecting a PR if work was already done) is calculated dynamically using a simplistic formula: `history_depth = max(5, pr_num)`. This simplistic backward lookup breaks under two conditions:
1. **Yellow Path Iterations**: When a PR goes through multiple reject/fix cycles, the commit count swells, causing the history window to fall short of reaching previous PRs.
2. **Cross-PRD Handoffs**: If a feature required in a new PRD was already implemented days ago in an older PRD, the Coder provides an empty `current_review.diff`. The Reviewer checks the tiny `5-commit` history window, finds no trace of the implementation, and incorrectly rejects the PR for "missing requirements," leading to a fatal deadlock.

We need a deterministic approach to compute the `recent_history.diff`. The solution is "Baseline Drift Anchoring": capturing the `HEAD` commit hash the moment the SDLC Orchestrator begins a PRD pipeline, and using the diff between that baseline and the current master as the absolute source of truth for "what has been accomplished so far in this pipeline."

## 2. Requirements & User Stories (需求定义)
1. **Deterministic SDLC Baseline**: The Orchestrator must record the exact `git rev-parse HEAD` when a pipeline starts (State 0 or initialization).
2. **State Resilience**: This baseline hash must be physically saved to a `.baseline_commit` file within the job's run directory so it survives process crashes or pipeline resumption.
3. **Accurate History Generation**: `spawn_reviewer.py` must stop using the arbitrary `max(5, pr_num)` formula. It must read the `.baseline_commit` file and execute a `git log -p <baseline_hash>..HEAD` (or equivalent diff) to generate `recent_history.diff`.
4. **Graceful Fallback**: If the baseline file is missing (e.g., legacy runs), it should gracefully fall back to the old depth-based logic.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
> **[Instruction to Main Agent/Architect]**
To prevent blast radius, implement this in two focused, atomic PRs:

**PR 1: Orchestrator Baseline Anchoring**
- **Target**: `scripts/orchestrator.py`
- **Logic**: During State 0 (or before checking out the first PR), capture the current `HEAD` commit using `git rev-parse HEAD`. Write this string to a file named `baseline_commit.txt` inside `run_dir`.
- **Constraint**: Do not overwrite the file if the Orchestrator is resuming a queue and the file already exists.

**PR 2: Reviewer History Strategy Shift**
- **Target**: `scripts/spawn_reviewer.py`
- **Logic**: Before generating `recent_history.diff`, attempt to read `baseline_commit.txt` from `args.run_dir`.
  - If found: Construct `history_cmd = f"git log -p {baseline_hash}..HEAD > ..."`.
  - If missing (Fallback): Use the legacy `history_depth = max(5, pr_num)` logic.
- **Cleanup**: Remove any legacy comments or dead code referencing the old limitation.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Baseline Anchoring on Startup**
  - **Given** The Orchestrator starts a new PRD pipeline
  - **When** State 0 is executed
  - **Then** A `baseline_commit.txt` file is generated in the run directory containing the exact 40-character SHA-1 hash of the master branch.
- **Scenario 2: Accurate History Generation**
  - **Given** A Reviewer is spawned for PR_003
  - **When** `spawn_reviewer.py` executes
  - **Then** It reads `baseline_commit.txt` and executes `git log -p <hash>..HEAD` to populate `recent_history.diff`, effectively capturing every change made since the pipeline started.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Unit Testing**: Update `tests/test_triad_agent_driver.py` (or similar spawn tests) to mock the presence and absence of `baseline_commit.txt` and assert that `spawn_reviewer.py` invokes the correct `subprocess.run` command.
- **E2E Stability**: The existing test suite will verify that this change doesn't break the standard pipeline flow.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/orchestrator.py`
- `scripts/spawn_reviewer.py`

## 7. Hardcoded Content (硬编码内容)
- **Baseline Filename**: The anchor file MUST be named exactly: `baseline_commit.txt`