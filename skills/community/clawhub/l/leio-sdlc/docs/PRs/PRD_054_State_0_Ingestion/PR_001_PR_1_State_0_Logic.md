status: closed

---
status: closed
dependencies: []
---
# PR 1: Implement State 0 Auto-Slicing and --force-replan in Orchestrator

## Description
Implement State 0 in `orchestrator.py` to auto-invoke the Planner when the PR directory is empty, enabling full autonomy.

## Tasks
1. In `scripts/orchestrator.py`, add `--force-replan` boolean flag (`action="store_true"`) to the argparse configuration.
2. Immediately after `job_dir` is calculated and before the main `while True` loop, insert State 0 logic:
   a. Check if `job_dir` exists and contains any `.md` files.
   b. If it contains `.md` files and `--force-replan` is `False`, print `State 0: Existing PRs detected. Resuming queue...` and skip Planner invocation.
   c. If `--force-replan` is `True` and `job_dir` exists, use `shutil.rmtree(job_dir)` to wipe it clean.
   d. Auto-invoke Planner: Print `State 0: Auto-slicing PRD...` and execute `subprocess.run([sys.executable, "scripts/spawn_planner.py", "--prd-file", args.prd_file, "--workdir", workdir], check=True)`.
   e. Validate `job_dir` now contains at least one `.md` file. If count `== 0`, print `[FATAL] Planner failed to generate any PRs.` and call `sys.exit(1)`.
