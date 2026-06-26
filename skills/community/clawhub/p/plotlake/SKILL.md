---
name: plotlake
description: 订阅微信公众号等信源，获取原始文章内容用于整合日报
version: 1.3.0
metadata:
  openclaw:
    homepage: https://github.com/eggyrooch-blip/wewerss
    requires:
      anyBins:
        - curl
        - jq
---

# Plotlake Open Channel Skill

**API 地址：`https://api.plotlake.com`**（无需配置环境变量，直接使用此地址）

通过 Open Channel API 订阅信源并获取原始文章数据。所有 AI 处理由 Agent 侧完成。

## 快速开始

```bash
BASE="https://api.plotlake.com"

# 1. 创建频道
curl -s -X POST "$BASE/api/open/channels" \
  -H "Content-Type: application/json" \
  -d '{"name":"我的日报频道"}' | jq .

# 2. 浏览可订阅的信源套餐
curl -s "$BASE/api/open/catalog/bundles" | jq .

# 3. 一键订阅套餐（如 AI入门包）
curl -s -X POST "$BASE/api/open/channels/$CHANNEL_ID/subscribe-bundle?bundle_id=ai_starter" | jq .

# 4. 获取文章
curl -s "$BASE/api/open/channels/$CHANNEL_ID/articles?days=1" | jq .
```

## 信源目录（策展精选）

### 浏览所有套餐

```bash
curl -s "$BASE/api/open/catalog/bundles" | jq .
```

### 按分类筛选

```bash
# 分类: technology, finance, developer, games, anime, movies, books, music, lifestyle, news
curl -s "$BASE/api/open/catalog/bundles?category=technology" | jq .
```

### 搜索

```bash
curl -s "$BASE/api/open/catalog/bundles?q=AI" | jq .
```

### 查看套餐详情（含 RSS 地址列表）

```bash
curl -s "$BASE/api/open/catalog/bundles/ai_starter" | jq .
```

### 可用套餐一览

| ID | 名称 | 分类 | 信源数 |
|---|---|---|---|
| `ai_starter` | AI入门包 | technology | 6 |
| `ai_researcher` | AI研究者包 | technology | 5 |
| `tech_daily` | 科技日报包 | technology | 6 |
| `chinese_tech` | 中文科技圈 | technology | 5 |
| `global_tech` | 全球科技圈 | technology | 4 |
| `developer_daily` | 开发者日报包 | developer | 4 |
| `frontend_dev` | 前端开发包 | developer | 4 |
| `backend_dev` | 后端开发包 | developer | 4 |
| `polyglot` | 全栈技术包 | developer | 6 |
| `finance_pro` | 财经专业包 | finance | 6 |
| `crypto_watch` | 加密货币观察包 | finance | 4 |
| `news_junkie` | 新闻达人包 | news | 5 |
| `deep_reads` | 深度阅读包 | news | 5 |
| `game_enthusiast` | 游戏爱好者包 | games | 6 |
| `indie_gamer` | 独立游戏包 | games | 4 |
| `anime_otaku` | 动漫宅包 | anime | 5 |
| `anime_critic` | 动画评论包 | anime | 3 |
| `movie_buff` | 电影爱好者包 | movies | 5 |
| `cinephile` | 影迷深度包 | movies | 4 |
| `book_lover` | 读书爱好者包 | books | 5 |
| `music_fan` | 音乐爱好者包 | music | 5 |
| `indie_music` | 独立音乐包 | music | 4 |
| `smart_shopper` | 聪明消费者包 | lifestyle | 4 |
| `minimalist` | 极简生活包 | lifestyle | 3 |

## 手动添加信源

提交任意 URL（RSS 地址、网站首页），系统自动发现 feed：

```bash
curl -s -X POST "$BASE/api/open/channels/$CHANNEL_ID/sources" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/feed.xml"}' | jq .
```

## 频道管理

```bash
# 查看频道详情
curl -s "$BASE/api/open/channels/$CHANNEL_ID" | jq .

# 列出信源
curl -s "$BASE/api/open/channels/$CHANNEL_ID/sources" | jq .

# 删除信源
curl -s -X DELETE "$BASE/api/open/channels/$CHANNEL_ID/sources/$SOURCE_ID"
```

## 获取文章

```bash
# 最近 1 天
curl -s "$BASE/api/open/channels/$CHANNEL_ID/articles?days=1" | jq .

# 最近 7 天，分页
curl -s "$BASE/api/open/channels/$CHANNEL_ID/articles?days=7&page=2&page_size=50" | jq .
```

返回字段：title, author, link, published_at, description, text_plain, source_name

**不返回 AI 字段** — Agent 自行用 LLM 处理。

## Atom Feed

```bash
curl -s "$BASE/api/open/channels/$CHANNEL_ID/feed"
```

## 典型工作流

1. 创建频道 → `POST /api/open/channels`
2. 浏览套餐 → `GET /api/open/catalog/bundles`
3. 一键订阅 → `POST /api/open/channels/{id}/subscribe-bundle?bundle_id=ai_starter`
4. 获取文章 → `GET /api/open/channels/{id}/articles?days=1`
5. Agent 用 LLM 整合日报
