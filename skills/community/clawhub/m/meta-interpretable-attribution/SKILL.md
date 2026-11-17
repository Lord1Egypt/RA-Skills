---
name: meta-interpretable-attribution
version: 1.0.0
description: |
  由 model-distillation 从教师技能 interpretable-attribution 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-interpretable-attribution（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **interpretable-attribution** 蒸馏并增强生成。
> 生成时间：2026-07-23 04:08:47 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：interpretable-attribution（可解释归因）, 何时使用, 工作流, 运行, 内置自检（无外部依赖）, 实际归因, 增强点（融入元进化闭环）, 已知限制
- 显性工作流步骤（6 步）：
  1. **数据/模型接入**：数据集(json list of dicts，含 label 字段) + 预测函数 `predict(r)->val`(py 文件定义)。
  2. **全局重要性**：permutation importance —— 打乱某特征，看整体评分下降幅度，排序得全局归因。
  3. **局部重要性**：local ablation —— 把待测样本某特征置为基值，看该样本预测变化。
  4. **反事实**：counterfactual —— 贪心选"置为极值/离散候选后预测最接近目标"的特征翻转，得最少改动集。
  5. **自然语言归因**：top-k 特征 -> 可读决策理由；边界附近样本给出"预测稳健"说明。
  6. **可靠自验证**：脚本内置 `--selftest` 实测断言（首要特征=真因、反事实可翻转），reliability<0.8 即回退重做。

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(interpretable-attribution) | 学生(meta-interpretable-attribution) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（1225 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 6 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | attributor.py, learner.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 已识别 1 处 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「interpretable-attribution」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- - 排列重要性依赖样本量，小样本方差大（建议 n_perm>=20）。
- 反事实为贪心近似，未必是全局最小改动集（NP 难）。
- 仅支持单样本、扁平特征；嵌套结构需先扁平化。
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
