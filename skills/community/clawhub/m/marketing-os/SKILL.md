---
name: marketing-os
description: AI Agent 营销操作系统 — 包含 Virtual CMO（战略大脑）和 Marketing Operator（执行引擎），提供市场分析、策略制定、Campaign 规划与执行追踪全链路能力。
tags:
  - marketing
  - strategy
  - campaign-management
  - growth
  - cmo
  - execution
  - analytics
  - openclaw
version: "1.0.0"
---

# 🚀 Marketing OS — AI Agent 营销操作系统

## 概述

Marketing OS 是一个模块化、Schema 驱动的营销智能系统，设计为可直接接入任何 AI Agent Runtime 的 Skill Package。

它提供两个核心角色：

| 角色 | 功能 |
|------|------|
| **Virtual CMO** | 战略大脑 — 市场分析、机会识别、策略制定 |
| **Marketing Operator** | 执行引擎 — 任务分解、Campaign 管理、指标追踪 |

两个角色通过**结构化协作协议** (`schemas/cmo_to_operator.schema.json`) 通信，确保战略到执行零歧义。

---

## 使用场景

| 场景 | 触发方式 |
|------|----------|
| 市场发现 | "分析当前市场机会并生成战略建议" |
| Offer 选择 | "从已识别的机会中选择最佳产品匹配" |
| Campaign 规划 | "把策略拆解为可执行任务" |
| 执行冲刺 | "执行所有任务并收集指标反馈" |

---

## 技能调用格式

```yaml
skill: marketing-os
input:
  mode: market_discovery | offer_selection | campaign_planning | execution_sprint
  business_context:
    company_name: "公司名称"
    products: ["产品1", "产品2"]
    target_market: "目标市场"
    budget_range: "预算范围"
    brand_positioning: "品牌定位"
  market_data:            # 可选 — 外部市场信号
    search_trends: []
    competitor_moves: []
    audience_signals: []
  mission_id: "xxx"       # campaign_planning / execution_sprint 时必填
  auto_mode: false        # 是否全自动执行
```

---

## 系统架构

