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
version: 5.2.9
allowed-tools: []
capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - illustrative-code-samples
---

# Insurance Agent Intelligent Trainer / 保险代理人智能陪练系统

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No runnable package is bundled:** the flow sketches, JSON samples and the short
  Python-style pseudocode below are illustrative reference material for you to adapt in
  your own environment; this skill ships no installer, service, parser or executable payload
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**
>
> **⚠️ 数据安全警告**
> - 本技能仅提供保险代理人的培训辅导参考框架，**不内置可运行的解析器、题库引擎或存储服务**；
  文中的流程示意、JSON 样例与伪代码均为教学参考，需由使用方在自己的系统中实现
> - 所有文档解析、日程分析、画像评估的描述均为**教学参考框架**，**不包含实际的OCR或PDF解析引擎**
> - 不会自动访问、存储或处理用户的任何培训数据或个人信息
> - 培训计划和话术建议需结合用户实际业务场景调整，**不能替代专业培训师**
> - **销售话术和异议处理仅为培训参考，实际使用须遵守《保险法》及相关监管规定，不得以AI输出替代合规审核**



> **🔒 数据最小化前置声明（2026-09-24 新增，使用任何模块前先执行）**
> 1. 只描述、不粘贴：客户信息以“45 岁私企老板、家庭年收入约 200 万”这类脱敏描述输入，禁止粘贴真实姓名、证件号、电话、住址、银行账号。
> 2. 代理人档案同样脱敏：`agent_id` 用编号，姓名可用“张**”或化名。
> 3. 训练记录默认只保留汇总指标（得分、弱项标签），不保留完整对话原文；确需保留须经本人同意并限定用途。
> 4. 任何要写入文件或对外发送的训练报告、话术稿，先在对话中完整展示给用户预览，经明确确认后再落盘/发送。

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

### 0. 2025-2026 代理人销售环境最新变化（截至 2026-11-24）

| 变化 | 内容 | 话术调整建议 | 对应培训模块 | 可信度标注 |
|------|------|------------|
| **预定利率降至3.0%** | 2024年9月后所有新产品执行 | 强调"锁定3.0%长期确定收益"，对比银行理财波动性 | 产品知识、促成话术 | 以官方最新发布为准 |
| **分红险主导市场** | 分红险、万能险替代传统高利率产品 | 学会讲"浮动收益+保底保障"的双重价值 | 产品知识、异议处理 | 以官方最新发布为准 |
| **健康险新规上线** | 2025年商业健康险管理办法修订 | 健康告知流程需更规范，禁止误导性说明 | 合规话术、情景对练 | 以官方最新发布为准 |
| **代理人资格考试升级** | 2025年加入AI伦理、数字化服务模块 | 新人需补充数字化能力培训 | 综合考核、新人路径 | 以官方最新发布为准 |
| **企微客户触达合规** | AI外呼需标注身份，营销需客户授权 | 培训合规营销话术，避免违规外呼 | 合规话术、直播带练 | 以官方最新发布为准 |
| **预定利率进一步下调至2.0%** | 2026年监管引导普通型人身险预定利率上限降至2.0%，分红/万能演示利率同步压降 | 话术从"锁定3.0%"转为"锁定2.0%长期确定+浮动分红对冲通胀" | 产品知识、养老规划 | 以官方最新发布为准 |
| **营销宣传合规强化** | 2026年整治"炒停售""夸大收益"，自媒体/直播带货纳入监管 | 培训合规表达，禁用绝对化收益承诺与演示红线 | 合规话术、直播带练 | 以官方最新发布为准 |
| **养老金融与税优扩容** | 个人养老金、商业养老金试点扩围，税优额度可期上调 | 强化养老规划与税优测算话术，绑定家庭现金流诊断 | 养老规划、税优保险 | 以官方最新发布为准 |
| **报行合一与费用约束延续** | 渠道费用与手续费率约束延续，代理人收入结构从"首年佣金"向"续期+服务"倾斜 | 培训从"单促成"转向"长期客户经营+续期服务"话术，弱化一次性冲规模表述 | 促成话术、客户经营 | 以官方最新发布为准 |
| **销售行为可回溯要求提高** | 双录、自媒体留痕、线上展业记录被更多用于检查 | 训练中同步演练"可回溯动作"：身份说明、条款重点提示、客户确认回执 | 合规话术、综合考核 | 以官方最新发布为准 |



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

