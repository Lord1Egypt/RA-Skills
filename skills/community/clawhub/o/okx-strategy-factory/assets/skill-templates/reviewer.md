---
name: <skill-name>
description: "<描述：审查/评审特定领域的内容，按检查清单输出分级结果。包含触发关键词。>"
license: Apache-2.0
metadata:
  author: <作者>
  version: "<major.minor.patch>"
  pattern: "reviewer"
  severity-levels: "error,warning,info"
---

# <Skill 名称> (Reviewer)

<!--
Reviewer 模式：分离"检查什么"和"如何检查"。
references/review-checklist.md 存放模块化评分标准。
指令定义检查流程和输出格式。

核心思路：
- "检查什么" 定义在 references/review-checklist.md（可独立维护）
- "如何检查" 定义在 SKILL.md 的 Instructions 中
- 输出按严重程度分组：error → warning → info
-->

一句话概述：审查 <目标类型>，按检查清单输出分级发现。

## Architecture

```
Input (code / doc / strategy / config)
    ↓
Load Checklist (references/review-checklist.md)
    ↓
For each checklist item:
    Check → Classify severity → Record finding
    ↓
Group by severity → Format output
    ↓
Summary + Recommendations
```

## Instructions

### Step 1: Load Review Checklist

```
LOAD references/review-checklist.md
Each checklist item has:
- ID: unique identifier (e.g., SEC-001)
- Category: grouping (e.g., Security, Performance)
- Check: what to verify
- Severity: default level if failed (error | warning | info)
- Fix: recommended remediation
```

### Step 2: Execute Review

```
For each item in checklist:
1. Apply the check to the input
2. Record result: PASS | FAIL
3. If FAIL: use the item's severity level
4. Collect evidence (line numbers, quotes, metrics)
```

### Step 3: Classify Findings

| Severity | Meaning | Action Required |
|---|---|---|
| `error` | 必须修复，阻塞发布/部署 | 立即处理 |
| `warning` | 应该修复，但不阻塞 | 计划处理 |
| `info` | 建议改进，可选 | 酌情处理 |

### Step 4: Output Report

```markdown
## Review Summary

- Errors: N
- Warnings: N
- Info: N
- Pass rate: X%

## Errors (must fix)

### [SEC-001] <检查标题>
- **Finding**: <具体发现>
- **Evidence**: <证据（行号、引用）>
- **Fix**: <修复建议>

## Warnings (should fix)

### [PERF-003] <检查标题>
...

## Info (nice to have)

### [STYLE-002] <检查标题>
...
```

### Severity Override Rules

<!-- 定义何时升级/降级严重程度 -->

```
- If <condition>: upgrade <ID> from warning → error
- If <condition>: downgrade <ID> from error → warning
- Context: <context that affects severity>
```

## Review Checklist Format

<!-- 这是 references/review-checklist.md 的格式规范 -->

```markdown
## <Category>

### <ID>: <Check Title>
- **Check**: <检查内容的具体描述>
- **Severity**: error | warning | info
- **Pass criteria**: <通过条件>
- **Fix**: <修复建议>
```

## Directory Structure

```
<skill-name>/
├── SKILL.md                        # 主文件：检查流程 + 输出格式
└── references/
    ├── review-checklist.md          # 检查清单（模块化，可独立维护）
    ├── <domain-standards>.md        # 领域标准（如安全规范）
    └── <scoring-rubric>.md          # 评分标准（如果需要打分）
```

## Anti-Patterns

| Pattern | Problem |
|---|---|
| 检查逻辑和检查清单混在一起 | 无法独立维护清单 |
| 不分级，所有发现同等对待 | 用户无法区分优先级 |
| 只列问题不给修复建议 | 审查没有可操作性 |
| 缺少证据/行号 | 用户找不到问题位置 |
| 检查清单太大不分类 | 难以导航和维护 |
