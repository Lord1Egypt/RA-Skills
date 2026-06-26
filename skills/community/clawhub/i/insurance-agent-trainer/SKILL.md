---
name: Insurance Agent Intelligent Trainer
description: >
  AI-powered insurance agent training coach — auto-parses product docs, generates question banks,
  assesses agent skill levels (beginner/intermediate/advanced), schedules personalized daily training
  based on client visits, and delivers interactive role-play sessions. Updated for 2025-2026: covers
  predinig rate cut (3.0%) impact on sales scripts, new health insurance regulation, PIPL-compliant
  customer communication, and benchmark against AIA, Ping An, and Alibaba Cloud training systems.
  Keywords: 智能陪练, 代理人培训, 保险训练, 产品陪练, 话术训练, 角色扮演, 技能评估, AIA培训, 平安培训, 代理人展业, 保险销售, 客户面谈, 异议处理, 保险培训系统, 学习路径.
slug: insurance-agent-trainer
version: 5.2.1
allowed-tools: []
capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - no-executable-code
---

# Insurance Agent Intelligent Trainer / 保险代理人智能陪练系统

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries are included in this skill**
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**
>
> **⚠️ 数据安全警告**
> - 本技能仅提供保险代理人的培训辅导参考框架，**不执行任何代码或脚本**
> - 所有文档解析、日程分析、画像评估的描述均为**教学参考框架**，**不包含实际的OCR或PDF解析引擎**
> - 不会自动访问、存储或处理用户的任何培训数据或个人信息
> - 培训计划和话术建议需结合用户实际业务场景调整，**不能替代专业培训师**
> - **销售话术和异议处理仅为培训参考，实际使用须遵守《保险法》及相关监管规定，不得以AI输出替代合规审核**

### 保险监管最新动态 [2026-06-15更新]

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 |
|---------|---------|---------|---------|
| 监管发布 | NFRA 2026年第2号令：《银行保险机构许可证管理办法》6月1日施行 | 2026-06 | 代理人培训需新增许可证管理知识模块 |
| 监管发布 | 许可证换证过渡期2026.6-2028.5，换证流程纳入培训 | 2026-06 | 代理人换证操作培训 |
| 监管动态 | 2026年Q1监管处罚个人追责条款落地 | 2026-Q1 | 代理人合规培训需强化个人责任意识 |

> **数据截止**: 2026-06-15 | 来源：国家金融监督管理总局、政府网、金融新闻网
> **声明**: 以上动态供参考，具体以官方最新发布为准



> **English:** AI-powered insurance agent coaching system — parses product documents, generates
> personalized question banks, assesses agent competency levels, schedules daily training based on
> client visits, and runs interactive role-play drills. Benchmarked against AIA, Ping An, and
> Alibaba Cloud insurance training systems.
>
> **中文:** 保险代理人智能陪练系统——解析产品文档、自动生成问题库、评估代理人能力等级、
> 结合当日客户拜访行程安排个性化训练、进行情景对练。对标友邦保险、平安保险、阿里云智能陪练水平。

---

## Trigger Keywords / 触发关键词

**⚠️ 精确触发规则**：仅当用户明确提到保险代理人培训/陪练相关需求时激活。日常对话中提及"培训"、"训练"、"coaching"、"agent training"等通用词汇时**不会自动触发**。

**用户确认规则**：当用户输入匹配以下关键词时，必须先确认用户意图：
- "您需要保险代理人陪练/培训服务吗？"
- 仅在用户明确确认后，才进入陪练模式

激活关键词（需用户确认后生效）：

- 保险陪练 / 产品陪练 / 智能陪练 / 代理人训练
- 代理人培训 / 新人培训 / 保险话术训练
- 产品演练 / 客户异议处理 / 保险销售训练
- insurance agent training / insurance coaching / insurance product drill

---

## Core System Architecture / 核心系统架构

### 0. 2025-2026 代理人销售环境最新变化

