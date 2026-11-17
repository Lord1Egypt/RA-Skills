---
name: meta-metacognitive-monitoring
version: 1.0.0
description: |
  由 model-distillation 从教师技能 metacognitive-monitoring 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-metacognitive-monitoring（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **metacognitive-monitoring** 蒸馏并增强生成。
> 生成时间：2026-07-23 04:07:02 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：metacognitive-monitoring（元认知监控）, 何时使用, 核心机制, 使用, 自进化学习系统, 已知限制, 自进化学习系统（越用越好用、越用越高效）, 记忆文件
- 显性工作流步骤（5 步）：
  1. **过置信告警 OVERCONFIDENT** — `confidence>0.8 且 uncertainty>0.6`：依据与自信矛盾，强制 SEEK_HELP 并标记 calibration_failure。
  2. **求助 SEEK_HELP** — `uncertainty≥0.7 或 scope_match<0.3`：超出可靠边界，需澄清/升级/检索。
  3. **降级 DEGRADE** — `uncertainty≥0.45 或 scope_match<0.6`：可用，但必须加验证、走保守方案。
  4. **暂缓 DEFER** — `necessity<0.2`：价值过低，暂缓或跳过（除非被显式要求）。
  5. **继续 PROCEED** — 其余：正常推进。

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(metacognitive-monitoring) | 学生(meta-metacognitive-monitoring) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（2559 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 5 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | learner.py, monitor.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 已识别 1 处 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「metacognitive-monitoring」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- - 阈值（0.45/0.7/0.3/0.2）为经验默认，首次用于新领域建议用校准数据回灌再调。
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
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
