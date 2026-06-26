---
name: hypurrfi
description: DeFi lending on Hyperliquid. Deposit to earn yield, borrow against collateral. Supports Pooled (Aave v3), Prime/Yield (Euler), and Vault markets. Use when an agent wants to earn yield on idle assets, borrow stablecoins against HYPE, or manage a DeFi treasury.
metadata: {"openclaw":{"emoji":"🐱","homepage":"https://hypurr.fi","requires":{"bins":["node"]}}}
---

# HypurrFi Skill

**DeFi lending for AI agents on Hyperliquid.**

Deposit assets → Earn yield. Post collateral → Borrow. All on HyperEVM.

## Quick Start (Git Clone → Deposit in 5 min)

```bash
# 1. Clone and install
git clone https://github.com/hypurrfi/hypurrfi-skill.git ~/.openclaw/workspace/skills/hypurrfi
cd ~/.openclaw/workspace/skills/hypurrfi && npm install

# 2. Setup wallet (if you don't have one)
node scripts/setup.js --json

# 3. Fund your wallet with HYPE or stablecoins
# Bridge via https://cctp.to or transfer from HyperCore L1

# 4. Deposit!
node scripts/deposit.js pooled usdt0 100 --json
```

---

## Market Types

| Market | Risk | Style | Best For |
|--------|------|-------|----------|
| **Pooled** | Shared | Aave v3 | Deepest liquidity, cross-collateral borrowing |
| **Prime** | Lower | Euler | Safer assets, conservative strategies |
| **Yield** | Higher | Euler | Higher APY, riskier assets |
| **Vault** | Managed | Curated | Set-and-forget, ClearstarLabs managed |

**⚠️ Important:** Assets in one market can't collateralize another. HYPE in Prime ≠ collateral for Pooled borrows.

---

## Commands

### Check Your Positions

```bash
# Overview of all positions across markets
node scripts/positions.js --json

# Detailed health factor and liquidation risk
node scripts/health.js --json
```

### Deposit (Earn Yield)

```bash
# Deposit to specific market
node scripts/deposit.js <market> <token> <amount> [--yes] [--json]

# Examples
node scripts/deposit.js pooled usdt0 100 --json      # Pooled market
node scripts/deposit.js prime hype 10 --json         # Prime market (lower risk)
node scripts/deposit.js yield hype 10 --json         # Yield market (higher APY)
node scripts/deposit.js vault usdt0 100 --json       # ClearstarLabs vault
```

### Withdraw

```bash
node scripts/withdraw.js <market> <token> <amount|max> [--yes] [--json]

# Examples
node scripts/withdraw.js pooled usdt0 50 --json
node scripts/withdraw.js pooled usdt0 max --json     # Withdraw everything
```

### Borrow (Against Collateral)

```bash
# First deposit collateral, then borrow
node scripts/borrow.js <market> <token> <amount> [--yes] [--json]

# Example: Borrow USDT0 against HYPE collateral in Pooled
node scripts/deposit.js pooled hype 10 --yes --json
node scripts/borrow.js pooled usdt0 1000 --yes --json
```

### Repay

```bash
node scripts/repay.js <market> <token> <amount|max> [--yes] [--json]

# Example
node scripts/repay.js pooled usdt0 500 --json
node scripts/repay.js pooled usdt0 max --json       # Repay full debt
```

### Check APY Rates

```bash
node scripts/rates.js --json
```

---

## Tokens Supported

| Token | Address | Markets |
|-------|---------|---------|
| HYPE | Native | Pooled, Prime, Yield |
| USDT0 | `0xB8CE59FC3717ada4C02eaDF9682A9e934F625ebb` | All |
| USDC | `0x211Cc4DD073734dA055fbF44a2b4667d5E5fE5d2` | Pooled |
| USDXL | `0xca79db4B49f608eF54a5CB813FbEd3a6387bC645` | Pooled |
| hwHYPE | `0x...` | Prime, Yield |

---

## Safety Rules

1. **Always check health factor** before borrowing more
   - Health > 1.5 = Safe
   - Health 1.0-1.5 = Caution
   - Health < 1.1 = Liquidation risk!

2. **Confirm before transactions** — use `--yes` only after reviewing

3. **Start small** — test with small amounts first

4. **Monitor positions** — run `node scripts/health.js` regularly

5. **Keep gas reserves** — need ~0.01 HYPE for transactions

---

## Common Workflows

### Earn Yield on Stablecoins
```bash
# Deposit USDT0 to Pooled for ~5-15% APY
node scripts/deposit.js pooled usdt0 1000 --yes --json
```

### Leverage HYPE (Loop)
```bash
# 1. Deposit HYPE
node scripts/deposit.js pooled hype 100 --yes --json

# 2. Borrow stables against it
node scripts/borrow.js pooled usdt0 5000 --yes --json

# 3. (Optional) Buy more HYPE with borrowed stables
# ... then deposit that HYPE too (looping)
```

### Conservative Treasury
```bash
# Use Vault for managed, lower-touch yield
node scripts/deposit.js vault usdt0 10000 --yes --json
```

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "No wallet found" | Wallet not setup | Run `node scripts/setup.js` |
| "Insufficient balance" | Not enough tokens | Fund wallet first |
| "Health factor too low" | Over-leveraged | Repay debt or add collateral |
| "Amount exceeds available" | Trying to withdraw too much | Check positions, use `max` |

---

## Links

- App: https://app.hypurr.fi
- Docs: https://docs.hypurr.fi
- Explorer: https://explorer.hyperliquid.xyz
- Support: https://discord.gg/hypurrfi

---

## Wallet Location

Private key stored at: `~/.hyperliquid-wallet.json`

**Never share this file.** Same wallet works for HyperCore L1 and HyperEVM.
