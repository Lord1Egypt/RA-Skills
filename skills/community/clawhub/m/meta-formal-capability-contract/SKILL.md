---
name: meta-formal-capability-contract
version: 1.0.0
description: |
  由 model-distillation 从教师技能 formal-capability-contract 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-formal-capability-contract（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **formal-capability-contract** 蒸馏并增强生成。
> 生成时间：2026-07-23 09:29:06 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：formal-capability-contract —— 形式化能力契约与可证正确, 为什么需要, 契约与校验（scripts/contract.py，真实可跑）, 用法, 输出, 设计要点, 自进化学习系统, 自进化学习系统（越用越好用、越用越高效）
- 显性工作流步骤（4 步）：
  1. **PRE（前置条件）**：执行前必须成立（如 除数 != 0）。
  2. **POST（后置条件）**：执行后必须成立（如 `output * b == a`）。
  3. **INVARIANT（不变量）**：全程不得破坏（如 状态长度守恒）。
  4. 校验器对每条轨迹逐一评估三子句，返回 `{satisfied, failed_clause, verdict}`；

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(formal-capability-contract) | 学生(meta-formal-capability-contract) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（2297 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 4 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | contract.py, learner.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 未显式标注 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「formal-capability-contract」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- （教师未显式标注限制）
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
