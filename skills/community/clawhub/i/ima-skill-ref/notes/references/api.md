# IMA笔记 API

Base: `https://ima.qq.com/openapi/note/v1`

## 响应格式

```json
{ "code": 0, "msg": "...", "data": {...} }
```
- code=0：成功，从data提取字段
- code≠0：失败，直接展示msg

## 数据结构

### DocBasic
`docid`, `title`, `summary`, `create_time`, `modify_time`(Unix毫秒), `status`(0正常/1删除), `folder_id`, `folder_name`

### SearchedDoc
`doc`: DocBasicInfo, `highlight_info`{doc_title: 含\<em\>高亮\</em\>}

### NoteBookFolderBasic
`folder_id`, `name`, `status`(0正常/1删除), `create_time`, `modify_time`(Unix毫秒), `note_number`, `folder_type`(0自建/1全部笔记/2未分类)

### QueryInfo
`title`, `content`

---

## 接口

### search_note_book
**请求：** `search_type`(0标题/1正文), `sort_type`(0更新时间), `query_info`{title,content}（⚠️不能全为空）, `start`, `end`

**响应：** `docs[]`(SearchedDoc), `is_end`, `total_hit_num`

---

### list_note_folder_by_cursor
**请求：** `cursor`(首页="0"), `limit`

**响应：** `note_book_folders[]`, `next_cursor`, `is_end`

---

### list_note_by_folder_id
**请求：** `folder_id`(空=全部笔记), `cursor`(首页=""), `limit`

**响应：** `note_book_list[]`, `next_cursor`, `is_end`

> 全部笔记folder_id格式：`user_list_{userid}`，从folder_type=1获取

---

### import_doc
**请求：** `content_format`(1=Markdown), `content`, `folder_id`(可选)

**响应：** `doc_id`

---

### append_doc
**请求：** `doc_id`, `content_format`(1=Markdown), `content`

**响应：** `doc_id`

> ⚠️追加会修改已有笔记。用户未明确指定目标时，必须先确认。

---

### get_doc_content
**请求：** `doc_id`, `target_content_format`(0=纯文本/1=Markdown不支持/2=JSON)

**响应：** `content`

---

## 枚举

| 枚举 | 值 | 说明 |
|------|-----|------|
| content_format | 0 | 纯文本 |
| content_format | 1 | Markdown（写入必须用1） |
| search_type | 0 | 按标题 |
| search_type | 1 | 按正文 |
| folder_type | 0 | 用户自建 |
| folder_type | 1 | 全部笔记 |
| folder_type | 2 | 未分类 |

## 注意
- folder_id不可为"0"
- 超限返回100009，拆分多次append_doc
- 本地图片不支持，过滤`![](file:///...)`
