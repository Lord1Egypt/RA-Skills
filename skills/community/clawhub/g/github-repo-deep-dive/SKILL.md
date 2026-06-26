---
name: github-repo-deep-dive
description: GitHub 仓库深度技术解读 — 输入任意开源项目 URL，一键生成架构分析、代码洞察、知识卡片和多平台发布报告。
category: 开发
triggers: 分析仓库, 解读项目, 架构分析, GitHub项目调研, 技术尽调, 项目分析, repo分析, 架构解读
---

# GitHub Repo Deep Dive

输入任意 GitHub 仓库 URL，自动完成技术架构分析、核心代码解读、文档摘要，并生成可视化知识卡片和多平台发布内容。

## 适用场景

- 开源项目技术选型调研
- 竞品技术架构分析
- 新人上手项目快速了解
- 技术博客/公众号素材积累
- 工程团队技术雷达构建

## 依赖技能

| 技能 | 作用 |
|------|------|
| `github` | 获取仓库元数据、文件结构、Stars/PRs 数据 |
| `summarize` | 深度摘要 README 和关键文档 |
| `Agent-Reach` | 搜索项目评价、使用场景、社区讨论 |
| `card-renderer` | 生成小红书风格架构解读知识卡片 |

## 工作流程

```
Step 1 → github
  │  gh repo view owner/repo
  │  gh api repos/owner/repo --jq '.description, .language, .stargazers_count'
  │  → 输出：仓库基本信息、语言、Star数、描述
  │
  ▼
Step 2 → github
  │  gh api repos/owner/repo/contents --jq '.[].name'
  │  → 输出：根目录文件列表
  │
  ▼
Step 3 → summarize
  │  summarize "https://github.com/owner/repo" --model google/gemini-3-flash-preview
  │  → 输出：README 深度摘要、技术亮点总结
  │
  ▼
Step 4 → Agent-Reach
  │  搜索项目在 Twitter、Reddit、GitHub Discussions 的评价
  │  → 输出：社区反馈、用户场景、使用痛点
  │
  ▼
Step 5 → github
  │  分析 package.json / requirements.txt / Cargo.toml 等依赖文件
  │  → 输出：技术栈判定、关键依赖列表
  │
  ▼
Step 6 → card-renderer
  │  生成「架构解读」风格知识卡片（Mac Pro 极客风）
  │  → 输出：封面图 + 详情页图
  │
  ▼
Step 7 → github
  │  生成 Markdown 格式完整分析报告
  │  → 输出：结构化技术报告文档
```

## 快速开始

### 分析单个仓库
```
输入：https://github.com/tensorflow/tensorflow
```

系统自动完成：
1. 获取仓库基本信息（语言、Star、描述）
2. 读取 README 并生成深度摘要
3. 分析核心文件结构和技术栈
4. 搜索社区讨论和用户评价
5. 生成架构知识卡片
6. 输出完整 Markdown 分析报告

### 批量分析多个仓库（对比场景）
```
输入：[vercel/next.js, remix-run/react-router, astro/astro]
```

生成并排对比报告，包含：
- 技术栈对比表
- Stars / Fork 对比
- 架构风格对比
- 适用场景总结

## 输出示例

### 知识卡片内容结构

**封面**
- 项目名称 + 一句话定位
- Star 数 / 语言 / 架构风格标签
- 技术雷达（核心依赖）

**详情页**
- 项目简介
- 核心架构模式
- 技术栈详解
- 优缺点分析
- 社区反馈摘要
- 适用场景建议

## 命令行使用

```bash
# 方式一：直接分析（由 Agent 执行）
gh repo view owner/repo --json name,description,language,stargazerCount

# 方式二：获取文件树
gh api repos/owner/repo/contents --jq 'map({name, type})'

# 方式三：获取 README
gh api repos/owner/repo/readme --jq '.content' | base64 -d
```

## 注意事项

- 部分私有仓库内容可能无法获取
- 卡片渲染建议使用 Mac Pro 极客风风格，契合技术内容调性
- 分析完成后建议保存报告到飞书 Wiki 或 Obsidian 知识库
