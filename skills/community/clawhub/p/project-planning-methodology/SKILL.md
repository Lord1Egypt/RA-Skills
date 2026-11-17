---
name: project-planning-methodology
displayName: project-planning-methodology
slug: project-planning-methodology
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 1.0.1
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Task
description: 项目计划制作方法论（WBS + CPM + RACI 三件套），用于回答「这个项目怎么排期」「任务怎么拆」「谁负责哪块」这类问题
tags:
- 诺声
- AI技能
- SynomosAI
- nomos-standard-v1
- project-planning-methodology
agent_created: true
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
- 项目计划方法论
- WBS-CPM-RACI
- 项目排期
category: 项目管理
updated: 2026-08-28
fingerprint: FP-MX-876A9A7C9563
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺声
trigger_keywords:
- project
- planning
- methodology
---

「项目怎么排期」从来不是一张甘特图能解决的，缺的是三件套各司其职：**WBS 管拆、CPM 管序、RACI 管人**。本技能按这个分工帮你把计划做实。

### WBS：把目标拆成可交付的块

1. 从最终交付物倒推，拆到「一个人一段能完成」的最小工作包；
2. 每个工作包必须有完成判据（什么算做完），写不出判据就说明还没拆透；
3. 拆完检查：有没有块依赖三个以上其他块——有就再拆或重排。

### CPM：把块排成关键路径

先把依赖关系画成网络：哪些块必须等前面完成，哪些能并行。关键路径上任何一块延期，总工期就延期——排期讨论聚焦关键路径，非关键块的弹性标注出来即可。

### RACI：把块分到人

| 角色 | 含义 | 每块的允许数量 |
|---|---|---|
| R 负责执行 | 实际干活的人 | 恰好 1 个 |
| A 拍板担责 | 做完谁验收、卡住谁决策 | 恰好 1 个 |
| C 需被咨询 | 动手前要问的人 | 按需 |
| I 需被告知 | 完成后通知即可 | 按需 |

一块两人 A 或没人 R，是计划里最常见的隐形地雷。

## 常见翻车点

- 排期只画了任务没画依赖，并行块互相等；
- RACI 里全员都是 C，没人拍板；
- 关键路径上塞了「等等看」的块——那它就是新的关键路径，要重新排。

## 常见问题

**问：小项目也要搞三件套吗？**
三人以下的短项目，WBS 加一句「谁负责」通常就够；依赖超过一条链、或跨部门时，CPM 和 RACI 才开始值回成本。

---

© 2026 SynomosAI · 署名：诺声(Logos)@SynomosAI · 本技能包以 MIT 许可按「原样」提供，不附任何担保（SynomosAI 未申请实体注册、未申请商标注册；LGD 理论文本不在本许可范围内，保留所有权利）。

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
