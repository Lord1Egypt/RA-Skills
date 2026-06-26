# Step 1.5 动态健康感知 — 详细参考

本文档是 SKILL.md 中 Step 1.5 的补充说明，提供完整的计算细节和边界情况处理。

## 1. 为什么需要动态感知

传统库存诊断只看"昨日快照"——售罄率是多少、库销比是多少。这相当于拍了一张照片。但库存管理的真正风险往往藏在"趋势"里：

- 售罄率 41%（刚过 40% 基准线）看着"健康"，但如果是从 52% 连跌 5 天跌到 41%，这其实是一个正在恶化的品类
- 库存量 500 件看着"还有"，但如果每天净消耗 200 件、补货只有 100 件，3 天后就断货了
- 库销比 0.3 看着"低"，但如果业务是高频补货模式、库存本来就只覆盖半天销售，0.3 已经偏高了

动态感知解决的核心问题是：**为后续的四象限分类提供趋势上下文和业务模式上下文**，避免在静态阈值上做出误判。

## 2. 数据需求

### 必需查询

通过 metric-query-v2 查询近 14 天每日数据（日粒度，无维度拆分）：

| 指标 | 用途 |
|------|------|
| stock_qty | 库存水位曲线、补货速率推算 |
| retail_qty | 消耗速率、库存覆盖天数 |
| stock_mtv | 资金占用趋势 |
| sell_trough_rate | 售罄率趋势、异常检测 |
| stock_to_sales_ratio | 库销比趋势、异常检测 |

### 为什么选 14 天而不是 30 天

14 天足以覆盖大多数补货周期（周补和双周补），同时避免跨月季节性干扰。如果业务有月度补货节奏，可扩展到 30 天，但 14 天是默认推荐。

## 3. 计算细节

### 3.1 统计基线异常检测

```python
import numpy as np

def detect_anomalies(daily_values, metric_name):
    """对单个指标做 ±2σ 异常检测"""
    arr = np.array(daily_values)
    mean_val = np.mean(arr)
    std_val = np.std(arr)
    latest = arr[-1]

    status = "正常"
    if std_val > 0:  # 避免除零
        z_score = (latest - mean_val) / std_val
        if z_score > 2:
            status = "偏高异常"
        elif z_score < -2:
            status = "偏低异常"

    return {
        "metric": metric_name,
        "mean": mean_val,
        "std": std_val,
        "latest": latest,
        "status": status
    }
```

**边界情况**：
- 若标准差为 0（所有天值相同），跳过异常检测，标记为"稳定"
- 若某天数据缺失（null），排除该天后重新计算

### 3.2 趋势检测

```python
def detect_trend(daily_values, window=5):
    """检测最近 window 天是否连续同向变化"""
    recent = daily_values[-window:]
    diffs = [recent[i+1] - recent[i] for i in range(len(recent)-1)]

    if all(d < 0 for d in diffs):
        return "持续走低 ⚠️", len(diffs)
    elif all(d > 0 for d in diffs):
        return "持续走高", len(diffs)
    else:
        return "波动", 0
```

### 3.3 业务模式识别

这是动态感知中最关键的判断——它决定了后续分析应该侧重什么。

```python
def identify_business_mode(avg_stock, avg_daily_sales):
    """
    库存覆盖天数 = 平均库存 / 日均销量
    覆盖天数越低，说明业务越依赖高频补货
    """
    if avg_daily_sales == 0:
        return "无销售", float('inf')

    coverage_days = avg_stock / avg_daily_sales

    if coverage_days < 1:
        # 库存不够卖一天 → 必须每天补货才能维持
        # 在此模式下，库销比的绝对值意义降低
        # 应转而关注"补货量 vs 消耗量"的平衡
        mode = "高频补货模式"
    elif coverage_days < 7:
        mode = "中频补货模式"
    else:
        # 库存能撑一周以上 → 传统四象限分析完全适用
        mode = "备货模式"

    return mode, coverage_days
```

### 3.4 补货速率估算

由于大多数系统不直接提供"补货量"指标，需要从库存变化中反推：

```python
def estimate_replenishment(daily_stock, daily_sales):
    """
    库存变化 = 补货 - 销售
    因此：补货 = 库存变化 + 销售
    只在库存增加的天取值（库存减少日可能没有补货）
    """
    replenishments = []
    for i in range(1, len(daily_stock)):
        delta = daily_stock[i] - daily_stock[i-1]
        estimated_repl = delta + daily_sales[i]
        if estimated_repl > 0:
            replenishments.append(estimated_repl)

    avg_replenishment = np.mean(replenishments) if replenishments else 0
    avg_consumption = np.mean(daily_sales)
    net_daily = avg_replenishment - avg_consumption

    return {
        "avg_daily_replenishment": avg_replenishment,
        "avg_daily_consumption": avg_consumption,
        "net_daily_change": net_daily,
        "replenishment_days_count": len(replenishments),
        "total_days": len(daily_stock) - 1
    }
```

## 4. 对后续步骤的影响规则

| Step 1.5 发现 | 影响的步骤 | 具体调整 |
|-------------|----------|---------|
| 指标偏离 ±2σ | Step 2 | 对应品类紧迫度 +1 |
| 连续 4+ 天下降 | Step 2 | 即使当前值在阈值内，仍标注"趋势恶化 ⚠️" |
| 高频补货模式 | Step 3 | 必须执行 Step 3c（渠道补货-消耗平衡分析） |
| 净日变化为负 | Step 3/4 | 断货风险上调，R1 规则放宽触发条件 |
| 备货模式 | Step 3 | Step 3c 可跳过，传统四象限分析已足够 |
