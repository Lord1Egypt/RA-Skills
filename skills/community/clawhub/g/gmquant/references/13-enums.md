# 枚举常量速查

## 运行模式
```python
MODE_LIVE = 1       # 实时模式（仿真/实盘）
MODE_BACKTEST = 2   # 回测模式
```

## 复权方式
```python
ADJUST_NONE = 0     # 不复权
ADJUST_PREV = 1     # 前复权
ADJUST_POST = 2     # 后复权
```

## 买卖方向 OrderSide
```python
OrderSide_Buy = 1   # 买入
OrderSide_Sell = 2  # 卖出
```

## 委托类型 OrderType
```python
OrderType_Limit = 1    # 限价委托
OrderType_Market = 2   # 市价委托
```

## 开平标志 PositionEffect
```python
PositionEffect_Open = 1        # 开仓
PositionEffect_Close = 2       # 平仓（平昨）
PositionEffect_Close_Today = 3 # 平今（期货）
```

## 持仓方向 PositionSide
```python
PositionSide_Long = 1   # 多头/股票买入方向
PositionSide_Short = 2  # 空头（期货做空）
```

## 委托状态 OrderStatus
```python
# 1=待报，2=已报，3=已报待撤，4=部成待撤
# 5=部撤，6=已撤，7=已成，8=废单，10=已报待改
```

## 执行回报类型 ExecType
```python
# 0=未知，1=新委托，2=部分成交，3=成交，4=撤单，5=废单
```

## 证券大类 sec_type1
```python
1010 = 股票
1020 = 基金
1030 = 债券
1040 = 期货
1050 = 期权
1060 = 指数
1070 = 板块
```

## 交易所代码
```python
'SHSE'   # 上交所
'SZSE'   # 深交所
'CFFEX'  # 中金所
'SHFE'   # 上期所
'DCE'    # 大商所
'CZCE'   # 郑商所
'INE'    # 上海国际能源交易中心
'GFEX'   # 广期所
```

## symbol 格式示例
| 市场 | 代码 | 说明 |
|------|------|------|
| 上交所股票 | SHSE.600000 | 浦发银行 |
| 深交所股票 | SZSE.000001 | 平安银行 |
| 中金所期货 | CFFEX.IC2412 | 中证500期货合约 |
| 上期所期货 | SHFE.rb2412 | 螺纹钢期货 |
| 上期所主力 | SHFE.RB | 螺纹钢主力连续（仅回测） |
| 板块 | BK.007347 | 鸿蒙概念板块 |
| 可转债 | SZSE.128041 | 可转债示例 |

## 注意
- symbol **严格区分大小写**，交易所代码全大写
- 板块代码通过 `get_symbols(sec_type1=1070)` 获取
- 期货虚拟合约（主力连续）仅回测模式可用
