# L2 行情数据查询（付费专项）

> 以下所有接口**仅特定付费券商托管版**可用

## get_history_l2ticks - 查询历史 L2 Tick

```python
get_history_l2ticks(symbols, start_time, end_time, fields=None,
                    skip_suspended=True, fill_missing=None,
                    adjust=ADJUST_NONE, adjust_end_time='', df=False)
```

**限制**：每次只能取**一天**数据；时间跨度超过 31 天则返回空。

```python
ticks = get_history_l2ticks('SHSE.600519', '2024-11-23 14:00:00',
                             '2024-11-23 15:00:00', df=True)
```

---

## get_history_l2bars - 查询历史 L2 Bar

```python
get_history_l2bars(symbols, frequency, start_time, end_time,
                   fields=None, skip_suspended=True, fill_missing=None,
                   adjust=ADJUST_NONE, adjust_end_time='', df=False)
```

**限制**：每次最多取 **31 天**（1 个自然月）。

```python
bars = get_history_l2bars('SHSE.600000', '60s',
                          '2024-11-01 09:30:00', '2024-11-30 15:30:00',
                          df=True)
```

---

## get_history_l2transactions - 查询历史 L2 逐笔成交

```python
get_history_l2transactions(symbols, start_time, end_time, fields=None, df=False)
```

**限制**：每次只能取**一天**数据。

```python
trans = get_history_l2transactions('SHSE.600000',
                                   '2024-11-23 14:00:00',
                                   '2024-11-23 15:00:00', df=True)
```

返回字段：`symbol`、`side`（沪市：B/S/N）、`price`、`volume`、`exec_type`（深市：4=撤单，F=成交）、`created_at`

---

## get_history_l2orders - 查询历史 L2 逐笔委托

> 仅深市标的可用

```python
get_history_l2orders(symbols, start_time, end_time, fields=None, df=False)
```

**限制**：每次只能取**一天**数据。

```python
orders = get_history_l2orders('SZSE.000001',
                              '2024-11-23 14:00:00',
                              '2024-11-23 15:00:00', df=True)
```

返回字段：`symbol`、`side`（深市：1=买，2=卖，F=借入，G=出借；沪市：B=买，S=卖）、`price`、`volume`、`order_type`、`order_index`、`created_at`

---

## get_history_l2orders_queue - 查询历史 L2 委托队列

```python
get_history_l2orders_queue(symbols, start_time, end_time, fields=None, df=False)
```

**限制**：每次只能取**一天**数据。

```python
queue = get_history_l2orders_queue('SZSE.000001',
                                   '2024-11-23 14:00:00',
                                   '2024-11-23 15:00:00', df=True)
```

返回字段：`symbol`、`price`、`total_orders`（委托总数）、`queue_orders`（队列数）、`queue_volumes`（前50个委托量列表）、`side`、`volume`、`created_at`
