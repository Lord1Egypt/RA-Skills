# Insurance Agent Intelligent Trainer / 保险代理人智能陪练系统

> **English** — AI-powered insurance agent coaching platform. Auto-parses product documents,
> generates question banks, assesses agent competency (L1/L2/L3), schedules personalized daily
> training based on client visits, and runs interactive role-play drills. Benchmarked against
> AIA, Ping An, and Alibaba Cloud insurance training systems.

> **中文** — 保险代理人智能陪练系统。自动解析产品文档、生成问题库、评估代理人能力等级、
> 结合当日客户拜访行程安排个性化训练、进行情景对练。对标友邦保险、平安保险、阿里云智能陪练水平。

---

## ✨ Features / 核心功能

### 🚀 Product Document Parser / 产品文档解析
- **Input formats**: PDF, Word (.docx), scanned images (OCR), plain text
- **Output**: Structured JSON product profile with coverage, terms, selling points, exclusions
- **Official data**: Integrates with China Welfare Lottery & Sports Lottery public APIs for training case design

### 🎯 Question Bank Generator / 问题库自动生成
- **116+ questions** per product across **8 categories** × **5 difficulty tiers**
- Categories: Product Knowledge · Objection Handling · Case Analysis · Competitive Comparison · Closing Techniques · Compliance Scripts · Needs Discovery · Digital Planning
- Difficulty: ⭐基础 → ⭐⭐⭐⭐⭐专家 (L1–L3 agents)

### 👤 Agent Profiling & Assessment / 代理人画像与评估
- **3-tier competency model**: L1 (Beginner) / L2 (Intermediate) / L3 (Advanced)
- **6-dimension radar chart**: Product Knowledge · Needs Discovery · Objection Handling · Closing · Compliance · Customer Relations
- **Growth roadmap**: 30/60/90-day personalized development plans

### 📅 Personalized Daily Training Scheduler / 个性化训练调度
- Analyzes agent's daily client visit schedule
- Maps visit products → training focus areas
- Generates minute-level daily training plan with session recommendations

### 🗣️ Interactive Training Modes / 智能陪练模式
- **快问快答** — Rapid-fire Q&A warmup (5–10 min)
- **情景对练** — Role-play (15–30 min)
- **案例研讨** — Case analysis (20–40 min)
- **异议攻关** — Objection busting focus (10–15 min)
- **综合考核** — Full simulation exam (30–60 min)

### 📊 Real-time Effect Tracking / 效果实时追踪
- Session-level scoring (6 dimensions, 100-point scale)
- 30-day trend analysis with improvement indicators
- Radar chart visualization of competency progress

---

## 🚀 Quick Start

### Installation / 安装

```bash
# Install via ClawHub
openclaw skills install insurance-agent-trainer

# Or via npm
npx clawhub install @gechengling/insurance-agent-trainer
```

### Basic Usage / 基本使用

#### 1. Upload product document and generate question bank
```markdown
User: 请帮我解析[产品名称]的产品文档，并生成L2级别的问题库
→ AI: 解析文档 → 生成116道题目 → 输出问题库JSON + Markdown报告
```

#### 2. Create agent profile and get daily training plan
```markdown
User: 帮我安排代理人张明今天的训练计划，他今天要拜访3个客户（健康险+养老+教育金）
→ AI: 分析行程 → 评估弱项 → 生成3段训练（共90分钟）
```

#### 3. Start interactive training session
```markdown
User: 开始健康险的异议处理对练，我是L2级别
→ AI: 启动情景对练 → AI扮演客户 → 实时点评 → 训练报告
```

#### 4. Full agent competency assessment
```markdown
User: 帮我评估代理人李华的综合能力，她入职8个月，主攻重疾险
→ AI: 全面评估 → 能力雷达图 → 90天成长路径
```

---

## 📁 File Structure / 文件结构

```
insurance-agent-trainer/
├── SKILL.md                                    # 主技能文件（含完整工作流程）
├── README.md                                   # 本文件（双语）
├── references/
│   ├── question_bank_templates.md              # 问题库模板（8类别×5难度）
│   ├── agent_profile_template.md               # 代理人画像模板 + 成长路径
│   └── training_evaluation_rubric.md           # 训练效果评估量表
└── scripts/
    ├── product_parser.py                       # 产品文档解析 + 彩票数据获取
    ├── question_generator.py                   # 问题库自动生成器
    └── training_scheduler.py                   # 训练日程调度器
```

---

## 📋 Script Usage / 脚本使用

```python
# 1. 产品文档解析
from scripts.product_parser import parse_insurance_product_from_text

text = open("product_manual.txt").read()
profile = parse_insurance_product_from_text(text)
print(profile)

# 2. 官方数据获取（供训练案例使用）
from scripts.product_parser import get_training_case_data
ssq_data = get_training_case_data("ssq", limit=10)  # 双色球
dlt_data = get_training_case_data("dlt", limit=10)  # 大乐透

# 3. 生成问题库
from scripts.question_generator import generate_question_bank
qb = generate_question_bank(profile, agent_level="L2", questions_per_category=5)
print(f"生成 {qb['meta']['total_questions']} 道题目")

# 4. 生成每日训练计划
from scripts.training_scheduler import generate_daily_training_plan, format_training_plan_markdown
plan = generate_daily_training_plan(agent_profile, daily_schedule, ["健康险", "年金险"])
print(format_training_plan_markdown(plan))
```

---

## 🔗 Related Skills / 相关技能

| Skill | Relationship |
|-------|-------------|
| `insurance-bidding-pro` | Use product analysis for corporate insurance bidding |
| `insurance-private-domain-ops` | Link training completion to customer retention campaigns |
| `insurance-claims-intelligence` | Train agents on claims processes for better client communication |
| `insurance-actuarial-cn` | Deep actuarial knowledge for advanced product training |

---

## ⚠️ Disclaimer / 免责声明

> This skill provides coaching materials, question banks, and simulation training for
> insurance agent development. All final sales advice, compliance decisions, and product
> recommendations must be reviewed by licensed insurance professionals in compliance with
> China CBIRC regulations. Model answers represent reference best practices, not guaranteed outcomes.

---

## 📄 License / 许可证

MIT-0 — Free for commercial use, no attribution required.

---

*Built for China life insurance companies, insurtech platforms, and agency leaders.*
*为中国寿险公司、保险科技平台、营业部主管打造。*
