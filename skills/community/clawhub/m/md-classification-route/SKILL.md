---
name: md-classification-route
slug: md-classification-route
title: 医疗器械分类与注册路径初判器
displayName: 医疗器械分类与注册路径初判器
display_name: 医疗器械分类与注册路径初判器
display_name_en: MD Classification & Registration Route Screener
version: 1.0.1
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
author: SynomosAI (LGD initiative)
copyright: SynomosAI
category: 医疗器械合规
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
tags: ["医疗器械","医械合规","医疗器械分类与注册路径初判器","判定器","TH-MED-006","决策支持"]
description: "器械该按几类报、走哪条路——判错一次，整套资料重做。分类是多市场准入的第一块多米诺骨牌。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例） 适用场景：当需要医疗器械分类与注册路径初判器能力时使用本技能；触发词：医疗器械、医械合规、医疗器械分类与注册路径初判器、判定器、TH-MED-006。"
description_en: "Deterministic zero-dependency CLI screener for medical-device compliance (md-classification-route). JSON IR output, rc=0/1/2, demo case included. Decision support only — always verify against official texts."
description_zh: "器械该按几类报、走哪条路——判错一次，整套资料重做。分类是多市场准入的第一块多米诺骨牌。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例）"
read_when:
  - 新产品注册申报前不确定器械风险分类（I/II/III 类）
  - 多市场准入策略阶段要对比 EU MDR / 中国分类目录 / FDA 路径的成本
  - 法规预审时担心因错误分类导致申报资料返工
  - 需要确定性 JSON IR 供下游系统自动化处理分类结果
agent_created: true
verified_links: "规则源条款号已逐条标注；包内全部外链（含徽章）于 2026-09-12 逐条 HTTP 探测核验，11/11 可达"
classification:
  skillhub: ["medtech-reg"]
  iso_25010: ["Functional suitability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: md-classification-route.py
  runtime: python3
  call_pattern: args
input_schema:
  market:
    type: string
    description: "目标市场: cn/eu/us（默认 cn）"
    required: false
  invasive:
    type: string
    description: "是否侵入性: yes/no"
    required: false
  duration:
    type: string
    description: "侵入时长: transient/short_term/long_term（侵入性必填）"
    required: false
  active:
    type: string
    description: "是否有源: yes/no"
    required: false
  implant:
    type: string
    description: "是否植入: yes/no"
    required: false
  contact:
    type: string
    description: "接触部位: skin/mucosa/blood/cns/heart"
    required: false
  software:
    type: string
    description: "是否含驱动决策的软件: yes/no"
    required: false
  demo:
    type: bool
    description: "跑内置冒烟案例"
    required: false
  json:
    type: bool
    description: "输出 JSON IR"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - medtech
  - classification
  - regulation
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
Use this skill when, before a new product registration filing, you are uncertain about the device's risk class or its applicable scope, to make a preliminary determination of the classification category. During multi-market market-access strategy work, use it to compare the costs and compliance requirements of different regulatory pathways. At the regulatory pre-review stage, use it to verify whether the filing materials face rework risk caused by misclassification. Use it whenever you need deterministic JSON structured data (JSON IR) so downstream systems can automate classification handling.

### Usage
Input parameters: provide device type, intended indication and target-market information through structured tool calls. Core action: invoke the skill logic to obtain an `rc` code (0/1/2), which represents Class I/II/III and maps to the corresponding filing pathway. Output format: directly returns deterministic JSON IR whose fields include the classification result, the admission channel and the dependencies. Test mode: when the environment supports it, use the `--demo` flag to load the built-in typical case and quickly verify the logic.

### Workflow
1. The input module receives the device attribute data and the target regulatory-region identifier.
2. The skill engine performs internal rule matching to compute the risk class and compliance pathway.
3. It produces a JSON IR document containing the classification result (Class) and the route code.
4. The reviewer verifies that the returned `rc` value matches the expected regulatory category.
5. Based on the confirmed classification route, determine the subsequent document-preparation checklist.
6. Hand off to the next stage to generate registration filing materials or start the market-access process.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.0.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
当新产品注册申报前不确定器械风险等级或适用范围时，用于初步判定分类类别。
在多市场准入策略制定阶段，用于对比不同监管路径的成本与合规要求。
在法规预审环节，用于验证申报资料是否因错误分类导致返工风险。
需输出确定性 JSON 结构化数据（JSON IR）供下游系统自动化处理时。

### 用法
输入参数：通过结构化工具提供器械类型、拟适应症及目标市场信息。
核心动作：调用技能逻辑获取 `rc` 代码（0/1/2），代表 I/II/III 类并关联申报路径。
输出格式：直接返回确定性 JSON IR，字段包含分类结果、准入通道及依赖项。
测试模式：若环境支持，使用 `--demo` 参数加载内置典型案例快速验证逻辑。

### 流程
1. 输入模块接收器械属性数据与目标法规区域标识。
2. 技能引擎执行内部规则匹配以计算风险系数与合规路径。
3. 生成包含分类结果（Class）及路由代码的 JSON IR 文档。
4. 审核人员校验返回的 `rc` 值是否符合预期监管类别。
5. 根据确认的分类路线确定后续资料准备清单。
6. 转入下一环节生成注册申报资料或启动市场准入流程。

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
