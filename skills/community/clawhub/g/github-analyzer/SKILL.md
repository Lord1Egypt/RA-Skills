---
name: github-analyzer
displayName: GitHub 项目分析助手
version: 1.0.0
description: >
  输入项目想法或 GitHub 链接，自动搜索相关开源项目，生成结构化分析报告（技术栈/优缺点/评分），
  并可下载评分最高的前3名代码包。支持意图搜索和直链分析两种模式。
author: antonia-sz
tags: [github, analysis, developer-tools, open-source, research]
---

# GitHub 项目分析助手 🔍

## 你能做什么

**模式一：意图搜索**
> "我想做一个 XXX 项目，帮我找找 GitHub 上有没有相关开源项目"

**模式二：直链分析**
> "帮我分析这几个项目：https://github.com/xxx/yyy https://github.com/aaa/bbb"

**模式三：对比分析**
> "帮我对比这几个项目，哪个更适合我的需求"

---

## 工作流程

### 模式一：意图搜索模式

1. 解析用户描述，提取 2-4 个核心关键词
2. 调用 GitHub Search API 搜索相关仓库（按 stars 降序，取 Top 10）
3. 过滤：排除 fork、归档、1年内未更新、stars < 50 的项目
4. 对每个项目调用 GitHub API 获取详情
5. AI 分析生成报告
6. 询问是否需要下载代码包

### 模式二：直链分析模式

1. 提取 URL 中的 owner/repo
2. 调用 GitHub API 获取仓库详情、README、语言统计
3. AI 分析生成报告
4. 询问是否需要下载代码包

---

## 报告格式

每个项目输出：

```
## [项目名](链接)

> 一句话描述

| 维度 | 详情 |
|------|------|
| ⭐ Stars | 12,345 |
| 🍴 Forks | 1,234 |
| 🔤 语言 | Python / TypeScript |
| 📅 最近更新 | 2024-01-15 |
| 📜 License | MIT |

### 核心功能
- 功能点1
- 功能点2
- 功能点3

### 优点 ✅
- ...

### 缺点 / 注意事项 ⚠️
- ...

### 适用场景
...

### 综合评分：8.5 / 10
评分依据：活跃度高（★★★★）、文档完善（★★★★）、社区活跃（★★★）、上手难度低（★★★★）
```

多个项目后附对比表格：

```
| 项目 | Stars | 语言 | 活跃度 | 文档 | 上手难度 | 综合分 |
|------|-------|------|--------|------|---------|--------|
```

---

## 下载功能

分析完成后询问用户是否下载：
- "需要下载评分最高的前3名代码包吗？"
- 用户确认后，执行 `python3 SKILL_DIR/scripts/download_repos.py <repo1> <repo2> <repo3>`
- 下载到 `~/Downloads/github-analyzer/` 目录
- 打包为 zip，告知文件路径

---

## 工具调用

```python
# 搜索 GitHub
exec: python3 SKILL_DIR/scripts/search_github.py "<query>" [--limit 10]

# 分析单个仓库
exec: python3 SKILL_DIR/scripts/analyze_repo.py "<owner/repo>"

# 批量下载
exec: python3 SKILL_DIR/scripts/download_repos.py "<owner/repo1>" "<owner/repo2>" ...
```

---

## 注意事项

- GitHub API 未认证时限速 60次/小时，认证后 5000次/小时
- 如有 `GITHUB_TOKEN` 环境变量则自动使用
- README 超长时只取前 3000 字符分析
- 项目极少时（<3个）告知用户并说明可能原因
