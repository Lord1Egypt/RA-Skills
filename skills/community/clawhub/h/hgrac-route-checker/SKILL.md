---
name: hgrac-route-checker
slug: hgrac-route-checker
displayName: 人类遗传资源事项路径判定器
version: 1.0.2
category: it-ops-security
display_name: 人类遗传资源事项路径判定器
title: 人类遗传资源事项路径判定器
author: 诺康(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 人类遗传资源事项路径判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-BIO-001域。 适用场景：当需要人类遗传资源事项路径判定器能力时使用本技能；触发词：合规、判定器、TH-BIO-001、hgrac-route-checker。
tags: [合规, 判定器, TH-BIO-001, hgrac-route-checker, 人类遗传资源]
description_zh: "人类遗传资源事项路径判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-BIO-001域。"
description_en: "Human genetic resources approval-path determination tool: zero-dependency decision support with JSON IR output (domain TH-BIO-001)."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
platforms: [windows, macos, linux]
read_when:
  - 人类遗传资源科研项目立项申报前要快速判定审批层级与路径
  - 生物样本采集申请书要自动匹配《人类遗传资源管理条例》分类
  - 审核流程中遇不确定条款，要基于官方规则源独立推理
  - TH-BIO-001 域特殊豁免申请或跨区域样本流转要路径比对
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: hgrac-route-checker.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见各包 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS/完成；1=FAIL/有警告或待补强；2=用法或参数错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.2: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
1. When a human-genetic-resource research project is being initiated, and the required approval tier and route compliance must be determined quickly.
2. When a biological-sample collection application is submitted, for auto-matching against the classification standard in the Human Genetic Resources Regulation.
3. When an ambiguous clause must be interpreted during project review, requiring independent reasoning from official rule sources.
4. When comparing routes for special exemption applications or cross-region sample transfer under the TH-BIO-001 domain.

### Usage
- **Input**: submit project details (sample type, collection purpose, institution qualification) via natural-language dialogue or a structured JSON object.
- **Built-in resources**: the TH-BIO-001 official rule source loads automatically on call — no external documents to upload.
- **Output**: standardized JSON IR; core fields are `path_decision`, `required_level`, `rule_ids`.
- **Limitations**: no script-directory support; the tool runs only as a context-triggered decision assistant.

### Workflow
1. Prepare the project basics and sort out the key elements of human genetic resources management.
2. Send a request (instruction or data) with a clear determination target.
3. The system parses the input and searches the internal rule base for logical matching.
4. Receive the JSON IR result; review the approval route and restriction clauses.
5. Verify filing-material completeness against the suggested route; confirm regulatory compliance.
6. Act on the determination: proceed with filing, revise the plan, or terminate the process.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.2
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 在进行人类遗传资源科学研究项目立项申报时，需快速判定所需审批层级及路径合规性。
2. 当用户上传生物样本采集申请书信息时，用于自动匹配《人类遗传资源管理条例》中的分类标准。
3. 在项目审核流程中遇到不确定条款解读需求，需要基于官方规则源进行独立逻辑推理时。
4. 涉及 TH-BIO-001 域下的特殊豁免申请或跨区域样本流转时的路径比对场景。

### 用法
**输入方式**：通过自然语言对话或结构化 JSON 对象提交项目详情（含样本类型、采集目的、机构资质）。
**内置资源**：调用技能时自动加载 TH-BIO-001 域官方规则源，无需用户上传外部文档。
**输出参数**：返回标准化 JSON IR，核心字段包含 `path_decision`、`required_level`、`rule_ids`。
**执行限制**：本技能为上下文触发的决策辅助工具。

### 流程
1. 准备项目基础信息并梳理人类遗传资源管理的关键要素。
2. 向技能发送包含明确判定目标的指令或数据请求。
3. 系统将自动解析输入并检索内部规则库进行逻辑匹配。
4. 获取 JSON IR 返回结果，重点审查审批路径与限制条款。
5. 根据建议路径验证申报材料完整性，确认是否符合法规要求。
6. 依据工具判定结果，执行后续申报、修改方案或终止流程。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.2
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
