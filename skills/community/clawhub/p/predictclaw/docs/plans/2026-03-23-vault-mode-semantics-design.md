# Vault Mode Semantics Design

## Goal

Correct the user-facing documentation so PredictClaw presents only four user-facing modes:

1. `read-only`
2. `eoa`
3. `predict-account`
4. `predict-account + vault`

The existing `mandated-vault` label should remain only as an internal/bootstrap implementation detail and compatibility term, not as a standalone user mode.

## Current Problem

README, README.zh-CN, SKILL, top-level CLI help, and template descriptions currently describe `mandated-vault` as a separate mode. That causes two kinds of confusion:

- Humans think there are five modes instead of four.
- OpenClaw sees `mandated-vault` as a first-class user choice instead of understanding it as the internal subflow used to create/bind a vault for `predict-account + vault`.

## Recommended Approach

Use a user-facing / implementation-facing split.

### User-facing semantics

Only describe four modes:

- `read-only`
- `eoa`
- `predict-account`
- `predict-account + vault`

For `predict-account + vault`, explain the onboarding decision tree:

- If the user already has a vault, bind it with env variables.
- If the user does not yet have a vault, use the bootstrap helper to create one, then bind the result.

### Implementation-facing semantics

Keep `mandated-vault` visible only as:

- an internal bootstrap subflow
- an internal/compatibility template
- a technical term needed to explain current env/runtime behavior

Do **not** present it as a standalone user mode.

## Template Strategy

Add a new canonical user-facing template:

- `template.predict-account-vault.env`

Keep the existing:

- `template.mandated-vault.env`

but relabel it as an internal/compatibility bootstrap template.

This preserves runtime compatibility while giving users/OpenClaw a canonical entry point that matches the intended product model.

## Copy Changes

### README / README.zh-CN / SKILL

- Replace all user-facing “mandated-vault mode” language with “predict-account + vault”.
- Add a short explanation that vault creation uses an internal bootstrap subflow.
- Reframe `wallet bootstrap-vault` as the helper command used during `predict-account + vault` onboarding.

### CLI help

- Top-level help should no longer imply `mandated-vault` is a user-facing mode.
- Environment notes should explain that `PREDICT_WALLET_MODE=mandated-vault` still exists internally for the bootstrap path, but is not a standalone user-facing mode.

### Templates

- `template.predict-account-vault.env`: canonical user-facing template.
- `template.mandated-vault.env`: internal/compatibility bootstrap template.

## Success Criteria

- Documentation consistently describes only four user-facing modes.
- `predict-account + vault` becomes the canonical advanced route.
- `mandated-vault` remains discoverable only as internal/bootstrap vocabulary.
- Template and docs tests lock this distinction to prevent regression.
