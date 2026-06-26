# 项目经历讲述框架与案例 / Project Storytelling Frameworks & Examples

---

## 一、STAR法则 / The STAR Framework

### 1.1 STAR框架 / STAR Structure

| 阶段 | EN | 含义 | 要点 |
|------|----|------|------|
| **S** | Situation | 背景 / Project context | 项目背景、业务场景、核心痛点 / Business context, scenario, key pain point |
| **T** | Task | 任务 / Your responsibility | 你的职责、面临的挑战、目标 / Your role, challenges, objectives |
| **A** | Action | 行动 / What you did | 具体做了什么、用了什么方法 / Steps taken, methods applied |
| **R** | Result | 结果 / Outcomes | 量化成果、验证方法、业务价值 / Quantified results, validation, business value |

---

### 1.2 讲述原则 / Storytelling Principles

<!-- ZH-CN -->
```
✅ 要点：
- 逻辑清晰：先框架后细节
- 用数据说话：所有成果量化
- 突出个人贡献：不是团队成果
- 展示方法论：用什么分析、为什么
- 体现业务价值：不只是技术炫技

❌ 禁忌：
- 背稿感太重
- 细节太多太碎
- 只有技术没有业务
- 说不清楚自己的角色
```

<!-- EN -->
```
✅ Do:
- Clear structure: framework first, then details
- Quantify everything: every result needs a number
- Own your contribution: this is your story
- Show methodology: what method and why
- Demonstrate business value: not just technical show-off

❌ Don't:
- Sound rehearsed
- Overload with tiny details
- Talk only tech with no business context
- Can't explain your specific role
```

---

## 二、项目故事模板 / Project Story Template

### 2.1 中文模板框架 / CN Template

```
【项目名称】
业务场景：

【背景】
- 业务目标是什么？
- 为什么做这个项目？
- 我的角色是什么？
- 团队有几个人？怎么分工？

【问题发现】
- 用什么数据/方法发现的？
- 发现的核心问题是什么？
- 数据支撑在哪里？

【分析方法】
- 用了什么方法论？
- 为什么选这个方法？
- 具体怎么做的？

【落地策略】
- 针对不同人群/场景的策略
- 怎么推动业务落地？
- 遇到什么阻力？

【量化结果】
- 核心指标提升多少？
- 怎么证明是项目的效果？
- 业务方认可吗？
```

### 2.2 English Template / English Template

```
[Project Name] | [Your Role] | [Duration]

Business Context:
- What was the business objective?
- Why was this project initiated?
- What was your specific responsibility?
- Team size and how work was divided?

Background:
- What problem were you trying to solve?
- What data/methods revealed the issue?

Analysis Approach:
- Which methodology did you use?
- Why was this method the right choice?
- Walk me through your process step by step

Action Plan & Execution:
- What strategies did you design for different user segments?
- How did you drive stakeholder buy-in?
- What obstacles did you face?

Quantified Results:
- What was the measurable impact?
- How did you validate the effect was real?
- Was the business satisfied with the outcome?

Personal Growth:
- What did you learn?
- What was your biggest challenge?
```

---

## 三、经典项目案例 / Worked Examples

### 案例一：AI选房工具分析（Company A）/ Case 1: AI Property Tool Analysis

**背景 / Background**：
<!-- ZH-CN -->
```
我在某头部互联网公司A负责企微项目的AI选房工具分析。
这是产运推出的新工具，上线5个月，
业务想知道工具是否带来核心指标（转化率、带看量）的提升。

我负责数据分析和策略建议，团队4人，
我主要对接前端获客和客源渗透率方向。
```

<!-- EN -->
```
At Company A, I led the data analysis for an AI-powered property recommendation
tool on the enterprise WeChat platform. This was a new tool launched by the
product and operations team. After 5 months live, the business wanted to know
if the tool was driving improvements in key metrics — conversion rate and showing volume.

My scope: data analysis and strategy recommendations. Team of 4.
I focused on top-of-funnel acquisition and private-channel lead penetration.
```

---

