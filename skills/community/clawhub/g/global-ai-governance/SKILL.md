---
name: global-ai-governance
slug: global-ai-governance
display_name: 全球AI治理版图
displayName: 全球AI治理版图
title: 全球AI治理版图
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
category: 通用技能
platforms:
  - windows
  - macos
  - linux
  - web
author: 注册老炮
license: MIT
description: >-
  A quick-reference map of global AI governance: who is setting the rules, in which forum, and on what timeline. It covers the World AI Cooperation Organization, UN processes, China's initiative lineage, national AI safety institutes and summits, and the strategies of major economies. Use when you need the big picture before a policy brief, a market-entry decision or a board discussion.

  全球 AI 治理版图速查手册——从宏观视角梳理 AI 世界治理格局：世界人工智能合作组织（WAICO，2026-07 上海成立、29 创始国、全球首个 AI 政府间国际组织）、联合国体系（全球数字契约、AI 独立国际科学小组首份报告 2026-07-01、联大能力建设决议、UNESCO）、中国 AI 治理倡议谱系（2023 全球人工智能治理倡议到 2026 人工智能合作发展行动计划）、国际 AI 安全机制（AI 安全峰会系列、各国 AI Safety Institute、国际 AI 安全报告）、主要经济体 AI 战略（美欧英日韩印）、全球南方能力建设与数字鸿沟、治理机制化转型趋势。附零依赖本地工具一键速查国际组织、倡议事件、地区战略与时间线。面向政策研究者、出海战略与行业观察者，企业 AI 治理（ai-governance-playbook）的宏观延伸。
description_en: A quick-reference playbook for global AI governance — the world-level landscape, covering the World Artificial Intelligence Cooperation Organization (WAICO, founded in Shanghai July 2026 with 29 founding members, the first intergovernmental AI organization), the UN system (Global Digital Compact, first report of the UN independent AI science panel July 2026, General Assembly capacity-building resolution, UNESCO), China's AI governance initiative lineage (2023 Global AI Governance Initiative to the 2026 AI Cooperation Development Action Plan), international AI safety mechanisms (AI Safety Summit series, national AI Safety Institutes, International AI Safety Report), major-economy AI strategies (US/EU/UK/JP/KR/IN), Global South capacity building and the digital divide, and the trend toward institutionalized governance. Includes a zero-dependency local toolkit for organization, initiative, regional-strategy and timeline queries. Built for policy researchers, go-global strategists and industry observers — the macro-level extension of the enterprise AI governance playbook.
tags:
  - 全球AI治理
  - WAICO
  - 世界人工智能合作组织
  - 联合国
  - AI安全
  - 国际治理
  - 全球数字契约
  - 地缘政治
  - Global AI Governance
  - AI Safety
  - 国际组织
---

# 全球 AI 治理版图

全球 AI 治理速查工作台：**看得懂国际格局、查得到组织机制、对得上倡议谱系、跟得上治理趋势**。面向政策研究者、出海战略与行业观察者——从 WAICO 成立到联合国科学小组报告，AI 世界治理正在从"论坛对话"走向"机制化合作"。

## 什么时候用这个技能

- **国际格局**：「全球 AI 治理有哪些主要机制和组织？」
- **WAICO**：「世界人工智能合作组织是什么？谁参加了？」
- **联合国**：「联合国在 AI 治理上做了什么？」
- **中国倡议**：「中国在全球 AI 治理上的倡议谱系？」
- **国际安全**：「AI 安全峰会和 AI Safety Institute 是什么？」
- **国别战略**：「各国 AI 战略重点是什么？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

> 「WAICO 是什么？和联合国什么关系？」
> 「中国在全球 AI 治理上提了哪些倡议？」
> 「全球 AI 治理未来会怎么走？」

### 模式二：本地工具（要结构化结果）

```bash
# ① 国际组织速查
python tools/global_ai_toolkit.py org --name waico      # waico/un/brics/g7/oecd/unesco

# ② 倡议事件速查（按主体）
python tools/global_ai_toolkit.py initiative --actor cn   # cn=中国 / un=联合国 / intl=国际峰会

# ③ 主要经济体 AI 战略速查
python tools/global_ai_toolkit.py region --name us       # us/eu/uk/jp/kr/in

# ④ 全球治理时间线
python tools/global_ai_toolkit.py timeline

# ⑤ 趋势观测清单
python tools/global_ai_toolkit.py assess

# 查看全部命令
python tools/global_ai_toolkit.py --help
```

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 全球治理格局 | `references/01-全球治理格局.md` | 多极格局、机制分类、组织地图 |
| ② 联合国体系 | `references/02-联合国体系.md` | 数字契约、科学小组、联大决议、UNESCO |
| ③ 中国倡议谱系 | `references/03-中国倡议谱系.md` | 2023 全球 AI 治理倡议到 2026 行动计划 |
| ④ WAICO 详解 | `references/04-WAICO详解.md` | 成立背景、组织架构、29 创始国、定位 |
| ⑤ 国际 AI 安全机制 | `references/05-国际AIS安全机制.md` | 峰会系列、AI Safety Institute、国际报告 |
| ⑥ 主要经济体战略 | `references/06-主要经济体战略.md` | 美欧英日韩印 AI 战略速览 |
| ⑦ 全球南方与能力建设 | `references/07-全球南方与能力建设.md` | 数字鸿沟、普惠计划、南南合作 |
| ⑧ 趋势与 FAQ | `references/08-趋势与FAQ.md` | 机制化转型、地缘政治、高频疑问 |

## 快速上手（三步）

1. **看格局**：`org` 命令速查主要组织，对照 01 模块组织地图；
2. **对倡议**：`initiative` 查倡议谱系，`timeline` 看时间线；
3. **跟趋势**：`assess` 输出观测清单，08 模块看机制化转型判断。

## 能力边界（如实说明）

- **本技能是速查与框架，不是政策立场**：全球治理动态变化快，引用前以官方发布为准；
- **组织与倡议信息以公开报道整理**（核对基准日见各模块头部），WAICO 等新机制细则待组织运转后更新；
- **工具不联网**：本地规则匹配，不采集数据、不调用外部服务。

## 常见问题（FAQ）

- **Q：WAICO 和联合国什么关系？** WAICO 是独立的政府间国际组织（总部上海、29 创始国），定位为联合国框架努力的有益补充；中国支持联合国发挥 AI 治理主渠道作用（见 04 模块）。
- **Q：全球 AI 治理为什么重要？** AI 发展速度已快于治理能力提升（联合国开发计划署署长语）——规则碎片化、数字鸿沟、话语权失衡是三大结构性挑战（01 模块）。
- **Q：和我们的企业 AI 治理什么关系？** 宏观版图是企业合规的方向标——全球治理规则会逐步转化为各市场法规（如欧盟 AI Act、中国法规），企业治理是微观落地。
- **Q：工具脚本要装依赖吗？** 不需要，仅 Python 标准库。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的全球治理方法论、组织梳理、倡议整理与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与信息准确性保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「各国AI监管现在到哪一步了」 / "Where do different countries actually stand on AI rules?"
- 「这个国际AI组织对出海有啥影响」 / "How does this new international AI body affect companies going global?"
- 「写政策简报要梳理全球治理脉络」 / "I need the global governance picture for a policy brief."
- 「欧盟和美国的AI立法差在哪」 / "How do EU and US AI laws differ?"
- 「进新市场前要不要看当地AI规则」 / "Should we check local AI rules before entering a market?"
- 「联合国那个AI科学小组出报告了吗」 / "Has the UN AI science panel published its report yet?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/global-ai-governance
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/global-ai-governance/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
