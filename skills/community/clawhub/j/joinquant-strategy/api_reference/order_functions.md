# 下单函数说明

## 1. 基本下单函数

### 1.1 order 函数

```python
def order(
    security,  # 股票代码
    amount,  # 交易数量，正数为买入，负数为卖出
    style=None  # 下单方式
):
    """下单函数"""
    pass
```

**参数说明**：
- `security`：股票代码
- `amount`：交易数量，正数为买入，负数为卖出
- `style`：下单方式，默认为市价单

**返回值**：
- Order对象，包含订单信息

**示例**：
```python
# 买入100股
order('600000.XSHG', 100)

# 卖出100股
order('600000.XSHG', -100)

# 限价买入
order('600000.XSHG', 100, style=LimitOrder(price=10.5))
```

### 1.2 order_target 函数

```python
def order_target(
    security,  # 股票代码
    amount,  # 目标持仓数量
    style=None  # 下单方式
):
    """调整持仓到目标数量"""
    pass
```

**参数说明**：
- `security`：股票代码
- `amount`：目标持仓数量
- `style`：下单方式，默认为市价单

**返回值**：
- Order对象，包含订单信息

**示例**：
```python
# 调整持仓到1000股
order_target('600000.XSHG', 1000)

# 清仓
order_target('600000.XSHG', 0)
```

### 1.3 order_value 函数

```python
def order_value(
    security,  # 股票代码
    value,  # 交易金额，正数为买入，负数为卖出
    style=None  # 下单方式
):
    """按金额下单"""
    pass
```

**参数说明**：
- `security`：股票代码
- `value`：交易金额，正数为买入，负数为卖出
- `style`：下单方式，默认为市价单

**返回值**：
- Order对象，包含订单信息

**示例**：
```python
# 买入1万元
order_value('600000.XSHG', 10000)

# 卖出1万元
order_value('600000.XSHG', -10000)
```

### 1.4 order_target_value 函数

```python
def order_target_value(
    security,  # 股票代码
    value,  # 目标持仓金额
    style=None  # 下单方式
):
    """调整持仓到目标金额"""
    pass
```

**参数说明**：
- `security`：股票代码
- `value`：目标持仓金额
- `style`：下单方式，默认为市价单

**返回值**：
- Order对象，包含订单信息

**示例**：
```python
# 调整持仓到5万元
order_target_value('600000.XSHG', 50000)

# 清仓
order_target_value('600000.XSHG', 0)
```

## 2. 下单方式

### 2.1 LimitOrder 限价单

```python
order('600000.XSHG', 100, style=LimitOrder(price=10.5))
```

**参数说明**：
- `price`：限价价格

**功能**：
- 以指定价格限价买入或卖出

### 2.2 MarketOrder 市价单

```python
order('600000.XSHG', 100, style=MarketOrder())
```

**功能**：
- 以市价买入或卖出

### 2.3 StopOrder 止损单

```python
order('600000.XSHG', -100, style=StopOrder(price=9.5))
```

**参数说明**：
- `price`：止损价格

**功能**：
- 当价格达到指定止损价格时执行卖出

### 2.4 StopLimitOrder 止损限价单

```python
order('600000.XSHG', -100, style=StopLimitOrder(stop_price=9.5, limit_price=9.4))
```

**参数说明**：
- `stop_price`：止损价格
- `limit_price`：限价价格

**功能**：
- 当价格达到指定止损价格时，以限价单执行卖出

## 3. 订单操作

### 3.1 cancel_order 函数

```python
def cancel_order(order_id):
    """撤单"""
    pass
```

**参数说明**：
- `order_id`：订单ID

**返回值**：
- bool，撤单是否成功

**示例**：
```python
# 下单
order_result = order('600000.XSHG', 100)
if order_result:
    # 撤单
    cancel_order(order_result.order_id)
```

### 3.2 get_orders 函数

```python
def get_orders(
    security=None,  # 股票代码
    status=None,  # 订单状态
    start_date=None,  # 开始日期
    end_date=None  # 结束日期
):
    """获取订单列表"""
    pass
```

