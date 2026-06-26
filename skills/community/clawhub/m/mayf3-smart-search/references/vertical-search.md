# 垂直搜索引擎速查

**核心原则：先选战场，再选武器。** "在哪搜"比"怎么搜"重要。

## 垂直搜索路由

| 场景 | 推荐引擎 | 备注 |
|------|---------|------|
| 学术论文 | Semantic Scholar（TLDR 快筛）→ Google Scholar（引用链） | arXiv 看 CS/AI 前沿 |
| 代码实现 | grep.app（轻量快查）→ GitHub Code Search（正则） | `sourcegraph.com` 替换 `github.com` 无需登录 |
| 最新新闻 | DDGS news() → Twitter 高级搜索 | `site:reuters.com OR site:apnews.com` 限定权威源 |
| 用户评价 | `site:reddit.com` → 搜狗微信搜索 | Reddit 站内搜索差，用通用引擎搜 site:reddit.com 更好 |
| 技术博客 | DDGS brave `site:dev.to OR site:medium.com` | - |
| 中文深度文章 | 搜狗微信搜索 `wx.sogou.com` | 公众号文章首选 |
| 图书搜索 | DDGS books() | 返回 title/author/publisher/url |
| 视频搜索 | DDGS videos() | 返回 duration/provider/statistics |
| 全文提取 | DDGS extract()（首选）/ Jina Reader（备选） | URL→Markdown |
| 语义搜索 | Exa | 按含义匹配，1000次/月免费 |

## 搜索→全文获取链路

```
DDGS 搜索（发现 URL）→ DDGS extract()（获取全文 Markdown，一站式完成）
```
