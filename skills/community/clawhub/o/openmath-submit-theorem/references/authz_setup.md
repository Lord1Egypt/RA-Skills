# OpenMath Authz Setup

Use this when `openmath-submit-theorem` is configured for the default authz-based flow and authz or feegrant still needs to be created manually.

This reference is not the primary setup guide. Use `references/init-setup.md` first for:

- creating or updating `openmath-env.json`
- resolving or creating the local `agent_key_name`
- getting `prover_address` and `agent_address`
- the normal website authorization flow

Use this document only when the environment is already configured but the authz/feegrant step must be checked or repaired manually.

## Preconditions

Before using the commands below, confirm:

- `openmath-env.json` already exists and has `prover_address`, `agent_key_name`, and `agent_address`
- the local key named by `agent_key_name` already exists in the `os` keyring
- `python3 scripts/check_authz_setup.py [--config <selected-path>]` is failing because authz or feegrant is still missing

If any of those are not true, stop and return to `references/init-setup.md`.

Before running manual authz or feegrant transactions, get explicit user approval.

Runtime chain settings are not stored in `openmath-env.json`:

- `SHENTU_CHAIN_ID` or default `shentu-2.2`
- `SHENTU_NODE_URL` or default `https://rpc.shentu.org:443`

## Manual CLI Fallback

If the website flow is unavailable, the OpenMath wallet owner can authorize the agent manually. Use `SHENTU_CHAIN_ID` and `SHENTU_NODE_URL`, or fall back to the built-in defaults `shentu-2.2` and `https://rpc.shentu.org:443`.

### Authz Grants

```bash
shentud tx authz grant <agent-address> generic \
  --msg-type=/shentu.bounty.v1.MsgSubmitProofHash \
  --expiration 2026-03-18T00:00:00Z \
  --from <prover-key> \
  --chain-id <shentu_chain_id> \
  --node <shentu_node_url>

shentud tx authz grant <agent-address> generic \
  --msg-type=/shentu.bounty.v1.MsgSubmitProofDetail \
  --expiration 2026-03-18T00:00:00Z \
  --from <prover-key> \
  --chain-id <shentu_chain_id> \
  --node <shentu_node_url>
```

### Feegrant

The feegrant must allow the outer authz wrapper:

```bash
shentud tx feegrant grant <prover-address> <agent-address> \
  --allowed-messages "/cosmos.authz.v1beta1.MsgExec" \
  --spend-limit 1000000uctk \
  --expiration 2026-03-18T00:00:00Z \
  --gas-prices 0.025uctk \
  --gas-adjustment 2.0 \
  --gas auto \
  --chain-id <shentu_chain_id> \
  --node <shentu_node_url> \
  --keyring-backend os
```

Add more message types only if the agent also needs direct access outside `authz exec`.

## Validation

Run the bundled checker before generating submission commands:

```bash
python3 scripts/check_authz_setup.py [--config <selected-path>]
```

The checker verifies:

- `shentud` is available
- the local agent key exists and matches the configured address
- authz grants exist for the required OpenMath message types
- a feegrant exists and allows `/cosmos.authz.v1beta1.MsgExec`

Warnings about missing `spend_limit` or `expiration` do not block submission, but they indicate a broad feegrant.

`generate_submission.py` in authz mode should be treated as blocked until this checker reports `Status: ready`.
