---
name: label-compliance-checker
slug: label-compliance-checker
displayName: 医疗器械标签合规核对器
version: 1.0.1
category: it-ops-security
display_name: 医疗器械标签合规核对器
title: 医疗器械标签合规核对器
author: 诺康(SynomosAI)
author_note: '"SynomosAI" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 医疗器械标签合规核对器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-004域（医疗器械全链路）。 适用场景：当需要医疗器械标签合规核对器能力时使用本技能；触发词：医疗器械、合规、判定器、TH-MED-004、label-compliance-checker。
tags: [医疗器械, 合规, 判定器, TH-MED-004, label-compliance-checker]
description_zh: "医疗器械标签合规核对器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-004域（医疗器械全链路）。"
description_en: "Medical device label compliance verification tool: zero-dependency decision support with JSON IR output (domain TH-MED-004, full device chain)."
classification:
  internal: ["medical-device compliance consulting"]
  skillhub: ["medtech-reg"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Functional suitability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
platforms: [windows, macos, linux]
read_when:
  - TH-MED-004 域内对医疗器械全链路标签做自动化合规预检
  - 官方规则源更新后要批量验证现有/新版标签适用性
  - 质量管理系统要无依赖生成结构化 JSON IR 决策支持数据
  - 用户说「标签上这些法定要素齐不齐」
ai_protocol: true

---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
1. Automated pre-compliance check of medical-device labels across the full chain within the TH-MED-004 domain.
2. After an official rule-source update, fast batch re-validation of existing or new-version labels.
3. When a quality-management system needs dependency-free decision-support data in structured JSON IR output.

### Usage
Document-style tool — no external script. Call via the standard request format:
1. Inputs: label text (`label_content`), device model (`device_model`) and rule-source version (`rule_source_version`).
2. For batch labels, pass a list in the single request via the `labels_list` field.
3. On call, the JSON IR verdict returns directly — no extra command parsing.

### Workflow
1. Confirm the device label under check and its TH-MED-004 rule version.
2. Build the standard request body; fill label text, metadata and rule IDs into the JSON fields.
3. Submit to trigger the internal rule engine for logical comparison and conflict detection.
4. The engine parses the built-in official rule source and runs the compliance algorithm.
5. Receive the JSON IR and check the `compliance_status`.
6. Emit a release slip or flag violations for human review.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. TH-MED-004 域内，对医疗器械全链路标签进行自动化合规性预检。
2. 官方规则源更新后，需快速批量验证现有或新版本标签的适用性。
3. 质量管理系统需要生成无依赖决策支持数据，要求输出为结构化 JSON IR。

### 用法
本技能为文档型工具，无需外部脚本执行，直接通过标准请求格式调用：
1. 输入参数需指定标签文本 (`label_content`)、设备型号 (`device_model`) 及规则源版本 (`rule_source_version`)。
2. 若需多标签批量处理，请在单一请求中将数据列表化传入 `labels_list` 字段。
3. 调用后将直接获取 JSON IR 格式的判定结果，无需额外解析命令。

### 流程
1. 确认待检设备标签及对应的 TH-MED-004 规则版本号。
2. 构建标准请求体，将标签文本、元数据及规则标识填入对应 JSON 字段。
3. 提交请求触发内部规则引擎进行逻辑比对与冲突检测。
4. 系统自动解析内置官方规则源并执行合规性推演算法。
5. 接收返回的 JSON IR 数据，确认 `compliance_status` 状态。
6. 根据结果生成放行单或标记违规项供人工复核处理。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
