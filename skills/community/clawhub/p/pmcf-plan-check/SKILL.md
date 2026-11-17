---
name: pmcf-plan-check
title: "PMCF Plan Completeness Checker"
slug: pmcf-plan-check
display_name: PMCF 计划完整性检查器
display_name_en: PMCF Plan Completeness Checker
version: 1.0.1
agent_created: true
author: SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, Task
category: medtech-reg
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description: PMCF 计划完整性检查器 — PMCF 计划写了一半交上去，公告机构说缺方法缺终点缺统计考量，来回补件三个月（零依赖，确定性输出，rc=0/1/2，--json 机器可读）。
description_zh: "PMCF 计划完整性检查器：查 PMCF 计划是否缺方法/终点/统计考量，避免公告机构多次补件延期（零依赖，确定性 JSON IR，rc=0/1/2，--json）。"
description_en: "Check PMCF plan completeness: methods, endpoints and statistical considerations, avoiding months of notified-body refill cycles (zero-dependency, deterministic JSON IR, rc=0/1/2, --json)."
classification:
  skillhub: ["medtech-reg", "medical-device", "post-market"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Functional suitability"]
read_when:
  - PMCF 计划初稿缺关键方法定义/终点考量/统计分析，需避免公告机构多次补件
  - 正式提交公告机构前快速校验文档是否具备完整合规要素
  - 零依赖环境需确定性输出(rc=0/1/2)做自审查
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [pmcf-plan-check, 医疗器械合规, PMCF, medtech-reg]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/pmcf_plan_check.py
  runtime: python3
  call_pattern: args
output_schema:
  stdout: structured JSON IR
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
changelog: "1.0.1: Bilingual rewrite (EN-first) + read_when/classification; risk_rationale ref neutralized; 1.0.0 initial"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# PMCF Plan Completeness Checker

## When to use
When a PMCF plan draft is missing key method definitions, endpoint considerations, or statistical analysis, and you want to avoid months of notified-body refill cycles. Use in a zero-dependency environment that needs deterministic output (rc=0/1/2) for self-review before formal submission.

## How to use
Run `python scripts/pmcf_plan_check.py --input plan.json --json --rc_level 1`. Use `--input_file` for the path, `--output_format json` for machine-readable results, and `--required_rc` to set the target compliance level.

## Workflow
1. Prepare the PMCF plan draft as input.
2. Run `python scripts/pmcf_plan_check.py` with correct args.
3. Read the rc code and listed missing items (deterministic, no randomness).
4. If non-zero, record gaps, fix the doc, and re-run.
5. Confirm final output is machine-readable and archive-ready.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# PMCF 计划完整性检查器

## 何时用
PMCF 计划初稿已完成但缺关键方法定义、终点考量或统计分析数据，需避免公告机构多次补件延期；零依赖环境需确定性输出(rc=0/1/2)做自审查时使用。

## 用法
执行 `python scripts/pmcf_plan_check.py --input plan.json --json --rc_level 1`。`--input_file` 指定路径，`--output_format json` 取机器可读结果，`--required_rc` 设定目标合规等级。

## 流程
准备计划草案 → 运行脚本传参校验 → 读 rc 码与缺失项清单（确定性）→ 非零则记录差异修复后重跑 → 确认机器可读可归档。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立安全扫描（TBD）。
