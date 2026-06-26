---
name: meddic-b2b-sales-review
description: Structured B2B sales review using original PTC MEDDIC Six-Step methodology. Stage gates and win rates follow the authentic PTC six-step framework (Discovery→Scope→Go/No-Go→Validation→Business Case→Close). Enhanced D1-D9/S1-S7 gates are labeled as VP-level depth tools for deeper review, not substitutes for the original gates.
version: 1.4.0
author: Dick Dunkel
license: MIT-0
tags: [sales, meddic, review, coaching, debrief]
category: sales
---

# Sales Review Manager

这个 skill 帮助销售管理者和一线销售做六件事：

1. **复盘判断**：看清当前阶段、卡点与风险
2. **方向引导**：判断下一步最正确的推进方向
3. **决策辅助**：帮助决定是否继续投入、如何分配资源、何时管理介入
4. **赢率判断**：基于原始六步法阶段赢率 + gate 校验 + MEDDIC 校准，给出更真实的机会判断
5. **拜访复盘**：单次拜访后的结构化复盘，MEDDIC 状态更新 + 六步法评估 + 行动计划和客户记忆联动
6. **Routine 触发**：支持 Cron 定时（如每日 20:00）主动询问当日拜访情况

## 重要说明：原始六步法 Gate vs 增强 Gate

**原始六步法 Gate（每步 1 个，共 6 个）**是阶段通过的**最低门槛**。
**D1-D9 / S1-S7 增强 Gate**是 VP 级深度复盘工具，不是阶段判断的替代标准。

使用顺序：先用原始 Gate 判断阶段是否通过 → 再用增强 Gate 做赢率折扣

## 使用顺序

### 第一步：先识别场景
- 单个机会 / 单子 → `references/review-opportunity.md`
- 项目推进 / 项目卡点 → `references/review-project.md`
- pipeline / 周会 / forecast → `references/review-pipeline.md`
- 输单复盘 → `references/review-loss.md`
- 销售 1on1 / 能力辅导 → `references/review-1on1.md`
- 单次拜访复盘（MEDDIC更新+六步法评估+行动计划） → `references/review-visit.md`

#### 通用框架层
- 三层 Agent 范式 → `references/methods/three-layer-agent.md`

### 第二步：补读方法 reference
- 六步法阶段判断 → `references/methods/six-step.md`
- MEDDIC / MEDDPICC 缺口分析 → `references/methods/meddic.md`
- Go/No-Go / forecast 校准 → `references/methods/go-no-go.md`
- 场景召回触发器 → `references/methods/recall-triggers.md`
- 三层 Agent 范式 → `references/methods/three-layer-agent.md`

### 第三步：做赢率判断
- 阶段赢率主表 → `references/scoring/stage-win-rates.md`
- 阶段 gate 校验 → `references/scoring/stage-gate-validation.md`
- MEDDIC 校准 → `references/scoring/meddic-calibration.md`

### 第四步：补读 Enhanced Gates（增强关卡）
- 增强 Discovery Gates → `references/gates/enhanced-discovery-gates.md`
- 增强 Scope Gates → `references/gates/enhanced-scope-gates.md`
- 追问模式 → `references/distilled/inquiry-patterns.md`

### 第四步（续）：补读蒸馏经验与引导
- 拜访后复盘模式 → `references/distilled/visit-review-patterns.md`
- 动作推荐规则 → `references/distilled/action-recommendation-rules.md`
- 管理判断规则 → `references/distilled/manager-judgement-rules.md`
- 跟进优先级规则 → `references/distilled/follow-up-prioritization.md`
- 下一步最优动作 → `references/guidance/next-best-action.md`
- 策略方向判断 → `references/guidance/strategic-direction.md`
- 管理介入规则 → `references/guidance/manager-intervention.md`

### 第五步：补读决策与模板
- forecast 校准 → `references/decision/forecast-calibration.md`
- 资源分配 → `references/decision/resource-allocation.md`
- Go/No-Go 决策 → `references/decision/go-no-go-decision.md`
- 输出结构 / 行动项模板 → `references/templates/output-format.md`
- 信息采集 / 追问问题 → `references/templates/questions.md`
- 输入清单 → `references/templates/input-checklists.md`
- 跟进模板 → `references/templates/follow-up-template.md`
- 评分卡模板 → `references/templates/scorecards.md`

## 使用原则

- 主文件只做索引与分流，不承载详细知识
- 不一次性加载全部 reference，只读取当前任务必需的文件
- **原始六步法 Gate（每步 1 个）**是阶段通过的最低门槛，**必须先验证通过**才能套用该阶段赢率
- **D1-D9 / S1-S7 增强 Gate**是 VP 级深度复盘工具，用于赢率折扣，不是阶段判断标准
- 如果原始 Gate 没真正通过，**优先阶段回退**，而不是轻微打折
- 输出必须帮助管理者做判断、给方向、做决策、落动作
- 先判断阶段与原始 Gate 是否真实通过，再用 MEDDIC + 增强 Gate 做保持 / 折扣 / 回退

## 索引

### 场景层
- `references/review-opportunity.md`
- `references/review-project.md`
- `references/review-pipeline.md`
- `references/review-loss.md`
- `references/review-1on1.md`
- `references/review-visit.md`

### 方法层
- `references/methods/six-step.md`
- `references/methods/meddic.md`
- `references/methods/go-no-go.md`
- `references/methods/recall-triggers.md`

### 赢率判断层
- `references/scoring/stage-win-rates.md`
- `references/scoring/stage-gate-validation.md`
- `references/scoring/meddic-calibration.md`

### 蒸馏经验层
- `references/distilled/visit-review-patterns.md`
- `references/distilled/action-recommendation-rules.md`
- `references/distilled/manager-judgement-rules.md`
- `references/distilled/follow-up-prioritization.md`
- `references/distilled/inquiry-patterns.md`
- `references/distilled/champion-vs-coach.md`
- `references/distilled/field-judgment.md`
- `references/distilled/practical-vs-display.md`
- `references/distilled/package-strategy.md`
- `references/distilled/tactical-skills.md`

### Gates 增强层
- `references/gates/enhanced-discovery-gates.md`
- `references/gates/enhanced-scope-gates.md`

### 引导层
- `references/guidance/next-best-action.md`
- `references/guidance/strategic-direction.md`
- `references/guidance/manager-intervention.md`

### 决策层
- `references/decision/forecast-calibration.md`
- `references/decision/resource-allocation.md`
- `references/decision/go-no-go-decision.md`

### 模板层
- `references/templates/output-format.md`
- `references/templates/questions.md`
- `references/templates/input-checklists.md`
- `references/templates/follow-up-template.md`
- `references/templates/scorecards.md`