**文档解析实操示例（2026-09-24 新增，示意）：**

| 步骤 | 输入（示意） | 提取要点 | 易错点 |
|------|-------------|---------|--------|
| 1 识别产品边界 | 产品手册封面 + 条款首页 | 产品全称、条款编号、适用险种 | 把附加险当成主险提取 |
| 2 抽取责任 | 保险责任章节 | 给付条件、给付比例、给付次数 | 漏掉"同一事故仅给付一次"限制 |
| 3 抽取责任免除 | 责任免除章节 | 逐条列出，标注条款号 | 只摘抄标题不摘内容 |
| 4 抽取费用与期间 | 费率表、条款附则 | 交费期间、等待期、犹豫期、宽限期 | 把等待期与犹豫期混淆 |
| 5 形成卖点与风险 | 全篇 | 3 条卖点 + 2 条风险提示 | 卖点写成绝对化收益承诺 |

**解析完的自检问题**：① 等待期、犹豫期、宽限期三个数字是否都取到了？② 责任免除是否逐条列出？
③ 卖点里有没有"保证""必然""最高"这类红线词？

**示例产品画像 2（重大疾病保险）：**
```json
{
  "product_name": "XX康健终身重疾险(2026版)",
  "product_type": "critical illness insurance",
  "insurer": "国联人寿",
  "target_customers": ["28-50岁家庭经济支柱", "有重疾保障缺口人群"],
  "coverage": {
    "ci_types": "120种重疾+20种中症+40种轻症",
    "multiple_payout": "重疾1次+中症2次+轻症3次，累计最高260%保额",
    "death_benefit": "身故赔已交保费或现金价值较大者"
  },
  "premium": {
    "sample": "30岁男，50万保额，30年缴，年缴约 6800 元",
    "payment_periods": ["10年","20年","30年"]
  },
  "key_selling_points": [
    "重疾+中症+轻症三重递进保障",
    "轻中症豁免后续保费",
    "可附加恶性肿瘤二次赔付"
  ],
  "exclusions": ["投保前已患重疾", "遗传性疾病（条款约定）", "等待期内出险"],
  "compliance_notes": ["重疾定义以监管规范为准", "需明确告知等待期90-180天", "如实健康告知义务"],
  "difficulty_tags": ["健康告知敏感", "条款专业度高", "需结合医疗知识"]
}
```

---

### 2. Agent Profile & Skill Assessment / 代理人画像与能力评估

> **⚠️ 数据处理提醒**：以下代理人画像和日程数据为**演示示例**。实际使用时，用户应自行管理代理人数据的收集和存储，确保符合《个人信息保护法》及保险行业合规要求。请勿输入真实客户PII信息。

**Three skill tiers:**

| Tier | Level | Description | Training Focus | 建议训练时长/周 |
|------|-------|-------------|----------------|----------------|
| 🌱 **L1 - 入门级** | Beginner | < 1 year experience, struggles with product details and objection handling | Foundation: product knowledge, basic sales scripts, simple objection responses | 5-8 小时（晨会快练+情景对练） |
| ⚡ **L2 - 进阶级** | Intermediate | 1-3 years, solid product knowledge but inconsistent closing rate | Application: complex scenarios, multi-product combination, competitive replacement, high-net-worth clients | 3-5 小时（聚焦弱项情景对练） |
| 🎯 **L3 - 专家级** | Advanced | 3+ years, high performance, needs strategy for complex cases | Mastery: enterprise/group clients, tax planning, estate planning, competitive stealing, mentoring skills | 2-3 小时（策略复盘+带教新人） |

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

**能力等级评定示例（2026-09-24 新增）：**

| 代理人 | 工龄 | 产品掌握度均值 | 成交率 | 弱项标签 | 评定等级 | 依据 |
|--------|------|---------------|--------|---------|---------|------|
| 示例A | 8 个月 | 0.62 | 0.18 | 条款细节、健康告知 | L1 入门级 | 工龄<1 年且产品掌握度均值<0.70 |
| 示例B | 2.5 年 | 0.70 | 0.32 | 组合销售、年金 | L2 进阶级 | 产品知识扎实但成交率波动大 |
| 示例C | 6 年 | 0.90 | 0.48 | 复杂传承架构 | L3 专家级 | 高成交率 + 高净值客户经营能力 |

