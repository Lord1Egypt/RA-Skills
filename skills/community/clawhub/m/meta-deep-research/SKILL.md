---
name: meta-deep-research
version: 1.0.0
description: |
  由 model-distillation 从教师技能 deep-research 蒸馏并增强的超越型元技能。
  蒸馏其「大纲 -> 并行深度搜索 -> 报告」三阶段人机协作调研流程，叠加自验证、
  自我反思、super-agent 编排与持续自进化闭环，输出更可靠可追溯、逐步超越教师。
agent_created: true
visibility: public
---
# meta-deep-research（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **deep-research** 蒸馏并增强生成。
> 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略「主动与其他大模型对话、蒸馏、逐步超越」）。

## 来源能力签名（教师 deep-research）
- 定位：基于 Deep-Research-skills 项目的人机协作结构化调研能力。
- 核心命令：`/research <topic>`（生成 outline.yaml+fields.yaml）→ `/research-deep`（并行 web-search-agent 逐项搜索，写入 results/）→ `/research-report`（汇总 report.md）；另有 `/research-add-items`、`/research-add-fields` 追加。
- 适用：学术综述 / Benchmark 对比 / 技术选型 / 竞品市场分析 / 尽职调查。
- 输出结构：`{topic}/outline.yaml`、`fields.yaml`、`results/item_N.yaml`、`report.md`。

## 蒸馏出的真实工作流（继承 + 强化）
1. **大纲阶段 `/research`**：把调研主题拆成 items（调研对象）与 fields（字段定义），产出 `outline.yaml`+`fields.yaml`，请用户确认/修改后再继续。
2. **深度阶段 `/research-deep`**：对每个 item 并行发起 web-search-agent，按 fields 收集结构化数据，落盘 `results/item_N.yaml`。
3. **报告阶段 `/research-report`**：汇总所有 results 为 Markdown `report.md`，覆盖每个 field、标注来源与不确定性。

## 增强点（超越教师）
1. **可靠自验证**：大纲生成后用 `reason-verify` 校验 items/fields 自洽与覆盖度；每个 results 落盘前做事实锚定（来源可追溯），reliability<0.8 即回退重做该 item。
2. **自我反思闭环**：每段调研结束后写入 `self-reflection-loop`，沉淀"哪些检索策略失败 / 哪些领域信息稀缺"，反哺下次大纲拆分。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被 `long-horizon-planner` 编排为长程调研任务。
4. **对抗验证蒸馏质量**：对"并行搜索是否漏检关键反方信息"做反例测试，防止只搜到支撑性证据（确认偏误）。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(deep-research) | 学生(meta-deep-research) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（2612 字符，薄包装） | 蒸馏提取真实三阶段流程 + 元进化增强 |
| 工作流 | 大纲→深度→报告（无自验证钩子） | 同流程 + 自验证钩子 + 反思步 + 反确认偏误 |
| 失败防护 | 未显式标注 | 显式 limits + 对抗验证（漏检反方） |
| 自进化 | 无 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点命令 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成深度调研任务；本技能在教师能力之上叠加自验证、反确认偏误与反思，输出更可靠、可追溯、可复用。

## 已知限制（来自教师蒸馏 + 元进化补充）
- 教师本身为薄包装（真实子技能在各 research-* 子目录），蒸馏未覆盖其全部子代理策略，深度使用需对照原技能核验。
- 依赖 WebSearch 能力；联网受限时并行搜索阶段会退化。
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
