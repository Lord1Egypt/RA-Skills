# Solana Meme Token Analyzer

Analyze Solana meme token risk in seconds. Detects insider wallets (老鼠仓), measures
top-holder concentration, and gives a clear risk rating for any token CA.

## What it does

- Fetches real-time price and liquidity from **DexScreener**
- Scans the **20 largest token holders** on-chain
- Identifies **insider wallets** (wallets holding large token amounts but almost no SOL — a classic pre-mine pattern)
- Calculates **top-10 concentration %** — high % means a few wallets can dump at any time
- Outputs a **risk level**: LOW / MEDIUM / HIGH / EXTREME

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
python3 scripts/psdm.py <TOKEN_CA>

# With JSON output (for automation/agents)
python3 scripts/psdm.py <TOKEN_CA> --json
```

## Optional: Helius API Key

Public Solana RPC nodes often reject requests for popular tokens. A free Helius key fixes this:

1. Sign up at https://helius.xyz/ (free, no credit card)
2. Copy your API key
3. Set it: `export HELIUS_API_KEY=your_key_here`

## Sample Output

```
=== Solana Meme Token Analyzer ===
Token: $PEPE | Price: $0.00001234 | Liquidity: $85,000
LP Address: 7xKXtg2CW...

正在分析前 20 大户...

+------+-------------+--------+--------------------------------+
| 排名 | 地址        | 占比   | 分析结果                       |
+------+-------------+--------+--------------------------------+
|    1 | AbCd...XyZw | 15.20% | ⚠️ 疑似老鼠仓 (SOL:0.001)     |
|    2 | Efgh...Mnop | 12.50% | LP 池子                        |
|    3 | Qrst...Uvwx | 8.30%  | SOL: 2.45                      |
+------+-------------+--------+--------------------------------+

📊 PEPE 风险简报:
⚠️ 发现 1 个疑似老鼠仓
前10名潜在控盘率: 38.50%
🚨 高度控盘预警！庄家随时可能砸盘。
```

## Paid API

A hosted version is available as a pay-per-request API ($0.02 USDC via x402 on Base chain):

```
https://solana-meme-analyzer-production.up.railway.app/analyze?ca=<TOKEN_CA>
```

No API key or subscription needed — just pay per request.

## Use as an OpenClaw Skill

Install via the OpenClaw CLI:

```bash
npx playbooks add skill openclaw/skills --skill solana-meme-analyzer
```

Or install manually by copying the `SKILL.md` into your skills directory.

## License

MIT
