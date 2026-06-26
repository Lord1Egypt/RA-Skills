---
Status: Completed
Affected_Projects: [leio-sdlc, AMS]
---

# PRD: Global Pipeline Lock (v4)

## Context
The previous V3 PRD for the Global Pipeline Lock feature was rejected due to three critical flaws:
1.  **Chicken-and-Egg Race Condition**: The Orchestrator could not know which locks to acquire before executing the Planner slice, but the slicing process itself required locks to proceed safely.
2.  **Cleanup Blast Radius**: The `--cleanup` flag risked blindly deleting other pipelines' locks if it cleaned a shared directory without state awareness.
3.  **Lock Leakage on Fail-Fast**: If acquiring multiple locks failed midway, the previously acquired locks were leaked and never released, causing pipeline deadlocks.

This v4 revision introduces strict static frontmatter parsing, atomic acquisition with rollback mechanisms, and a lock manifest to guarantee safe and isolated cleanup.

## Requirements
1.  **Static Frontmatter Declaration**: PRD documents MUST contain a static frontmatter or a clear header section (e.g., `Status: Completed
Affected_Projects: [leio-sdlc, AMS]`).
2.  **Pre-Flight Parsing**: The Orchestrator parses this `Affected_Projects` list at the very start of execution (T=0) to know exactly which locks to acquire before invoking the Planner or any other components.
3.  **Atomic Acquisition & Rollback**: Lock acquisition MUST be atomic. The Orchestrator sorts the projects lexicographically and attempts to lock them via file system locks (e.g., `.openclaw/workspace/locks/<project_name>.lock`).
4.  **Fail-Fast & Rollback Protocol**: If ANY lock fails to acquire, the Orchestrator MUST catch the error, perform a reverse Rollback to release any locks it already successfully acquired in this batch, and then exit to prevent Lock Leakage.
5.  **Lock Manifest (Ownership)**: Upon successfully acquiring all required locks, the Orchestrator MUST write a `.sdlc_lock_manifest.json` file inside its current working directory (the project it was invoked from) recording exactly which locks it holds.
6.  **Safe Cleanup (`--cleanup`)**: The existing `scripts/orchestrator.py --cleanup` command MUST be updated to read the `.sdlc_lock_manifest.json` file. It will only release the specific locks listed in that manifest, ensuring zero blast radius (it won't touch other pipelines' locks). The lock release must remain the final step, occurring strictly after the 'WIP Commit & Rename Quarantine' protocol.

## Architecture
-   **Lock Directory**: `.openclaw/workspace/locks/` (Global)
-   **Lock Tracking**: `.sdlc_lock_manifest.json` (Local to the invoking project/orchestrator run)
-   **Acquisition Flow**: T=0 -> Parse PRD Frontmatter -> Lexicographical Sort -> Acquire Locks Iteratively -> Write Manifest (On Success) OR Reverse Rollback (On Failure).
-   **Release Flow**: Orchestrator `--cleanup` -> Read Manifest -> Delete Specific Locks -> Delete Manifest.

## Acceptance Criteria
- [ ] PRDs now require an `Affected_Projects` section in the frontmatter.
- [ ] Orchestrator parses this section and acquires locks before invoking `spawn_planner.py`.
- [ ] Failed lock acquisition actively rolls back any partially acquired locks before failing fast.
- [ ] Orchestrator generates a `.sdlc_lock_manifest.json` tracking its held locks.
- [ ] The `--cleanup` command uses the manifest to safely and accurately release only its own locks.

## Framework Modifications
- `scripts/orchestrator.py`