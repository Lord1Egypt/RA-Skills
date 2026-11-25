---
name: hu5-self-evolve-v1
display_name: "任务后三问复盘与进化日志"
display_name_en: "Post-Task Three-Question Review & Evolution Log"
description: "任务后自省复盘与进化日志沉淀。触发场景：用户说复盘一下/自省/进化日志/这次学到了什么/沉淀经验，或一次复杂任务完成后需要收尾沉淀时触发。产出物：①三问复盘结论（做对了什么/踩了什么坑/下次怎么更快）②可写入长期记忆的教训条目与改进清单 ③scripts/gen_evolution_log.py 生成的 Markdown 进化日志。不适用于业务经营或行情复盘（用 行情复盘类技能）、纯知识问答、单文件操作。"
description_zh: "每件事办完问三句，把经验沉淀成可复用的进化日志，下次同类任务直接从教训里起步。"
description_en: "Three questions after every task turn experience into a reusable evolution log, so the next similar task starts from lessons already learned."
examples_zh:
  - "这件事办完了，帮我做个三问复盘"
  - "把这周的经验沉淀成进化日志"
  - "帮我复盘刚才那个失误，下次别再犯"
examples_en:
  - "Run a three-question review on what we just finished"
  - "Turn this week's experience into an evolution log"
  - "Review my mistake just now so it does not repeat"
version: 1.0.1
author: "HU5 琉璃宇宙"
---
# 任务后自省复盘（self-evolve）

## 概述
把“干完一件活”变成“下一次更快、更稳”。每次复杂任务收尾时，用**三问复盘法**把经验沉淀为可复用的记忆与日志，让助手这具分身持续变强。

> 注意：这是“能力工程化沉淀”，**不是**宣称能自我进化成 AGI。它让工具更好用、记忆更厚，但不改变底层模型。

## 你的工作方式
- **只写真实发生的**：做对了什么、踩了什么坑，必须是真实过程，禁止编造“感悟”。
- **区分三类产出**：①可固化的方法（→写成 skill/清单）；②需记住的教训（→写 memory 的 agent_md）；③项目进展/决策（→写 memory 的 memory_md）。
- **不刷流水账**：每条经验要能指导下次行动，否则不写。
- **确认门**：涉及写入长期记忆或改动已有技能时，先列要点让用户过目（用户已明确要求“自动沉淀”时可直接执行）。

## 三问复盘法
1. **做对了什么？** → 哪个动作/顺序/工具组合有效，能否固化成标准动作。
2. **踩了什么坑？** → 报错原因、弯路、返工点；根因是什么，下次怎么提前避开。
3. **下次怎么更快？** → 一句话可执行的改进（预置模板、并行策略、先查后做等）。

## Phase 1 · 回顾
读本次任务的执行链，按三问提取事实（清单随本技能内置，不再依赖外部 references 文件）：

**一问 · 做对了什么**
- [ ] 哪个步骤顺序/工具组合让任务一次成？
- [ ] 哪个并行/批处理省了时间？
- [ ] 哪次确认门（先问再做）避免了返工？
- [ ] 能否抽成模板/脚本/清单，下次直接套？

**二问 · 踩了什么坑**
- [ ] 报错的**根因**是什么（不是现象）？
- [ ] 是否重复犯了以前记过的坑？
- [ ] 返工/等待发生在哪一步？
- [ ] 环境依赖（如 dot、目录、接口参数）是否需要预检？

**三问 · 下次怎么更快**
- [ ] 用一句话写出可执行改进（谁来、何时、做什么）。
- [ ] 需要预置的模板/脚本/清单是否已就位？
- [ ] 是否需要把这条写进 memory 或 skill？

## Phase 2 · 沉淀
- 教训类 → 写入长期经验档（可追加的经验条目）
- 进展/决策类 → 写入项目记忆档（可复用的结论与决策）
- 方法类 → 建议固化为 skill 或追加到相关参考文档
- 汇总成进化日志：
```bash
python3 scripts/gen_evolution_log.py review.json -o 进化日志_YYYYMMDD_任务名.md
```
`review.json` 格式见 `scripts/review.example.json`。

## Phase 3 · 归档
生成的进化日志按需归档到项目文档库（与本技能正文同目录的项目资料区）。

## 示例
**示例1（技术踩坑）**：任务中 `dot` 缺失报错 → 记入 agent_md「沙箱系统包不持久，渲染前先装 graphviz」；下次直接预检。
**示例2（流程优化）**：并行写同目录冲突 → 记入 agent_md「先建目录或串行写」；下次一次成功。

## 资源目录
- `scripts/gen_evolution_log.py` — 进化日志生成器（JSON → Markdown）
- `scripts/review.example.json` — 输入示例
- 三问复盘检查清单已内置于 Phase 1

## 边界
- 不做业务经营/市场行情复盘（那是行情复盘类技能的活）。
- 不替代对项目的正式复盘报告；本技能只沉淀“我的工作经验”。
- 不修改底层模型、不承诺 AGI 能力。
