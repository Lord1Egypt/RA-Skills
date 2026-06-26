status: in_progress

# PR-001: Mandatory Ignition Handshake & Execution Pulse

## 1. Objective
Implement a failure-fast ignition handshake to validate the communication channel and add real-time execution pulses (Slack notifications) during the SDLC process.

## 2. Scope & Implementation Details
- Update `orchestrator.py` to perform an initial synchronous blocking check. Attempt to send an "Initial Handshake" message to the configured `--channel` using `openclaw message send`.
- If the command returns a non-zero exit code, `sys.exit(1)` with a clear error message (e.g., expected format `slack:CXXXXXX`).
- Update `notification_formatter.py` to support new events: `sdlc_handshake`, `coder_spawned`, `reviewer_spawned`, `review_rejected`, `pr_merged`.
- Integrate these notifications into `orchestrator.py` at the appropriate lifecycle stages.

## 3. TDD & Acceptance Criteria
- Orchestrator fails to start with a helpful error when given a misconfigured channel.
- Intermediate progress messages (Coder/Reviewer/Merge) are successfully sent and visible.
- Tests verify the new notification events and the blocking ignition behavior.
