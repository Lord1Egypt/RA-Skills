---
name: governance-method-suite
display_name: LGD 治理方法论合集
display_name_en: LGD Governance Method Suite
slug: governance-method-suite
title: LGD 治理方法论合集（Governance Method Suite）
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
description: >-
  One playbook for the full AI-agent governance loop: red-team drill -> injection shield -> leak scan -> desensitization -> kill-switch -> badge issue/verify -> skill & publish quality gates.

  一套方法论跑通智能体治理全流程：红队演练 -> 注入防护 -> 泄漏扫描 -> 文档脱敏 -> 停机开关 -> 徽章签发/核验 -> 技能质量门与发布门。按 slug 编排 9 个已独立发布的子技能，不内嵌子包内部实现。当用户要治理方案、安全审计或发布合规评审时使用。
description_zh: "一套方法论跑通智能体治理全流程：红队演练 -> 注入防护 -> 泄漏扫描 -> 文档脱敏 -> 停机开关 -> 徽章签发/核验 -> 技能质量门与发布门。按 slug 编排 9 个已独立发布的子技能，不内嵌子包内部实现。当用户要治理方案、安全审计或发布合规评审时使用。"
description_en: "One playbook for the full AI-agent governance loop: red-team drill -> injection shield -> leak scan -> desensitization -> kill-switch -> badge issue/verify -> skill & publish quality gates. Orchestrates 9 independently published sub-skills by slug; does not vendor their internals."
read_when:
  - 用户要一套智能体治理/安全合规的端到端方案或路线图
  - 上线前要做安全审计：红队、注入防护、泄漏扫描、文档脱敏
  - 发布合规评审：技能质量门、发布门、徽章凭证签发与核验
  - 用户说「治理全流程怎么跑」「发布前要过哪些门」「给我一套治理方法论」
agent_created: true
author: SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中方法论文本不在 MIT 覆盖范围内
allowed-tools: Read, Grep, Bash
category: AI 治理
platforms: [windows, macos, linux, cli]
copyright: SynomosAI
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: low
risk_rationale: "纯文档编排 + 只读路由脚本：不调用外部 API、不读写业务数据、不代执行发布动作；仅按 slug 索引已有子技能。"
tags: [governance, 治理, security, red-team, method-suite, quality-gate, badge, 合集]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/governance_flow.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "--list 列出全流程环节；--route <stage|slug> 给出该环节的调用说明与预期输出"
    required: false
output_schema:
  stdout: 路由表（环节 | slug | 何时用 | 调用说明 | 预期输出）
  exit_code: "rc=0 正常；rc=2 未知环节/slug"
changelog: "1.0.1: Bump to dodge ClawHub version conflict on initial submit; 1.0.0: Initial bilingual collection (打法2合集化) — orchestrates 9 published governance sub-skills by slug."
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### What this is
A **collection / orchestration** skill: one playbook that wires the full AI-agent governance loop end to end. It does not re-implement security logic — it routes you, stage by stage, to 9 sub-skills that are already published and maintained on their own. Treat this as the table of contents; the sub-skills are the chapters.

The flow is:

`red-team drill -> injection shield -> leak scan -> desensitization -> kill-switch -> badge issue/verify -> skill gate -> publish gate`

### Entry index (slug | stage | when to use | call note)

| # | Stage | Sub-skill slug | When to use | Call note | Expected output |
|---|-------|----------------|-------------|-----------|-----------------|
| 1 | Red-team drill | `agent-redteam-kit` | Before launch: stress-test the agent adversarially | Invoke the sub-skill; run its drill | Scored attack-surface report + fix list |
| 2 | Injection shield | `prompt-injection-shield` | Hostile user/tool input must be blocked | Invoke the sub-skill on the prompt | Guard allow/block decision |
| 3 | Leak scan | `prompt-leak-scanner` | Before shipping a system prompt: catch internal/secret leakage | Invoke the sub-skill on the prompt | Leak findings (line-level) |
| 4 | Desensitization | `doc-desens-scanner` | Before a doc/code/log goes external | Invoke the sub-skill on the file | Masked copy + audit ledger |
| 5 | Kill switch | `agent-kill-switch` | Before deploying a high-risk/funds agent | Generate then `--check` the kill card | Complete kill card; blocks if fields missing |
| 6 | Badge issue | `lgd-badge-issuer` | After three-law assessment passes | Invoke the sub-skill to issue | Badge certificate + SHA-256 fingerprint + ledger row |
| 7 | Badge verify | `lgd-badge-verify` | Before trusting an external badge | Invoke the sub-skill on the badge | Verify pass/fail with reasons |
| 8 | Skill quality gate | `skill-quality-gate` | Before admitting a skill to the library | Invoke the sub-skill on the skill dir | Gate verdict + blocking findings |
| 9 | Publish gate | `publish-quality-gate` | Right before external publish | Invoke the sub-skill | Publish verdict; blocks launch on blockers |

