---
name: llms-generator
description: "Generate llms.txt (LLMs.txt v2 spec) and AI-discoverability packages for any project, so AI agents can find and read your assets. 为任意项目生成 llms.txt（LLMs.txt v2 规范）与 AI 可发现性包，让 AI 代理能找到并读懂你的资产。"
slug: llms-generator
title: llms-generator
version: 1.0.1
license: MIT
category: 效率
author: SynomosAI (LGD initiative)
platforms: [windows, macos, linux]
tags: [llms-generator,ai-discoverability,llms-txt,seo]
description_zh: "为任意项目生成 llms.txt（LLMs.txt v2 规范）与 AI 可发现性包，让 AI 代理能找到并读懂你的资产。"
description_en: "Generate llms.txt (LLMs.txt v2 spec) and AI-discoverability packages for any project, so AI agents can find and read your assets."
read_when:
  - 为项目生成 llms.txt 让 AI 代理可发现并读懂
  - 内置生态互链（ORCID/仓库/标准）或内联全文生成 llms-full
risk_tier: medium
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/llms_gen.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数（--name/--url/--desc/--link/--full/--out）透传给主脚本"
    required: false
output_schema:
  stdout:
    type: string
    description: "生成 llms.txt 文件，stdout 为生成结果摘要"
  exit_code:
    type: integer
    description: "0=正常生成；非 0=用法或运行错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### Why
AI agents discover projects via llms.txt / AGENTS.md. A project without llms.txt is half-blind to AI. This skill generates the spec file in one command.

### Capabilities
- Generates llms.txt per LLMs.txt v2 spec (H1 title + curated links).
- Embeds ecosystem links (awesome / ORCID / Zenodo / SWH / standards) for AI agents.
- Optionally inlines full markdown as llms-full.txt content.

### When to use
- Generate llms.txt for any project so AI agents can discover and read it.
- Add ecosystem links or inline full text for llms-full.

### Usage
```bash
python scripts/llms_gen.py --name MyProject --url https://github.com/org/repo --desc "..." [--link ...] [--full README.md]
```

### Flow
1. Run `llms_gen.py --name <name> --url <repo> --desc <one-liner> [--link ...] [--full README.md] [--out llms.txt]`.
2. The script emits v2 structure: H1 + quote desc + Ecosystem links + Identity & Archive (ORCID/repo); with `--full` it inlines the full text.
3. Writes `--out` (default llms.txt); generates only, never auto-publishes.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 背景
AI 代理通过 llms.txt / AGENTS.md 发现项目。没有 llms.txt 的项目对 AI 是"半盲的"。本技能一条命令生成规范文件。

### 功能
- 按 LLMs.txt v2 规范生成 llms.txt（H1 标题 + 精选链接）。
- 内置生态互链（awesome / ORCID / Zenodo / SWH / 标准）供 AI 代理读取。
- 可选内联全文作为 llms-full 内容。

### 何时用
- 当需要为任意项目生成 llms.txt（LLMs.txt v2 规范）让 AI 代理能发现并读懂项目时使用本技能。
- 当需要内置生态互链（ORCID/仓库/标准）或内联全文生成 llms-full 内容时使用本技能。

### 用法
```bash
python scripts/llms_gen.py --name MyProject --url https://github.com/org/repo --desc "..." [--link ...] [--full README.md]
```

### 流程
1. 运行 `python scripts/llms_gen.py --name <项目名> --url <仓库地址> --desc <一句话描述> [--link <生态互链，可重复>] [--full README.md] [--out llms.txt]`。
2. 脚本按 LLMs.txt v2 结构生成：H1 标题 + 引用描述 + Ecosystem 链接 + Identity & Archive（ORCID/仓库）；带 --full 时内联全文。
3. 写出 --out 指定的 llms.txt（默认 llms.txt）；只生成文件，不自动发布。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
