# Vault Auto Bootstrap Design

## Goal

Replace the current pure `mandated-vault` onboarding flow that requires users to supply an explicit deployed vault address or full derivation tuple. The new default path should let users provide only an EOA signer plus deployment-fee funding and selected amount controls, then preview, confirm, auto-deploy, and backfill the user vault configuration.

## Current Mismatch

The current repo still assumes manual vault addressing:

- `template.mandated-vault.env` starts with `ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT`
- `README.md` and `SKILL.md` document either an explicit vault address or a full derivation tuple
- `lib/funding_service.py` returns `createVaultPreparation` with `broadcast: manual-only`
- `lib/wallet_manager.py::resolve_mandated_vault()` calls `vault_bootstrap(... mode="plan")` and never promotes that plan into an execute-and-backfill path

That is inconsistent with the desired user story: users should not need to know their future vault address or fill derivation fields if the protocol factory is fixed and the product intends to deploy the vault on their behalf.

## Assumptions

- The current supported protocol factory is fixed to `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6`
- The intended bootstrap signer is an EOA private key that can pay deployment gas / fees
- The host should continue to fail closed if deployment prerequisites or MCP health checks are not satisfied
- Sensitive signing/broadcasting still requires explicit user confirmation before the chain-side deployment action happens

## Options Considered

### Option A: Keep manual-only bootstrap

Users must continue to provide a deployed vault address or the full derivation tuple.

Pros:
- Minimal implementation changes
- Preserves current control-plane model

Cons:
- Conflicts with the intended user experience
- Causes the exact hard block the user reported
- Keeps docs and OpenClaw assistance overly expert-oriented

### Option B: Auto-deploy immediately inside `wallet deposit`

When the system detects an undeployed vault, `wallet deposit` automatically broadcasts deployment and writes the resolved vault address.

Pros:
- Lowest friction once users choose vault mode

Cons:
- `wallet deposit` stops being an informational command and gains a hidden side effect
- Harder to explain and harder to trust in a safety-sensitive control-plane flow
- Makes preview/review of factory, chain, signer, and fee assumptions less explicit

### Option C: Preview -> explicit confirm -> auto-deploy -> backfill (recommended)

`wallet deposit` and/or setup flow first surfaces the predicted vault, fixed factory, signer, chain, and estimated deployment action. Users then confirm deployment explicitly. After confirmation, PredictClaw uses MCP `vault_bootstrap(... mode="execute")`, captures the deployed vault address, and writes the resolved values back into `.env`.

Pros:
- Removes the hard block for normal users
- Preserves an explicit safety checkpoint before on-chain side effects
- Matches the desired product mental model: users bring signer + funding, product handles vault bootstrap

Cons:
- Requires coordinated runtime and doc changes
- Needs careful backfill rules so the final config is deterministic

## Recommended Design

Use Option C.

The system should stop treating explicit vault address and full derivation tuple as the default user entry point. Instead:

1. Users choose `mandated-vault` mode.
2. They supply only:
   - signer EOA private key
   - chain selection (or default chain)
   - any user-tunable funding/deployment amount controls
3. PredictClaw fills the protocol-level factory address automatically.
4. PredictClaw asks MCP for a bootstrap plan first.
5. PredictClaw shows a preview of what will happen.
6. User confirms.
7. PredictClaw calls MCP bootstrap execute mode.
8. PredictClaw writes back the actual deployed vault address and resolved chain/command state.

## UX Flow

### Step 1: Minimal configuration

The initial vault template should move away from this requirement:

- `ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT`

And instead guide the user toward:

- `PREDICT_WALLET_MODE=mandated-vault`
- `PREDICT_PRIVATE_KEY=...` (or whichever single EOA path is selected)
- `ERC_MANDATED_CHAIN_ID=...`
- optional deployment/funding caps if relevant
- `ERC_MANDATED_MCP_COMMAND` handled by the setup helper

