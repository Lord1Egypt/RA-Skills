# 标记/书架/评论/笔记 API 参考

## 目录
- [标记 (Mark)](#标记-mark)
- [书架 (Shelf)](#书架-shelf)
- [评论 (Review)](#评论-review)
- [笔记 (Note)](#笔记-note)

---

## 标记 (Mark)

### GET `/api/me/shelf/item/{item_uuid}`
获取当前用户对条目的标记状态。

**Auth:** Required

**Response: MarkSchema**
```json
{
  "shelf_type": "complete",
  "visibility": 0,
  "post_id": 12345,
  "item": { /* ItemSchema */ },
  "created_time": "2024-01-15T10:30:00Z",
  "comment_text": "短评内容",
  "rating_grade": 8,
  "tags": ["科幻", "推荐"]
}
```

### POST `/api/me/shelf/item/{item_uuid}`
创建或更新标记。

**Auth:** Required

**Request Body: MarkInSchema**
```json
{
  "shelf_type": "complete",
  "visibility": 0,
  "comment_text": "短评内容",
  "rating_grade": 8,
  "tags": ["科幻"],
  "created_time": "2024-01-15T10:30:00Z",
  "post_to_fediverse": false
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shelf_type` | string | 是 | `wishlist`, `progress`, `complete`, `dropped` |
| `visibility` | int(0-2) | 是 | 0=公开, 1=仅关注者, 2=私密 |
| `comment_text` | string | 否 | 短评（默认空） |
| `rating_grade` | int(0-10) | 否 | 0=不评分, 2=1星, 4=2星, 6=3星, 8=4星, 10=5星 |
| `tags` | string[] | 否 | 标签列表 |
| `created_time` | datetime | 否 | ISO 8601，回溯标记用 |
| `post_to_fediverse` | bool | 否 | 同步到联邦宇宙（默认 false） |

### DELETE `/api/me/shelf/item/{item_uuid}`
删除标记。

**Auth:** Required

### GET `/api/me/shelf/items/{item_uuids}`
批量查询标记状态。item_uuids 用逗号分隔。

**Auth:** Required

### GET `/api/me/shelf/item/{item_uuid}/logs`
查看标记历史日志。

**Auth:** Required

---

## 书架 (Shelf)

### GET `/api/me/shelf/{type}`
浏览当前用户书架。

**Auth:** Required

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | path | 是 | `wishlist`, `progress`, `complete`, `dropped` |
| `category` | query | 否 | `book`, `movie`, `tv`, `music`, `game`, `podcast`, `performance` |
| `page` | query | 否 | 页码（默认 1） |

**Response: PagedMarkSchema**
```json
{
  "data": [ /* MarkSchema[] */ ],
  "pages": 3,
  "count": 25
}
```

### GET `/api/user/{handle}/shelf/{type}`
浏览其他用户书架（公开内容）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `handle` | path | 用户名 |
| `type` | path | shelf type |
| `category` | query | 分类过滤 |
| `page` | query | 页码 |

### GET `/api/user/{handle}/calendar`
用户标记日历统计。

---

## 评论 (Review)

### GET `/api/me/review/`
列出当前用户所有评论。

**Auth:** Required

### GET `/api/me/review/item/{item_uuid}`
获取当前用户对某条目的评论。

**Auth:** Required

### POST `/api/me/review/item/{item_uuid}`
发布评论。

**Auth:** Required

**Request Body: ReviewInSchema**
```json
{
  "title": "评论标题",
  "body": "评论正文（支持 Markdown）",
  "visibility": 0,
  "created_time": null,
  "post_to_fediverse": false
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 评论标题 |
| `body` | string | 是 | 正文（Markdown） |
| `visibility` | int(0-2) | 是 | 0=公开, 1=仅关注者, 2=私密 |
| `created_time` | datetime | 否 | ISO 8601 |
| `post_to_fediverse` | bool | 否 | 默认 false |

### DELETE `/api/me/review/item/{item_uuid}`
删除评论。

**Auth:** Required

### GET `/api/review/{review_uuid}`
获取任意评论详情（公开）。

**Response: ReviewSchema**
```json
{
  "url": "https://neodb.social/...",
  "api_url": "/api/review/...",
  "visibility": 0,
  "post_id": 12345,
  "item": { /* ItemSchema */ },
  "created_time": "2024-01-15T10:30:00Z",
  "title": "标题",
  "body": "Markdown 正文",
  "html_content": "<p>HTML 正文</p>"
}
```

---

## 笔记 (Note)

### GET `/api/me/note/item/{item_uuid}/`
列出条目相关笔记。

**Auth:** Required

### POST `/api/me/note/item/{item_uuid}/`
创建笔记。

**Auth:** Required

**Request Body: NoteInSchema**
```json
{
  "title": "笔记标题",
  "content": "笔记内容（Markdown）",
  "visibility": 0,
  "sensitive": false,
  "progress_type": "page",
  "progress_value": "120",
  "post_to_fediverse": false
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 标题 |
| `content` | string | 是 | 内容（Markdown） |
| `visibility` | int(0-2) | 是 | 公开/关注者/私密 |
| `sensitive` | bool | 否 | 敏感内容标记 |
| `progress_type` | string | 否 | `page`, `chapter`, `timestamp`, `percentage`, null |
| `progress_value` | string | 否 | 进度值（如页码 "120"） |
| `post_to_fediverse` | bool | 否 | 默认 false |

### PUT `/api/me/note/{note_uuid}`
更新笔记。Body 同 NoteInSchema。

**Auth:** Required

### DELETE `/api/me/note/{note_uuid}`
删除笔记。

**Auth:** Required
