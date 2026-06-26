# PRD-045: Automated Orchestrator State Machine (Green/Yellow/Red Path Engine)

## 1. Background & Problem Statement
Currently, the `leio-sdlc` process requires a human operator to manually string together the pipeline. If an LLM hallucinates or a task is too complex, there is no deterministic mechanism to detect failure, clean up the environment, or escalate the task. This manual "meatbag orchestration" limits the system's autonomy.

## 2. Objectives
Build `scripts/orchestrator.py`, a pure Python Finite State Machine (FSM) that:
1. Automates the full PR lifecycle from ingestion to Merge/Abort.
2. Manages Git feature branches (Idempotent creation/cleanup).
3. Implements a **3-Tier Escalation Protocol** for handling sub-agent failures.
4. Introduces Tech Lead Arbitration to resolve infinite loops.
5. Defines strict mathematical boundaries for recursive task slicing.

## 3. Tech Lead Arbitration (Resolving Reviewer vs. Coder Deadlocks)
When `spawn_reviewer.py` rejects a PR 5 consecutive times, the Orchestrator halts the Coder loop and invokes `scripts/spawn_arbitrator.py`.

**Inputs to Arbitrator:**
1. The original PR Contract (`docs/PRs/PR_XXX.md`).
2. The current code diff (`git diff master...HEAD`).
3. The final Reviewer rejection report (`review_report.txt`).

**Prompt/Instruction:**
> "You are the Tech Lead. The Coder and Reviewer are stuck in a 5-round loop. 
> Evaluate the PR requirements against the Code Diff. 
> If the code satisfies the core functional requirements and the Reviewer is being overly pedantic (e.g., minor stylistic issues, unreachable edge cases), output exactly `[OVERRIDE_LGTM]`.
> If the code genuinely fails to meet the PR requirements or has critical bugs, output exactly `[CONFIRM_REJECT]`."

**FSM Integration:**
- If Arbitrator outputs `[OVERRIDE_LGTM]`: The Orchestrator overwrites `review_report.txt` with `[LGTM] (Overridden by Tech Lead)` and transitions to **State 6 (Green Path / Merge)**.
- If Arbitrator outputs `[CONFIRM_REJECT]`: The FSM transitions to **State 5 (Red Path / Tier 1 Reset)**.

## 4. Recursive Slicing Bounds (Resolving "Too Complex" Tasks)
When a PR fails Tier 1 (Stochastic Reset), it enters Tier 2 (Micro-Slicing). The Orchestrator invokes Planner to break the failing PR into smaller pieces.

**How do we track sliced PRs?**
- YAML Frontmatter in PR documents will include `slice_depth`.
- A standard PR has `slice_depth: 0`.
- When Planner slices `PR_002_Auth.md` (depth 0), it generates `PR_002.1_DB.md` and `PR_002.2_API.md`, both with `slice_depth: 1`.
- The original `PR_002_Auth.md` is marked `status: superseded` (archived, not deleted).

**Definition of "Planner can't slice anymore":**
The Orchestrator defines a task as "Un-sliceable" (triggering Tier 3 / Dead Letter Queue) if **EITHER** of these conditions are met:
1. **Mathematical Depth Limit**: The failing PR already has `slice_depth >= 2` (Max configurable limit). We do not allow infinite recursive slicing (depth 3+).
2. **Planner Refusal**: The Orchestrator asks the Planner to slice a failing PR, but the Planner returns only 1 new PR file (meaning the LLM structurally cannot decompose the atomic task any further).

## 5. Core Architecture (The 7-State FSM)

### State 1: Polling & Job Assignment
- Polls `get_next_pr.py` (ignores `superseded` or `blocked` PRs). Mark found PR as `in_progress`.

### State 2: Branch Lifecycle (Idempotent)
- Define `feature/PR_XXX`. If exists, `git checkout`. If not, `git checkout -b`.

### State 3: Coder Execution (The Black Box)
- Invokes `spawn_coder.py`. Limits: `MAX_RUNTIME` (20m), `MAX_TOKENS` (500k).
- If Coder exits 0: Transition to **State 4**.
- If Coder times out / exceeds tokens: Transition to **State 5 (Tier 1 Reset)**.

### State 4: Reviewer Execution & Arbitration
- Invokes `spawn_reviewer.py`. Parse `review_report.txt`.
- If `[LGTM]`: Transition to **State 6 (Green Path)**.
- If `[ACTION_REQUIRED]`: Increment `rejection_count`.
  - If `< 5`: Back to **State 3**.
  - If `>= 5`: Invoke **Tech Lead Arbitrator**. (See Section 3).

### State 5: The Red Path (3-Tier Escalation)
#### Tier 1: Stochastic Reset
- `git checkout master && git branch -D <feature_branch>`.
- Restart Coder ONCE with an appended "Anti-Pattern" prompt based on the failure.
- If it fails again: Transition to **Tier 2**.

#### Tier 2: Micro-Slicing Act
- Check `slice_depth` of current PR.
- If `slice_depth >= 2`, Transition to **Tier 3**.
- Else, invoke Planner with `--slice-failed-pr`.
- If Planner generates < 2 files, Transition to **Tier 3**.
- Else, mark current PR `status: superseded`. Transition to **State 1**.

#### Tier 3: Dead Letter Queue (Human Intervention)
- Mark PR `status: blocked_fatal`.
- Prompt Boss: `[A]bort (Discard PR)`, `[C]ontinue (Manual human code fix & force merge)`.

### State 6: Green Path (Merge & Cleanup)
- Call `merge_code.py`.
- `git branch -d <feature_branch>`.
- Mark PR as `status: closed`. Transition to **State 1**.

### State 7: Fault Recovery
- On script startup, check for `in_progress` PRs. Auto-checkout existing feature branches and resume.

## 6. Testing Strategy (Deterministic Sandbox & Stubbing)
Because the FSM relies heavily on side-effects (Git operations, file I/O, subprocesses) and LLMs are non-deterministic, testing MUST NOT use real LLMs. 
We will use the **"Deterministic Sandbox"** approach:
1. **The Sandbox**: Create a temporary directory (`mktemp -d`), initialize a dummy git repo, and create dummy PR files.
2. **The Stubs**: Replace the actual `spawn_*.py` scripts with fake executable bash/python stubs that deterministically simulate agent behaviors:
   - *Stub Coder*: Always exits 0 (success) or 1 (timeout/failure) based on the test scenario.
   - *Stub Reviewer*: Always writes `[ACTION_REQUIRED]` or `[LGTM]` to `review_report.txt`.
   - *Stub Arbitrator*: Always writes `[OVERRIDE_LGTM]` or `[CONFIRM_REJECT]`.
   - *Stub Planner*: Simulates slicing by creating `PR_XXX.1.md` and `PR_XXX.2.md`.
3. **Physical Assertions**: The test script `scripts/test_orchestrator_fsm.sh` will execute `orchestrator.py` against these stubs and assert the physical state:
   - `git branch` (ensure feature branches are created/deleted correctly).
   - `cat docs/PRs/PR_XXX.md | grep status:` (ensure status transitions to `closed`, `superseded`, or `blocked_fatal`).
