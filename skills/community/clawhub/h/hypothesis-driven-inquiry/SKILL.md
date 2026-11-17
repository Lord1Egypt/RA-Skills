---
name: hypothesis-driven-inquiry
version: 1.0.0
description: |
  假设驱动探究（溯因推理 Abduction）：由观测反推成因、按解释覆盖与简约度排序候选假设，
  并为每个假设设计判别性实验，逼近真因。零依赖、可本地实跑、输出可追溯。
agent_created: true
visibility: public
---

# hypothesis-driven-inquiry（假设驱动探究 · 溯因推理）

> 由 meta-evolver 在第 39 轮构建，闭环 `build:通用智能体(AGI梯队):假设驱动探究`。
> 这是北极星「超越一线大模型」最后一段高价值空白：从观测反推成因、并设计判别性实验。

## 机制

1. **观测归集（observe）**：把零散事实整理成观测集合 O。
2. **假设生成/归集（hypothesize）**：每个候选假设 h 声明它能解释哪些观测（coverage）与复杂度成本（complexity）。
3. **评分排序（rank）**：`score = coverage_ratio × parsimony`，其中
   - `coverage_ratio = |h.explains ∩ O| / |O|`（解释了多少观测）
   - `parsimony = 1 / (1 + complexity)`（越简洁越高）
4. **判别性实验设计（discriminate）**：对每条假设找一个「它解释、但最强竞对不解释」的观测作为判别性检验；找不到则说明假设不可证伪 → 标记为弱。
5. **逼近真因（conclude）**：输出排序后的假设 + 各自判别实验，供下一步实据验证。

## 何时使用

- 给定一堆异常/现象，需要反推「最可能成因」并规划如何验证时。
- 故障根因分析、科学假设生成、诊断推理、A/B 实验设计前置。
- 用户要求「不只列可能原因，还要告诉我先验证哪条、怎么验证」。

## 运行

```bash
# 自带夹具自测（零依赖，断言评分/排序/判别全通过）
python scripts/hypothesis.py --selftest

# 对真实观测+假设做探究（JSON 入参）
python scripts/hypothesis.py --obs o1,o2,o3 \
  --hypo "hA|explains=o1,o2|complexity=1" \
  --hypo "hB|explains=o2,o3|complexity=3"
```

## 与"强模型"的差异

普通模型常止于「可能的 N 个原因」罗列；本技能进一步给出**可证伪的判别实验**，把探询推进到可行动、可收敛的真因逼近——这正是超级 agent 相较强文本模型的分水岭。

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）
```bash
python scripts/learner.py record <本技能目录> --capability 溯因探究
python scripts/learner.py insight <本技能目录>
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