**问题发现 / Problem Discovery**：
<!-- ZH-CN -->
```
我用SQL从Hive仓提取了近万名经纪人的数据：
- 工具使用数据（推荐次数、发送次数）
- 客聊数据（对话频次、回复率）
- 交易数据（商机量、转化率）

Python清洗后发现两个核心问题：

问题1：渗透率虚高
- 工具使用渗透率60%，但40%是被动使用
- 偶发性推荐，非主动跟进
- 被动使用的经纪人商机量只有头部1/3

问题2：转化链路断裂
- 公域转私域渗透率只有28%
- 远低于业务预期
- 经纪人跟进话术不规范
```

<!-- EN -->
```
I extracted data on ~10,000 agents from Hive using SQL:
- Tool usage data (recommendation count, send count)
- Chat data (message frequency, reply rate)
- Transaction data (lead volume, conversion rate)

After cleaning in Python, two critical issues emerged:

Issue 1: Inflated adoption rate
- Tool adoption was 60%, but 40% was passive (accidental taps)
- These agents received recommendations but didn't actively follow up
- Passive users generated only ⅓ of the leads compared to active top-tier agents

Issue 2: Broken conversion funnel
- Public-to-private conversion was only 28%
- Far below business expectations
- Agents lacked standardized follow-up scripts
```

---

**分析方法 / Analysis Approach**：
<!-- ZH-CN -->
```
用RFM模型对经纪人做精细化分层：

R = 近30天使用天数
F = 近30天使用频次
M = 近30天客源量

分层结果：
- 忠粉用户：高频使用、高转化（20%）
- 先锋非忠粉：高潜但被动使用（30%）
- 低潜用户：低频低转化（50%）

结合K-means补充细分，发现：
- 潜在经纪人（高R低F有上升趋势）
- 高召回经纪人（低R但历史高F高M）
```

<!-- EN -->
```
Applied RFM model for agent segmentation:

R = Days of tool usage in last 30 days
F = Tool usage frequency in last 30 days
M = Leads generated in last 30 days

Segments:
- Loyal users: High frequency, high conversion (20%)
- Promising non-loyals: High potential, passive usage (30%)
- Low-potential users: Low frequency, low conversion (50%)

Supplemented with K-means clustering, which identified:
- Rising agents: High R, low F, but upward engagement trend
- At-risk power users: Low R, but historically high F and M
```

---

**落地策略 / Action Plan**：
<!-- ZH-CN -->
```
针对不同分层制定策略：

1. 先锋非忠粉（高潜经纪人）
   - 专项培训：工具使用技巧
   - 阶梯激励：客源倾斜
   - 解决被动使用问题

2. 忠粉用户
   - 话术更新：标准化跟进话术
   - 意向标签：增加客户意向识别
   - 解决跟进不及时问题

3. 低潜用户
   - 宣教推广：工具价值传递
   - 简化流程：降低使用门槛
```

<!-- EN -->
```
Different strategies for different segments:

1. Promising non-loyals (high-potential, passive users)
   - Targeted training sessions on tool usage
   - Tiered incentive program with lead allocation priority
   - Addressing passive engagement

2. Loyal users
   - Updated follow-up scripts (standardized)
   - Intent tagging for better customer identification
   - Solving delayed follow-up issues

3. Low-potential users
   - Tool value communication campaign
   - Simplified onboarding process to reduce friction
```

---

**量化结果 / Quantified Results**：
<!-- ZH-CN -->
```
用DID剔除季节/地域干扰后：

- 人均商机增长：111.9%
- 商机转化率：28% → 44%（+57%）
- 新房业绩增长：37.5%

业务方认可我们的分析，后续持续合作。
```

<!-- EN -->
```
Results (DID-adjusted, removing seasonality and regional effects):

- Leads per agent: +111.9%
- Lead conversion rate: 28% → 44% (+57%)
- New property revenue: +37.5%

The business accepted our analysis and we continued collaborating.
```

---

**面试追问应对 / Follow-Up Response Guide**：

