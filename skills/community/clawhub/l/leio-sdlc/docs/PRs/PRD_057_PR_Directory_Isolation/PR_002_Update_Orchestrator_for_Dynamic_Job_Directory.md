status: closed

---
status: closed
dependencies: []
---
# PR 2: Update Orchestrator for Dynamic Job Directory

## Description
Modify `scripts/orchestrator.py` to enforce strict physical isolation for PR queues.

## Requirements
- Override or set the `job_dir` variable by dynamically computing it from the required `--prd-file` argument.
- The Orchestrator's internal polling loop (State 1) and any calls to `get_next_pr.py` must strictly point to this isolated subdirectory.
- Gracefully handle the missing directory (treat as empty queue, do not crash with FileNotFoundError, exit 0).
