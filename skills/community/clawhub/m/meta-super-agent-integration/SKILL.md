---
name: meta-super-agent-integration
version: 1.0.0
description: |
  由 model-distillation 从教师技能 super-agent-integration 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-super-agent-integration（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **super-agent-integration** 蒸馏并增强生成。
> 生成时间：2026-07-23 09:23:40 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：super-agent-integration —— 端到端自主闭环真实跑通, 为什么需要, 闭环编排（全链路，真实调用各引擎）, 用法, 自检（真实跑通一次端到端闭环并断言健康度）, 真实跑一次, 输出, 设计要点
- 显性工作流步骤（7 步）：
  1. **规划（planner）**：目标写进跨引擎记忆总线 `MemoryBus.write("planner","goal",...)`
  2. **执行内核（super-agent-bootstrap）**：`SuperAgent().run(goal, items)` 跑通 感知→执行→自验证→反思重规划
  3. **自验证（reason-verify）**：对汇总论断调用 `reason()` 做可靠性评分（reliability）
  4. **反思重规划（reflection-replanner）**：若自验证不达标，用 `Replanner.replan()` 增补针对性补救步骤
  5. **跨引擎记忆贯通（memory-cross-engine）**：每个结果 `MemoryBus.write("memory",...)` 并与目标 `link`
  6. **回归评测（agent-eval-harness）**：`EvalHarness` 跑 4 个分类用例，量化 `pass_rate` 与是否回退
  7. **健康度综合**：`health = 0.35*verify_gate + 0.30*eval_pass_rate + 0.20*reason_rate + 0.15*replan>=1`

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(super-agent-integration) | 学生(meta-super-agent-integration) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（2903 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 7 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | integration_runner.py, learner.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 未显式标注 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「super-agent-integration」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- （教师未显式标注限制）
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
