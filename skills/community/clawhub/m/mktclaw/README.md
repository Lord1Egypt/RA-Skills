<div align="center">

# 营销虾 MktClaw

**Demand-to-Delivery AI Agency**

[![Version](https://img.shields.io/badge/version-5.5.0-blue.svg)](./references/CHANGELOG.md)
[![Agents](https://img.shields.io/badge/agents-10-green.svg)](./agents)
[![Industries](https://img.shields.io/badge/industries-18-purple.svg)](./references/industries)
[![Protocols](https://img.shields.io/badge/protocols-12-orange.svg)](./references/_shared)
[![Architecture](https://img.shields.io/badge/architecture-Hot%20%7C%20Warm%20%7C%20Cold-red.svg)](#三层冷热分层架构)
[![SMM](https://img.shields.io/badge/SMM-L5%20Production-brightgreen.svg)](#自进化-triple-loop)
[![Evals](https://img.shields.io/badge/evals-75-informational.svg)](./evals/evals.json)
[![Compliance](https://img.shields.io/badge/compliance-GDPR%20%7C%20CCPA%20%7C%20PIPL-green.svg)](./references/_shared/privacy-compliance.md)
[![International](https://img.shields.io/badge/international-KR%20%7C%20JP%20%7C%20SEA%20%7C%20NA%20%7C%20EU%20%7C%20ME%20%7C%20CA%20%7C%20AF-blue.svg)](./references/industries/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](./LICENSE)

**AI 直接扮演 10 种代理商角色 · Triple Loop 自进化 · SMM L5 Production**

[中文](#中文) · [English](#english) · [变更日志](./references/CHANGELOG.md)

</div>

---

<a id="中文"></a>

## 中文

### 是什么

营销虾（MktClaw）是 **Demand-to-Delivery AI Agency**。AI 直接扮演代理商角色，沟通需求后**直接交付专业工作成果**（不是推荐代理商，而是替代 Junior 层的第一次提案起草）。

### 能做什么

| 用户场景 | AI 直接交付 |
|---------|-----------|
| 品牌从未做过品牌规划 | 品牌定位报告 + VI 方案 + 品牌手册大纲 |
| 双 11 Campaign | Big Idea + 传播策略 + Social 内容矩阵 + 排期表 |
| 小红书 KOL 种草 | 达人矩阵方案 + 种草策略 + 投放排期 + 预算 |
| 抖音直播从 0 到 1 | 搭建方案 + 选品排品 + 直播脚本 + 流量策略 |
| 营销预算优化 | MMM 建模（Python）+ 归因分析 + 预算再分配方案 |
| 品牌突发负面舆情 | 危机评估 + 应对策略 + 公关声明模板 + 媒体 Q&A |

### 10 种代理角色

| # | 角色 | 直接交付的成果 |
|---|------|--------------|
| 1 | 战略咨询顾问 | 品牌定位报告、竞争分析、增长策略、商业模式画布 |
| 2 | 品牌设计顾问 | 品牌策略文档、Logo 创意 Brief、VI 系统、品牌手册大纲 |
| 3 | 创意总监 | Big Idea、Campaign 策略、KV 创意简报、TVC 脚本、Social 内容矩阵 |
| 4 | 内容制作总监 | 拍摄脚本、分镜表、制作规范、内容排期表 |
| 5 | 媒介策划总监 | 媒介计划书、预算分配方案、投放策略、KPI 框架 |
| 6 | KOL 营销顾问 | 达人筛选策略、KOL 矩阵方案、种草内容策略 |
| 7 | MCN 运营顾问 | 账号矩阵规划、内容策略、变现模式设计 |
| 8 | 直播运营总监 | 直播间搭建方案、选品排品、直播脚本、流量策略 |
| 9 | 数据分析顾问 | 数据分析报告、MMM 建模（Python）、归因框架、预算优化方案 |
| **10** | **危机公关顾问** | **危机评估报告、应对策略、公关声明模板、媒体 Q&A、声誉修复方案** |

### 怎么用

用户视角只有 **3 个阶段**，AI 内部细节对用户透明：

```
1. 澄清需求  →  2. AI 交付成果  →  3. 用户确认
   (Clarify)      (Deliver)         (Confirm)
```

**两种模式**（可随时切换）：

| 模式 | 触发 | 确认节点 | 适用 |
|------|------|:--------:|------|
| **⚡ 快速模式** | 信息完整度 ≥50% 或 用户说"快速/直接开始/我是专家" | 0-1 次 | 老手、紧急、专业用户 |
| **📋 标准模式** | 默认 | 2-3 次 | 新手、模糊需求、复杂全案 |

> 单一 Agent 场景自动启用**一键交付**——跳过计划确认，直接产出成果。
> 全案场景（≥2 角色）自动启用 **Pitch 模式**——N Agent 并行生成 + Tournament 择优。

### 核心亮点

| 亮点 | 说明 |
|------|------|
| **三层冷热分层架构** | Hot（入口必读）→ Warm（按 type 加载）→ Cold（按需引用），Token 消耗降 76% |
| **12 大共享协议** | 质量自检 / 合规 / 创意多样性 / 数据连接器 / 运行时护栏 / 并行生成 / Campaign Vault / 品牌安全 / 隐私合规 / 性能埋点 / 方案指纹 / 输出规范 |
| **行业垂直知识层** | 10 国内行业 + 8 海外市场（KR/JP/SEA/NA/EU/ME/CA/AF）专属 KPI / 渠道权重 / 合规模块 |
| **Tournament + Adversarial** | Swiss-System 多方案 PK + Red Team 对抗式自检 + LLM-as-Judge 语义评分 |
| **框架层硬拦截** | 合规 Blocker 命中即阻断，用户不可豁免（除资质证明） |
| **Campaign Vault** | 用户私有投放数据库，按 Brand/BU 多租户隔离，自动沉淀投放效果 |
| **GDPR / CCPA / PIPL** | 完整隐私合规声明 + 数据留存/删除机制 |
| **能力诚实声明** | 明确 AI 不能做什么（客户政治 / 突破性创意 / 现场执行），不夸大能力 |
| **Triple Loop 自进化** | L7 Monitor → L7.5 Feedback → L6 Learning → L6.5 Knowledge Update → 自动版本递增，技能持续自我优化 |

<a id="自进化-triple-loop"></a>

### 自进化：Triple Loop 闭环架构

mktclaw 是**首批实现完整 Triple Loop 自进化的 AI Skill**（基于 SkillForge SMM v4.0），技能能持续从生产数据中学习并自我优化：

```
Loop 1 — Execution:    L2 Creator → L2.5 Execution → L5 Validator
Loop 2 — Optimization: L2.5 → L3 Auditor → L3.5 Regression → L4 Optimizer → re-L2.5
Loop 3 — Evolution:    L7 Monitor → L7.5 Feedback → L6 Learning → L6.5 Update → L2  ← 自进化
```

**一键自进化命令**：

```bash
# 完整 Triple Loop（生产环境周期性执行）
python scripts/harness_runner.py --log session.json --gate-check --learn --evolve --bump-version

# 仅学习模式（生成 learning_report.json 供人工审核）
python scripts/harness_runner.py --log session.json --learn

# 审核模式（所有变更标记为待审核）
python scripts/harness_runner.py --log session.json --learn --evolve --review-mode
```

**自进化管道组件**：

| 组件 | 层级 | 职能 |
|------|------|------|
| `runtime_monitor.py` | L7 | PPAF 追踪 + R.E.S.T 四维评分 + 失败模式检测 |
| `feedback_engine.py` | L7.5 | 信号提取 / 去重 / 优先级排序 / 趋势分析 |
| `learning_engine.py` | L6 | 模式提取 + 历史合并 + Creator vNext 指令生成 |
| `knowledge_updater.py` | L6.5 | 知识库文件更新 + 白名单安全 + 自动备份 + 回归测试 |
| `harness_runner.py` | 管道 | L7→L7.5→L5→L6→L6.5→Version Bump 一键串联 |

### 三层冷热分层架构

```
┌─ Hot Layer（入口必读，常驻上下文）─────────────────────┐
│  SKILL.md + 3 根 agent + agency-types.md               │
└────────────────────────────────────────────────────────┘
           │
           ↓ (Router 决定 type 后才加载)
┌─ Warm Layer（按需加载，仅当前 type）────────────────────┐
│  agents/types/{type}/main-agent.md + workflow.yaml     │
└────────────────────────────────────────────────────────┘
           │
           ↓ (Type Agent 内部需要时才引用)
┌─ Cold Layer（按需引用，绝不预读）───────────────────────┐
│  references/**.md (含 _shared/ 12 共享协议)             │
│  tools/ (load_industry_knowledge / load_shared_protocol)│
└────────────────────────────────────────────────────────┘
```

### 文件结构

```
mktclaw/
├── SKILL.md                          ← 架构入口
├── config.yaml                       ← 加载策略 + 路由 + Agent + Runtime Harness 配置
├── version.json                      ← 版本 SSOT（单一版本源）
├── api-spec.md                       ← RESTful API + MCP Server 接口
│
├── agents/
│   ├── intake-agent.md               ← 需求澄清
│   ├── router-agent.md               ← 角色路由
│   ├── transition-agent.md           ← 全案串联
│   └── types/                        ← 10 种代理角色（每 type 2 文件）
│       ├── strategy-consulting/
│       ├── brand-design/
│       ├── creative-agency/
│       ├── content-production/
│       ├── media-agency/
│       ├── kol-agency/
│       ├── mcn/
│       ├── live-streaming/
│       ├── data-analytics/
│       └── crisis-pr/
│
├── workflows/
│   ├── routing-workflow.yaml
│   └── parallel-workflow.yaml
│
├── tools/                            ← 工具化懒加载
│   ├── load_industry_knowledge.md
│   └── load_shared_protocol.md
│
├── scripts/                          ← Triple Loop 自进化管道
│   ├── runtime_monitor.py            ← L7 Runtime Monitor（PPAF + R.E.S.T + 失败模式）
│   ├── feedback_engine.py            ← L7.5 Feedback Engine（信号提取 + 优先级排序）
│   ├── learning_engine.py            ← L6 Learning Engine（模式提取 + Creator vNext）← v5.5 新增
│   ├── knowledge_updater.py          ← L6.5 Knowledge Updater（知识库更新 + 回归测试）← v5.5 新增
│   ├── harness_runner.py             ← L7→L7.5→L5→L6→L6.5→Version 一键管道
│   ├── test_runner.py                ← Eval 自动化 + --gate-check 门禁
│   └── templates/
│       └── session_log_template.json
│
├── schemas/                          ← JSON Schema 校验（5 个）
│   ├── session_log_schema.json
│   ├── l7_report_schema.json
│   ├── feedback_report_schema.json
│   ├── learning_report_schema.json   ← v5.5 新增
│   └── knowledge_update_schema.json  ← v5.5 新增
│
├── references/
│   ├── _shared/                      ← 12 共享协议
│   ├── industries/                   ← 18 行业知识库（10 国内 + 8 海外）
│   ├── CHANGELOG.md                  ← 版本演进历史
│   ├── agency-types.md
│   ├── creative-brief-template.md
│   ├── marketing-frameworks.md
│   └── ... (12 个字典文件)
│
└── evals/
    └── evals.json                    ← 75 条测试用例
```

### 版本历史

完整变更见 [CHANGELOG.md](./references/CHANGELOG.md)。

| 版本 | 里程碑 |
|------|--------|
| v4.0 | Demand-to-Delivery AI Agency 范式确立 |
| v5.0 | 三层冷热分层 + 共享层抽取，Token -76% |
| v5.1 | 行业垂直层 + 合规护栏 + Swiss-System + LLM-as-Judge |
| v5.2 | 框架层硬拦截 + Pitch 模式 + Campaign Vault + 工具化懒加载 |
| v5.2.1 | GDPR/CCPA/PIPL + 品牌安全 + 8 海外市场 + 方案指纹 + 自动降级 |
| v5.3.0 | L7 Runtime Monitor + L7.5 Feedback Engine + PPAF 追踪 + R.E.S.T 评分 + 失败模式检测 |
| v5.4.0 | version.json SSOT + harness_runner 自动化管道 + L5 Validator 量化门禁 + Baseline 管理 + L3.5 回归引擎 + JSON Schema + PPAF 精确采集 |
| **v5.5.0** | **Triple Loop 自进化闭环：L6 Learning Engine + L6.5 Knowledge Updater + Creator vNext 指令生成 + auto_apply/require_review/archive 决策门禁 + 版本自动递增 + 回归测试集成 + SMM L5 Production** |

---

<a id="english"></a>

## English

### What is MktClaw

MktClaw is a **Demand-to-Delivery AI Agency**. AI directly acts as agency professionals, communicating with users to clarify needs, then **delivering professional work products** (replacing Junior-level first-draft proposals, not Senior decision-making).

### 10 Agency Roles

| # | Role | Deliverables |
|---|------|--------------|
| 1 | Strategy Consultant | Brand positioning, competitive analysis, growth strategy |
| 2 | Brand Designer | Brand strategy, Logo brief, VI system, brand manual |
| 3 | Creative Director | Big Idea, Campaign strategy, TVC script, Social matrix |
| 4 | Content Producer | Shooting script, storyboard, production specs |
| 5 | Media Planner | Media plan, budget allocation, KPI framework |
| 6 | KOL Strategist | Influencer matrix, seeding strategy |
| 7 | MCN Operator | Account matrix, content strategy, monetization |
| 8 | Livestream Director | Studio setup, product selection, livestream script |
| 9 | Data Analyst | Analysis report, MMM (Python), attribution |
| **10** | **Crisis PR** | **Assessment, response strategy, PR statements, media Q&A** |

### Workflow (User-Visible)

```
1. Clarify  →  2. Deliver  →  3. Confirm
```

- **Fast Mode**: 0-1 confirmation, for experienced users
- **Standard Mode**: 2-3 confirmations, for complex cases
- **One-Click Delivery**: auto-triggered for single-role tasks
- **Pitch Mode**: N agents parallel generate + Tournament selection

### Highlights

- **Three-Tier Architecture**: Hot/Warm/Cold loading reduces tokens by 76%
- **12 Shared Protocols**: quality / compliance / diversity / data / runtime-guard / parallel / vault / brand-safety / privacy / telemetry / fingerprint / output-spec
- **18 Industry Knowledge Bases**: 10 domestic + 8 international markets
- **Tournament + Adversarial**: Swiss-System pairwise PK + Red Team attack + LLM-as-Judge
- **Framework-Level Guardrails**: compliance blockers cannot be user-bypassed
- **Campaign Vault**: multi-tenant private database with GDPR/CCPA/PIPL compliance
- **Capability Honesty**: explicitly declares what AI cannot do
- **Triple Loop Self-Evolution**: L7→L7.5→L6→L6.5→L2 closed loop — skill continuously learns from production data and self-optimizes (SMM L5 Production)

### Version History

See [CHANGELOG.md](./references/CHANGELOG.md) for full history.

| Version | Milestone |
|---------|-----------|
| v4.0 | Demand-to-Delivery paradigm |
| v5.0 | 3-tier loading + shared layer, -76% tokens |
| v5.1 | Industry verticals + compliance + Swiss-System |
| v5.2 | Framework guardrails + Pitch mode + Campaign Vault |
| v5.2.1 | GDPR + Brand Safety + 8 intl markets + fingerprint + auto-degradation |
| v5.3.0 | L7 Runtime Monitor + L7.5 Feedback Engine + PPAF + R.E.S.T + failure mode detection |
| v5.4.0 | version.json SSOT + harness_runner pipeline + L5 Validator gates + Baseline mgmt + L3.5 regression + JSON Schema + PPAF precision |
| **v5.5.0** | **Triple Loop self-evolution: L6 Learning Engine + L6.5 Knowledge Updater + Creator vNext + auto_apply/require_review/archive gates + auto version bump + regression testing + SMM L5 Production** |

---

## 加入群聊

<div align="center">
  <img src="https://qomob.ai/xskill.jpg" width="600" alt="XSkill">
</div>
