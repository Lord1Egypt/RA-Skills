---
name: medical-data-export-compliance
slug: medical-data-export-compliance
display_name: 医械数据出海合规
displayName: 医械数据出海合规
title: 医械数据出海合规
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
  A practical guide to moving medical device data across borders, covering China's three lawful export pathways, the volume thresholds that decide which one applies, and the extra rules for health data. It also maps the main destination markets — GDPR, HIPAA, PDPA, Japan and Korea — and walks through clinical trial, telehealth, cloud and employee data scenarios. Use when you need to judge whether an export is allowed and what to file.

  医疗器械企业数据出境与出海合规实操手册——覆盖中国数据出境"3+2+4"监管体系与三条合规路径（数据出境安全评估、个人信息出境标准合同、2026-01-01 施行的个人信息出境认证）、10万/100万人数阈值与累计计算规则、医疗健康数据特殊要求（首部医疗数据强制性国标、医疗数据安全审查、大湾区标准合同）、主要目标市场数据法（欧盟 GDPR/EHDS、美国 HIPAA、新加坡 PDPA、日韩），含出海场景实操（临床试验数据/远程诊疗/云服务/员工数据）、合规落地五步流程与年度审计要求（2026-08-20 施行风险评估办法），附零依赖本地工具一键判定出境路径、计算人数阈值、输出场景清单。面向医疗器械企业国际业务、合规与数据负责人。
description_en: A practical playbook for data export and cross-border compliance for medical device companies going global — covering China's '3+2+4' data-export regulatory system and three compliance pathways (data-export security assessment, personal information standard contract, and the personal information export certification effective 2026-01-01), the 100k/1M volume thresholds with cumulative counting rules, special requirements for medical and health data (first mandatory national standard, medical data security review, GBA standard contracts), and key destination-market data laws (EU GDPR/EHDS, US HIPAA, Singapore PDPA, Japan/Korea), with export scenario playbooks (clinical trial data, telehealth, cloud services, employee data), a 5-step compliance process and annual assessment requirements (Risk Assessment Measures effective 2026-08-20). Includes a zero-dependency local toolkit for pathway determination, volume-threshold calculation and scenario checklists. Built for international business, compliance and data leaders in medical device companies.
tags:
  - 数据出境
  - 医疗器械
  - 出海合规
  - 个人信息保护
  - 安全评估
  - GDPR
  - HIPAA
  - 医疗数据
  - 跨境传输
  - Data Export
  - 数据合规
---

# 医械数据出海合规

医疗器械企业数据出境合规工作台：**判得准走哪条路、算得清人数阈值、认得出特殊要求、落得了出海场景**。中国数据出境"三条路径+豁免"制度框架 2026 年基本定型（认证办法 2026-01-01 施行、风险评估办法 2026-08-20 施行、首批安全评估 2026 集中到期）——医械出海的数据合规再也不能拖。

## 什么时候用这个技能

- **路径判定**：「我们的数据出境要走安全评估、标准合同还是认证？」
- **阈值计算**：「出境多少个人信息要申报？累计怎么算？」
- **医疗数据**：「医疗健康数据有什么特殊要求？」
- **目标市场**：「去欧盟/美国/东南亚，数据要求是什么？」
- **出海场景**：「临床试验数据、远程诊疗、云服务、员工数据怎么合规？」
- **运营审计**：「评估结果快到期了怎么办？年度审计要求？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

> 「我们临床试验数据要传给海外 CRO，走什么路径？」
> 「公司把患者数据存到境外云服务器，合规吗？」
> 「去欧盟卖设备，健康数据要满足什么要求？」

### 模式二：本地工具（要结构化结果）

```bash
# ① 出境路径判定：输入数据出境情况描述
python tools/data_export_toolkit.py path --desc "向海外CRO传输临床试验受试者个人信息，全年约50万人"

# ② 人数阈值计算：输入全年出境数量（个人信息/敏感）
python tools/data_export_toolkit.py threshold --personal 500000 --sensitive 2000

# ③ 出海场景合规清单（按场景）
python tools/data_export_toolkit.py scene --type clinical    # clinical/trial 等

# ④ 目标市场数据要求速查
python tools/data_export_toolkit.py market --region eu       # eu/us/sg/jp/kr

# ⑤ 合规落地审计清单
python tools/data_export_toolkit.py audit

# 查看全部命令
python tools/data_export_toolkit.py --help
```

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 监管体系全景 | `references/01-数据出境监管体系.md` | "3+2+4" 体系、什么是数据出境、管辖对象 |
| ② 三条合规路径 | `references/02-三条合规路径.md` | 安全评估/标准合同/出境认证、数量阈值、豁免 |
| ③ 医疗数据特殊要求 | `references/03-医疗数据特殊要求.md` | 医疗数据国标、安全审查、大湾区通道 |
| ④ 目标市场数据法 | `references/04-目标市场数据法.md` | 欧盟 GDPR/EHDS、美国 HIPAA、新加坡/日韩 |
| ⑤ 出海场景实操 | `references/05-出海场景实操.md` | 临床数据/远程诊疗/云服务/员工数据 |
| ⑥ 落地流程与审计 | `references/06-落地流程与审计.md` | 五步落地、评估到期处理、年度审计 |
| ⑦ FAQ 与术语 | `references/07-FAQ与术语.md` | 高频疑问 + 术语表 |

## 快速上手（三步）

1. **判路径**：用 `path` 命令输入出境情况，对照 02 模块三条路径；
2. **算阈值**：`threshold` 命令确认是否需要申报；
3. **落场景**：`scene` 命令按出海场景取清单，`market` 查目标市场要求。

## 能力边界（如实说明）

- **本技能是方法库与工具，不是法律意见**：监管要求基于公开法规整理（核对基准日见各模块头部），正式申报请以监管部门最新指南与专业顾问为准；
- **数量口径复杂**：阈值按"当年 1 月 1 日累计"计算，实际申报前需精确盘点；
- **工具不联网**：本地规则匹配，不采集数据、不调用外部服务。

## 常见问题（FAQ）

- **Q：所有数据出境都要申报吗？** 否——数据出境管理对象限于**重要数据和个人信息**；且按数量阈值分路径，低阈值可走标准合同/认证，还有豁免情形（见 02 模块）。
- **Q：医疗健康数据是敏感个人信息吗？** 是——敏感个人信息（含健康医疗）出境门槛更低（1 万条即触发安全评估），要求更严。
- **Q：数据存到境外云服务器算出境吗？** 算——境内运营收集产生的数据向境外提供即构成数据出境，无论存储还是处理。
- **Q：工具脚本要装依赖吗？** 不需要，仅 Python 标准库。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的医械数据出海合规方法论、路径整理、法规梳理与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与监管准确性保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「临床试验数据传到国外服务器行不行」 / "Can we push clinical trial data to an overseas server?"
- 「多少人的个人信息要去做安全评估」 / "How many people's data triggers a security assessment?"
- 「海外子公司员工数据算不算出境」 / "Do our overseas subsidiary's employee records count as an export?"
- 「用境外云服务存病历要不要申报」 / "Do we need to file if patient records sit on a foreign cloud?"
- 「标准合同和认证该选哪条路」 / "Should we use the standard contract or the certification?"
- 「远程诊疗的海外患者数据怎么处理」 / "How do we handle overseas patient data from telehealth?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-data-export-compliance
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-data-export-compliance/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