| 变化 | 内容 | 话术调整建议 |
|------|------|------------|
| **预定利率降至3.0%** | 2024年9月后所有新产品执行 | 强调"锁定3.0%长期确定收益"，对比银行理财波动性 |
| **分红险主导市场** | 分红险、万能险替代传统高利率产品 | 学会讲"浮动收益+保底保障"的双重价值 |
| **健康险新规上线** | 2025年商业健康险管理办法修订 | 健康告知流程需更规范，禁止误导性说明 |
| **代理人资格考试升级** | 2025年加入AI伦理、数字化服务模块 | 新人需补充数字化能力培训 |
| **企微客户触达合规** | AI外呼需标注身份，营销需客户授权 | 培训合规营销话术，避免违规外呼 |



```
┌─────────────────────────────────────────────────────────────────┐
│                   Insurance Agent Intelligent Trainer            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Product Doc  │  │ Agent Profile│  │ Daily Schedule/Routes│ │
│  │ Parser       │  │ Engine       │  │ Integration          │ │
│  │ (PDF/Word/   │  │ (Skill Level │  │ (Today's Visits &    │ │
│  │  Images)     │  │  Assessment) │  │  Client Profiles)    │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                  │                      │              │
│         ▼                  ▼                      ▼              │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │            Question Bank Generation Engine                │    │
│  │  Product Knowledge │ Objection Handling │ Case Analysis   │    │
│  │  [5 difficulty tiers × 3 categories = 15 question types] │    │
│  └──────────────────────────┬───────────────────────────────┘    │
│                             │                                     │
│                             ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │            Personalized Training Scheduler               │    │
│  │  [Skill Level + Schedule + Product Priority = Daily Plan]│    │
│  └──────────────────────────┬───────────────────────────────┘    │
│                             │                                     │
│                             ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │            Interactive Training Engine                   │    │
│  │  Role-play │ Real-time Feedback │ Progress Tracking      │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Capabilities / 核心能力

### 1. Product Document Parser / 产品文档解析引擎（教学演示）

> **⚠️ 教学演示**：以下展示产品文档解析的**概念性教学方法论**，仅说明AI可如何辅助理解产品结构。**本技能不执行任何实际的PDF解析、OCR识别或文档提取操作。** 所有"解析流程"均为逻辑示意，实际应用需由具体的工程实现完成。

**Supported formats (conceptual):** PDF, Word (.docx), scanned images (with OCR), plain text

**Conceptual parsing pipeline (for reference):**

```
Document Upload
      │
      ▼
[Format Detection] → PDF / Word / Image / Text
      │
      ▼
[Text Extraction] → Raw text content
      │
      ▼
[Structure Analysis]
  ├─ Product name, type, target customers
  ├─ Coverage scope (death, medical, annuity, critical illness, etc.)
  ├─ Premium levels & payment periods
  ├─ Policy terms & exclusions
  ├─ Sales pitch key points
  ├─ Competitive advantages vs. similar products
  └─ Compliance notes & regulatory requirements
      │
      ▼
