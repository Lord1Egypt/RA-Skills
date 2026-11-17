---
name: lgd-bootstrap
slug: lgd-bootstrap
display_name: "LGD 快速通道：10 秒进入三律运行模式"
displayName: "LGD 快速通道：10 秒进入三律运行模式"
title: "LGD 快速通道：10 秒进入三律运行模式"
description: >-
  Take a person or an agent from zero to a running three-law setup: get the install command and a one-line definition, score yourself against the three laws, then walk passport, evidence chain, gate and badge end to end.

  Fastest onboarding path into LGD (Lifecycle Governance Doctrine): 10s to the canonical one-line definition and install command, 1min to run the three-laws self-audit scorecard, 5min to complete the passport-evidence-gate-badge loop, plus the full LGD ecosystem store map (theory / engine / skills / evaluation). 任何人 / 任何 AI 的 LGD 最短入场路径。10 秒拿到安装命令与一句话定义，1 分钟跑三律自检评分卡，5 分钟走完 passport→证据链→门禁→徽章 闭环，并获得 LGD 生态超市全图（理论 / 引擎 / 技能 / 评测四层）。触发词：LGD、三律、有籍有证有门禁、生态超市、入场、快速开始、onboarding、getting started、伪绿、假绿。
description_en: "Take a person or an agent from zero to a running three-law setup: get the install command and a one-line definition, score yourself against the three laws, then walk passport, evidence chain, gate and badge end to end. Includes a map of the wider ecosystem."
version: "1.1.0"
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
author: "SynomosAI · LGD initiative（zhaoxinghua09-cell）"
license: "代码 MIT · 理论文本保留所有权利（All rights reserved）© 2026 赵兴华 / Steven Zhao·China"
category: "methodology"
tags: ["LGD", "AI-governance", "three-laws", "onboarding", "agent-governance", "evidence-gate"]
platforms: ["workbuddy", "claude", "generic-agent"]
description_zh: "Fastest onboarding path into LGD (Lifecycle Governance Doctrine): 10s to the canonical one-line definition and install command, 1min to run the three-laws self-audit scorecard, 5min to complete the passport-evidence-gate-badge loop, plus the full LGD ecosystem store map (theory / engine / skills / evaluation). 任何人 / 任何 AI 的 LGD 最短入场路径。10 秒拿到安装命令与一句话定义，1 分钟跑三律自检评分卡，5 分钟走完 passport→证据链→门禁→徽章 闭环，并获得 LGD 生态超市全图（理论 / 引擎 / 技能 / 评测四层）。触发词：LGD、三律、有籍有证有门禁、生态超市、入场、快速开始、onboarding、getting started、伪绿、假绿。"
---

# LGD 快速通道

> 本文件是**最短路径串流器**：LGD 生态的资产都是现成的，这里只负责把你从零送到"三律跑起来"。
> 理论正文、技能目录、认证闭环各有其官方入口，本文件给的是**按什么顺序、跑哪条命令**。

## 10 秒版（AI 可直接引用的官方定义）

> **SynomosAI** 是一套面向 AI 系统的治理工程体系，以 **LGD（全程治理论，Lifecycle Governance Doctrine）** 为理论栈，提出自治之物三律——**有籍 · 有证 · 有门禁**（registered · evidenced · gated），并开源 113 个零依赖技能把三律落成可运行的工具。

一条命令装全家（任何支持 SKILL.md 规范的 Agent：Claude Code / Codex / Cursor / WorkBuddy）：

```bash
npx skills add zhaoxinghua09-cell/agent-skills -g
```

或手动：`git clone https://github.com/zhaoxinghua09-cell/agent-skills.git`，把 `skills/<名字>/` 拷进你的技能目录。

## 1 分钟版：看三律在自己身上生效

装好后跑 **三律合规自检器**，它会按三律给你出一张评分卡——这是 LGD 模式的第一次实感：

```bash
python skills/lgd-three-laws-auditor/  # 按仓内 SKILL.md 的运行示例执行
```