```
┌─────────────────────────────────────────────────┐
│                  Agent Runtime                   │
├─────────────────────────────────────────────────┤
│                                                  │
│   ┌──────────────┐     ┌─────────────────────┐  │
│   │ Virtual CMO   │────▶│ Marketing Operator  │  │
│   │ (Strategy)    │◀────│ (Execution)         │  │
│   └──────┬───────┘     └──────────┬──────────┘  │
│          │                        │              │
│   ┌──────▼────────────────────────▼──────────┐  │
│   │              Shared Memory                │  │
│   │  (insights / campaigns / learnings)       │  │
│   └──────────────────────────────────────────┘  │
│          │                        │              │
│   ┌──────▼──────┐   ┌────────────▼───────────┐  │
│   │  Workflows   │   │      Adapters          │  │
│   │  (flow.json) │   │  (CRM/Data/Content)    │  │
│   └─────────────┘   └───────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 核心模块

### 1. 🧠 Virtual CMO — 战略分析

**执行步骤**：
```
Step 1: 收集市场数据（信号、趋势、竞争对手动态）
Step 2: 分析信号 — 分类、评分（signal_strength 1-10）
Step 3: 识别机会 — 聚类相关信号，评估市场规模/竞争/匹配度
Step 4: 计算优先级 — priority_score = (信号强度×0.3) + (市场规模×0.25) + (能力匹配×0.25) + (紧迫度×0.2)
Step 5: 生成策略 — 定位、渠道推荐、KPI、风险评估
Step 6: 输出任务简报 — 传递给 Marketing Operator
```

**输出格式**（`schemas/cmo_output.schema.json`）：
```json
{
  "analysis_id": "UUID",
  "market_opportunities": [{"title": "...", "priority_score": 85, "confidence": "high"}],
  "target_segments": [{"name": "...", "pain_points": ["..."]}],
  "recommended_actions": [{"action": "...", "priority": "high", "owner": "operator"}],
  "risks": [{"description": "...", "severity": 7, "mitigation": "..."}],
  "next_steps": [{"action": "...", "owner": "operator", "deadline_type": "immediate"}],
  "confidence_level": 78
}
```

### 2. ⚙️ Marketing Operator — 任务执行

**执行步骤**：
```
Step 1: 验证 CMO Mission Brief
Step 2: 任务分解 — 将 action 拆成原子任务（每个任务有 owner/deadline/expected_result）
Step 3: 资源分配 — 预算、渠道、工具映射
Step 4: Campaign 组装 — 聚合任务，设置 KPI 目标
Step 5: 执行追踪 — 状态管理（pending → in_progress → completed/blocked/failed）
Step 6: 指标收集 — 量化（曝光/点击/转化）+ 定性（互动质量/品牌感知）
Step 7: 生成反馈 — 向 CMO 报告结果、学习、建议调整
```

---

## 协作协议

CMO → Operator 通信格式（`schemas/cmo_to_operator.schema.json`）：
```json
{
  "mission_id": "UUID",
  "objective": "明确的可衡量目标",
  "target_audience": {"segment_name": "...", "pain_points": ["..."]},
  "strategy": {"positioning": "...", "approach": "..."},
  "priority": "critical | high | medium | low",
  "recommended_channels": [{"channel": "LinkedIn", "priority_rank": 1}],
  "actions": [{"action": "...", "priority": "high"}],
  "success_criteria": {"primary_kpi": {"metric": "conversions", "target": "100"}}
}
```

Operator → CMO 反馈格式（`schemas/feedback.schema.json`）：
```json
{
  "feedback_id": "UUID",
  "execution_result": "事实总结",
  "metrics": {"impressions": 15000, "clicks": 450, "conversions": 23},
  "learnings": ["[MEASURED] LinkedIn 数据驱动标题 3x 互动率"],
  "recommendations": ["将 30% 预算从 Display 转移到 LinkedIn"]
}
```

---

## 行为规则

> [!IMPORTANT]
> 系统内建以下严格约束：
> - ❌ 不允许模糊建议（"考虑"、"或许"、"可以试试" 一律禁止）
> - ✅ 必须给出优先级（critical / high / medium / low）
> - ✅ 必须给出下一步行动
> - ✅ 必须给出风险评估
> - ✅ 必须区分 [FACT] / [INFERENCE] / [RECOMMENDATION]
> - ✅ 信号强度 < 4 必须标记 "uncertain"
> - ✅ 信息不足必须明确声明 "INSUFFICIENT DATA"

---

## 文件结构

```
marketing-os/
├── SKILL.md                          # 本文件
├── README.md                         # 系统文档
├── skills/
│   ├── virtual-cmo/                  # 战略分析
│   └── marketing-operator/           # 执行引擎
├── prompts/                          # 4 个结构化 LLM Prompt
├── schemas/                          # 5 个 JSON Schema
├── workflows/                        # 3 个工作流编排
├── memory/                           # 3 个持久化存储
├── logs/                             # 执行审计日志
├── configs/                          # 运行时配置
└── adapters/                         # 外部接口规范（CRM/Data/Content）
```

---

## 扩展方式

- **新增 Skill**：在 `skills/` 下创建目录，包含 `skill.json` + `logic.md` + `system_prompt.txt`
- **新增 Workflow**：在 `workflows/` 下创建 `.flow.json`
- **新增 Adapter**：在 `adapters/` 下创建 `.adapter.md`
- **接入 Stripe / CRM / 内容系统**：配置 `configs/system.config.json` 中的 adapters 部分

> [!TIP]
> 建议先以 `auto_mode: false` 手动运行各 workflow，验证输出质量后再开启自动模式。

---

*Skill Version: 1.0.0 | Designed for AI Agent Runtime Integration | 2026-03-22*