**评级使用注意**：等级只用于安排训练强度，不用于人事考核；同一代理人不同产品线可落在不同等级，
建议按产品线条分别记录，避免用一个总分掩盖结构性短板。

**示例画像 2（L3 专家级）：**
```json
{
  "agent_id": "AG20230088",
  "name": "李华",
  "level": "L3",
  "level_label": "专家级",
  "tenure_years": 6,
  "certifications": ["保险代理人资格证", "CFP国际金融理财师", "私人银行家"],
  "performance": {
    "monthly_premium_target": 200000,
    "monthly_premium_actual": 235000,
    "closing_rate": 0.48,
    "avg_policy_size": 86000,
    "new_customer_rate": 0.62
  },
  "product_mastery": {
    "term_life": 0.95, "whole_life": 0.92, "critical_illness": 0.90,
    "medical_insurance": 0.93, "annuity": 0.88, "investment_linked": 0.82
  },
  "weak_points": ["家族信托等复杂传承架构经验不足", "跨境税务筹划需外部专家协同"],
  "strong_points": ["高净值客户经营", "企业团险开拓", "复杂方案设计"],
  "coaching_focus": ["传承架构进阶", "监管合规红线强化", "带教新人方法论"]
}
```

---

### 3. Question Bank Generation / 问题库自动生成（教学模板）

> **⚠️ 教学演示**：以下问题库和话术为**培训场景的教学参考模板**，展示如何结构化设计代理人训练内容。所有涉及销售话术、竞品对比、异议处理的内容均为**培训素材**，实际销售行为须遵循《保险法》及相关监管规定，并经持牌保险专业人士审核后方可执行。

**Generated from product profile + agent level + training objectives**

#### Question Types (15 categories across 3 dimensions)

**By Category:**

| Category | Description | Example | 考核重点 | 常见失分点 |
|----------|-------------|---------|---------|
| **产品知识** | Product features, terms, coverage | "XX福的等待期是多久？" | 条款准确性、关键利益点无误 | 把等待期答成犹豫期；漏讲除外责任 |
| **客户画像** | Target customer identification | "什么样的客户适合购买这款产品？" | 需求诊断与匹配逻辑 |
| **异议处理** | Objection handling scripts | "客户说'我已经有社保了，不需要商业保险'，如何回应？" | 共情+数据化反驳能力 | 直接否定客户、用恐吓式话术 |
| **案例分析** | Real case discussion | "40岁国企中层，年薪50万，如何用这款产品做养老规划？" | 方案完整性与定制化 |
| **合规话术** | Compliance-approved scripts | "如何向客户解释犹豫期和退保损失？" | 红线词零触发 | 使用"保本""稳赚""最高收益"等表述 |
| **竞品对比** | vs. competitors | "相比平安福，这款产品的核心优势是什么？" | 客观不贬损竞品 |
| **促成话术** | Closing techniques | "客户表现出购买意向，如何自然促成？" | 时机把握自然度 |
| **交叉销售** | Multi-product combination | "如何将主险与医疗险组合销售？" | 保障缺口覆盖度 |
| **养老规划** | 养老现金流与替代率测算 | "客户55岁期望退休月领8000，如何测算缺口？" | 测算逻辑与工具使用 |
| **税优保险** | 个人养老金/税优健康险政策应用 | "年缴1.2万养老金，节税多少？" | 政策准确、不夸大节税 |
| **客户经营** | 续期服务与转介绍 | "成交一年后的客户，如何自然开启加保话题？" | 服务触点设计、不打扰式回访 |
| **数字化展业** | 企微/自媒体合规触达 | "在朋友圈讲产品，哪些表述不能出现？" | 平台规则与监管红线双重合规 |

**By Difficulty (5 tiers):**