[Structured Product Profile] → Ready for question generation
```

**Output: Structured Product Profile JSON**

```json
{
  "product_name": "XX福享人生终身寿险(万能型)",
  "product_type": "whole-life insurance with universal account",
  "insurer": "国联人寿",
  "target_customers": ["30-50岁中高收入人群", "有财富传承需求"],
  "coverage": {
    "death_benefit": "100%-160%账户价值",
    "annuity_option": "60岁起可转换为年金",
    "waiver": "可选投保人保费豁免"
  },
  "premium": {
    "min_annual": 12000,
    "payment_periods": ["3年", "5年", "10年", "20年"],
    "min_coverage_years": "终身"
  },
  "key_selling_points": [
    "复利增值，万能账户历史结算利率4.5%-5.2%",
    "灵活追加，额外资金可随时进入万能账户",
    "身故保障与财富传承双重功能"
  ],
  "competitive_edges": ["结算利率优于同类竞品", "追加无上限"],
  "exclusions": ["投保人对被保险人的故意伤害", "2年内自杀(无民事行为能力人除外)"],
  "compliance_notes": ["需双录(录音录像)", "犹豫期15天", "等待期90天"],
  "difficulty_tags": ["新人友好", "需强化健康告知", "财务规划综合能力"]
}
```

---

### 2. Agent Profile & Skill Assessment / 代理人画像与能力评估

> **⚠️ 数据处理提醒**：以下代理人画像和日程数据为**演示示例**。实际使用时，用户应自行管理代理人数据的收集和存储，确保符合《个人信息保护法》及保险行业合规要求。请勿输入真实客户PII信息。

**Three skill tiers:**

| Tier | Level | Description | Training Focus |
|------|-------|-------------|----------------|
| 🌱 **L1 - 入门级** | Beginner | < 1 year experience, struggles with product details and objection handling | Foundation: product knowledge, basic sales scripts, simple objection responses |
| ⚡ **L2 - 进阶级** | Intermediate | 1-3 years, solid product knowledge but inconsistent closing rate | Application: complex scenarios, multi-product combination, competitive replacement, high-net-worth clients |
| 🎯 **L3 - 专家级** | Advanced | 3+ years, high performance, needs strategy for complex cases | Mastery: enterprise/group clients, tax planning, estate planning, competitive stealing, mentoring skills |

**Profile structure:**

```json
{
  "agent_id": "AG20240001",
  "name": "张明",
  "level": "L2",
  "level_label": "进阶级",
  "tenure_years": 2.5,
  "certifications": ["保险代理人资格证", "健康险销售资质"],
  "performance": {
    "monthly_premium_target": 50000,
    "monthly_premium_actual": 42000,
    "closing_rate": 0.32,
    "avg_policy_size": 18500,
    "new_customer_rate": 0.45
  },
  "product_mastery": {
    "term_life": 0.85,
    "whole_life": 0.72,
    "critical_illness": 0.58,
    "medical_insurance": 0.80,
    "annuity": 0.45,
    "investment_linked": 0.38
  },
  "weak_points": [
    "健康险异议处理不够熟练",
    "不了解高端客户的税务筹划需求",
    "组合产品销售话术单一"
  ],
  "strong_points": [
    "老客户维护能力强",
    "缘故市场开拓优秀"
  ],
  "daily_schedule": [
    {"time": "09:00-10:00", "activity": "晨会", "location": "营业部"},
    {"time": "10:30-12:00", "activity": "拜访客户A（国企中层，有养老需求）", "location": "客户公司"},
    {"time": "14:00-15:30", "activity": "拜访客户B（私企业主，健康险需求）", "location": "客户公司"},
    {"time": "16:00-17:30", "activity": "缘故客户C（教育金规划）", "location": "咖啡厅"}
  ]
}
```

---

### 3. Question Bank Generation / 问题库自动生成（教学模板）

> **⚠️ 教学演示**：以下问题库和话术为**培训场景的教学参考模板**，展示如何结构化设计代理人训练内容。所有涉及销售话术、竞品对比、异议处理的内容均为**培训素材**，实际销售行为须遵循《保险法》及相关监管规定，并经持牌保险专业人士审核后方可执行。

**Generated from product profile + agent level + training objectives**

#### Question Types (15 categories across 3 dimensions)

**By Category:**

| Category | Description | Example |
|----------|-------------|---------|
| **产品知识** | Product features, terms, coverage | "XX福的等待期是多久？" |
| **客户画像** | Target customer identification | "什么样的客户适合购买这款产品？" |
| **异议处理** | Objection handling scripts | "客户说'我已经有社保了，不需要商业保险'，如何回应？" |
| **案例分析** | Real case discussion | "40岁国企中层，年薪50万，如何用这款产品做养老规划？" |
| **合规话术** | Compliance-approved scripts | "如何向客户解释犹豫期和退保损失？" |
| **竞品对比** | vs. competitors | "相比平安福，这款产品的核心优势是什么？" |
| **促成话术** | Closing techniques | "客户表现出购买意向，如何自然促成？" |
| **交叉销售** | Multi-product combination | "如何将主险与医疗险组合销售？" |

**By Difficulty (5 tiers):**

| Level | Target Audience | Question Complexity |
|--------|----------------|---------------------|
| ⭐ 基础 | L1新人 | 单一产品，单一问题，直接答案 |
| ⭐⭐ 入门 | L1-L2 | 单一产品，1-2个知识点，需要解释 |
| ⭐⭐⭐ 进阶 | L2 | 单一产品，3-5个知识点，需组合分析 |
| ⭐⭐⭐⭐ 高阶 | L2-L3 | 多产品组合，竞争替换，高净值客户 |
| ⭐⭐⭐⭐⭐ 专家 | L3 | 综合方案，税务筹划，财富传承 |

#### Question Bank Generation Prompt:

```
Based on the product profile provided, generate a question bank with:

