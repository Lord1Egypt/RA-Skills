# PredictClaw Order Session Continuation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Repair PredictClaw's overlay workflow by reconciling local tracked positions with remote truth, binding funding sessions to trade identity, and exposing a public CLI continuation surface for funding/follow-up session execution.

**Architecture:** Persist trade-bound overlay session records in local storage when overlay buys stop at `funding-required`, use those records to enrich wallet status/deposit output and drive continuation commands, and reconcile tracked positions against both remote positions and remote order truth. Preserve explicit wallet mode semantics and do not auto-broadcast chain actions.

**Tech Stack:** Python 3.11+, pytest, existing PredictClaw CLI, local JSON storage, MandatedVault MCP bridge, Predict API client.

---

### Task 1: Add failing tests for position/order reconciliation

**Files:**
- Modify: `tests/test_positions.py`
- Modify: `tests/test_storage.py`

**Step 1: Write a failing merge test**

- Seed a tracked local position with `status=OPEN` and `order_hash`.
- Stub remote positions as empty.
- Stub remote order lookup to return `CANCELLED`.
- Assert the merged view is no longer `OPEN` and the local storage status is updated.

**Step 2: Run the test to verify RED**

Run: `uv run pytest tests/test_positions.py tests/test_storage.py -q`

### Task 2: Implement local position reconciliation

**Files:**
- Modify: `lib/positions_service.py`
- Modify: `lib/position_storage.py`
- Modify: `lib/models.py` if order data shape needs expansion
- Test: `tests/test_positions.py`
- Test: `tests/test_storage.py`

**Step 1: Add order-truth lookup path**

- Add a small helper in `PositionsService` to look up remote order status by `order_hash`.
- Use it only when there is no matching remote position.

**Step 2: Add local storage update support**

- Add a targeted storage update method or reuse `upsert` so resolved status can be written back to `positions.json`.

**Step 3: Apply merge priority**

- Use `remote position truth > remote order truth > local tracked fallback`.

**Step 4: Re-run focused tests to verify GREEN**

Run: `uv run pytest tests/test_positions.py tests/test_storage.py -q`

### Task 3: Add failing tests for trade-bound overlay session persistence

**Files:**
- Modify: `tests/test_trade.py`
- Create or modify: `tests/test_session_storage.py`

**Step 1: Write a failing overlay buy test**

- For insufficient overlay balance, assert PredictClaw persists a trade-bound session record with:
  - `positionId`
  - `marketId`
  - `outcome`
  - `orderHash` (nullable)
  - `sessionId`

**Step 2: Run tests to verify RED**

Run: `uv run pytest tests/test_trade.py tests/test_session_storage.py -q`

### Task 4: Implement session storage and identity binding

**Files:**
- Create: `lib/session_storage.py`
- Modify: `lib/trade_service.py`
- Modify: `lib/wallet_manager.py`
- Modify: `lib/funding_service.py`
- Test: `tests/test_trade.py`
- Test: `tests/test_session_storage.py`
- Test: `tests/test_wallet.py`
- Test: `tests/test_funding.py`

**Step 1: Add local session storage**

- Create a JSON-backed storage helper for active fund-and-action sessions.
- Persist session metadata separately from MCP session payloads.

**Step 2: Bind trade identity at creation time**

- When overlay buy stops at `funding-required`, create a deterministic `positionId` and persist `marketId`, `outcome`, and nullable `orderHash` with the session record.
- Do not mutate MCP session schemas with extra fields; keep trade binding alongside the session wrapper record.

**Step 3: Enrich wallet status/deposit output**

- If an active stored session exists for the current Predict Account overlay, expose `linkedPositionId`, `linkedMarketId`, `linkedOrderHash`, and `sessionScope` in wallet output.

**Step 4: Re-run focused tests to verify GREEN**

Run: `uv run pytest tests/test_trade.py tests/test_session_storage.py tests/test_wallet.py tests/test_funding.py -q`

### Task 5: Add failing tests for public continuation CLI

**Files:**
- Modify: `tests/test_cli_router.py`
- Modify: `tests/integration/test_cli_flows.py`
- Modify: `tests/integration/test_openclaw_host_contract.py`

**Step 1: Write a failing `continue-funding` test**

- Seed an active stored session.
- Use a fake MCP server that supports:
  - `vault_asset_transfer_result_create`
  - `agent_fund_and_action_session_apply_event`
  - `agent_fund_and_action_session_next_step`
- Assert the command applies `fundingConfirmed`, updates the stored session, and returns the next step.

**Step 2: Write a failing `continue-follow-up` test**

- Seed a pending-follow-up session and a next-step that includes a follow-up action plan.
- Assert the command creates a follow-up result, applies `followUpResultReceived`, and returns the updated session.

**Step 3: Run tests to verify RED**

Run: `uv run pytest tests/test_cli_router.py tests/integration/test_cli_flows.py tests/integration/test_openclaw_host_contract.py -q`

### Task 6: Implement public wallet continuation commands

**Files:**
- Modify: `scripts/wallet.py`
- Modify: `lib/funding_service.py`
- Modify: `lib/wallet_manager.py` only if shared helpers belong there
- Modify: `lib/mandated_mcp_bridge.py` only if helper wrappers are needed
- Test: `tests/test_cli_router.py`
- Test: `tests/integration/test_cli_flows.py`
- Test: `tests/integration/test_openclaw_host_contract.py`

**Step 1: Add parser surface**

- Add public wallet subcommands for continuation, for example:
  - `wallet continue-funding`
  - `wallet continue-follow-up`

**Step 2: Implement funding confirmation flow**

- Load the active stored session.
- Build `assetTransferResult` from the next-step funding plan and CLI inputs such as `--tx-hash`.
- Apply `fundingConfirmed` and store the updated session.

**Step 3: Implement follow-up result flow**

- Load the active stored session.
- Use `create_agent_follow_up_action_result` with the stored follow-up plan.
- Apply `followUpResultReceived` and store the updated session.

**Step 4: Re-run focused tests to verify GREEN**

Run: `uv run pytest tests/test_cli_router.py tests/integration/test_cli_flows.py tests/integration/test_openclaw_host_contract.py -q`

### Task 7: Final verification

**Files:**
- Modify only if verification reveals gaps

**Step 1: Run targeted regression suite**

Run: `uv run pytest tests/test_positions.py tests/test_storage.py tests/test_trade.py tests/test_wallet.py tests/test_funding.py tests/test_cli_router.py tests/integration/test_cli_flows.py tests/integration/test_openclaw_host_contract.py -q`

**Step 2: Run full suite**

Run: `uv run pytest -q`

**Step 3: Run CLI smoke checks**

Run:
- `uv run python scripts/predictclaw.py wallet --help`
- `uv run python scripts/wallet.py continue-funding --help`
- `uv run python scripts/wallet.py continue-follow-up --help`

**Step 4: Keep changes grouped by concern**

- position reconciliation
- session storage and binding
- public continuation CLI
