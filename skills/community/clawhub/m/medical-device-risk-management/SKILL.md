---
name: medical-device-risk-management
displayName: 医械风险管理专家
description: >-
  Medical device risk management skill — ISO 14971:2019 / GB/T 42062-2022 6-step process, hazard identification checklists, risk matrix & acceptability criteria, risk management report framework, global standard mapping with official references.

  医疗器械风险管理专题——ISO 14971/GB/T 42062 六步流程实操、危害识别清单、风险矩阵与可接受准则、风险管理报告框架，全球标准对照与官方入口直达。
description_zh: 医疗器械风险管理专题——ISO 14971/GB/T 42062 六步流程实操、危害识别清单、风险矩阵与可接受准则、风险管理报告框架，全球标准对照与官方入口直达。
description_en: Medical device risk management skill — ISO 14971:2019 / GB/T 42062-2022 6-step process, hazard identification checklists, risk matrix & acceptability criteria, risk management report framework, global standard mapping with official references.
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
author: 注册老炮
category: 文档处理
xiaping_category: ["效率工具"]
xiaping_tags: ["医疗器械","风险管理","风险分析","风险评价","风险控制","残余风险","获益风险","ISO 14971","GB/T 42062","YY/T 0316","ISO/TR 24971","EN ISO 14971","JIS T 0304","FMEA","FMECA","危害识别","危险情况","可接受准则","风险矩阵","风险管理报告","风险收益分析","设计控制","21 CFR 820.30","GSPR","协调标准","医疗器械注册","风险管理文件","risk management","hazard","residual risk","risk benefit"]
agent_created: true
slug: medical-device-risk-management
display_name: 医械风险管理专家
title: 医械风险管理专家
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
license: MIT
tags: ["医疗器械","风险管理","风险分析","ISO 14971","GB/T 42062","FMEA","危害识别","风险矩阵","残余风险","风险管理报告","获益风险","风险控制","risk management","hazard","residual risk"]
---

# 医械风险管理专家

## 这是什么

聚焦「风险管理文件」这一**每份注册案卷的必备文件**的实操技能：ISO 14971:2019 六步流程怎么走、危害怎么识别、风险矩阵怎么定、风险管理报告怎么写。无论走中国 NMPA、美国 510(k)/PMA、欧盟 MDR 还是日本 PMDA，审评首先看的都是"风险是否被识别、评价与控制"。本技能给的是**可落地的流程 + 清单 + 模板**。

## 为什么用本技能

- **流程不跳步**：六步流程按证据链顺序组织，风险分析→评价→控制→综合剩余风险→报告→生产后反馈，一步不缺。
- **危害识别有清单**：能量/生物学/化学/操作/信息五大类危害源清单，避免"想不到"导致的审评发补。
- **全球一套文件**：以 ISO 14971 方法论写一套，映射各国标准（GB/T 42062 / EN ISO 14971 / JIS T 0304 / FDA 认可），最大化复用。

## 触发场景（Triggers）

- "风险管理 / 风险分析 / 风险评价 / 风险控制"
- "ISO 14971 / GB/T 42062 / YY/T 0316 / EN ISO 14971 / JIS T 0304"
- "FMEA / FMECA" / "危害识别" / "风险矩阵" / "可接受准则"
- "风险管理报告" / "风险收益分析" / "残余风险"
- "设计控制 / 21 CFR 820.30" / "GSPR 风险条款"
- 注册资料里"风险管理资料"模块怎么写

## 使用流程（Workflow）

1. **确定预期用途**：写明预期用途、适应证、目标人群、使用环境——这是风险分析的前提。
2. **危害识别**：用 `references/风险管理知识库.md` 的危害清单逐类排查，结合产品特性（材料/灭菌/软件/操作）。
3. **风险估计与评价**：对每个危险情况估计风险（严重度 × 发生概率），与可接受准则比较。
4. **风险控制**：按优先级（本质安全设计 → 防护 → 安全信息），验证控制有效性，评估剩余风险。
5. **综合剩余风险评价**：结合获益-风险判断整体可接受性。
6. **写报告 + 闭环**：输出风险管理报告（注册提交），建立生产后数据反馈机制（呼应上市后监管技能）。

### references/ 文件导航

| 用户问题 | 加载文件 |
|---|---|
| 全球标准与法规对照 | `风险管理知识库.md` 第一章 |
| 六步流程与危害清单 | `风险管理知识库.md` 第二章 |
| 风险矩阵与可接受准则 | `风险管理知识库.md` 第三章 |
| 风险管理报告框架 | `风险管理知识库.md` 第四章 |
| 案卷位置与常见误区 | `风险管理知识库.md` 第五章、第六章 |

## 使用示例

**示例 1 · 报告结构**
问："风险管理报告怎么写？"
→ 按证据链：预期用途与误用 → 危害识别清单 → 危险情况与风险估计 → 风险评价（对照可接受准则）→ 风险控制措施及验证 → 残余风险评估 → 综合剩余风险与获益-风险结论 → 生产后活动计划。每项控制措施与设计输出/验证记录互相引用。

**示例 2 · 风险控制优先级**
问："一个危害怎么控制？"
→ 按 ISO 14971 优先级：①本质安全设计（消除/降低危害）→ ②防护措施（如安全装置）→ ③安全信息（警告/IFU 说明）；每项控制须验证有效性，控制后的残余风险再评估是否可接受。

## 边界说明

- 本技能提供框架与要点，不替代审评机构对具体产品的裁定；风险可接受准则需公司按产品定位制定并经管理层批准。
- 标准会更新（GB/T 42062 现行、ISO 14971 以最新版为准），使用前核对标准版本与各国认可状态。

## 版权与许可

- © 2026 **注册老炮**。本技能及 references 知识库为原创整理，以 **MIT 协议**开源发布。
- **知识版权声明**：本技能整理的合成知识、方法论与编排体系归「注册老炮」所有；未经授权不得复制、转载、转售，或用于训练任何模型（含商业与开源模型）。
- **免责声明**：本技能按「现状（AS IS）」提供，不提供任何明示或默示的担保；因使用、误用本技能或其输出导致的任何直接或间接损失，作者不承担责任。
- 引用的法规与标准均以官方原文（NMPA / FDA / EU MDR 等）为准，链接指向官方站点；如与官方最新版本不一致，以官方为准。
- 内容仅供合规工作参考，不构成注册代理服务或法律意见。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「风险管理报告按什么结构写」 / "What structure should the risk management report follow?"
- 「危害清单怎么才能不漏项」 / "How do we build a hazard list that misses nothing?"
- 「剩余风险可接受怎么判定」 / "How do we decide the residual risk is acceptable?"
- 「做完分析还要不要做风险矩阵」 / "Do we still need a risk matrix after the analysis?"
- 「审评说风险控制没闭环怎么补」 / "The reviewer says risk control isn't closed — how do we fix it?"
- 「生产后信息怎么反馈回风险管理」 / "How does post-production information feed back into risk management?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-risk-management
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-risk-management/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
