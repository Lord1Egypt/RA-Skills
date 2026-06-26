# 🚀 OpenClaw Agent v3.0: Evolution Guide from Assistant to Coordinator

This guide is designed to help OpenClaw users upgrade their agents from simple "Instruction Executors" to "v3.0 Coordinators" with deep orchestration capabilities.

## 🌟 What is the v3.0 Coordinator Mode?

Traditional Agent modes follow a **linear execution** path: `Receive Instruction` → `Call Tool` → `Output Result`. This pattern often loses detail and relies on "luck" when facing complex tasks like large-scale refactoring or deep financial analysis.

**v3.0 Coordinator Mode** upgrades the workflow to a **closed-loop orchestration**:
`Receive` → `Deconstruct` → `Parallel Research` → `Synthesis` → `Precise Execution` → `Verification`

---

## 🛠️ Four Core Capability Upgrades

### 1. Mandatory Synthesis
**Core Logic**: Prohibit passing raw research results directly to the execution step.
*   **Ban**: Phrases like "Based on the research, please fix X" are forbidden.
*   **Requirement**: Before issuing any execution command, the agent must internally synthesize fragmented data into a **self-contained** precise plan, including: absolute paths, specific line numbers, exact parameters, and defined expected results.
*   **Value**: Eliminates guesswork at the execution end and dramatically increases the first-time success rate.

### 2. Atomic Task Scheduling
**Core Logic**: Implement a task state machine (`Pending` → `Running` → `Terminal`).
*   **Parallelism Awareness**: Identify which tasks can run concurrently (e.g., reading 5 files at once) and which must be serial (e.g., modify code → run tests).
*   **Value**: Greatly increases speed while maintaining strict logical dependencies.

### 3. Dynamic Context Injection
**Core Logic**: Force synchronization of "System Snapshots" before task initiation.
*   **Snapshot Mechanism**: Automatically fetch the current Git branch, directory structure, and environment variables.
*   **Precision Backtracking**: Optimize index for history to ensure suggestions are based on the most current state of the system, not fuzzy memory.

### 4. Verification as Proof
**Core Logic**: Verification $\neq$ Confirming Existence → Verification = Proving Effectiveness.
*   **Closed-Loop Protocol**: `Execute` → `Verify` → `Correct`.
*   **Requirement**: After modifying code, the agent must not simply `cat` the file to confirm the change. It MUST prove the function works via running tests, type-checks (Lint), or edge-case probing.

---

## 🎯 Fool-Proof Implementation Steps

To evolve your OpenClaw Agent immediately, follow these steps:

### Step 1: Source Deconstruction (Learning Phase)
It is recommended that the agent reads the following core source files to internalize the logic:
- `src/coordinator/coordinatorMode.ts`: Understand coordinator roles and synthesis logic.
- `src/services/tools/toolOrchestration.ts`: Understand the partitioning mechanism for parallel vs serial tool calls.
- `src/services/extractMemories/extractMemories.ts`: Understand background memory distillation and the Forked Agent pattern.
- `src/query.ts`: Understand the main loop's error recovery and context compaction.

### Step 2: Gene Locking (Persistence Phase)
Write the following templates into your workspace files (see `SOP_GENE_LOCKING.md`).

1.  **Update `IDENTITY.md`**: Inject the [Mandatory Synthesis] and [Partitioned Parallelism] into the core identity.
2.  **Update `AGENTS.md`**: Upgrade `qa_agent` to a "Prover" role and add the [Sub-Agent Management Matrix].

### Step 3: Behavior Internalization (Practice Phase)
Strictly enforce the cycle: **Research → Synthesize → Execute → Verify** in all subsequent tasks.

---

## 📋 Sub-Agent Management Matrix (Continue vs Spawn)

When coordinating tasks, decide whether to reuse a worker or spawn a new one:

| Scenario | Action | Reason |
| :--- | :--- | :--- |
| Research scope matches execution scope exactly | **Continue** | Worker already has the context; maximum efficiency |
| Research was broad but execution is narrow | **Spawn Fresh** | Avoid carrying noise; cleaner context |
| Correcting a failure or extending recent work | **Continue** | Worker knows what was tried and why it failed |
| Verifying code written by another worker | **Spawn Fresh** | Verifier should have an independent perspective |
| Previous attempt followed the wrong path | **Spawn Fresh** | Avoid anchoring on the failed path; clear the slate |
