---
name: kyc-checklist-gen
description: KYC 材料齐备清单 — 一键生成个人/企业 KYC 必备材料清单并核算齐备度，缺项即 FAIL（零依赖） 适用场景：当需要KYC 材料齐备清单能力时使用本技能；触发词：kyc-checklist-gen。
slug: kyc-checklist-gen
version: 1.0.1
display_name: KYC 材料齐备清单
display_name_en: KYC Checklist Generator
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "KYC 材料齐备清单 — 一键生成个人/企业 KYC 必备材料清单并核算齐备度，缺项即 FAIL（零依赖）"
description_en: "Generate personal and enterprise KYC document checklists with completeness scoring; missing items FAIL (zero-dependency)."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [kyc-checklist-gen, AI 治理, KYC, 开户材料]
read_when:
  - 金融账户开户/企业注册申报前要核验合规材料
  - 不确定 KYC 清单标准或要快速评估现有资料是否完备
  - 要一键生成个人/企业 KYC 必备材料清单并核算齐备度
  - 用户说「开户要准备哪些材料」「我的资料齐不齐」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/kyc_checklist_gen.py
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
Applies to scenarios that must verify compliant materials — financial account opening, enterprise registration filings and the like. Use it when the user is unsure what the KYC checklist standard requires, or needs a fast assessment of whether existing documents are complete — i.e. an independent document-generation need that outputs a standardized checklist with a FAIL/PASS verdict.

### Usage
The command is `python kyc_checklist_gen.py --mode [generate|check] --subject_type [personal|company]`. The `-d` flag points at a data file for the system to read and compare. As a tool, just run the script to get the output checklist and the completeness score — no extra dependencies to configure.

### Workflow
1. Choose the personal or enterprise subject type; confirm the data source to verify.
2. Launch `kyc_checklist_gen.py` to load the standard library and run the logic.
3. The system compares the current material list against the KYC spec requirements.
4. Output a detailed missing-items report and the completeness score.
5. If the verdict is FAIL, fill in the missing files as prompted or regenerate.
6. Re-verify until the result reaches a compliant pass.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
适用于金融账户开户、企业注册申报等需要核验合规材料的场景。当用户不确定所需 KYC 清单标准，或需快速评估现有资料是否完备时。用于生成标准化检查表并提供 FAIL/PASS 判定结论的独立文档生成需求。

### 用法
调用命令为 `python kyc_checklist_gen.py --mode [generate|check] --subject_type [personal|company]`。支持 `-d` 参数指定数据文件路径供系统读取比对。作为工具使用时，直接执行脚本即可获取输出清单及齐备度数值，无需额外配置依赖项。

### 流程
1. 选择个人或企业主体类型，确认待核验的数据源。
2. 启动 `kyc_checklist_gen.py` 进行标准库加载与逻辑计算。
3. 系统比对当前材料清单与 KYC 规范需求。
4. 输出详细的缺项报告及齐备度评分结果。
5. 若判定为 FAIL，根据提示补全缺失文件或重新生成。
6. 验证最终结果直至达到合规通过状态。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
