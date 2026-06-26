---
name: improvement-discriminator
description: "当需要对改进候选多人盲审打分、用 LLM 做语义评估、判断候选是否应被接受、或打分结果全是 hold 想知道为什么时使用。支持 --panel 多审阅者盲审和 --llm-judge 语义评估。不用于结构评估（用 improvement-learner）或门禁决策（用 improvement-gate）。"
license: MIT
triggers:
  - score candidate
  - evaluate improvement
  - multi-reviewer panel
  - LLM judge
  - 候选打分
  - 盲审
version: 0.1.0
author: OpenClaw Team
---

# Improvement Discriminator

Multi-signal scoring engine: heuristic rules + evaluator rubrics + LLM-as-Judge + multi-reviewer blind panel.

## When to Use

- 对改进候选打分和排序——产出 ranked list 供 executor 按优先级执行
- 运行多审阅者盲审（CONSENSUS/VERIFIED/DISPUTED 认知标签），降低单人偏见
- 用 LLM-as-Judge 评估 4 个语义维度（clarity, specificity, consistency, safety）
- 组合 --panel + --llm-judge 获得最全面的评估（两者不互斥）
- 调试为什么所有候选都被标为 hold——通常是 risk_penalty 过高或缺少 source_refs
- 在 orchestrator pipeline 第 2 阶段自动调用
- 需要可解释的评分明细时（每个维度独立打分，附 judge_notes）
- 需要对比多轮改进的候选质量趋势时

## When NOT to Use

- **评估 skill 目录结构** → use `improvement-learner`（learner 做 6 维结构分析，discriminator 做语义评分）
- **keep/revert/reject 决策** → use `improvement-gate`（discriminator 只打分不做决策）
- **执行文件变更** → use `improvement-executor`（discriminator 不修改任何文件）
- **生成改进候选** → use `improvement-generator`
- 候选数量为 0 时调用会报错，应先确认 generator 产出了候选
- 不要用 discriminator 做回归检测——回归检测是 gate 的 RegressionGate 层负责
- 不要把 discriminator 的 accept 当做最终决策——它只是评分建议，最终 keep/reject 由 gate 决定
- 不要在没有 candidates.json 的情况下调用——输入必须是 generator 产出的标准格式

## Scoring Modes

4 种模式可以独立或组合使用，从纯启发式到全信号融合逐步增加评估深度。
默认模式（Heuristic only）零成本、确定性，适合快速过滤。
加入 evaluator evidence 后，利用 task_suite 执行结果作为评分依据，更贴近实际效果。
加入 LLM Judge 后引入语义理解，但会消耗 token 且结果有随机性。
Panel 模式引入多视角盲审，捕捉单一审阅者无法发现的偏差。

| Mode | Flag | Scoring |
|------|------|---------|
| Heuristic only | (default) | category bonus + source refs + risk penalty |
| + Evaluator | `--use-evaluator-evidence` | Heuristic 70% + evaluator 30% |
| + LLM Judge | `--llm-judge {claude,openai,mock}` | Heuristic 60% + LLM 40% |
| + Panel | `--panel` | 2+ reviewers independently, cognitive label decides |
| All combined | `--panel --llm-judge mock --use-evaluator-evidence` | Full |

## Why Panel Review Matters

**Tradeoff: single reviewer speed vs. multi-reviewer accuracy.**

之所以引入 panel 盲审而非依赖单一评分器，原因是：

1. **Single reviewer bias is real** — 一个 "structural" 审阅者倾向于高分（偏好结构完整的候选），而 "conservative" 审阅者倾向于低分（偏好最小变更）。单一审阅者会系统性地偏向某类候选。
2. **CONSENSUS/VERIFIED/DISPUTED 三态标签**捕捉了审阅者之间的分歧程度。DISPUTED 意味着候选质量有争议，gate 层会据此做更谨慎的决策。
3. **LLM-as-Judge 弥补启发式盲区** — 启发式规则无法判断"这段改写是否真的更清晰"，LLM judge 的 clarity/specificity 维度填补了这个空白。

**问题**: 为什么不直接用 LLM judge 替代所有启发式规则？Because LLM judge 有 token 成本（每个候选约 500-1000 tokens）且存在随机性。启发式规则是确定性的、零成本的，适合作为第一层过滤。组合使用时，启发式占 60% 权重、LLM 占 40%，既保证了稳定性又引入了语义理解。

