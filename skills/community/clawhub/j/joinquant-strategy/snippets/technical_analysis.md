# 技术分析代码

## 1. 移动平均线

### 1.1 简单移动平均线 (SMA)

```python
# 计算简单移动平均线
def calculate_sma(stock, period=20):
    """
    计算简单移动平均线
    stock: 股票代码
    period: 周期，默认20
    """
    df = get_price(stock, end_date=context.current_dt, count=period*2, frequency='daily')
    if len(df) >= period:
        df['sma'] = df['close'].rolling(window=period).mean()
        return df['sma'].iloc[-1]
    return None

# 使用示例
sma20 = calculate_sma('600000.XSHG', period=20)
sma50 = calculate_sma('600000.XSHG', period=50)
log.info(f'20日均线：{sma20}，50日均线：{sma50}')

# 金叉死叉判断
if sma20 > sma50:
    log.info('金叉信号')
elif sma20 < sma50:
    log.info('死叉信号')
```

### 1.2 指数移动平均线 (EMA)

```python
# 计算指数移动平均线
def calculate_ema(stock, period=20):
    """
    计算指数移动平均线
    stock: 股票代码
    period: 周期，默认20
    """
    df = get_price(stock, end_date=context.current_dt, count=period*3, frequency='daily')
    if len(df) >= period:
        df['ema'] = df['close'].ewm(span=period, adjust=False).mean()
        return df['ema'].iloc[-1]
    return None

# 使用示例
ema12 = calculate_ema('600000.XSHG', period=12)
ema26 = calculate_ema('600000.XSHG', period=26)
log.info(f'12日EMA：{ema12}，26日EMA：{ema26}')
```

## 2. MACD 指标

```python
# 计算 MACD 指标
def calculate_macd(stock, fast_period=12, slow_period=26, signal_period=9):
    """
    计算 MACD 指标
    stock: 股票代码
    fast_period: 快速周期，默认12
    slow_period: 慢速周期，默认26
    signal_period: 信号周期，默认9
    """
    df = get_price(stock, end_date=context.current_dt, count=slow_period*3, frequency='daily')
    if len(df) >= slow_period:
        # 计算 EMA
        df['ema_fast'] = df['close'].ewm(span=fast_period, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=slow_period, adjust=False).mean()
        # 计算 MACD 线
        df['macd'] = df['ema_fast'] - df['ema_slow']
        # 计算信号线
        df['signal'] = df['macd'].ewm(span=signal_period, adjust=False).mean()
        # 计算柱状图
        df['histogram'] = df['macd'] - df['signal']
        
        return {
            'macd': df['macd'].iloc[-1],
            'signal': df['signal'].iloc[-1],
            'histogram': df['histogram'].iloc[-1]
        }
    return None

# 使用示例
macd_data = calculate_macd('600000.XSHG')
if macd_data:
    log.info(f'MACD: {macd_data["macd"]}, Signal: {macd_data["signal"]}, Histogram: {macd_data["histogram"]}')
    
    # MACD 金叉死叉判断
    if macd_data['macd'] > macd_data['signal']:
        log.info('MACD 金叉信号')
    else:
        log.info('MACD 死叉信号')
```

## 3. RSI 指标

```python
# 计算 RSI 指标
def calculate_rsi(stock, period=14):
    """
    计算 RSI 指标
    stock: 股票代码
    period: 周期，默认14
    """
    df = get_price(stock, end_date=context.current_dt, count=period*2, frequency='daily')
    if len(df) >= period + 1:
        # 计算每日收益率
        df['returns'] = df['close'].pct_change()
        # 计算上涨和下跌
        df['up'] = df['returns'].apply(lambda x: x if x > 0 else 0)
        df['down'] = df['returns'].apply(lambda x: -x if x < 0 else 0)
        # 计算平均上涨和下跌
        df['avg_up'] = df['up'].rolling(window=period).mean()
        df['avg_down'] = df['down'].rolling(window=period).mean()
        # 计算 RSI
        df['rsi'] = 100 - (100 / (1 + df['avg_up'] / df['avg_down']))
        
        return df['rsi'].iloc[-1]
    return None

# 使用示例
rsi = calculate_rsi('600000.XSHG', period=14)
if rsi:
    log.info(f'RSI: {rsi}')
    
    # RSI 超买超卖判断
    if rsi > 70:
        log.info('RSI 超买，可能下跌')
    elif rsi < 30:
        log.info('RSI 超卖，可能上涨')
```

## 4. KDJ 指标

```python
# 计算 KDJ 指标
def calculate_kdj(stock, period=9, k_period=3, d_period=3):
    """
    计算 KDJ 指标
    stock: 股票代码
    period: 周期，默认9
    k_period: K值周期，默认3
    d_period: D值周期，默认3
    """
    df = get_price(stock, end_date=context.current_dt, count=period*3, frequency='daily')
    if len(df) >= period:
        # 计算 RSV
        df['lowest'] = df['low'].rolling(window=period).min()
        df['highest'] = df['high'].rolling(window=period).max()
        df['rsv'] = (df['close'] - df['lowest']) / (df['highest'] - df['lowest']) * 100
        
        # 计算 K 值
        df['k'] = 0
        df['k'].iloc[period-1] = 50  # 初始值
        for i in range(period, len(df)):
            df['k'].iloc[i] = df['k'].iloc[i-1] * (k_period-1)/k_period + df['rsv'].iloc[i] * 1/k_period
        
        # 计算 D 值
        df['d'] = 0
        df['d'].iloc[period-1] = 50  # 初始值
        for i in range(period, len(df)):
            df['d'].iloc[i] = df['d'].iloc[i-1] * (d_period-1)/d_period + df['k'].iloc[i] * 1/d_period
        
        # 计算 J 值
        df['j'] = 3 * df['k'] - 2 * df['d']
        
        return {
            'k': df['k'].iloc[-1],
            'd': df['d'].iloc[-1],
            'j': df['j'].iloc[-1]
        }
    return None

# 使用示例
kdj_data = calculate_kdj('600000.XSHG')
if kdj_data:
    log.info(f'K: {kdj_data["k"]}, D: {kdj_data["d"]}, J: {kdj_data["j"]}')
    
    # KDJ 金叉死叉判断
    if kdj_data['k'] > kdj_data['d']:
        log.info('KDJ 金叉信号')
    else:
        log.info('KDJ 死叉信号')
```

