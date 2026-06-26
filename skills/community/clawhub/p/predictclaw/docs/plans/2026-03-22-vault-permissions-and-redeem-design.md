# Vault Permissions And Redeem Design

## Goal

Make PredictClaw explain vault asset permissions and signer safety boundaries clearly to both humans and OpenClaw, then add a safe preview-first redemption flow for vault share tokens before any real redeem broadcast path is considered.

## Current Problems

- `wallet status` and `wallet deposit` expose addresses and balances, but they do not explain the permission model in a structured way.
- Users cannot easily tell which signer is the authority, which signer executes, which signer bootstraps deployment, or what token/recipient limits apply.
- OpenClaw receives fragmented text instead of stable JSON fields describing those limits and roles.
- The current withdrawal command only supports direct `BNB` / `USDT` wallet withdrawals and explicitly blocks pure `mandated-vault` flows.
- There is no product path for previewing a vault share redemption into the underlying asset, so users hit raw chain/runtime errors when they try to reason about redeemability.

## Observed Redeem Constraint

The requested vault token `0x4a88c1c95d0f59ee87c3286ed23e9dcdf4cf08d7` behaves like an ERC4626-style share token:

- name: `Predict Mainnet USDT Vault`
- symbol: `pmUSDT`
- decimals: `18`
- underlying asset: USDT

However, a static full-share redeem call currently returns `ERC4626ExceededMaxRedeem`, which means the token is not presently redeemable through an unconditional "redeem all now" path. The product should surface this as a structured preview result instead of blindly broadcasting.

## Options Considered

### Option A: Docs-only clarification

Update README/templates/help text without changing JSON/status shape or adding a redeem preview command.

Pros:
- Smallest implementation

Cons:
- OpenClaw still cannot reliably infer permission boundaries or redeemability
- Users still need to manually reason through raw chain errors

### Option B: Add full redeem execution immediately

Add `wallet redeem-vault --confirm` right away.

Pros:
- Fastest path to a possible on-chain action

Cons:
- Unsafe while redeemability is currently blocked
- Risks turning a chain-specific vault rule into a user-facing broadcast failure

### Option C: Structured permissions + redeem preview first (recommended)

Expose permission and safety information in stable JSON fields, then add a preview-only redeem command that reports balances, underlying asset, redeem limits, and blocking reasons. Only after preview proves safe should a future confirm/broadcast path be added.

Pros:
- Safer for real funds
- Clear for users and OpenClaw
- Converts raw contract errors into actionable product state

Cons:
- Requires cross-cutting CLI, service, docs, and test changes

## Recommended Design

Use Option C.

### 1. Structured vault permission model

For `wallet status --json` and `wallet deposit --json`, add a stable object that explains:

- `vaultAuthority`
- `vaultExecutor`
- `bootstrapSigner`
- `underlyingAsset`
- `shareToken` when known
- `permissionModel`
- `fundingPolicy.allowedTokenAddresses`
- `fundingPolicy.allowedRecipients`
- `fundingPolicy.maxAmountPerTx`
- `fundingPolicy.maxAmountPerWindow`
- `fundingPolicy.windowSeconds`
- `safetyNotes`

This object should be explicit enough that OpenClaw can explain what is allowed without reverse-engineering env variables.

### 2. Human-readable CLI summary

Plain-text `wallet status` / `wallet deposit` should summarize:

- who controls the vault
- who can execute funding actions
- what asset is permitted
- which recipients are allowed
- whether limits are configured or effectively unlimited

### 3. Preview-first redeem command

Add a new command family:

- `predictclaw wallet redeem-vault --preview --json`
- `predictclaw wallet redeem-vault --all --preview --json`

The command should inspect a share token and return:

- share token address
- holder address
- token metadata
- underlying asset metadata
- share balance
- `previewRedeem`
- `maxRedeem`
- `maxWithdraw`
- `redeemableNow`
- `blockingReason`
- `contractError`
- `recommendedNextAction`

### 4. No immediate confirm path

Do not add a real `--confirm` redeem path in this iteration unless preview proves there is a consistently safe execution path. The current on-chain state already shows a redeemability block, so the product should diagnose first.

## Files Likely To Change

- `lib/wallet_manager.py`
- `lib/funding_service.py`
- `scripts/wallet.py`
- `README.md`
- `README.zh-CN.md`
- `SKILL.md`
- `template.env`
- `template.mandated-vault.env`
- tests under `tests/test_wallet.py`, `tests/test_funding.py`, `tests/test_cli_router.py`, `tests/test_docs_examples.py`

## Success Criteria

- Users can tell, from the product output alone, which signer and policy constraints protect vault funds.
- OpenClaw receives structured fields instead of raw prose for vault permissions.
- `redeem-vault --preview` explains whether a share token is redeemable right now and why.
- Current blocked redemptions fail as structured preview results, not as blind broadcast attempts.
