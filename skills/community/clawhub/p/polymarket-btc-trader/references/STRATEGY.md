# Polymarket BTC 5m Bot 策略详解

## 市场结构

 Polymarket 的 BTC Up/Down 市场每 5 分钟一个盘口，格式为 `btc-updown-5m-{unix_timestamp}`。

- **到期时间**：每个整点后 5 分钟的窗口（如 7:00-7:05AM ET）
- **结算价格**：Binance BTC/USD 在窗口结束时的价格 vs 开盘时
- **UP 结局**：BTC 上涨 → UP token = $1，DOWN = $0
- **DOWN 结局**：BTC 下跌 → DOWN token = $1，UP = $0

## 双信号决策系统

Bot 同时运行两套独立的信号系统，**必须两者都同意才开仓**。

### 信号 1：AI 决策（MiniMax）

每 30 秒调用一次 MiniMax，输入：
- BTC 当前价格、24h 高低点、日内变化
- 15 分钟 K 线形态（趋势/震荡）
- 3 分钟成交量变化
- 当前持仓状态和浮盈

输出：`BUY_UP` / `BUY_DOWN` / `HOLD`

### 信号 2：价差套利策略

公式：
```
BTC_5m_change = (BTC当前 - BTC_5min前) / BTC_5min前
signal = BTC_5m_change * 10   # 放大 10 倍
price_gap = PM_UP_price - 0.5  # PM 定价相对 50-50 的偏离
divergence = signal - price_gap
```

条件：
- `divergence > 0.003` → 买入 UP（BTC 涨势被低估）
- `divergence < -0.003` → 买入 DOWN（BTC 跌势被低估）

### 双重确认（HOLD 条件）

以下任一条件成立则不开仓：
- AI 信号 = HOLD
- 策略信号 < 0.003 且 > -0.003（无明显偏离）
- 当前已有持仓（max 1 单）
- 剩余时间 < 3 分钟
- ask > 0.60 或 spread > 0.06

## 入场规则

```
1. 扫描未来 8 个 5m 盘口
2. 过滤条件：
   - 剩余时间 ≥ 3 分钟
   - spread ≤ 0.06
   - 顶档 bid_size ≥ 25 shares
   - ask 价格在 0.15-0.60 区间
3. 等待 AI + 策略双重 BUY 信号
4. 以 ask 价买入 $10 仓位
```

## 出场规则

**主动止盈（提前平仓）**：
- best_bid 浮盈 > $1.00 → 立即以 bid 价卖出

**被动止损**：
- 剩余时间 = 0 → 等到期结算（不支持主动止损）

**到期结算**：
- 剩余时间 = 0 时，自动以 mark_price 卖出

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| PAPER_BET_AMOUNT | $10 | 单仓金额 |
| PAPER_MIN_ENTRY_PRICE | 0.15 | 最低入场价格 |
| PAPER_MAX_ENTRY_PRICE | 0.60 | 最高入场价格 |
| PAPER_MAX_SPREAD | 0.06 | 最大点差 |
| PAPER_MIN_TOP_BOOK_SIZE | 25 | 最低 bid 深度 |
| PAPER_MIN_MINUTES_TO_EXPIRY | 3 | 最低剩余时间 |
| PAPER_TAKE_PROFIT_USD | $1.00 | 止盈阈值 |
| PAPER_MAX_OPEN_POSITIONS | 1 | 最大持仓数 |
| AI_DECISION_INTERVAL_SECONDS | 30 | AI 决策间隔 |
| PAPER_POLL_INTERVAL_SECONDS | 15 | 主循环间隔 |

## 风险控制

1. **同时最多 1 单**：避免过度交易
2. **资金上限 $100 → $10/单**：即使全输也剩 $90
3. **点差保护**：spread > 6% 不交易（避免滑点）
4. **深度保护**：bid_size < 25 不交易（防止卖不掉）
5. **价格保护**：ask > 0.60 不追高，ask < 0.15 不贪便宜
