---
name: medical-device-intl-business
displayName: 医疗器械出海经营
description: >-
  Business-level playbook for medical device international expansion — market selection, market-access tiering, entry modes, export trade, distribution channels, international business development, compliance (anti-bribery / export control / data), and localization.

  医疗器械国际业务（出海）经营军师——市场选择、准入分层、进入模式、出口贸易、渠道经销、国际商务、合规（反贿赂/出口管制/数据合规）、本地化的经营视角总入口，与注册技能 reg-hub 分工互补。
description_zh: "医疗器械国际业务（出海）经营军师——市场选择、准入分层、进入模式、出口贸易、渠道经销、国际商务、合规（反贿赂/出口管制/数据合规）、本地化的经营视角总入口，与注册技能 reg-hub 分工互补。"
description_en: "Business-level playbook for medical device international expansion — market selection, market-access tiering, entry modes, export trade, distribution channels, international business development, compliance (anti-bribery / export control / data), and localization. Anchored on IMDRF / MDSAP / ISO 13485 / ISO 14971 and classic international-business theory."
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
slug: medical-device-intl-business
display_name: 医疗器械出海经营
title: 医疗器械出海经营
tags:
  - 医疗器械
  - 出海
  - 国际业务
  - 合规
author: '注册老炮@MedXpert'
license: MIT
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
category: professional
xiaping_category: ["效率工具"]
xiaping_tags: ["医疗器械","国际业务","出海","国际市场","市场准入","海外市场","出口","经销商","代理商","分销","国际商务","国际贸易","市场选择","进入模式","反商业贿赂","FCPA","出口管制","数据合规","GDPR","自由销售证书","CFS","FSC","本地化","IMDRF","MDSAP","ISO 13485","ISO 14971","医疗器械出口","海外报证","海外销售","国际化","market access","international business","medical device export","distribution","regulatory strategy","市场进入","目标市场","海外经销商","医疗器械公司","出海战略"]
agent_created: true
verified_links: "2026-08-24 联网查证：IMDRF 管理委员会成员（含中/美/欧/日/澳/加/巴/韩/新加坡/英/瑞士/俄，WHO 为官方观察员）与 MDSAP 五国（澳TGA/巴ANVISA/加HC/日MHLW-PMDA/美FDA）已按 imdrf.org、mdsap.global、fda.gov 最新状态核对"
icon: "lucide:Globe"
---

# 医疗器械国际业务·出海经营军师

## 这是什么

医疗器械公司做**国际业务（出海）**时的经营决策与执行手册。回答的是老板/国际业务负责人真正会问的问题：

- "我该先做哪个市场？"（市场选择）
- "这个国家怎么进去？注册要多久、花多少？"（准入策略）
- "是找经销商，还是自己设办事处？"（进入模式）
- "出口要哪些证、走什么单证流程？"（出口贸易）
- "跟海外经销商/客户怎么谈、怎么签？"（国际商务）
- "有没有合规红线会让我出事？"（反贿赂/出口管制/数据合规）

它比 `medxpert-reg-hub`（注册合规技术层）**高一层**：reg-hub 管"怎么拿证"，本技能管"怎么把生意做到海外"。

## 与 reg-hub 的分工（重要，避免重复造轮子）

| 维度 | 本技能（intl-business） | medxpert-reg-hub（注册合规） |
|---|---|---|
| 视角 | **经营 / 业务 / 决策** | **法规 / 合规 / 技术文件** |
| 核心问题 | 选市场、定模式、找渠道、控风险 | 分类、技术文件、注册申报、拿证 |
| 典型输出 | 出海路线图、市场对比、经销商协议要点、合规清单 | 注册路径、UDI/STED、生物相容、GMP 核查 |
| 关系 | **注册是其中一环，引用 reg-hub** | 独立完整，只管注册 |

> **铁则**：凡是落到"某产品在 X 国归几类、走 510(k) 还是 MDR、UDI 怎么发码"这类**具体注册技术问题**，一律让位给 `medxpert-reg-hub`，本技能只给"要不要做、怎么做生意、要花多少钱多久"的经营层判断，并指路 reg-hub 拿注册细节。

