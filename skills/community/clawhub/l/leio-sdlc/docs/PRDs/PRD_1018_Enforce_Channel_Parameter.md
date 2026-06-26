Status: Closed

status: open

# PRD-1018: Enforce Channel Parameter and Fail-Fast on Missing Notification Target

## 1. Problem Statement
The `leio-sdlc` orchestrator's notification system (`notify_channel`) silently drops Slack notifications if the `channel` is not provided via environment variables (`OPENCLAW_SESSION_KEY` or `OPENCLAW_CHANNEL_ID`). This violates the Fail-Fast principle and the strict Orchestrator Self-Explanation rules defined in PRD-1010, resulting in the manager being unaware of the pipeline completion.

## 2. Solution & Scope
- **Target Project:** `/root/.openclaw/workspace/projects/leio-sdlc`
- **Scope:** Modify `scripts/orchestrator.py` and any associated test scripts.
- **Implementation Details:**
  1. Add `--channel` as an explicit argument to `argparse.ArgumentParser` in `orchestrator.py`. Make it optional in `argparse` to allow fallback to environment variables, BUT explicitly validate its presence immediately after parsing.
  2. The validation logic must be: `effective_channel = args.channel or os.environ.get("OPENCLAW_SESSION_KEY") or os.environ.get("OPENCLAW_CHANNEL_ID")`.
  3. If `effective_channel` is empty/None, the orchestrator MUST immediately abort execution and print a self-explaining error using `HandoffPrompter` (e.g., `[FATAL_STARTUP]` / `[ACTION REQUIRED FOR MANAGER] Missing channel parameter.`).
  4. Update `notify_channel` function to accept this `effective_channel` explicitly rather than reading environment variables implicitly inside the function.
  5. **Crucial:** Update ALL existing `.sh` test scripts in `scripts/` that call `orchestrator.py` to pass a dummy `--channel "#test"` so they don't break.

## 3. Autonomous Test Strategy
- **Testing Approach:** Shell script unit testing.
- **Validation Script:** Create `scripts/test_missing_channel.sh` to explicitly run `orchestrator.py` WITHOUT the `--channel` parameter and WITHOUT the `OPENCLAW_` environment variables. 
- **Assertion:** The test MUST verify that the orchestrator exits with a non-zero exit code and outputs the `[FATAL_STARTUP]` handoff string indicating the missing channel.

## 4. TDD Guardrail
The implementation and its failing test (`scripts/test_missing_channel.sh`) MUST be delivered in the same PR contract.
