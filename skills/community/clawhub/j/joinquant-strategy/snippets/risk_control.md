# 风险控制代码

## 1. 止损策略

### 1.1 固定百分比止损

```python
# 固定百分比止损
def stop_loss(context, stock, stop_loss_pct=0.05):
    """
    固定百分比止损
    stock: 股票代码
    stop_loss_pct: 止损百分比，默认5%
    """
    position = context.portfolio.positions.get(stock)
    if position:
        cost_price = position.avg_cost
        current_price = get_current_data()[stock].last_price
        loss_pct = (current_price - cost_price) / cost_price
        
        if loss_pct < -stop_loss_pct:
            order_target(stock, 0)
            log.info(f'{stock} 触发止损，亏损 {loss_pct:.2%}')

# 使用示例
for stock in list(context.portfolio.positions.keys()):
    stop_loss(context, stock, stop_loss_pct=0.05)
```

### 1.2 移动止损

```python
# 移动止损
def trailing_stop_loss(context, stock, trailing_stop_pct=0.08):
    """
    移动止损
    stock: 股票代码
    trailing_stop_pct: 移动止损百分比，默认8%
    """
    position = context.portfolio.positions.get(stock)
    if position:
        # 获取历史最高价
        df = get_price(stock, end_date=context.current_dt, count=20, frequency='daily')
        if len(df) > 0:
            highest_price = df['high'].max()
            current_price = get_current_data()[stock].last_price
            
            # 计算止损价格
            stop_price = highest_price * (1 - trailing_stop_pct)
            
            if current_price < stop_price:
                order_target(stock, 0)
                log.info(f'{stock} 触发移动止损，当前价格 {current_price}，止损价格 {stop_price}')

# 使用示例
for stock in list(context.portfolio.positions.keys()):
    trailing_stop_loss(context, stock, trailing_stop_pct=0.08)
```

### 1.3 时间止损

```python
# 时间止损
def time_stop_loss(context, stock, hold_days=10):
    """
    时间止损
    stock: 股票代码
    hold_days: 持有天数，默认10天
    """
    position = context.portfolio.positions.get(stock)
    if position:
        # 计算持有天数
        hold_days_count = (context.current_dt - position.init_time).days
        
        if hold_days_count >= hold_days:
            order_target(stock, 0)
            log.info(f'{stock} 持有时间达到 {hold_days} 天，执行时间止损')

# 使用示例
for stock in list(context.portfolio.positions.keys()):
    time_stop_loss(context, stock, hold_days=10)
```

## 2. 止盈策略

### 2.1 固定百分比止盈

```python
# 固定百分比止盈
def take_profit(context, stock, take_profit_pct=0.1):
    """
    固定百分比止盈
    stock: 股票代码
    take_profit_pct: 止盈百分比，默认10%
    """
    position = context.portfolio.positions.get(stock)
    if position:
        cost_price = position.avg_cost
        current_price = get_current_data()[stock].last_price
        profit_pct = (current_price - cost_price) / cost_price
        
        if profit_pct > take_profit_pct:
            order_target(stock, 0)
            log.info(f'{stock} 触发止盈，盈利 {profit_pct:.2%}')

# 使用示例
for stock in list(context.portfolio.positions.keys()):
    take_profit(context, stock, take_profit_pct=0.1)
```

### 2.2 移动止盈

```python
# 移动止盈
def trailing_take_profit(context, stock, trailing_take_profit_pct=0.05):
    """
    移动止盈
    stock: 股票代码
    trailing_take_profit_pct: 移动止盈百分比，默认5%
    """
    position = context.portfolio.positions.get(stock)
    if position:
        # 获取历史最低价
        df = get_price(stock, end_date=context.current_dt, count=20, frequency='daily')
        if len(df) > 0:
            lowest_price = df['low'].min()
            current_price = get_current_data()[stock].last_price
            
            # 计算止盈价格
            take_price = lowest_price * (1 + trailing_take_profit_pct)
            
            if current_price > take_price:
                order_target(stock, 0)
                log.info(f'{stock} 触发移动止盈，当前价格 {current_price}，止盈价格 {take_price}')

# 使用示例
for stock in list(context.portfolio.positions.keys()):
    trailing_take_profit(context, stock, trailing_take_profit_pct=0.05)
```

## 3. 仓位管理

### 3.1 总仓位控制

```python
# 总仓位控制
def control_total_position(context, max_position_pct=0.8):
    """
    总仓位控制
    max_position_pct: 最大仓位百分比，默认80%
    """
    current_position_pct = context.portfolio.positions_value / context.portfolio.total_value
    
    if current_position_pct > max_position_pct:
        # 需要降低仓位
        reduce_amount = (current_position_pct - max_position_pct) * context.portfolio.total_value
        
        # 按比例减持所有持仓
        for stock in list(context.portfolio.positions.keys()):
            position = context.portfolio.positions[stock]
            reduce_value = reduce_amount * (position.value / context.portfolio.positions_value)
            current_price = get_current_data()[stock].last_price
            reduce_shares = int(reduce_value / current_price)
            
            if reduce_shares > 0:
                order(stock, -reduce_shares)
                log.info(f'降低 {stock} 仓位，减持 {reduce_shares} 股')

# 使用示例
control_total_position(context, max_position_pct=0.8)
```

### 3.2 单只股票仓位控制

