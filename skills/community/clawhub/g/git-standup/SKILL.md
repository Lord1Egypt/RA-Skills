---
name: git-standup
description: 分析 Git 提交自动生成工作日报
author: openclaw
version: 1.0.0
commands:
  /daily-standup: 生成指定日期范围的工作日报
---

# Git Standup — 自动化工作日报生成

自动分析 Git 提交历史，生成结构化的工作日报。

## 功能特性

- 📅 按日期范围筛选提交
- 👤 支持多作者筛选
- 📁 按仓库/目录分组
- 🏷️ 智能分类（功能/修复/重构/文档）
- 📝 生成 Markdown 格式日报
- 🔗 自动关联 issue/PR 链接

## 使用方法

### 生成今日日报

```bash
/daily-standup
```

### 生成指定日期日报

```bash
/daily-standup --date 2026-03-10
```

### 生成周报

```bash
/daily-standup --since "1 week ago"
```

### 指定作者

```bash
/daily-standup --author "username"
```

### 多仓库汇总

```bash
/daily-standup --repos /path/to/project1,/path/to/project2
```

## 选项说明

| 选项 | 说明 |
|------|------|
| `--date` | 指定日期（默认今天） |
| `--since` | 起始时间（Git 日期格式） |
| `--until` | 结束时间 |
| `--author` | 按作者筛选 |
| `--repos` | 指定多个仓库路径 |
| `--format` | 输出格式（markdown/json） |
| `--output` | 输出文件路径 |
| `--group-by` | 分组方式（repo/type/date） |

## 输出示例

```markdown
# 工作日报 - 2026-03-10

## 项目: my-project

### ✨ 新功能
- [feat] 添加用户登录功能 (#123)
- [feat] 实现数据导出功能 (#124)

### 🐛 修复
- [fix] 修复登录页面样式问题 (#125)

### ♻️ 重构
- [refactor] 优化数据库查询性能 (#126)

### 📝 文档
- [docs] 更新 API 文档 (#127)

## 统计
- 提交次数: 5
- 涉及文件: 12
- 新增行数: +245
- 删除行数: -38
```

## 提交信息规范

工具会解析符合以下格式的提交信息：

```
[type] 描述 (#issue)

类型:
- feat: 新功能
- fix: 修复
- refactor: 重构
- docs: 文档
- test: 测试
- chore: 杂项
```

## 高级用法

```bash
# 生成周报并保存
/daily-standup --since "1 week ago" --output weekly-report.md

# 多作者汇总
/daily-standup --author "author1|author2"

# JSON 格式输出
/daily-standup --format json

# 按类型分组
/daily-standup --group-by type
```
