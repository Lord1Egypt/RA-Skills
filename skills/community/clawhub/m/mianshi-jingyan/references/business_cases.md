# 业务场景题解题思路 / Business Case Problem-Solving Guide

---

## 一、题型分类 / Case Type Overview

### 1.1 指标设计题 / Metric Design Questions

**典型问题 / Typical Questions**：
- "如果让你做XX业务，你会关注哪些指标？" / "If you were analyzing XX business, what metrics would you focus on?"
- "怎么设计XX功能的评估指标？" / "How would you design metrics to evaluate XX feature?"
- "北极星指标是什么？怎么拆解？" / "What is the North Star metric? How do you break it down?"

<!-- ZH-CN -->
**解题框架**：
```
1. 理解业务目标
   - 这个功能/产品解决什么问题？
   - 用户价值是什么？商业价值是什么？

2. 确定北极星指标
   - 唯一核心指标
   - 反映用户价值和商业价值的平衡

3. 拆解一级指标
   - 影响北极星的关键因素（通常2-5个）

4. 拆解二级指标
   - 可落地的运营指标

5. 确定数据来源
   - 从哪个表取数？口径怎么定义？
```

<!-- EN -->
**Framework**:
```
1. Understand the business objective
   - What problem does this product/feature solve?
   - What is the user value? The business value?

2. Define the North Star metric
   - Single, unifying metric
   - Balances user value and business value

3. Break down into L1 metrics
   - Key drivers of the North Star (typically 2–5)

4. Break down into L2 metrics
   - Actionable operational metrics

5. Define data sources
   - Which tables? What is the calculation definition?
```

---

## 二、经典案例分析 / Worked Business Cases

### 案例一：灵感提示词产品评估 / Case 1: AI Prompt Feature Evaluation

**背景 / Background**：
<!-- ZH-CN -->
```
即梦/Seedance产品新增"灵感提示词"功能。
用户在生成视频时，可以用AI推荐的提示词。

问题：要不要上这个功能？怎么评估效果？
```

<!-- EN -->
```
A new "inspiration prompts" feature was added to an AI video generation product.
Users can use AI-recommended prompts when creating videos.

Question: Should we launch this feature? How do we measure its impact?
```

---

**解题思路 / Solution Approach**：

<!-- ZH-CN -->
```
第一层：采纳率（用户是否用？）
- 定义：使用了灵感提示词的用户 / 看到了提示词的用户
- 反映：提示词是否匹配用户需求

第二层：渗透率（用户真的用了？）
- 定义：真正使用提示词生成视频的用户 / 曝光用户
- 反映：功能是否有用

第三层：效果率（生成结果好吗？）
- 定义：生成后用户满意的比率
- 反映：提示词质量

第四层：留存率（用户还来吗？）
- 定义：使用提示词的用户 vs 未使用的用户留存对比
- 反映：功能是否提升用户粘性
```

<!-- EN -->
```
Layer 1: Adoption rate (Are users trying it?)
- Definition: Users who used prompts / Users who saw prompts
- Reflects: Whether prompts match user intent

Layer 2: Penetration rate (Are users actively using it?)
- Definition: Users who generated videos with prompts / Exposed users
- Reflects: Whether the feature is genuinely useful

Layer 3: Output quality rate (Are results good?)
- Definition: Satisfied outputs / Total generations
- Reflects: Prompt quality and relevance

Layer 4: Retention rate (Do users come back?)
- Definition: Retention comparison: prompt users vs. non-prompt users
- Reflects: Whether the feature drives user loyalty
```

---

**面试追问 / Follow-Up Q&A**：

| 问题 | 中文回答 | English Answer |
|------|---------|---------------|
| 除了结果效果，还有什么价值？ | 提效！用户不需要自己想提示词，缩短创作时间。 | Efficiency! Users don't need to craft prompts themselves, cutting creation time. |
| 怎么衡量提效？ | 看平均生成时长、使用次数。提效+效果好 = 用户满意度提升。 | Measure avg. generation time and usage frequency. Efficiency + quality = user satisfaction. |
| 如果要做付费，怎么设计？ | 核心指标：广告收入。观测指标：订阅率、付费转化率。AB测试：实验组付费提示词 vs 对照组免费提示词。 | Core: ad revenue. Secondary: subscription rate, paid conversion. A/B test: paid prompts vs. free prompts. |

