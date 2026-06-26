---
name: neodb
description: NeoDB 书影音标注助手 — 通过 API 替代网页/客户端完成所有 NeoDB 操作。支持搜索条目、标记（想看/在看/看过/放弃）、评分、短评、长评、笔记、收藏单、标签管理。触发场景：(1) 用户提到 NeoDB、书影音、标记、想看、看过、在读、读完、评分、评论 (2) 用户要搜索/标注书籍、电影、剧集、音乐、游戏、播客、演出 (3) 用户要管理书架、收藏单、标签 (4) 用户提到豆瓣链接需要导入 NeoDB
metadata:
  short-description: Search, mark, rate, and review books, movies, music, games on NeoDB
---

# NeoDB 书影音标注助手

通过 NeoDB API 替代网页/客户端完成搜索、标注、评论等全部操作。

## 前置条件

需要环境变量（`~/.claude/settings.json` → `env`）：
- `NEODB_TOKEN` — OAuth Access Token（必须）
- `NEODB_INSTANCE` — 实例域名（可选，默认 `neodb.social`）

首次使用运行鉴权：`bash scripts/setup-auth.sh [instance]`

## API 调用模板

```bash
# GET
curl -s -H "Authorization: Bearer $NEODB_TOKEN" \
  "https://${NEODB_INSTANCE:-neodb.social}/api/{endpoint}"

# POST (JSON)
curl -s -X POST -H "Authorization: Bearer $NEODB_TOKEN" \
  -H "Content-Type: application/json" -d '{...}' \
  "https://${NEODB_INSTANCE:-neodb.social}/api/{endpoint}"
```

所有写入操作执行前必须向用户确认。

## 核心工作流

### 搜索 → 标记（最常用）

```bash
# 1. 搜索
curl -s "https://${NEODB_INSTANCE:-neodb.social}/api/catalog/search?query={关键词}&category={类型}"
# category: book, movie, tv, movie,tv, music, game, podcast, performance

# 2. 标记
curl -s -X POST -H "Authorization: Bearer $NEODB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"shelf_type":"complete","visibility":0,"rating_grade":8,"comment_text":"短评","tags":["标签"],"post_to_fediverse":false}' \
  "https://${NEODB_INSTANCE:-neodb.social}/api/me/shelf/item/{uuid}"
```

**shelf_type**: `wishlist`=想看, `progress`=在看, `complete`=看过, `dropped`=放弃
**visibility**: `0`=公开, `1`=仅关注者, `2`=私密
**rating_grade**: 1-10（五星对应: 2/4/6/8/10），0=不评分

### 从外部链接导入

```bash
curl -s "https://${NEODB_INSTANCE:-neodb.social}/api/catalog/fetch?url={豆瓣/IMDB/Goodreads链接}"
# 302=已存在(提取URL中UUID), 202=抓取中(等15秒重试), 422=不支持
```

### 浏览书架

```bash
curl -s -H "Authorization: Bearer $NEODB_TOKEN" \
  "https://${NEODB_INSTANCE:-neodb.social}/api/me/shelf/{type}?category={category}&page=1"
# type: wishlist, progress, complete, dropped
# category: book, movie, tv, music, game, podcast, performance
```

### 写长评

```bash
curl -s -X POST -H "Authorization: Bearer $NEODB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"标题","body":"正文(Markdown)","visibility":0,"post_to_fediverse":false}' \
  "https://${NEODB_INSTANCE:-neodb.social}/api/me/review/item/{uuid}"
```

### 写笔记

```bash
curl -s -X POST -H "Authorization: Bearer $NEODB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"标题","content":"内容","visibility":0,"progress_type":"page","progress_value":"120"}' \
  "https://${NEODB_INSTANCE:-neodb.social}/api/me/note/item/{uuid}/"
# progress_type: page, chapter, timestamp, percentage, null
```

## 完整 API 参考

按需查阅，不必全部加载：

- **标记/书架/评论/笔记**: [references/shelf-and-journal.md](references/shelf-and-journal.md)
- **收藏单/标签**: [references/collection-and-tag.md](references/collection-and-tag.md)
- **目录/搜索/条目详情**: [references/catalog.md](references/catalog.md)
- **官方 OpenAPI Spec**: [references/openapi.json](references/openapi.json)

## 输出格式

搜索结果：
```
📖 书名 — 作者
   ⭐ 8.5/10 (120人) | UUID: xxx
```

标记成功：
```
✅ 已标记「书名」为 读过 ⭐⭐⭐⭐ (8/10)
   短评：评论内容 | 标签：标签1, 标签2
```

## 错误处理

| 状态码 | 含义 | 处理 |
|--------|------|------|
| 401 | 未授权 | 检查 NEODB_TOKEN |
| 404 | 未找到 | 条目不存在 |
| 202 | 抓取中 | 等 15 秒重试 fetch |
| 429 | 频率限制 | 等待重试 |
