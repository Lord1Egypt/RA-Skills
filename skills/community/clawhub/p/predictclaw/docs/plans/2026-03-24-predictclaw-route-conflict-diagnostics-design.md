# PredictClaw Route Conflict Diagnostics Design

## Goal

Keep `PREDICT_WALLET_MODE` as the explicit execution truth, but make PredictClaw explain route conflicts and route intent clearly when users mix `mandated-vault` mode with Predict Account credentials or try to use the wrong local route for their funding goal.

## Current Problem

- The repository intentionally treats pure `mandated-vault` and `predict-account + ERC_MANDATED_*` as different product routes.
- `lib/config.py` rejects `PREDICT_ACCOUNT_*` credentials when `PREDICT_WALLET_MODE=mandated-vault`, but the current error only says the credentials are not allowed.
- That error is technically correct, but it does not explain the routing implication: the current mode is still the pure vault control-plane path, not the Predict Account funding path.
- `wallet status` and `wallet deposit` describe the active route once config is valid, but they do not help enough when the configuration is in a route-conflict state.

## Constraints

- Do not silently change the active route.
- Do not infer a different execution mode from extra credentials.
- Keep `PREDICT_WALLET_MODE` as the single source of execution truth.
- Improve diagnostics and guidance without weakening current safety boundaries.

## Options Considered

### Option A: Auto-switch to overlay when Predict Account credentials are present

If `PREDICT_ACCOUNT_ADDRESS` and `PREDICT_PRIVY_PRIVATE_KEY` are present together with `ERC_MANDATED_*`, auto-route to `predict-account` semantics even when the explicit mode still says `mandated-vault`.

Pros:
- Fewer manual config edits for users who clearly want Predict Account funding.

Cons:
- Breaks the current contract that `PREDICT_WALLET_MODE` is authoritative.
- Silently changes execution semantics and trust boundaries.
- Risks surprising users during real-funds workflows.

### Option B: Keep explicit mode authoritative and add route-aware diagnostics (recommended)

Keep the current validation boundary, but raise a richer route-conflict error and expose route intent explicitly in valid `wallet status` / `wallet deposit` outputs.

Pros:
- Preserves safety and predictability.
- Solves the actual UX problem: users cannot tell why the current route does not match their funding goal.
- Keeps docs/tests aligned with the current architecture.

Cons:
- Users still need to edit `.env` to switch routes.

### Option C: Add a read-only overlay preview on top of conflicts

Keep failures strict, but attach a preview of the recommended route when credentials suggest the user wants Predict Account funding.

Pros:
- More helpful than a plain failure.

Cons:
- More complex CLI and JSON semantics.
- Easier for users to misread a failed command as partially successful.

## Recommended Design

Use Option B.

### 1. Add a structured route-conflict error

When config validation detects `PREDICT_WALLET_MODE=mandated-vault` together with `PREDICT_ACCOUNT_ADDRESS` and `PREDICT_PRIVY_PRIVATE_KEY`, raise a dedicated route-aware config error instead of a generic mutual-exclusion message.

The error should include:

- `activeMode`
- `activeRoute`
- `recommendedMode`
- `recommendedRoute`
- `routeConflictReason`
- `detectedCapabilities`
- `nextStep`

For text output, the message should explain that pure `mandated-vault` is the vault control-plane route, while Predict Account top-up requires `PREDICT_WALLET_MODE=predict-account`.

### 2. Emit structured JSON errors for wallet commands

`scripts/wallet.py` should not print only a string on config failure in JSON mode. Instead it should emit a stable error payload that preserves the route-aware guidance fields.

This keeps `wallet status --json` and `wallet deposit --json` useful even when the configuration is invalid.

### 3. Expose active route metadata in successful wallet outputs

For valid configurations, enrich `wallet status` / `wallet deposit` output with explicit route semantics:

- pure `mandated-vault` -> `activeRoute = vault-control-plane`
- overlay `predict-account + ERC_MANDATED_*` -> `activeRoute = vault-to-predict-account`

Also add a short human-readable route purpose, such as:

- `bootstrap-or-direct-vault-ops`
- `predict-account-top-up-and-trading`

### 4. Improve plain-text guidance

Plain-text `wallet status` and `wallet deposit` should say which route is currently active and whether that route funds the vault itself or the Predict Account.

For pure `mandated-vault`, add a direct line explaining that the current route funds the vault itself and is not the Predict Account top-up route.

## Files Likely To Change

- `lib/config.py`
- `lib/wallet_manager.py`
- `lib/funding_service.py`
- `scripts/wallet.py`
- `tests/test_config.py`
- `tests/test_wallet.py`
- `tests/test_funding.py`
- `tests/test_cli_router.py`

## Success Criteria

- Route-conflict failures tell users exactly why the current mode and credentials do not match.
- JSON wallet commands return structured route guidance on failure.
- Successful pure-vault outputs explicitly identify themselves as vault control-plane routes.
- Successful overlay outputs continue to identify themselves as `vault-to-predict-account` routes.
- No command silently changes route semantics behind the user's back.
