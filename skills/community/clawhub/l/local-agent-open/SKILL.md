---
name: local-agent-open
displayName: local-agent-open
slug: local-agent-open
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 1.0.1
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, WebFetch
description: 一键打开本地 AI 助手页面（agent-skeleton，http://localhost:3000），用于回答「怎么把本地助手拉出来」「3000 页面打不开」这类问题
tags:
- 诺声
- AI技能
- SynomosAI
- nomos-standard-v1
- local-agent-open
agent_created: true
category: 本地工具
updated: 2026-08-28
fingerprint: FP-MX-A10420410DE8
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
- 打开本地助手
- agent-skeleton启动
- 本地AI页面
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺声
trigger_keywords:
- local
- agent
- open
---

## 用途

本地 AI 助手页面（agent-skeleton）跑在 `http://localhost:3000`。本技能管一件事：把页面可靠地拉起来并打开。「怎么把本地助手拉出来」「3000 页面打不开」都归它。

## 标准动作

1. 探测 3000 端口是否已有服务在听；
2. 在听 → 直接打开浏览器到该地址；
3. 没在听 → 按本地部署路径启动 agent-skeleton，等服务就绪后再开页；
4. 启动失败 → 转入下面的排查清单，不盲目重试。

### 打不开的三种常见原因

- **服务没起**：端口探测失败，先看启动日志最后一行报错；
- **起了但没就绪**：端口通了页面 5xx，等几秒再刷新，别急着重启；
- **端口被占**：另一进程占着 3000，换端口或停占用者，二选一前先问用户。

## 红线

- 只打开本机 `localhost` 页面，**不把本地地址暴露到公网**；
- 不代替用户改防火墙、改 hosts、装依赖——列命令让用户确认；
- 启动命令带副作用（写文件、起后台进程）前，先复述将要执行的动作。

## 常见问题

**问：能固定用别的端口吗？**
可以。启动参数里换端口即可，本技能按新端口探测，不需要改任何文件。

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
