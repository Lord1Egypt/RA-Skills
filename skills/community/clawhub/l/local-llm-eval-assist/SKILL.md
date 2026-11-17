---
name: local-llm-eval-assist
displayName: local-llm-eval-assist
slug: local-llm-eval-assist
author: 诺衡(Krites)@SynomosAI
copyright: SynomosAI
version: 1.0.1
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
description: 本地 LLM 自评辅助，用于回答「自己给自己打分会不会虚高」「评估怎么省积分」这类问题
tags:
- 诺衡
- AI技能
- SynomosAI
- nomos-standard-v1
- local-llm-eval-assist
agent_created: true
category: productivity
platforms:
- windows
- macos
- linux
updated: 2026-08-28
fingerprint: FP-MX-0EACEF754985
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
aliases:
- 本地自评辅助
- 机器分校准
- local LLM eval
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺衡(Krites)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺衡
trigger_keywords:
- local
- llm
- eval
- assist
---

自己给自己打分，天然有「虚高」倾向：模型倾向于认同自己的输出，评估者与被评估者不分离，分数就会漂移。本技能解决两件事：让本地 LLM 的自评尽量可信，以及让评估过程少花积分。

## 三个防虚高设计

- **评分维度前置**：先定维度和分档标准，再看被评内容——顺序反了就是「先有结论再找分」；
- **证据必须引用原文**：每个打分点附被评内容的原句，引不出原文的加分扣分无效；
- **双通道对照**：同一份内容用「规则校验」和「模型自评」各跑一次，分差大时以规则为准并标记复核。

## 省积分策略

1. 分层评估：先用零成本的规则检查（长度、格式、关键词命中）筛掉明显不合格；
2. 只对通过初筛的样本调模型细评，调用量通常降一个数量级；
3. 抽样复评：全量细评改为按比例抽检，抽中不合格则扩大该批次抽检面；
4. 缓存判分：相同输入直接复用历史评分，不重复计算。

## 判读边界

- 输出的是**参考分**，不构成对模型能力的认证结论；
- 规则层与模型层结论冲突时，明确报告冲突本身，不取平均和稀泥；
- 「省积分」指减少评估调用量，不承诺任何具体成本数字。

## 常见问题

**问：自评分数能对外引用吗？**
内部迭代用没问题；对外引用须换成独立评测集与可复算脚本——本技能会在输出里主动标注这一限制。

---

© 2026 SynomosAI · 署名：诺衡(Krites)@SynomosAI · 本技能包以 MIT 许可按「原样」提供，不附任何担保（SynomosAI 未申请实体注册、未申请商标注册；LGD 理论文本不在本许可范围内，保留所有权利）。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | 本包无独立代码文件（纯文档/理论件） | — |
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

**本包补充（包级许可事实）**：本包无独立代码文件（纯文档与理论文本件），整体**保留所有权利（All Rights Reserved）**；不适用任何代码许可（含 MIT / Apache-2.0）。