当 panel 结果全是 hold 时，通常是以下原因之一：
- 候选缺少 `source_refs`（引用来源），导致 source_ref_bonus = 0
- `risk_level` 被标为 high，导致 risk_penalty 过大
- LLM judge 的 safety 维度给了低分（候选可能引入了不安全的模式）

<example>
正确用法: 多审阅者盲审 + LLM 语义打分
$ python3 scripts/score.py --input candidates.json --panel --llm-judge mock --output scored.json
→ 输出包含:
  panel_reviews: [{reviewer: "structural", score: 7.5}, {reviewer: "conservative", score: 5.0}]
  cognitive_label: "VERIFIED"  (2人同意)
  llm_verdict: {score: 0.78, decision: "conditional", dimensions: {clarity: 0.85, ...}}
</example>

<anti-example>
常见误解: --panel 和 --llm-judge 互斥
→ 错！两者可以同时使用。每个审阅者独立调用 LLM judge，得到独立的语义分数。
→ 如果只用 --panel 不加 --llm-judge，panel 只做启发式评分，不做语义评估。
</anti-example>

## CLI

score.py 是核心入口，接收 candidates.json，输出 scored.json。
所有模式共用同一个入口，通过 flag 组合控制评分深度。
`--llm-judge` 支持 3 种 provider: claude（最准）、openai、mock（测试用，零成本）。
`--panel` 会自动创建 structural 和 conservative 两个独立审阅者。
输出的 scored.json 可直接传给 executor 或 gate 消费。
使用 `--verbose` 可查看每个审阅者的详细评分过程和 judge_notes。

```bash
# Basic scoring (heuristic only, fastest)
python3 scripts/score.py --input candidates.json --output scored.json

# Full pipeline: panel + LLM judge
python3 scripts/score.py \
  --input candidates.json --panel --llm-judge mock --output scored.json
```

Panel-only mode (no LLM, lower cost):

```bash
# Panel blind review without LLM judge — heuristic scoring only
python3 scripts/score.py \
  --input candidates.json \
  --panel \
  --output scored.json
```

LLM-judge-only mode (no panel, single reviewer):

```bash
# Single reviewer + LLM semantic evaluation
python3 scripts/score.py \
  --input candidates.json \
  --llm-judge claude \
  --use-evaluator-evidence \
  --output scored.json
```

## Output Artifacts

| Request | Deliverable |
|---------|------------|
| Score | JSON: per-candidate scores, blockers, recommendations, judge_notes |
| Panel | JSON: panel_reviews[], cognitive_label (CONSENSUS/VERIFIED/DISPUTED), aggregated_score |
| LLM judge | JSON: llm_verdict with score, decision (accept/conditional/reject), 4 dimensions, confidence |
| Combined | All above fields merged into a single scored candidate object |

输出中的 `cognitive_label` 含义：
- **CONSENSUS** — 所有审阅者评分方向一致（全部 accept 或全部 reject），高置信度
- **VERIFIED** — 多数审阅者同意，少数有保留意见，中等置信度
- **DISPUTED** — 审阅者之间存在根本分歧（一人 accept 一人 reject），需要 gate 层额外审慎处理

`decision` 字段的三态语义：accept 直接通过，conditional 需要满足附加条件（记录在 judge_notes），reject 直接拒绝。

## Related Skills

- **improvement-generator**: Produces the candidates that this skill scores — discriminator 的输入来自 generator
- **improvement-gate**: Consumes scored candidates for keep/revert/reject — gate 依赖 cognitive_label 做 ReviewGate 判定
- **improvement-learner**: Structural evaluation (6-dim); discriminator focuses on semantic — 两者互补，learner 看结构，discriminator 看内容
- **benchmark-store**: Frozen benchmarks for regression checking — 提供历史基线数据
- **improvement-executor**: Applies top-ranked candidates — executor 按 discriminator 的排序依次执行
- **improvement-evaluator**: Task-based evaluation — evaluator 的 pass_rate 可作为 `--use-evaluator-evidence` 的数据源
- **improvement-orchestrator**: Calls discriminator as stage 2 — 全流程中 discriminator 在 generator 之后、evaluator 之前

Pipeline 中的数据流: generator → **discriminator** → evaluator → executor → gate
