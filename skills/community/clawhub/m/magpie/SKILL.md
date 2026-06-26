---
name: magpie
description: Query A-share (Chinese stock market) quotes, fund flows, K-lines, watchlist, alert rules, and 龙虎榜 via the local magpie daemon. Use when the user asks about a stock by code or name, wants to set/list/remove price alerts, asks for today's resource fund flow, requests a morning/evening/weekly portfolio digest, queries 龙虎榜 (top billboard), or asks "what's <stock> doing now". DO NOT use for US stocks, HK stocks, crypto, technical analysis (MA/MACD), order execution, or news/sentiment — magpie is v1 A-share monitoring only.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [], "endpoints": ["http://127.0.0.1:17891/api/v1/health"] }
      }
  }
---

# magpie — A-share quote & alert agent skill

> 🐦 magpie is a **local daemon** at `http://127.0.0.1:17891` exposing a tiny HTTP API. This skill teaches you how to call it. The daemon must already be running — if `/health` fails, tell the user to `magpie start`.

## When to activate

- "茅台现在多少" / "查 600519" / "海康威视" → quote lookup
- "今天主力资金流向" / "X 股票主力流入多少" → fund flow
- "给 600519 设个 1500 突破告警" / "茅台跌破 1300 提醒我" → add alert
- "看看我自选股" / "我加了哪些股" → watchlist
- "今天龙虎榜" / "谁上龙虎榜了" → lhb
- "早盘要点" / "收盘复盘" / "周报" → digest
- "今天我的盘怎么样" → digest evening
- "K 线" / "最近 X 天怎么样" → kline

## Don't activate

- 美股 / 港股 / 加密币（v1 不支持）
- 选股策略 / 技术分析 / 买卖建议（magpie 是监控工具，**非投资建议**）
- 写策略 / 回测 / 下单
- 新闻 / 公告 / 财报数据

## Health check first

Always check `/health` before issuing requests. If down:

```bash
curl -s http://127.0.0.1:17891/api/v1/health
```

If non-200 / connection refused, tell user:
> "magpie daemon 没启动，请运行 `cd /Volumes/DevDisk/symbol/magpie && node dist/cli.js start`（或如果已安装 npm 包，`magpie start`）。"

## HTTP API reference

Base URL: `http://127.0.0.1:17891`

### Quotes

```bash
# Single
curl -s "http://127.0.0.1:17891/api/v1/quote/600519"

# Batch
curl -s "http://127.0.0.1:17891/api/v1/quotes?codes=600519,000858,002594"
```

Response shape:
```json
{
  "ok": true,
  "quote": {
    "code": "600519", "name": "贵州茅台",
    "price": 1344.09, "change": -10.46, "changePct": -0.77,
    "open": 1354.5, "prevClose": 1354.55,
    "high": 1358.6, "low": 1338,
    "volume": 5696787, "turnover": 7653257144,
    "source": "sina", "delaySec": 5
  }
}
```

**Stock code rules:**
- 6 digits, no prefix needed — `600519` not `sh600519`
- 上海: 6xxxxx / 9xxxxx
- 深圳: 0xxxxx / 3xxxxx
- 北交所: 8xxxxx / 4xxxxx

**If user gave a stock name**, you need to know the code. Try this order:
1. **Reverse-lookup the watchlist first** — `GET /watchlist` to see if user already added it (matches by `name` substring)
2. Use the common-stock table below
3. If still unknown, **ask the user for the 6-digit code**, don't guess

Common Chinese A-share stocks (verified):
- 贵州茅台 600519 / 五粮液 000858 / 泸州老窖 000568 / 山西汾酒 600809
- 比亚迪 002594 / 宁德时代 300750 / 長城汽车 601633
- 中国平安 601318 / 招商银行 600036 / 平安银行 000001 / 工商银行 601398
- 海康威视 002415 / 美的集团 000333 / 万科A 000002 / 中国中车 601766
- 海尔智家 600690 / 隆基绿能 601012 / 长江电力 600900
- 世纪华通 002602 / 京东方 A 000725 / 洁美科技 002859 / 巨人网络 002558

