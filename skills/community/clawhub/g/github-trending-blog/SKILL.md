---
name: github-trending-blog
description: GitHub Trending 监控 → AI摘要分析 → 知识卡片生成 → 公众号技术博客一键创作，自动化技术内容生产工作流
category: AI
triggers: GitHub热门, 技术博客, 趋势追踪, 开发者内容, GitHub日报, 技术周报, 追踪开源趋势
---

# GitHub Trending Blog Pipeline

自动化技术内容生产工作流：从 GitHub Trending 监控到公众号技术博客发布的完整流水线。

## 业务场景

技术博主、内容创作者每天花 2-3 小时手动搜索 GitHub Trending、整理项目信息、撰写技术博客。本工作流将这个过程压缩到 10 分钟以内。

**典型场景：**
- "帮我写一篇关于今天 GitHub Trending Python 项目的技术博客"
- "追踪本周 Rust 热门项目，生成周报"
- "分析某个 GitHub 仓库，生成配图卡片"

## 工作流步骤

### Step 1: GitHub Trending 数据采集 (`github`)
使用 `gh api` 采集 GitHub Trending 页面的热门项目列表。

```bash
gh api graphql -f query='
{
  search(query: "stars:>1000 pushed:>2026-05-01", type: REPOSITORY, first: 20) {
    nodes { ... on Repository { nameWithOwner description stargazerCount primaryLanguage url } }
  }
}'
```

### Step 2: 项目详情摘要 (`summarize`)
对每个目标仓库的 README 和关键文件使用 `summarize` 提取核心信息。

```bash
summarize "https://github.com/owner/repo" --extract-only
```

### Step 3: 开发者知识卡片生成 (`card-renderer`)
将分析结果渲染为精美的开发者风格知识卡片（支持 Mac Pro / VS Code / 赛博朋克等多种风格）。

```bash
python3 /root/.openclaw/workspace/skills/card-renderer/scripts/render_vscode_card.py \
  "项目名称" "一行简介" "/tmp/readme_summary.md" "/tmp/output/"
```

### Step 4: 技术博客撰写 (`wechat-article-pro`)
生成 3000-5000 字刘润风格技术博客，包含开篇洞察 + 案例分析 + 结论建议。

### Step 5: 保存草稿
将文章保存为 Markdown 文件，完成整个工作流。

## 输出产物

```json
{
  "repos_discovered": 20,
  "selected_repo": "owner/repo",
  "summary": "项目核心价值描述",
  "card_path": "/tmp/output/cover.png",
  "blog_path": "/tmp/blog_article.md",
  "language": "Python",
  "stars": "5000+",
  "key_insights": ["洞察1", "洞察2", "洞察3"]
}
```

## 技能编排图谱

```
[GitHub Trending] 
      ↓ github (数据采集)
[项目列表 + Stars + 语言]
      ↓ summarize (AI摘要)
[README核心内容 + 关键特性]
      ↓ card-renderer (可视化)
[开发者风格知识卡片]
      ↓ wechat-article-pro (文章创作)
[3000-5000字技术博客]
      ↓ 文件保存
[完整产出物]
```

## 依赖技能

- **github** — GitHub API 采集 Trending 数据
- **summarize** — URL/文档 AI 摘要
- **card-renderer** — 开发者风格知识卡片生成
- **wechat-article-pro** — 公众号技术博客撰写

## 注意事项

- GitHub API 有速率限制，建议每次采集间隔 >1 分钟
- 公众号草稿需用户手动在 mp.weixin.qq.com 发布
- 卡片渲染建议使用 `render_vscode_card.py` 风格（开发者最友好）
