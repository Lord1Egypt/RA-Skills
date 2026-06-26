# Architectural Audit Report v6: Hub & Spoke Polyrepo (PRD-1022 v3)

**STATUS: REJECTED / CRITICAL FAILURES DETECTED**
**AUDITOR:** Senior Architecture Auditor
**DATE:** 2026-03-25

## 1. Executive Summary
An autonomous, deep-dive inspection of PRD-1022 v3 and the current SDLC Orchestrator source code (`orchestrator.py`, `spawn_planner.py`, `spawn_coder.py`) reveals a catastrophic gap between design and implementation. The much-touted "OS-Safe Prompt Injection" to resolve `E2BIG` (Argument list too long) vulnerabilities **has not been implemented**. Furthermore, the architectural design proposed in the PRD for the `/tmp/` injection contains severe concurrent execution and security flaws. 

The system is currently **NOT READY** for the Polyrepo migration.

---

## 2. Devastating Findings & Discrepancies

### FINDING 1: Implementation Illusion (The E2BIG Fix is Missing)
**Severity:** CRITICAL
The PRD mandates writing the fully assembled prompt text into an ephemeral `/tmp` file to avoid Linux `MAX_ARG_STRLEN` limits when invoking the `openclaw agent -m` command. 
**Reality:** The source code completely ignores this.
- In `spawn_coder.py`: `openclaw_agent_call` still passes the massive `task_string` directly via the `--message` (`-m`) argument.
- In `spawn_planner.py`: `subprocess.run(["openclaw", "agent", "--session-id", session_id, "-m", task_string])` does the same.
**Impact:** As soon as Playbooks + PRDs + PR Contracts scale up, the OS will violently reject the subprocess call with `[Errno 7] Argument list too long`. The pipeline will crash hard.

### FINDING 2: Cross-Talk & Clashing in /tmp/ (Flawed PRD Design)
**Severity:** CRITICAL
**Flaw in PRD-1022 v3:** The PRD proposes naming the file `/tmp/sdlc_task_<pr_id>.txt`. 
In a Polyrepo environment, you have multiple isolated repositories (e.g., `projects/AMS` and `projects/ClawOS`). If two concurrent orchestrators happen to be processing `PR_001.md` in their respective repos, they will both attempt to read/write `/tmp/sdlc_task_PR_001.txt` simultaneously.
**Impact:**
1. **Data Corruption (Cross-talk):** The AMS Coder agent reads the ClawOS prompt, hallucinates, and destroys the workspace.
2. **Permission Denied (EACCES):** If orchestrators run under different user identities (or cron jobs), User A creates the file with 644 permissions, and User B fails to overwrite it, crashing the pipeline.
3. **Symlink Clobbering (CWE-377):** A predictable `/tmp` path allows a malicious local user to pre-create the file as a symlink to `/etc/shadow` or a critical project file, tricking the orchestrator into overwriting it.

### FINDING 3: The Zombie File Apocalypse
**Severity:** HIGH
The PRD states: "The openclaw agent -m command should only receive a short pointer instruction... Do not modify this file."
**Flaw:** The PRD completely forgets to specify the **teardown phase**. There is no instruction to delete the temporary file after the `openclaw` subprocess exits. 
**Impact:** Every single agent spawn will leak a file containing thousands of tokens into `/tmp/`. Over a few weeks of automated CI/CD, the `/tmp` partition will exhaust its inodes or disk space, causing a system-wide ungraceful degradation.

### FINDING 4: Global Directory Propagation Incomplete
**Severity:** MEDIUM
The PRD demands that `orchestrator.py` accept a `--global-dir` argument or dynamically resolve it and "pass this down to all spawner scripts." 
**Reality:** `orchestrator.py` correctly resolves `RUNTIME_DIR`, but it does *not* pass `--global-dir` to the spawners. The spawners are doing their own independent `os.path.dirname(__file__)` resolution. While functionally identical right now, it breaks the strict top-down propagation contract defined in the PRD, making the spawners fragile if executed from symlinks or moved.

---

## 3. Mandatory Remediation Directives

Before approving PRD-1022 v4 or merging any code, the following changes MUST be enforced:

1. **Actually Implement the Fix:** Stop passing `task_string` to `-m`.
2. **Use Secure Tempfiles:** Reject predictable `/tmp` filenames. Python's `tempfile.NamedTemporaryFile(delete=False)` or `tempfile.mkstemp()` MUST be used to guarantee unique, collision-proof, atomic file creation (e.g., `/tmp/sdlc_prompt_a98b4f2x.txt`).
3. **Enforce Cleanup via `try/finally`:** The python spawner scripts must wrap the `subprocess.run` call in a `try...finally` block to execute `os.unlink()` on the temporary prompt file, guaranteeing no zombie files are left behind even if the process times out or crashes.
4. **Restrict Permissions:** Ensure the temporary file is created with `0o600` permissions so other users cannot read proprietary PRDs.

**FINAL VERDICT:** The orchestrator is heavily out of sync with the mitigation plan, and the mitigation plan itself introduces a critical concurrency hazard in `/tmp`. Stop the Polyrepo split immediately until these fixes are coded and tested.