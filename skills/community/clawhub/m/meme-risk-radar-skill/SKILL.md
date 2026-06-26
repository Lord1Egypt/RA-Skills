---
name: meme-risk-radar-skill
description: Bilingual meme token risk radar for Binance Web3 data. Scan newly launched or fast-rising meme tokens from Meme Rush, enrich with token audit and token info, produce a normalized risk report in Chinese or English, and support SkillPay billing hooks for paid scan and audit calls.
---

# Skill: meme-risk-radar-skill

## Purpose
Use this skill to turn Binance Web3 meme discovery data into a tradable risk workflow.
It is designed for users who want fast meme coverage, but need structured filtering before deciding whether to research further.

Default output supports both `zh` and `en`.

## Product Positioning
- Built for traders, researchers, alpha groups, and content operators who need faster meme token triage.
- Focus on `risk-first discovery`: find candidates first, then downgrade obvious traps before deeper research.
- Suitable for ClawHub-style paid usage because value is tied to each actionable scan, not to raw static content.

## Trust Posture
- Read-only by default. This skill does not place orders or request exchange trading keys.
- Secrets are read only from environment variables and are never hard-coded.
- Output is explainable: every score is backed by visible signals such as holder concentration, dev share, liquidity, audit hits, and tax flags.
- User-facing language must remain neutral. Never promise profits or "safe coins."

## Commands
Run from the skill root:

```bash
python3 scripts/meme_risk_radar.py scan --chain solana --stage new --limit 10 --lang zh
python3 scripts/meme_risk_radar.py scan --chain bsc --stage finalizing --limit 5 --lang en --min-liquidity 10000
python3 scripts/meme_risk_radar.py audit --chain bsc --contract 0x1234... --lang en
python3 scripts/meme_risk_radar.py health
```

## Output Contract
Each scan returns:
- `chain`
- `stage`
- `lang`
- `generated_at_utc`
- `tokens[]`

Each token entry contains:
- `symbol`
- `name`
- `contract_address`
- `score`
- `risk_level`
- `summary`
- `signals[]`
- `metrics`
- `audit`
- `links`

## Billing Hook (SkillPay)
- Bill only `scan` and `audit`.
- Read API key from `SKILLPAY_APIKEY`.
- Default price is read from `SKILLPAY_PRICE_USDT` (default `0.002`).
- Do not hard-code secrets.

## Suggested Monetization
- Entry offer: charge per `scan` and per `audit`, keep `health` free.
- Recommended starting price: `0.002 USDT` per call for public listing, then raise after usage data is stable.
- Best value narrative for users: "pay for a filtered shortlist, not for raw token noise."
- If later adding premium tiers, gate advanced filters, watchlists, exports, or alert delivery instead of the base explanation output.

## Required/Useful Env Vars
- `SKILLPAY_APIKEY` (required for paid mode)
- `SKILLPAY_BASE_URL` (optional, default `https://skillpay.me`)
- `SKILLPAY_CHARGE_URL` (optional override)
- `SKILLPAY_CHARGE_PATH` (optional, default `/charges`)
- `SKILLPAY_USER_REF` (optional, default `anonymous`)
- `SKILLPAY_PRICE_USDT` (optional, default `0.002`)
- `SKILLPAY_BILLING_MODE` (optional, `skillpay` or `noop`)
- `BINANCE_WEB3_BASE_URL` (optional, default `https://web3.binance.com`)
- `BINANCE_HTTP_TIMEOUT_SEC` (optional, default `12`)

## Notes
- This skill is a risk-filtering tool, not an execution tool.
- `LOW` risk never means safe. The report is a point-in-time snapshot.
- Keep user-facing language neutral. Do not give trading guarantees or profit promises.
