# 账户查询函数（独立调用版）

> 以下函数可在策略外通过 `set_token` 直接调用

## get_orders - 查询委托

```python
get_orders(account=None)
```

## get_execution_reports - 查询成交回报

```python
get_execution_reports(account=None)
```

## get_cash - 查询资金

```python
get_cash(account=None)
```

## get_position - 查询持仓

```python
get_position(symbol=None, side=None, account=None)
```

详细字段说明见 `09-algo-order.md`。