---

### 案例二：AI选房工具效果评估 / Case 2: AI Property Tool Impact Assessment

**背景 / Background**：
<!-- ZH-CN -->
```
Company A 企业微信上线AI选房工具5个月。
业务想知道：工具是否带来转化率提升？
```

<!-- EN -->
```
Company A launched an AI property recommendation tool on Enterprise WeChat.
After 5 months, the business wants to know: Is the tool driving conversion rate improvement?
```

---

**评估框架 / Evaluation Framework**：

<!-- ZH-CN -->
```
1. 确定北极星指标
   - 企微商机转化率（公域→私域）
   - 客源带看量
   - 成交转化率

2. 拆解一级指标
   - 工具使用渗透率（60% vs 目标）
   - 推荐转化率（推荐→跟进）
   - 跟进转化率（跟进→成交）

3. 拆解二级指标
   - 经纪人日活
   - 话术发送率
   - 客户意向标签完善率

4. 评估方法
   - PSM+DID（匹配+差分）
   - 剔除季节/地域干扰
```

<!-- EN -->
```
1. Define North Star metrics
   - WeChat lead conversion rate (public → private)
   - Property showing requests
   - Deal closure rate

2. L1 metrics
   - Tool adoption rate (60% vs. target)
   - Recommendation → follow-up conversion
   - Follow-up → deal conversion

3. L2 metrics
   - Agent daily active users
   - Script message send rate
   - Customer intent tag completion rate

4. Evaluation method
   - PSM + DID (matching + differencing)
   - Removing seasonality and regional effects
```

---

**数据分析发现 / Data Analysis Findings**：

<!-- ZH-CN -->
```
问题1：被动使用
- 渗透率60%，但40%是偶发性
- 被动使用的经纪人商机量只有头部1/3

问题2：转化链路断裂
- 公域转私域只有28%
- 话术不规范、意向识别不及时

→ 针对性策略：分层运营+话术优化
→ 量化结果：转化率提升57%
```

<!-- EN -->
```
Issue 1: Passive usage inflating adoption
- 60% adoption rate, but 40% was accidental/passive taps
- Passive users generated only ⅓ of the leads of top-tier agents

Issue 2: Broken conversion funnel
- Public-to-private conversion was only 28%
- Inconsistent follow-up scripts, delayed intent recognition

→ Action: Segmented operations + script optimization
→ Result: Conversion rate improved 57%
```

---

### 案例三：物流平台撮合效率 / Case 3: Logistics Platform Matching Efficiency

**背景 / Background**：
<!-- ZH-CN -->
```
物流撮合平台（满帮/货拉拉类似）。
双边市场：货主发货 → 司机接单 → 运输完成。

问题：怎么评估平台撮合效率？
```

<!-- EN -->
```
A logistics matching platform (similar to Uber Freight / LoadRunner).
Two-sided marketplace: Shipper posts load → Driver accepts → Delivery completes.

Question: How do you evaluate platform matching efficiency?
```

---

**评估框架 / Framework**：

<!-- ZH-CN -->
```
北极星指标：
- 撮合成功率
- 货主留存率
- 司机留存率

一级指标：
- 发货响应时间
- 匹配转化率
- 完成履约率

二级指标：
- 货源发布量
- 司机在线时长
- 取消率
- 投诉率
```

<!-- EN -->
```
North Star metrics:
- Match success rate
- Shipper retention rate
- Driver retention rate

L1 metrics:
- Response time to shipment posts
- Match conversion rate
- Fulfillment rate

L2 metrics:
- Shipment post volume
- Driver online hours
- Cancellation rate
- Complaint rate
```

---

**数据分析方向 / Data Analysis Directions**：

<!-- ZH-CN -->
```
1. 用户分层
   - 高频发货货主 vs 低频
   - 活跃司机 vs 沉默司机

2. 流失分析
   - 为什么货主流失？响应慢、司机质量差、价格高
   - 为什么司机流失？单量少、结算慢、差评多

3. 匹配效率
   - 匹配算法优化空间
   - 供需平衡分析
```