| 问题 | 中文回答 | English Response |
|------|---------|----------------|
| DID是怎么做的？| 先用PSM匹配特征相近的两批经纪人（各300人），一组使用AI选房，一组未使用。再用DID计算实验前后的净效应。| I first used PSM to match 300 agents in the treatment group (AI tool users) with 300 comparable non-users. Then applied DID to calculate the net pre/post effect. |
| 样本量够吗？| 一开始有1万人，PSM匹配后各300人，线索量级1500-2000，用DID剔除了自然增长。| Started with ~10,000 agents. After PSM matching, had 300 per group with ~1,500–2,000 leads — sufficient for DID analysis. |
| 怎么判断显著性？| 计算了置信区间，看p值。核心指标在95%置信区间下显著。| Calculated confidence intervals and checked p-values. Key metrics were significant at the 95% level. |

---

### 案例二：达人治理评估（Company B）/ Case 2: Creator Policy Evaluation

**背景 / Background**：
<!-- ZH-CN -->
```
我在某头部互联网公司B做海外电商合规分析。
当时有个"轻量达人"政策——对优质达人放宽审核。
担心政策被滥用导致合规风险上升，
我需要评估政策对达人影响的净效应，
平衡合规和业务增长。
```

<!-- EN -->
```
At Company B, I worked on overseas e-commerce compliance analysis.
A "lightweight creator" policy was launched — relaxing review requirements
for top creators. There was concern about compliance abuse.
I needed to evaluate the net effect of this policy on creator retention,
balancing compliance with business growth.
```

---

**分析方法 / Analysis**：
<!-- ZH-CN -->
```
用PSM模型匹配：

特征变量：粉丝量、交易额、合规分数、活跃度
用Logistic回归算倾向性得分，
为政策组（享受轻量的）和对照组（没享受的）匹配相似达人。
然后对比两组的留存率。
```

<!-- EN -->
```
Applied PSM to match creators:

Features: follower count, transaction volume, compliance score, activity level.
Built a logistic regression to calculate propensity scores,
then matched creators who received the policy benefit with similar ones who didn't.
Compared retention rates between the two groups.
```

---

**结果 / Results**：
<!-- ZH-CN -->
```
优质达人次日留存率提升：15%
推动了申诉机制优化，
平衡了合规和业务增长。
```

<!-- EN -->
```
Day-2 retention for quality creators improved by 15%.
This informed an optimized appeals mechanism,
achieving a better balance between compliance and business growth.
```

---

### 案例三：指标体系搭建（通用）/ Case 3: KPI Framework Design

<!-- ZH-CN -->
**框架**：
```
1. 确定北极星指标
   - 例如：企微商机转化率

2. 拆解一级指标
   - 例如：工具使用率 × 转化率

3. 拆解二级指标
   - 例如：日活、话术发送率

4. 搭建监控看板
   - 实时监测指标变化
   - 设置预警阈值
```

**实战要点**：
```
- 口径要拉齐：和业务方确认定义
- 数据要准确：验证数据来源
- 看板要实用：面向运营，不要太复杂
- 预警要有效：避免false alarm
```

<!-- EN -->
**Framework**:
```
1. Define North Star metric
   E.g., WeChat lead conversion rate

2. Break down into L1 metrics
   E.g., tool adoption rate × conversion rate

3. Break down into L2 metrics
   E.g., daily active users, script send rate

4. Build monitoring dashboard
   - Real-time metric tracking
   - Alert thresholds configured
```

**Execution Tips**:
```
- Align definitions: confirm metric logic with stakeholders
- Validate data sources: ensure accuracy before building
- Keep dashboards practical: designed for operations, not too complex
- Set meaningful alerts: avoid alert fatigue
```

---

## 四、项目准备Checklist / Project Preparation Checklist

### 4.1 必须准备的内容 / Must-Prepare Per Project

<!-- ZH-CN -->
```
□ 项目名称和背景
□ 业务目标是什么
□ 我的角色和分工
□ 团队有几个人
□ 项目周期多长
□ 发现的问题（数据支撑）
□ 用了什么分析方法（原理）
□ 落地的策略是什么
□ 量化结果（百分比/倍数）
□ 怎么验证效果
□ 遇到的挑战和解决方案
□ 业务方反馈如何
□ 个人在项目的成长
```