**Ambiguous abbreviations — always ask the user to clarify**:
- “平安” → 中国平安 (601318) or 平安银行 (000001)?
- “招行 / 招商” → 招商银行 (600036) 是常规映射但确认一句更稳
- “万科” → 万科A (000002) vs 万科企业 (000540) etc.

If in doubt, ask: "你指的是哪个股票？请给 6 位代码。"

> **Note**: stock names from sina data source occasionally arrive with full/half-width spaces (e.g. `五 粮 液`). magpie v0.0.3+ trims these in the server. If you ever see one, just trim before rendering.

### Fund flow（资金流）

```bash
curl -s "http://127.0.0.1:17891/api/v1/flow/600519"
```

Units are **CNY (元)**. Divide by 1e8 for 亿. **Negative = 净流出，positive = 净流入**.

Fields: `mainNetIn` (主力), `superNetIn` (超大单), `bigNetIn` (大单), `midNetIn` (中单), `smallNetIn` (小单).

**Rendering rule** (do not parrot negative numbers):
- value `< 0` → `净流出 ¥{abs(v/1e8).toFixed(2)} 亿`
- value `> 0` → `净流入 ¥{(v/1e8).toFixed(2)} 亿`
- value `0` → `持平`

`delaySec` is usually 60s for flow (vs 5s for quote). If user is asking real-time, add a hint: "_资金流数据延迟~1min、以交所清算为准_".

### K-line（K线）

```bash
curl -s "http://127.0.0.1:17891/api/v1/kline/600519?period=daily&days=30"
```

`period` ∈ `daily|weekly|monthly`. Default 30 rows. Rows have `date, open, close, high, low, volume, turnover, changePct, change, turnoverRate`.

### 龙虎榜 lhb

```bash
curl -s "http://127.0.0.1:17891/api/v1/lhb"                      # today
curl -s "http://127.0.0.1:17891/api/v1/lhb?date=2026-05-13"      # specific date
```

Returns up to 50 rows. After 18:00 SH local is most reliable.

### Watchlist

```bash
# List
curl -s "http://127.0.0.1:17891/api/v1/watchlist"

# Add
curl -s -X POST -H "content-type: application/json" \
  -d '{"code":"600519","name":"贵州茅台","group":"持仓","note":"长持"}' \
  http://127.0.0.1:17891/api/v1/watchlist

# Remove
curl -s -X DELETE "http://127.0.0.1:17891/api/v1/watchlist/600519"
```

### Alert rules

```bash
# List
curl -s "http://127.0.0.1:17891/api/v1/alerts"
curl -s "http://127.0.0.1:17891/api/v1/alerts?code=600519"

# Add
curl -s -X POST -H "content-type: application/json" \
  -d '{"code":"600519","type":"lte","threshold":1300,"note":"抄底位"}' \
  http://127.0.0.1:17891/api/v1/alerts

# Disable
curl -s -X DELETE "http://127.0.0.1:17891/api/v1/alerts/1"

# History
curl -s "http://127.0.0.1:17891/api/v1/alerts/history?days=7"
```

**Rule types:**
| type | trigger | typical use |
|---|---|---|
| `gte` | price ≥ threshold | take-profit / breakout-watch |
| `lte` | price ≤ threshold | stop-loss / buy-the-dip |
| `breakout` | price ≥ threshold AND prevClose < threshold | 突破阻力 |
| `breakdown` | price ≤ threshold AND prevClose > threshold | 跌破支撑 |

