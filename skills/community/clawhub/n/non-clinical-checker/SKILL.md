---
name: non-clinical-checker
title: "Medical Device Non-clinical Research Checker"
slug: non-clinical-checker
display_name: 医疗器械非临床研究判定器
display_name_en: Medical Device Non-clinical Research Checker
version: 1.0.1
category: medtech-reg
author: SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
description: 医疗器械非临床研究判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖 TH-MED-001 域（医疗器械全链路）。
description_zh: "医疗器械非临床研究判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖 TH-MED-001 域（医疗器械全链路）。"
description_en: "Medical device non-clinical research determination tool: zero-dependency decision support with JSON IR output (domain TH-MED-001, full device chain)."
tags: [医疗器械, 合规, 判定器, TH-MED-001, non-clinical-checker, medtech-reg]
classification:
  skillhub: ["medtech-reg", "medical-device", "compliance"]
  clawhub: ["productivity", "development", "search"]
  iso_25010: ["Functional suitability"]
read_when:
  - 研发立项初期依据 TH-MED-001 域规则判定研究阶段是否属非临床范畴
  - 临床/注册申报前验证已产生非临床数据的合规性与有效性
  - 审查内部设计方案是否存在违反官方规则的非临床实验安排
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
ai_protocol: true
spec: usk/1.0
interface:
  type: prompt
  entry_point: SKILL.md
  runtime: none
  call_pattern: prompt
output_schema:
  stdout: structured JSON IR
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
changelog: "1.0.1: Bilingual rewrite (EN-first) + read_when; risk_rationale ref neutralized; 1.0.0 initial"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# Medical Device Non-clinical Research Checker

## When to use
1. At R&D project initiation, use TH-MED-001 domain rules to quickly determine whether a research stage falls under non-clinical research.
2. Before clinical trial or registration submission, verify the compliance and validity of non-clinical data already produced.
3. When an R&D organization needs to review internal design plans for non-clinical arrangements that violate official rules.
4. Zero-dependency regulatory rule comparison for a specific device model, producing standardized determination recommendations.

## How to use
Documentation-type tool; no scripts to run. The user describes device parameters and target standard numbers in natural language; the system retrieves and logically matches against the built-in official rule library. Results are structured as JSON IR for direct parsing.

## Workflow
1. Provide the device model and the non-clinical research scope to evaluate.
2. The system silently loads TH-MED-001 rules and matches across conditions.
3. Logical determination: validate research-stage attributes and experiment conditions against official definitions.
4. Generate JSON IR with conclusion, cited clauses, and risk analysis.
5. Parse the result and confirm it meets the zero-dependency output format.
6. Revise the R&D plan or adjust inputs to close the compliance loop.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# 医疗器械非临床研究判定器

## 何时用
1. 研发立项初期，依据 TH-MED-001 域规则快速判定研究阶段是否属于非临床研究范畴。
2. 临床/注册申报前，辅助验证已产生非临床数据的合规性与有效性。
3. 审查内部设计方案是否存在违反官方规则的非临床实验安排。
4. 针对特定型号器械做零依赖法规规则比对，生成标准化判定建议。

## 用法
文档型工具，无需调用脚本或安装插件。用户以自然语言描述器械参数与目标标准号，系统基于内置官方规则库检索与逻辑匹配；结果以 JSON IR 结构化输出，可直接解析集成。

## 流程
提供型号与评估范围 → 系统加载 TH-MED-001 规则并匹配 → 按官方定义做合规校验 → 生成含结论/引用条款/风险点的 JSON IR → 解析确认格式 → 修正研发计划或调整输入闭环。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立安全扫描（TBD）。
