# 数据订阅与事件

## subscribe - 订阅行情

```python
subscribe(symbols, frequency='1d', count=1,
          wait_group=False, wait_group_timeout='10s',
          unsubscribe_previous=False, fields=None, format='df')
```

| 参数 | 类型 | 说明 |
|------|------|------|
| symbols | str or list | 标的代码，多个用英文逗号分隔 |
| frequency | str | 频率：`'tick'`、`'60s'`、`'300s'`、`'900s'`、`'1800s'`、`'3600s'`、`'1d'`，L2：`'l2transaction'`、`'l2order'` |
| count | int | 数据滑窗大小，`context.data` 可用的最大条数 |
| wait_group | bool | 是否等同频率所有标的 bar 到齐再触发，默认 False |
| wait_group_timeout | str | wait_group 超时，默认 `'10s'` |
| unsubscribe_previous | bool | 是否取消之前订阅，默认 False |
| fields | str | 指定返回字段，越少越快 |
| format | str | 数据格式：`'df'`(DataFrame)、`'row'`(list[dict])、`'col'`(dict) |

**性能说明**：`row > col > df`，对性能敏感时用 `format='row'`。

```python
def init(context):
    # 订阅日线，滑窗20条
    subscribe(symbols='SHSE.600000,SZSE.000001', frequency='1d', count=20)
    # 同时订阅分钟线
    subscribe(symbols='SHSE.600000', frequency='60s', count=60)
```

---

## unsubscribe - 取消订阅

```python
unsubscribe(symbols='*', frequency='60s')
```

- 默认取消所有已订阅行情
- 只取消指定标的的指定频率，其他频率不受影响

---

## on_tick - Tick 数据事件

```python
def on_tick(context, tick):
    print(tick['symbol'], tick['price'])
```

tick 对象包含：`symbol`、`open`、`high`、`low`、`price`、`cum_volume`、`cum_amount`、`last_volume`、`last_amount`、`quotes`（5档买卖盘）、`created_at`

---

## on_bar - Bar 数据事件

```python
def on_bar(context, bars):
    for bar in bars:
        print(bar['symbol'], bar['close'])
```

bars 是 list，单标的时长度为 1（wait_group=False），多标的全到时长度 > 1。

bar 对象包含：`symbol`、`frequency`、`open`、`close`、`high`、`low`、`volume`、`amount`、`bob`、`eob`

---

## on_l2transaction - 逐笔成交（L2）

> 仅特定付费券商可用

```python
def init(context):
    subscribe(symbols='SHSE.600000', frequency='l2transaction')

def on_l2transaction(context, transaction):
    print(transaction)
```

---

## on_l2order - 逐笔委托（L2）

> 仅特定付费券商可用，仅深市标的

```python
def init(context):
    subscribe(symbols='SZSE.000001', frequency='l2order')

def on_l2order(context, l2order):
    print(l2order)
```

---

## 交易事件回调

| 函数 | 触发时机 |
|------|--------|
| `on_execution_report(context, execrpt)` | 委托执行时触发 |
| `on_order_status(context, order)` | 委托状态变更时触发 |
| `on_account_status(context, account)` | 账户状态变更时触发 |
| `on_error(context, code, info)` | 发生异常时触发 |
| `on_parameter(context, parameter)` | 动态参数修改时触发 |
| `on_backtest_finished(context, indicator)` | 回测结束时触发 |

### 回测结束事件示例
```python
def on_backtest_finished(context, indicator):
    print('累计收益率:', indicator['pnl_ratio'])
    print('年化收益率:', indicator['pnl_ratio_annual'])
    print('夏普比率:', indicator['sharp_ratio'])
    print('最大回撤:', indicator['max_drawdown'])
    print('胜率:', indicator['win_ratio'])
```

---

## on_execution_report - 成交回报事件（✅ 已实测通过）

> **触发时机**：每当有成交发生时触发（包括部分成交）
> **实测环境**：回测模式 (MODE_BACKTEST)，SDK v3.0.183