### Per-stage notes
- **1. Red-team first.** You can't defend what you haven't attacked. Run `agent-redteam-kit` early and feed its findings into stages 2–4.
- **2–4. Defense in depth.** Shield runtime input (2), scan the prompt itself (3), and desensitize anything that leaves the boundary (4).
- **5. Control plane.** Even with good scans, a high-risk agent needs a pre-authored kill card — `--check` makes completeness a hard gate.
- **6–7. Provenance.** Issue a badge only after gates pass; verify someone else's badge before relying on it.
- **8–9. Release gates.** Two gates, two purposes: library admission (8) vs. external publish (9). Both must be green.

### Demo
```bash
# list the whole flow
python3 scripts/governance_flow.py --list

# get the call note for one stage
python3 scripts/governance_flow.py --route redteam

# ...or by sub-skill slug
python3 scripts/governance_flow.py --route lgd-badge-verify
```

### Scope & red lines
- This suite **vendors no sub-skill internals**. It references sub-skills by slug only; their code stays in their own packages.
- Pure documentation + a read-only router. No network, no business-data writes, no acting on your behalf.
- Sub-skill release status is tracked separately in the governance ledger; this suite does not republish or fork them.

## 中文

### 这是什么
一个**合集/编排**技能：用一套 playbook 把智能体治理的完整闭环串起来。它不重写安全逻辑——而是按环节，把你路由到 9 个已独立发布、各自维护的子技能。本合集是目录，子技能是章节。

治理闭环：

`红队演练 -> 注入防护 -> 泄漏扫描 -> 文档脱敏 -> 停机开关 -> 徽章签发/核验 -> 技能质量门 -> 发布门`

### 入口索引（slug | 环节 | 何时用 | 调用说明）

| # | 环节 | 子技能 slug | 何时用 | 调用说明 | 预期输出 |
|---|------|-------------|--------|----------|----------|
| 1 | 红队演练 | `agent-redteam-kit` | 上线前对抗性压测智能体 | 调子技能跑演练 | 攻击面评分报告 + 修复清单 |
| 2 | 注入防护 | `prompt-injection-shield` | 需拦截恶意用户/工具输入 | 对 prompt 调子技能 | 放行/拦截判定 |
| 3 | 泄漏扫描 | `prompt-leak-scanner` | 发系统提示词前查内部/密钥泄漏 | 对 prompt 调子技能 | 泄漏发现（行级） |
| 4 | 文档脱敏 | `doc-desens-scanner` | 文档/代码/日志对外前 | 对文件调子技能 | 脱敏版 + 留痕清单 |
| 5 | 停机开关 | `agent-kill-switch` | 高危/资金类智能体部署前 | 先生成再 `--check` 制动卡 | 完整制动卡；缺项即阻断 |
| 6 | 徽章签发 | `lgd-badge-issuer` | 三律考核通过后申请徽章 | 调子技能签发 | 徽章证书 + SHA-256 指纹 + 台账行 |
| 7 | 徽章核验 | `lgd-badge-verify` | 信任外部徽章前 | 对徽章调子技能 | 通过/不通过 + 原因 |
| 8 | 技能质量门 | `skill-quality-gate` | 技能入库存准入前 | 对技能目录调子技能 | 门禁结论 + 阻断项 |
| 9 | 发布门 | `publish-quality-gate` | 对外发布前最后一道 | 调子技能 | 发布结论；有阻断项即不许上线 |

### 环节说明
- **1. 先红队。** 没攻过就谈不上防。尽早跑 `agent-redteam-kit`，把发现喂给 2–4。
- **2–4. 纵深防御。** 运行时拦注入（2）、扫提示词本身（3）、对出边界的东西脱敏（4）。
- **5. 控制面。** 即使扫描到位，高危智能体也要预先写好制动卡——`--check` 把字段齐全做成硬门禁。
- **6–7. 凭证。** 门禁全过才发徽章；信任别人的徽章前先核验。
- **8–9. 发布门。** 两道门两种用途：入库准入（8）与对外发布（9），两道都要绿。

### 示例
```bash
# 列出全流程
python3 scripts/governance_flow.py --list

# 查某个环节怎么调
python3 scripts/governance_flow.py --route redteam

# 也可按子技能 slug 查
python3 scripts/governance_flow.py --route lgd-badge-verify
```

### 边界与红线
- 本合集**不内嵌任何子技能内部实现**，仅按 slug 引用；子包代码留在各自包内，不改不复制。
- 纯文档 + 只读路由脚本：无网络、不写业务数据、不代你执行任何动作。
- 各子技能的发布状态在治理台账单独跟踪；本合集不重发、不 fork 它们。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「公司要上一套AI治理方案，从哪开始」 / "We need an AI governance program, where do we start"
- 「帮我把这些安全工具串成一条流程」 / "Chain these security tools into one workflow"
- 「上线前要做哪些合规检查」 / "What compliance checks before we go live"
- 「红队演练、脱敏、熔断怎么排顺序」 / "Red team, desensitization, kill-switch, what order"
- 「这套治理方案覆盖全了吗」 / "Does this governance plan cover everything"
- 「技能发布前要过几道闸门」 / "How many gates before a skill can ship"

Trigger when the user says any of the above, in Chinese or English.

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/governance-method-suite
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/governance-method-suite/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
