---
name: lgd-three-laws-auditor
slug: lgd-three-laws-auditor
display_name: LGD 三律合规自检器（凡自治之物）
display_name_en: "LGD Three-Laws Compliance Auditor"
description: >-
  Self-assess AI systems against the LGD three laws (registered, evidenced, gated) as a standard rubric: identity/version/lineage/responsibility, evidence chains and permission gates.

  当用户问『我的 AI 系统合不合规 / 怎么评判 AI 治理水平 / agent 要不要上治理护栏』，或要落地『有籍·有证·有门禁』时用。把 LGD 三律做成一套可自评的标准 rubric（有籍=身份/版本/血缘/责任四项登记；有证=六类证据工件齐备；有门禁=触发/评审/放行/复盘四道门），输入系统描述即出评分卡+改进项。这不仅是工具，更是 LGD 治理思想的『定义器』——谁用三籍词汇自评，谁就采用了我们的治理定义权（竞争优势）。触发词：LGD 三律、有籍有证有门禁、凡自治之物、AI 合规自评、AI 治理标准、agent 治理护栏、三律审计。
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
read_when:
  - 用户要评判一个 AI 系统 / agent / 工作流的治理合规水平
  - 用户提到「凡自治之物」「有籍有证有门禁」「LGD 三律」
  - 要给别人讲清楚 AI 治理该看哪几栏（标准定义）
  - 做合规自检、写治理方案、准备认证前摸底
tags: [LGD, 三律, 凡自治之物, AI治理, 合规自检, 有籍, 有证, 有门禁, 标准定义]
copyright: XLGD · SynomosAI
description_zh: "当用户问『我的 AI 系统合不合规 / 怎么评判 AI 治理水平 / agent 要不要上治理护栏』，或要落地『有籍·有证·有门禁』时用。把 LGD 三律做成一套可自评的标准 rubric（有籍=身份/版本/血缘/责任四项登记；有证=六类证据工件齐备；有门禁=触发/评审/放行/复盘四道门），输入系统描述即出评分卡+改进项。这不仅是工具，更是 LGD 治理思想的『定义器』——谁用三籍词汇自评，谁就采用了我们的治理定义权（竞争优势）。触发词：LGD 三律、有籍有证有门禁、凡自治之物、AI 合规自评、AI 治理标准、agent 治理护栏、三律审计。"
description_en: "Self-assess AI systems against the LGD three laws (registered, evidenced, gated) as a standard rubric: identity/version/lineage/responsibility, evidence chains and permission gates."
classification:
  skillhub: ["ai-governance"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true


spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/lgd_audit.py
  runtime: python3
  call_pattern: args
input_schema:
  rubric:
    type: bool
    description: "打印完整三律标准"
    required: false
  system:
    type: string
    description: "AI 系统/工作流描述文本（启发式自评）"
    required: false
  answers:
    type: string
    description: "答卷 JSON 路径 {律:{检查项:yes|partial|no}}"
    required: false
  json:
    type: bool
    description: "输出 JSON"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - governance
  - audit
  - three-laws
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); read_when kept; 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
1. When a user asks about AI-system compliance, governance-level assessment, or whether an agent needs safety guardrails.
2. When the "registered · evidenced · gated" framework must be landed, turning the LGD three laws into a self-scoring standard rubric.
3. When the user provides a system description and wants an LGD-based compliance-audit scorecard with concrete improvement suggestions.

### Usage
1. Script: run `python lgd_audit.py` (or the related CLI) in the runtime to start the audit logic.
2. Input: `<system_description>` is the core required argument — describe the AI system's architecture, business logic or governance state; natural-language input is auto-parsed.
3. The skill reads the local script `lgd_audit.py` and the standard library; output is a JSON scorecard plus a text report, embeddable in CI/CD.

### Workflow
1. **Intent detection**: the system sees triggers like "LGD three laws" or "AI compliance self-check" and enters audit mode.
2. **Element extraction**: pull identity (registered), evidence (evidenced) and gate-process (gated) info from the description.
3. **Scoring**: run `lgd_audit.py`; the internal engine computes the "four registrations" and "four gates" compliance scores from the LGD definitions.
4. **Report**: emit a structured scorecard with defect points, a missing-evidence list and governance-gap analysis.
5. **Improvement**: guide the user to complete identity/lineage, archive key artifacts or add review-gate nodes.
6. **Closed loop**: suggest the user revise the description per the report and re-run, verifying the three laws now hold locally.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 当用户咨询 AI 系统合规性、治理水平评估或是否需要为 Agent 部署安全护栏时。
2. 当需要落地『有籍·有证·有门禁』治理框架，将 LGD 三律转化为可自评分标准 rubric 时。
3. 当用户提供系统描述，希望获得基于 LGD 标准的合规审计评分及具体的改进项建议时。

### 用法
1. 脚本命令：在运行环境调用 `python lgd_audit.py` 或相关 CLI 接口直接启动审计逻辑。
2. 输入参数：<system_description> 为核心必填参数，描述待评估的 AI 系统架构、业务逻辑或治理现状；支持自然语言输入自动解析。
3. 文档交互：技能核心读取本地脚本 `lgd_audit.py` 及标准库，输出为 JSON 评分卡与文本报告，可嵌入到 CI/CD 流程中。

### 流程
1. **意图识别**：系统检测到「LGD 三律」「AI 合规自评」等触发词，确认进入审计模式。
2. **要素提取**：从输入描述中提取身份（有籍）、证据（有证）及门禁流程（门禁）相关信息。
3. **标准评分**：运行 `lgd_audit.py`，内部引擎依据 LGD 定义计算「四登记」与「四道门」的合规分。
4. **报告生成**：输出包含缺陷点、缺失证据清单及治理缺口分析的结构化评分卡。
5. **改进执行**：指导用户在系统中补全身份血缘、归档关键工件或增加评审门禁节点。
6. **闭环确认**：建议用户根据报告修正描述并再次调用，验证 LGD 三律已在本地落地生效。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-three-laws-auditor
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-three-laws-auditor/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
