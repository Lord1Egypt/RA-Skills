---
name: <skill-name>
description: "<描述：按需加载特定 API/库的上下文，作为绝对真理指导 agent 操作。包含触发关键词。>"
license: Apache-2.0
metadata:
  author: <作者>
  version: "<major.minor.patch>"
  pattern: "tool-wrapper"
---

# <Skill 名称> (Tool Wrapper)

<!--
Tool Wrapper 模式：按需加载特定库/API 的上下文。
SKILL.md 监听关键词，从 references/ 目录动态加载文档，作为绝对真理应用。

核心思路：
- references/ 目录存放 API 规范、SDK 文档、类型定义
- 指令告诉 agent 何时加载哪个 reference
- 加载后的内容覆盖 agent 的先验知识
-->

一句话概述：封装 <API/库> 的操作接口，提供精确的上下文加载。

## Architecture

```
User Request
    ↓
Keyword Match → 加载 references/<relevant>.md
    ↓
Agent + Loaded Context → 执行操作
    ↓
Structured Output
```

**依赖的外部服务/Skill**:
- <API/库名>: `<调用方式>` -> `<具体命令>`

## Trigger Keywords

<!-- 列出触发此 Skill 的关键词，用于 agent 路由 -->

| Keyword / Pattern | Load Reference | Description |
|---|---|---|
| `<keyword-1>` | `references/<file1>.md` | <何时加载> |
| `<keyword-2>` | `references/<file2>.md` | <何时加载> |
| `<keyword-3>` | `references/<file1>.md, references/<file2>.md` | <组合加载> |

## Instructions

When the user mentions any trigger keyword:

1. **Load Context**: Read the corresponding reference file(s) from `references/` directory
2. **Apply as Ground Truth**: Treat loaded content as the authoritative specification — override any prior knowledge that conflicts
3. **Execute**: Follow the API/library conventions exactly as documented
4. **Validate**: Check output against the reference specification before returning

<!--
关键原则：
- Reference 文件是绝对真理，覆盖 agent 的训练知识
- 只加载需要的 reference，不要一次全加载（节省 context window）
- 如果用户请求与 reference 矛盾，以 reference 为准并告知用户
-->

### Context Loading Rules

```
IF user mentions <keyword-1>:
    LOAD references/<file1>.md
    APPLY as ground truth for <specific domain>

IF user mentions <keyword-2>:
    LOAD references/<file2>.md
    APPLY as ground truth for <specific domain>

IF task requires both:
    LOAD both, <file1>.md takes precedence on conflicts
```

### Core Operations

<!-- 列出此 Skill 封装的核心操作 -->

| Operation | Command / API | Input | Output |
|---|---|---|---|
| `<op-1>` | `<command>` | <输入参数> | <返回格式> |
| `<op-2>` | `<command>` | <输入参数> | <返回格式> |

### Error Handling

```python
# 统一错误格式
failure_info = {
    "reason": str,      # 机器可读
    "detail": str,      # 人类可读上下文
    "retriable": bool,  # 是否可自动重试
    "hint": str         # 提示
}
```

## Directory Structure

```
<skill-name>/
├── SKILL.md                    # 主文件：触发规则 + 指令
└── references/                 # API 规范和文档（绝对真理）
    ├── <api-spec>.md           # API 端点、参数、返回值
    ├── <type-definitions>.md   # 类型定义、枚举值
    └── <error-codes>.md        # 错误码和处理方式
```

## Anti-Patterns

| Pattern | Problem |
|---|---|
| 一次加载所有 references | 浪费 context window，降低精度 |
| 忽略 reference 与先验知识的冲突 | Reference 是真理，必须覆盖 |
| Reference 文件太大（>2000行） | 拆分为更细粒度的文件 |
| 把执行逻辑写在 reference 里 | Reference 只存事实，指令写在 SKILL.md |