<!-- EN -->
```
1. User segmentation
   - High-frequency shippers vs. low-frequency
   - Active drivers vs. dormant drivers

2. Churn analysis
   - Why do shippers churn? Slow response, poor driver quality, high prices
   - Why do drivers churn? Low order volume, slow payment, bad reviews

3. Matching efficiency
   - Room for algorithm optimization
   - Supply-demand balance analysis
```

---

### 案例四：内容平台增长策略 / Case 4: Content Platform Growth Strategy

**背景 / Background**：
<!-- ZH-CN -->
```
快手/抖音等短视频平台。
用户：创作者 + 消费者

问题：怎么用数据驱动用户增长？
```

<!-- EN -->
```
Short-video platforms (e.g., TikTok/Douyin, Kuaishou variants).
Users: Creators + Consumers

Question: How do you use data to drive user growth?
```

---

**增长框架 / Growth Framework**：

<!-- ZH-CN -->
```
北极星指标：DAU（日活）、用户时长、内容消费量

用户分层：
- 创作者：发布频率、内容质量
- 消费者：观看时长、互动率

增长策略：
1. 创作者激励
   - 新手任务引导
   - 优质内容补贴
   - 粉丝增长激励

2. 消费者召回
   - 流失用户识别
   - 个性化召回策略
   - 沉默用户激活

效果评估：AB测试、留存分析、LTV预测
```

<!-- EN -->
```
North Star metrics: DAU, time spent, content consumption volume

User segmentation:
- Creators: posting frequency, content quality
- Consumers: watch time, engagement rate

Growth strategies:
1. Creator incentives
   - Onboarding tasks for new creators
   - Quality content subsidies
   - Follower growth rewards

2. Consumer win-back
   - Identify churned users
   - Personalized re-engagement campaigns
   - Dormant user activation

Evaluation: A/B testing, retention analysis, LTV prediction
```

---

## 三、业务理解题 / Business Understanding Questions

### 3.1 常见问题 / Common Questions

<!-- ZH-CN -->
```
Q: 你对我们公司/行业了解多少？
Q: 你觉得XX行业有哪些痛点？
Q: 为什么考虑换行业？
Q: 你觉得哪些行业发展比较好？
```

<!-- EN -->
```
Q: How much do you know about our company/industry?
Q: What are the biggest pain points in this industry?
Q: Why are you considering a career change?
Q: Which industries do you think have the best growth prospects?
```

---

### 3.2 回答策略 / Answer Strategies

<!-- ZH-CN -->
```
✅ 好的回答示例：

行业认知：
- "房地产行业处于下行区间，但数字化转型有价值"
- "物流是实体经济核心，传统物流效率低，有优化空间"
- "AI内容创作是蓝海，创作者经济还在发展中"

公司了解：
- "XX公司做的是XX撮合，类似双边平台模型"
- "XX公司组织效率优化是挑战，也是机会"

个人规划：
- "希望找有发展前景的行业，同时能迁移我的数据分析能力"
- "传统行业数字化转型有机会"
```

<!-- EN -->
```
✅ Good answer examples:

Industry awareness:
- "The real estate industry is in a downturn, but digital transformation creates real value"
- "Logistics is the backbone of the physical economy — traditional logistics have major efficiency gaps"
- "AI-generated content is a blue ocean; the creator economy is still evolving"

Company knowledge:
- "XX company operates a two-sided marketplace for XX — similar to the agent-buyer model"
- "XX company's organizational efficiency is both a challenge and an opportunity"

Career goals:
- "I'm looking for a growing industry where I can apply my data analytics skills"
- "Digital transformation in traditional industries presents real opportunity"
```

---

### 3.3 了解公司的小技巧 / Tips for Researching a Company

<!-- ZH-CN -->
```
1. 面试前必看：
   - 公司官网/业务介绍
   - 最新财报（如果是上市公司）
   - 行业研究报告

2. 面试中获取：
   - "你们主要的业务线是什么？"
   - "这个岗位服务于哪个业务？"
   - "团队近期的挑战是什么？"

3. 体现主动性：
   - "我有了解到你们在XX方面有布局"
   - "我觉得这个和XX公司的模式有点像"
```

