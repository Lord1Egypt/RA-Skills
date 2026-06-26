# Vault Auto Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make pure `mandated-vault` onboarding default to preview + confirm + auto-deploy + `.env` backfill, so users no longer need to prefill a deployed vault address or full derivation tuple.

**Architecture:** Keep PredictClaw's MCP bridge as the execution backend, but move the user-facing entry point from manual vault addressing to a product-configured bootstrap flow. The runtime should use a fixed factory default, generate a preview via MCP, require an explicit confirmation step before broadcasting, then persist the resolved vault address and related values back into the local `.env` file.

**Tech Stack:** Python 3.11+, pytest, pydantic config validation, ClawHub/OpenClaw skill CLI, external `erc-mandated-mcp` runtime.

---

### Task 1: Lock the new bootstrap contract in tests

**Files:**
- Modify: `tests/test_config.py`
- Modify: `tests/test_wallet.py`
- Modify: `tests/test_funding.py`
- Modify: `tests/test_docs_examples.py`
- Modify: `tests/test_cli_router.py`

**Step 1: Write the failing config tests**

- Add a test that pure `mandated-vault` can start with only:
  - `PREDICT_WALLET_MODE=mandated-vault`
  - `PREDICT_PRIVATE_KEY`
  - default/fixed factory path
- Add a test that `ERC_MANDATED_FACTORY_ADDRESS` defaults to `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6`
- Add a test that explicit deployed vault and advanced manual derivation still remain supported

**Step 2: Run the focused config test to verify RED**

Run: `uv run pytest tests/test_config.py -q`
Expected: failures because the current validator still expects explicit vault address or manual derivation inputs.

**Step 3: Write the failing wallet/funding tests**

- Add a wallet-status/deposit test that undeployed vaults return a preview object instead of only `manual-only` guidance
- Add a confirm/execute-path test that bootstrap can produce a deployed vault result and backfill-ready payload
- Add CLI/help tests for the new bootstrap command and confirmation flags

**Step 4: Run focused wallet/funding/CLI tests to verify RED**

Run: `uv run pytest tests/test_wallet.py tests/test_funding.py tests/test_cli_router.py -q`
Expected: failures because no preview/confirm/execute path exists yet.

**Step 5: Write the failing docs tests**

- Require docs to remove the default-first `0xYOUR_DEPLOYED_VAULT` onboarding path
- Require docs to explain the fixed factory default and preview-before-broadcast flow

**Step 6: Run docs tests to verify RED**

Run: `uv run pytest tests/test_docs_examples.py -q`
Expected: failures because the docs still describe manual-only bootstrap.

### Task 2: Add fixed factory defaults and split bootstrap modes

**Files:**
- Modify: `lib/config.py`
- Test: `tests/test_config.py`

**Step 1: Implement the fixed factory default**

- Set the default factory address to `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6`
- Keep explicit override support for advanced/manual workflows

**Step 2: Split configuration meaningfully**

- Distinguish:
  - initial bootstrap flow
  - explicit deployed vault flow
  - advanced manual derivation flow
- Allow pure `mandated-vault` to start from signer-driven bootstrap intent rather than failing early on missing vault address

**Step 3: Run focused config tests to verify GREEN**

Run: `uv run pytest tests/test_config.py -q`
Expected: pass

### Task 3: Add preview and execute bootstrap runtime path

**Files:**
- Modify: `lib/wallet_manager.py`
- Modify: `lib/funding_service.py`
- Modify: `lib/mandated_mcp_bridge.py` only if extra result parsing is needed
- Test: `tests/test_wallet.py`
- Test: `tests/test_funding.py`

**Step 1: Implement preview-first behavior**

- Rework the current undeployed-vault path so it returns a preview payload instead of terminal `manual-only`
- Include:
  - fixed factory address
  - predicted vault
  - signer address
  - chain id
  - tx summary / fee-related metadata if available
  - explicit `confirmationRequired: true`

**Step 2: Implement execute path**

