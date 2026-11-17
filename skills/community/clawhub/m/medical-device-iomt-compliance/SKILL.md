---
name: medical-device-iomt-compliance
display_name: 智能医疗器械IoMT合规
description: >-
  Compliance guide for connected medical devices that combine sensors, a companion app and a cloud service: it lays out the SaMD and SiMD registration paths, cybersecurity expectations, UDI traceability and remote patient monitoring scope across NMPA, FDA and EU MDR. Produces a submission-document checklist and the key points reviewers will look for. Use when a hardware product gains software, connectivity or an AI feature and the regulatory picture suddenly gets complicated.

  带传感器/APP/云的智能医疗器械（IoMT）合规助手：SaMD+SiMD注册路径、网络安全IEC 81001-5-1、UDI追溯、RPM远程监测。3分钟理清联网器械的NMPA/FDA/MDR合规拼图，输出可提交文档清单与要点。
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
author: 注册老炮
category: 文档处理
tags: ["医疗器械","IoMT医疗物联网","智能器械合规","SaMD/SiMD","网络安全","UDI追溯","RPM远程监测","合规生成","注册老炮"]
license: MIT
platforms: ["workbuddy"]
---

# 智能医疗器械 IoMT 合规

## 这是什么
面向「带联网能力的医疗器械」（IoMT / 智能医疗器械）的合规编写助手：把传感器、嵌入式软件、手机 APP、云端服务串起来后，如何按 NMPA / FDA / MDR 走通注册与合规。

与 `medical-device-samd`（软件器械合规）的关系：本技能覆盖「联网硬件 + 软件 + 云」整体；`samd` 聚焦纯软件层。两者配套使用，本技能负责整体拼图，`samd` 负责软件细节。

## 触发场景
- "带蓝牙/传感器的器械怎么注册"
- "智能穿戴 / 远程监测设备合规路径"
- "联网器械的网络安全证据怎么准备"
- "UDI 怎么和追溯系统打通"
- "SaMD 和 SiMD 怎么区分界定"

## 使用流程
1. **界定形态**：明确是 SaMD（独立软件器械）、SiMD（器械内软件）还是「硬件 + 软件 + 云」组合器械；定预定用途与软件安全分级（IEC 62304 A/B/C）。
2. **注册路径**：按目标市场映射——NMPA（注册检验 + 临床评价 + 技术文件）、FDA（510(k)/De Novo + 网络安全指南）、MDR（Annex II 技术文档 + Annex I 23 条）。
3. **网络安全**：按 IEC 81001-5-1 / FDA 预市网络安全指南做威胁建模、漏洞管理、SBoM（软件物料清单）。
4. **可追溯**：UDI-DI/PI 赋码 + 数据库上报（GUDID / EUDAMED / 国家UDI数据库）+ 供应链追溯接口设计。
5. **远程监测（如适用）**：RPM 类器械的受益-风险、数据质量、算法性能监控。
6. **数据合规衔接**：联网器械的数据流若跨境，转 `medical-device-data-privacy-compliance`（GDPR / HIPAA / 个保法）。
7. **自测闭环**：用 `medical-device-compliance-grader` 的 C9（软件/SaMD）+ C2（标签IFU）维度打分。

## 要点速查
- 网络安全证据是预市必交项（美/欧趋严），不得事后补；SBoM 已成标配。
- 「云」若承担医疗功能，常被认定为 SaMD 一部分，须一并纳入体系。
- UDI 不是贴标签，是「数据库 + 追溯」系统工程，早规划省返工。
- 算法/模型变更属重大变更，须走变更注册并复评受益-风险。

## 关联技能
- 软件细节：`medical-device-samd`
- 数据跨境合规：`medical-device-data-privacy-compliance`
- 查规则/官方链接：`medical-device-reg-hub`
- 评测自检：`medical-device-compliance-grader`（C9 软件/SaMD、C2 标签IFU）

## references 导航表
| 文件 | 内容 |
|---|---|
| `references/01-SaMD与SiMD注册路径.md` | SaMD/SiMD 界定、IEC 62304 分级、中美欧注册路径映射 |
| `references/02-医疗器械网络安全IEC81001-5-1.md` | 网络安全证据清单、SBoM、常见雷区 |
| `references/03-UDI追溯与供应链物联网.md` | UDI-DI/PI、GUDID/EUDAMED/国家数据库、一物一码 |
| `references/04-RPM远程监测合规.md` | RPM 产品形态、注册路径提示、数据合规衔接 |

## 注意事项
- 本技能为公开官方信息整理的**编写辅助**，不构成法规意见；重大注册决策请咨询专业 RA 或律师。
- 法规会更新，关键数据以监管机构最新发布为准。
- 输入/输出去敏：不出现客户真名、报价、未公开项目。

## 版权与许可
© 2026 注册老炮（MedXpert）。本技能著作权归注册老炮所有。本作品以 MIT 许可证发布（详见 LICENSE.md）。

免责声明：本技能按"现状"（AS IS）提供，不提供任何明示或暗示担保；使用本技能产生的任何后果由使用者自行承担，作者及 MedXpert 不承担责任。本技能不构成专业法规或法律意见，请以监管机构最新发布为准。

知识版权：本技能所含合成知识、方法论、模板归注册老炮 / MedXpert 所有，禁止复制、转售或用于训练模型。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「设备加了蓝牙和APP，要重新注册吗」 / "We added Bluetooth and an app, do we re-register"
- 「远程监测功能归哪一类器械」 / "Which device class covers remote monitoring"
- 「网络安全测试报告要测哪些项」 / "What should the cybersecurity test report cover"
- 「UDI码怎么编，追溯链怎么打通」 / "How do we assign UDI codes and build traceability"
- 「软件升级后要不要重新申报」 / "Does a software update need a new submission"
- 「带AI算法的影像软件按SaMD报吗」 / "Is AI imaging software filed as SaMD"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-iomt-compliance
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-iomt-compliance/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