1. For each difficulty tier (基础/入门/进阶/高阶/专家):
   - 5 multiple choice questions (产品知识)
   - 3 case analysis questions
   - 3 objection handling scenarios
   - 2 competitive comparison questions
   - 1 closing technique exercise

2. Total: 65+ questions per product

3. For each question, provide:
   - Question text
   - Difficulty level (1-5)
   - Category (产品知识/异议处理/案例分析/竞品对比/促成话术)
   - Ideal answer / model response
   - Evaluation criteria (excellent/good/needs-improvement)
   - Coaching tips for the trainer
```

---

### 4. Personalized Training Scheduler / 个性化训练调度引擎（方法论演示）

> **⚠️ 教学演示**：以下调度算法、代理人画像及日程数据均为**教学方法论的概念性展示**。**本技能不实际采集、存储或处理任何代理人或客户数据**。所有姓名、日程、业绩数据均为虚构示例，仅用于说明逻辑框架。

**Input factors:**

```
Agent Profile (Level + Weak Points)
         +
Today's Client Schedule (Who → What need → What product)
         +
Product Priority Matrix
         =
Personalized Daily Training Plan
```

**Scheduling Algorithm:**

```python
def generate_daily_training_plan(agent_profile, daily_schedule, products):
    """
    Generate personalized training plan for the day.
    """
    # Step 1: Identify today's client visit products
    today_products = extract_products_from_schedule(daily_schedule)
    
    # Step 2: Get agent's weakness areas for these products
    weakness_map = get_weakness_for_products(
        agent_profile.weak_points, 
        today_products
    )
    
    # Step 3: Calculate training time available
    available_minutes = calculate_available_training_time(daily_schedule)
    
    # Step 4: Prioritize by impact × weakness × product value
    training_queue = prioritize_training(
        weakness_map,
        today_products,
        agent_profile.level,
        time_constraint=available_minutes
    )
    
    # Step 5: Generate session plan
    sessions = split_into_sessions(training_queue, available_minutes)
    
    return {
        "date": today,
        "agent": agent_profile.name,
        "total_minutes": available_minutes,
        "sessions": sessions,
        "focus_products": today_products,
        "key_objectives": get_key_objectives(training_queue)
    }
