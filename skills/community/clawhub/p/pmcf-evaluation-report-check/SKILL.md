---
name: pmcf-evaluation-report-check
title: "PMCF Evaluation Report Completeness Checker"
slug: pmcf-evaluation-report-check
display_name: PMCF 评价报告完整性检查器
display_name_en: PMCF Evaluation Report Completeness Checker
version: 1.0.1
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
author: SynomosAI
copyright: SynomosAI
category: medtech-reg
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
description: PMCF 评价报告完整性检查器——报告交上去还是被退，少一节「所采取措施」或少一次年度周期就得重来（零依赖，确定性 JSON IR，rc=0/1/2，--demo 自带案例）。
description_zh: "PMCF 评价报告完整性检查器：报告被退常因缺「所采取措施」章节或缺年度周期计数；提交前预检（零依赖，确定性 JSON IR，rc=0/1/2，--demo 自带案例）。"
description_en: "PMCF evaluation report completeness checker: reports are often rejected for missing 'measures taken' sections or annual-cycle counts; pre-check before filing (zero-dependency, deterministic JSON IR, rc=0/1/2, demo case included)."
classification:
  skillhub: ["medtech-reg", "medical-device", "post-market"]
  clawhub: ["productivity", "development", "search"]
  iso_25010: ["Functional suitability"]
read_when:
  - PMCF 报告已提交但被退，提示缺「所采取措施」章节
  - 计划执行完毕但年度周期统计缺失或不满足计数标准
  - 正式归档前对草案做合规预检确保过自动审核
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [pmcf-evaluation-report-check, 医疗器械合规, PMCF, medtech-reg]
ai_protocol: true
spec: usk/1.0
interface:
  type: prompt
  entry_point: SKILL.md
  runtime: none
  call_pattern: prompt
output_schema:
  stdout: structured JSON IR
  exit_code: rc=0 pass / rc=1 missing section / rc=2 bad input
changelog: "1.0.1: Bilingual rewrite (EN-first) + read_when/classification; copyright/platform refs neutralized; 1.0.0 initial"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# PMCF Evaluation Report Completeness Checker

## When to use
- A PMCF evaluation report was submitted and rejected, with a missing "measures taken" section.
- The plan executed but annual-cycle counts are missing or below the required threshold.
- Pre-filing compliance pre-check of a draft to pass automated review.

## How to use
- Input: text or JSON IR report data.
- Optional `--demo` runs a built-in test case.
- Returns an integer rc: 0 pass, 1 or 2 for different missing-item errors.
- Pure documentation tool; no external scripts.

## Workflow
1. Standardize the PMCF content as JSON IR or a text draft.
2. Choose whether to enable `--demo`.
3. Submit the validated data structure and parameters.
4. Read the returned rc for the compliance verdict.
5. If non-zero, interpret whether a section or annual-cycle step is missing.
6. Fill gaps and resubmit until pass.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# PMCF 评价报告完整性检查器

## 何时用
- PMCF 报告已提交但被退，提示缺「所采取措施」章节。
- 计划执行完毕但年度周期统计缺失或不满足计数标准。
- 正式归档前对草案做合规预检确保过自动审核。

## 用法
- 输入：文本或 JSON IR 报告数据。
- 可选 `--demo` 跑内置案例。
- 返回整数 rc：0 通过，1 或 2 对应不同缺失项。
- 纯文档型工具，无外部脚本。

## 流程
将 PMCF 内容标准化为 JSON IR 或文本草案 → 决定是否启用 --demo → 提交规范数据结构与参数 → 读 rc 判断合规性 → 非零时定位缺章节还是缺年度周期 → 补全后重交至通过。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立安全扫描（TBD）。