The fixed factory address should be injected by the product default rather than required in user docs.

### Step 2: Preview

The first stateful bootstrap action should produce a preview payload containing at least:

- fixed factory address
- target chain id / chain name
- signer address
- predicted vault address
- whether the vault already exists
- deployment transaction summary (to / value / gas estimate if available)
- explicit note that confirmation is required before broadcast

### Step 3: Confirmation

The user confirms the deployment action. This should be a distinct confirmation step, not an implicit side effect of simply reading deposit guidance.

### Step 4: Execute and backfill

After confirmation:

- call MCP `vault_bootstrap(... mode="execute")`
- read the resulting `deployedVault`
- backfill `.env` with:
  - `ERC_MANDATED_VAULT_ADDRESS=<actual deployed vault>`
  - fixed `ERC_MANDATED_FACTORY_ADDRESS` if you still want it materialized for transparency
  - `ERC_MANDATED_CHAIN_ID`
  - `ERC_MANDATED_MCP_COMMAND` if already resolved by setup

### Step 5: Post-bootstrap status

From that point onward:

- `wallet deposit --json` becomes informational again
- `wallet status --json` should show `vaultAddressSource=explicit` or another resolved post-bootstrap state
- docs should no longer tell normal users to hand-author the vault address first

## Config Model Changes

### Defaults

- Treat `ERC_MANDATED_FACTORY_ADDRESS` as a product default, not a required first-time user input
- Current fixed default: `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6`

### New user-facing minimum

For first-time pure `mandated-vault`, the minimum path should become:

- signer EOA private key
- deployment-fee funding on the signer
- chain selection if non-default
- MCP launcher readiness

### Deprecated as default-first guidance

- manual explicit vault address
- full derivation tuple as the primary onboarding path

These can remain documented as advanced/manual recovery paths.

## Runtime Changes

### `lib/config.py`

- Add fixed factory default instead of requiring the user to provide it manually for the standard path
- Ensure config validation distinguishes between:
  - first-time bootstrap mode
  - already-deployed explicit vault mode
  - advanced manual derivation override mode

### `lib/wallet_manager.py`

- Extend `resolve_mandated_vault()` or a sibling flow so it can produce both:
  - preview plan
  - execute-and-backfill result
- Stop treating `mode="plan"` as the terminal bootstrap state for normal onboarding

### `lib/funding_service.py`

- Replace `broadcast: manual-only` as the only undeployed-vault path
- Return a preview object that clearly indicates confirmable deployment
- After execution, return the deployed vault address and refreshed status

### CLI / host flow

- Add an explicit bootstrap command or interactive confirm path rather than making plain `wallet deposit` silently broadcast
- Good candidates:
  - `predictclaw wallet bootstrap-vault --json`
  - or a two-step `wallet deposit --json` preview + `wallet bootstrap-vault --confirm`

## Documentation Changes

Update all of these to remove the current default-first manual path:

- `README.md`
- `README.zh-CN.md`
- `SKILL.md`
- `template.mandated-vault.env`
- `.env.mandated-vault.example`

New docs should say:

- default onboarding only needs signer + funding + MCP runtime
- factory address is product-configured
- deployment preview happens before broadcast
- advanced users can still override with explicit vault address or manual derivation tuple if needed

## Testing Changes

Add or update tests to cover:

- config default uses fixed factory address
- bootstrap preview path no longer hard-blocks on missing explicit vault address
- execute path backfills vault address after successful deployment
- docs no longer instruct default users to start with `0xYOUR_DEPLOYED_VAULT`
- old advanced/manual paths still work when explicitly chosen

## Hard Block Resolution

After this design is implemented, the reported hard block should disappear:

- current failure: placeholder `ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT`
- desired behavior: no placeholder vault address is required for the normal onboarding path

The new hard block, if any, should instead be limited to truly necessary inputs:

- missing signer key
- insufficient deployment fee funding
- missing MCP runtime
- failed bootstrap execution