```python
def on_execution_report(context, execrpt):
    """
    execrpt 对象关键字段（已验证）:
      symbol       — str,   标的代码（如 'SHSE.600519'）
      side         — int,   1=买入, 2=卖出
      volume       — int,   成交数量（股）
      price        — float, 成交均价
      exec_type    — int/str, 回测中为数字15(成交确认), 实盘可能为'T'/'C'
      commission   — float, 本笔手续费
      cl_ord_id    — str,   客户端订单ID（系统生成）
      order_id     — str,   柜台订单ID
      created_at   — datetime, 成交时间
    """
    # 推荐的兼容写法（支持 dict 和属性两种风格）:
    if isinstance(execrpt, dict):
        symbol = execrpt.get('symbol', '')
        volume = execrpt.get('volume', 0)
        price = execrpt.get('price', 0)
    else:
        symbol = getattr(execrpt, 'symbol', '')
        volume = getattr(execrpt, 'volume', 0)
        price = getattr(execrpt, 'price', 0)

    print(f'成交: {symbol} {volume}股 @ {price}')
```

**实测行为（2026-04-17 验证）**：
- `order_target_volume` 买入 → 触发 **1次** on_execution_report（全部成交汇总）
- `order_target_volume` 卖出 → 触发 **1次** on_execution_report
- 每笔成交回报都带 `commission` 手续费值
- `exec_type` 在回测中返回数字 `15`，不是字符 `'T'`

---

## on_order_status - 委托状态变更事件（✅ 已实测通过）

> **触发时机**：订单生命周期中的每个状态变化都会触发
> **特别重要**：status=7(拒绝) 时包含拒单原因
> **实测环境**：回测模式 (MODE_BACKTEST)，SDK v3.0.183

```python
def on_order_status(context, order):
    """
    order 对象关键字段（已验证）:
      cl_ord_id          — str,   客户端订单ID
      order_id           — str,   柜台订单ID
      symbol             — str,   标的代码
      status             — int,   委托状态（见下方枚举）
      side               — int,   1=买, 2=卖
      volume             — int,   委托总量
      price              — float, 委托价格
      filled_volume      — int,   已成交数量
      filled_vwap        — float, 已成交均价
      created_at         — datetime, 创建时间
      rejection_reason   — str,   仅 status=7 时有值（拒单原因）
    """

    # 状态码映射（完整版，含回测特有码）
    status_map = {
        1: '新建(New)',
        2: '已报(Sent)',
        3: '部分成交(PartiallyFilled)',
        4: '已成交(Filled)',
        5: '已撤(Cancelled)',
        6: '未成交(Expired)',          # 限价超时未成交
        7: '拒绝(Rejected)',            # ⚠️ 含 rejection_reason
        8: '待撤(Cancelling)',          # 正在撤销
        9: '未知(Unknown)',
        10: '内部态(Internal)',          # ⚠️ 回测模式特有！文档未记录
    }

    status = order.get('status') if isinstance(order, dict) else getattr(order, status, None)
    status_text = status_map.get(status, f'未知({status})')

    if status == 7:
        reason = order.get('rejection_reason') if isinstance(order, dict) \
                 else getattr(order, 'rejection_reason', None)
        print(f'❌ 订单被拒绝! 原因: {reason}')
```

**实测状态流转（2026-04-17 验证）**：

| 下单方式 | 触发的状态序列 | 备注 |
|----------|---------------|------|
| `order_volume` 市价买 | **10 → 8** | 资金不足时：内部态→待撤 |
| `order_target_volume` 买 | **10 → 1 → 3** | 内部态→新建→部分成交 |
| `order_target_volume` 卖 | **10 → 1 → 3** | 内部态→新建→部分成交 |
| `order_volume` 限价(低价) | **10 → 8** | 不会成交→自动撤单 |
| 超额卖出 | **10 → 8** | 回测不报Rejected，变Cancelling |
| 超额买入(资金不足) | **10 → 8** | 同上 |

**⚠️ 关键发现**：
- **回测模式没有 Rejected(7)**：所有风控违规（超额/资金不足）都变为 Cancelling(8)
- **要测试 Rejected(7)**：必须用 **live（仿真/实盘）** 模式
- 状态 **10** 是回测内部中间态，每个订单首先收到一个 status=10
- `order_target_volume` 会产生比 `order_volume` 更多的状态事件（多了 New → PartiallyFilled 流转）