Default cooldown: 30 min (same rule won't re-fire within 30min).

### Digest

```bash
curl -s "http://127.0.0.1:17891/api/v1/digest?type=morning"
curl -s "http://127.0.0.1:17891/api/v1/digest?type=evening"   # includes fund flow
curl -s "http://127.0.0.1:17891/api/v1/digest?type=weekly"    # 5-day change
```

Response has `digest.markdown` you can directly forward to the user.

## How to respond to common asks

### "查 X" / "X 现在多少"
1. Map name → 6-digit code (or ask)
2. `GET /quote/<code>`
3. Reply concise: `贵州茅台 600519: ¥1344.09 📉 -0.77% (今高 ¥1358.6 / 今低 ¥1338)`
4. If `delaySec` > 30 add: "_数据延迟 Xs_"

### "X 资金流"
1. `GET /flow/<code>`
2. Convert to 亿元 (`/1e8`), highlight `mainNetIn`. **Negative → say "净流出"，不要写负号。**
3. **Default report**: `main` + `super` 两项足够。
   - Concise: `茅台 600519 主力净流出 ¥11.78 亿（超大单净流出 ¥11.55 亿）`
4. “详细” / “全部” 才担 mid/small：`· 大单 -0.23 亿 · 中单 +11.78 亿 · 小单 -0.003 亿`

### "给 X 设个 ¥N 告警"
1. Determine type:
   - 跌破/止损 → `lte` (价格简单 ≤) or `breakdown` (需 prevClose > threshold)
   - 突破/止盈 → `gte` (价格简单 ≥) or `breakout` (需 prevClose < threshold)
2. `POST /alerts` with `{code, type, threshold, note}`
3. **Confirm template by type** (don't free-style):
   - `gte`       → `✓ 规则 #N 已添加：{name} ({code}) 涨到 ¥{th} ping 你`
   - `lte`       → `✓ 规则 #N 已添加：{name} ({code}) 跌到 ¥{th} ping 你`
   - `breakout`  → `✓ 规则 #N 已添加：{name} ({code}) 突破 ¥{th} ping 你`
   - `breakdown` → `✓ 规则 #N 已添加：{name} ({code}) 跌破 ¥{th} ping 你`
4. **Distance hint** (optional but nice): if current price differs from threshold by >5%, append `（当前 ¥{p}，距阈值 {+±X%}）`

### "今天我的盘"
1. `GET /digest?type=evening` (after 15:00) or `morning` (before 09:30)
2. Return the `digest.markdown` verbatim — already formatted nicely

### "今天龙虎榜"
1. `GET /lhb` (after 18:00 SH for stable data)
2. Summarize top 3-5 with reasons, don't dump all 50

## Market phase semantics (from `/health`)

| phase | meaning | what to tell user |
|---|---|---|
| `pre` | 盘前 00:00-09:30 | “今日未开盘，显示是上一交易日收盘” |
| `morning` | 上午 09:30-11:30 | “盘中，数据实时” |
| `lunch` | 午休12 11:30-13:00 | “午间休市” |
| `afternoon` | 下午 13:00-15:00 | “盘中，数据实时” |
| `post` | 盘后 15:00-24:00 | “今日已收盘” |
| `closed` | 节假日或周末 | “非交易日，上一交易日收盘数据” |

**Unknown phase value** → fall back to "`closed`" handling.

## Output style

- **Numbers**: prices always with `¥` prefix and 2 decimals; percentages with sign and 2 decimals
- **Direction emoji**: 📈 涨 / 📉 跌 / ➖ 平
- **Brevity**: a single line per stock unless user asks for detail
- **Disclaimer**: 不要给买卖建议；如果用户问"该买吗"，回答"magpie 只看数据，不建议买卖决策"

## Failure modes

| Error | What to say |
|---|---|
| `not_found` in quote | "代码 XXXXXX 找不到，是不是写错了？" |
| `/flow` returns error | "Eastmoney 接口抽风，等 1 分钟重试，或者用 `/quote` 看价格" |
| connect refused | "magpie 没启动，请 `magpie start`" |
| empty lhb | "今天龙虎榜数据还没出，通常 18:00 后才稳" |
| Non-trading day | 健康响应里 `phase: closed`，告诉用户："今天非交易日，行情是上一交易日收盘数据" |

## Trigger words (Chinese)

盯盘 / 自选股 / 查股 / 股价 / 资金流 / 主力 / 龙虎榜 / 涨跌 / 早盘 / 收盘 / 茅台 / 五粮液 / 比亚迪 / 招行 / 平安 / K线 / 突破 / 跌破 / 止损 / 止盈 / 设告警 / 提醒我 / 我的盘
