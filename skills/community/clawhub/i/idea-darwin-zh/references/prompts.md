# Prompt 模板

每个动作的 Prompt 模板。执行动作时，将变量替换为实际值后作为思考指引。

---

## 通用模板结构

所有动作 Prompt 遵循以下结构：

```
你是"Idea 迭代孵化系统"中的 {action_name} 模块。

你的任务是对下面这个 idea 执行 {action_name} 操作。

【当前 idea 卡片】
{idea_card}

【当前轮次上下文】
- round: {round_id}
- 当前阶段: {stage}
- 可用预算: {budget_level}
- 相关 idea: {related_ideas_summary}

【操作目标】
{goal_description}

【操作要求】
1. 保持逻辑严谨，不要空泛扩写。
2. 尽可能保留原 idea 的核心意图。
3. 若发现明显漏洞，要指出。
4. 若生成新 idea，必须和原 idea 有清晰关系。
5. 输出必须结构化。
```

---

## 深化 Prompt

```
请对这个 idea 做"深化"处理。这不是表面改写，而是补齐它的逻辑结构。

从以下角度展开：
1. 它到底解决什么问题？
2. 目标用户是谁？
3. 为什么这个方案成立？
4. 最小可行版本是什么？
5. 最大风险是什么？
6. 还缺少哪些关键假设验证？

输出：
- 充实后的 idea 描述
- 核心假设
- 用户场景
- MVP 版本
- 风险与待验证问题
- 建议下一步动作
```

---

## 派生 Prompt

```
基于下面这个 idea 派生出 2~3 个高质量变体。

沿以下维度拉开差异：
- 用户群差异
- 场景差异
- 商业模式差异
- 产品形态差异
- 技术路径差异

要求：
1. 每个派生 idea 必须保留原 idea 的核心基因
2. 但必须有明确差异
3. 不要生成只是换表述的重复方案

输出格式（每个派生）：
- 变体标题
- 核心变化点
- 为什么值得保留
- 与原 idea 的关系
```

---

## 交叉 Prompt

```
请将下面两个 idea 做交叉融合，寻找新的组合方向。

【Idea A】
{idea_a_card}

【Idea B】
{idea_b_card}

先分析：
1. 它们的共同点是什么？
2. 它们的互补点是什么？
3. 它们之间是否存在冲突？

再输出：
1. 1~3 个交叉后新 idea
2. 每个新 idea 的核心机制
3. 为什么这种交叉有意义
4. 最大风险
5. 是否值得进入下一轮
```

---

## 批判 Prompt

```
请对下面这个 idea 进行批判性审查。

重点检查：
1. 是否逻辑自洽
2. 是否只是概念包装
3. 是否缺乏真实需求
4. 是否成本过高
5. 是否有更简单替代方案
6. 该 idea 最可能失败在哪一步

输出：
- 核心漏洞
- 风险等级（高/中/低）
- 是否建议继续
- 如果继续，最应该修补什么
```

---

## 评分 Prompt

```
请从以下 6 个维度对这个 idea 打分（1-10）并给出理由：

- 创新性（Novelty，权重 0.1）：是否有真正的突破，还是简单重复？
- 可行性（Feasibility，权重 0.2）：技术、资源、路径上是否可行？
- 潜在价值（Value，权重 0.2）：做成后价值有多大？
- 逻辑完整性（Logic，权重 0.2）：是否自洽，有无明显漏洞？
- 交叉潜力（CrossPotential，权重 0.1）：与其他 idea 碰撞出新东西的可能性？
- 可验证性（Verifiability，权重 0.2）：能否设计实验或最小验证路径？

然后计算：
Survival = 0.10×Novelty + 0.20×Feasibility + 0.20×Value + 0.20×Logic + 0.10×CrossPotential + 0.20×Verifiability

输出 JSON 格式：
{
  "novelty": 0,
  "feasibility": 0,
  "value": 0,
  "logic": 0,
  "cross_potential": 0,
  "verifiability": 0,
  "survival_score": 0.0,
  "reasoning": {
    "novelty": "...",
    "feasibility": "...",
    "value": "...",
    "logic": "...",
    "cross_potential": "...",
    "verifiability": "..."
  },
  "suggested_action": "deepen / derive / cross / critique / dormant"
}
```

---

## 验证 Prompt

```
请对这个 idea 执行双层验证检查。

【第一层：硬伤检查】
回答以下 4 个问题（Yes/No + 理由）：
1. 是否存在逻辑硬伤？（核心假设是否自相矛盾或明显不成立）
2. 是否缺乏真实需求？（能否找到明确目标用户或使用场景）
3. 是否完全不可落地？（技术/资源/路径上是否有无法克服的障碍）
4. 是否与已有 idea 高度重复？（是否只是换了说法的旧 idea）

如果任一项为 Yes，标记 validated: false 并给出简要理由。

【第二层：价值判断】（仅在第一层全部 No 时执行）
1. 是否值得继续投入资源？
2. 下一步最应该做什么动作？
3. 当前最大的风险是什么？

输出 JSON 格式：
{
  "hard_check": {
    "logic_flaw": {"result": "Yes/No", "reason": "..."},
    "no_real_demand": {"result": "Yes/No", "reason": "..."},
    "not_feasible": {"result": "Yes/No", "reason": "..."},
    "duplicate": {"result": "Yes/No", "reason": "..."}
  },
  "validated": true/false,
  "value_judgment": {
    "worth_continuing": "Yes/No",
    "next_action": "...",
    "biggest_risk": "..."
  }
}
```

---

## 轮次报告模板

```markdown
# 第 {round_id} 轮报告

## 概要
- 执行时间：{timestamp}
- 池中 idea 总数：{total}（活跃 {active} / 休眠 {dormant}）
- 本轮处理 idea 数：{processed}
- 新产生 idea 数：{new_count}

## 执行动作

| Idea ID | 标题 | 动作 | 结果摘要 |
|---|---|---|---|
| IDEA-XXXX | ... | 深化 | ... |

## 新产生的 idea

| Idea ID | 标题 | 来源 | 初始 Priority |
|---|---|---|---|
| IDEA-XXXX | ... | 派生自 IDEA-XXXX | 6.5 |

## Top 5 分数变化

| Idea ID | 标题 | Priority 变化 | 原因 |
|---|---|---|---|
| IDEA-XXXX | ... | +1.2 | 深化后逻辑更完整 |

## 验证未通过（需用户决策）

| Idea ID | 标题 | 未通过原因 | 建议处理 |
|---|---|---|---|
| IDEA-XXXX | ... | 与 IDEA-XXXX 高度重复 | 合并或休眠 |

## 下轮建议
- 优先处理：IDEA-XXXX, IDEA-XXXX
- 建议交叉：IDEA-XXXX × IDEA-XXXX
- 关注：IDEA-XXXX 连续 3 轮无变化
```
