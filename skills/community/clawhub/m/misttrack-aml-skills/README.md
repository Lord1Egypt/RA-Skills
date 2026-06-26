# MistTrack Skills

An AI Agent skill pack for the MistTrack OpenAPI - cryptocurrency address risk analysis, AML compliance checks, and on-chain transaction tracing.

## Overview

[MistTrack](https://misttrack.io/) is an AML tracking tool developed by [SlowMist](https://www.slowmist.com/en/), covering 400M+ addresses and 500K+ threat intelligence entries.

- Works with OpenClaw, Claude Code, and other major agent platforms
- Integrates with **Bitget Wallet Skill** / **Trust Wallet Skills** / **Binance Skills** / **OKX Agent Skills** - automatically runs MistTrack address security checks before any transfer
- Supports identifying and parsing multi-signature addresses
- Supports x402 Payment, allowing usage without an API key by paying via x402.

## Installation

### Via skills CLI (recommended for agent platforms)

```bash
npx skills add slowmist/misttrack-skills
```

### Direct Python (recommended for security-sensitive environments)

Run the scripts directly from source without any binary packaging:

```bash
# 1. Clone or download the source
git clone https://github.com/slowmist/misttrack-skills
cd misttrack-skills

# 2. Install core dependencies (for AML scripts)
pip install -r requirements.txt

# 3. Optional: install payment dependencies (only if using pay.py)
pip install -r requirements-pay.txt

# 4. Set your API key
export MISTTRACK_API_KEY=your_api_key

# 5. Run directly
python3 scripts/risk_check.py --address 0x... --coin ETH
python3 scripts/transfer_security_check.py --address 0x... --chain eth
python3 scripts/batch_risk_check.py --input addresses.txt --coin ETH
python3 scripts/address_investigation.py --address 0x... --coin ETH
python3 scripts/multisig_analysis.py --address 0x... --chain eth
```

## Where to Find Our Project

- [Skills](https://skills.sh/slowmist/misttrack-skills/misttrack-skills)
- [Clawhub](https://clawhub.ai/MistTrack/misttrack-aml-skills)

## Example Prompts

### Quick Risk Check (KYT)

- Check the risk score for ETH address `0x6487B5006904f3Db3C4a3654409AE92b87eD442f`
- Is TRX address `TNfK1r5jb8Wa1Ph1MApjqJobsY8SPwj3Yh` safe? Any money laundering history?
- What's the risk score for transaction `0xabc123...`? Does it involve any sanctioned entities?

### Full Address Investigation

- Run a complete on-chain investigation on `0x6487B5006904f3Db3C4a3654409AE92b87eD442f` - labels, balance, risk score, platform interactions, and counterparties
- Where did the funds in BTC address `1A1zP1eP5QGefi2DMPTfTL5SLmv7Divf` come from and go to?
- Analyze the behavior of `0xd90e2f925da726b50c4ed8d0fb90ad053324f31b` - is it mostly interacting with DEXes, mixers, or exchanges?

### Account Multisig Information Check

- Help me check whether this ETH address `0x849D52316331967b6fF1198e5E32A0eB168D039d` is a multisig address
- Whether this TRX address `TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW` is a multisig address
- Whether this BTC address `3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy` is a multisig address

### Pre-Transfer Security Check

> Works with **Bitget Wallet Skill** / **Trust Wallet Skills** / **Binance Skills** / **OKX Agent Skills**,  automatically checks the recipient address before any transfer

- Swap my 0.1 ETH to USDT and send to `0x6487B5006904f3Db3C4a3654409AE92b87eD442f` (auto-checks recipient risk)
- Send 100 TRX to `TNfK1r5jb8Wa1Ph1MApjqJobsY8SPwj3Yh`
- Bridge 500 USDT from BNB Chain to `0x28C6c06298d514Db089934071355E5743bf21d60`

### Transaction Tracing

- Trace where funds from `0x6487B5006904f3Db3C4a3654409AE92b87eD442f` went - focus on outgoing transfers
- Has this address ever interacted with Tornado Cash, directly or indirectly?
- Show me the main counterparties for `TNfK1r5jb8Wa1Ph1MApjqJobsY8SPwj3Yh` - where did most funds originate?

### Status & Support

- Does MistTrack support USDT on Solana?
- List all tokens currently supported by MistTrack

## Supported APIs

| Endpoint | Description |
|----------|-------------|
| `v1/status` | API status & supported token list |
| `v1/address_labels` | Address labels (entity name, type) |
| `v1/address_overview` | Address balance & statistics |
| `v2/risk_score` | Address / tx risk score (sync) |
| `v2/risk_score_create_task` | Create risk score task (async) |
| `v2/risk_score_query_task` | Query task result (async, no rate limit) |
| `v1/transactions_investigation` | Transaction flow analysis (in/out) |
| `v1/address_action` | Behavior analysis (DEX/Exchange/Mixer ratio) |
| `v1/address_trace` | Address profile (platforms, events, relations) |
| `v1/address_counterparty` | Counterparty analysis |

## Supported Blockchains

Bitcoin, Ethereum, TRON, BNB Smart Chain, Polygon, Arbitrum, Optimism, Base, Avalanche, zkSync Era, Toncoin, Solana, Litecoin, Dogecoin, Bitcoin Cash, Merlin Chain, HashKey Chain, Sui, IoTeX

## Quick Start

1. Log in to the [MistTrack Dashboard](https://dashboard.misttrack.io/upgrade) using email verification code, then subscribe to the Standard Plan (new users can choose the limited-time trial plan for $10). After payment, you can [create an API Key](https://dashboard.misttrack.io/apikeys)
2. Set the environment variable (recommended):
   ```bash
   export MISTTRACK_API_KEY=your_api_key_here
   ```
3. See `SKILL.md` for full API documentation
4. See `scripts/` for example scripts

## Example Scripts

```bash
export MISTTRACK_API_KEY=your_api_key_here

# Single address risk score
python scripts/risk_check.py --address 0x... --coin ETH

# Batch async risk scoring
python scripts/batch_risk_check.py --input addresses.txt --coin ETH

# Full address investigation
python scripts/address_investigation.py --address 0x... --coin ETH

# Pre-transfer security check
python scripts/transfer_security_check.py --address 0x... --chain eth

# ETH multisig check
python3 scripts/multisig_analysis.py --address 0x... --chain eth

```

## x402 Payment (Pay-per-use)

If you do not have a MistTrack API Key, you can use the x402 payment protocol to pay per API call. We currently support EVM (EIP-3009) payments using USDC.

```bash
# One-time setup: store key in a permission-restricted file
echo "your_hex_private_key" > ~/.x402_key
chmod 600 ~/.x402_key

# Example: Pay-per-use via CLI
python3 scripts/pay.py pay \
  --url https://openapi.misttrack.io/x402/address_labels?address=0x... \
  --key-file ~/.x402_key \
  --chain-id 8453
```

## API Rate Limits

| Plan | Rate | Daily Limit |
|------|------|-------------|
| Standard | 1 req/sec | 10,000/day |
| Compliance | 5 req/sec | 50,000/day |
| Enterprise | Unlimited | Unlimited |

## Compatible Platforms

### Recommended Tools

| Platform                | Type              | How to Use |
|-------------------------|-------------------|------------|
| OpenClaw               | Native Platform   | install skill from Clawhub |
| Claude Code            | CLI Agent         | Clone repo |
| Codex CLI              | CLI Agent         | Clone repo |
| Crush                  | CLI Agent         | Clone repo |
| Cursor                 | IDE Agent         | Clone into project |
| Windsurf               | IDE Agent         | Clone into project |
| Cline                  | VS Code Agent     | Clone into project |
| Dify                   | Workflow Platform | Use as Code node or external API Tool |
| LangChain / CrewAI     | Frameworks        | Wrap `misttrack-skills` as a Tool |

## Documentation

- [Full API Docs](./SKILL.md)
- [MistTrack Official Docs](https://docs.misttrack.io/)
- [Common Error Messages](https://docs.misttrack.io/support/common-error-messages)

---
