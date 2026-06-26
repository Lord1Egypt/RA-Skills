---
name: <skill-name>
description: "<描述：生成一致结构的输出，如报告、配置、文档等。包含触发关键词。>"
license: Apache-2.0
metadata:
  author: <作者>
  version: "<major.minor.patch>"
  pattern: "generator"
  output-format: "markdown"
  # output-format: "json" | "yaml" | "code" | "markdown"
---

# <Skill 名称> (Generator)

<!--
Generator 模式：强制一致的输出结构。
用 assets/ 存输出模板，references/ 存风格指南。
指令协调检索并逐步填充。

核心思路：
- assets/ 目录存放输出模板（骨架）
- references/ 存放风格指南和约束规则
- 指令定义：加载模板 → 加载风格 → 询问缺失信息 → 填充 → 输出
-->

一句话概述：根据输入数据生成结构一致的 <输出类型>。

## Architecture

```
Input Data / User Request
    ↓
Load Template (assets/<template>.md)
    ↓
Load Style Guide (references/<style>.md)
    ↓
Check for Missing Variables → Ask User (if needed)
    ↓
Fill Template → Validate → Output
```

## Instructions

### Step 1: Load Template

```
LOAD assets/<output-template>.md
This defines the output skeleton — every section is REQUIRED unless marked [optional].
```

### Step 2: Load Style Guide

```
LOAD references/<style-guide>.md
Apply these rules to ALL generated content:
- Tone, voice, formatting constraints
- Domain-specific terminology
- Naming conventions
```

### Step 3: Collect Variables

<!-- 列出模板需要的所有变量 -->

| Variable | Source | Required | Default |
|---|---|---|---|
| `<var-1>` | User input | Yes | — |
| `<var-2>` | Auto-detect | No | `<default>` |
| `<var-3>` | User input | Yes | — |

**If any required variable is missing**: Ask the user before proceeding. Do NOT guess.

### Step 4: Fill Template

```
For each section in the template:
1. Substitute variables
2. Apply style guide rules
3. Validate against constraints (length limits, format rules, etc.)
```

### Step 5: Output

```
Output the filled template in <output-format> format.
If validation fails, report which sections need fixes.
```

## Template Variables Reference

<!-- 详细描述每个变量的格式要求 -->

### `<var-1>`
- Type: string
- Format: <格式描述>
- Constraints: <约束>
- Example: `<示例值>`

### `<var-2>`
- Type: string
- Format: <格式描述>
- Constraints: <约束>
- Example: `<示例值>`

## Directory Structure

```
<skill-name>/
├── SKILL.md                    # 主文件：生成流程指令
├── assets/                     # 输出模板（骨架）
│   ├── <output-template>.md    # 主输出模板
│   └── <variant-template>.md   # 变体模板（如不同格式）
└── references/                 # 风格指南和约束
    ├── <style-guide>.md        # 语气、格式、术语
    └── <constraints>.md        # 字数限制、必填字段等
```

## Anti-Patterns

| Pattern | Problem |
|---|---|
| 不加载模板直接生成 | 输出结构不一致 |
| 猜测缺失变量 | 输出内容不准确，应该问用户 |
| 模板里写死内容 | 模板应该是骨架+占位符，不是完整文档 |
| 风格指南太模糊 | "写得好一点" 没有用，要具体到格式规则 |
| 跳过验证步骤 | 输出可能不符合约束 |
