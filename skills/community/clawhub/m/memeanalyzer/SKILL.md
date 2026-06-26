---
name: solana-meme-analyzer
description: |
  Analyze Solana meme token (CA) risk by scanning holder distribution, detecting insider
  wallets (老鼠仓/rat warehouse), and evaluating top-holder concentration.
  Use when the user wants to analyze a Solana token contract address, check for rugs,
  detect insiders, evaluate meme coin safety, check holder concentration, or assess
  if a token is likely to be dumped. Keywords: CA分析, 老鼠仓, 控盘, 持仓分析, Solana token risk.
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    env: ["HELIUS_API_KEY"]
    primaryEnv: "HELIUS_API_KEY"
---

# Solana Meme Token Analyzer

Detects insider wallets and concentration risk for Solana meme tokens using on-chain data
from DexScreener and Solana RPC nodes. Works without API keys (using public RPC), but
a free Helius API key dramatically improves reliability.

## Paid API (Recommended for Agent Use)

A hosted version of this skill is available as a pay-per-request API via x402 micropayments.
No setup required — just call the endpoint and pay $0.02 USDC per analysis.

```bash
# Check payment requirements
npx awal@latest x402 details https://solana-meme-analyzer-production.up.railway.app/analyze?ca=TOKEN_CA

# Make a paid request (auto-pays from your wallet)
npx awal@latest x402 pay "https://solana-meme-analyzer-production.up.railway.app/analyze?ca=TOKEN_CA"
```

Payment is settled instantly on Base chain. No API keys or subscriptions needed.

---

## Self-Hosted Setup

### Prerequisites

Install Python dependencies from the skill directory:

```bash
pip install -r {baseDir}/requirements.txt
```

Optional but recommended — set your Helius API key for stable RPC access:

```bash
export HELIUS_API_KEY=your_key_here
```

Get a free key at https://helius.xyz/ (no credit card required).

## Usage

### Basic analysis (interactive)

```bash
python3 {baseDir}/scripts/psdm.py
```

Then paste the token CA when prompted.

### Analysis with a CA argument

```bash
python3 {baseDir}/scripts/psdm.py <TOKEN_CA>
```

### Analysis with JSON output (for agent use)

```bash
python3 {baseDir}/scripts/psdm.py <TOKEN_CA> --json
```

## Output Explained

### Table columns

| Column | Meaning |
|--------|---------|
| 排名 | Rank by holdings |
| 地址 | Wallet address (truncated) |
| 占比 | % of total supply held |
| 分析结果 | Classification (see below) |

### Wallet classifications

| Label | Meaning | Risk |
|-------|---------|------|
| `LP 池子` | Liquidity pool contract | Normal |
| `⚠️ 疑似老鼠仓` | Holds many tokens but very little SOL (<0.05 SOL) — classic insider pre-mine pattern | High |
| `🐋 巨鲸/交易所` | Large SOL balance (>500 SOL) — likely whale or exchange | Low |
| `SOL: X.XX` | Regular wallet with displayed SOL balance | Normal |
| `普通大户` | Unable to fetch SOL balance | Unknown |

### Risk levels (JSON output)

| Level | Meaning |
|-------|---------|
| `LOW` | No red flags, healthy distribution |
| `MEDIUM` | Top 10 hold 30–50% — some concentration |
| `HIGH` | Insider wallets detected OR top 10 > 30% |
| `EXTREME` | Top 10 hold > 50% — severe dump risk |

## JSON Output Format

When `--json` is passed, structured data is printed after the table:

```json
{
  "token": {
    "symbol": "PEPE",
    "price_usd": "0.00001234",
    "liquidity_usd": 85000
  },
  "risk_level": "HIGH",
  "top10_concentration": 38.5,
  "suspicious_insider_count": 2,
  "warnings": [
    "发现 2 个疑似老鼠仓 (持币多但没钱)",
    "高度控盘！前10名持有 38.5%"
  ],
  "holders": [
    {
      "rank": 1,
      "address": "AbCd...XyZw",
      "percent": 12.3,
      "tag": "疑似老鼠仓 (SOL:0.001)",
      "sol_balance": 0.001
    }
  ]
}
```

## Examples

### Check a token for rug risk

```bash
python3 {baseDir}/scripts/psdm.py EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

### Get machine-readable output

```bash
python3 {baseDir}/scripts/psdm.py EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --json
```

### With a Helius key for best results

```bash
HELIUS_API_KEY=your_key python3 {baseDir}/scripts/psdm.py <TOKEN_CA> --json
```

## Interpreting Results

**When to AVOID a token:**
- `suspicious_insider_count` > 0 (insider wallets present)
- `top10_concentration` > 40% (too centralized)
- `risk_level` is `HIGH` or `EXTREME`

**Reasonably safe signals:**
- LP pool is the largest holder
- `top10_concentration` < 25%
- No `⚠️ 疑似老鼠仓` entries
- risk_level is `LOW`

## Agent Usage Notes

- Always use `--json` flag for programmatic access to structured data
- The script auto-rotates through multiple RPC nodes on 429 rate-limit errors
- Without `HELIUS_API_KEY`, large/popular tokens may fail on `getTokenLargestAccounts`
- Analysis of ~12 wallets takes 5–15 seconds due to per-wallet RPC calls

## Troubleshooting

**"无法获取持仓" error:**
Set `HELIUS_API_KEY` — public RPC nodes reject this call for tokens with many holders.

**Slow analysis:**
Normal. The script checks each wallet's SOL balance individually to detect insiders.

**"DexScreener 未找到数据":**
The token CA is invalid, or the token is too new (<5 min old) to be indexed.
