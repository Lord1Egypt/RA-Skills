# 数据分析方法论详解 / Data Analytics Methodology Deep-Dives

<!-- LANG: Reply in the user's language. Match CN/EN accordingly. -->

---

## 一、RFM模型 / RFM Model

### 1.1 什么是RFM / What is RFM

| 维度 | CN | EN |
|------|----|----|
| **R** - Recency | 最近一次时间 — 用户最近一次互动距今多久 | Days since last interaction |
| **F** - Frequency | 频次 — 一定周期内的使用/购买次数 | Frequency — interaction count within a period |
| **M** - Monetary | 金额 — 贡献的客源量/交易额 | Monetary — revenue or value contribution |

---

### 1.2 RFM在经纪人分层中的应用 / RFM for Agent Segmentation

**场景 / Scenario**：Company A 企业微信 AI 选房工具 / AI Property Tool on Enterprise WeChat

<!-- ZH-CN -->
```
R = 近30天使用AI选房的天数
F = 近30天使用AI选房的频次
M = 近30天产生的客源量

分层结果：
- 高R高F高M：忠粉用户（头部活跃）
- 高R低F低M：初涉功能（需要激活）
- 低R高F高M：高召回用户（流失风险）
- 低R低F低M：低潜用户（持续流失）
```

<!-- EN -->
```
R = Days using AI property tool in last 30 days
F = Frequency of tool usage in last 30 days
M = Leads generated in last 30 days

Segmentation:
- High R, High F, High M: Loyal users (top-tier active)
- High R, Low F, Low M: New users (needs activation)
- Low R, High F, High M: At-risk power users (churn risk)
- Low R, Low F, Low M: Low-potential users (churning)
```

---

### 1.3 阈值设定方法 / Threshold Setting Methods

<!-- ZH-CN -->
**方法一：业务经验**
根据业务方对"活跃"的定义设定阈值
例如：月使用≥10次 → 高频；近7天有使用 → 最近

**方法二：数据分布**
观察历史数据分布，找拐点
例如：80%用户月使用<5次，5次作为分界

**方法三：K-means辅助**
先用K-means找到自然聚类，再用业务经验微调阈值
适用于数据分布不均匀的场景

<!-- EN -->
**Method 1: Business rules**
Set thresholds based on the business team's definition of "active."
E.g., ≥10 uses/month = high frequency; used in last 7 days = recent

**Method 2: Data distribution**
Plot historical data and find inflection points.
E.g., 80% of users use <5 times/month — use 5 as the cutoff

**Method 3: K-means assisted**
Use K-means to find natural clusters, then fine-tune with business logic.
Best for uneven data distributions.

---

### 1.4 RFM+K-means组合应用 / RFM + K-means Combined

<!-- ZH-CN -->
**为什么需要K-means补充？**
- 人工阈值可能不适合数据分布
- 8类分层可能过于粗粒度
- 想找到更精准的特征分组

**实战案例**：
```
RFM分8类后，我发现有些"潜力用户"被误分到低潜。
用K-means聚类后，补充了：
- 潜在经纪人（特征：高R低F，但有上升趋势）
- 高召回经纪人（特征：低R但历史高F高M）
最终通过人工+模型的方式让分层更科学。
```

<!-- EN -->
**Why complement RFM with K-means?**
- Manual thresholds may not fit the actual data distribution
- 8-class segmentation can be too coarse
- You want more precise, data-driven segments

**Worked example**:
```
After RFM's 8-class split, some "potential users" were mislabeled as low-potential.
After applying K-means clustering, two additional segments emerged:
- Rising agents: High R, low F, but upward trend
- At-risk power users: Low R, but historically high F and M
Human judgment + model-driven clustering = more robust segmentation.
```

---

## 二、PSM模型（倾向性得分匹配）/ Propensity Score Matching (PSM)

### 2.1 什么是PSM / What is PSM

<!-- ZH-CN -->
**定义**：Propensity Score Matching，通过 Logistic 回归计算每个个体的倾向性得分，然后匹配特征相似的个体。

**解决的问题**：选择偏差（Selection Bias）
- 实验组和对照组天然特征不同
- 直接比较会放大混杂因素影响

<!-- EN -->
**Definition**: PSM calculates a propensity score for each individual using logistic regression, then matches individuals with similar scores to create comparable treatment and control groups.

**Problem solved**: Selection bias — when treatment and control groups have inherently different characteristics, direct comparison amplifies confounding effects.

---

