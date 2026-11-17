---
name: medical-device-techfile-sted
displayName: 医械技术文件STED专家
description: >-
  Medical device technical documentation & STED skill — IMDRF STED 6-chapter structure, EU MDR Annex II/III, FDA 510(k) Summary/eSTAR, CN submission files (Notice 121/122), JP technical files comparison & writing points with official references.

  医疗器械技术文件与STED专题——IMDRF STED 六章、MDR Annex II/III、510(k) Summary/eSTAR、中国121/122号公告申报资料、日本技术资料对照与撰写要点，官方入口直达。
description_zh: 医疗器械技术文件与STED专题——IMDRF STED 六章、MDR Annex II/III、510(k) Summary/eSTAR、中国121/122号公告申报资料、日本技术资料对照与撰写要点，官方入口直达。
description_en: Medical device technical documentation & STED skill — IMDRF STED 6-chapter structure, EU MDR Annex II/III, FDA 510(k) Summary/eSTAR, CN submission files (Notice 121/122), JP technical files comparison & writing points with official references.
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
author: 注册老炮
category: 文档处理
xiaping_category: ["效率工具"]
xiaping_tags: ["医疗器械","技术文件","技术文档","STED","Summary Technical Documentation","IMDRF","GHTF","MDR Annex II","MDR Annex III","技术文档结构","510(k) Summary","eSTAR","eRPS","注册申报资料","121号公告","122号公告","DHF","DMR","ISO 13485","医疗器械档案","设计控制","21 CFR 820.30","807.92","技术文档撰写","CTD","医疗器械注册","technical documentation","technical file","design history file"]
agent_created: true
slug: medical-device-techfile-sted
display_name: 医械技术文件STED专家
title: 医械技术文件STED专家
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
license: MIT
tags: ["医疗器械","技术文件","技术文档","STED","IMDRF","MDR Annex II","510(k) Summary","eSTAR","eRPS","注册申报资料","121号公告","122号公告","DHF","DMR","ISO 13485","设计控制","technical documentation","technical file"]
---

# 医械技术文件STED专家

## 这是什么

聚焦「技术文件（Technical Documentation）」这一注册核心交付物的**实操技能**：以 IMDRF STED 六章为骨架，映射欧盟 MDR Annex II/III、美国 510(k) Summary/DHF、中国 121/122 号公告申报资料、日本技术资料的撰写要点与结构差异。同一款器械的证据链（描述→风险→验证→临床→标签）高度一致，**写一套、映射各国**，最大化复用、减少重复工作。

## 为什么用本技能

- **骨架统一**：以 STED 六章为底座，各国章节映射表一眼看清"这一段是哪国的哪一章"。
- **不踩结构坑**：MDR Annex II 六章、510(k) Summary 必备内容、中国 eRPS 六模块，结构差异对照表逐条对齐。
- **入口直达**：eSTAR 电子模板、eRPS 系统、IMDRF 文档库、EUR-Lex 法规原文，官方入口全部备齐。

## 触发场景（Triggers）

- "技术文件 / 技术文档 / STED" / "Summary Technical Documentation"
- "MDR 技术文档 / Annex II / Annex III"
- "510(k) Summary" / "eSTAR" / "DHF / DMR"
- "注册申报资料 / eRPS" / "121 号公告 / 122 号公告"
- "技术文档结构" / "文档差异对照"
- 产品注册资料体系怎么搭

## 使用流程（Workflow）

1. **定市场与类别**：产品在哪些市场注册、类别（影响提交物与审评方式）。
2. **以 STED 六章搭骨架**：器械描述与规格 / 基本信息（标签） / 设计与制造 / 通用安全性能原则 / 风险分析 / 验证与确认。
3. **按市场映射**：用 `references/技术文件STED知识库.md` 的对照表，补齐各国特有章节（中国综述资料、欧盟 GSPR、美国 SE 论证）。
4. **逐章撰写**：每章按撰写要点组织，证据链互相引用（风险→验证→临床→标签闭环）。
5. **提交前自查**：用结构差异对照表核对完整性；标注时效（eSTAR 模板版本、法规更新）。

### references/ 文件导航

| 用户问题 | 加载文件 |
|---|---|
| 文档类型对照总览 | `技术文件STED知识库.md` 第一章 |
| STED 六章结构 | `技术文件STED知识库.md` 第二章 |
| 美国 510(k) Summary / eSTAR | `技术文件STED知识库.md` 第三章 |
| 欧盟 MDR 技术文档 | `技术文件STED知识库.md` 第四章 |
| 中国注册申报资料 | `技术文件STED知识库.md` 第五章 |
| 日本技术资料 | `技术文件STED知识库.md` 第六章 |
| 结构差异对照表 | `技术文件STED知识库.md` 第七章 |

## 使用示例

**示例 1 · 写一套多市场用**
问："产品要出中国、欧盟、美国，技术文件怎么写才不重复？"
→ 以 STED 六章为骨架写一套完整技术文件，再按市场映射：中国补综述资料/技术要求章节（121 号公告）、欧盟补 GSPR 符合性章节（Annex II 第 4 章）、美国补 SE 论证与 Summary（807.92）。证据链（描述→风险→验证→临床→标签）一次建立、处处引用。

**示例 2 · eSTAR 提交**
问："美国 510(k) 用什么提交？"
→ 用 FDA eSTAR 电子模板（当前模板以 FDA 官网最新版为准）强制电子提交；Summary 必备内容：器械名称/分类/预期用途、predicate 对比、技术特征、性能数据摘要、标准符合性、标签要点。

## 边界说明

- 本技能提供框架与要点，不替代审评中心/公告机构对具体产品的裁定；eSTAR 模板版本、法规要求以官方最新发布为准。
- 法规会更新（eSTAR 模板滚动升级、中国公告如有修订、MDR 协调标准滚动更新），使用前点开链接复核版本。

## 版权与许可

- © 2026 **注册老炮**。本技能及 references 知识库为原创整理，以 **MIT 协议**开源发布。
- **知识版权声明**：本技能整理的合成知识、方法论与编排体系归「注册老炮」所有；未经授权不得复制、转载、转售，或用于训练任何模型（含商业与开源模型）。
- **免责声明**：本技能按「现状（AS IS）」提供，不提供任何明示或默示的担保；因使用、误用本技能或其输出导致的任何直接或间接损失，作者不承担责任。
- 引用的法规与标准均以官方原文（NMPA / FDA / EU MDR 等）为准，链接指向官方站点；如与官方最新版本不一致，以官方为准。
- 内容仅供合规工作参考，不构成注册代理服务或法律意见。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「技术文件按六章结构怎么搭」 / "How should we structure the technical file around the six chapters?"
- 「一套资料能不能同时报欧美中」 / "Can one document set cover the US, EU and China at once?"
- 「美国的摘要要写多长」 / "How long should the US summary document be?"
- 「提交前要准备哪些附件」 / "What attachments do we need ready before we submit?"
- 「设计历史文件和技术文档啥区别」 / "What is the difference between the design history file and the technical file?"
- 「公告机构说技术文档缺章节怎么办」 / "The notified body says chapters are missing — what now?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-techfile-sted
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-techfile-sted/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