| Level | Target Audience | Question Complexity | 建议题量/次 |
|--------|----------------|---------------------|------------|
| ⭐ 基础 | L1新人 | 单一产品，单一问题，直接答案 | 10-15 题 |
| ⭐⭐ 入门 | L1-L2 | 单一产品，1-2个知识点，需要解释 | 15-20 题 |
| ⭐⭐⭐ 进阶 | L2 | 单一产品，3-5个知识点，需组合分析 | 20-30 题 |
| ⭐⭐⭐⭐ 高阶 | L2-L3 | 多产品组合，竞争替换，高净值客户 | 25-35 题 |
| ⭐⭐⭐⭐⭐ 专家 | L3 | 综合方案，税务筹划，财富传承 | 30-40 题 |

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

**示例生成题目（养老规划类别 / ⭐⭐⭐ 进阶）：**
- **题目**：客户 55 岁，当前社保养老金预计月领 3500 元，期望退休后月生活支出 8000 元，如何测算商业养老金缺口？
- **参考答案**：缺口 = (8000 - 3500) × 12 × 退休年限（按 25 年计）≈ 135 万；结合预期投资收益率反推年缴/趸交金额，并叠加通胀与医疗支出弹性。
- **评分**：优秀（准确测算+工具使用）/ 良好（逻辑正确但忽略通胀）/ 待改进（未考虑长寿风险）。
- **教练提示**：引导代理人用"替代率"概念切入，避免直接推销产品。

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

**示例计划 2（健康险异议攻坚日）：**
```json
{
  "date": "2026-08-12",
  "agent": "李华",
  "level": "L3",
  "total_minutes": 60,
  "sessions": [
    {
      "time": "13:00-13:20",
      "duration": 20,
      "type": "午间强化",
      "mode": "异议攻关",
      "focus": "健康险'已有社保'高频异议",
      "scenario": "客户：'我有医保，重疾险没必要'",
      "level": "⭐⭐⭐ 进阶",
      "coaching_tips": "用'医保目录外用药+收入补偿'双轴拆解，量化缺口而非否定客户"
    },
    {
      "time": "18:00-18:40",
      "duration": 40,
      "type": "晚间复盘",
      "mode": "案例研讨 + 角色扮演",
      "focus": "高净值客户重疾+医疗+寿险组合",
      "scenario": "50岁企业主，家庭年收入300万，已有多张保单如何查漏补缺？",
      "level": "⭐⭐⭐⭐ 高阶",
      "model_response_guide": "从企业资产与家庭资产隔离、重疾收入补偿、医疗高端资源三维度切入"
    }
  ],
  "key_metrics_to_track": [
    "异议处理响应时间（目标<25秒）",
    "方案组合维度（目标≥4个）",
    "合规红线触发（目标0次）"
  ]
}
```

---

### 5. Interactive Training Session / 智能陪练对话引擎

**Session modes:**

| Mode | Description | Duration | Best For | 适用场景 | 教练干预时机 |
|------|-------------|----------|----------|---------|
| **快问快答** | Rapid-fire Q&A | 5-10 min | Pre-meeting warmup | 晨会热身、拜访前激活产品知识 | 连续 2 题答错即给提示 |
| **情景对练** | Role-play (client vs. agent) | 15-30 min | Skill practice | 健康险/养老险高频异议实战 | 出现红线词立即打断纠正 |
| **案例研讨** | Real case analysis | 20-40 min | Advanced agents | 高净值综合保障方案设计 | 方案缺口遗漏 ≥2 项时给结构化提示 |
| **异议攻关** | Objection busting focus | 10-15 min | Weak point training | 单一弱项（如"已有社保"）专项突破 |
| **综合考核** | Full simulation exam | 30-60 min | Level assessment | 晋升/季度能力认证 |
| **直播带练** | 模拟自媒体/直播讲保险 | 15-25 min | 数字化展业 | 合规表达与镜头前讲产品 | 出现绝对化表述当场叫停并重录 |
| **续期服务演练** | 成交后回访与加保触达 | 10-20 min | 客户经营 | 续期提醒、理赔陪伴、转介绍开场 | 出现"推销感"过强时提示改为服务切入 |
| **红线词扫雷** | 集中训练合规表达 | 8-12 min | 全员必修 | 演示利益、收益承诺、停售炒作 | 命中即判不合格并给正确说法 |

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