## 顶层框架（已对齐国际标准，2026-08-24 核验）

### 1. IMDRF —— 全球监管趋同的"总纲"
- **全称**：International Medical Device Regulators Forum（国际医疗器械监管机构论坛），前身 GHTF，2011 年成立。
- **使命**：加速国际医疗器械监管趋同（convergence），降低多市场重复审评负担。
- **管理委员会成员**（11 + 1）：中国 NMPA、美国 FDA、欧盟 DG SANTE、日本 MHLW/PMDA、澳大利亚 TGA、加拿大 HC、巴西 ANVISA、韩国 MFDS、新加坡 HSA、英国 MHRA、瑞士 Swissmedic、俄罗斯卫生部；**WHO 为官方观察员**。
- **对你意味着什么**：这 12 个市场基本覆盖了全球医疗器械的"主流盘子"，是出海优先级的第一梯队参考。
- 官方：https://www.imdrf.org/

### 2. MDSAP —— "一次审核，五国通行"的质量体系杠杆
- **5 个正式成员（RAC）**：澳大利亚 TGA、巴西 ANVISA、加拿大 HC、日本 MHLW/PMDA、美国 FDA。
- **官方观察员**：欧盟（DG SANTE）、新加坡 HSA、英国 MHRA、WHO（IVD 预认证）。
- **附属成员**：韩国 MFDS、墨西哥 COFEPRIS、阿根廷 ANMAT、南非 SAHPRA、马来西亚 MDA、以色列、肯尼亚、TFDA 等。
- **本质**：以 **ISO 13485** 为底 + 各国特定要求，由认可的审核机构（AO）做**一次审核**，出标准 MDSAP 报告/证书，多国互认。
- **关键差异**：MDSAP 证书 ≠ 产品注册批准（仍要单独报注册）；ISO 13485 证书 ≠ MDSAP 证书。
- **强制点**：加拿大 Class II/III/IV 原则上强制要 MDSAP 证书；FDA 可用 MDSAP 报告替代部分常规检查（保留执法权）。
- **三年周期**：初审 → 第 2/3 年监督审核 → 第 3 年再认证。
- **经营价值**：想同时做北美（美/加）+ 日本 + 巴西 + 澳洲，**一个 MDSAP 覆盖五个市场的体系审核**，是成本最省的打法。
- 官方：https://www.mdsap.global/ ｜ https://www.fda.gov/medical-devices/cdrh-international-programs/medical-device-single-audit-program-mdsap

### 3. 底层质量标准
- **ISO 13485:2016** —— 医疗器械质量管理体系（现行版，MDSAP 的底）。
- **ISO 14971:2019** —— 风险管理（各国注册技术文件都要）。

## 触发场景（Triggers）

用户提到以下任意内容时加载本技能：

- "出海" / "国际业务" / "国际化" / "海外市场" / "出口"
- "先做哪个国家" / "哪个市场好做" / "市场选择" / "目标市场"
- "找经销商" / "代理商" / "分销" / "渠道" / "本地合作伙伴"
- "自己设公司还是找代理" / "办事处" / "子公司" / "进入模式"
- "出口单证" / "报关" / "物流" / "关税" / "结算" / "信用证"
- "自由销售证书" / "CFS" / "FSC" / "出口销售证明"
- "反商业贿赂" / "FCPA" / "合规红线" / "出口管制" / "数据出境" / "GDPR"
- "国际商务" / "询盘" / "报价" / "投标" / "国际展会"
- "本地化" / "多语言标签" / "翻译" / "当地代表"
- "MDSAP" / "一次审核多国" / "IMDRF" / "监管趋同"
- 结合产品问经营问题，如"关节镜钳出海先做哪几个国家、要准备多少钱"

## 使用流程（Workflow）

