---
name: lgd-audit
description: lgd-audit — LGD 审计中枢（meta 薄分发器）。把 GovernanceOS 的 AUDIT 阶段 10 个审计节点聚合成可检索、可一键探测的入口：徽章签发/验真、三律审计、行为追溯、偏见审计、环境密钥审计、治理审计链、审计留痕、专家包合规审计、可追溯性审计团。另含 LGD三律审计器（lgd-audit.py）口径说明。只按 slug 路由到独立子技能，不搬运、不重实现任何子技能代码。 适用场景：当需要AI 智能体审计/合规/可追溯/三律核验能力时使用本技能；触发词：lgd-audit、审计、三律、可追溯、合规审计。
slug: lgd-audit
version: 1.0.3
homepage: https://zhaoxinghua09-cell.github.io/lgd-skills-index/
display_name: LGD 审计中枢
display_name_en: LGD Audit Hub
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
copyright: XLGD · SynomosAI
description_zh: "lgd-audit — LGD 审计中枢（meta 薄分发器），把 AUDIT 阶段 10 个审计节点聚合成可检索可探测入口。"
description_en: "LGD Audit Hub — a thin meta-dispatcher that aggregates the 10 AUDIT-phase governance nodes into one discoverable, self-verifying entry point."
classification:
  internal: ["主轴2 理论体系(LGD)"]
  skillhub: ["ai-governance"]
  clawhub: ["search", "development"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "meta 薄分发器默认 medium：仅按 slug 路由并只读探测（--help），不代执行子技能、不对外写；若需经本技能触发实际审计/合规拦截，须由被路由的子技能各自走其 own 风险评审。"
tags: [lgd-audit, AI 治理, 审计, 三律, 可追溯, 合规]
ai_protocol: true

lineage: ["LGD-有籍", "LGD-有证", "LGD-有门禁", "GovernanceOS-AUDIT"]
---

# LGD 审计中枢（lgd-audit）

> **薄分发器（thin dispatcher）**：本技能不搬运、不重实现任何审计代码。它只是 GovernanceOS
> `SPEC → PLAN → GATE → AUDIT → EVO` 生命周期里 **AUDIT 阶段**的聚合入口——把 10 个独立发布的
> 审计子技能按 slug 列出、一键探测可用性、给出调用说明。所有真实审计由被路由的子技能完成。

## When to Use

- 你要给一个 AI 智能体/技能/交付物**做审计、合规核验、可追溯**，但不知道该用哪个审计器。
- 你需要**一键看清**当前 AUDIT 阶段有哪些审计器、哪些真的装上了、哪些只在生态/备份层。
- 你要核验别人/自己签发的三律徽章是否真实（有籍/有证/有门禁）。
- 触发词：`lgd-audit`、`审计`、`三律`、`可追溯`、`合规审计`。

## 核心能力（AUDIT 阶段 10 节点）

| # | slug | 用途 | 预期产出 |
|---|------|------|----------|
| 1 | `lgd-badge-issuer` | 三律全过签发 lgd-certified 徽章证书（SHA-256 指纹 + 签发台账） | 徽章证书 + 指纹 |
| 2 | `lgd-badge-verify` | 核验他人徽章指纹与台账，依赖前先验证 | 验真 pass/fail + 理由 |
| 3 | `lgd-three-laws-auditor` | 审计包是否符合三律（有籍/有证/有门禁） | 三律审计判定 + 每律证据 |
| 4 | `agent-trace-audit` | 重建智能体行为追溯日志（事后审计） | 行为追溯日志 + 异常标记 |
| 5 | `bias-auditor` | 发布前对输出/决策做偏见审计 | 偏见审计报告 + 标记维度 |
| 6 | `env-var-audit` | 部署前环境变量/密钥暴露审计 | 密钥暴露报告 + 命中项 |
| 7 | `ai-governance-audit-chain` | 跨生命周期构建治理审计链 | 串联各门禁/证据的审计链文档 |
| 8 | `audit-trail-keeper` | 维护不可变审计留痕台账（append-only） | 审计留痕台账 |
| 9 | `expert-package-compliance-audit` | 专家/包发布前合规审计 | 合规审计判定 + 阻断项 |
| 10 | `traceability-audit-team` | 跨交付物跑可追溯性审计团 | 可追溯性矩阵 + 覆盖缺口 |

## 配套的 LGD 三律审计器（lgd-audit.py）

除上面 10 个节点外，生态层还有独立的 **LGD三律审计器** `lgd-audit.py`（发布总账维护），
按方案口径扫描全库：

- **有籍 7/7**：`name / version / author / license / display_name / copyright / lineage` 全非空
- **有证 3/3**：`demo/`或`examples/`目录 + `evidence.json` + 评测报告 三者存在
- **有门禁**：发布台账有该包行 + 台账/CHG/章程三文件在

退出码：`0` = 全库三律 100% 达标；`1` = 存在未达标包（发布前不放行）；`2` = 环境错误。
红线：只读扫描，不改任何技能包，凭证零落盘。

## 真实可用性（诚实分级）

`lgd-audit --verify` 会**实探**每个节点的活动工作集目录与可执行脚本，给出三种状态：

- **LIVE**：活动工作集内有目录且有可运行脚本（`--help` 退出码 0）→ 真能审。
- **ECOSYSTEM**：在 GovernanceOS 路由里声明、但当前活动工作集无目录（仅生态/备份层）→ 需
  `openclaw plugins install clawhub:<slug>` 或引用生态层后才可用。
- **ERROR**：目录在但脚本执行异常 → 需修复。

> 诚实声明：截至本技能发布快照，AUDIT 阶段 10 节点中**部分**在活动工作集（如 `lgd-badge-issuer`、
> `lgd-badge-verify`、`lgd-three-laws-auditor`、`agent-trace-audit`、`bias-auditor`、`env-var-audit`），
> 其余声明于路由/生态层。`--verify` 输出以**当前机器实际探测**为准。

## 用法

```bash
python lgd_audit_dispatcher.py --list                       # 列出 10 个审计节点
python lgd_audit_dispatcher.py --verify --json-out evidence.json   # 实探可用性
python lgd_audit_dispatcher.py --route lgd-three-laws-auditor       # 调用说明
```

## 设计纪律（为什么是薄分发器）

- **零臃肿**：新增/下线一个审计器 = 改本技能 `NODES` 表里一行，不复制任何代码。
- **可插拔**：每个节点是独立 slug，各自版本独立、各自发布；本技能只引用。
- **诚实**：探测不到的节点如实标 ECOSYSTEM，绝不伪称"已实跑"或"全绿"。
- **只读**：`--verify` 仅以 `--help` 只读探针方式读取子技能元信息，不做任何审计写动作、不对外写。

## Known Limits

- 本技能**不替**子技能做审计；它只路由与探测。真实审计由 `governance_flow.py` 或各子技能 CLI 执行。
- 跨机/未安装子技能时，`--verify` 会显示 ECOSYSTEM，属预期，非缺陷。

## 参考

- 上游编排器：`governanceos` → `scripts/governance_flow.py`（PHASES["audit"] 为权威节点清单）。
- 三律：`有籍 / 有证 / 有门禁`（registered / evidenced / gated）。