**示例对练对话片段（健康险异议攻关）：**
```
AI(客户): "我单位福利好，重疾险真没必要买。"
Agent: "您说的对，单位福利是重要保障。不过重疾理赔是'确诊即付'的一笔钱——您想过没有，万一需要长期康复，单位会不会照发全额工资？"
AI(客户): "那倒不会，病假工资大概只发底薪……"
Agent: "这就是缺口。重疾险补的正是'收入中断+自费药'这两块。我们按您月支出算一下具体差额？"
[实时点评] ✅ 共情到位；✅ 用'收入补偿'替代'恐吓式'话术；⚠️ 下一步应主动给出测算而非直接推产品。
```

---

### 6. Effect Assessment & Progress Tracking / 效果评估与进度追踪

**Metrics tracked per session:**

| Metric | Definition | Target | 评估方式 | 提升抓手 |
|--------|------------|--------|---------|
| **产品知识得分** | 知识点正确率 | L1: ≥70%, L2: ≥80%, L3: ≥90% | 自动判分题库 + 人工抽检 | 错题回到条款原文定位，不靠背话术 |
| **异议处理时效** | 从异议提出到满意回答的时间 | < 30秒 | 对话时间戳测算 | 建"异议—回应"对照卡，形成肌肉记忆 |
| **促成成功率** | 能否自然引入促成信号 | ≥ 1次有效尝试 | 教练引擎标记 + 主管复核 |
| **话术合规率** | 合规敏感词使用正确性 | 100% | 合规词库实时监测 |
| **方案完整性** | 保障覆盖广度 | ≥ 3个维度 | 结构化评分表 |
| **合规红线触发率** | 触碰禁语/误导表述次数 | 0 次 | 实时拦截 + 事后复盘 | 红线词清单前置到每次对练开场 |

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
- Treat all agent and client data as sensitive: the user decides where it is stored.
  This skill itself stores nothing; keep PII inside your own controlled systems
- No sensitive PII should be included in training documents
- Comply with China CBIRC insurance sales compliance regulations

**Lianxi with other Skills:**
- `insurance-bidding-pro`: Use product analysis for bidding scenarios
- `insurance-private-domain-ops`: Link training completion to customer follow-up
- `insurance-claims-intelligence`: Train agents on claim processes for better client communication

---

## 保存与外发前确认 / Save & Send Confirmation（2026-09-24 新增）

1. 训练报告、话术稿、题库先在对话中完整展示，供用户逐段预览；
2. 用户明确确认后再写入文件或对外发送；未经确认不落盘、不发送；
3. 落盘时一并记录：生成时间、适用的产品条款版本、审核人。

---

## 变更记录 / Changelog

| 版本 | 日期 | 变更摘要 |
|------|------|---------|
| 5.2.5 | 2026-09-24 | 新增文档解析实操示例、能力等级评定示例、红线词扫雷与续期服务演练两种模式；环境变化表新增“对应培训模块/可信度标注”两列并补充报行合一、销售可回溯两条；题库与模式表新增维度列；修复 3 处未闭合代码块；修正能力与代码示例不一致的声明 |
| 5.2.4 | 2026-08-29 | 补充 2026 年预定利率与营销合规环境变化 |

---

## Disclaimer / 免责声明

> ⚠️ **Training is advisory only.** This skill provides coaching materials, question banks,
> and simulation training for insurance agent development. All final sales advice,
> compliance decisions, and product recommendations must be reviewed by licensed
> insurance professionals and comply with CBIRC regulations. Model answers represent
> reference best practices, not guaranteed outcomes.

## 本轮增量（2026-11-12）：复核维度与举例补充

> 本节为 2026-11-12 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**3. Question Bank Generation**：

- 每道题附「合规敏感点」标注（如不得承诺收益、不得贬损同业），判分 rubric 中把合规项错误设为一票否决项而非普通扣分项。
- 产品条款题须引用条款原文与页码，不用销售话术替代条款表述，并在题干中标注条款版本与生效日期以便追溯。

**5. Interactive Training**：

- 对「客户说别家更便宜」的异议场景，评分维度增加「是否先复述客户诉求再作对比」，不直接给反驳话术作为标准答案。
- 训练回放固定保留「输入、模型输出、评分、耗时、教练批注」五项留痕，供复盘与题库迭代；涉及客户信息一律脱敏后留存。