<!-- EN -->
```
1. Before the interview:
   - Company website and business overview
   - Latest earnings report (if public)
   - Industry research reports

2. During the interview:
   - "What are the main business lines?"
   - "Which business does this role support?"
   - "What are the team's biggest challenges right now?"

3. Show initiative:
   - "I noticed you're expanding in XX — that's interesting"
   - "I see parallels to the model at XX company"
```

---

## 四、AB测试设计题 / A/B Test Design

### 4.1 经典题型 / Classic Questions

<!-- ZH-CN -->
```
Q: 如果要上线XX功能，你怎么设计AB测试？
Q: 哪些指标可以衡量XX的效果？
Q: 样本量怎么算？
Q: 显著性怎么判断？
```

<!-- EN -->
```
Q: If you were launching XX feature, how would you design the A/B test?
Q: Which metrics can measure the impact of XX?
Q: How do you calculate the minimum sample size?
Q: How do you determine statistical significance?
```

---

### 4.2 AB测试设计模板 / A/B Test Design Template

<!-- ZH-CN -->
```
1. 确定核心指标（Primary Metric）
   - 转化率 / 留存率 / 收入 等
   - 必须是可量化的

2. 确定观测指标（Secondary Metrics）
   - 留存率、使用时长、满意度评分
   - 用来辅助判断

3. 计算最小样本量
   - 预期提升值
   - 基准值
   - 显著性水平（通常95%）
   - 统计功效（通常80%）

4. 设计分流策略
   - 用户随机分流
   - 保证实验组和对照组特征一致
   - 注意AA测试

5. 确定实验周期
   - 通常1-2周
   - 需要覆盖完整周期（如周周期）

6. 效果评估
   - p值检验
   - 置信区间
   - 效果稳定性
```

<!-- EN -->
```
1. Define the primary metric
   - Conversion rate / retention / revenue — must be quantifiable

2. Define secondary metrics
   - Retention, session duration, satisfaction score
   - Used as guardrails

3. Calculate minimum sample size
   - Expected lift
   - Baseline value
   - Significance level (typically 95%)
   - Statistical power (typically 80%)

4. Design traffic split
   - Random user-level assignment
   - Verify treatment/control group balance
   - Run AA test first to validate randomization

5. Set experiment duration
   - Typically 1–2 weeks
   - Must cover a full cycle (e.g., weekly pattern)

6. Evaluate results
   - p-value test
   - Confidence intervals
   - Result stability over time
```

---

### 4.3 面试追问应对 / Follow-Up Q&A

| 问题 | 中文 | English |
|------|------|---------|
| 小样本怎么办？ | 延长周期、降低显著性水平（谨慎）、回归分析、PSM+DID、贝叶斯方法 | Extend duration, lower significance threshold (cautiously), regression analysis, PSM+DID, Bayesian methods |
| 结果不显著怎么办？ | 看趋势不看绝对值、看细分人群、延长周期、接受阴性结果 | Look at trends not absolutes, analyze by segment, extend duration, accept null results |
| 两组差异大怎么办？ | 检查分流逻辑、看外部因素、做AA测试验证、重新分流 | Check split logic, look for external factors, run AA test to validate, re-randomize |

---

## 五、开放性问题 / Open-Ended Strategy Questions

### 5.1 经典题型 / Classic Questions

<!-- ZH-CN -->
```
Q: 如果让你用数据驱动XX业务增长，你怎么做？
Q: 你觉得XX业务最大的增长机会在哪？
Q: 怎么用数据分析提升用户体验？
```

<!-- EN -->
```
Q: If you were to use data to drive growth for XX business, what would you do?
Q: Where do you see the biggest growth opportunity for XX business?
Q: How would you use data analytics to improve user experience?
```

---

### 5.2 解题思路 / Problem-Solving Framework

<!-- ZH-CN -->
```
1. 理解业务
   - 这个业务是什么？
   - 目标用户是谁？核心价值是什么？

2. 找痛点
   - 用户旅程中哪里有问题？
   - 转化链路中哪里有流失？
   - 用户反馈中常见抱怨？

3. 提方案
   - 基于数据分析的洞察
   - 可以量化的预期收益
   - 落地的可行性

4. 评估方案
   - AB测试、ROI计算、风险评估
```

