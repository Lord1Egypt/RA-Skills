# 下单处理代码

## 1. 基本下单函数

### 1.1 order 函数

```python
# 买入股票
order('600000.XSHG', 100)  # 买入100股

# 卖出股票
order('600000.XSHG', -100)  # 卖出100股
```

### 1.2 order_target 函数

```python
# 调整持仓到目标数量
order_target('600000.XSHG', 1000)  # 调整持仓到1000股

# 清仓
order_target('600000.XSHG', 0)  # 清仓
```

### 1.3 order_value 函数

```python
# 按金额买入
order_value('600000.XSHG', 10000)  # 买入1万元

# 按金额卖出
order_value('600000.XSHG', -10000)  # 卖出1万元
```

### 1.4 order_target_value 函数

```python
# 调整持仓到目标金额
order_target_value('600000.XSHG', 50000)  # 调整持仓到5万元

# 清仓
order_target_value('600000.XSHG', 0)  # 清仓
```

## 2. 下单参数说明

### 2.1 下单价格

```python
# 限价单
order('600000.XSHG', 100, price=10.5)  # 限价10.5元买入

# 市价单（默认）
order('600000.XSHG', 100)  # 市价买入
```

### 2.2 下单类型

```python
# 买单
order('600000.XSHG', 100)  # 正数为买入

# 卖单
order('600000.XSHG', -100)  # 负数为卖出
```

### 2.3 交易方向

```python
# 开多
order('600000.XSHG', 100)

# 平多
order('600000.XSHG', -100)

# 开空（仅支持期货）
order('IF1901.CCFX', -1)  # 期货开空

# 平空（仅支持期货）
order('IF1901.CCFX', 1)  # 期货平空
```

## 3. 下单结果处理

### 3.1 获取下单结果

```python
# 获取下单结果
order_result = order('600000.XSHG', 100)
if order_result:
    log.info(f'下单成功，订单ID：{order_result.order_id}')
else:
    log.info('下单失败')
```

### 3.2 撤单

```python
# 撤单
order_result = order('600000.XSHG', 100)
if order_result:
    cancel_order(order_result.order_id)  # 撤销订单
```

## 4. 批量下单

### 4.1 批量买入

```python
# 批量买入股票
stock_list = ['600000.XSHG', '600519.XSHG', '000001.XSHE']
cash_per_stock = context.portfolio.available_cash / len(stock_list)

for stock in stock_list:
    order_value(stock, cash_per_stock)
    log.info(f'买入 {stock}，金额 {cash_per_stock}')
```

### 4.2 批量卖出

```python
# 批量卖出股票
for stock in list(context.portfolio.positions.keys()):
    order_target(stock, 0)
    log.info(f'卖出 {stock}')
```

## 5. 下单策略

### 5.1 等权配置

```python
# 等权配置
stock_list = ['600000.XSHG', '600519.XSHG', '000001.XSHE']
target_weight = 1.0 / len(stock_list)

for stock in stock_list:
    target_value = context.portfolio.total_value * target_weight
    order_target_value(stock, target_value)
    log.info(f'调整 {stock} 持仓到 {target_weight:.2%}')
```

### 5.2 按市值加权

```python
# 按市值加权
stock_list = ['600000.XSHG', '600519.XSHG', '000001.XSHE']

# 获取市值数据
df = get_fundamentals(
    query(valuation.code, valuation.market_cap)
    .filter(valuation.code.in_(stock_list)),
    date=context.current_dt.strftime('%Y-%m-%d')
)

# 计算总市值
total_market_cap = df['market_cap'].sum()

# 按市值加权配置
for index, row in df.iterrows():
    stock = row['code']
    weight = row['market_cap'] / total_market_cap
    target_value = context.portfolio.total_value * weight
    order_target_value(stock, target_value)
    log.info(f'调整 {stock} 持仓到 {weight:.2%}')
```

## 6. 下单风控

### 6.1 检查股票是否可交易

```python
# 检查股票是否可交易
def can_trade(stock):
    current_data = get_current_data()
    if stock not in current_data:
        return False
    stock_data = current_data[stock]
    if stock_data.paused:  # 停牌
        return False
    if stock_data.limit_up:  # 涨停
        return False
    if stock_data.limit_down:  # 跌停
        return False
    return True

# 使用示例
stock = '600000.XSHG'
if can_trade(stock):
    order(stock, 100)
else:
    log.info(f'{stock} 不可交易')
```

### 6.2 控制下单金额

```python
# 控制下单金额
def limit_order(stock, amount):
    current_data = get_current_data()
    if stock in current_data:
        price = current_data[stock].last_price
        order_value = amount * price
        max_order_value = context.portfolio.available_cash * 0.3  # 单次下单不超过可用资金的30%
        if order_value > max_order_value:
            amount = int(max_order_value / price)
            log.info(f'调整下单数量到 {amount}')
        if amount > 0:
            order(stock, amount)

# 使用示例
limit_order('600000.XSHG', 1000)
```
