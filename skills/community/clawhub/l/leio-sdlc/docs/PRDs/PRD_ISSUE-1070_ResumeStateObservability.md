# PRD for ISSUE-1070: Resume State Observability and TTL Telemetry

## 1. Problem Statement
During a hard crash (e.g., OS `SIGKILL`), a PR might be left in `status: in_progress`. When the Orchestrator restarts, it occasionally bypasses the in-progress PR. Because debug logs were only output to `stdout`, the exact failure reason vanished upon crash. We need durable, distinct logs for every run that survive crashes, with an automatic TTL to prevent disk bloat, utilizing standard Python logging rather than manual/low-level I/O hacks.

## 2. Requirements

### 2.1 Standard Python `logging` Infrastructure
- **Logger Setup**: In `scripts/orchestrator.py`, replace the custom `dlog()` implementation and ad-hoc `print()` statements for debugging with the standard Python `logging` module.
- **Global Logger**: Configure a global logger (e.g., `logger = logging.getLogger("sdlc_orchestrator")`) with two distinct handlers:
  1. **File Handler (Persistent & Detailed)**:
     - Output to `.tmp/sdlc_logs/orchestrator_<YYYYMMDD_HHMMSS>_<pid>.log`. Ensure `.tmp/sdlc_logs` is created safely using the resolved `--workdir`, not blindly at script start.
     - To handle SIGKILL survival, configure the file handler to flush immediately (e.g., use a simple custom handler overriding `emit` to call `self.flush()`). Do not manually sprinkle `os.fsync()` throughout the codebase.
     - This file handler must ALWAYS capture `DEBUG` level logs, regardless of CLI flags.
  2. **Console Handler (User-Facing)**:
     - Output to `sys.stdout`.
     - Its log level must be tied to the `--debug` flag (or `SDLC_DEBUG_MODE=1`). If enabled, set to `DEBUG`; if disabled, set to `INFO`.

### 2.2 TTL Mechanism
- **Automated Cleanup**: Implement a simple, safe cleanup function at logger initialization utilizing standard `pathlib/os` stat times to safely clear files older than 7 days in `.tmp/sdlc_logs/`.
- Ensure this handles exceptions gracefully (e.g., permission errors, directory missing) so it doesn't crash the orchestrator.

### 2.3 Wrap Subprocess Output
- **Integration with Subprocesses**: Update `drun()` and `dpopen()` in `orchestrator.py` to route their internal diagnostic `print` outputs into `logger.debug()` or `logger.info()` so they are captured by the persistent file handler.

### 2.4 Targeted State 0/1 Telemetry
- **Granular PR Scanning Logs**: Inject granular `logger.debug()` calls into the PR scanning block (`for md_file in md_files:`) in `scripts/orchestrator.py`.
- **Data to Log**:
  - The exact `job_dir` being scanned.
  - The list of `md_files` found.
  - For each file, log its name, the first 50 characters read (or the exact `status:` line), and the boolean result of the `re.search(r'^status:\s*in_progress'...)` regex.
  - Log if the native loop fails and `get_next_pr.py` is invoked, including its output and exit code.

## 3. Boundaries and Technical Constraints
- **State Machine Integrity**: Do not modify the core state machine logic or transitions. Only wrap the existing PR ingestion loop with telemetry and logging logic.
- **Path Resolution**: Ensure all file paths and logs are relative to the `--workdir`, NOT the random CWD at script launch. Avoid cross-environment issues.
- **Exception Handling**: Log cleanup and I/O operations must be wrapped in `try/except` blocks to prevent logging failures from aborting the pipeline execution.

## 4. Expected Outcomes
- Robust, post-mortem debug logs for every orchestrator run inside `.tmp/sdlc_logs/`.
- Clear visibility into why an `in_progress` PR is skipped after a crash.
- No disk bloat due to the automated 7-day TTL cleanup.