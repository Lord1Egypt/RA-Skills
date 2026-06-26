# Joplin Data API - Complete Reference

Source: https://joplinapp.org/help/api/references/restapi

## Table of Contents
- [Data Model](#data-model)
- [Authentication](#authentication)
- [Notes](#notes)
- [Folders](#folders)
- [Resources](#resources)
- [Tags](#tags)
- [Revisions](#revisions)
- [Events](#events)
- [Search](#search)
- [Item Type IDs](#item-type-ids)

---

## Data Model

```
Folders (笔记本)                    Notes (笔记)
├── 顶层 (parent_id 为空/根)        ├── parent_id → 所属 folder 的 ID（唯一归属）
│   ├── 子笔记本 (parent_id→父ID)   ├── body = Markdown 格式内容
│   │   ├── 孙笔记本                ├── 可关联 tags、resources
│   │   │   └── ...无限层级         └── deleted_time=0 表示未删除
│   │   └── 孙笔记本
│   └── 子笔记本
└── 顶层
```

### Core Rules

- **Folders（笔记本）** = 目录/文件夹，通过 `parent_id` 形成**无限层级的树形结构**。没有层级深度限制，每个 folder 可有任意多个子 folder。
- **Notes（笔记）** = 内容载体，每条笔记归属到**一个且仅一个** folder（`parent_id` → folder ID）。内容是 Markdown 格式。
- **Tags（标签）** = 跨笔记本分类标记，不受 folder 层级限制。
- **Resources（资源）** = 附件文件，可关联到笔记上。

### parent_id 关系

| 对象 | parent_id 含义 |
|------|---------------|
| Folder | 指向父 folder ID；顶级 folder 为空或根 ID |
| Note | 指向所属 folder ID（唯一归属） |

- 两者都用 `deleted_time` 字段标记软删除（0=活跃，>0=已删）

---

## Authentication

Every API call requires `?token=YOUR_TOKEN` query parameter. Token from Joplin → Web Clipper Options.

Base URL: `http://localhost:41184` (scan ports 41184–41194 if not found).

Verify: `GET /ping` returns `"JoplinClipperServer"`.

---

## Notes

### Properties

| Name | Type | Description |
|------|------|-------------|
| id | text | Note ID |
| parent_id | text | Notebook ID containing this note |
| title | text | Note title |
| body | text | Note body in Markdown (may contain HTML) |
| body_html | text | Note body in HTML format |
| created_time | int | Creation timestamp (ms) |
| updated_time | int | Last update timestamp (ms) |
| is_conflict | int | Whether note is a conflict |
| latitude | numeric | GPS latitude |
| longitude | numeric | GPS longitude |
| altitude | numeric | GPS altitude |
| author | text | Author |
| source_url | text | Source URL |
| is_todo | int | Whether this is a todo |
| todo_due | int | Todo due date (ms) |
| todo_completed | int | Todo completion timestamp (ms) |
| source | text | Source |
| source_application | text | Source application |
| application_data | text | Application data |
| order | numeric | Sort order |
| user_created_time | int | User-set creation time |
| user_updated_time | int | User-set update time |
| encryption_cipher_text | text | Encrypted content |
| encryption_applied | int | Whether encryption is applied |
| markup_language | int | Markup language |
| is_shared | int | Whether note is published |
| share_id | text | Share ID |
| master_key_id | text | Master key ID |
| user_data | text | User data |
| deleted_time | int | Deletion timestamp (ms) |

### Create Note (POST /notes)

Supports `body` (Markdown) or `body_html` (HTML). When using `body_html`, also provide `base_url` for relative URL resolution.

Optional: `image_data_url` (Data URL format), `crop_rect` (`{x, y, width, height}`).

Custom ID: supply 32-char hex string as `id` property.

### Delete Note (DELETE /notes/:id)

Default: move to trash. Add `?permanent=1` for permanent deletion.

### DELETE /notes/:id/revisions

Delete all revisions for a note.

---

## Folders

Internally called "folders" (notebooks).

### Properties

| Name | Type | Description |
|------|------|-------------|
| id | text | Folder ID |
| title | text | Folder title |
| parent_id | text | Parent folder ID |
| created_time | int | Creation timestamp (ms) |
| updated_time | int | Last update timestamp (ms) |
| user_created_time | int | User-set creation time |
| user_updated_time | int | User-set update time |
| encryption_cipher_text | text | Encrypted content |
| encryption_applied | int | Whether encryption is applied |
| is_shared | int | Whether folder is shared |
| share_id | text | Share ID |
| master_key_id | text | Master key ID |
| icon | text | Icon |
| user_data | text | User data |
| deleted_time | int | Deletion timestamp (ms) |

### GET /folders

Returns all folders as a paginated flat list. Each folder has `parent_id` indicating its parent folder (empty/null = top-level). Use `parent_id` to reconstruct the tree hierarchy.

**Note:** When no `fields` parameter is specified, the API may return a tree structure with `children` key. When `fields` is specified, it returns a flat paginated list.

### DELETE /folders/:id

Default: move to trash. Add `?permanent=1` for permanent deletion.

---

## Resources

Attached files (images, documents, etc.).

### Properties

| Name | Type | Description |
|------|------|-------------|
| id | text | Resource ID |
| title | text | Resource title |
| mime | text | MIME type |
| filename | text | Filename |
| size | int | File size in bytes |
| file_extension | text | File extension |
| created_time | int | Creation timestamp (ms) |
| updated_time | int | Last update timestamp (ms) |
| ocr_text | text | OCR extracted text |
| ocr_status | int | OCR status |
| ocr_error | text | OCR error |

### POST /resources (Create with file upload)

Uses `multipart/form-data`:

```bash
curl -F 'data=@/path/to/file.jpg' \
     -F 'props={"title":"my resource title"}' \
     "http://localhost:41184/resources?token=$JOPLIN_TOKEN"
```

### PUT /resources/:id (Update file)

```bash
curl -X PUT -F 'data=@/path/to/file.jpg' \
          -F 'props={"title":"new title"}' \
     "http://localhost:41184/resources/RESOURCE_ID?token=$JOPLIN_TOKEN"
```

Or update properties only (no file change):

```bash
curl -X PUT --data '{"title": "New title"}' \
     "http://localhost:41184/resources/RESOURCE_ID?token=$JOPLIN_TOKEN"
```

### GET /resources/:id/file

Download the actual file.

---

## Tags

### Properties

| Name | Type | Description |
|------|------|-------------|
| id | text | Tag ID |
| title | text | Tag title |
| created_time | int | Creation timestamp (ms) |
| updated_time | int | Last update timestamp (ms) |

### POST /tags/:id/notes

Add tag to a note. Note data must contain at least an `id` property.

### DELETE /tags/:id/notes/:note_id

Remove tag from note.

---

## Revisions

Track note history changes.

### Properties

| Name | Type | Description |
|------|------|-------------|
| id | text | Revision ID |
| parent_id | text | Parent item ID |
| item_type | int | Item type (see Item Type IDs) |
| item_id | text | Item ID |
| item_updated_time | int | Item update timestamp |
| title_diff | text | Title diff |
| body_diff | text | Body diff |
| metadata_diff | text | Metadata diff |

---

## Events

Track recent note changes.

### Properties

| Name | Type | Description |
|------|------|-------------|
| id | int | Event ID |
| item_type | int | Item type |
| item_id | text | Item ID |
| type | int | Change type: 1=created, 2=updated, 3=deleted |
| created_time | int | Event timestamp (ms) |

### GET /events

Paginated list of recent events. Requires `cursor` parameter. Events kept for up to 90 days.

Without cursor: returns latest change ID (use as starting point).

Response includes `cursor`, `has_more`, and `items`.

---

## Search

### GET /search?query=YOUR_QUERY

Full-text search for notes. Supports `fields` parameter.

Query syntax: https://joplinapp.org/help/apps/search

For non-notes items, add `type` parameter:
- `type=folder` — search notebooks (case-insensitive, supports `*` wildcard)
- `type=tag` — search tags (case-insensitive, supports `*` wildcard)

Examples:
- `GET /search?query=recipes&type=folder` — find notebook named "recipes"
- `GET /search?query=project-*&type=tag` — find tags starting with "project-"

---

## Item Type IDs

| Name | Value |
|------|-------|
| note | 1 |
| folder | 2 |
| setting | 3 |
| resource | 4 |
| tag | 5 |
| note_tag | 6 |
| search | 7 |
| alarm | 8 |
| master_key | 9 |
| item_change | 10 |
| note_resource | 11 |
| resource_local_state | 12 |
| revision | 13 |
| migration | 14 |
| smart_filter | 15 |
| command | 16 |

---

## Filtering & Pagination

### Fields Filtering

Use `fields=` query parameter with comma-separated field names:

```
GET /notes/NOTE_ID?fields=longitude,latitude
GET /tags?fields=id
```

Default fields returned: `id`, `parent_id`, `title`.

### Pagination

All multi-result endpoints return:
```json
{
  "items": [...],
  "has_more": true
}
```

Parameters:
- `page` — page number (starts at 1, default 1)
- `limit` — items per page (max 100)
- `order_by` — sort field
- `order_dir` — sort direction (`ASC` or `DESC`)

---

## Error Handling

Errors return HTTP status ≥ 400 with JSON:
```json
{ "error": "description of error" }
```
