# Vault Deposit Default Design

## Goal

Align PredictClaw's `predict-account + vault` funding semantics so the default user-facing funding entry is the Vault deposit flow, while Predict Account remains the trading identity and downstream recipient of vault-driven funding.

## Problem

Current product messaging and CLI output are split:

- Some output fields still suggest the user should manually top up the Predict Account directly.
- The intended product model is that `predict-account + vault` defaults to funding through the Vault deposit flow.
- OpenClaw needs stable fields that distinguish:
  - default funding ingress
  - trading identity
  - downstream funding target

## Design

### User-facing semantics

- `fundingAddress` should point to the Vault address for `predict-account + vault`.
- `manualTopUpAddress` should also point to the Vault, because it represents the default funding ingress.
- `predictAccountAddress` and `tradingIdentityAddress` should continue to identify the Predict Account.
- Human-readable output should explain that users fund the Vault first, then Vault-driven orchestration tops up the Predict Account.

### Internal semantics

- The internal funding route remains `vault-to-predict-account`.
- The internal orchestration target can still be the Predict Account.
- We are changing the *user-facing* funding entry semantics, not the underlying orchestration identifier.

## Success Criteria

- `wallet deposit --json` and `wallet status --json` point user-facing funding entry fields at the Vault.
- CLI text says Vault deposit flow is the default funding entry.
- Docs and tests describe Predict Account as the trading identity while Vault is the default funding ingress.
