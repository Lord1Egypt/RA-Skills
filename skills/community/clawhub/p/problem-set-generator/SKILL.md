---
name: problem-set-generator
slug: problem-set-generator
displayName: 赛事赛题生成器
version: 1.1.1
category: ai-agent
display_name: 赛事赛题生成器
title: 赛事赛题生成器
author: 诺声(SynomosAI)
author_note: '"SynomosAI" / "SynomosAI" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事赛题生成器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-002域。 适用场景：当需要赛事赛题生成器能力时使用本技能；触发词：赛事、判定器、TH-EVT-002、problem-set-generator。
tags: [赛事, 判定器, TH-EVT-002, problem-set-generator, 赛题生成, UIBC]
description_zh: "赛事赛题生成器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-002域。"
description_en: "Contest problem-set generator: zero-dependency decision support with JSON IR output (UIBC spec, domain TH-EVT-002)."
read_when:
  - 筹备 UIBC 竞赛要快速生成符合官方规范的题目
  - 工作流要求结构化输出而非自然语言
  - 需按 TH-EVT-002 领域标准产出赛题
  - 无外部脚本库/文件/代码执行环境的自动化场景
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
  entry_point: problem-set-generator.py
  runtime: python3
  call_pattern: args
input_schema:
  theme:
    type: string
    description: "赛题主题(默认 迁移的判定与问责)"
    required: false
  difficulty:
    type: string
    description: "难度: easy/mid/hard"
    required: false
  count:
    type: string
    description: "生成数量 1-10"
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
  - education
  - problem-set
  - generation
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
1. While preparing UIBC-related contests, when you need to quickly produce problem content that complies with official contest rules.
2. When the workflow requires structured data output rather than natural-language description, and must strictly follow the TH-EVT-002 domain standard.
3. In automated decision-support scenarios where external script libraries, files or code-execution environments are unavailable.

### Usage
Pass parameter configurations directly through the skill interface; no local scripts or config files need to be loaded. Core inputs: `domain` specifying the TH-EVT-002 domain, `difficulty_level` setting the difficulty tier, and `output_format` forcing JSON IR return. The skill directly generates format-compliant JSON blocks without extra file operations or script parsing.

### Workflow
1. Confirm the current task context matches UIBC generation needs; define the target problem domain and count.
2. Initialize input variables per the parameter contract; ensure `output_format` points to JSON IR.
3. Invoke the skill and emphasize TH-EVT-002 compliance constraints in the prompt.
4. Receive the returned raw data and verify its structure against the preset IR schema.
5. Feed the generated JSON into downstream workflows, or perform field extraction and completeness checks.
6. Deliver the problem set; ensure the whole run is zero-dependency and spec-compliant.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.1.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 在筹备 UIBC 相关竞赛时，需要快速生成符合赛事官方规范的题目内容。
2. 当工作流要求输出结构化数据而非自然语言描述，且需严格遵循 TH-EVT-002 领域标准时。
3. 在进行自动化决策支持场景下，当前无法依赖外部脚本库、文件或代码执行环境时。

### 用法
通过调用该技能接口直接传入参数配置，无需加载本地脚本或配置文件。核心输入包含：`domain` 指定 TH-EVT-002 相关领域，设置 `difficulty_level` 定义难度等级，配置 `output_format` 强制返回 JSON IR。技能将直接生成符合格式的 JSON 数据块，无需用户进行额外的文件操作或脚本解析。

### 流程
1. 确认当前任务上下文符合 UIBC 赛事生成需求，明确目标赛题领域与数量。
2. 根据参数要求初始化输入变量，确保 `output_format` 指向 JSON IR 格式。
3. 发送指令调用技能，并在提示词中强调 TH-EVT-002 领域的合规性约束。
4. 接收系统返回的原始数据，验证其结构是否符合预设的 IR Schema 标准。
5. 将生成的 JSON 数据导入后续工作流，或进行必要的字段提取与完整性检查。
6. 完成问题集交付，确保整个过程为零依赖运行且符合规范输出要求。

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
