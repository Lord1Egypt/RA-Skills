---
name: meta-autonomous-deep-research
version: 1.0.0
description: |
  由 model-distillation 从教师技能 autonomous-deep-research 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-autonomous-deep-research（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **autonomous-deep-research** 蒸馏并增强生成。
> 生成时间：2026-07-22 23:28:35 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：autonomous-deep-research —— 自主深度研究, 闭环（research.py 真实实现）, 使用, 输出 `report.json`, 自我进化
- 显性工作流步骤（5 步）：
  1. **分解 Decompose**：把主问题拆成 3–5 个可独立检索的子问题（按连词/关键概念切分）。
  2. **检索 Retrieve**：对每个子问题，优先调用 `rag`(本地知识库) 或 `web-fetch`(在线)；
  3. **综合 Synthesize**：把各子答案按「主张 + 依据 + 置信度」结构聚合成研究报告。
  4. **反思 Reflect**：检查每个子问题是否已有依据、是否存在自相矛盾，定位覆盖空洞。
  5. **迭代 Iterate**：对空洞子问题进入下一轮检索（最多 `max-iter` 轮），逐步逼近完整答案。

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(autonomous-deep-research) | 学生(meta-autonomous-deep-research) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（1395 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 5 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | learner.py, research.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 未显式标注 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「autonomous-deep-research」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- （教师未显式标注限制）
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
