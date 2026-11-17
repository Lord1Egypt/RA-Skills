---
name: md-link-audit
title: "Markdown Link Auditor"
slug: md-link-audit
display_name: Markdown 链接体检器
display_name_en: Markdown Link Auditor
description: Markdown 链接体检器 — README 里链接一堆 404、改了路径没人发现，CI 上还老因为外网检查超时误报（零依赖，确定性输出，rc=0/1/2，--json 机器可读）。
description_zh: "Markdown 链接体检器：查 README/Wiki/技术手册里的 404 与路径漂移，CI 友好的外网超时处理（零依赖，确定性输出，rc=0/1/2，--json）。"
description_en: "Audit Markdown links for 404s and path drift, with CI-friendly external-link timeout handling (zero-dependency, deterministic output rc=0/1/2, --json machine-readable)."
version: 1.0.1
agent_created: true
author: SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write
category: 效率工具
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
classification:
  skillhub: ["productivity", "documentation"]
  iso_25010: ["Maintainability", "Usability"]
read_when:
  - 本地文档发布前自查 README/Wiki/手册里的失效链接
  - CI/CD 中替代易因外网超时误报的传统链接检查
  - 项目路径重构后验证文档引用是否指向新位置
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [md-link-audit, 效率工具, 链接检查, CI]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/md_link_audit.py
  runtime: python3
  call_pattern: args
output_schema:
  stdout: structured JSON IR (result / rc / error_code / warnings)
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
capabilities: [documentation, link-check]
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (EN-first) + read_when/classification; legacy author/platform refs neutralized; 1.0.0 initial"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# Markdown Link Auditor

## When to use
1. Before publishing local docs, quickly self-check README/Wiki/technical manuals for dead links.
2. In CI/CD, replace traditional link checkers that false-positive on external-network timeouts.
3. After a project path refactor, verify doc references point to the new locations.

## How to use
Run `python scripts/md_link_audit.py <input_file>`; it also reads stdin. Add `--json` for machine-readable output. Use the return code (rc 0/1/2) to set strictness and the pass threshold.

## Workflow
1. Prepare the Markdown path and runtime.
2. Pass the file argument or pipe stdin into auto-parse mode.
3. Run the auditor and wait for results/log.
4. Check console output for link status and errors.
5. Inspect rc to judge whether the result meets zero-fault expectations.
6. If non-zero, record dead paths and fix or skip.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# Markdown 链接体检器

## 何时用
1. 本地文档发布前，快速自查 README、Wiki 或技术手册中是否存在失效链接。
2. CI/CD 构建场景中，替换易受外部网络波动影响且导致超时误报的传统检测工具。
3. 项目路径重构时，验证历史及新代码中的文档引用是否准确指向新位置。

## 用法
执行 `python scripts/md_link_audit.py <input_file>`，支持读标准输入流；加 `--json` 输出机器可读格式；用返回码 rc(0/1/2) 定义检查严格程度与通过阈值。

## 流程
准备文件路径 → 传入参数或 stdin 自动解析 → 运行审计 → 核对链接状态与错误详情 → 按 rc 判断是否零故障 → 非零则记录失效路径并修正。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立安全扫描（TBD）。
