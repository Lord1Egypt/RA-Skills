---
name: github-trending
description: 获取 GitHub Trending 热门仓库列表。当用户要求查看 GitHub 热榜、每日 GitHub trending、推送 GitHub 热门项目时使用。支持可选语言过滤，返回结构化 JSON 由 agent 自行决定输出格式。
---

# GitHub Trending 数据获取

## 工作流程

1. **抓取 Trending 页面**：获取 GitHub 热门仓库列表
2. **获取仓库详情**：对每个仓库调用 GitHub REST API 获取 description、stars、language
3. **返回 JSON**：agent 自行格式化为目标平台的消息

## 使用方法

### 基础用法
```bash
python3 ~/.openclaw/workspace/skills/github-trending/scripts/fetch_trending.py
```

### 语言过滤
```bash
python3 ~/.openclaw/workspace/skills/github-trending/scripts/fetch_trending.py python
python3 ~/.openclaw/workspace/skills/github-trending/scripts/fetch_trending.py javascript
```

### 输出格式

返回 JSON 数组，每个元素：
```json
{
  "full_name": "owner/repo",
  "description": "仓库描述",
  "language": "Python",
  "stars": 12345,
  "url": "https://github.com/owner/repo"
}
```

### Agent 使用建议

获取数据后，根据所在平台格式化输出：

**飞书**：
```
📊 **GitHub Trending · 今日热榜**
🔥 1. owner/repo - 描述 ⭐ 12345 | Python 🔗 https://github.com/owner/repo
```

**Discord/Telegram**：
```
📊 GitHub Trending 今日热榜
1. owner/repo - 描述 ⭐ 12345 | Python | https://github.com/owner/repo
```

**控制台**：
```
1. owner/repo (⭐ 12345 | Python)
   描述
   https://github.com/owner/repo
```

## 注意事项

- GitHub API 有速率限制，高频使用建议配合缓存
- 脚本自动处理 API 错误，失败时会返回 fallback 数据
- 默认返回 9 个仓库，语言过滤时返回 10 个
