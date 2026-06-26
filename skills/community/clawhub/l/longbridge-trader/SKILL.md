---
name: longbridge-trader
description: 长桥交易助手。通过 longport Python SDK 帮助用户查询实时行情、K线、盘口，提交/修改/撤销订单，查看账户余额和持仓。当用户提到股票行情、买入、卖出、下单、持仓、账户余额、订单、K线、盘口、成交记录、现金流等与证券交易相关的操作时，必须使用此 skill。即使用户只是随口问「AAPL 多少钱」或「我账户里还有多少钱」也应触发。
---

# 长桥交易助手

通过 longport Python SDK 帮助用户完成港股、美股的行情查询和交易操作。

## 环境要求

- Python 包：`longport`（通过 `pip install longport` 安装）
- 环境变量（SDK 通过 `Config.from_env()` 自动读取）：
  - `LONGPORT_APP_KEY`
  - `LONGPORT_APP_SECRET`
  - `LONGPORT_ACCESS_TOKEN`

如果用户未配置环境变量，提示他们到 [长桥开放平台](https://open.longbridge.cn) 获取。

## 标的代码格式

所有标的使用 `{市场}.{代码}` 格式：

| 市场 | 前缀 | 示例 |
|------|------|------|
| 美股 | `US` | `US.AAPL`, `US.TSLA` |
| 港股 | `HK` | `HK.00700`, `HK.09988` |
| A股（沪） | `SH` | `SH.600519` |
| A股（深） | `SZ` | `SZ.000001` |

## 标的代码补全

用户经常省略市场前缀或直接用中文名称，需要自动补全为完整的 `{市场}.{代码}` 格式：

1. **纯英文字母**（如 `AAPL`、`TSLA`）→ 美股，补全为 `US.AAPL`
2. **5位数字**（如 `00700`、`09988`）→ 港股，补全为 `HK.00700`
3. **6位数字，6开头**（如 `600519`）→ 沪市，补全为 `SH.600519`
4. **6位数字，0/3开头**（如 `000001`、`300750`）→ 深市，补全为 `SZ.000001`
5. **中文名称**（如「腾讯」「苹果」「茅台」）→ 根据常识映射到对应标的代码；不确定时询问用户确认

## 安全规则

**下单、改单操作必须遵循以下流程：**

1. 先向用户展示完整的订单参数（标的、方向、类型、数量、价格）
2. 明确询问用户「确认下单吗？」
3. 收到用户确认后才执行

**禁止**：在没有用户明确确认的情况下执行任何买入/卖出/改单操作。查询类操作（行情、持仓、余额）无需确认，直接执行。

## 工作流程

根据用户意图选择对应工作流。所有代码通过 Bash 工具执行 `python3 -c "..."` 运行。

### 1. 查询行情

获取股票实时报价、K线、盘口等数据。

```python
from longport.openapi import QuoteContext, Config

config = Config.from_env()
ctx = QuoteContext(config)

# 实时行情
resp = ctx.quote(["US.AAPL"])
for q in resp:
    print(f"{q.symbol} 最新: {q.last_done} 涨跌: {q.change_rate}%")

# K线（最近 30 根日K）
from longport.openapi import Period, AdjustType
candles = ctx.candlesticks("US.AAPL", Period.Day, 30, AdjustType.ForwardAdjust)

# 盘口
depth = ctx.depth("US.AAPL")

# 分时
intraday = ctx.intraday("US.AAPL")
```

有关 QuoteContext 完整方法列表和参数说明，阅读 `references/quote-api.md`。

### 2. 交易操作

提交、修改、撤销订单。

```python
from longport.openapi import TradeContext, Config, OrderType, OrderSide, TimeInForceType, Decimal

config = Config.from_env()
ctx = TradeContext(config)

# 提交限价单：买入 100 股 AAPL，价格 150.00
resp = ctx.submit_order(
    symbol="US.AAPL",
    order_type=OrderType.LO,
    side=OrderSide.Buy,
    submitted_quantity=Decimal("100"),
    time_in_force=TimeInForceType.Day,
    submitted_price=Decimal("150.00"),
)
print(f"订单ID: {resp.order_id}")

# 修改订单
ctx.replace_order(order_id="xxx", quantity=Decimal("200"), price=Decimal("151.00"))

# 撤单
ctx.cancel_order(order_id="xxx")
```

有关 TradeContext 完整方法列表和参数说明，阅读 `references/trade-api.md`。

### 3. 资产查询

```python
from longport.openapi import TradeContext, Config

config = Config.from_env()
ctx = TradeContext(config)

# 账户余额
balances = ctx.account_balance()
for b in balances:
    print(f"币种: {b.currency} 净资产: {b.net_assets} 可用: {b.total_cash}")

# 持仓
positions = ctx.stock_positions()
for ch in positions.channels:
    for p in ch.positions:
        print(f"{p.symbol} 数量: {p.quantity} 可用: {p.available_quantity} 成本: {p.cost_price}")

# 今日订单
orders = ctx.today_orders()
for o in orders:
    print(f"[{o.status}] {o.symbol} {o.side} {o.quantity}@{o.price}")

# 今日成交
executions = ctx.today_executions()

# 历史订单
from datetime import datetime
history = ctx.history_orders(start_at=datetime(2024, 1, 1), end_at=datetime(2024, 12, 31))

# 现金流
flows = ctx.cash_flow(start_at=datetime(2024, 1, 1), end_at=datetime(2024, 12, 31))
```

### 4. 高级查询

```python
# 估算最大可买数量
from longport.openapi import OrderType, OrderSide, Decimal
resp = ctx.estimate_max_purchase_quantity(
    symbol="US.AAPL",
    order_type=OrderType.LO,
    side=OrderSide.Buy,
    price=Decimal("150.00"),
)
print(f"可买: {resp.cash_max_qty} 融资可买: {resp.margin_max_qty}")

# 保证金比率
ratio = ctx.margin_ratio("HK.00700")
print(f"初始: {ratio.im_factor} 维持: {ratio.mm_factor}")
```

## 常用订单类型

| 类型 | 枚举值 | 说明 | 适用市场 |
|------|--------|------|----------|
| 限价单 | `OrderType.LO` | 指定价格 | 港股/美股 |
| 市价单 | `OrderType.MO` | 市场价成交 | 港股/美股 |
| 增强限价单 | `OrderType.ELO` | 港股增强限价 | 港股 |
| 竞价限价单 | `OrderType.ALO` | 竞价时段 | 港股 |
| 触价限价单 | `OrderType.LIT` | 触发价+限价 | 美股 |
| 触价市价单 | `OrderType.MIT` | 触发价+市价 | 美股 |
| 跟踪止损限价（金额） | `OrderType.TSLPAMT` | 跟踪止损 | 美股 |
| 跟踪止损限价（百分比） | `OrderType.TSLPPCT` | 跟踪止损 | 美股 |
| 跟踪止损市价（金额） | `OrderType.TSMAMT` | 跟踪止损 | 美股 |
| 跟踪止损市价（百分比） | `OrderType.TSMPCT` | 跟踪止损 | 美股 |

## 输出格式

- 行情数据用表格展示，包含关键字段（价格、涨跌幅、成交量）
- 持仓数据按市场分组，显示盈亏
- 订单列表显示状态、方向、数量、价格
- 金额保留 2 位小数，百分比保留 2 位小数

## 错误处理

捕获 `OpenApiException` 并向用户展示清晰的错误信息：

```python
from longport.openapi import OpenApiException
try:
    # ... API 调用
except OpenApiException as e:
    print(f"API 错误: {e}")
```

常见错误：
- 环境变量未配置 → 提示用户设置
- 标的代码无效 → 检查格式是否为 `市场.代码`
- 权限不足 → 提示用户检查 API 权限
- 市场未开盘 → 告知交易时段
