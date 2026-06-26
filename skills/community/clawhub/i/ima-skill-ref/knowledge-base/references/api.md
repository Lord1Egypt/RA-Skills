# IMA知识库 API

Base: `https://ima.qq.com/openapi/wiki/v1`

## media_type

| 值 | 类型 | 备注 |
|----|------|------|
| 1 | PDF | |
| 2 | 网页 | add_knowledge时web_info.content_id=url |
| 3 | Word | |
| 4 | PPT | |
| 5 | Excel | |
| 6 | 微信公众号 | URL匹配mp.weixin.qq.com/s |
| 7 | Markdown | |
| 9 | 图片 | png/jpeg/webp |
| 11 | 笔记 | note_info.content_id=doc_id |
| 12 | AI会话 | session_info.content_id=session_id |
| 13 | TXT | |
| 14 | Xmind | |
| 15 | 音频 | mp3/m4a/wav/aac |
| 16 | 视频 | 不支持 |

## 响应格式

```json
{ "code": 0, "msg": "...", "data": {...} }
```
- code=0：成功，从data提取字段
- code≠0：失败，直接展示msg

## 数据结构

### KnowledgeBaseInfo
`id`, `name`, `cover_url`, `description`, `recommended_questions[]`

### KnowledgeInfo
`media_id`, `title`, `parent_folder_id`

### FolderInfo
`folder_id`(以folder_开头), `name`, `file_number`, `folder_number`, `is_top`

### SearchedKnowledgeInfo
`media_id`, `title`, `parent_folder_id`, `highlight_content`

### Credential
`token`, `secret_id`, `secret_key`, `start_time`, `expired_time`, `bucket_name`, `region`, `cos_key`

---

## 接口

### create_media
获取COS上传凭证。

**请求：** `file_name`, `file_size`(uint64), `content_type`, `knowledge_base_id`, `file_ext`(无点号)

**响应：** `media_id`, `cos_credential`

---

### add_knowledge
添加知识。

**请求：** `media_type`(int), `title`, `knowledge_base_id`
- 文件时加：`media_id`, `file_info{cos_key, file_size, file_name}`
- 笔记时加：`note_info{content_id}` (media_type=11)
- 网页时加：`web_info{content_id}` (media_type=2)
- 可选：`folder_id`(省略=根目录)

**响应：** `media_id`

---

### get_knowledge_base
**请求：** `ids[]` (1-20个)

**响应：** `infos`{id: KnowledgeBaseInfo}

---

### get_knowledge_list
浏览内容/文件夹。

**请求：** `knowledge_base_id`, `cursor`(首次=""), `limit`(1-50), `folder_id`(省略=根目录)

**响应：** `knowledge_list[]`, `current_path[]`(FolderInfo), `is_end`, `next_cursor`

---

### search_knowledge
**请求：** `query`, `knowledge_base_id`, `cursor`(首次="")

**响应：** `info_list[]`(SearchedKnowledgeInfo), `is_end`, `next_cursor`

---

### search_knowledge_base
**请求：** `query`(空=返回所有), `cursor`(首次=""), `limit`(1-50)

**响应：** `info_list[]{id,name,cover_url}`, `is_end`, `next_cursor`

---

### get_addable_knowledge_base_list
用户要添加但未指定知识库时用。

**请求：** `cursor`(首次=""), `limit`(1-50)

**响应：** `addable_knowledge_base_list[]{id,name}`, `is_end`, `next_cursor`

---

### check_repeated_names
仅文件类型。

**请求：** `params[]{name, media_type}`, `knowledge_base_id`, `folder_id`(省略=根目录)

**响应：** `results[]{name, is_repeated}`

---

### import_urls
**请求：** `knowledge_base_id`, `folder_id`(省略=根目录), `urls[]`(1-10个)

**响应：** `results{url: {ret_code, media_id}}`

> ⚠️ 根目录时**省略folder_id**，不要传knowledge_base_id

---

## 文件大小限制

| 类型 | media_type | 限制 |
|------|-----------|------|
| Excel/TXT/Xmind/MD | 5/13/14/7 | 10MB |
| 图片 | 9 | 30MB |
| 其他 | 1/3/4/15等 | 200MB |

音频额外：最长2小时。
