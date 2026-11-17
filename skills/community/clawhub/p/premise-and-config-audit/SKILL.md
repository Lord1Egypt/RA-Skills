---
name: premise-and-config-audit
displayName: premise-and-config-audit
slug: premise-and-config-audit
author: 诺衡(Krites)@SynomosAI
copyright: SynomosAI
version: 1.0.1
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
description: 「前提验证 + 配置审计」方法论，用于回答「开工前该先验什么」「我现在的工具链配置是不是较优」「方案为什么走偏了」这类问题
tags:
- 诺衡
- AI技能
- SynomosAI
- nomos-standard-v1
- premise-and-config-audit
agent_created: true
category: 方法论
updated: 2026-08-28
fingerprint: FP-MX-8DC22AE3866A
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
- 前提验证方法论
- 配置审计
- 假设证伪
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺衡(Krites)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺衡
trigger_keywords:
- premise
- and
- config
- audit
---

## 为什么先验前提

大多数「方案走偏」不是执行出错，是开工时有一条错误前提没被质疑：以为数据是全的、以为接口是通的、以为上次的结论这次还成立。本技能把「开工前该先验什么」变成清单动作，把「为什么走偏」变成可回溯的检查。

### 前提四问（动工前逐条回答）

1. **事实前提**：方案依赖哪些「我认为是真的」？每条标注证据来源；
2. **失效后果**：哪条前提若不成立，方案哪一步最先崩？
3. **最便宜的验证**：有没有一条命令、一次查询能在短时间内证伪它？
4. **回退路径**：前提被证伪时，退回哪个备选方案？

### 配置审计三查

- **漂移**：当前配置与文档基线是否一致——不一致处以实跑结果为准、文档标记待修；
- **冗余与冲突**：同一件事是否有两套配置在竞争生效（helper 链、环境变量、多份配置文件）；
- **敏感项**：密钥、令牌是否落在配置文件明文里——是则只报位置与建议，不复述值。

## 方案走偏了怎么回溯

1. 找到当前结果与预期的第一个分岔点；
2. 在分岔点列出当时依赖的前提，逐条补验；
3. 修正前提后重放，而不是在偏了的路径上继续打补丁。

## 边界

- 审计结论落到「哪条前提、什么证据、验没验过」，不给笼统的「配置有问题」；
- 不替代正式的安全审计与渗透测试；
- 清单是通用的，行业特定前提（如合规基线）由使用者按需补充。

## 常见问题

**问：前提验证会不会拖慢开工？**
四问通常十几分钟；相比在错误前提上跑完整条流水线再返工，这是最便宜的一段路。

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
