> Follow the FORMAT ENFORCEMENT rules from SKILL.md. Output must match templates character-for-character.

# Report E — Daily Digest

Position overview + estimated yield + market snapshot in one report.

## E.1 — Fetch data

Positions: same as Report A step A.1, metrics via `references/domain.md` (MCP-based).

User vault deposits:
- MCP: `lista_get_dashboard({ wallet: "<address>" })` → use `vaults[]` (per-vault `assetsUsd`, `apy`, `emissionApy`)
- moolah.js: `node skills/lista/scripts/moolah.js dashboard <address>` → use `vaultDeposits[]` (same fields: `assetsUsd`, `apy`, `emissionApy`)

Protocol-level vault data (for Market Snapshot section):
```
lista_get_lending_vaults({ pageSize: 50, chain: "<chain>" })
```

**Vault fallback — moolah.js** (if MCP unavailable):
```bash
node skills/lista/scripts/moolah.js --chain <bsc|eth> vaults
```

Yield estimation:
- `supplyUSD` = user's `assetsUsd` per vault (from dashboard, NOT protocol TVL)
- `vaultAPY` = `apy + emissionApy` from the same vault record
- `estimatedDailyYield = supplyUSD × vaultAPY / 365` per vault
- `estimatedWeeklyYield = estimatedDailyYield × 7`

Claimable rewards:
```
lista_get_rewards({ wallet: "<address>" })
```
Returns claimable rewards across all sources (LISTA emission, bribe, distributor). Show non-zero reward lines only.

**Rewards fallback — moolah.js** (if MCP unavailable):
```bash
node skills/lista/scripts/moolah.js rewards <address>
```
Returns JSON with `rewards[]` (each: `source`, `amount`, `symbol`, `usd`) and `totalUsd`.

Market snapshot rate deltas:
- If previous rate data is available (e.g. from a prior run), show change indicators: ↑, ↓, or "unchanged" / "持平"
- If no previous data, omit the delta parenthetical

## E.2 — Output template

⛔ STOP BEFORE OUTPUTTING. You MUST copy the template below character-for-character. Substitute `<placeholder>` values with real data. Change NOTHING else — no bullet points, no overview section, no preamble, no trailing remarks. Your response must start with the exact first line shown in the template.

### English

```
📊 Lista Daily Digest · <YYYY-MM-DD>
Wallet: 0xAbCd...5678
━━━━━━━━━━━━━━━━━━━━━━━━━

🏦 Lending Positions
─────────────────────

- - - - -

#1 BTCB / U
Collateral: 2.50 BTCB (~＄250,000)
Borrowed: 100,000.00 U (~＄100,000)
LTV: 40.0% / LLTV: 86.0%
LTV gap: 46.0%
Liq. price: ＄46,511 / BTCB (current: ＄100,000)

- - - - -

─────────────────────

💰 Yield Summary
WBNB Vault: ~＄2.31/day (12.4% APY on ＄6,800 supply)
USD1 Vault: ~＄0.87/day (5.6% APY on ＄5,670 supply)
Daily total: ~＄3.18 | Weekly: ~＄22.26

─────────────────────

🎁 Claimable Rewards
LISTA emission: 12.5 LISTA (~＄3.80)
Bribe rewards: 0.02 BNB (~＄12.40)
Total claimable: ~＄16.20

─────────────────────

📈 Market Snapshot
USDT borrow rate: 8.2% (↑0.3%)
WBNB Vault APY: 12.4% (unchanged)
USD1 Vault APY: 5.6% (↓0.2%)

━━━━━━━━━━━━━━━━━━━━━━━━━

Data: <DATA_SOURCE> | <NETWORK>
```

If risk alerts exist, add before closing ━━━. Use two tiers:
- HF < 1.2 but above alert threshold → ⚠️ yellow warning
- At or below alert threshold → 🔴 red alert

```
─────────────────────

⚠️ Risk Alerts
#2 slisBNB / WBNB — HF: 1.15 ⚠️ LTV gap: 4.2%
Consider adding collateral or repaying ~0.5 WBNB.

🔴 Critical
#3 ETH / USDT — HF: 1.004 🔴 LTV gap: 0.4%
Repay debt or add collateral immediately.
```

### 繁體中文

```
📊 Lista 每日報告 · <YYYY-MM-DD>
錢包：0xAbCd...5678
━━━━━━━━━━━━━━━━━━━━━━━━━

🏦 借貸持倉
─────────────────────

- - - - -

#1 BTCB / U
抵押品：2.50 BTCB（約 ＄250,000）
已借出：100,000.00 U（約 ＄100,000）
LTV：40.0% / 清算線：86.0%
LTV 差距：46.0%
清算價格：＄46,511 / BTCB（當前價：＄100,000）

- - - - -

─────────────────────

💰 收益匯總
WBNB 金庫：約 ＄2.31/日（12.4% 年化，供款 ＄6,800）
USD1 金庫：約 ＄0.87/日（5.6% 年化，供款 ＄5,670）
每日合計：約 ＄3.18 | 每週：約 ＄22.26

─────────────────────

🎁 可領取獎勵
LISTA 排放：12.5 LISTA（約 ＄3.80）
賄賂獎勵：0.02 BNB（約 ＄12.40）
可領取合計：約 ＄16.20

─────────────────────

📈 市場快訊
USDT 借款利率：8.2%（↑0.3%）
WBNB 金庫年化：12.4%（持平）
USD1 金庫年化：5.6%（↓0.2%）

━━━━━━━━━━━━━━━━━━━━━━━━━

資料來源：<DATA_SOURCE> | <NETWORK>
```

For weekly: replace "Daily Digest" / "每日報告" with "Weekly Digest" / "每週報告". Show weekly yield estimates instead of daily.

## E.3 — Subscription setup

If user says "subscribe to daily" / "訂閱日報" / "订阅日报" or "subscribe to weekly" / "訂閱週報" / "订阅周报":

> **EN:** Which channel? 1) Telegram  2) Discord
> **中文：** 推送渠道？1) Telegram  2) Discord

After channel is selected:

> **EN (daily):** Done. Daily reports will be delivered at 08:00 UTC via [channel].
> **EN (weekly):** Done. Weekly reports will be delivered every Monday at 08:00 UTC via [channel].
> **中文（日報）：** 已設置。每日報告將於 08:00 UTC 透過 [渠道] 發送。
> **中文（週報）：** 已設置。每週報告將於每週一 08:00 UTC 透過 [渠道] 發送。

If user says "cancel subscription" / "unsubscribe" / "取消推送" / "取消訂閱" / "取消订阅":

> **EN:** Subscription cancelled. You can re-subscribe anytime.
> **中文：** 已取消訂閱。隨時可重新訂閱。
