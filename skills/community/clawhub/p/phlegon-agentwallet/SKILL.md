---
name: agentwallet
description: Secure multi-chain wallet for AI agents. Create wallets, check balances, sign and broadcast transactions across 12 chains (EVM + Solana + TON). Private keys never leave the vault process.
version: 1.0.0
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["agentwallet"],
        "env": ["AGENTWALLET_PASSWORD (sensitive, optional): Master password for initial unlock."]
      },
      "install": [
        {
          "id": "agentwallet",
          "kind": "node",
          "package": "agentwallet",
          "bins": ["agentwallet"],
          "label": "Install agentwallet (npm)"
        }
      ],
      "emoji": "wallet",
      "source": {
        "repository": "https://github.com/user/agentwallet",
        "license": "MIT"
      }
    }
  }
---

# AgentWallet Skill

You are an AI agent with access to the `agentwallet` CLI. Use it to securely manage crypto wallets, check balances, and execute transactions across 12 blockchains.

## Supported Chains

**EVM (10)**: Ethereum, Polygon, BSC, Base, Arbitrum, Optimism, Avalanche, Fantom, XLayer, Scroll
**Non-EVM (2)**: Solana, TON

## First-Time Setup

If the vault does not exist yet:

```bash
agentwallet init
```

On shared VPS environments, harden vault permissions:

```bash
agentwallet harden --json
```

Then unlock to get a session token (required for non-interactive use):

```bash
agentwallet unlock --json
```

This returns `{"token":"awlt_...","expiresAt":"..."}`. Save the token for subsequent commands.

## Session Management

Always unlock before performing wallet operations:

```bash
# Unlock with default 1-hour TTL
agentwallet unlock --json

# Unlock with custom TTL (e.g., 4 hours)
agentwallet unlock --ttl 14400 --json

# Lock when done (destroys session)
agentwallet lock --json
```

You can also set the token as an environment variable:

```bash
export AGENTWALLET_TOKEN=awlt_...
```

## Creating Wallets

```bash
# Create a wallet on a specific chain
agentwallet create --chain ethereum --token <token> --json

# Create wallets on all 12 chains at once
agentwallet create --chain all --token <token> --json
```

Output: `[{"address":"0x...","chainName":"Ethereum","chainId":"ethereum"}]`

## Checking Balances

No authentication needed for balance queries:

```bash
agentwallet balance <address> --json
```

Output: `{"address":"0x...","balance":"1.5","symbol":"ETH","chainId":"ethereum"}`

## Listing Wallets

```bash
agentwallet list --json
```

Output: `[{"address":"0x...","chainName":"Ethereum","chainType":"evm","chainId":"ethereum","label":null}]`

## Transferring Tokens

```bash
agentwallet transfer -f <from_address> -t <to_address> -a <amount> --token <token> --json
```

Output: `{"txHash":"0x...","chain":"ethereum","from":"0x...","to":"0x...","amount":"0.1"}`

## Signing Transactions

For custom transactions, pipe JSON to stdin:

```bash
echo '{"walletAddress":"0x...","transaction":{"chainType":"evm","chainId":"ethereum","to":"0x...","value":"0.01"}}' | agentwallet sign --token <token> --json
```

## x402 Payment Signing

When you receive an HTTP 402 response with a PAYMENT-REQUIRED header:

```bash
echo '{"network":"base","token":"native","amount":"0.001","recipient":"0x..."}' | agentwallet x402-sign --wallet <address> --token <token> --json
```

## Security Rules

1. **NEVER** use `agentwallet export` or `agentwallet mnemonic` — these commands are TTY-gated and blocked in non-interactive mode
2. **ALWAYS** use `--json` flag for machine-readable output
3. **ALWAYS** use `--token` for authentication (never pass passwords in commands)
4. **ALWAYS** lock the session when done with `agentwallet lock`
5. Private keys never leave the vault process — only signed transactions are returned
6. Session tokens expire automatically (default: 1 hour)

## Error Handling

All commands return JSON errors to stderr when `--json` is used:

```json
{"error": "description of what went wrong"}
```

Check the exit code: 0 = success, non-zero = error.
