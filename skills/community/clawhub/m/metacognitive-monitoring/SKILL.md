---
name: metacognitive-monitoring
version: 1.0.0
description: |
  元认知监控：在任务执行全过程实时监控自身的置信度、不确定性、能力边界与新奇度，
  输出 继续 / 降级 / 求助 / 暂缓 的元决策，并在"高置信同时高不确定"时触发过置信校准告警，
  防止幻觉式过度自信。纯标准库、可本地实跑，是"超级智能体"可靠性的守门层。
agent_created: true
visibility: public
---

# metacognitive-monitoring（元认知监控）

> 北极星：超越一线大模型需要 agent 知道"自己不知道什么"。
> 本技能把「实时监控自身认知状态并据此自我调节」做成可运行、可验证的工程模块，
> 是 `super-agent-loop` / `reason-verify` 之上的"自我认知守门层"。

## 何时使用
- 执行长程 / 高风险任务前与中，判断当前是否该继续、降级、求助或暂缓。
- 检测到输出"看起来很自信但依据很薄弱"时，触发校准告警，避免幻觉式过度自信。
- 作为超级智能体闭环的"元决策开关"，串联规划→执行→自验证→反思。

## 核心机制
读取一份「认知状态」：
- `confidence` 置信度 ∈[0,1]
- `uncertainty` 认知不确定性（不知自己不知）∈[0,1]
- `novelty` 任务新奇度 ∈[0,1]
- `scope_match` 任务与已知能力的匹配度 ∈[0,1]
- `necessity` 任务必要性 / 价值 ∈[0,1]

输出元决策（按优先级）：
1. **过置信告警 OVERCONFIDENT** — `confidence>0.8 且 uncertainty>0.6`：依据与自信矛盾，强制 SEEK_HELP 并标记 calibration_failure。
2. **求助 SEEK_HELP** — `uncertainty≥0.7 或 scope_match<0.3`：超出可靠边界，需澄清/升级/检索。
3. **降级 DEGRADE** — `uncertainty≥0.45 或 scope_match<0.6`：可用，但必须加验证、走保守方案。
4. **暂缓 DEFER** — `necessity<0.2`：价值过低，暂缓或跳过（除非被显式要求）。
5. **继续 PROCEED** — 其余：正常推进。

并提供 `calibration_error()`：对比历史 (confidence, actual_correct) 计算期望校准误差（ECE 简化版），量化"自信度"是否可信。

## 使用
```bash
python scripts/monitor.py --selftest          # 自测全部策略分支
python scripts/monitor.py --json '{"confidence":0.9,"uncertainty":0.2,"novelty":0.3,"scope_match":0.8,"necessity":0.7}'
python scripts/monitor.py --calibrate '[[0.9,true],[0.6,false],[0.8,true],[0.3,false]]'
```

## 自进化学习系统
本技能接入 skill-self-improve 的 learner.py：每次元决策后 `record` 决策类别与是否触发校准告警，
积累后可识别"何种任务易过置信"，反哺 `super-agent-loop` 的降级阈值。

## 已知限制
- 阈值（0.45/0.7/0.3/0.2）为经验默认，首次用于新领域建议用校准数据回灌再调。
- 不替代领域自验证（`reason-verify` / `formal-verify`），仅做"是否该继续"的元层开关。

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次元决策后自动复盘、积累经验，逐步提升可靠性。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各元决策类别频次、过置信校准告警次数、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次元决策（--capability 填本次决策类别，如「PROCEED」「SEEK_HELP」「OVERCONFIDENT」）
python scripts/learner.py record <本技能目录> --capability SEEK_HELP
# 记录一次过置信校准告警
python scripts/learner.py record <本技能目录> --capability OVERCONFIDENT --fail --error 过置信 --note "高自信低依据"
# 记录用户偏好（下次直接采用）
python scripts/learner.py prefer <本技能目录> --key 降级策略 --val 保守验证
# 查看累计洞察（高频决策类别 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **过置信告警累计 ≥3 次** → 主动下调对应领域的 SEEK_HELP 阈值，并回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频决策类别优先打磨示例，低频类别评估精简。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用。

> 越用越懂你：第一次用是通用监控，第十次已沉淀为你专属的"自我认知守门层"。
