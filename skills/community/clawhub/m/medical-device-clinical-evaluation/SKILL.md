---
name: medical-device-clinical-evaluation
slug: medical-device-clinical-evaluation
displayName: 医械临床评价专家
display_name: 医械临床评价专家
title: 医械临床评价专家
description: >-
  Medical device clinical evaluation skill — 3-path decision tree (exemption / equivalence / clinical investigation), CER writing framework, literature search & clinical data assessment checklists, with official references (NMPA exemption catalog 2025, MDCG 2020-13, FDA 510(k) SE).

  医疗器械临床评价专题——免临床/同品种/临床试验三条路径判定 + CER 撰写框架 + 文献检索与数据评估清单，附 NMPA/MDCG/FDA 官方依据直达。
description_zh: 医疗器械临床评价专题——免临床/同品种/临床试验三条路径判定 + CER 撰写框架 + 文献检索与数据评估清单，附 NMPA/MDCG/FDA 官方依据直达。
description_en: Medical device clinical evaluation skill — 3-path decision tree (exemption / equivalence / clinical investigation), CER writing framework, literature search & clinical data assessment checklists, with official references (NMPA exemption catalog 2025, MDCG 2020-13, FDA 510(k) SE).
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
author: 注册老炮
category: 文档处理
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
license: MIT
tags: ["医疗器械","临床评价","临床评估","CER","同品种比对","等同性论证","免临床目录","免临床试验","临床试验","GCP","MDCG 2020-13","MDCG 2020-5","MDCG 2023-7","SSCP","510(k)","实质等同","substantial equivalence","De Novo","PMA","predicate","对比器械","临床数据","文献检索","PMCF","医疗器械注册","临床评价报告","clinical evaluation report","NMPA","FDA","MDR","CE","临床评价决策树","临床评价报告模板"]
xiaping_category: ["效率工具"]
xiaping_tags: ["医疗器械","临床评价","临床评估","CER","同品种比对","等同性论证","免临床目录","免临床试验","临床试验","GCP","MDCG 2020-13","MDCG 2020-5","MDCG 2023-7","SSCP","510(k)","实质等同","substantial equivalence","De Novo","PMA","predicate","对比器械","临床数据","文献检索","PMCF","医疗器械注册","临床评价报告","clinical evaluation report","NMPA","FDA","MDR","CE"]
agent_created: true
---

# 医械临床评价专家

## 这是什么

聚焦「临床评价」这一个注册关键环节的**实操型技能**：帮你判断产品走哪条临床评价路径、怎么组织临床评价证据、CER（Clinical Evaluation Report）怎么写、文献与临床数据怎么评估。与「注册枢纽」的资料库定位不同，本技能给的是**可落地的决策树 + 检查清单 + 报告框架**，并附各国官方依据直达。

## 为什么用本技能

- **路径不跑偏**：免临床目录 → 同品种比对 → 临床试验，判定顺序和依据一条条给清楚，避免"该免临床的上了试验、该比对的走了目录"这种高成本失误。
- **报告有框架**：CER 按官方模板结构（MDCG 2020-13）组织，文献检索方案先定再查，可追溯、可复核。
- **依据可溯源**：所有结论指向 NMPA / CMDE / MDCG / FDA 官方文件，不凭记忆编造。

## 触发场景（Triggers）

- "临床评价 / 临床评估 / CER" / "免临床目录" / "豁免临床" / "同品种比对" / "等同性论证"
- "510(k) 实质等同 / SE / predicate" / "De Novo" / "PMA 临床数据"
- "MDR 临床评价 / MDCG 2020-13" / "SSCP" / "PMCF"
- "临床试验 / GCP" / "境外临床数据"
- 注册资料里"临床评价资料"模块怎么写

## 使用流程（Workflow）

1. **先定路径**：查免临床目录（中国）→ 不在目录则评估同品种/等同性 → 都不行才临床试验。用 `references/临床评价知识库.md` 的判定决策树。
2. **对市场取依据**：中国看 CMDE 指导原则、欧盟看 MDCG 系列、美国看 510(k) SE / De Novo / PMA，各自取对应章节。
3. **组织证据**：按「文献检索方案 → 等同性/同品种论证 → 临床数据评估 → 获益-风险结论」写 CER；与风险管理文件呼应。
4. **交付**：输出 CER 章节框架 / 路径判定结论 / 文献检索方案表，标注时效（法规会更新，关键处给官方链接复核）。

### references/ 文件导航

| 用户问题 | 加载文件 |
|---|---|
| 路径判定（免临床/同品种/试验） | `临床评价知识库.md` 第一章 |
| 中国免临床目录与同品种比对 | `临床评价知识库.md` 第二章 |
| 欧盟 CER / 等同性 / SSCP | `临床评价知识库.md` 第三章 |
| 美国 510(k) SE / De Novo / PMA | `临床评价知识库.md` 第四章 |
| CER 撰写框架与文献检索 | `临床评价知识库.md` 第五章 |
| 常见误区自查 | `临床评价知识库.md` 第六章 |
| 边界与时效（法规版本核对提醒） | `临床评价知识库.md` 第七章 |

## 使用示例

**示例 1 · 路径判定**
问："我们的产品在中国能免临床吗？"
→ 先查免临床目录（2025 年版，1047 项）是否收录同类产品 → 收录则提交与目录描述的对比说明；未收录评估同品种比对（境内已注册同品种 + 基本等同论证）；都不行才上临床试验。

**示例 2 · CER 撰写**
问："出口欧盟的 IIb 器械 CER 怎么写？"
→ 按 MDCG 2020-13 模板结构组织；等同性论证满足三要素（技术/生物/临床特性 + 可获取等同器械数据）；文献检索方案先行；结论与获益-风险判定（ISO 14971）呼应；IIb/III 类另备 SSCP 摘要。

## 边界说明

- 本技能提供框架与要点，**不替代**公告机构/审评中心的个案裁定；创新器械、边界分类产品建议先咨询专业 RA 或走官方分类界定。
- 法规/标准会更新：免临床目录（2025 版现行）、MDCG 指南（以官方指南库最新版为准）、FDA 指南（改版频繁，用官方检索入口），使用前点开链接复核版本。

## 版权与许可

- © 2026 **注册老炮**。本技能及 references 知识库为原创整理，以 **MIT 协议**开源发布。
- **知识版权声明**：本技能整理的合成知识、方法论、判定决策树与编排体系归「注册老炮」所有；未经授权不得复制、转载、转售，或用于训练任何模型（含商业与开源模型）。
- **免责声明**：本技能按「现状（AS IS）」提供，不提供任何明示或默示的担保；因使用、误用本技能或其输出导致的任何直接或间接损失，作者不承担责任。
- 引用的法规与标准均以官方原文（NMPA / FDA / EU MDR 等）为准，链接指向官方站点；如与官方最新版本不一致，以官方为准。
- 内容仅供合规工作参考，不构成注册代理服务或法律意见。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「这个产品能不能免临床直接报」 / "Can this device skip clinical trials entirely?"
- 「同品种比对要准备哪些证据」 / "What evidence do we need for an equivalence claim?"
- 「临床评价报告从哪几章开始写」 / "Which chapters does the CER start with?"
- 「文献检索要查到什么程度才算够」 / "How thorough does the literature search have to be?"
- 「公告机构要求补 PMCF 计划怎么办」 / "The notified body wants a PMCF plan — now what?"
- 「选哪个已上市产品做对比器械」 / "Which cleared device should we pick as predicate?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-clinical-evaluation
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-clinical-evaluation/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
