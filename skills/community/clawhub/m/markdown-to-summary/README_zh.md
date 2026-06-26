# Markdown To Summary

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 将长篇 Markdown 文档提炼为简洁摘要 — 保留关键事实，删除冗余内容

## 解决什么问题

长的 README、文章或文档需要花几小时而不是几分钟理解。这个技能识别文档类型（技术文档、文章、会议记录、变更日志）并提取关键要点，同时保持技术准确性。

**触发条件：** Markdown 文本 + 摘要/精简/tl;dr 意图。

## 功能特性

- **文档类型检测** — 自动识别 README、文章、会议记录或变更日志并调整策略
- **保持技术准确性** — 保留准确的版本号、命令、路径和 URL
- **长度控制** — 输出原文的 20-40%，除非用户另有指定
- **结构化输出选项** — 散文段落、项目符号列表或单句 tl;dr

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install markdown-to-summary

# 或手动复制
cp -r markdown-to-summary ~/.openclaw/skills/
```

### 使用方法

```
/markdown-to-summary
```

粘贴 Markdown 并要求摘要。

```
/markdown-to-summary/bullet
```

输出要点为快速浏览的项目符号列表。

```
/markdown-to-summary/tl-dr
```

绝对最短版本：一句话 + 一段。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/markdown-to-summary` | 简洁散文摘要，原文的 ~20-30% |
| `/markdown-to-summary/bullet` | 关键要点作为结构化项目符号 |
| `/markdown-to-summary/tl-dr` | 绝对最短：一句话 + 一段 |

## 示例

| 输入 | 输出 |
|------|------|
| 2000 词的 README | 保留：前提条件、关键命令、架构。删除：安装闲聊 |
| 20 条目的变更日志 | 分组：3 个功能，5 个修复，1 个破坏性变更 |
| 带代码示例的 API 文档 | 代码块作为参考保留，周围的文本摘要 |
| 有题外话的文章 | 跳过题外话，保留主要论点和论据 |

## 目录结构

```
markdown-to-summary/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # 文档类型分类、长度指南
└── tests/
```

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。