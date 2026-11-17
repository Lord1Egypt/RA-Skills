---
name: medical-device-postmarket
slug: medical-device-postmarket
display_name: 医械上市后监管
displayName: 医械上市后监管
title: 医械上市后监管
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
  A practical playbook for post-market surveillance of medical devices, comparing reporting duties across the US, EU, China and Japan and turning them into checklists. It covers adverse event reporting, PSUR frequency, field safety corrective actions, recalls and PMCF follow-up. Use when you need to know what to report, to whom, and by when after a device is already on the market.

  医疗器械上市后监管（Post-Market Surveillance, PMS）实操手册——中美欧日四市场上市后义务对照（不良事件报告、PSUR 定期安全报告、FSCA/召回现场安全纠正、PMCF 上市后临床跟踪）、各市场报告时限与流程清单（美国 21 CFR 803 致死 30 天/严重 90 天、欧盟 MDCG 2022-21 PSUR 频率、中国 2018 年 1 号令报告时限、日本 PMDA）、PMS 计划与 PSUR 撰写框架、监测-报告-纠正闭环落地，附零依赖本地工具一键查询义务对照、报告时限与生成 PMS/PSUR 框架。面向医械法规、质量与临床负责人，拿证后的持续合规一站理清。
description_en: A hands-on playbook for medical device post-market surveillance (PMS) — four-market obligation comparison (US/EU/CN/JP) covering adverse event reporting, PSUR, FSCA/recall field safety corrective actions and PMCF post-market clinical follow-up, with report timelines and process checklists per market (US 21 CFR 803 30-day death/90-day serious injury, EU MDCG 2022-21 PSUR frequency, China 2018 Order No.1 timelines, Japan PMDA), PMS plan and PSUR writing frameworks, and the monitor-report-correct closed loop. Includes a zero-dependency local toolkit for obligation comparison, timeline queries and PMS/PSUR framework generation. Built for regulatory, quality and clinical leaders — one-stop continuous compliance after certification.
tags:
  - 医疗器械
  - 上市后监管
  - PMS
  - 不良事件
  - PSUR
  - FSCA
  - 召回
  - PMCF
  - MDR
  - Post-market
  - 21 CFR 803
  - MDCG 2022-21
---

# 医械上市后监管

医疗器械上市后监管（PMS）工作台：**对得上四市场义务、报得了不良事件、写得出 PSUR、纠得了 FSCA/召回、闭环不踩雷**。拿证之后，「监测—报告—纠正」闭环做不好，注册证都可能被收回。

## 什么时候用这个技能

- **义务对照**：「产品在中美欧日上市，各有哪些 PMS 义务？」
- **不良事件**：「美国收到严重伤害事件，多久报告？中国呢？」
- **定期文件**：「IIb 器械 PSUR 怎么写？多久更新一次？」
- **纠正措施**：「什么时候触发 FSCA/召回？流程是什么？」
- **PMCF**：「上市后临床跟踪计划怎么写？」
- **闭环落地**：「PMS 计划怎么建？监测-报告-纠正怎么转起来？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

> 「我们在美国收到一起严重伤害不良事件，要报告吗？多久？」
> 「出口欧盟的 IIb 器械 PSUR 怎么写？」
> 「中国的不良事件报告时限是多少？」

### 模式二：本地工具（要结构化结果）

```bash
# ① 义务对照（按市场）
python tools/pms_toolkit.py obligations --region us      # us=美国 / eu=欧盟 / cn=中国 / jp=日本

# ② 不良事件报告时限速查
python tools/pms_toolkit.py report --region us

# ③ PMS 计划框架（生成 Markdown 骨架）
python tools/pms_toolkit.py plan

# ④ PSUR 撰写框架（按风险等级）
python tools/pms_toolkit.py psur --class IIb

# ⑤ FSCA/召回流程
python tools/pms_toolkit.py recall

# 查看全部命令
python tools/pms_toolkit.py --help
```

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 四市场义务对照 | `references/上市后监管知识库.md` 第一章 | 中美欧日 PMS 义务总览 |
| ② 美国报告（21 CFR 803） | `references/上市后监管知识库.md` 第二章 | eMDR/MAUDE、30/90 天时限 |
| ③ 欧盟警戒/FSCA/PSUR | `references/上市后监管知识库.md` 第三章 | MDCG 指南、PSUR 频率 |
| ④ PMCF 计划与报告 | `references/上市后监管知识库.md` 第四章 | MDCG 2020-7/8 框架 |
| ⑤ 中国监测与再评价 | `references/上市后监管知识库.md` 第五章 | 2018 年 1 号令、报告时限 |
| ⑥ 日本 PMDA 报告 | `references/上市后监管知识库.md` 第六章 | 日本报告义务 |
| ⑦ PMS 计划/PSUR 框架 | `references/上市后监管知识库.md` 第七章 | 撰写结构 |

## 快速上手（三步）

1. **对义务**：`obligations` 命令查产品所在市场义务，对照知识库第一章；
2. **建闭环**：`report` 查报告时限，建不良事件接收→评估→报告流程；
3. **写文件**：`plan`/`psur` 生成框架，按知识库第七章程式组织。

## 能力边界（如实说明）

- **本技能提供框架与要点，不替代各国监管机构个案裁定**：具体事件报告时限与格式，以产品所在市场最新法规和监管机构最新通知为准；
- **法规持续更新**（FDA 指南改版频繁、EU 协调标准滚动更新），引用前复核官方原文；
- **工具不联网**：本地规则匹配，不采集数据、不调用外部服务。

## 常见问题（FAQ）

- **Q：所有上市产品都要做 PMS 吗？** 是——PMS 是拿证后的持续义务，四市场都有要求（中国/欧盟明确强制，美国通过不良事件报告体现）。
- **Q：PSUR 多久写一次？** 欧盟按风险等级：IIb 至少每 2 年、III 类至少每年（MDCG 2022-21），可并入技术文档更新。
- **Q：FSCA 和召回什么区别？** FSCA 是现场安全纠正措施（含召回）——欧盟触发 FSCA 须报告主管当局；召回是纠正方式之一（见知识库第三章）。
- **Q：工具脚本要装依赖吗？** 不需要，仅 Python 标准库。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的上市后监管方法论、义务整理、流程框架与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与监管准确性保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「拿到证以后还要定期交什么报告」 / "What reports do we still owe after approval?"
- 「客户投诉算不算不良事件要上报」 / "Does this customer complaint count as a reportable adverse event?"
- 「欧盟那个定期安全报告多久交一次」 / "How often does the EU periodic safety report have to go in?"
- 「海外客户反馈骨折了要不要召回」 / "A patient abroad reported a fracture — do we recall?"
- 「经销商报上来的问题几天内得上报」 / "How fast must we report an issue a distributor raised?"
- 「上市后临床跟踪还要不要接着做」 / "Do we still need to keep the post-market clinical follow-up running?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-postmarket
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-postmarket/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
