# OWS - Open Wallet Standard

Local-first, multi-chain wallet management for AI agents. By MoonPay.

- Website: https://openwallet.sh
- GitHub: https://github.com/open-wallet-standard/core
- npm: https://www.npmjs.com/package/@open-wallet-standard/core

## Prerequisites

OWS CLI (`ows`) must be pre-installed by the user. This skill does not install software. See https://openwallet.sh for installation instructions.

## When to Use

- Checking wallet balances
- Signing transactions or messages
- Making x402 payments to paid APIs
- Querying wallet info

## CLI Reference

```bash
# Wallet info
ows wallet list                    # List all wallets
ows wallet info                    # Show vault path + supported chains

# Balances
ows fund balance --wallet <name> --chain <chain>   # Check balance (base, ethereum, solana, etc.)

# Signing
ows sign message --wallet <name> --chain <chain> --message <msg>
ows sign tx --wallet <name> --chain <chain> --tx <hex>

# x402 payments
ows pay request --wallet <name> <url>       # Pay an x402-enabled API
ows pay discover <url>                       # Discover x402 services
```

## Node.js SDK

```typescript
import { signMessage } from "@open-wallet-standard/core";

const sig = signMessage("my-wallet", "evm", "hello");
```

## Supported Chains

EVM (Ethereum, Base, Polygon, Arbitrum), Solana, Bitcoin, Cosmos, Tron, TON, Sui, Filecoin, Spark. All derived from a single BIP-39 seed via CAIP-2 chain identifiers.

## Security Model

- Keys encrypted at rest (AES-256-GCM)
- Keys decrypted only during signing, wiped from memory immediately after
- Pre-signing policy engine for spending limits and chain allowlists
- The OWS API never returns raw private keys
- Append-only audit log

## Important

- Never ask for or handle raw private keys. OWS signs internally.
- Do not install or update OWS packages. Only use pre-installed CLI.
- See https://openwallet.sh for full documentation.
