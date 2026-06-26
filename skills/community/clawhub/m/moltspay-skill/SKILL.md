---
name: moltspay-skill
description: |
  Pay for and use AI services via MoltsPay protocol.
  Trigger: User asks to generate video, use a paid service, etc.
  Auto-discovers services from /.well-known/agent-services.json
---

# MoltsPay Client Skill

Pay for AI services using USDC/USDT across 8 crypto chains (gasless), or in CNY via Alipay (支付宝) — the fiat rail added in MoltsPay 2.0.

## When to Use

- User asks to generate a video, image, or use any paid AI service
- User asks about wallet balance or payment history
- User wants to discover available services
- User mentions "pay", "buy", "purchase" + AI service

## Available Commands

| Command | Description |
|---------|-------------|
| `moltspay init` | Create wallet (works on all EVM chains + Solana) |
| `moltspay fund <amount>` | Fund wallet via QR code (debit card/Apple Pay) |
| `moltspay status` | Check balance on all chains |
| `moltspay config` | Modify spending limits |
| `moltspay services <url>` | List services from a provider or marketplace |
| `moltspay pay <url> <service> --chain <chain>` | Pay for a service |

## Supported Chains

| Chain | ID | Tokens | Notes |
|-------|-----|--------|-------|
| Base | `base` | USDC, USDT | Recommended, lowest fees |
| Polygon | `polygon` | USDC | Alternative EVM |
| BNB Chain | `bnb` | USDC, USDT | High liquidity |
| opBNB | `opbnb` | USDC | BNB L2, very low fees |
| Solana | `solana` | USDC | Fast, separate wallet |
| Tempo | `tempo_moderato` | pathUSD | Testnet only |
| Base Sepolia | `base_sepolia` | USDC | Testnet |
| BNB Testnet | `bnb_testnet` | USDC | Testnet |
| Solana Devnet | `solana_devnet` | USDC | Testnet |

## Fiat Rail — Alipay (new in MoltsPay 2.0)

In addition to the crypto chains above, MoltsPay 2.0 adds a **fiat rail**: pay in **CNY via Alipay (支付宝)**.

| Rail | ID | Currency | Notes |
|------|-----|----------|-------|
| Alipay | `alipay` | CNY (yuan) | For services that price in CNY; no crypto balance needed |

- Use it the same way as a chain: `moltspay pay <url> <service> --chain alipay`.
- A service exposes a CNY price when its provider has the Alipay rail enabled; if a service is crypto-only, pay on one of the crypto chains instead.
- Settlement is handled by the Alipay rail — the agent does not manage a crypto wallet for these payments.

## Wallet Setup

`moltspay init` creates wallets for all chains:

**EVM Chains** (Base, Polygon, BNB, opBNB, Tempo):
- Single address works on all EVM chains
- Same private key, different networks

**Solana**:
- Separate Ed25519 keypair
- Different address from EVM

After setup, tell user their wallet addresses and that they need to fund with USDC on their preferred chain.

## Discover Services

### Marketplace Discovery

List all services on MoltsPay marketplace:
```
moltspay services https://moltspay.com
```

### Single Provider Discovery

List services from a specific provider:
```
moltspay services https://juai8.com/zen7
```

Shows provider name, wallet, supported chains, and all services with prices.

**Present results as a table to users:**

| Service | Price | Chains |
|---------|-------|--------|
| text-to-video | $0.99 USDC | Base, Polygon, BNB |
| image-to-video | $1.49 USDC | Base, Polygon, BNB |

Never show raw JSON to users - always format nicely.

## Chain Selection (Pay Only)

When paying:
- If server accepts only one chain → auto-selected
- If server accepts multiple chains → specify with `--chain`

