# Agent Registry — Lazy Loading Protocol

## Loading Protocol

每个Agent执行前，按以下顺序加载资源：

1. 读取 `agents/<name>.md` — Agent执行流程
2. 按需读取 `references/` — 仅加载当前Agent引用的参考文件
3. 不预加载未调用Agent的文件

## Agent Registry

| Agent | File | References | Est. Lines | Est. Tokens |
|-------|------|-----------|:----------:|:-----------:|
| Intake | agents/intake-agent.md | — | 108 | ~1,800 |
| Information | agents/information-agent.md | — | 239 | ~4,000 |
| Strategy | agents/strategy-agent.md | references/strategy-frameworks.md | 201 + 313 | ~5,100 |
| Decision | agents/decision-agent.md | references/decision-engine.md | 228 + 181 | ~4,100 |
| Expression | agents/expression-agent.md | references/pitch-structure.md | 269 + 336 | ~6,000 |
| Delivery | agents/delivery-agent.md | — | 102 | ~1,700 |

**按需加载（条件触发）：**
- references/bilingual-templates.md — 仅当用户使用英文提问时加载（~3,500 tokens）

## Mode → Agent → Reference Mapping

| Mode | Agents | References to Load | Total Est. Tokens | Est. API Cost |
|------|--------|-------------------|:-----------------:|:-------------:|
| Full | 全部6个 | strategy-frameworks + decision-engine + pitch-structure [+ bilingual] | ~22,700 [+3,500] | ~$0.35-0.70 |
| Preview | Intake → Information → Strategy | strategy-frameworks | ~10,900 | ~$0.15-0.30 |
| Custom | 按用户指定 + 最小依赖图 | 按需 | 变化 | 变化 |
| Resume | 从指定Agent开始 | 仅该Agent及下游的references | 变化 | 变化 |

**成本估算说明：** 基于 Claude Sonnet 级别模型，输入 $3/M tokens + 输出 $15/M tokens。Full模式假设总消耗约60K input + 15K output tokens。实际成本取决于Brief复杂度和用户交互轮数。

## Inter-Agent Handoff Protocol

Agent间传递的不是原始输出，而是**结构化摘要**：

```
Intake → Information:
  Battle Card (完整)

Information → Strategy:
  Battle Card (摘要: 项目类型 + 隐性信号 + 作战方针)
  + 需求解构结论 (真痛点/伪需求/隐性需求)
  + 决策者画像 (每角色1-2行)
  + Strategy Gap (完整)

Strategy → Decision:
  Battle Card 摘要
  + 需求解构结论
  + 策略路径 (Challenge → Idea → Framework → Impact)
  + 逻辑链自检结果
  + 风险对冲方案概要

Decision → Expression:
  策略路径摘要
  + 决策模式 + 权力图谱
  + 胜率评估 + Top 3风险
  + 模拟结论 + 优化建议

Expression → Delivery:
  策略路径摘要 + 决策模式
  + 8段式Pitch结构
  + 情绪引擎评估结果
  + AIGC Demo提示词包
  + Q&A Red Team
```

**摘要规则：**
- Battle Card: 下游Agent只接收项目类型 + 隐性信号 + 作战方针（~5行），不重复完整卡
- 需求解构: 下游Agent只接收结论（真/伪/隐性列表），不重复推导过程
- 决策者画像: 每角色压缩为1-2行（角色 + 权力等级 + 风险偏好 + KPI痛点）
- 策略路径: 保持完整，是核心交付物
- 权力图谱: 保持完整，Decision的核心输出

## Fallback Table

| Agent | 失败场景 | 降级动作 | 输出标记 |
|-------|---------|---------|---------|
| Intake | Brief信息严重不足 | 用行业默认假设填充，标注【假设】 | ⚠️ 信息不足 |
| Information | 无法联网搜索/信息极度缺乏 | 标注推断等级E，输出假设性方向 | ⚠️ 完全推断 |
| Strategy | 逻辑链自检发现重大跳跃(C级) | 标注跳跃点，提供补强建议，不强行推导 | ⚠️ 逻辑跳跃 |
| Decision | 证据链严重不足(整体证据质量"低") | 胜率标注为参考值，明确告知用户 | ⚠️ 证据不足 |
| Expression | 用户未提供足够品牌素材 | AIGC Demo用通用品牌风格替代 | ⚠️ 通用风格 |
| Delivery | 上游Agent输出不完整 | 标注缺失项，交付可用部分 | ⚠️ 部分交付 |

**用户触发重执行：**
在任何Checkpoint处，用户可以说"重做这个Agent"或"跳过这个Agent"。
- 重做：重新读取Agent文件，基于用户反馈调整输入后重新执行
- 跳过：标注【用户跳过】，用合理默认值填充下游依赖，继续流水线