<!-- EN -->
```
□ Project name and background
□ Business objective
□ My role and responsibilities
□ Team size
□ Project duration
□ Problem identified (with data backing)
□ Analysis methodology used (and why)
□ Action strategies deployed
□ Quantified results (% or ×)
□ How impact was validated
□ Challenges faced and how they were resolved
□ Stakeholder feedback
□ Personal growth from the project
```

---

### 4.2 量化成果的表达 / Quantifying Results

<!-- ZH-CN -->
```
❌ 不好的表达：
"效果还不错"
"有明显提升"
"带来了很大价值"

✅ 好的表达：
"商机转化率提升57%（28%→44%）"
"新房业绩增长37.5%"
"达人次留提升15%"
"人均商机增长111.9%"
```

<!-- EN -->
```
❌ Weak:
"Results were pretty good"
"There was a noticeable improvement"
"It created a lot of value"

✅ Strong:
"Lead conversion rate improved 57% (28% → 44%)"
"New property revenue grew 37.5%"
"Creator day-2 retention increased 15%"
"Leads per agent grew 111.9%"
```

---

### 4.3 方法论的讲解 / Methodology Explanation Checklist

<!-- ZH-CN -->
```
□ 是什么（1句话定义）
□ 解决什么问题（场景）
□ 怎么用（步骤）
□ 为什么选这个方法
□ 局限性是什么
□ 在我的项目中的应用
```

<!-- EN -->
```
□ What is it? (one-sentence definition)
□ What problem does it solve? (context)
□ How do you use it? (step-by-step)
□ Why did you choose this method?
□ What are its limitations?
□ How was it applied in your project?
```

---

## 五、面试常见追问 / Common Follow-Up Questions

### 5.1 关于项目本身 / About the Project

| 问题 / Question | 中文回答 | English Answer |
|----------------|---------|---------------|
| 项目是你主动发起的吗？/ Did you initiate this project? | 可以是主动发现问题，也可以是接的需求。关键是推进力。| It can be either — what matters is how you drove it forward. |
| 你具体负责什么？/ What was your specific role? | "我主要负责数据分析和策略建议，运营执行由产运负责"| "I owned the data analysis and strategy recommendations; operations execution was handled by product and ops teams." |
| 项目周期多长？/ How long did it take? | 3-4周（分析+落地），或持续性（指标监控）| 3–4 weeks for analysis and implementation, or ongoing for monitoring frameworks. |
| 数据量多少？/ What was the data volume? | "近万名经纪人"、"百万级交易数据"| "~10,000 agents", "millions of transaction records" |

---

### 5.2 关于分析方法 / About Methodology

| 问题 / Question | 中文回答 | English Answer |
|----------------|---------|---------------|
| 为什么选这个方法？/ Why this method? | "因为样本量小，传统AB不够显著，PSM+DID更适合"| "Sample size was small, making traditional A/B insufficient — PSM + DID was the right fit." |
| 有什么局限性？/ What are the limitations? | "PSM只能控制已观测变量，未观测的混杂因素无法控制"| "PSM can only control for observed confounders — unobserved variables remain a limitation." |
| 怎么验证效果？/ How did you validate results? | "用DID剔除自然增长，看置信区间和p值"| "DID removed organic growth; I validated using confidence intervals and p-values." |

---

### 5.3 关于业务价值 / About Business Value

| 问题 / Question | 中文回答 | English Answer |
|----------------|---------|---------------|
| 业务方认可吗？/ Were stakeholders satisfied? | "认可，后续持续合作" 或 "落地遇阻，调整了方案"| "Yes, we continued working together." Or "We faced adoption resistance and adjusted the approach." |
| 落地差距在哪？/ What's the gap between analysis and implementation? | "数据分析是建议权，落地需要业务方配合。我会做可视化看板方便他们观测效果"| "Data analysis is advisory — implementation requires stakeholder buy-in. I built dashboards to make results easy to track." |