<!-- EN -->
```
1. Understand the business
   - What is the product/service?
   - Who are the target users? What is the core value proposition?

2. Find pain points
   - Where are the drop-offs in the user journey?
   - Where in the conversion funnel do users leave?
   - What are the most common user complaints?

3. Propose solutions
   - Based on data-driven insights
   - With quantifiable expected impact
   - With feasibility assessment

4. Evaluate solutions
   - A/B testing, ROI calculation, risk assessment
```

---

### 5.3 回答示例 / Sample Answer

<!-- ZH-CN -->
```
Q: 如果让你用数据驱动Company A业务增长，你怎么做？

A:
"我觉得Company A的核心是撮合：买家-经纪人-房源

增长机会在：
1. 经纪人端：提升工具使用效率
   - AI选房渗透率还有提升空间
   - 通过RFM分层做精细化运营

2. 房源端：优化匹配效率
   - 用户画像和房源标签匹配
   - 提升带看转化率

3. 整体链路：提升转化
   - 漏斗分析找到流失点
   - 针对性优化

我会先搭指标体系，然后通过数据分析找到机会点，
和产运对齐后推AB测试验证。"
```

<!-- EN -->
```
Q: If you were to drive growth for Company A using data, what would you do?

A:
"I believe Company A's core is a matching business: buyers ↔ agents ↔ listings

Growth opportunities:
1. Agent side: Improve tool adoption
   - AI tool penetration still has room to grow
   - RFM segmentation enables precision operations

2. Listing side: Optimize matching efficiency
   - Better user-profile to listing-tag matching
   - Improve showing-to-deal conversion rate

3. End-to-end: Improve funnel conversion
   - Funnel analysis to identify drop-off points
   - Targeted optimization at each stage

My approach: First build a KPI framework, then use data to identify opportunities,
align with product and ops teams, and validate with A/B tests."
```

---

## 六、反问环节问题推荐 / Questions to Ask the Interviewer

### 6.1 团队相关 / About the Team
<!-- ZH-CN -->
- "这个团队有多少人？怎么分工？"
- "分析师和产品/运营是怎么配合的？"
- "日常工作是什么？"

<!-- EN -->
- "How big is the team and how is work divided?"
- "How do analysts work with PMs and operations teams?"
- "What does day-to-day work look like?"

---

### 6.2 工作内容 / About the Role
<!-- ZH-CN -->
- "会用哪些数据工具？"
- "数据基建情况怎么样？"
- "分析流程是什么？"

<!-- EN -->
- "What data tools will I be working with?"
- "What's the data infrastructure like?"
- "What does the analytics workflow look like?"

---

### 6.3 发展相关 / Growth & Development
<!-- ZH-CN -->
- "这个岗位的发展路径是什么？"
- "公司对分析师的期望是什么？"
- "团队近期的挑战是什么？"

<!-- EN -->
- "What is the career path for this role?"
- "What does the company expect from analysts?"
- "What are the biggest challenges the team is currently facing?"

---

### 6.4 面试流程 / Process
<!-- ZH-CN -->
- "面试有几轮？"
- "什么时候会有反馈？"
- "后续流程是什么？"

<!-- EN -->
- "How many rounds of interviews are there?"
- "When can I expect to hear back?"
- "What are the next steps?"

---

## 七、高频业务场景汇总 / Common Business Scenarios by Industry

| 行业 / Industry | 北极星指标 / North Star | 一级指标 / L1 Metrics | 方法论 / Methods |
|----------------|----------------------|----------------------|-----------------|
| 电商 / E-commerce | GMV / 订单量 | 流量×转化率×客单价 | 漏斗分析 |
| 内容平台 / Content | DAU / 时长 | 发布量×消费率 | 留存分析 |
| 工具产品 / SaaS/Tools | 付费率 | 激活率×付费转化 | 漏斗分析 |
| 双边平台 / Marketplace | 撮合率 | 供给×需求×匹配效率 | 相关性分析 |
| 风控 / Risk | 违规率 | 识别率×误杀率 | 分类模型 |
| 增长 / Growth | LTV | 获客成本×留存×变现 | 归因分析 |
