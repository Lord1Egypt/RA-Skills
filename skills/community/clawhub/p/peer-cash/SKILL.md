---
name: peer-cash
description: Cash out Base USDC to fiat through Peer with custody-separated MCP tools.
metadata:
  openclaw:
    requires:
      bins:
        - npx
    envVars:
      - name: PEER_CASH_ENVIRONMENT
        required: false
        description: Peer Cash environment. Defaults to production.
      - name: PEER_CASH_RPC_URL
        required: false
        description: Custom Base RPC URL for reads and receipt finalization.
      - name: PEER_CASH_API_KEY
        required: false
        description: Curator API key when the selected environment requires one.
      - name: PEER_CASH_REFERRAL_CODE
        required: false
        description: Six-character Peer integration referral code.
      - name: PEER_CASH_REFERRER
        required: false
        description: Analytics-only ERC-8021 attribution code.
    homepage: https://github.com/zkp2p/peer-cash-mcp
---

# Peer Cash

Use Peer Cash when the user wants to cash out Base USDC to fiat, compare live payout rails, estimate fiat received, track a cash-out, withdraw unmatched funds, or top up an open order.

Peer Cash is custody-separated. Its MCP server prepares transactions and reads protocol state, but it never accepts a private key, signs, or broadcasts. The OpenClaw host or connected wallet owns approval, signing, submission, and receipt confirmation.

## One-time setup

Check whether the server is already configured:

```bash
openclaw mcp show peer-cash --json
```

If it is missing, add the published stdio server and prove that it starts:

```bash
openclaw mcp add peer-cash --command npx --arg -y --arg peer-cash-mcp
openclaw mcp doctor peer-cash --probe
```

Do not overwrite an existing `peer-cash` definition without showing the current configuration and getting operator approval. Optional environment variables belong on the OpenClaw gateway host. Never place secrets in a prompt, tracked config, or command argument.

The MCP tool names may be namespaced by the runtime. Match them by the exact suffixes documented below.

## Required operating rules

1. Call `peer_cash_capabilities` before naming a payout platform, currency, amount bound, or source asset.
2. Treat `peer_cash_estimate` as approximate. The binding Chainlink rate resolves when a buyer fills; never call it a locked quote.
3. Amounts are decimal base-unit strings. Base USDC has 6 decimals, so 100 USDC is `100000000`.
4. Never request or handle a private key or seed phrase.
5. Before any host signs or submits a transaction, show the destination, value, calldata purpose, ordered steps, and expected effect. Get explicit user approval for that exact plan.
6. Submit prepared transactions in the returned order. Confirm each required receipt before continuing.
7. Persist the returned `depositId`. It is the durable resume key for order tracking and recovery.
8. Do not blindly retry an unknown transaction outcome. Inspect the named hash, wallet activity, and existing orders first.

## Cash-out flow

1. Call `peer_cash_capabilities`.
2. Call `peer_cash_estimate` with the requested Base USDC amount and currency. Explain that the result is an oracle estimate, not a guaranteed payout.
3. Collect only the payee fields required by the chosen platform.
4. Call `peer_cash_prepare` with the amount and one or more receive legs.
5. Present the returned unsigned transactions and `steps` for approval.
6. After approval, have the configured host wallet submit each transaction in order on Base.
7. Confirm the `createDeposit` receipt, then call `peer_cash_finalize` with that transaction hash.
8. If the prepare result set `accessPolicyRequired` to `true`, call `peer_cash_prepare_access_policy`, obtain approval, and submit that policy transaction with the depositor wallet.
9. Return and persist the `depositId`. Use `peer_cash_order` for current state and next actions.

## Order management

- `peer_cash_order`: read one order from its `depositId`.
- `peer_cash_orders`: list a maker wallet's orders. Set `inFlight` to `true` for orders still needing attention.
- `peer_cash_prepare_withdraw`: prepare a full close when `amount` is omitted, or a partial unmatched-funds withdrawal when it is present.
- `peer_cash_prepare_top_up`: prepare approval and `addFunds` transactions for a live order.

Withdrawal and top-up plans follow the same approval and ordered-submission rules as a new cash-out.

## Recovery

Peer Cash errors may include `code`, `retryable`, `remediation`, and `recovery`. Follow those fields instead of improvising retries.

- `ORDER_NOT_FOUND` immediately after finalization can be indexer lag. Retry only the read. The confirmed receipt remains the source of truth.
- `TRANSACTION_SUBMISSION_UNKNOWN`: inspect wallet activity and existing orders before any resubmission.
- `TRANSACTION_STATUS_UNKNOWN`: inspect the named transaction hash first.
- `ACCESS_POLICY_CONFIGURATION_FAILED`: the deposit already exists. Repair the policy step; do not create another cash-out.
- `INDEXER_UNAVAILABLE` or `ORACLE_READ_FAILED`: retry the read only.

If the evidence cannot prove whether a mutation happened, stop and ask the user to inspect the wallet or block explorer. Do not manufacture certainty.
