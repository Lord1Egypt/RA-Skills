---
name: invoice-risk-scan
description: 发票要素风险扫描 — 报销/入账前扫发票要素：税号格式、金额、日期合理性，异常即拦（零依赖） 适用场景：当需要发票要素风险扫描能力时使用本技能；触发词：invoice-risk-scan。
slug: invoice-risk-scan
version: 1.0.1
display_name: 发票要素风险扫描
display_name_en: Invoice Risk Scan
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "发票要素风险扫描 — 报销/入账前扫发票要素：税号格式、金额、日期合理性，异常即拦（零依赖）"
description_en: "Scan invoice elements before reimbursement or booking: tax-ID format, amounts and date plausibility; anomalies are blocked (zero-dependency)."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [invoice-risk-scan, AI 治理, 发票, 报销风控]
read_when:
  - 财务报销/入账前要对发票要素做前置风险扫描
  - 自动化流程需要零依赖外部风控工具校验发票
  - 批量票据审核要快速识别税号格式/金额/日期异常
  - 用户说「这张发票能不能报」「税号金额有没有问题」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/invoice_risk_scan.py
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
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
- As a pre-check step for invoice-element risk scanning and compliance validation before financial reimbursement or booking.
- Fits automated pipelines that need a zero-dependency external risk-control tool.
- Used in batch invoice review to quickly flag anomalies in tax-ID format, amounts and dates.

### Usage
- Call the script `invoice_risk_scan.py`, passing the invoice file path or structured data through the parameter interface.
- Risk thresholds and blocking actions are configurable; main parameters include the input file path, validation rules and the anomaly-handling switch.
- In document-style environments, reference the script path directly and define the input/output field mapping.

### Workflow
- Prepare the invoice data; ensure file completeness and a format the parser can read.
- Start the service and submit the call with the chosen validation parameters and rule config.
- The risk model scans and logically compares key elements: tax ID, amount, date.
- Emit the detection report and risk level; anomalous data triggers an automatic block of the downstream process.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
- 在财务报销或入账前，作为前置环节对发票要素进行风险扫描与合规校验。
- 适用于自动化处理流程，满足“零依赖”外部风控工具的场景需求。
- 用于批量票据审核中，快速识别税号格式、金额及日期等方面的异常信息。

### 用法
- 调用系统脚本 `invoice_risk_scan.py`，通过参数接口传入发票文件路径或结构化数据。
- 支持配置风险阈值与拦截动作，主要参数包括输入文件路径、校验规则及异常处理开关。
- 在文档型环境中，直接引用该脚本路径并定义输入输出字段映射关系。

### 流程
- 准备待处理发票数据，确保文件完整性及格式符合系统解析标准。
- 启动技能服务并提交调用请求，传入指定的校验参数及规则配置。
- 执行风险模型扫描，对税号、金额、日期等关键要素进行逻辑比对。
- 输出检测报告并返回风险等级，若存在异常数据则自动触发拦截阻断后续流程。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
