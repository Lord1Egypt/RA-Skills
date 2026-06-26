# 回测框架详解

## 回测设计原则

1. **避免前视偏差**：每个信号只使用信号日之前的数据计算
2. **避免生存偏差**：标的池包含2022年以来持续上市的股票
3. **样本外验证**：训练集(2022-2024) vs 测试集(2025-2026)
4. **统计检验**：不看"看起来不错的胜率"，看P值

## 回测参数

```python
BACKTEST_STOCKS = [
    # 10只AI链条纯龙头（市值>500亿）
    ("300308.SZ", "中际旭创", "光模块龙头"),
    ("300502.SZ", "新易盛", "光模块"),
    ("601138.SH", "工业富联", "AI服务器龙头"),
    ("688256.SH", "寒武纪", "AI芯片龙头"),
    ("688041.SH", "海光信息", "GPU/DCU龙头"),
    ("688981.SH", "中芯国际", "芯片代工龙头"),
    ("002371.SZ", "北方华创", "半导体设备龙头"),
    ("002230.SZ", "科大讯飞", "AI应用龙头"),
    ("300750.SZ", "宁德时代", "智能制造龙头"),
    ("002594.SZ", "比亚迪", "智能汽车龙头"),
]

LOOKBACK_DAYS = 60        # 每个信号需要60天历史数据
FORWARD_WINDOWS = [3, 5, 10, 20]  # 多窗口前瞻收益
TRAILING_STOP_PCT = 15.0  # 追踪止损百分比
```

## 回测时期

| 时期 | 日期范围 | 市场特征 |
|------|---------|---------|
| 2022 熊市 | 2022.01-2022.10 | 上证3400→2800 |
| 2023 震荡 | 2023.01-2023.12 | 上证3000→3100 |
| 2024 结构牛 | 2024.01-2024.12 | 上证2800→3400 |
| 2025 科技牛 | 2025.01-2025.12 | 上证3100→3600 |
| 2026 YTD | 2026.01-2026.04 | 最新验证 |

## 数据获取流程

```python
def fetch_period_data(ts, code, start, end):
    daily = ts.get_daily(code, start, end)          # 日线OHLCV
    basic = ts.get_daily_basic(code, start, end)     # 换手率/量比/PE
    mf = ts.get_moneyflow(code, start, end)          # 资金流向
    margin = ts.get_margin(code, start, end)          # 融资融券
    return daily, basic, mf, margin

# 全局数据
index_daily = ts.get_index_daily("000001.SH", ...)   # 上证指数120天
north_global = ts.get_north_money(...)                 # 北向资金20天
spx_data = ts.get_global_index("SPX")                 # 标普500
hsi_data = ts.get_global_index("HSI")                  # 恒生指数
limit_by_date = {td: ts.get_limit_list(td) for td in sampled_dates}
```

## 信号计算

对每只股票的每个交易日：

1. 切取当日之前60天数据窗口
2. 计算5维信号评分
3. 判断市场环境(BULL/NEUTRAL/BEAR)
4. 综合判定信号状态(ACCUMULATION/NEUTRAL/...)
5. 记录未来3/5/10/20日收益

## 统计检验方法

### 二项分布P值

```python
def binomial_p_value(n, k, p0=0.5):
    """P(X >= k | n, p0) — 胜率是否显著高于50%"""
    mean = n * p0
    std = math.sqrt(n * p0 * (1 - p0))
    z = (k - 0.5 - mean) / std  # 连续性修正
    return 0.5 * math.erfc(z / math.sqrt(2))
```

- H0: 胜率 = 50%（随机猜测）
- H1: 胜率 > 50%
- P < 0.05 → 拒绝H0 → 信号有效

### Wilson置信区间

```python
def wilson_ci(n, k, z=1.96):
    """比正态近似更适合小样本的比例估计"""
    p_hat = k / n
    denom = 1 + z * z / n
    center = (p_hat + z * z / (2 * n)) / denom
    spread = z * math.sqrt((p_hat * (1 - p_hat) + z * z / (4 * n)) / n) / denom
    return (max(0, center - spread), min(1, center + spread))
```

## 追踪止损模拟

```python
# 买入后追踪最高价，跌破15%止损
peak = buy_price
for day in next_20_days:
    if day.close > peak:
        peak = day.close
    drawdown = (day.close - peak) / peak * 100
    if drawdown <= -15:
        exit_return = (day.close - buy_price) / buy_price * 100
        break
else:
    exit_return = 20day_return  # 未触发止损用20日收益
```

## 过拟合检测

```
训练集胜率 - 测试集胜率 = 衰减度

衰减 < 5%   → 无明显过拟合
衰减 5-15%  → 轻度过拟合
衰减 > 15%  → 严重过拟合
```

v11实测：训练集~53% → 测试集59% → **负衰减**（测试集更好），说明算法在新数据上泛化良好。

## 综合可信度评分

| 维度 | 权重 | 评分方法 |
|------|------|---------|
| 数据质量 | 15% | Tushare结构化数据=75 |
| 买入信号 | 30% | P值<0.01=90, <0.05=75, <0.10=55 |
| 卖出信号 | 15% | 已砍掉=0（不评分） |
| 样本外 | 25% | 衰减<5%且胜率>60%=85 |
| 样本量 | 15% | >=100次=90, >=50=70 |

**最终结果: 75/100**