Examples:
```bash
# Pay on Base (recommended)
moltspay pay https://juai8.com/zen7 text-to-video --prompt "a cat dancing" --chain base

# Pay on Polygon
moltspay pay https://juai8.com/zen7 text-to-video --prompt "a cat dancing" --chain polygon

# Pay on BNB
moltspay pay https://juai8.com/zen7 text-to-video --prompt "a cat dancing" --chain bnb

# Pay on Solana
moltspay pay https://example.com/service image-gen --prompt "sunset" --chain solana

# Pay in CNY via Alipay (fiat, no crypto balance needed)
moltspay pay https://example.com/service text-to-video --prompt "a cat dancing" --chain alipay
```

## Paying for Services

Use the `moltspay pay` command with the provider URL and service ID.

**Parameters vary by service:**
- `--prompt` for text-based services
- `--image` for image-based services
- `--chain` to specify which chain to pay on
- `--token` to specify token (USDC or USDT, default USDC)

Example: Zen7 video generation
```
moltspay pay https://juai8.com/zen7 text-to-video --prompt "sunset over ocean" --chain base
```

## Spending Limits

Users can configure:
- **max-per-tx**: Maximum per transaction (default $2)
- **max-per-day**: Daily spending limit (default $10)

Use `moltspay config` to modify limits.

## Funding Your Wallet

### Option 1: QR Code (Easiest - No crypto needed!)

```bash
# Fund $10 on Base (recommended)
moltspay fund 10

# Fund $20 on Polygon  
moltspay fund 20 --chain polygon

# Fund $10 on Solana
moltspay fund 10 --chain solana
```

Scan QR code → pay with US debit card or Apple Pay → tokens arrive in ~2 minutes.

**No CDP credentials or crypto knowledge needed.** Server handles everything.

### Option 2: Direct Transfer

**EVM Chains** - Same address works on Base, Polygon, BNB, opBNB:
- Send USDC from Coinbase, MetaMask, etc.
- Make sure you're on the correct network!

**Solana** - Different address:
- Send USDC to your Solana wallet address
- Check with `moltspay status`

⚠️ **Important:**
- Balance on Base ≠ Balance on Polygon ≠ Balance on Solana (separate!)
- Check balance per chain with `moltspay status`
- No ETH/MATIC/SOL needed for gas (gasless transactions via x402)
- Exception: BNB needs tiny amount of BNB for first approval (~$0.0001)

## Common User Requests

### "Generate a video of X"

1. Check wallet status (`moltspay status`)
2. If not initialized → run `moltspay init`
3. If balance is 0 → tell user to fund wallet
4. If funded → pay for text-to-video service with appropriate chain
5. Return video URL to user

### "What's my balance?"

Run `moltspay status` and report:
- Wallet addresses (EVM + Solana)
- Balance on each chain
- Spending limits
- Today's usage

### "What services are available?"

Run `moltspay services https://moltspay.com` to list marketplace.
Format results as a clean table with service names, prices, and providers.

## Error Handling

| Error | Solution |
|-------|----------|
| Insufficient balance | Fund wallet with USDC on the chain you want to use |
| Exceeds daily limit | Wait until tomorrow, or increase limit with `moltspay config` |
| Exceeds per-tx limit | Increase limit with `moltspay config` |
| Service not found | Verify service URL and ID |
| Chain mismatch | Server doesn't accept specified chain. Check supported chains. |
| Multi-chain required | Server accepts multiple chains. Specify `--chain` |
| BNB approval needed | First BNB payment needs tiny gas (~$0.0001 BNB) |
| Alipay not accepted | Service is crypto-only. Pay on a crypto chain instead |

## Testnet Faucets

For testing without real money:

```bash
# Get 1 USDC on Base Sepolia
moltspay faucet --chain base_sepolia

# Get 1 USDC on BNB Testnet (+ 0.001 tBNB for gas)
moltspay faucet --chain bnb_testnet

# Get 1 USDC on Solana Devnet
moltspay faucet --chain solana_devnet
```

Limit: 1 USDC per address per 24 hours.

## Links

- Docs: https://moltspay.com/docs
- Marketplace: https://moltspay.com/services
- GitHub: https://github.com/Yaqing2023/moltspay-skill