```python
# 单只股票仓位控制
def control_single_position(context, stock, max_single_pct=0.2):
    """
    单只股票仓位控制
    stock: 股票代码
    max_single_pct: 单只股票最大仓位百分比，默认20%
    """
    position = context.portfolio.positions.get(stock)
    if position:
        single_position_pct = position.value / context.portfolio.total_value
        
        if single_position_pct > max_single_pct:
            # 需要降低仓位
            target_value = context.portfolio.total_value * max_single_pct
            order_target_value(stock, target_value)
            log.info(f'调整 {stock} 仓位到 {max_single_pct:.2%}')

# 使用示例
for stock in list(context.portfolio.positions.keys()):
    control_single_position(context, stock, max_single_pct=0.2)
```

## 4. 风险指标监控

### 4.1 波动率监控

```python
# 波动率监控
def monitor_volatility(stock, lookback_days=20, max_volatility=0.02):
    """
    波动率监控
    stock: 股票代码
    lookback_days: 回看天数，默认20天
    max_volatility: 最大日波动率，默认2%
    """
    df = get_price(stock, end_date=context.current_dt, count=lookback_days, frequency='daily')
    if len(df) >= lookback_days:
        # 计算日收益率
        df['returns'] = df['close'].pct_change()
        # 计算波动率
        volatility = df['returns'].std()
        
        if volatility > max_volatility:
            log.info(f'{stock} 波动率过高：{volatility:.2%}，超过阈值 {max_volatility:.2%}')
            return False
    return True

# 使用示例
for stock in list(context.portfolio.positions.keys()):
    if not monitor_volatility(stock):
        order_target(stock, 0)
        log.info(f'因波动率过高，卖出 {stock}')
```

### 4.2 夏普比率监控

```python
# 夏普比率监控
def calculate_sharpe_ratio(stock, lookback_days=252, risk_free_rate=0.03):
    """
    计算夏普比率
    stock: 股票代码
    lookback_days: 回看天数，默认252天
    risk_free_rate: 无风险利率，默认3%
    """
    df = get_price(stock, end_date=context.current_dt, count=lookback_days, frequency='daily')
    if len(df) >= lookback_days:
        # 计算日收益率
        df['returns'] = df['close'].pct_change()
        # 计算年化收益率
        annual_return = df['returns'].mean() * 252
        # 计算年化波动率
        annual_volatility = df['returns'].std() * np.sqrt(252)
        # 计算夏普比率
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
        return sharpe_ratio
    return 0

# 使用示例
for stock in list(context.portfolio.positions.keys()):
    sharpe = calculate_sharpe_ratio(stock)
    if sharpe < 0.5:
        log.info(f'{stock} 夏普比率过低：{sharpe:.2f}')
        # 可以考虑减持或卖出
```

## 5. 市场风险控制

### 5.1 大盘风险控制

```python
# 大盘风险控制
def market_risk_control(context, index_code='000300.XSHG', max_drawdown=0.05):
    """
    大盘风险控制
    index_code: 指数代码，默认沪深300
    max_drawdown: 最大回撤，默认5%
    """
    # 获取指数历史数据
    df = get_price(index_code, end_date=context.current_dt, count=30, frequency='daily')
    if len(df) >= 2:
        # 计算指数回撤
        index_high = df['high'].max()
        index_current = df['close'][-1]
        index_drawdown = (index_current - index_high) / index_high
        
        if index_drawdown < -max_drawdown:
            # 大盘回撤过大，降低仓位
            log.info(f'大盘回撤过大：{index_drawdown:.2%}，超过阈值 {max_drawdown:.2%}')
            # 可以选择降低仓位或清仓
            for stock in list(context.portfolio.positions.keys()):
                order_target(stock, 0)
                log.info(f'因大盘风险，卖出 {stock}')

# 使用示例
market_risk_control(context, index_code='000300.XSHG', max_drawdown=0.05)
```

### 5.2 行业风险控制

```python
# 行业风险控制
def industry_risk_control(context, industry_code, max_drawdown=0.08):
    """
    行业风险控制
    industry_code: 行业代码
    max_drawdown: 最大回撤，默认8%
    """
    # 获取行业成分股
    industry_stocks = get_industry_stocks(industry_code, date=context.current_dt.strftime('%Y-%m-%d'))
    
    if industry_stocks:
        # 计算行业平均回撤
        total_drawdown = 0
        valid_stocks = 0
        
        for stock in industry_stocks[:10]:  # 取前10只股票计算
            df = get_price(stock, end_date=context.current_dt, count=30, frequency='daily')
            if len(df) >= 2:
                stock_high = df['high'].max()
                stock_current = df['close'][-1]
                stock_drawdown = (stock_current - stock_high) / stock_high
                total_drawdown += stock_drawdown
                valid_stocks += 1
        
        if valid_stocks > 0:
            avg_drawdown = total_drawdown / valid_stocks
            if avg_drawdown < -max_drawdown:
                log.info(f'行业 {industry_code} 回撤过大：{avg_drawdown:.2%}，超过阈值 {max_drawdown:.2%}')
                # 可以选择减持该行业股票
                for stock in list(context.portfolio.positions.keys()):
                    if stock in industry_stocks:
                        order_target(stock, 0)
                        log.info(f'因行业风险，卖出 {stock}')

# 使用示例
industry_risk_control(context, '801010', max_drawdown=0.08)  # 801010 为农林牧渔行业代码
```