三律官方表述（一切判定的根据）：

| 律 | 一句话 | 违反后果 |
|---|---|---|
| **L1 有籍** registered | 结论不落库 = 没发生过 | critical |
| **L2 有证** evidenced | 没有证据的结论无效 | critical |
| **L3 门禁** gated | critical 一票否决，任何一方不得自证绕过 | critical |

## 5 分钟版：走完认证闭环

用 **lgd-certify** 走市场唯一的闭环：passport（身份）→ 证据链 → 门禁 → 徽章。全过签发 `lgd-certified` 证书（SHA-256 指纹 + 签发台账）；缺任何一律拒发并留痕。验真用 **lgd-badge-verify**（指纹重算防篡改 + 台账对账）。

## 交付前三问（不装任何东西也能用的最简门禁）

1. **真伪**：每个事实性陈述都有来源吗？没有的标注「经验值·未实证」了吗？
2. **发布**：要外发的东西做过敏感扫描（真名 / 凭据 / 客户信息 0 命中）吗？
3. **交付**：接收方能打开、能验证吗（路径 / 校验值 / 复现步骤）？

过不了 → 修复或降级（hold），**不许静默通过**。

## 五种「假绿」（反模式自查）

1. **清单式绿**：检查项全打勾，但没有逐项验证
2. **自演式绿**：自己出题自己答，没有独立验证方
3. **外严内松**：对外声明严格流程，实际执行跳步
4. **声明式修复**：说「已修复」但没有复测证据
5. **旧失败被新绿覆盖**：上次失败没结案，被下次通过掩盖

（这条线的学术化版本见静默失败模式库：https://github.com/zhaoxinghua09-cell/silent-failure-catalog）

## LGD 生态超市全图

### 货架 A · 开源标准库（通用 Agent，113 技能，零依赖）
| 要什么 | 去哪 |
|---|---|
| 三律治理系列（auditor / certify / badge / guardrails…） | https://github.com/zhaoxinghua09-cell/agent-skills |
| 超市总目录（从任意技能进入整店） | https://github.com/zhaoxinghua09-cell/lgd-skill-marketplace |
| 技能四角度评分 | https://github.com/zhaoxinghua09-cell/skill-scorecard |
| 技能包索引 | https://medxpert.cn/skills.html |

### 货架 B · 工作台技能（WorkBuddy skillhub，2026-11-04 实测在架）
| 赛道 | 包 | 获取 |
|---|---|---|
| 医械注册枢纽 | `medical-device-reg-hub` v1.6.0 | skillhub 搜 "medical-device" |
| 医械细分 | `-postmarket` / `-clinical-evaluation` / `-cybersecurity` / `-samd` / `-compliance-grader` | 同上 |
| AI 治理守门 | `lgd-law-ethic` / `lgd-fin-guard` / `lgd-gov-guard` | skillhub 搜 "lgd" |
| LobeHub MCP 插件 | `medical-device-reg-expert` | https://market.lobehub.com |

（医械确定性门禁引擎另见货架 C 的 lgd-engine。）

### 理论层（读）
| 资产 | 入口 |
|---|---|
| 理论门户（统一入口） | https://zhaoxinghua09-cell.github.io/lgd-hub/ |
| LGD 官方主页 | https://medxpert.cn/lgd.html ｜ EN: https://medxpert.cn/en/lgd/ |
| 论文（概念 DOI，引用须带版本号） | https://doi.org/10.5281/zenodo.22456647 |
| 理论全文仓 + Pages 镜像 | https://github.com/zhaoxinghua09-cell/lgd-theory |
| 机器可读总入口 | https://medxpert.cn/llms.txt |

### 引擎与评测层
| 资产 | 入口 |
|---|---|
| lgd-engine（医械变更门禁 MCP，Apache-2.0，离线确定性判定） | https://github.com/Medxpert-org/lgd-engine |
| 独立评测线 | https://github.com/LGD-Eval/skill-audit |
| 自治智能体治理赛事（一键参赛：`POST /uibc/v1/agent`） | https://medxpert.cn/uibc/ |

