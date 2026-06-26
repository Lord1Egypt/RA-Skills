# PredictClaw Route Conflict Diagnostics Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Keep `PREDICT_WALLET_MODE` authoritative while making route conflicts and active route semantics explicit in PredictClaw wallet errors, JSON output, and plain-text guidance.

**Architecture:** Introduce a dedicated route-conflict config error, thread structured diagnostics through `scripts/wallet.py`, and enrich valid status/deposit payloads with explicit route metadata. Preserve the current pure `mandated-vault` vs `predict-account + ERC_MANDATED_*` execution split.

**Tech Stack:** Python 3.11+, pytest, existing PredictClaw CLI, current config/wallet/funding services.

---

### Task 1: Lock the conflict contract in tests

**Files:**
- Modify: `tests/test_config.py`
- Modify: `tests/test_cli_router.py`

**Step 1: Write the failing config test**

- Add a test that `PREDICT_WALLET_MODE=mandated-vault` plus valid Predict Account credentials raises a route-aware config error.
- Assert the error text mentions the active route, the recommended mode, and the next step.

**Step 2: Run the config test to verify RED**

Run: `uv run pytest tests/test_config.py -q`

**Step 3: Write the failing CLI JSON/text tests**

- Add `wallet status --json` and `wallet deposit --json` tests for the same conflict configuration.
- Assert the JSON error payload includes route guidance fields.
- Add a plain-text assertion that the output tells the user to switch to `PREDICT_WALLET_MODE=predict-account` for Predict Account funding.

**Step 4: Run the CLI tests to verify RED**

Run: `uv run pytest tests/test_cli_router.py -q`

### Task 2: Add a dedicated route-conflict error type

**Files:**
- Modify: `lib/config.py`
- Test: `tests/test_config.py`

**Step 1: Introduce a route-aware config error**

- Add a small error subclass or structured payload helper for route-conflict diagnostics.
- Include fields for active mode/route, recommended mode/route, detected capabilities, and next step.

**Step 2: Use it in mandated-vault + Predict Account conflicts**

- Replace the generic `does not allow Predict Account credentials` path with the route-aware error for this exact mixed configuration.

**Step 3: Run focused tests to verify GREEN**

Run: `uv run pytest tests/test_config.py -q`

### Task 3: Surface structured wallet command errors

**Files:**
- Modify: `scripts/wallet.py`
- Test: `tests/test_cli_router.py`

**Step 1: Add a shared wallet error emitter**

- In JSON mode, emit a stable object with `success=false`, error class, message, and any route guidance fields from the config error.
- In text mode, print the message and the route guidance lines in a readable order.

**Step 2: Wire the emitter into wallet handlers**

- Apply it to `status`, `deposit`, `bootstrap-vault`, and other wallet handlers that already catch `ConfigError`.

**Step 3: Run focused CLI tests to verify GREEN**

Run: `uv run pytest tests/test_cli_router.py -q`

### Task 4: Add explicit active-route metadata to successful status output

**Files:**
- Modify: `lib/wallet_manager.py`
- Test: `tests/test_wallet.py`

**Step 1: Extend status payloads**

- Add explicit route fields for pure mandated-vault snapshots such as `activeRoute` and `routePurpose`.
- Add matching route metadata for overlay snapshots without changing existing `fundingRoute` semantics.

**Step 2: Update plain-text status rendering**

- Show the route intent clearly for pure `mandated-vault` and overlay outputs.

**Step 3: Run focused wallet tests to verify GREEN**

Run: `uv run pytest tests/test_wallet.py -q`

### Task 5: Add explicit active-route metadata to successful deposit output

**Files:**
- Modify: `lib/funding_service.py`
- Modify: `scripts/wallet.py`
- Test: `tests/test_funding.py`
- Test: `tests/test_cli_router.py`

**Step 1: Extend deposit payloads**

- Add route metadata for pure `mandated-vault` deposit details.
- Preserve existing overlay deposit fields while adding the same route-purpose vocabulary.

**Step 2: Update plain-text deposit rendering**

- Add a line for pure `mandated-vault` clarifying that the current route funds the vault itself, not the Predict Account.

**Step 3: Run focused tests to verify GREEN**

Run: `uv run pytest tests/test_funding.py tests/test_cli_router.py -q`

### Task 6: Final verification

**Files:**
- Modify only if verification reveals small gaps

**Step 1: Run targeted regression suite**

Run: `uv run pytest tests/test_config.py tests/test_cli_router.py tests/test_wallet.py tests/test_funding.py -q`

**Step 2: Run full tests**

Run: `uv run pytest -q`

**Step 3: Run CLI checks**

Run:
- `uv run python scripts/predictclaw.py --help`
- `uv run python scripts/wallet.py status --help`
- `uv run python scripts/wallet.py deposit --help`

**Step 4: Commit in small pieces**

- route-conflict error contract
- wallet CLI error/output plumbing
- status/deposit route metadata
