---
name: code-review
source: eo-native
compatibility: full
description: 代码审查指令，调度 CodeReviewer 专家进行代码质量、安全和性能审查
whenToUse: 当需要进行代码审查、安全检查、性能优化时使用
allowedTools: ["Read", "Grep", "Glob", "Bash"]
context: inline
expert: code-reviewer
aliases: ["/code-review", "/review", "/cr"]
version: 1.0.1
---

# /code-review - 代码审查指令

> **v1.0.1 新增**: frontmatter 标准化，包含 expert 映射和 allowedTools

## 功能
调度 CodeReviewer 专家，对代码进行质量、安全、性能审查。

## 参数
```
/code-review <路径> [options]

参数:
  <路径>          必填，要审查的代码路径
  --scope <范围>  可选，审查范围
                  值: security | performance | style | full
                  默认: full
  --rules <规则> 可选，规则级别
                  值: strict | standard | loose
                  默认: standard
  --format <格式> 可选，输出格式
                  值: json | markdown | console
                  默认: markdown
```

## 执行流程

1. **解析参数** - 提取路径和选项
2. **确定审查范围** - security/performance/style/full
3. **加载 CodeReviewer 专家** - 读取相关 prompt
4. **Spawn 子Agent** - 执行代码审查
5. **输出报告** - 结构化的审查报告

## 输出格式

```markdown
# 👁️ 代码审查报告

## 📍 审查目标
`/path/to/code`

## 📊 审查范围
- [x] Security (安全)
- [x] Performance (性能)
- [ ] Style (风格)

## 🔍 发现问题

### 🔴 高危 (N项)
1. **[SQL注入]** `file:line` - 建议使用参数化查询
2. **[XSS]** `file:line` - 建议转义用户输入

### 🟡 中危 (N项)
1. **[性能]** `file:line` - 建议添加索引

### 🟢 建议 (N项)
1. 命名规范 - `file:line`

## 📈 质量评分
| 维度 | 分数 |
|------|------|
| 安全性 | 85/100 |
| 性能 | 78/100 |
| 可维护性 | 90/100 |
| 整体 | 84/100 |

## 💡 优化建议
[N条具体优化建议]
```

## 示例

```
用户: /code-review "~/project/src --scope security --rules strict"

我:
1. 解析 → 路径 ~/project/src, scope=security, rules=strict
2. 加载 Security CodeReviewer 专家
3. spawn 子Agent 执行审查
4. 输出安全审查报告
```

## 对应专家
- CodeReviewer (代码审查)
- SecurityReviewer (安全审查，如 scope=security)
- 关联 skill: `coding-standards`, `security-review`