### 新增复核维度表（2026-11-12）

> 本表新增「由谁执行 / 数据来源 / 风险等级 / 复核要点 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 合规一票否决 | 合规岗 + 教练 | 合规词库 + 产品条款 | 敏感表述、条款引用准确性 | 高 | 培训用途，不替代产品信息披露 |
| 训练留痕 | 教练 | 训练平台记录 | 输入 / 输出 / 评分 / 耗时 / 批注五项 | 中 | 涉及客户信息须脱敏后留存 |

### 适用边界 / 数据最小化 / 执行边界（本期补齐）

**适用边界**：本技能仅用于保险代理人训练与通关考核的方法论参考与结构拆解，输出为供具备相应资质人员复核的草稿；不构成对具体主体、标的或客户的最终结论、指令或承诺。超出该范围的场景（如实盘执行、自动审批、对外正式报送）不适用本技能，应转由相应业务系统与授权人员处理。

**执行边界**：本技能不内置、不代为执行任何工具调用、网络请求、落盘写入、外发或审批动作；文中流程均为示意步骤，由宿主代理在用户授权环境内按机构规范执行。涉及不可逆或高影响动作须经人工预览与确认，并保留输入、输出、版本、耗时与责任人的最小留痕；无人工确认环节不得自动推进。

### 时效性说明

- 本期时效性核查：**截至 2026-11-12**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-16）：复核维度与举例补充

> 本节为 2026-11-16 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**1. Product Knowledge / 产品知识**：

- 知识点清单补「条款版本追踪」一列：每个产品知识点标注所依据条款的版本与生效日期，条款更新后旧题目标注待重编，不沿用旧版话术作标准答案。
- 保障责任对照新增「除外责任并列」要求：讲解某项保障时同屏列出对应除外责任与等待期，避免只展示正面责任造成理解偏差。

**4. Compliance Training / 合规训练**：

- 合规情景题新增「信息不足应对」考点：客户问题超出可核实信息时，正确作答应为如实说明并转由授权人员处理，而非自行补全产品细节。
- 话术评分表补「可核实性」维度：话术中每个具体数字与承诺须标注可核实的条款出处，无出处的一律按待核实扣分，交教练复核。

### 新增复核维度表（2026-11-16）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 条款版本与出处 | 教练 + 合规岗 | 产品条款 + 版本台账 | 知识点是否标注版本与生效日、是否有出处 | 高 | 培训用途，不替代产品信息披露 |
| 信息不足应对 | 教练 | 情景题库 + 评分 rubric | 是否如实说明并转授权、无出处是否扣分 | 中 | 训练草稿，涉及客户信息须脱敏 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于保险代理人训练与通关考核的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及真实销售、产品信息披露与对外承诺的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 时效性说明

- 本期时效性核查：**截至 2026-11-16**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-24）：复核维度与举例补充

> 本节为 2026-11-24 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**3. Question Bank Generation / 问题库生成（教学模板）**：

- 题库模板补一条「题目是否含可识别个人信息」的占位检查项，由使用者圈选并留白说明，草稿只保留占位标签。
- 为「难度分级」新增一张纸面对照：左列列难度标签，右列留白记录需人工校准的依据，不预置答案。

**6. Effect Assessment & Progress Tracking / 效果评估**：

- 评估草稿补一条「评分依据是否可追溯」的占位标注位，由使用者填写证据标签，分数留白。
- 为「明日训练重点」新增一行纸面提示位：标注待人工确认的训练项，具体安排留白。

### 新增复核维度表（2026-11-24）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 题目脱敏核对 | 题库维护人 + 复核人 | 题目占位清单 | 是否仅保留占位标签、未写入可识别个人信息 | 高 | 教学模板，草稿不对外使用 |
| 评分依据留痕 | 训练评估人 | 评估草稿 | 是否填写证据标签、分数留白待人工确认 | 中 | 文档记录，不构成人员考核结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于保险代理人训练题库与评估的纸面模板的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及正式培训结论、人员考核与对外发布的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 时效性说明

- 本期时效性核查：**截至 2026-11-24**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