### 2.2 PSM的步骤 / PSM Step by Step

```
1. 选择特征变量（X）
   影响是否"被处理"的变量
   例如：商机转化率、私域渗透率、使用频次

2. 建立Logistic回归模型
   P(Treatment=1) = f(X1, X2, ..., Xn)
   
3. 计算每个个体的倾向性得分（0-1之间）

4. 匹配方法
   - 最近邻匹配：找得分最接近的个体
   - 卡尺匹配：在一定范围内匹配
   - 分层匹配：按得分分层后匹配

5. 平衡性检验
   匹配后两组特征应该无显著差异

6. 计算处理效应
   ATT = E[Y|T=1] - E[Y|T=0]
```

```
EN:
1. Select feature variables (X)
   Variables that influence treatment assignment
   E.g., lead conversion rate, private-channel adoption, usage frequency

2. Build logistic regression model
   P(Treatment=1) = f(X1, X2, ..., Xn)
   
3. Calculate propensity score for each individual (0–1)

4. Matching methods
   - Nearest neighbor: match to closest score
   - Caliper: match within a score radius
   - Stratification: stratify by score, then match within strata

5. Balance check
   After matching, treatment and control groups should have no significant differences

6. Calculate treatment effect
   ATT = E[Y|T=1] - E[Y|T=0]
```

---

### 2.3 PSM的局限性 / PSM Limitations

| 局限 / Limitation | 说明 / Description |
|---|---|
| 只能控制已观测变量 | Cannot control for unobserved confounders |
| 需要足够大的样本 | Small samples result in poor matching |
| 匹配后样本量减少 | Unmatched individuals are discarded |

---

## 三、DID（双重差分法）/ Difference in Differences (DID)

### 3.1 什么是DID / What is DID

<!-- ZH-CN -->
**定义**：Difference in Differences，通过两次差分剔除时间趋势和组间差异的影响。

**解决的问题**：自然增长/季节性/政策因素的干扰

<!-- EN -->
**Definition**: DID compares pre/post changes between treatment and control groups to isolate the causal effect of an intervention from time trends and between-group differences.

**Problem solved**: Removes interference from organic growth, seasonality, or policy changes.

---

### 3.2 DID的原理 / DID Logic

```
         实验组     对照组     差分
         Treatment  Control   Difference
实验前     Y0        Y1        Y0-Y1
实验后     Y2        Y3        Y2-Y3
差分   (Y2-Y0)  (Y3-Y1)  (Y2-Y0)-(Y3-Y1)
                              = DID Estimate
```

**核心假设 / Key assumption**：平行趋势假设（Parallel Trends）
如果没有处理，实验组和对照组的变化趋势相同。
If there were no treatment, both groups would have followed the same trend.

---

### 3.3 PSM+DID组合 / PSM + DID Combo

<!-- ZH-CN -->
这是面试中最高频的组合！

```
PSM：解决选择偏差，找到可比的对照组
DID：解决时间趋势，剔除自然增长

实操步骤：
1. 用PSM匹配实验组和对照组
2. 观察两组在实验前后的指标变化
3. 用DID计算净效应
4. 做显著性检验
```

<!-- EN -->
This is the most frequently tested combo in BA/DA interviews!

```
PSM: Solves selection bias → finds a comparable control group
DID: Solves time trends → removes organic growth

Full workflow:
1. Use PSM to match treatment and control groups
2. Observe pre/post metric changes in both groups
3. Apply DID to calculate net effect
4. Run significance tests
```

---

### 3.4 DID的局限性 / DID Limitations

| 局限 / Limitation | 说明 / Description |
|---|---|
| 平行趋势假设 | Requires parallel trends validation;两组处理前趋势应相近 |
| 不能处理动态变化 | Not suitable if treatment effects change over time |
| 需要多期数据 | Requires data from at least pre- and post-treatment periods |

---

## 四、K-means聚类 / K-means Clustering

### 4.1 什么是K-means / What is K-means

<!-- ZH-CN -->
**定义**：将数据分成K个簇，使得簇内方差最小。

**算法步骤**：
1. 选择K值（要分成几类）
2. 随机初始化K个中心点
3. 计算每个点到K个中心的距离，归入最近的簇
4. 重新计算每个簇的中心
5. 重复3-4，直到中心不再变化

<!-- EN -->
**Definition**: K-means partitions data into K clusters to minimize within-cluster variance.