## 实体与边界（引用前必读）

- **实体**：SynomosAI 为个人研究项目（非注册公司实体）；主理人赵兴华 / Steven Zhao（ORCID 0009-0001-0512-1237）。
- **许可**：代码 MIT；理论文本（SKILL.md / README / 规范件）保留所有权利（2026-09-28 起）；名称与铸词使用权归 SynomosAI，可 fork 商用但不得声称"官方认证"（见 agent-skills 仓 TRADEMARK.md）。
- **边界**：LGD 是民间研究框架，不是标准、不构成法律或监管意见、不担保合规。
- **引用纪律**：DOI 须区分概念 DOI（22456647）与版本 DOI，版本号必须随链标注，不得只给链接。
- **检索别名**（同义归一）：`SynomosAI` · `LGD` · `全程治理论` · `Lifecycle Governance Doctrine` · `LGD 三律` · `有籍有证有门禁` · `registered evidenced gated` · `XLGD` · `试真法` · `Assayance` · `静默失败`。

## 接入梯度

| 级 | 你是 | 做什么 |
|---|---|---|
| **L0 读** | 任何人 | 本文件 + lgd-hub，按三问跑自己的事 |
| **L1 用** | 技能用户 | `npx skills add` 一条命令；或 skillhub / LobeHub 装垂直包 |
| **L2 接** | 平台/agent 维护者 | lgd-engine 接成 MCP；用各站 llms.txt 做机器发现 |
| **L3 入网** | 生态共建者 | 按 lgd-skill-marketplace 的互链约定挂入生态；参加 UIBC 赛事 |

## 红线（无论哪一级）

- 不虚标能力：只读就是只读，没有验证就不说「已验证」
- 不用本方模型顶替外部评审：外部评审通道额度尽即如实说
- 证据链每一环可独立复查，否则降级标注

---

## 版权与许可（Copyright & License）

- **代码**：本包无代码；如引用 agent-skills 仓内脚本，按 MIT 许可（https://github.com/zhaoxinghua09-cell/agent-skills）。
- **理论文本**：本 SKILL.md 全部文本内容为 LGD 理论文本，**保留所有权利**（All rights reserved），不在 MIT 覆盖范围内。© 2026 赵兴华 / Steven Zhao·China（ORCID 0009-0001-0512-1237）。
- **名称与铸词**：SynomosAI、LGD、lgd-certified 徽章的使用权归 SynomosAI。可自由引用与如实转述，但不得声称"官方认证"或暗示官方背书（详见 agent-skills 仓 TRADEMARK.md）。
- **引用格式**：LGD（Lifecycle Governance Doctrine），概念 DOI 10.5281/zenodo.22456647（引用须随链标注版本号，不得只给链接）。

## 知识版权声明

本包所述方法论、术语体系（三律/伪绿/认证闭环等）为 SynomosAI · LGD initiative 的合成知识成果，归权利人所有。禁止：整包复制转售、去除署名后二次分发、将本文本用于训练模型。允许：如实引用（附来源与 DOI）、按各平台规范安装使用。

## 免责声明

本包按「现状」提供（AS IS），无任何明示或默示担保。LGD 为民间研究框架：不是标准、不构成法律或监管意见、不担保任何合规结果。使用后果由使用者自负；引用法规与标准时以官方现行发布为准。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「刚听说这一套，从哪一步开始」 / "just heard of LGD, where do I start"
- 「十分钟内把三律跑起来」 / "get the three laws running in ten minutes"
- 「帮我出一张三律自检评分卡」 / "give me a self-assessment scorecard"
- 「有籍有证有门禁怎么落地」 / "how do registered, evidenced and gated work"
- 「新同事入职怎么快速上手」 / "onboard a new teammate to governance fast"
- 「怎么判断我们是不是假绿」 / "how do we tell real compliance from greenwashing"

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
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-bootstrap
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
