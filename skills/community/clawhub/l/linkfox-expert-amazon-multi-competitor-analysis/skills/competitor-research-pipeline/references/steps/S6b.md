# S6b: 竞品横向对比分析（7维度）

> 与S6/S7并行执行，全部基于S2-S5已有数据，无需额外API调用。

## 输入
- keepa_data: S2 Keepa历史数据（含12月月销、BSR 30/90/180、price）
- sellersprite_data: S3 卖家精灵流量词数据（含adRatio/bid/latest30daysAds）
- aba_data: S4 ABA数据（含clickShare/conversionShare）
- target_asin + competitors: S1竞品名单

## 依赖
S2, S3, S4

## 操作

调用 `scripts/competitor_comparison_analyzer.py`，对目标+全部竞品做7维度横向对比：

### 维度1: 销量趋势横向对比
- 数据: Keepa `monthlySalesUnits1-12MonthsAgo`
- 计算: 12个月月销量折线图，所有ASIN画在同一张图上
- 输出: 趋势方向分类（增长/衰退/稳定/震荡）+ 月度销量对比表

### 维度2: 市场份额变动追踪
- 数据: Keepa 12月月销量
- 计算: 每月市场份额 = ASIN月销量 / 全部ASIN月销量总和
- 输出: 12月份额变动曲线 + 份额增减排名（谁在抢份额/丢份额）

### 维度3: Deal冲击波对比
- 数据: Keepa 12月月销量
- 计算: 识别Deal月（单月≥前后月均3x），Deal后留存率 = 次月销量/Deal月销量
- 输出: 每个ASIN的Deal月+留存率+Deal依赖度评级

### 维度4: 销量稳定性对比
- 数据: Keepa 12月月销量
- 计算: 变异系数CV = 标准差/均值，剔除Deal月后重新计算
- 输出: 稳定性排名 + CV对比表

### 维度5: 季节性同步对比
- 数据: Keepa 12月月销量
- 计算: 各ASIN月销量的皮尔逊相关系数矩阵 + 峰值月检测
- 输出: 同步/异步判断 + 峰值月对比表

### 维度6: BSR动量对比
- 数据: Keepa `salesRank30`/`salesRank90`/`salesRank180`
- 计算: 动量方向 = 30d vs 90d vs 180d 三点趋势
  - 30<90<180 → 加速改善 ↑↑
  - 30>90>180 → 加速恶化 ↓↓
  - 30≈90≈180 → 稳定 →
  - 其他 → 混合 ↕
- 输出: 动量方向标注表 + BSR三时段对比图

### 维度7: 价格-销量弹性对比
- 数据: Keepa 12月 `price` + `monthlySalesUnits`
- 计算: 弹性系数 = (ΔQ/Q) / (ΔP/P)，用对数回归斜率
- 输出: 弹性系数排名 + 价格敏感度分类（敏感/中性/不敏感）

### 维度8: 功能参数对比矩阵
- 数据: Keepa `packageWeight`/`packageDimensions`/`variationNum`/`model`/`manufacturer`/`fbaFees`/`profit` + Amazon Product Detail `itemSpecifications`
- 计算:
  - 规格参数并排对比表（所有ASIN的所有spec字段横排）
  - 物理参数对比：重量/尺寸 → 物流效率排名
  - 变体策略对比：variationNum + color → 颜色/容量覆盖丰富度
  - 制造商/OEM分析：同manufacturer = 可能同工厂代工
  - FBA费用结构对比：fbaFees/price → 费用占比 + profit → 利润空间 + 降价空间
  - 差异化参数识别：目标独有参数 / 目标缺失参数 / 竞品共有参数
- 输出: 参数对比矩阵表 + 差异化分析 + 物流效率排名 + 利润空间排名

## 输出
```json
{
  "sales_trend": {asin: {trend: "growing/declining/stable/volatile", monthly_data: [...]}},
  "market_share": {monthly: [{month, shares: {asin: pct}}], change: {asin: delta_pct}},
  "deal_impact": {asin: {has_deal: bool, deal_month: N, retention_rate: pct, dependency: "high/medium/low/none"}},
  "volatility": {asin: {cv: N, cv_excl_deal: N, stability: "high/medium/low"}},
  "seasonality": {correlation_matrix: {}, peak_months: {asin: N}, is_synchronized: bool},
  "bsr_momentum": {asin: {rank30: N, rank90: N, rank180: N, direction: "accelerating_up/declining_down/stable/mixed"}},
  "price_elasticity": {asin: {elasticity: N, sensitivity: "sensitive/neutral/insensitive"}},
  "spec_comparison": {
    "matrix": [{param, values: {asin: value}}],
    "logistics_ranking": [{asin, weight, volume, efficiency_score}],
    "variant_strategy": {asin: {variation_num, colors: [], coverage: "high/medium/low"}},
    "oem_analysis": {manufacturer: [asins]},
    "cost_structure": {asin: {fba_fee, fba_pct, profit, profit_pct, price_cut_space}},
    "differentiation": {target_unique: [], target_missing: [], common: []}
  }
}
```

## 用途
被S8(SWOT研判)消费：每个维度的对比结果直接支撑SWOT的优势/劣势/机会/威胁判断
被S9(报告)消费：生成7个对比图表章节