**Algorithm steps**:
1. Choose K (number of clusters)
2. Randomly initialize K centroids
3. Assign each point to the nearest centroid
4. Recalculate each cluster's centroid
5. Repeat 3–4 until centroids stabilize

---

### 4.2 K值选择方法 / Choosing K

| 方法 | CN | EN |
|------|----|----|
| 肘部法则 | 画SSE-K曲线，找拐点 | Plot SSE vs. K, find the elbow |
| 轮廓系数 | 衡量聚类质量，越接近1越好 | Measures clustering quality; closer to 1 = better |
| 业务解释 | 根据业务需求设定 | Set K based on business needs |

---

### 4.3 在RFM中的应用 / Applying K-means to RFM

<!-- ZH-CN -->
```
场景：RFM分层后，有些用户特征不明显，人工阈值不合适

方法：
1. 用RFM的三个值做特征
2. 用K-means找到自然的分组
3. 结合业务解释给每类命名
4. 发现人工阈值没发现的"潜力用户"和"高召回用户"
```

<!-- EN -->
```
Scenario: After RFM segmentation, some users have ambiguous profiles
and manual thresholds don't fit well.

Method:
1. Use R, F, M values as features
2. Apply K-means to find natural clusters
3. Assign business-meaningful labels to each cluster
4. Discovers segments manual thresholds miss: "rising users" and "at-risk power users"
```

---

## 五、漏斗分析 / Funnel Analysis

### 5.1 什么是漏斗分析 / What is Funnel Analysis

<!-- ZH-CN -->
**定义**：追踪用户在转化链路中每一步的流失情况。

**典型场景**：
访问 → 注册 → 激活 → 付费 → 复购

<!-- EN -->
**Definition**: Tracks user drop-off at each step of a conversion funnel.

**Classic example**:
Visit → Sign-up → Activation → Purchase → Repurchase

---

### 5.2 漏斗分析要点 / Funnel Analysis Key Points

| 要点 | CN | EN |
|------|----|----|
| 步骤定义 | 每一步要有明确口径 | Each step must have a clear, defined criterion |
| 转化率 | 步骤间的转化比例 | Conversion rate between steps |
| 流失点识别 | 哪一步流失最严重 | Which step has the worst drop-off |
| 原因分析 | 为什么在这个环节流失 | Why are users dropping at this step |
| 优化策略 | 怎么提升转化率 | How to improve conversion |

---

### 5.3 实战案例：企微链路 / Case: Enterprise WeChat Funnel

<!-- ZH-CN -->
```
企微触达 → AI选房 → 商机获取 → 私域转化 → 带看 → 成交

各环节指标：
- 工具渗透率：60%
- 被动使用率：40%
- 公域转私域：28%
- 商机转化：33%

发现问题：
- 40%是被动使用，转化的商机只有头部1/3
- 公域转私域28%远低于预期

策略：
- 高潜经纪人：培训+激励
- 话术优化+意向标签
```

<!-- EN -->
```
WeChat outreach → AI property tool → Lead generation → Private conversion → Showing → Deal

Stage metrics:
- Tool adoption: 60%
- Passive usage rate: 40%
- Public-to-private conversion: 28%
- Lead conversion: 33%

Issues found:
- 40% passive usage — only top ⅓ generate leads
- Public-to-private at 28% is far below target

Actions:
- High-potential agents: training + incentive program
- Script optimization + intent tagging
```

---

## 六、AB测试 / A/B Testing

### 6.1 什么时候用AB / When to Use A/B Testing

<!-- ZH-CN -->
- 上新功能/策略
- 评估改动效果
- 做因果推断

<!-- EN -->
- Launching a new feature or strategy
- Measuring the impact of a change
- Making causal inferences

---

### 6.2 AB测试步骤 / A/B Test Process

```
1. 明确核心指标（primary metric）
2. 确定最小样本量
3. 设计实验（分流策略）
4. 跑实验周期
5. 显著性检验
6. 结论判断

EN:
1. Define the primary metric
2. Calculate minimum sample size
3. Design experiment (traffic split strategy)
4. Run for experiment duration
5. Run significance test
6. Draw conclusion
```

---

### 6.3 小样本场景怎么办 / Handling Small Sample Sizes

<!-- ZH-CN -->
**问题**：样本量小（<2000），AB测试难显著

**解决方案**：
1. 延长实验周期
2. 降低显著性水平（但要有充分理由）
3. 用回归分析控制混杂变量
4. 用合成控制法（Synthetic Control）
5. 用贝叶斯方法