## 5. 布林带

```python
# 计算布林带
def calculate_bollinger_bands(stock, period=20, std_dev=2):
    """
    计算布林带
    stock: 股票代码
    period: 周期，默认20
    std_dev: 标准差倍数，默认2
    """
    df = get_price(stock, end_date=context.current_dt, count=period*2, frequency='daily')
    if len(df) >= period:
        # 计算中轨
        df['middle'] = df['close'].rolling(window=period).mean()
        # 计算标准差
        df['std'] = df['close'].rolling(window=period).std()
        # 计算上轨和下轨
        df['upper'] = df['middle'] + df['std'] * std_dev
        df['lower'] = df['middle'] - df['std'] * std_dev
        
        return {
            'upper': df['upper'].iloc[-1],
            'middle': df['middle'].iloc[-1],
            'lower': df['lower'].iloc[-1]
        }
    return None

# 使用示例
bollinger_data = calculate_bollinger_bands('600000.XSHG')
if bollinger_data:
    current_price = get_current_data()['600000.XSHG'].last_price
    log.info(f'布林带上轨：{bollinger_data["upper"]}，中轨：{bollinger_data["middle"]}，下轨：{bollinger_data["lower"]}')
    
    # 布林带突破判断
    if current_price > bollinger_data['upper']:
        log.info('价格突破布林带上轨，可能继续上涨')
    elif current_price < bollinger_data['lower']:
        log.info('价格突破布林带下轨，可能继续下跌')
```

## 6. 成交量指标

### 6.1 成交量移动平均线

```python
# 计算成交量移动平均线
def calculate_volume_ma(stock, period=20):
    """
    计算成交量移动平均线
    stock: 股票代码
    period: 周期，默认20
    """
    df = get_price(stock, end_date=context.current_dt, count=period*2, frequency='daily')
    if len(df) >= period:
        df['volume_ma'] = df['volume'].rolling(window=period).mean()
        return df['volume_ma'].iloc[-1]
    return None

# 使用示例
volume_ma = calculate_volume_ma('600000.XSHG', period=20)
current_volume = get_price('600000.XSHG', end_date=context.current_dt, count=1, frequency='daily')['volume'].iloc[-1]
log.info(f'成交量：{current_volume}，20日均量：{volume_ma}')

# 量价配合判断
if current_volume > volume_ma * 1.5:
    log.info('成交量放大，可能有资金进入')
```

### 6.2 量比

```python
# 计算量比
def calculate_volume_ratio(stock, days=5):
    """
    计算量比
    stock: 股票代码
    days: 参考天数，默认5
    """
    df = get_price(stock, end_date=context.current_dt, count=days+1, frequency='daily')
    if len(df) >= days+1:
        # 计算当前成交量
        current_volume = df['volume'].iloc[-1]
        # 计算过去N天平均成交量
        avg_volume = df['volume'].iloc[:-1].mean()
        # 计算量比
        volume_ratio = current_volume / avg_volume
        return volume_ratio
    return None

# 使用示例
volume_ratio = calculate_volume_ratio('600000.XSHG', days=5)
if volume_ratio:
    log.info(f'量比：{volume_ratio}')
    if volume_ratio > 2:
        log.info('量比大于2，成交量明显放大')
```

## 7. 其他技术指标

### 7.1 乖离率 (BIAS)

```python
# 计算乖离率
def calculate_bias(stock, period=20):
    """
    计算乖离率
    stock: 股票代码
    period: 周期，默认20
    """
    df = get_price(stock, end_date=context.current_dt, count=period*2, frequency='daily')
    if len(df) >= period:
        # 计算移动平均线
        df['ma'] = df['close'].rolling(window=period).mean()
        # 计算乖离率
        df['bias'] = (df['close'] - df['ma']) / df['ma'] * 100
        return df['bias'].iloc[-1]
    return None

# 使用示例
bias = calculate_bias('600000.XSHG', period=20)
if bias:
    log.info(f'20日乖离率：{bias:.2f}')
    if bias > 10:
        log.info('乖离率过大，可能回调')
    elif bias < -10:
        log.info('乖离率过小，可能反弹')
```

### 7.2 心理线 (PSY)

```python
# 计算心理线
def calculate_psy(stock, period=12):
    """
    计算心理线
    stock: 股票代码
    period: 周期，默认12
    """
    df = get_price(stock, end_date=context.current_dt, count=period+1, frequency='daily')
    if len(df) >= period+1:
        # 计算上涨天数
        df['up'] = df['close'].pct_change() > 0
        up_days = df['up'].iloc[1:].sum()
        # 计算心理线
        psy = up_days / period * 100
        return psy
    return None

# 使用示例
psy = calculate_psy('600000.XSHG', period=12)
if psy:
    log.info(f'心理线：{psy:.2f}')
    if psy > 75:
        log.info('心理线过高，市场可能超买')
    elif psy < 25:
        log.info('心理线过低，市场可能超卖')
```
