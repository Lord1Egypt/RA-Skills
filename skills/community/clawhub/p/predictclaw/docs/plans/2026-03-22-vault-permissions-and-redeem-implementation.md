# Vault Permissions And Redeem Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add structured vault permission/safety output and a preview-first vault share redemption flow so users and OpenClaw can understand signer authority, funding limits, and redeemability without blind broadcasts.

**Architecture:** Extend the current wallet status/deposit surfaces with a shared permission summary object, then add a read-only redeem preview service that interrogates the share token, underlying asset, and ERC4626 limits. Keep redeem execution out of scope for now unless preview proves it is safe.

**Tech Stack:** Python 3.11+, pytest, web3, existing PredictClaw CLI, mandated vault config/runtime helpers.

---

### Task 1: Lock the permission and redeem-preview contract in tests

**Files:**
- Modify: `tests/test_wallet.py`
- Modify: `tests/test_funding.py`
- Modify: `tests/test_cli_router.py`
- Modify: `tests/test_docs_examples.py`

**Step 1: Write failing permission-shape tests**

- Add tests that `wallet status --json` for mandated-vault emits a structured permission object with authority, executor, bootstrap signer, and safety notes.
- Add tests that `wallet deposit --json` includes enough permission/funding-policy context for users/OpenClaw to understand allowed asset and recipient behavior.

**Step 2: Run focused tests to verify RED**

Run: `uv run pytest tests/test_wallet.py tests/test_funding.py -q`

**Step 3: Write failing redeem-preview tests**

- Add tests for a new redeem preview command/output shape.
- Include a redeemable case and a blocked case with a structured `blockingReason`.

**Step 4: Run focused redeem tests to verify RED**

Run: `uv run pytest tests/test_wallet.py tests/test_cli_router.py -q`

### Task 2: Add a shared vault permission summary model

**Files:**
- Modify: `lib/wallet_manager.py`
- Modify: `lib/funding_service.py`
- Test: `tests/test_wallet.py`
- Test: `tests/test_funding.py`

**Step 1: Introduce a stable permission summary object**

- Add a small serializer/model that captures authority, executor, bootstrap signer, underlying asset, share token (if known), and safety notes.

**Step 2: Thread the object into mandated-vault outputs**

- Add it to `wallet status --json`.
- Add it to `wallet deposit --json`.
- If overlay/funding-policy details exist, include allowed asset/recipient/window fields.

**Step 3: Run focused tests to verify GREEN**

Run: `uv run pytest tests/test_wallet.py tests/test_funding.py -q`

### Task 3: Add redeem preview service logic

**Files:**
- Modify: `lib/funding_service.py` or add a sibling helper module under `lib/`
- Test: `tests/test_wallet.py`

**Step 1: Implement read-only share-token inspection**

- Query token name, symbol, decimals, balance, underlying asset, `previewRedeem`, `maxRedeem`, and `maxWithdraw`.
- Convert ERC4626 custom errors into structured preview blockers instead of raw exceptions.

**Step 2: Define preview output**

- Include `redeemableNow`, `blockingReason`, `contractError`, and `recommendedNextAction`.

**Step 3: Run focused tests to verify GREEN**

Run: `uv run pytest tests/test_wallet.py -q`

### Task 4: Add CLI command for redeem preview

**Files:**
- Modify: `scripts/wallet.py`
- Test: `tests/test_cli_router.py`

**Step 1: Add the command shape**

- Add `predictclaw wallet redeem-vault --preview --json`
- Add `--all` support for the preview path

**Step 2: Keep execution out of scope**

- If the user requests confirm, fail cleanly with a message that preview-first support exists and confirm is not yet enabled.

**Step 3: Run CLI tests to verify GREEN**

Run: `uv run pytest tests/test_cli_router.py -q`

### Task 5: Rewrite docs/templates for users and OpenClaw

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `SKILL.md`
- Modify: `template.env`
- Modify: `template.mandated-vault.env`
- Test: `tests/test_docs_examples.py`

**Step 1: Document vault permission boundaries clearly**

- Explain authority / executor / bootstrap signer roles.
- Explain funding-policy constraints and how they bound asset movement.

**Step 2: Document redeem preview semantics**

- Explain that preview reads redeemability first.
- Explain why a vault can hold shares but still be non-redeemable right now.

**Step 3: Run docs tests to verify GREEN**

Run: `uv run pytest tests/test_docs_examples.py -q`

### Task 6: Final verification and release prep

**Files:**
- Modify only if verification reveals small gaps

**Step 1: Run full tests**

Run: `uv run pytest -q`

**Step 2: Run build verification**

Run: `uv build`

**Step 3: Run CLI help/manual checks**

Run:
- `uv run python scripts/predictclaw.py --help`
- `uv run python scripts/predictclaw.py wallet status --help`
- `uv run python scripts/predictclaw.py wallet redeem-vault --help`

**Step 4: Commit in small pieces**

- permission summary
- redeem preview service/CLI
- docs/templates/tests
- version bump and publish
