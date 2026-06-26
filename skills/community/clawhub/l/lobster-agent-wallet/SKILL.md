# 🦞 Agent Wallet Skill

USDC wallet for AI agents on Base with x402 payment protocol support.

## ⚠️ Security

This skill interacts with real blockchain assets. Every precaution is taken.

| Rule | Status |
|------|--------|
| Private key from env var only | ✅ `WALLET_PRIVATE_KEY` / `.env` |
| Private key never logged | ✅ Zero logging of key material |
| Payments need explicit --confirm | ✅ Double security gate |
| Address separate from key | ✅ `WALLET_ADDRESS` for read-only mode |

## Phase 1 — Read-Only (Zero Dependencies)

```bash
export WALLET_ADDRESS=0x...
export WALLET_NETWORK=base-sepolia
node wallet.mjs balance
```

## Phase 2 — x402 Payments (Requires viem)

```bash
npm install viem
export WALLET_PRIVATE_KEY=0x...         # your wallet key (keep secret!)
export WALLET_ADDRESS=0x...             # derived from key, or set manually
export WALLET_NETWORK=base-sepolia      # or "base" for mainnet

node wallet.mjs pay <url> --confirm
```

## CLI Reference

| Command | Requires | Description |
|---------|----------|-------------|
| `balance` | WALLET_ADDRESS | Check USDC + ETH balance |
| `status` | WALLET_ADDRESS | Show wallet config (safe) |
| `pay <url>` | + PRIVATE_KEY + --confirm | Pay x402 resource |

## Architecture

```
agent-wallet/
├── SKILL.md               ← Usage docs
├── package.json           ← Zero deps (viem optional for Phase 2)
├── .env.example           ← Config template
├── wallet.mjs             ← CLI entry point
└── lib/
    ├── core.mjs           ← Core wallet (native fetch RPC, no deps)
    ├── crypto.mjs         ← EIP-3009 signing (viem-powered)
    └── x402-client.mjs    ← x402 payment protocol client
```

## Networks

| Network | Chain ID | RPC | Explorer |
|---------|----------|-----|----------|
| Base | 8453 | mainnet.base.org | basescan.org |
| Base Sepolia | 84532 | sepolia.base.org | sepolia.basescan.org |

## Integration (for agents/skills)

```javascript
import { getWallet, getBalances } from './lib/core.mjs';

// Read-only — safe
const wallet = await getWallet();
const { eth, usdc } = await getBalances(wallet);

// Payments (requires viem)
const { payX402 } = await import('./lib/x402-client.mjs');
const result = await payX402(url, privateKey, { confirm: true });
```

## License MIT-0
