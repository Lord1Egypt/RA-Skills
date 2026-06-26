# PRD: SDLC Observability, Ignition Guardrail & Review Protocol Migration (PRD-033)

## Context
The `leio-sdlc` system currently lacks visibility during long Coder/Reviewer loops and allows execution with invalid communication channels. Furthermore, the system is stuck in a "protocol gap" where some components (Reviewer) use JSON while others (`merge_code.py`) still legacy-check for `[LGTM]` strings, leading to merge failures or incorrect "fixes" by agents. This PRD addresses **ISSUE-1036** and finalizes the transition to a structured JSON-based review protocol.

## Requirements

### 1. Mandatory Ignition Handshake (Failure-Fast)
- **First Action**: Before any slicing or state transitions, the Orchestrator MUST attempt to send an "Initial Handshake" message to the configured `--channel`.
- **Validation**: If the `openclaw message send` command returns a non-zero exit code, the Orchestrator MUST immediately `sys.exit(1)`.
- **Actionable Error**: Print a clear error message stating that the channel parameter is invalid and providing the expected format (e.g., `slack:CXXXXXX`).

### 2. Intermediate Execution Pulse (Respiratory Feedback)
- Send real-time Slack notifications for:
    - **Coder Spawned**: "Calling Coder for [PR_ID]..."
    - **Reviewer Spawned**: "Coder submitted changes. Reviewer is now auditing..."
    - **Review Rejected**: "❌ Reviewer rejected changes. Reason: [Summary]. Retrying..."
    - **PR Merged**: "✅ [PR_ID] successfully merged to master."

### 3. Review Protocol Migration (JSON Enforcement)
- **Deprecate `[LGTM]`**: Completely remove any logic that relies on searching for the `[LGTM]` string in review reports.
- **Native JSON Check**: Update `scripts/merge_code.py` to natively parse the JSON output from the Reviewer and check for `"status": "APPROVED"`.
- **Universal Clean-up**: Identify and update any other scripts or templates that still mention or rely on the legacy `[LGTM]` protocol.
- **Test Alignment**: Update all preflight and integration tests (including `scripts/test_preflight_guardrails.sh`) to use JSON-formatted mock review reports.

## Architecture
- **Process Guard**: Synchronous blocking check at the start of `orchestrator.py`.
- **Event Mapping**: Update `notification_formatter.py` with `sdlc_handshake`, `coder_spawned`, `reviewer_spawned`, `review_rejected`, `pr_merged`.
- **Protocol Refactor**: Logic in `merge_code.py` must use `json.loads()`.

## Framework Modifications
The Coder is explicitly authorized to modify:
- `scripts/orchestrator.py`
- `scripts/notification_formatter.py`
- `scripts/merge_code.py`
- `scripts/test_preflight_guardrails.sh` (and any other relevant test scripts)

## Acceptance Criteria
- [ ] Orchestrator fails to start with helpful error on misconfigured channel.
- [ ] Intermediate progress (Coder/Reviewer/Merge) is visible in real-time in Slack.
- [ ] `merge_code.py` successfully merges PRs based on JSON `"status": "APPROVED"` without any `[LGTM]` string present.
- [ ] ALL preflight tests pass using the new JSON review protocol.