1. **判断是经营问题还是注册问题**：注册技术细节（分类/510(k)/MDR/UDI）→ 转 `medxpert-reg-hub`；经营决策（选市场/定模式/找渠道/控风险）→ 本技能。
2. **定位子问题**：按 `references/` 导航表加载对应文件。
3. **给结论 + 权威框架**：结论对齐 IMDRF / MDSAP / ISO / 国际商务理论，附官方链接。
4. **生成交付物**：出海路线图、市场对比表、合规清单、经销商协议要点等，输出 Markdown / HTML。
5. **标注时效与边界**：法规与准入门槛会变，关键数据提示"以官方最新发布为准"；不构成法律/贸易合规意见。

### references/ 文件导航

| 用户问题类型 | 加载文件 |
|---|---|
| 全局框架 / 市场分级 / 准入路径总览 | `国际业务全景与市场准入分层.md` |
| 先做哪个市场 / 市场选择 / 进入模式 | `出海战略与市场选择.md` |
| 经销商 / 代理 / 询盘报价 / 投标 | `国际商务与渠道管理.md` |
| 反贿赂 / 出口管制 / 数据合规 / CFS | `国际合规与贸易.md` |

## 关键事实速查（避免常见误判）

- **MDSAP 五国 ≠ 产品批准**：MDSAP 只解决"质量体系一次审核多国认"，产品仍要逐国报注册。别以为拿了 MDSAP 就能直接卖。
- **加拿大是 MDSAP 的"硬门槛"**：Class II/III/IV 器械在加拿大原则上要有 MDSAP 证书才发产品注册证（MDL）。
- **FDA 注册（Establishment Registration + Listing）≠ 510(k) 获批**：注册列名是"交钱登记"，510(k) 是"上市前许可"。两者常被混淆。
- **欧盟 CE 是"自我声明 + 公告机构"分级**：低风险（Class I 非无菌非测量）可自我声明，中高风险要公告机构（Notified Body）审——公告机构产能是欧盟出海的关键瓶颈之一。
- **出海第一梯队参考**：IMDRF 管理委员会成员（中/美/欧/日/澳/加/巴/韩/新加坡/英/瑞士/俄）+ WHO 覆盖市场，通常也是注册路径最成熟、付费能力最强的盘子。
- **合规是"生意能做多久"的命门**：海外渠道给回扣、灰色佣金、数据带出境，任何一条踩雷都可能让整条出海线崩掉——见 `国际合规与贸易.md`。

## 注意事项

- 本技能为经营决策参考，**不构成法律意见 / 贸易合规意见 / 注册代理服务**；重大合同、合规红线请咨询专业律师与注册事务（RA）专家。
- 市场准入门槛、关税、汇率、合规规则会变，关键结论以官方与专业渠道最新发布为准。
- 注册技术细节一律以 `medxpert-reg-hub` 的 references（20 枢纽，已核验）为准，本技能不重复维护。

## 版权与许可

- © 2026 注册老炮 (MedXpert)。原创整理，采用 MIT 协议（详见随包 LICENSE.md）；软件依 LICENSE 使用，零数据收集。
- **知识版权声明**：本作品汇集的方法论、对比分析、结构化知识与合成内容，其编排与原创表达归 注册老炮 (MedXpert) 所有；未经书面许可，不得复制、转载、摘编、转售或用于训练任何模型 / 商业系统。
- **免责声明**：本作品按「现状」（AS IS）提供，不提供任何明示或暗示担保；使用风险由使用者自行承担，因使用所致任何损失作者不承担责任。
- 引用的监管框架（IMDRF / MDSAP / ISO）与法规以官方原文为准，链接指向官方站点；与官方不一致时以官方为准。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「我们的器械想卖到东南亚，先打哪个国家」 / "Which Southeast Asian country should we enter first"
- 「直接出口还是找当地经销商」 / "Should we export directly or use a local distributor"
- 「海外市场准入要分几步走」 / "How many steps to get market access overseas"
- 「经销商压价太狠，渠道怎么重搭」 / "Distributors are squeezing our margin, how to rebuild the channel"
- 「出海团队怎么搭，本地化要投多少」 / "How do we staff an overseas team and localize"
- 「海外销售给医院返点算不算商业贿赂」 / "Are hospital rebates overseas considered bribery"

Trigger when the user says any of the above, in Chinese or English.

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-intl-business
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-intl-business/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
