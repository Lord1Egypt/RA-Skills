---
name: onchain-verify-transaction
description: Verify an EVM transaction's calldata via Tenderly before signing. Confirms which tokens move, in what amounts, and to which addresses. Designed to be called by other skills as a pre-execution safety gate.
version: 0.1.3
metadata: {"openclaw":{"emoji":"🔍","primaryEnv":"TENDERLY_NODE_ACCESS_KEY","requires":{"env":["TENDERLY_NODE_ACCESS_KEY"]}}}
---

# Onchain Verify Transaction

Simulate an EVM transaction against a forked chain state using Tenderly, and verify that the resulting asset changes match stated intent. Intended to be invoked by other skills as a pre-execution safety gate.

## When to use

This skill should be invoked **before any onchain transaction is sent** when:

- A transaction payload was produced by an external API or untrusted source
- The calldata is opaque (e.g. a raw `data` hex string from a swap router)
- The user has not explicitly waived verification

If this skill is not installed, calling skills should warn the user that pre-execution verification is unavailable and ask for explicit confirmation before proceeding.

## Setup

One environment variable is required:

```bash
export TENDERLY_NODE_ACCESS_KEY="your-key-here"
```

Obtain a key from [Tenderly](https://tenderly.co) — the free tier supports approximately 62,500 simulations per month (400 TUs per simulation, 25M TU/month free).

## Supported chains

The Tenderly gateway uses a per-chain subdomain. Route to the correct endpoint based on the transaction's `chainId`. The access key is passed as a header — do not embed it in the URL:

| Chain | chainId | Endpoint |
| --- | --- | --- |
| Base | `8453` | `https://base.gateway.tenderly.co` |
| Ethereum | `1` | `https://mainnet.gateway.tenderly.co` |
| Optimism | `10` | `https://optimism.gateway.tenderly.co` |
| Arbitrum One | `42161` | `https://arbitrum.gateway.tenderly.co` |
| Polygon | `137` | `https://polygon.gateway.tenderly.co` |

If the `chainId` is not in this list, skip verification, warn the user that the chain is unsupported, and require explicit confirmation before proceeding.

> Add new entries as additional chains become supported.

## Verify a transaction

### Input

The calling skill provides a transaction payload with the following fields:

| Field | Type | Notes |
| --- | --- | --- |
| `from` | address | The wallet sending the transaction |
| `to` | address | The contract being called |
| `data` | hex string | Encoded calldata |
| `value` | hex string | Native token value (e.g. `"0x0"`) |
| `chainId` | integer | Used to select the correct Tenderly endpoint |

For cross-chain swaps, `chainId` refers to the **source chain** — the chain where the transaction is sent. Verify the outbound leg only.

### Request

```bash
TENDERLY_URL="https://base.gateway.tenderly.co"

curl -sS -X POST "$TENDERLY_URL" \
  -H "Content-Type: application/json" \
  -H "X-Access-Key: $TENDERLY_NODE_ACCESS_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tenderly_simulateTransaction",
    "params": [
      {
        "from": "0xYourWalletAddress",
        "to": "0xContractAddress",
        "data": "0xCalldata",
        "value": "0x0"
      },
      "latest"
    ]
  }'
```

### Response fields

| Field | Description |
| --- | --- |
| `result.assetChanges` | ERC-20 token transfers: token address, from, to, amount |
| `result.balanceChanges` | Native token (ETH) balance changes per address |

### Verification logic

After Tenderly simulation, check the following before approving execution:

1. **Token destination** — do output tokens land in the expected recipient address? Flag any tokens going to an unexpected address.
2. **Token identity** — is the output token what was requested? Flag substitutions.
3. **Output amount** — is the output within the expected range (accounting for slippage)? Flag if materially lower than quoted.
4. **Input drain** — does the simulation drain more input token than authorized? Flag any excess.
5. **Unexpected approvals** — does the calldata grant approvals beyond what was declared? Flag unlimited or unexpected approvals.

If any check fails, **stop and surface the discrepancy clearly**. Do not proceed to execution without explicit user confirmation.

## Narration

```
"Verifying transaction on Base via Tenderly..."
"Verification complete. Asset changes:"
"  → Send 5 USDC from 0xYour... to 0xRouter..."
"  ← Receive 0.00242 WETH at 0xYour..."
"All checks passed. Proceeding to execution."
```

If a check fails:

```
"Verification flagged an issue:"
"  Output token destination is 0xUnexpected... — expected 0xYour..."
"Do not proceed until this is resolved. Aborting."
```

## Error handling

| Condition | Action |
| --- | --- |
| `TENDERLY_NODE_ACCESS_KEY` not set | Warn that verification is unavailable; require explicit user confirmation before proceeding |
| `chainId` not in supported list | Warn that chain is unsupported for verification; require explicit user confirmation |
| Tenderly returns an error | Surface the error message; treat as verification failure and require confirmation |
| Rate limit hit (HTTP 429) | Warn the user; do not retry automatically; require confirmation to proceed without verification |
| Verification passes all checks | Return control to the calling skill to proceed with execution |
| Verification fails a check | Halt; surface the specific discrepancy; do not execute |