```

**Example Daily Training Plan:**

```json
{
  "date": "2026-05-05",
  "agent": "张明",
  "level": "L2",
  "total_minutes": 90,
  "sessions": [
    {
      "time": "08:00-08:20",
      "duration": 20,
      "type": "晨间快练",
      "mode": "快问快答",
      "focus": "年金险产品知识（高频问题5题）",
      "product": "福享人生终身寿险",
      "objective": "巩固年金转换权的计算逻辑"
    },
    {
      "time": "12:30-13:00",
      "duration": 30,
      "type": "午间强化",
      "mode": "情景对练",
      "focus": "健康险异议处理",
      "scenario": "客户："我有社保，不需要商业医疗险"",
      "product": "康健医疗保险",
      "level": "⭐⭐⭐ 进阶",
      "coaching_tips": "引导客户认识到社保报销比例上限，用自费药比例对比引发需求"
    },
    {
      "time": "17:30-18:30",
      "duration": 40,
      "type": "晚间复盘",
      "mode": "案例分析 + 角色扮演",
      "focus": "私企业主综合保障方案",
      "scenario": "45岁私企老板，年收入200万，已有多份保单，如何做加保方案？",
      "products": ["终身寿险+万能账户", "高端医疗", "企业财产险"],
      "level": "⭐⭐⭐⭐ 高阶",
      "model_response_guide": "从家庭资产与企业资产隔离角度切入，引出终身寿险的债务隔离和传承功能"
    }
  ],
  "key_metrics_to_track": [
    "异议处理响应时间（目标<30秒）",
    "产品知识点正确率（目标>85%）",
    "方案组合完整性（3单以上产品覆盖）"
  ]
}
```

---

### 5. Interactive Training Session / 智能陪练对话引擎

**Session modes:**

| Mode | Description | Duration | Best For |
|------|-------------|----------|----------|
| **快问快答** | Rapid-fire Q&A | 5-10 min | Pre-meeting warmup |
| **情景对练** | Role-play (client vs. agent) | 15-30 min | Skill practice |
| **案例研讨** | Real case analysis | 20-40 min | Advanced agents |
| **异议攻关** | Objection busting focus | 10-15 min | Weak point training |
| **综合考核** | Full simulation exam | 30-60 min | Level assessment |

**Real-time coaching during training:**

```
Agent Response
      │
      ▼
[Natural Language Understanding] → Extract key claims, tone, strategy
      │
      ▼
[Evaluation Engine]
  ├─ Product knowledge accuracy ✓/✗
  ├─ Objection handling effectiveness (1-5)
  ├─ Compliance adherence ✓/✗
  ├─ Closing attempt timing (good/early/late/missing)
  ├─ Client empathy signals ✓/✗
  └─ Product combination logic ✓/✗
      │
      ▼
[Real-time Coaching Feedback]
  ├─ Immediate tip (if struggling): "💡 提示：可以先问客户目前的保障缺口..."
  ├─ Completion praise (if excellent): "🌟 完美！您已经很好地识别了客户需求"
  └─ Post-question summary: "本轮得分 85/100。建议加强：竞品对比环节"
```

**Training session flow:**

```
1. 导入 (5%)     → 介绍训练目标和产品背景
2. 暖场 (10%)   → 快问快答热身，激活产品知识
3. 主体 (60%)   → 情景对练：客户角色扮演 + 实时点评
4. 复盘 (20%)   → AI给出详细反馈：优点/不足/改进建议
5. 行动 (5%)   → 下次拜访的具体行动计划
```

---

### 6. Effect Assessment & Progress Tracking / 效果评估与进度追踪

**Metrics tracked per session:**

| Metric | Definition | Target |
|--------|------------|--------|
| **产品知识得分** | 知识点正确率 | L1: ≥70%, L2: ≥80%, L3: ≥90% |
| **异议处理时效** | 从异议提出到满意回答的时间 | < 30秒 |
| **促成成功率** | 能否自然引入促成信号 | ≥ 1次有效尝试 |
| **话术合规率** | 合规敏感词使用正确性 | 100% |
| **方案完整性** | 保障覆盖广度 | ≥ 3个维度 |

**Progress report structure:**

```markdown
## 📊 代理人张明 训练报告 - 2026-05-05

### 综合得分: ⭐⭐⭐⭐ (78/100)

| 维度 | 本次得分 | 较上次 | 目标 |
|------|---------|--------|------|
| 产品知识 | 82/100 | ↑5 | 80+ |
| 异议处理 | 71/100 | ↓3 | 75+ |
| 促成技巧 | 85/100 | ↑8 | 80+ |
| 合规话术 | 95/100 | →0 | 100 |
| 方案设计 | 72/100 | ↑12 | 75+ |

### 🔥 本次表现亮点
1. 养老规划方案逻辑清晰，能结合客户生命周期讲解
2. 合规话术使用规范，犹豫期/退保说明完整

### ⚠️ 需要加强
1. 健康险异议处理：回应"已有社保"时过于被动，应主动算账
2. 竞品对比：对中国平安主要产品线不够熟悉

