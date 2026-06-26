# 可转债交易 API

> 以下可转债特殊操作**仅实盘环境**可用，仿真/回测不支持

## 普通可转债交易

普通买卖与股票一致，使用 `order_volume` 直接替换 symbol：

```python
# 买入可转债
order_volume(symbol='SZSE.128041', volume=100, side=OrderSide_Buy,
             order_type=OrderType_Limit, position_effect=PositionEffect_Open, price=340)
```

## bond_convertible_call - 可转债转股

```python
bond_convertible_call(symbol, volume, price)
```

```python
# 申请转股100份
bond_convertible_call('SHSE.110051', 100, 0)
```

## bond_convertible_put - 可转债回售

```python
bond_convertible_put(symbol, volume, price)
```

```python
# 申请回售100份
bond_convertible_put('SHSE.183350', 100, 0)
```

## bond_convertible_put_cancel - 撤销回售

```python
bond_convertible_put_cancel(symbol, volume)
```

```python
# 撤销回售100份
bond_convertible_put_cancel('SHSE.183350', 100)
```

## 查询可转债基本信息

```python
from gm.api import *
set_token('YOUR_TOKEN')

# 获取可转债基本信息
infos = get_symbol_infos(sec_type1=1030, sec_type2=103001,
                         symbols='SHSE.113038', df=True)
print(infos)

# 可转债历史行情
data = history(symbol='SHSE.113038', frequency='1d',
               start_time='2024-01-01', end_time='2024-12-31',
               adjust=ADJUST_PREV, df=True)
```

## 注意事项
- 转股价 = `conversion_price`（可通过 `get_symbol_infos` 查询）
- 转股价值 = (100 / 转股价) × 正股股价
- `delisted_date` = 可转债到期日（赎回登记日）
- 可转债回购 `103008` 类型通过 `sec_type2=103008` 查询
