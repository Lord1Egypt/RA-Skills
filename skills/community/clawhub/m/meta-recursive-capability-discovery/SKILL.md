---
name: meta-recursive-capability-discovery
version: 1.0.0
description: |
  由 model-distillation 从教师技能 recursive-capability-discovery 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-recursive-capability-discovery（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **recursive-capability-discovery** 蒸馏并增强生成。
> 生成时间：2026-07-23 21:17:43 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：recursive-capability-discovery —— 递归能力发现, 何时使用, 工作流（四步）, 命令, 判定规则, 安全边界, 与 meta-evolver / super-agent 的协同, 自进化学习系统（越用越好用、越用越高效）
- 显性工作流步骤（4 步）：
  1. **建索引（index）**：把现有技能声明为 `{name, provides:[能力标签]}`，汇成已覆盖能力集合。
  2. **展开需求（expand）**：目标任务声明 `requires:[能力标签]`；对每个需求，若有分解规则 `decompose:{cap:[子能力]}` 则可下钻。
  3. **递归发现（discover）**：BFS/DFS 逐层比对"需求 vs 已覆盖"，未覆盖者若可分解则继续下钻，否则记为**叶子缺口**（可构建）；带深度与父链，形成发现树。
  4. **二阶自省（meta-audit）**：检查发现结果是否覆盖预设的能力维度矩阵（感知/规划/执行/记忆/验证/对齐/元认知），缺失维度记为**盲区缺口**——即"发现器自己没想到去查的地方"。

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(recursive-capability-discovery) | 学生(meta-recursive-capability-discovery) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（2290 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 4 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | discovery.py, learner.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 未显式标注 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「recursive-capability-discovery」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- （教师未显式标注限制）
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