- Add a runtime function that calls MCP `vault_bootstrap(... mode="execute")`
- Capture deployed vault address and any result metadata needed for user feedback

**Step 3: Preserve fail-closed behavior**

- Missing MCP
- unhealthy MCP
- insufficient signer prerequisites
- failed bootstrap execution

All should still produce actionable failures without hidden side effects.

**Step 4: Run wallet/funding tests to verify GREEN**

Run: `uv run pytest tests/test_wallet.py tests/test_funding.py -q`
Expected: pass

### Task 4: Add a user-facing bootstrap command with confirmation

**Files:**
- Modify: `scripts/predictclaw.py`
- Modify: `scripts/wallet.py` or add a dedicated bootstrap script if that fits the current command structure better
- Test: `tests/test_cli_router.py`

**Step 1: Add a preview command**

- Add a clear user-facing command such as:
  - `predictclaw wallet bootstrap-vault --json`
  - or equivalent under the existing command layout

The preview command must not broadcast.

**Step 2: Add a confirm/execute command**

- Add an explicit execution form such as:
  - `predictclaw wallet bootstrap-vault --confirm --json`

This step should be the only point where deployment is broadcast.

**Step 3: Emit backfill-ready results**

- Return deployed vault address
- Return fixed factory and chain values
- Return enough information for `.env` persistence and UX messaging

**Step 4: Run CLI tests to verify GREEN**

Run: `uv run pytest tests/test_cli_router.py -q`
Expected: pass

### Task 5: Add `.env` backfill after successful deployment

**Files:**
- Create or modify: a helper near `lib/` or `scripts/` that updates `.env`
- Modify: CLI execution path from Task 4
- Test: new or existing test file covering `.env` writes

**Step 1: Write the failing backfill test**

- Start from a bootstrap-style `.env`
- Simulate successful bootstrap execute result
- Assert `.env` gains:
  - `ERC_MANDATED_VAULT_ADDRESS=<actual deployed vault>`
  - `ERC_MANDATED_FACTORY_ADDRESS=0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6`
  - `ERC_MANDATED_CHAIN_ID=<resolved chain>`
  - existing `ERC_MANDATED_MCP_COMMAND` remains or is preserved

**Step 2: Run the test to verify RED**

**Step 3: Implement minimal backfill logic**

- Update or append env values deterministically
- Do not overwrite unrelated user secrets

**Step 4: Run the test to verify GREEN**

### Task 6: Rewrite user-facing docs and templates

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `SKILL.md`
- Modify: `template.mandated-vault.env`
- Modify: `.env.mandated-vault.example`
- Test: `tests/test_docs_examples.py`
- Test: `tests/test_scaffold.py`

**Step 1: Remove the old default-first guidance**

- Stop telling default users to start with `ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT`
- Stop telling default users to fill the whole derivation tuple first

**Step 2: Document the new default flow**

- signer private key
- deployment fee funding
- fixed factory handled by product
- preview before broadcast
- explicit confirmation for deployment
- auto-backfill after success

**Step 3: Keep advanced/manual escape hatches**

- explicit vault address remains documented as advanced/manual mode
- manual derivation tuple remains documented as recovery/advanced mode

**Step 4: Run docs/scaffold tests to verify GREEN**

Run: `uv run pytest tests/test_docs_examples.py tests/test_scaffold.py -q`
Expected: pass

### Task 7: Final verification and release prep

**Files:**
- Modify only if verification reveals small gaps

**Step 1: Run the broader regression suite**

Run: `uv run pytest -q`
Expected: all pass

**Step 2: Run build verification**

Run: `uv build`
Expected: `dist/predictclaw-<version>.tar.gz` and wheel build cleanly

**Step 3: Run CLI/manual checks**

Run:
- `uv run python scripts/predictclaw.py --help`
- `uv run python scripts/predictclaw.py wallet bootstrap-vault --help` (or the final chosen command)

**Step 4: Commit in small pieces**

- config/bootstrap defaults
- runtime preview/execute/backfill
- docs/templates
- tests
- version bump if release is needed
