# Mandated MCP Install UX Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add an explicit-but-low-friction mandated-vault setup flow that can detect, optionally install, and auto-backfill `ERC_MANDATED_MCP_COMMAND` without silently installing prerequisites or guessing vault credentials.

**Architecture:** The install UX belongs primarily in the OpenClaw host, because mode selection, installer execution, and config persistence happen there. `predictfunclaw` remains the runtime contract: it documents the behavior, keeps the launcher env var stable, and fails closed when the MCP command is unavailable or unhealthy.

**Tech Stack:** OpenClaw host installer/config flow, PredictClaw docs and tests, external `erc-mandated-mcp` runtime.

---

### Task 1: Add host-side mandated MCP preflight hook

**Files:**
- Modify: `<openclaw-host>/mode-selection flow`
- Modify: `<openclaw-host>/skill installer flow`
- Test: `<openclaw-host>/tests` covering mode selection and dependency detection

**Step 1: Write the failing host test**

- Selecting `mandated-vault` should trigger MCP detection.
- Selecting `read-only`, `eoa`, or plain `predict-account` should not.

**Step 2: Run host test to verify RED**

Run the host test command for the mode-selection suite.
Expected: failure because no mandated MCP preflight exists yet.

**Step 3: Add minimal implementation**

- On vault-mode selection, look for:
  - existing `ERC_MANDATED_MCP_COMMAND`
  - fallback launcher `erc-mandated-mcp`
- If neither is usable, surface the install prompt.

**Step 4: Re-run host test to verify GREEN**

### Task 2: Add one-click MCP install with explicit boundary

**Files:**
- Modify: `<openclaw-host>/installer integration`
- Modify: `<openclaw-host>/user prompt copy`
- Test: `<openclaw-host>/tests` for install success and missing-prerequisite failure

**Step 1: Write failing install tests**

- Successful install should auto-backfill `ERC_MANDATED_MCP_COMMAND`.
- Missing prerequisite should fail with explicit guidance and no silent secondary installs.

**Step 2: Run host tests to verify RED**

Expected: failures because install/backfill behavior does not exist yet.

**Step 3: Implement minimal install flow**

- Offer "Install now" only after explicit user selection of vault mode.
- Install only `erc-mandated-mcp`.
- Do not auto-install Node, npm, uvx, or other prerequisites.
- If install succeeds, re-run launcher detection and persist the resolved command.

**Step 4: Re-run host tests to verify GREEN**

### Task 3: Keep PredictClaw docs aligned with the host UX

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `SKILL.md`
- Test: `tests/test_docs_examples.py`

**Step 1: Write the failing docs test**

- Require docs to say vault mode can trigger MCP detection/install.
- Require docs to say PredictClaw integrates the bridge, not the bundled runtime.

**Step 2: Run `uv run pytest tests/test_docs_examples.py` to verify RED**

**Step 3: Update docs minimally**

- Add one paragraph in README/SKILL explaining the host-assisted install path.
- Keep the explicit boundary: vault credentials are still user-confirmed.

**Step 4: Run `uv run pytest tests/test_docs_examples.py` to verify GREEN**

### Task 4: Preserve runtime contract and fail-closed behavior

**Files:**
- Modify: `lib/config.py` only if the launcher contract needs clarification
- Modify: `lib/mandated_mcp_bridge.py` only if diagnostics need improvement
- Test: `tests/test_mandated_mcp_bridge.py`

**Step 1: Write failing regression tests if behavior changes**

- Missing command should still fail closed.
- Unhealthy MCP should still fail closed with actionable diagnostics.

**Step 2: Run `uv run pytest tests/test_mandated_mcp_bridge.py` to verify RED if any behavior is changed**

**Step 3: Make the smallest runtime adjustment needed**

- Prefer copy/diagnostics changes over contract changes.
- Keep `ERC_MANDATED_MCP_COMMAND` as the public launcher contract.

**Step 4: Re-run `uv run pytest tests/test_mandated_mcp_bridge.py` to verify GREEN**

### Task 5: Final verification and integration

**Files:**
- No new files beyond changes above

**Step 1: Run standalone repo verification**

Run: `uv run pytest tests/test_docs_examples.py tests/test_mandated_mcp_bridge.py -q`

**Step 2: Run host-side verification**

- Run the host mode-selection / installer tests.
- Manually verify:
  - select `mandated-vault`
  - see explicit dependency copy
  - install `erc-mandated-mcp`
  - observe `ERC_MANDATED_MCP_COMMAND` auto-filled
  - continue into vault config without auto-filling credentials

**Step 3: Commit in small pieces**

- host preflight/install flow
- docs updates
- runtime/diagnostic changes if any
