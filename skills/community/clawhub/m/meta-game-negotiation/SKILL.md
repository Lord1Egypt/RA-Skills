---
name: meta-game-negotiation
version: 1.0.0
description: |
  由 model-distillation 从教师技能 game-negotiation 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-game-negotiation（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **game-negotiation** 蒸馏并增强生成。
> 生成时间：2026-07-23 00:37:28 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：game-negotiation（博弈谈判）, 何时使用, 工作流, 运行, Nash 等权分 100：--mode nash --json '{"disagree":[0,0],"surplus":100,"weights":[1,1]}', Rubinstein δ=0.9：--mode rubinstein --json '{"p":0.9,"r":0.9}', 增强点（融入元进化闭环）, 已知限制
- 显性工作流步骤（6 步）：
  1. **识别博弈型**：合作分配→Nash/Shapley；序贯谈判→Rubinstein；对抗→minimax。
  2. **Nash 议价**：威胁点(disagree) + 可分配剩余(surplus) + 议价力权重(weights) → 闭式分配。
  3. **Rubinstein**：双方贴现因子(p,r) → 子博弈完美均衡份额。
  4. **Shapley**：特征函数(char_func) → 每玩家平均边际贡献。
  5. **minimax**：收益矩阵 → 离散网格近似最大最小均衡值。
  6. **可靠自验证**：`--selftest` 断言全部符合闭式/理论值，reliability<0.8 即回退。

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(game-negotiation) | 学生(meta-game-negotiation) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（1231 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 6 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | learner.py, negotiator.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 已识别 1 处 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「game-negotiation」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- - minimax 为离散网格近似，矩阵>2 维退化为等权（仅 2xN 精确）。
- Shapley 复杂度 2^n，玩家>~12 需采样近似。
- 假设理性/共同知识，非理性对手需加行为博弈层。
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
