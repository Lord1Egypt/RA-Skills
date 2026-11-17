---
name: pms-vigilance-intake
title: "Medical Device Vigilance Reporting Pathway Intake"
slug: pms-vigilance-intake
display_name: 医疗器械不良事件报告路径判定器
display_name_en: Medical Device Vigilance Reporting Pathway Intake
version: 1.0.1
category: medtech-reg
author: SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
description: 医疗器械不良事件报告路径判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖 TH-MED-002 域（医疗器械全链路）。
description_zh: "医疗器械不良事件报告路径判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖 TH-MED-002 域（医疗器械全链路）。"
description_en: "Medical device adverse-event reporting pathway determination tool: zero-dependency decision support with JSON IR output (domain TH-MED-002, full device chain)."
tags: [医疗器械, 合规, 判定器, TH-MED-002, pms-vigilance-intake, medtech-reg, 不良事件]
classification:
  skillhub: ["medtech-reg", "medical-device", "pharmacovigilance"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Functional suitability"]
read_when:
  - 收到新提交的不良事件数据需自动判定法定报告路径
  - 多部门管辖的复杂事件初筛需按官方规则库合规分类
  - 需生成符合 JSON IR 标准、可被后续步骤直接解析的决策建议
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

# Medical Device Vigilance Reporting Pathway Intake

## When to use
1. When newly submitted adverse-event data arrives and its statutory reporting pathway must be determined.
2. For triaging complex events involving multi-department jurisdiction, classifying them against the official rule library.
3. When an automated flow needs JSON-IR-standard decisions parseable by downstream steps.

## How to use
Pure documentation tool; no local scripts. Pass structured adverse-event elements or a full report summary as input; the interface returns JSON IR with the recommended pathway and rationale.

## Workflow
1. Confirm the adverse-event data has been basic-validated and formatted.
2. Wrap the structured text as input into the skill node.
3. Trigger execution; the backend matches TH-MED-002 regulatory rules.
4. Inspect the returned JSON IR for the recommended pathway code and clauses.
5. Close the business loop or route for manual review.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# 医疗器械不良事件报告路径判定器

## 何时用
1. 收到新提交的不良事件数据，需自动判定其法定报告路径。
2. 涉及多部门管辖的复杂事件初筛，需按官方规则库合规分类。
3. 自动化流程需生成符合 JSON IR 标准、可被后续步骤直接解析的决策建议。

## 用法
纯文档型工具，无需本地执行脚本。以结构化不良事件要素列表或完整报告摘要为输入，返回含推荐路径与判定依据的 JSON IR。

## 流程
完成数据基础校验与格式化 → 封装为输入参数 → 触发执行并匹配 TH-MED-002 规则库 → 查看 JSON IR 中推荐路径代码与条款 → 闭环或转人工复核。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立安全扫描（TBD）。
