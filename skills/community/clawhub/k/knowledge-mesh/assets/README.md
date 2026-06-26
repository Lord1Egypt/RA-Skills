# Knowledge Mesh / 知识网格

> Cross-platform knowledge search aggregator — unified search across GitHub, Stack Overflow, Discord, Confluence, Notion, and Slack
>
> 跨平台知识搜索聚合器 — 统一搜索 GitHub、Stack Overflow、Discord、Confluence、Notion、Slack

---

## Features / 功能亮点

- **Unified Search / 统一搜索** — Search across 8 platforms with one query. 一次查询搜索 8 个平台，结果统一排序展示。
- **TF-IDF Ranking / 智能排序** — Relevance + authority + recency scoring. TF-IDF 相关性评分 + 权威性 + 时间衰减综合排序。
- **Self-Learning / 自学习排序** — Search gets smarter with use. 搜索越用越精准，根据反馈自动优化排序权重。
- **Obsidian Integration / Obsidian 集成** — Search your local notes too. 本地笔记也能一起搜，支持 wikilinks、标签、frontmatter。
- **Baidu Search / 百度搜索** — Enhanced Chinese content search. 中文内容搜索增强，覆盖中文技术社区。
- **Deduplication / 智能去重** — Jaccard similarity dedup across sources. 基于 Jaccard 相似度跨平台去重。
- **Local Indexing / 本地索引** — Index local .md/.txt/.py files with full-text search. 索引本地文档，支持全文检索。
- **Topic Monitoring / 主题监控** — Set keyword alerts, get daily/weekly digests. 设置关键词监控，获取日报/周报摘要。
- **Knowledge Synthesis / 知识合成** — AI-powered summary of search results. 将搜索结果合成为结构化知识报告。
- **Mermaid Charts / 可视化图表** — Trend analysis with Mermaid pie/bar/line charts. 趋势分析生成 Mermaid 饼图/柱状图/折线图。
- **Export / 导出** — Markdown reports and CSV files. 支持导出 Markdown 报告和 CSV 文件。

---

## Version Comparison / 版本对比

| Feature / 功能 | Free / 免费版 | Paid / 付费版 ¥129/月 |
|----------------|:------------:|:-------------------:|
| Knowledge sources / 知识源数量 | 5 | 10 |
| Supported platforms / 支持平台 | GitHub + SO + Baidu + Obsidian | All 8 platforms / 全部 8 平台 |
| Daily searches / 每日搜索次数 | 10 | Unlimited / 无限 |
| Max results per search / 单次结果数 | 20 | 100 |
| Self-learning ranking / 自学习排序 | Basic / 基础 | Advanced / 高级分析 |
| Obsidian integration / Obsidian 集成 | Supported / 支持 | Supported / 支持 |
| Baidu search / 百度搜索 | Supported / 支持 | Supported / 支持 |
| Local indexing / 本地知识索引 | -- | Supported / 支持 |
| Topic monitoring / 主题监控 | -- | Supported / 支持 |
| Knowledge synthesis / 知识合成 | -- | Supported / 支持 |
| Mermaid trend charts / 趋势图表 | -- | Supported / 支持 |
| Export / 导出 | Markdown + CSV | Full / 全格式 + 趋势分析 |

---

## Quick Start / 快速开始

### 1. Install / 安装

Search for `knowledge-mesh` in ClawHub, or use CLI:

在 ClawHub 中搜索 `knowledge-mesh`，或使用命令行：

```bash
openclaw skill install knowledge-mesh
```

### 2. Configure Sources / 配置知识源

Set environment variables for the platforms you want to search:

设置你要搜索的平台的环境变量：

```bash
# GitHub (recommended / 推荐)
export KM_GITHUB_TOKEN="ghp_your_token_here"

# Stack Overflow (optional / 可选，提高速率限制)
export KM_STACKOVERFLOW_KEY="your_key_here"

# Discord (paid / 付费版)
export KM_DISCORD_BOT_TOKEN="your_bot_token"
export KM_DISCORD_CHANNEL_ID="channel_id"

# Confluence (paid / 付费版)
export KM_CONFLUENCE_URL="https://your-domain.atlassian.net"
export KM_CONFLUENCE_TOKEN="your_token"

# Notion (paid / 付费版)
export KM_NOTION_TOKEN="ntn_your_token"

# Slack (paid / 付费版)
export KM_SLACK_TOKEN="xoxb-your-token"

# Baidu Search / 百度搜索 (free / 免费)
export KM_BAIDU_API_KEY="your_baidu_api_key"

# Obsidian (free / 免费)
export KM_OBSIDIAN_VAULT_PATH="/path/to/your/vault"
```

