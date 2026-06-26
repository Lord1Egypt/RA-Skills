# 数据对象字段速查

## Tick 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | str | 标的代码 |
| open | float | 日线开盘价 |
| high | float | 日线最高价 |
| low | float | 日线最低价 |
| price | float | 最新价（集合竞价成交前为 0） |
| cum_volume | long | 累计成交量 |
| cum_amount | float | 累计成交额 |
| last_volume | int | 瞬时成交量 |
| last_amount | float | 瞬时成交额 |
| quotes | list[dict] | 买卖盘口（股票5档，期货1档，L2行情10档） |
| created_at | datetime | 创建时间 |
| cum_position | int | 期货持仓量（股票为0） |
| trade_type | int | 交易类型（期货）：1=双开，2=双平，3=多开，4=空开... |
| iopv | float | 基金份额参考净值（仅基金） |

**quotes 单档结构**：
```python
{'bid_p': 16.54, 'bid_v': 209200, 'ask_p': 16.56, 'ask_v': 296455}
# L2 还有: 'bid_q': {'total_orders': 155, 'queue_volumes': [...]}
```

## Bar 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | str | 标的代码 |
| frequency | str | 频率 |
| open | float | 开盘价 |
| close | float | 收盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| volume | long | 成交量 |
| amount | float | 成交额 |
| position | long | 持仓量（期货） |
| bob | datetime | bar 开始时间 |
| eob | datetime | bar 结束时间 |
| pre_close | float | 昨收（L2 bar 含此字段） |

## Order 委托对象关键字段

| 字段 | 类型 | 说明 |
|------|------|------|
| cl_ord_id | str | 委托客户端 ID（唯一标识） |
| order_id | str | 柜台委托 ID |
| symbol | str | 标的代码 |
| status | int | 委托状态（见枚举） |
| side | int | 买卖方向 |
| volume | int | 委托量 |
| price | float | 委托价格 |
| filled_volume | int | 已成量 |
| filled_vwap | float | 已成均价 |
| created_at | datetime | 委托创建时间 |

## Position 持仓对象关键字段

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | str | 标的代码 |
| side | int | 持仓方向 |
| volume | int | 总持仓量 |
| volume_today | int | 今日买入量 |
| available | int | 可用持仓 |
| vwap | float | 持仓均价 |
| market_value | float | 持仓市值 |
| fpnl | float | 浮动盈亏 |
| cost | float | 持仓成本 |
| amount | float | 持仓额 |

## Cash 资金对象

| 字段 | 类型 | 说明 |
|------|------|------|
| nav | float | 总资产 |
| available | float | 可用资金 |
| fpnl | float | 浮动盈亏 |
| market_value | float | 市值 |
| balance | float | 资金余额 |
| order_frozen | float | 冻结资金 |

## Indicator 绩效指标对象（回测结束后）

| 字段 | 说明 |
|------|------|
| pnl_ratio | 累计收益率 |
| pnl_ratio_annual | 年化收益率 |
| sharp_ratio | 夏普比率 |
| max_drawdown | 最大回撤 |
| win_ratio | 胜率 |
| calmar_ratio | 卡玛比率 |
| open_count | 开仓次数 |
| close_count | 平仓次数 |
| win_count | 盈利次数 |
| lose_count | 亏损次数 |
