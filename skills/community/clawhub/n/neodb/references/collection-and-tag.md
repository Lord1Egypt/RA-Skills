# 收藏单/标签 API 参考

## 目录
- [收藏单 (Collection)](#收藏单-collection)
- [标签 (Tag)](#标签-tag)
- [精选收藏单 (Featured)](#精选收藏单-featured)

---

## 收藏单 (Collection)

### GET `/api/me/collection/`
列出当前用户的收藏单。

**Auth:** Required

| 参数 | 类型 | 说明 |
|------|------|------|
| `page` | query | 页码（默认 1） |
| `page_size` | query | 每页数量 |

**Response: PagedCollectionSchema**

### POST `/api/me/collection/`
创建收藏单。

**Auth:** Required

**Request Body: CollectionInSchema**
```json
{
  "title": "收藏单标题",
  "brief": "描述（Markdown）",
  "visibility": 0,
  "query": null
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 标题 |
| `brief` | string | 是 | 描述（Markdown） |
| `visibility` | int(0-2) | 是 | 0=公开, 1=仅关注者, 2=私密 |
| `query` | string | 否 | 自动收藏查询条件 |

### GET `/api/me/collection/{collection_uuid}`
获取收藏单详情。

**Auth:** Required

### PUT `/api/me/collection/{collection_uuid}`
更新收藏单。Body 同 CollectionInSchema。

**Auth:** Required

### DELETE `/api/me/collection/{collection_uuid}`
删除收藏单。

**Auth:** Required

### GET `/api/collection/{collection_uuid}`
获取任意收藏单详情（公开）。

### GET `/api/collection/{collection_uuid}/item/`
列出收��单中的条目（公开）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `page` | query | 页码 |
| `page_size` | query | 每页数量 |

### GET `/api/me/collection/{collection_uuid}/item/`
列出自己收藏单中的条目。

**Auth:** Required

### POST `/api/me/collection/{collection_uuid}/item/`
添加条目到收藏单。

**Auth:** Required

**Request Body: CollectionItemInSchema**
```json
{
  "item_uuid": "条目UUID",
  "note": "收藏备注"
}
```

### DELETE `/api/me/collection/{collection_uuid}/item/{item_uuid}`
从收藏单移除条目。

**Auth:** Required

### GET `/api/item/{item_uuid}/collection/`
列出包含某条目的所有收藏单。

---

## 标签 (Tag)

### GET `/api/me/tag/`
列出当前用户所有标签。

**Auth:** Required

### POST `/api/me/tag/`
创建标签。

**Auth:** Required

**Request Body: TagInSchema**
```json
{
  "title": "标签名",
  "visibility": 0
}
```

### GET `/api/me/tag/{tag_uuid}`
获取标签详情。

**Auth:** Required

### PUT `/api/me/tag/{tag_uuid}`
更新标签。Body 同 TagInSchema。

**Auth:** Required

### DELETE `/api/me/tag/{tag_uuid}`
删除标签。

**Auth:** Required

### GET `/api/me/tag/{tag_uuid}/item/`
列出标签下的条目。

**Auth:** Required

### POST `/api/me/tag/{tag_uuid}/item/`
给标签添加条目。

**Auth:** Required

**Request Body: TagItemInSchema**
```json
{
  "item_uuid": "条目UUID"
}
```

### DELETE `/api/me/tag/{tag_uuid}/item/{item_uuid}`
从标签移除条目。

**Auth:** Required

### GET `/api/trending/tag/`
热门标签。

---

## 精选收藏单 (Featured)

### GET `/api/me/collection/featured/`
列出精选收藏单。

**Auth:** Required

### POST/DELETE `/api/me/collection/featured/{collection_uuid}`
添加/移除精选。

**Auth:** Required

### GET `/api/me/collection/featured/{collection_uuid}/stats`
精选收藏单统计。

**Auth:** Required

### GET `/api/trending/collection/`
热门收藏单。
