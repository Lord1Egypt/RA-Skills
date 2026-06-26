# 目录/搜索/条目 API 参考

## 目录
- [搜索](#搜索)
- [外部链接导入](#外部链接导入)
- [条目详情](#条目详情)
- [条目帖文](#条目帖文)
- [热门/趋势](#热门趋势)
- [用户信息](#用户信息)

---

## 搜索

### GET `/api/catalog/search`
搜索 NeoDB 目录。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 关键词、ISBN、书名、创作者 |
| `category` | string | 否 | `book`, `movie`, `tv`, `movie,tv`, `music`, `game`, `podcast`, `performance` |
| `page` | int | 否 | 页码（默认 1） |

**Response: SearchResult**
```json
{
  "data": [
    {
      "type": "Edition",
      "uuid": "xxx",
      "url": "/book/xxx",
      "api_url": "/api/book/xxx",
      "category": "book",
      "display_title": "书名",
      "title": "书名",
      "description": "简介...",
      "cover_image_url": "https://...",
      "rating": 8.5,
      "rating_count": 120,
      "external_resources": [{"url": "https://book.douban.com/..."}]
    }
  ],
  "pages": 5,
  "count": 50
}
```

注意：count 和 pages 是估算值，实际数据可能更少。不会显示外部结果，也不会解析 URL。如需 URL 导入，使用 `/api/catalog/fetch`。

---

## 外部链接导���

### GET `/api/catalog/fetch`
从外部站点 URL 导入条目。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | 是 | 外部 URL（豆瓣、IMDB、Goodreads、Steam、Spotify 等） |

**响应逻辑：**
- **302** — 条目已存在，`url` 字段包含 NeoDB 条目地址，提取 UUID
- **202** — 正在抓取，等 15 秒后重试（最长等 120 秒）
- **422** — URL 不支持
- **429** — 请求过于频繁

---

## 条目详情

### GET `/api/{category}/{uuid}`
按类型获取条目详情。

| 路径 | 类型 |
|------|------|
| `/api/book/{uuid}` | 图书 |
| `/api/movie/{uuid}` | 电影 |
| `/api/tv/{uuid}` | 剧集 |
| `/api/tv/season/{uuid}` | 剧集季 |
| `/api/tv/episode/{uuid}` | 剧集集 |
| `/api/album/{uuid}` | 音乐专辑 |
| `/api/podcast/{uuid}` | 播客 |
| `/api/podcast/episode/{uuid}` | 播客单集 |
| `/api/game/{uuid}` | 游戏 |
| `/api/performance/{uuid}` | 演出 |
| `/api/performance/production/{uuid}` | 演出制作 |

共同返回字段 (ItemSchema)：
```json
{
  "type": "Edition",
  "uuid": "string",
  "url": "string",
  "api_url": "string",
  "category": "book",
  "parent_uuid": null,
  "display_title": "string",
  "title": "string",
  "description": "string",
  "cover_image_url": "https://...",
  "rating": 8.5,
  "rating_count": 120,
  "localized_title": [{"lang": "zh", "text": "中文标题"}],
  "localized_description": [{"lang": "zh", "text": "中文简介"}],
  "external_resources": [{"url": "https://..."}]
}
```

图书额外字�� (EditionSchema)：`subtitle`, `orig_title`, `author[]`, `translator[]`, `language[]`, `pub_house`, `pub_year`, `pub_month`, `binding`, `price`, `pages`, `series`, `imprint`, `isbn`

电影额外字段 (MovieSchema)：`orig_title`, `other_title[]`, `director[]`, `playwright[]`, `actor[]`, `genre[]`, `language[]`, `area[]`, `year`, `duration`

### GET `/api/book/{uuid}/sibling/`
获取同一作品的其他版本。

| 参数 | 说明 |
|------|------|
| `page` | 页码 |
| `page_size` | 每页数量 |

### GET `/api/podcast/{uuid}/episode/`
列出播客的所有单集。

| 参数 | 说明 |
|------|------|
| `page` | 页码 |
| `guid` | 按 GUID 查找特定单集 |

---

## 条目帖文

### GET `/api/item/{item_uuid}/posts/`
获取条目相关的社区帖文。

| 参数 | 类型 | 说明 |
|------|------|------|
| `type` | string | 逗号分隔：`comment`, `review`, `collection`, `mark` |

**Response: PaginatedPostList**
```json
{
  "data": [ /* Mastodon Status objects */ ],
  "pages": 5,
  "count": 50
}
```

---

## 热门/趋势

### GET `/api/trending/{category}/`

| 路径 | 说明 |
|------|------|
| `/api/trending/book/` | 热门图书 |
| `/api/trending/movie/` | 热门电影 |
| `/api/trending/tv/` | 热门剧集 |
| `/api/trending/music/` | 热门音乐 |
| `/api/trending/game/` | 热门游戏 |
| `/api/trending/podcast/` | 热门播客 |
| `/api/trending/performance/` | 热门演出 |
| `/api/trending/collection/` | 热门收藏单 |
| `/api/trending/tag/` | 热门标签 |

**Response:** Array of ItemSchema

---

## 用户信息

### GET `/api/me`
当前用户基本信息。**Auth:** Required

### GET `/api/me/preference`
当前用户偏好设置。**Auth:** Required

```json
{
  "default_crosspost": false,
  "default_visibility": 0,
  "hidden_categories": [],
  "language": "zh"
}
```

### GET `/api/token`
验证 Token 是否有效。**Auth:** Required

### GET `/api/user/{handle}`
获取其他用户信息。

---

## 外部资源平台标识

`external_resources` 中的 URL 可识别的平台：
douban, goodreads, booksTW, googleBooks, imdb, tmdb, bangumi, bandcamp, spotify, appleMusic, discogs, applePodcasts, igdb, steam, bgg, ao3, jinjiang, qidian, bilibili, fedi, rss
