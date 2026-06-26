status: closed

# PR-001: Pre-flight Parsing & Atomic Lock Acquisition

## 1. Objective
Implement static frontmatter parsing in the Orchestrator to identify affected projects and atomically acquire global file system locks with a rollback mechanism on failure.

## 2. Scope (Functional & Implementation Freedom)
- Build a parser that extracts the `Affected_Projects` list from the PRD frontmatter at the very start of the execution pipeline (T=0).
- Implement an atomic lock acquisition mechanism that lexicographically sorts the required projects and attempts to create file system locks in the global lock directory.
- Implement a fail-fast rollback protocol: if any lock fails to acquire during the batch, all previously acquired locks in that batch must be released before exiting, preventing lock leakage.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. The Orchestrator successfully parses `Affected_Projects` from a PRD document.
2. The Orchestrator acquires locks iteratively for all parsed projects in lexicographical order.
3. If a lock cannot be acquired, the Orchestrator actively rolls back (deletes) any partially acquired locks from that batch and exits.
4. The Coder MUST write or update tests for this specific functional slice. All tests MUST pass (GREEN) before submitting.
