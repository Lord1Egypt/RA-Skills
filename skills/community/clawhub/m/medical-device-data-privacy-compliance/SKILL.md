---
name: medical-device-data-privacy-compliance
display_name: 医械跨境数据隐私合规
description: >-
  Data-compliance companion for medical devices sold across borders: it maps how patient and device data flows through apps, cloud backends and service partners, then checks each flow against GDPR, HIPAA, China's PIPL and cross-border transfer rules. Outputs a data-flow inventory, privacy impact assessment (PIA/DPIA) notes and a list of compliance actions before launch. Use when a connected device or companion app will collect, store or transfer data outside its home market.

  医疗器械出海数据合规：GDPR / HIPAA / 中国个保法（PIPL）、数据出境安全评估、隐私影响评估（PIA/DPIA）。输出数据流映射清单与合规要点，降低联网器械出海的数据合规风险。
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
author: 注册老炮
category: 文档处理
tags: ["医疗器械","数据跨境","隐私合规","GDPR","HIPAA","个保法","PIPL","数据出境","出海合规","注册老炮"]
license: MIT
platforms: ["workbuddy"]
---

# 医械跨境数据 / 隐私合规

## 这是什么
面向**出海联网医疗器械**的数据合规工具技能：把 GDPR（欧盟）、HIPAA（美国）、中国《个人信息保护法》（PIPL）以及数据出境安全评估串成一张可执行的检查清单与数据流映射。

与 `medical-device-iomt-compliance` 的关系：本技能专注「数据合规」这一专项；IoMT 技能在涉及跨境数据流时会指向本技能。

## 触发场景
- "带 APP 的器械出欧盟，数据合规怎么过"
- "中国患者数据能不能传到境外服务器"
- "GDPR / HIPAA / 个保法都要满足哪些点"
- "数据出境安全评估怎么启动"
- "联网器械隐私影响评估（DPIA）模板"

## 使用流程
1. **梳理数据流**：画出「患者/用户 → 器械/APP → 网关/云 → 境外接收方」全链路，标注数据类型、处理目的、保留期限。
2. **识别法律触发**：目标市场卖到哪里，就触发哪套法律——欧盟 GDPR、美国 HIPAA / State Law、中国 PIPL。
3. **评估出境场景**：患者个人信息、健康数据、设备日志是否出境；是否需要中国网信部门数据出境安全评估 / 标准合同 / 认证。
4. **补齐组织措施**：隐私政策、用户协议、数据主体权利响应机制、DPO / 法定代表人指定、安全事件响应。
5. **落地技术措施**：加密传输（TLS 1.2+）、数据最小化、访问控制、日志审计、匿名化/去标识化。
6. **输出文档包**：数据流映射表、DPIA / PIA、跨境合规备忘录、隐私政策草稿要点。
7. **自测闭环**：用 `medical-device-compliance-grader` 的 C5 质量体系 + C2 标签IFU 维度交叉检查文档完整性。

## 要点速查
- 数据本地化 ≠ 不能出境，而是要经过评估 + 有合法基础（同意、合同履行、法定职责等）。
- GDPR 对「健康数据」是特殊类别个人数据，默认禁止处理，须有法律依据。
- HIPAA 只监管美国 Covered Entity / Business Associate 处理的健康信息（PHI）；消费级 APP 不一定适用，但FDA/NIST安全要求仍在。
- 中国 PIPL 下，处理敏感个人信息须单独同意；出境重要数据 / 达量个人信息须走安全评估。
- 隐私政策不是免责条款，而是数据处理的「说明书」，写不清会直接影响市场准入。

## 关联技能
- 联网器械整体合规：`medical-device-iomt-compliance`
- 出海市场准入：`medical-device-intl-business`
- 查规则/官方链接：`medical-device-reg-hub`
- 评测自检：`medical-device-compliance-grader`

## references 导航表
| 文件 | 内容 |
|---|---|
| `references/01-GDPR与医疗器械.md` | GDPR 特殊类别数据、DPIA、跨境传输 |
| `references/02-HIPAA与医疗器械.md` | PHI、安全规则、BAA、与 GDPR 差异 |
| `references/03-个保法与数据出境评估.md` | PIPL 三条出境路径、安全评估材料 |
| `references/04-出海器械数据流映射模板.md` | 数据流表、8 个问题、输出物清单 |

## 注意事项
- 本技能为公开法规信息整理的**编写辅助**，不构成法律意见；具体出境评估请咨询专业律师或合规顾问。
- 法规会更新，关键数据以监管机构最新发布为准。
- 输入/输出去敏：不出现患者真名、客户名称、内部系统路径、报价等。

## 版权与许可
© 2026 注册老炮（MedXpert）。本技能著作权归注册老炮所有。本作品以 MIT 许可证发布（详见 LICENSE.md）。

免责声明：本技能按"现状"（AS IS）提供，不提供任何明示或暗示担保；使用本技能产生的任何后果由使用者自行承担，作者及 MedXpert 不承担责任。本技能不构成专业法规或法律意见，请以监管机构最新发布为准。

知识版权：本技能所含合成知识、方法论、模板归注册老炮 / MedXpert 所有，禁止复制、转售或用于训练模型。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「客户健康数据能不能传到海外服务器」 / "Can patient health data be stored on overseas servers"
- 「联网设备采集的数据要出境，怎么报」 / "Connected device data leaves the country, how do we file"
- 「欧洲客户问我们符不符合GDPR」 / "A European customer asks if we comply with GDPR"
- 「美国医院要我们签BAA，怎么弄」 / "A US hospital wants a BAA signed"
- 「用户数据给第三方云厂商，风险在哪」 / "We hand user data to a third-party cloud vendor"
- 「App收集哪些字段才算必要」 / "Which fields does the app really need to collect"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-data-privacy-compliance
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-data-privacy-compliance/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