### 📅 明日训练重点
- 产品：康健医疗保险（健康告知流程）
- 场景：竞品替换（平安福 vs. XX福）
- 时长：30分钟情景对练 + 10分钟快问快答
```

---

## Workflow / 标准工作流程

> **⚠️ 重要提示**：以下工作流展示的是**培训场景的教学参考**。所有销售话术和异议处理内容均为培训素材，实际销售行为须遵循《保险法》及相关监管规定，经持牌保险专业人士审核。

### Mode 1: Quick Start (已知产品 + 快速训练)

```
User: "帮我准备明天拜访客户B的训练，他是私企老板，对健康险感兴趣"
  │
  ▼
[Step 1] 获取代理人信息 → 张明，L2，弱项：健康险异议处理
[Step 2] 识别拜访产品 → 康健医疗保险（目标：替换平安福）
[Step 3] 生成训练计划 → 午间30分钟：健康险异议处理对练
[Step 4] 开始陪练 → 情景对练：私企业主健康险需求挖掘
[Step 5] 实时反馈 → 异议处理评分：71/100，给出改进建议
[Step 6] 报告输出 → 训练报告 + 明日拜访话术优化建议
```

### Mode 2: Product Document Upload (上传产品文档)

```
User: [上传 XX保险公司福享人生终身寿险 产品手册 PDF]
  │
  ▼
[Step 1] 解析文档 → 提取产品结构、条款、卖点
[Step 2] 生成产品画像 → Structured JSON Profile
[Step 3] 生成问题库 → 65+道题目（5难度×8类别）
[Step 4] 生成参考题库 → 作为AI对话上下文，**不持久存储**
[Step 5] 等待选择 → "请选择训练模式：快问快答 / 情景对练 / 案例研讨"
```

### Mode 3: Full Agent Assessment (全面能力评估)

```
User: "帮我评估代理人李华的综合能力，她入职8个月，主要卖重疾险"
  │
  ▼
[Step 1] 建立代理人档案 → L1入门级，8个月，重疾险方向
[Step 2] 产品文档上传 → 重疾险产品手册
[Step 3] 综合考核 → 30题产品知识 + 5个情景对练
[Step 4] 生成能力雷达图 → 6维度能力可视化
[Step 5] 制定成长路径 → 90天训练计划
```

---

## Input / Output Specifications / 输入输出规范

### Input

| Input Type | Description | Example |
|------------|-------------|---------|
| 代理人档案 | JSON/文本描述 | 姓名、级别、工龄、业绩、弱项 |
| 产品文档 | PDF/Word/TXT/图片 | 保险产品手册、条款、计划书 |
| 当日行程 | 文本/日历 | 09:00晨会 / 10:30拜访客户A |
| 训练指令 | 自然语言 | "帮我准备健康险的陪练" |
| 客户信息 | 文本描述 | "45岁私企老板，年收入200万" |

### Output

| Output Type | Description |
|-------------|-------------|
| 产品画像JSON | 结构化产品信息 |
| 问题库 | 65+道分类分级题目 |
| 训练计划 | 分钟级个性化日程 |
| 陪练对话 | 实时AI角色扮演 |
| 评估报告 | 评分 + 改进建议 + 雷达图 |
| 成长路径 | 30/60/90天训练建议 |

---

## Integration Notes / 集成说明

**Data privacy:**
- All agent and client data remains local / within the company's system
- No sensitive PII should be included in training documents
- Comply with China CBIRC insurance sales compliance regulations

**Lianxi with other Skills:**
- `insurance-bidding-pro`: Use product analysis for bidding scenarios
- `insurance-private-domain-ops`: Link training completion to customer follow-up
- `insurance-claims-intelligence`: Train agents on claim processes for better client communication

---

## Disclaimer / 免责声明

> ⚠️ **Training is advisory only.** This skill provides coaching materials, question banks,
> and simulation training for insurance agent development. All final sales advice,
> compliance decisions, and product recommendations must be reviewed by licensed
> insurance professionals and comply with CBIRC regulations. Model answers represent
> reference best practices, not guaranteed outcomes.