**参数说明**：
- `security`：股票代码
- `status`：订单状态，可选 'submitted', 'filled', 'cancelled', 'rejected'
- `start_date`：开始日期，格式为 'YYYY-MM-DD'
- `end_date`：结束日期，格式为 'YYYY-MM-DD'

**返回值**：
- 订单对象列表

**示例**：
```python
# 获取所有订单
orders = get_orders()

# 获取已成交订单
filled_orders = get_orders(status='filled')
```

### 3.3 get_order 函数

```python
def get_order(order_id):
    """获取单个订单"""
    pass
```

**参数说明**：
- `order_id`：订单ID

**返回值**：
- Order对象，包含订单详细信息

**示例**：
```python
# 下单
order_result = order('600000.XSHG', 100)
if order_result:
    # 获取订单信息
    order_info = get_order(order_result.order_id)
    log.info(f'订单状态：{order_info.status}')
```

## 4. 订单对象属性

### 4.1 Order 对象属性

```python
# 订单ID
order.order_id

# 股票代码
order.security

# 交易方向（1为买入，-1为卖出）
order.direction

# 交易数量
order.amount

# 交易价格
order.price

# 交易金额
order.value

# 订单状态
order.status  # 'submitted', 'filled', 'cancelled', 'rejected'

# 下单时间
order.create_time

# 成交时间
order.fill_time
```

**属性说明**：
- `order_id`：订单ID
- `security`：股票代码
- `direction`：交易方向，1为买入，-1为卖出
- `amount`：交易数量
- `price`：交易价格
- `value`：交易金额
- `status`：订单状态，可选 'submitted', 'filled', 'cancelled', 'rejected'
- `create_time`：下单时间
- `fill_time`：成交时间

## 5. 批量下单

### 5.1 批量买入

```python
def batch_buy(stock_list, cash_per_stock):
    """批量买入"""
    for stock in stock_list:
        order_value(stock, cash_per_stock)

# 使用示例
stock_list = ['600000.XSHG', '600519.XSHG', '000001.XSHE']
cash_per_stock = context.portfolio.available_cash / len(stock_list)
batch_buy(stock_list, cash_per_stock)
```

### 5.2 批量卖出

```python
def batch_sell(stock_list):
    """批量卖出"""
    for stock in stock_list:
        order_target(stock, 0)

# 使用示例
batch_sell(list(context.portfolio.positions.keys()))
```

## 6. 下单策略

### 6.1 等权配置

```python
def equal_weight_allocation(stock_list, total_value):
    """等权配置"""
    target_weight = 1.0 / len(stock_list)
    for stock in stock_list:
        target_value = total_value * target_weight
        order_target_value(stock, target_value)

# 使用示例
equal_weight_allocation(['600000.XSHG', '600519.XSHG'], context.portfolio.total_value)
```

### 6.2 按市值加权

```python
def market_cap_weighted_allocation(stock_list, total_value):
    """按市值加权配置"""
    # 获取市值数据
    df = get_fundamentals(
        query(valuation.code, valuation.market_cap)
        .filter(valuation.code.in_(stock_list)),
        date=context.current_dt.strftime('%Y-%m-%d')
    )
    
    if not df.empty:
        # 计算总市值
        total_market_cap = df['market_cap'].sum()
        
        # 按市值加权配置
        for index, row in df.iterrows():
            stock = row['code']
            weight = row['market_cap'] / total_market_cap
            target_value = total_value * weight
            order_target_value(stock, target_value)

# 使用示例
market_cap_weighted_allocation(['600000.XSHG', '600519.XSHG'], context.portfolio.total_value)
```

## 7. 下单风控

### 7.1 检查股票是否可交易

```python
def can_trade(stock):
    """检查股票是否可交易"""
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
if can_trade('600000.XSHG'):
    order('600000.XSHG', 100)
else:
    log.info('股票不可交易')
```

### 7.2 控制下单金额

```python
def limit_order_amount(stock, amount):
    """控制下单金额"""
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
limit_order_amount('600000.XSHG', 1000)
```
