---
name: github-pr-knowledge-wiki-sync
description: GitHub PR 文档自动生成与知识库同步 — 自动抓取PR内容、分析代码变更、生成技术文档并同步到飞书/wiki。
category: 开发
triggers: PR文档, 自动生成文档, PR知识库同步, GitHub文档, 代码变更文档, PR总结
version: 1.0.0
author: OpenClaw Agent
tags:
  - github
  - documentation
  - automation
  - wiki
  - pr
  - feishu
dependencies:
  - github
  - summarize
  - feishu-wiki
  - code-review
---

# GitHub PR 文档自动生成与知识库同步

一条命令完成：**PR内容抓取 → 代码变更分析 → 技术文档生成 → 飞书Wiki/企业微信文档同步**。

## 核心价值

- **全自动**：只需提供一个 PR 链接，自动完成全流程
- **代码分析**：智能解读代码变更，提取新增/删除/修改的核心逻辑
- **多格式输出**：支持飞书 Wiki、企业微信文档、Markdown 三种格式
- **团队共享**：生成的文档自动发布到团队知识库，永久留存

## 适用场景

- 开发者合并 PR 后需要快速生成变更记录
- 技术负责人需要将代码变更同步到团队知识库
- 团队使用飞书或企业微信进行文档管理
- 需要为每次发布生成 changelog 文档

## 工作流程（4步）

```
Step 1 → 获取 PR 详情（github）
   ↓
Step 2 → 分析代码变更（code-review）
   ↓
Step 3 → 生成技术文档（summarize + AI 生成）
   ↓
Step 4 → 同步到知识库（feishu-wiki / wecom-doc）
```

## 使用方法

### 触发词

```
"生成PR文档 [PR链接]"
"PR知识库同步 [PR链接]"
"帮我写这个PR的变更文档"
"这个PR改了什么，帮我生成文档"
```

### 完整工作流

**Step 1：获取 PR 信息**
```bash
# 使用 github skill 获取 PR 详情
gh pr view <PR_NUMBER> --repo <OWNER/REPO> --json title,body,files,commits
```

**Step 2：分析变更文件**
```bash
# 获取变更文件列表
gh pr diff <PR_NUMBER> --repo <OWNER/REPO>
```

**Step 3：生成文档**
AI 综合以下信息生成结构化文档：
- PR 标题和描述
- 代码变更文件列表
- 关键代码片段
- Commit 历史

**Step 4：同步到知识库**

- **飞书 Wiki**：`feishu_wiki` → 在指定知识空间创建或更新文档
- **企业微信**：`wecom-doc` → 在指定文档库创建文档

## 输出文档结构

```markdown
# [PR标题]

## 📋 基本信息
- **仓库**：`owner/repo`
- **PR 编号**：#123
- **作者**：@username
- **合并时间**：2026-04-18
- **状态**：✅ Merged

## 📝 变更摘要
（AI 生成的简短摘要，1-3句话）

## 📂 变更文件
| 文件路径 | 变更类型 | 说明 |
|---------|---------|------|
| src/a.py | ✏️ 修改 | 核心逻辑更新 |

## 🔍 关键代码变更
（列出最重要的代码片段及说明）

## 📌 注意事项
- 需要关注的风险点
- 关联的 Issue 或依赖
```

## 注意事项

- 确保 `gh` CLI 已登录：`gh auth login`
- 飞书 Wiki 需要有目标知识空间的管理权限
- 企业微信文档需要已创建目标文档库
