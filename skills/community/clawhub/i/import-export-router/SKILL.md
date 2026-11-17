---
name: import-export-router
slug: import-export-router
displayName: 医疗器械进出口路径判定器
version: 1.0.1
category: it-ops-security
display_name: 医疗器械进出口路径判定器
title: 医疗器械进出口路径判定器
author: 诺衡(SynomosAI)
author_note: '"SynomosAI" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 医疗器械进出口路径判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-005域（医疗器械全链路）。 适用场景：当需要医疗器械进出口路径判定器能力时使用本技能；触发词：医疗器械、合规、判定器、TH-MED-005、import-export-router。
tags: [医疗器械, 合规, 判定器, TH-MED-005, import-export-router]
description_zh: "医疗器械进出口路径判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-005域（医疗器械全链路）。"
description_en: "Medical device import/export pathway determination tool: zero-dependency decision support with JSON IR output (domain TH-MED-005, full device chain)."
classification:
  internal: ["medical-device compliance consulting"]
  skillhub: ["medtech-reg"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Functional suitability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
platforms: [windows, macos, linux]
read_when:
  - 医疗器械进出口前要基于官方规则源判定合规路径
  - 要构建零依赖决策支持，避免外部脚本/数据库依赖
  - 业务要覆盖 TH-MED-005 域全链路监管查询与路径生成
  - 用户说「这个设备出口要不要先注册」「进口路径怎么走」
ai_protocol: true

---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
This skill applies when the import/export compliance path of a medical device must be determined strictly from official rule sources; when building a zero-dependency decision-support system that must avoid external scripts or databases; and when the business logic must cover full-chain regulatory lookup and path generation across the TH-MED-005 domain.

### Usage
No local script to load — call through the document interface. The core input is JSON: `device_category`, `origin_country` and `target_regime`. The result returns as standard JSON IR, embeddable directly into workflow variables for downstream computation or decision logic.

### Workflow
1. Prepare the device model and its trade-path info; ensure the data source meets the TH-MED-005 standard.
2. Build the JSON request body with the required parameters and send it through the skill interface.
3. Receive the JSON IR verdict — no local file read/write.
4. Parse the route type and required approval nodes (drug regulator, commodity inspection, etc.) from the output.
5. Produce the decision report per the rule source, or auto-trigger the downstream filing step.
6. Keep the full call log for audit traceability, so the compliance decision stays verifiable.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
本技能适用于以下场景：当您需要对医疗器械进出口路径进行合规性判定，且必须严格基于官方规则源时；在构建零依赖的决策支持系统，需避免引入外部脚本或数据库依赖；以及当业务逻辑需要覆盖 TH-MED-005 域的全链路监管查询与路径生成。

### 用法
调用本技能无需加载本地脚本文件，直接通过文档型接口进行参数传递。核心输入参数为 JSON 格式，包含 `device_category`（设备分类）、`origin_country`（原产国）及 `target_regime`（目标监管地）。输出结果以标准 JSON IR 形式返回，直接嵌入流程变量中即可用于后续计算或判断逻辑的调用。

### 流程
1. 准备待判定的医疗器械型号及其贸易路径信息，确保数据源符合 TH-MED-005 标准。
2. 构造包含必要参数的 JSON 请求体，并通过技能调用接口发送指令。
3. 等待系统返回 JSON IR 形式的判定结果，无需处理本地文件读写操作。
4. 解析输出中的路径类型及所需审批节点（如药监、商检等）字段。
5. 依据规则源指引生成决策报告，或自动触发后续的申报流程动作。
6. 保存完整的调用日志以供审计追溯，确保合规性决策可验证。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