<!-- EN -->
**Problem**: Sample size is small (<2,000), A/B tests struggle to reach significance.

**Solutions**:
1. Extend the experiment duration to accumulate more data
2. Lower the significance threshold (requires justification)
3. Use regression analysis to control for confounders
4. Use Synthetic Control Methods for quasi-experimental settings
5. Apply Bayesian statistical methods with informative priors

---

## 七、回归分析 / Regression Analysis

### 7.1 回归分析类型与应用 / Regression Types & Use Cases

| 类型 | CN | EN |
|------|----|----|
| 线性回归 | 连续变量预测 | Continuous variable prediction |
| 逻辑回归 | 分类问题、概率预测 | Classification, probability estimation |
| 多元回归 | 控制多个变量看净效应 | Multi-variable control for net effect |

---

### 7.2 在效果评估中的应用 / Regression for Impact Assessment

```
Y = β0 + β1*Treatment + β2*X1 + β3*X2 + ε

其中：
- Y是结果变量（转化率、GMV等）
- Treatment是处理变量（是否用新功能）
- X1, X2是控制变量（用户特征、时间趋势等）
- β1就是 Treatment 的净效应

EN:
- Y = outcome variable (conversion rate, GMV, etc.)
- Treatment = treatment variable (new feature user or not)
- X1, X2 = control variables (user characteristics, time trends, etc.)
- β1 = net effect of the treatment variable
```

---

### 7.3 AB测试 vs 回归分析 / A/B Test vs. Regression

| | AB测试 | 回归分析 |
|--|--------|----------|
| 因果推断 / Causal inference | 强（随机分流）/ Strong (random assignment) | 弱（观察数据）/ Weak (observational data) |
| 适用场景 / Use case | 可做实验 / Experiments possible | 不能做实验 / Cannot run experiments |
| 控制变量 / Control variables | 随机化控制 / Randomized control | 手动控制 / Manually controlled |
| 结果解释 / Result interpretation | 直观 / Straightforward | 需注意内生性 / Watch for endogeneity |

---

## 八、指标体系搭建 / KPI Framework Design

### 8.1 指标体系框架 / KPI Framework

```
北极星指标（North Star Metric）
    ↓
一级指标（Key Metrics）
    ↓
二级指标（Secondary Metrics）
    ↓
落地指标（Operational Metrics）

EN:
North Star Metric
    ↓
Key Metrics (L1)
    ↓
Secondary Metrics (L2)
    ↓
Operational Metrics
```

---

### 8.2 搭建步骤 / Framework Design Steps

<!-- ZH-CN -->
```
1. 理解业务目标
   - 业务的核心诉求是什么？
   - 成功的标准是什么？

2. 定义北极星指标
   - 唯一核心指标
   - 反映用户价值和商业价值

3. 拆解一级指标
   - 影响北极星的关键因素
   - 通常2-5个

4. 拆解二级指标
   - 可落地的运营动作
   - 可以直接取数和分析

5. 建立监控看板
   - 日常监测核心指标
   - 设置预警阈值
```

<!-- EN -->
```
1. Understand the business objective
   - What is the core business ask?
   - What does success look like?

2. Define the North Star metric
   - Single, unifying metric
   - Reflects both user value and business value

3. Break down into Key (L1) metrics
   - Key drivers of the North Star
   - Typically 2–5 metrics

4. Break down into Secondary (L2) metrics
   - Actionable operational levers
   - Directly measurable and analyzable

5. Build monitoring dashboards
   - Daily tracking of key metrics
   - Alert thresholds for anomalies
```

---

### 8.3 示例：企微项目指标体系 / Example: WeChat Project KPI Framework

<!-- ZH-CN -->
```
北极星指标：企微商机转化率
    ↓
一级指标：
  - 工具使用渗透率
  - 公域转私域率
  - 商机跟进率
    ↓
二级指标：
  - AI选房推荐次数
  - 话术发送次数
  - 客户意向标签完善率
    ↓
落地指标：
  - 经纪人日活
  - 培训覆盖率
  - 话术更新频率
```

<!-- EN -->
```
North Star: WeChat lead conversion rate
    ↓
L1 Metrics:
  - Tool adoption rate
  - Public-to-private conversion rate
  - Lead follow-up rate
    ↓
L2 Metrics:
  - AI property recommendation count
  - Script message send count
  - Customer intent tag completion rate
    ↓
Operational Metrics:
  - Agent daily active users
  - Training coverage rate
  - Script update frequency
```
