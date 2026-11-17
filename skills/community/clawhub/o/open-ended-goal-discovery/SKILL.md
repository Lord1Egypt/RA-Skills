---
name: open-ended-goal-discovery
version: 1.0.0
description: |
  开放式目标发现：让 agent 不再被动接任务，而是主动从能力图谱、用户兴趣信号与反馈中
  自主发现值得攻克的新目标。对候选目标做 价值×新颖度×可行性×用户对齐 四维打分并排序，
  输出 Top-N 建议。纯标准库、可本地实跑，是"超级智能体"主动设目标能力的延伸与强化。
agent_created: true
visibility: public
---

# open-ended-goal-discovery（开放式目标发现）

> 北极星：超越一线大模型需要 agent 能"自己找到该做的事"，而非只等指令。
> 本技能把「主动目标发现」做成可运行、可验证的工程模块，是 proactive-goal-setter 的
> 升维版——从"给定候选自动排课"升级为"从信号自主生成候选并打分"。

## 何时使用
- 长程空闲 / 任务间隙，需要主动发现高价值待办（而非空转）。
- 给用户提供"我还能帮你做这些"的主动建议清单。
- 作为超级智能体闭环的"目标生成器"节点，喂给 long-horizon-planner 排程。

## 核心机制
输入一份「环境状态」JSON：
- `capabilities`: 已知能力名列表
- `pursued_goals`: 已攻克/进行中目标列表（用于新颖度惩罚）
- `signals`: 兴趣信号列表 `[{"topic":..,"interest":0..1,"positive":int}]`
- `preferences`: 用户偏好（可选，如 `{"domain":"finance"}`）

对每条信号生成候选目标，四维打分（权重可调）：
- **value 价值** = 信号兴趣度聚合（interest 均值 × log(1+正向反馈)）
- **novelty 新颖度** = 1 − 与已追目标的最大字符级相似度（避免重复立项）
- **feasibility 可行性** = 目标所需能力中"已具备占比"（缺失能力越多分越低）
- **alignment 对齐** = 命中用户偏好域的程度

`score = 0.35*value + 0.30*novelty + 0.25*feasibility + 0.10*alignment`，排序取 Top-N。

## 使用
```bash
python scripts/discover.py --selftest
python scripts/discover.py --json '{...}' --top 3
```

## 自进化学习系统
接入 skill-self-improve 的 learner.py：每次发现的"被用户采纳/否决"目标记 record，
积累后识别高价值信号域，反哺 value 权重与 alignment 偏好。

## 已知限制
- novelty 用字符级 Jaccard，短目标区分度有限；长目标更准确。
- feasibility 依赖 capabilities 清单完整性，清单缺失会高估可行性。
- 不替代领域价值研判，仅做"值得主动提"的初筛排序。

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每轮目标发现后自动复盘、积累经验。

### 记忆文件
`learned_patterns.json` 记录：操作总数、各信号域使用频次、被用户采纳/否决的目标、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次发现（--capability 填本次主域，如「finance」「行业链分析」）
python scripts/learner.py record <本技能目录> --capability finance
# 记录一个被用户否决的目标（用于下调该域权重）
python scripts/learner.py record <本技能目录> --capability 冷门彩蛋 --fail --error 用户否决 --note "价值不足"
# 记录用户偏好（下次直接采用）
python scripts/learner.py prefer <本技能目录> --key 偏好域 --val finance
# 查看累计洞察（高频信号域 / 反复否决）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **被否决累计 ≥3 次** → 下调对应信号域 value 权重，并回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频信号域优先打磨，低频域评估降权。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用。

> 越用越懂你：第一次发现是通用初筛，第十次已沉淀为你专属的"主动目标雷达"。
