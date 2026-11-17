---
name: originality-check
slug: originality-check
displayName: 赛事作品原创性查重器
version: 1.1.1
category: ai-agent
display_name: 赛事作品原创性查重器
title: 赛事作品原创性查重器
author: 诺源(SynomosAI)
author_note: '"SynomosAI" / "SynomosAI" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事作品原创性查重器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-005域。 适用场景：当需要赛事作品原创性查重器能力时使用本技能；触发词：赛事、判定器、TH-EVT-005、originality-check。
tags: [赛事, 判定器, TH-EVT-005, originality-check, 原创性, 查重]
description_zh: "赛事作品原创性查重器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-005域。"
description_en: "Contest submission originality and plagiarism checker: zero-dependency decision support with JSON IR output (UIBC spec, domain TH-EVT-005)."
read_when:
  - 参赛者提交作品前需做原创性预审
  - 担心作品与历史/公开库雷同、违反学术道德
  - 需要零依赖的原创性合规检查报告供决策
  - 赛事评审要批量比对作品指纹
classification:
  skillhub: ["community-events"]
  iso_25010: ["Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: originality-check.py
  runtime: python3
  call_pattern: args
input_schema:
  submission_hash:
    type: string
    description: "作品指纹（必填，缺失时报错 rc=2）"
    required: false
  known_hashes:
    type: string
    description: "历史/公开库指纹 JSON 字符串列表（缺省按空库从严告警）"
    required: false
  demo:
    type: bool
    description: "跑内置冒烟案例"
    required: false
  json:
    type: bool
    description: "输出 JSON IR（默认）"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - originality
  - plagiarism
  - contest
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
- When a contestant is preparing to submit a work and needs an originality pre-check per UIBC contest rules.
- When working in technical (TH) domains such as TH-EVT-005 and you worry about content overlap or violations of academic-integrity standards.
- When you need a quick compliance check report, produced by a zero-dependency tool, to support decision-making.

### Usage
- **Invocation**: trigger the skill directly through system instructions or conversation context; no external script loading is required.
- **Parameters**: pass `work_content` (work text or file summary) and `target_domain` (e.g. TH-EVT-005).
- **Output format**: the response strictly follows JSON IR and includes similarity metrics and a risk rating.

### Workflow
1. The user prepares and uploads or types the work content to be checked into context.
2. The required check-standard domain is specified (e.g. the TH-EVT-005 technical spec).
3. The system performs an internal comparison, invoking the built-in knowledge base for duplicate detection.
4. It generates a JSON IR feedback report containing the originality score.
5. Based on the risk level in the feedback, adjust the work or the submission decision.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.1.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用

- 当参赛者准备提交作品，需依据 UIBC 赛事规范进行原创性预审时。
- 在涉及技术类（TH）领域（如 TH-EVT-005），担心内容雷同或违反学术道德标准时。
- 需要快速生成符合零依赖工具要求的合规性检查报告供决策参考时。

### 用法

- **调用方式**：通过系统指令或对话上下文直接触发技能，无需加载外部脚本。
- **参数定义**：需传入 `work_content`（作品文本或文件摘要）及 `target_domain`（指定如 TH-EVT-005）。
- **输出规范**：响应将严格遵循 JSON IR 格式，包含相似度指标与风险评级。

### 流程

1. 用户准备并上传或输入待检作品内容至上下文。
2. 明确指定核查标准域（如 TH-EVT-005 技术规范）。
3. 系统执行内部比对，调用内置知识库进行查重分析。
4. 生成包含原创性评分的 JSON IR 反馈报告。
5. 依据反馈中的风险等级调整作品或提交决策。

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
