---
name: lgd-evo
description: lgd-evo — LGD 演化中枢（meta 薄分发器）。把 GovernanceOS 的 EVO 阶段 1 个演化节点（agent-evolution）聚合成可检索、可一键探测的入口：部署后让智能体记录发现、演化并精炼自身操作手册。只按 slug 路由到独立子技能，不搬运、不重实现任何子技能代码。 适用场景：当需要AI 智能体自我演化/经验回流/操作手册精炼能力时使用本技能；触发词：lgd-evo、演化、自进化、经验回流。
slug: lgd-evo
version: 1.0.3
homepage: https://zhaoxinghua09-cell.github.io/lgd-skills-index/
display_name: LGD 演化中枢
display_name_en: LGD Evolution Hub
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
copyright: XLGD · SynomosAI
description_zh: "lgd-evo — LGD 演化中枢（meta 薄分发器），把 EVO 阶段 1 个演化节点聚合成可检索可探测入口。"
description_en: "LGD Evolution Hub — a thin meta-dispatcher that aggregates the 1 EVO-phase node into one discoverable, self-verifying entry point."
classification:
  internal: ["主轴2 理论体系(LGD)"]
  skillhub: ["ai-governance"]
  clawhub: ["search", "development"]
  iso_25010: ["Maintainability"]
risk_tier: medium
risk_rationale: "meta 薄分发器默认 medium：仅按 slug 路由并只读探测（--help），不代执行子技能、不对外写；若需经本技能触发实际演化写入，须由被路由的子技能各自走其 own 风险评审。"
tags: [lgd-evo, AI 治理, 演化, 自进化, 经验回流]
ai_protocol: true

lineage: ["LGD-有籍", "LGD-有门禁", "GovernanceOS-EVO"]
---

# LGD 演化中枢（lgd-evo）

> **薄分发器（thin dispatcher）**：本技能不搬运、不重实现任何演化代码。它只是 GovernanceOS
> `SPEC → PLAN → GATE → AUDIT → EVO` 生命周期里 **EVO 阶段**的聚合入口——把 1 个独立发布的
> 演化子技能按 slug 列出、一键探测可用性、给出调用说明。所有真实演化由被路由的子技能完成。

## When to Use

- 你部署了智能体后，希望它**记录发现、自我演化、把经验回流成更精炼的操作手册**。
- 你要把"踩过的坑 / 跑通的路径"沉淀成可复用的 playbook，而不是每次从头来。
- 触发词：`lgd-evo`、`演化`、`自进化`、`经验回流`。

## 核心能力（EVO 阶段 1 节点）

| # | slug | 用途 | 预期产出 |
|---|------|------|----------|
| 1 | `agent-evolution` | 部署后让智能体记录发现、演化并精炼自身操作手册 | 演化日志 + 精炼后的操作程序 |

## 真实可用性（诚实分级）

`lgd-evo --verify` 会**实探**该节点的活动工作集目录与可执行脚本，给出三种状态：

- **LIVE**：活动工作集内有目录且有可运行脚本（`--help` 退出码 0）→ 真能演化。
- **ECOSYSTEM**：在 GovernanceOS 路由里声明、但当前活动工作集无目录（仅生态/备份层）→ 需
  `openclaw plugins install clawhub:agent-evolution` 或引用生态层后才可用。
- **ERROR**：目录在但脚本执行异常 → 需修复。

> 诚实声明：`--verify` 输出以**当前机器实际探测**为准，不以文档宣称。

## 用法

```bash
python lgd_evo.py --list                       # 列出 EVO 阶段节点
python lgd_evo.py --verify --json-out evidence.json   # 实探可用性
python lgd_evo.py --route agent-evolution             # 调用说明
```

## 设计纪律（为什么是薄分发器）

- **零臃肿**：演化能力扩展 = 改本技能 `NODES` 表里一行，不复制任何代码。
- **可插拔**：节点是独立 slug，版本独立、各自发布；本技能只引用。
- **诚实**：探测不到如实标 ECOSYSTEM，绝不伪称"已实跑"或"全绿"。
- **只读**：`--verify` 仅以 `--help` 只读探针方式读取子技能元信息，不做任何演化写动作、不对外写。

## Known Limits

- 本技能**不替**子技能做演化；它只路由与探测。真实演化由 `agent-evolution` CLI 执行。
- 跨机/未安装子技能时，`--verify` 会显示 ECOSYSTEM，属预期，非缺陷。

## 参考

- 上游编排器：`governanceos` → `scripts/governance_flow.py`（PHASES["evo"] 为权威节点清单）。
- 三律：`有籍 / 有证 / 有门禁`（registered / evidenced / gated）。
