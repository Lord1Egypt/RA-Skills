---
name: misttrack-payment
description: MistTrack x402 pay-per-use payment protocol. When the user does not have a MistTrack API Key, use the x402 protocol to pay per call with USDC.
disable_model_calls: true
---

# MistTrack x402 Payment

> **This sub-skill requires explicit user invocation.** Autonomous agent calls are disabled (`disable_model_calls: true`) because this skill can sign and broadcast on-chain transactions. Note that `disable_model_calls` is a documentation-level hint; platforms may not enforce it. The runtime guards below are enforced in code.

> When the user does not have a MistTrack API Key, the Agent can use the x402 protocol to pay per API call with USDC via EVM (EIP-3009) or Solana partial signing. Base chain is used by default.

> **SECURITY — Runtime protections enforced in code:**
> - This skill signs on-chain USDC transactions using a private key.
> - A hard cap of **$1.00 USDC per call** is enforced in code; amounts above this are rejected.
> - **Private keys must be supplied via `--key-file <path>`** — stored in a `chmod 600` file, never on the command line or in environment variables.
> - **`X402_PRIVATE_KEY` environment variable is refused** — `pay.py` exits with an error if this variable is set.

## Supported APIs and Pricing (USDC per call)

| # | x402 API Path | Original Path | Price |
|---|---|---|---|
| 1 | `https://openapi.misttrack.io/x402/address_labels` | `v1/address_labels` | $0.1 |
| 2 | `https://openapi.misttrack.io/x402/address_overview` | `v1/address_overview` | $0.5 |
| 3 | `https://openapi.misttrack.io/x402/risk_score` | `v2/risk_score` | $1.0 |
| 4 | `https://openapi.misttrack.io/x402/risk_score_create_task` | `v2/risk_score_create_task` | $1.0 |
| 5 | `https://openapi.misttrack.io/v2/risk_score_query_task` | `v2/risk_score_query_task` | $0 (free polling) |
| 6 | `https://openapi.misttrack.io/x402/transactions_investigation` | `v1/transactions_investigation` | $1.0 |
| 7 | `https://openapi.misttrack.io/x402/address_action` | `v1/address_action` | $0.5 |
| 8 | `https://openapi.misttrack.io/x402/address_trace` | `v1/address_trace` | $0.5 |
| 9 | `https://openapi.misttrack.io/x402/address_counterparty` | `v1/address_counterparty` | $0.5 |

## Supported EVM Chains

| Chain ID | Network |
|:---:|:---|
| 1 | Ethereum Mainnet |
| 10 | Optimism |
| 137 | Polygon |
| 8453 | Base (default) |
| 42161 | Arbitrum One |
| 43114 | Avalanche C-Chain |

---

## Usage

### 1. CLI

Private keys must never appear on the command line or in environment variables.
Store the key in a permission-restricted file and pass the file path:

```bash
# One-time setup: create key file
echo "your_hex_private_key" > ~/.x402_key
chmod 600 ~/.x402_key

# Full x402 payment flow (request → parse 402 → sign → retry)
python3 scripts/pay.py pay \
  --url "https://openapi.misttrack.io/x402/address_labels?address=0x..." \
  --key-file ~/.x402_key \
  --chain-id 8453

# Manually sign EIP-3009
python3 scripts/pay.py sign-eip3009 \
  --key-file ~/.x402_key \
  --token 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --chain-id 8453 \
  --to 0x209693Bc6afc0C5328bA36FaF03C514EF312287C \
  --amount 10000

# Sign a Solana partial transaction
echo "<base64_encoded_tx>" > tx.b64
python3 scripts/pay.py sign-solana \
  --key-file ~/.x402_key \
  --transaction-file tx.b64
```

**`X402_PRIVATE_KEY` environment variable is not supported.** `pay.py` exits with an error if this variable is set.

### 2. Inline Code Usage

> **Warning**: The example below uses `auto_pay=True`, which means the Agent will automatically sign and broadcast payment transactions without per-call confirmation. Do not enable this in production environments, and avoid hardcoding or storing private keys in environment variables long-term.

```python
from scripts.pay import request_with_x402

response = request_with_x402(
    url="https://openapi.misttrack.io/x402/address_labels?address=0x...",
    private_key="your_private_key_hex",
    chain_id=8453,
    auto_pay=True,  # True = auto-pay without confirmation; set to False in production
)
print(response.json())
```

---

## Security Limits

- Per-call payment cap: **$1.00 USDC (1,000,000 smallest units)**. Amounts exceeding this are automatically rejected to prevent a malicious server from draining the wallet.
- Private keys must be supplied via `--key-file <path>`. The file is read at invocation time; the key never appears on the command line or in environment variables. Use `chmod 600` on the key file. `X402_PRIVATE_KEY` environment variable is not accepted.

---

## Dependencies

```bash
pip install eth-account eth-abi eth-utils requests
# For Solana payments, additionally install:
pip install solders base58
```