### 3. Search / 搜索

```bash
# Unified search / 统一搜索
/knowledge-mesh search "python async best practices"

# Search specific source / 搜索指定平台
/knowledge-mesh search-source github "fastapi websocket"

# View configured sources / 查看已配置知识源
/knowledge-mesh list-sources
```

### 4. Advanced Features / 高级功能 (Paid / 付费版)

```bash
# Index local files / 索引本地文件
/knowledge-mesh index "./docs" "./src"

# Set up monitoring / 设置主题监控
/knowledge-mesh monitor "kubernetes" "deployment"

# Export report / 导出报告
/knowledge-mesh export markdown
```

---

## Example / 使用示例

```
用户: 搜索 Python FastAPI WebSocket 最佳实践

知识网格: 正在搜索 GitHub、Stack Overflow...

搜索结果（共 15 条）:

1. [Stack Overflow] FastAPI WebSocket connection best practices
   - 链接: https://stackoverflow.com/questions/...
   - 相关度: 0.92
   - 摘要: For **FastAPI** **WebSocket** connections, it's recommended to...

2. [GitHub] tiangolo/fastapi#1234 - WebSocket documentation improvements
   - 链接: https://github.com/tiangolo/fastapi/issues/1234
   - 相关度: 0.87
   - 摘要: This PR improves the **WebSocket** section with **best practices**...

3. [Stack Overflow] How to handle WebSocket disconnections in FastAPI?
   - 链接: https://stackoverflow.com/questions/...
   - 相关度: 0.81
   - 摘要: When dealing with **WebSocket** disconnections in **FastAPI**...
```

---

## FAQ / 常见问题

### Q1: Which platforms can I search for free? / 免费版可以搜索哪些平台？

Free tier supports GitHub and Stack Overflow. These two platforms cover the majority of technical Q&A and open-source project discussions.

免费版支持 GitHub 和 Stack Overflow。这两个平台覆盖了绝大多数技术问答和开源项目讨论。

### Q2: Is my data uploaded to the cloud? / 数据会上传到云端吗？

No. All search requests go directly from your machine to each platform's API. Local index data is stored locally. No data passes through any third-party server.

不会。所有搜索请求从你的机器直接发送到各平台 API。本地索引数据存储在本地。没有数据经过任何第三方服务器。

### Q3: Do I need API keys for all platforms? / 需要配置所有平台的 API Key 吗？

No. You only need to configure the platforms you want to search. Stack Overflow works without an API key (with rate limits). GitHub search also works without a token but with lower rate limits.

不需要。你只需配置你想搜索的平台。Stack Overflow 无需 API Key 即可使用（有速率限制）。GitHub 搜索无 Token 也可工作但速率限制更低。

### Q4: How does deduplication work? / 去重是怎么实现的？

We use Jaccard similarity on tokenized title + snippet text. Results with similarity above 0.7 are considered duplicates, keeping the one with higher relevance score.

使用标题+摘要的分词集合计算 Jaccard 相似度。相似度超过 0.7 的结果被视为重复，保留相关度更高的结果。

### Q5: Can I search in Chinese? / 可以用中文搜索吗？

Yes. The search query is passed directly to each platform's API. Chinese queries work well on GitHub, Confluence, Notion, and Slack. Stack Overflow results are primarily in English.

可以。搜索查询直接传递给各平台 API。中文查询在 GitHub、Confluence、Notion 和 Slack 上效果良好。Stack Overflow 结果以英文为主。

### Q6: What file types can be locally indexed? / 本地索引支持哪些文件类型？

Supported: `.md`, `.txt`, `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.rb`, `.sh`, `.yaml`, `.json`, `.html`, `.css`, `.sql` and more.

支持：`.md`、`.txt`、`.py`、`.js`、`.ts`、`.java`、`.go`、`.rs`、`.rb`、`.sh`、`.yaml`、`.json`、`.html`、`.css`、`.sql` 等。

---

## Support / 技术支持

- **Docs / 文档**: See `references/` directory for API and syntax guides
- **Issues / 问题反馈**: Submit issues on ClawHub skill page
- **Community / 社区**: Join `#knowledge-mesh` channel on ClawHub community
- **Email / 邮件**: skill-support@clawhub.dev

---

*knowledge-mesh v1.1.0 | Compatible with OpenClaw 0.5+ / 兼容 OpenClaw 0.5+*
