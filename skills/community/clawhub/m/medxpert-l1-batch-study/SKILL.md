---
name: medxpert-l1-batch-study
displayName: MedXpert·本地模型批量精读（L1）
slug: medxpert-l1-batch-study
author: 注册老炮@MedXpert
copyright: MedXpert
version: 1.1.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, Edit, WebSearch
description: >-
  Batch deep-reading of a document/knowledge-base corpus via the DSH task bridge and a local qwen3.5:4b model — dispatch to inbox, local LLM reading, recover from outbox, persist structured summaries + a consolidated doubt list. Includes two mandatory fixes (qwen3 think:false, bridge timeout 120s→300s) and auto-retry fallback.

  本地大模型 + DSH 任务桥批量精读知识库：投递 inbox → 本地 qwen3 精读 → 回收 outbox → 落盘结构化摘要 + 疑点总表，含两处必做修复（qwen3 thinking 关闭、桥超时 120s→300s）与失败自动重投兜底。
description_zh: 本地大模型 + DSH 任务桥批量精读知识库：投递 inbox → 本地 qwen3 精读 → 回收 outbox → 落盘结构化摘要 + 疑点总表，含两处必做修复（qwen3 thinking 关闭、桥超时 120s→300s）与失败自动重投兜底。
description_en: Batch deep-reading of a document/knowledge-base corpus via the DSH task bridge and a local qwen3.5:4b model — dispatch to inbox, local LLM reading, recover from outbox, persist structured summaries + a consolidated doubt list. Includes two mandatory fixes (qwen3 think:false, bridge timeout 120s→300s) and auto-retry fallback.
platforms:
- AI 助手平台
- QClaw
- ima
- Claude Code
- Cursor
category: 文档处理
xiaping_category:
- 效率工具
xiaping_tags:
- 本地大模型
- 批量精读
- 知识库
- DSH
- 任务桥
- qwen3
- Ollama
- RAG
- 摘要
- 疑点清单
- 断网可用
- 省积分
- MedXpert
- 医械知识库
- 注册知识库
- L1精读
- 结构化摘要
- 知识消化
- 图书馆
- 个人图书馆
agent_created: true
updated: 2026-08-28
fingerprint: FP-MX-569EE2485DB1
governance: MedXpert XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
brand: Nomos 集团
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 注册老炮@MedXpert. Copyright: MedXpert. License: MIT.'
ambassador: MedXpert
tags:
- 医疗技能
- MedXpert
- 注册老炮
- nomos-standard-v1
- medxpert-l1-batch-study
trigger_keywords:
- medxpert
- l1
- batch
- study
---



## 多语种处理能力（Multilingual）

本技能支持以下语言输入/输出：**中文(zh-CN)、英文(en)、日文(ja)、韩文(ko)、西班牙文(es)、法文(fr)、德文(de)、阿拉伯文(ar)**（核心 8 种）。

- **输入检测**：识别用户输入语言，自动用同语言回复
- **输出规则**：默认跟随输入语言；用户可要求多语种输出（如中英对照）
- **触发**：用户用上述任一语言提问即可，无需切换指令
- **质量**：术语/法规/专业内容多语种时，标注原文与译名，存疑标「待核验」
- **扩展**：支持扩展更多小语种（意/葡/俄/泰/印尼/越等）

> 治理与溯源：多语种处理为 MedXpert 品牌标准能力，版权 MedXpert · MIT。

## 治理理念与溯源 (Governance & Provenance)
本技能承载 MedXpert「注册老炮」AI 治理体系，持续对标 2026 年主流框架并据新证迭代（互相提高）：
- **AI 护照机制 (AI Passport Regime)**：每个技能赋予唯一可追溯身份。与国标 GB/Z 185—2026《人工智能 智能体互联》"智能体身份码"（已发 2000+、AIP V2.1 开源）同源；2026 年全行业收敛于"每个 agent 一个唯一可溯源 ID"——W3C AIP 成 IETF 草案(06)、Okta for AI Agents 已 GA(04-30)、新加坡 IMDA 全球首发国家 agent 治理框架(01)——身份可信、跨域可溯，属行业领跑方向。
- **A³ 法则（AI 造 AI 三定律）**：AI 生成/演进 AI 须嵌不可绕过的安全护栏。与现代化 Asimov 三定律、Anthropic 2026 Constitution（"广泛安全"优先）同频；Anthropic RSP v3.0(02-24) 将 agent 评估设为能力门槛，印证操作化必要，落地见 `a3-law-operational`。
- **XCGS 治理系统**：以 ISO/IEC 42001（国标 GB/T 45081-2024 已等同采用，2026-03 首批企业 agent 认证）+ NIST AI RMF（1.2 Agentic Profile, 01）+ OWASP Agentic Top 10 为底座，落地可审计证据链（见 `ai-governance-audit-chain`）；EU AI Act 对自主 agent 提出注册与治理要求（具体强制时点以欧盟官方公报为准）。
- **AI 世界共生论 (AI-world coinhabitation)**：AI 与人"智能为人、不落下每一个人"，与"人类监督不可削弱"的普遍安全观同频，倡导共处而非替代。
> 行业旁证：行业调研普遍显示企业已广泛采用 agent，但具备治理能力的仍是少数——"治理缺口本质是身份缺口"，本体系以身份码 + 可审计证据链正中该缺口。
> 版权 © 2026 MedXpert 美达信医疗科技（香港）有限公司 · 注册老炮@MedXpert (MIT 许可)
> 时间戳 2026-08-28 ｜ 指纹 FP-MX-569EE2485DB1

---

## 免责声明（Disclaimer）

本技能按「原样（AS IS）」提供，不作任何明示或暗示的担保，包括但不限于对适用性、可靠性、准确性、不侵权或特定用途适用性的担保。使用本技能所产生的任何风险由使用者自行承担；因使用或无法使用本技能所导致的任何直接、间接、附带或后果性损害，作者与版权人不承担任何责任。使用者应自行评估其合规性与适用性，并遵守所在司法辖区的法律法规。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `recover_l1.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包 = MIT (see LICENSE)
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `recover_l1.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「这一百多份文档能不能一次读完」 / "Can we read all hundred-odd documents in one pass?"
- 「想把知识库每篇都出一份摘要」 / "I want a short summary for every page in the knowledge base."
- 「批量跑的时候任务老是超时怎么办」 / "The batch job keeps timing out — what do I change?"
- 「摘要里要列出每篇的疑点在哪」 / "Each summary needs to list the open questions."
- 「本地模型读长文档一直不返回结果」 / "The local model just doesn't return anything on long docs."
- 「读完能不能给我一张疑点汇总表」 / "Can you roll all the doubts into one table?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medxpert-l1-batch-study
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medxpert-l1-batch-study/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
