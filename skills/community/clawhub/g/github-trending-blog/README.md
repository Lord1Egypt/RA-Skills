# GitHub Trending Blog Pipeline

> 从 GitHub Trending 监控到公众号技术博客发布的完整自动化工作流

## 🎯 业务场景

技术博主、独立开发者、技术 newsletter 作者，每天面临以下痛点：

- **信息过载**：GitHub Trending 每天新增数百个项目，不知道追哪个
- **调研耗时**：手动打开每个项目、读 README、整理信息，平均每个项目 15 分钟
- **写作拖延**：好不容易调研完，写博客又是 1-2 小时
- **排版麻烦**：写完还要找配图、调格式

**结果：想做个技术内容账号，但永远停在"下次一定"。**

## 💡 解决方案

本工作流将 GitHub Trending → AI 摘要 → 知识卡片 → 技术博客的完整链路压缩到 **10 分钟**，让你每天轻松产出一篇高质量技术博客。

## ⚙️ Skill 编排图谱

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Trending                       │
│                    (数据采集层)                          │
│              github + gh api                            │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│                   AI 摘要分析                            │
│                    (理解层)                              │
│              summarize CLI                              │
│         README → 核心特性 + 关键洞察                      │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│                  开发者知识卡片                          │
│                   (视觉层)                              │
│           card-renderer (VS Code 风格)                  │
│          生成封面图 + 详情页，适合社交媒体                  │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│                  技术博客撰写                            │
│                   (内容层)                              │
│           wechat-article-pro                           │
│     3000-5000字刘润风格深度技术博客                       │
└─────────────────────────────────────────────────────────┘
```

## 📦 涉及的 Skill

| Skill | 作用 | 调用方式 |
|-------|------|---------|
| `github` | 采集 Trending repos | `gh api` / `gh search` |
| `summarize` | AI 摘要 README 和项目信息 | `summarize <url>` |
| `card-renderer` | 生成开发者风格知识卡片 | Python PIL 脚本 |
| `wechat-article-pro` | 撰写 3000-5000 字技术博客 | Browser 自动化 |

## 🚀 使用方法

### 完整工作流命令

```bash
# Step 1: 采集 GitHub Trending（Python 语言，今日）
gh api graphql -f query='
{
  search(query: "language:Python stars:>100 pushed:>2026-05-01", 
         type: REPOSITORY, first: 10) {
    nodes { 
      ... on Repository { 
        nameWithOwner description stargazerCount 
        primaryLanguage url 
      } 
    }
  }
}' --jq '.data.search.nodes[] |

# Step 2: 摘要感兴趣的项目
summarize "https://github.com/owner/repo" --extract-only

# Step 3: 渲染知识卡片
python3 /root/.openclaw/workspace/skills/card-renderer/scripts/render_vscode_card.py \
  "项目名" "一句话描述" "/tmp/readme.md" "/tmp/output/"

# Step 4: 撰写博客（使用 wechat-article-pro Skill）
# 参考 wechat-article-pro/SKILL.md 执行步骤
```

### 触发词

以下任一触发时激活本工作流：
- "GitHub热门" / "GitHub Trending"
- "技术博客" / "技术周报" / "技术日报"
- "追踪开源趋势" / "开发者内容"
- "帮我写一篇关于 XXX 的技术博客"

## 📊 输出示例

**采集结果：**
```json
{
  "repo": "owner/awesome-project",
  "stars": "12.3k",
  "language": "Python",
  "description": "AI-powered code review tool",
  "url": "https://github.com/owner/awesome-project"
}
```

**知识卡片：** `render_vscode_card.py` 输出 1080x1440 PNG，封面 + 详情页

**技术博客：** 3000-5000 字，含：
- 开篇：一个具体的开发痛点切入
- 正文：3-4 个小节，每节含案例 + 分析 + 结论
- 总结：核心洞察 + 可操作建议
- 全程无 emoji，无话题标签

## ⚠️ 注意事项

1. **GitHub API 速率限制**：未认证 60 次/小时，建议适当控制采集频率
2. **公众号发布**：生成草稿后需用户登录 mp.weixin.qq.com 手动发布
3. **卡片风格**：建议技术内容用 `render_vscode_card.py`（开发者共鸣感最强）
4. **内容质量**：建议每次选择 1-2 个核心项目深入分析，而非泛泛介绍 10 个
