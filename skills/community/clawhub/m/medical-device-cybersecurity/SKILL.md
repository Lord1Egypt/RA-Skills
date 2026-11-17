---
name: medical-device-cybersecurity
slug: medical-device-cybersecurity
display_name: 医疗器械网络安全
displayName: 医疗器械网络安全
title: 医疗器械网络安全
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
  A working reference for medical device cybersecurity, covering what regulators expect in a premarket submission and how to keep a device secure once it is in use.

  医疗器械网络安全合规实操手册——覆盖全球三大市场监管要求（美国 FDA 2026 网络安全强制：SBOM 软件物料清单/漏洞管理/渗透测试，缺失即不予受理 RTA；欧盟 MDR Annex I 17.2 + NIS2 + Cyber Resilience Act 2027；中国 NMPA 网络安全注册审查指导原则）、SBOM 构建实操（字段/更新/供应链）、漏洞管理与协调披露（CVSS 分级/修复时限）、网络安全体系与文档（ISO/IEC 81001-5-1、与 ISO 13485/62304 联动、上市后监控），含三地要求对照与申报文档清单，附零依赖本地工具一键查询区域要求、生成检查清单与 SBOM 字段模板。面向医械法规、研发与信息安全负责人，与 AI 医疗器械合规互补。
description_en: "A working reference for medical device cybersecurity, covering what regulators expect in a premarket submission and how to keep a device secure once it is in use. It walks through threat modelling, security requirements, the software bill of materials, vulnerability handling, and the documentation reviewers ask for. Use when preparing security materials for a submission or responding to a reported vulnerability."
tags:
  - 医疗器械
  - 网络安全
  - SBOM
  - FDA
  - MDR
  - NMPA
  - 渗透测试
  - 漏洞管理
  - CRA
  - Medical Device
  - Cybersecurity
  - ISO 81001
description_zh: "医疗器械网络安全合规实操手册——覆盖全球三大市场监管要求（美国 FDA 2026 网络安全强制：SBOM 软件物料清单/漏洞管理/渗透测试，缺失即不予受理 RTA；欧盟 MDR Annex I 17.2 + NIS2 + Cyber Resilience Act 2027；中国 NMPA 网络安全注册审查指导原则）、SBOM 构建实操（字段/更新/供应链）、漏洞管理与协调披露（CVSS 分级/修复时限）、网络安全体系与文档（ISO/IEC 81001-5-1、与 ISO 13485/62304 联动、上市后监控），含三地要求对照与申报文档清单，附零依赖本地工具一键查询区域要求、生成检查清单与 SBOM 字段模板。面向医械法规、研发与信息安全负责人，与 AI 医疗器械合规互补。"
---

# 医疗器械网络安全

医疗器械网络安全合规工作台：**对得上三地要求、建得出 SBOM、管得住漏洞、写得出申报文档**。FDA 2026 起联网器械缺 SBOM/渗透测试 = 不予受理（RTA），欧盟 CRA 2027 将至——医械网络安全已是注册硬门槛。

## 什么时候用这个技能

- **监管要求**：「FDA/欧盟/NMPA 对联网器械的网络安全要求是什么？」
- **SBOM 实操**：「SBOM 怎么建？包含哪些字段？」
- **漏洞管理**：「漏洞怎么分级？修复时限？协调披露？」
- **体系文档**：「网络安全申报文档有哪些？ISO 81001-5-1 是什么？」
- **上市后**：「上市后网络安全监控怎么做？漏洞怎么响应？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

> 「我们的联网诊断设备要过 FDA，网络安全要准备什么？」
> 「SBOM 怎么做？用什么格式？」
> 「发现漏洞了，协调披露流程是什么？」

### 模式二：本地工具（要结构化结果）

```bash
# ① 区域要求速查
python tools/meddev_cyber_toolkit.py reg --region us        # us=美国 / eu=欧盟 / cn=中国

# ② 网络安全检查清单（按阶段）
python tools/meddev_cyber_toolkit.py checklist --phase design   # design/development/submission/postmarket

# ③ SBOM 字段模板（JSON）
python tools/meddev_cyber_toolkit.py sbom

# ④ 漏洞分级（CVSS 风格）
python tools/meddev_cyber_toolkit.py vuln --desc "远程可被利用执行任意代码"

# ⑤ 标准速查
python tools/meddev_cyber_toolkit.py standard

# 查看全部命令
python tools/meddev_cyber_toolkit.py --help
```

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 全景与监管 | `references/01-网络安全全景与监管.md` | 为什么强制、三地监管框架、风险 |
| ② 美国 FDA 要求 | `references/02-美国FDA网络安全要求.md` | SBOM/漏洞管理/渗透/RTA、2026 强制 |
| ③ 欧盟要求 | `references/03-欧盟网络安全要求.md` | MDR 17.2、NIS2、CRA 2027、RED |
| ④ 中国 NMPA 要求 | `references/04-中国NMPA网络安全要求.md` | 注册审查指导原则、标准 |
| ⑤ SBOM 实操 | `references/05-SBOM实操.md` | 字段、格式、更新、供应链 |
| ⑥ 漏洞管理 | `references/06-漏洞管理与协调披露.md` | CVSS 分级、修复时限、披露流程 |
| ⑦ 体系与文档 | `references/07-网络安全体系与文档.md` | ISO 81001-5-1、与 13485/62304 联动、申报文档 |
| ⑧ FAQ | `references/08-FAQ.md` | 高频疑问 |

## 快速上手（三步）

1. **看要求**：`reg` 命令查目标市场监管要求，对照 02/03/04 模块；
2. **建 SBOM**：`sbom` 命令取字段模板，按 05 模块实操；
3. **管漏洞**：`vuln` 分级 + 06 模块协调披露流程，07 模块备文档。

## 能力边界（如实说明）

- **本技能是方法库与工具，不是监管意见**：要求基于公开法规整理（核对基准日见各模块头部），申报以监管机构最新指南与专业咨询为准；
- **标准版本持续更新**（ISO 81001-5-1、IEC 62304、SP 800-53 等），引用前复核最新版；
- **工具不联网**：本地规则匹配，不发起扫描、不采集数据。

## 常见问题（FAQ）

- **Q：所有医疗器械都要做网络安全吗？** 联网器械（Cyber Device）强制；非联网器械视数据处理情况评估（见 01 模块）。
- **Q：SBOM 是什么？不做行吗？** 软件物料清单——FDA 2026 起联网器械缺 SBOM 直接不予受理（RTA）。
- **Q：和 ISO 27001 什么关系？** 27001 管组织信息安全；医械网络安全另有 ISO/IEC 81001-5-1（产品网络安全工程）+ 注册申报要求。
- **Q：工具会真的扫描吗？** 不会——只出要求/清单/模板，不发起扫描。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的医械网络安全方法论、要求整理、流程与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与监管准确性保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「注册资料里的网络安全部分怎么写」 / "How do we write the cybersecurity section of the submission?"
- 「设备联网了要不要做渗透测试」 / "Do we need penetration testing now that the device is connected?"
- 「软件成分清单要列到哪一层」 / "How deep should the software bill of materials go?"
- 「客户报了个漏洞我们多久得修」 / "How quickly must we patch a vulnerability a customer reported?"
- 「医院老设备没有安全更新怎么办」 / "What do we do about old devices that can no longer be updated?"
- 「医院采购要网络安全声明怎么给」 / "A hospital is asking for a security statement — what do we send?"

Trigger when the user says any of the above, in Chinese or English.

---

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-cybersecurity
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-cybersecurity/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
