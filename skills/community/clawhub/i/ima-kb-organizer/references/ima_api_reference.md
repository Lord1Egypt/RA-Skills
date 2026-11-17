# IMA MCP 工具能力参考

## 可用工具

### mcp__ima-mcp__get_knowledge_base_list
获取用户的 IMA 知识库列表。

**参数：**
- `params`: 数组，每个元素包含：
  - `limit`: int - 返回数量上限
  - `type`: string - 知识库类型，如 `"KBT_MINE_KB"`

**返回：** 知识库列表，含 `kb_id`、`kb_name`、`kb_type` 等。

---

### mcp__ima-mcp__get_knowledge_list
获取指定知识库中的内容列表。

**参数：**
- `knowledge_base_id`: string - 知识库 ID
- `limit`: int - 每页数量（建议 50）
- `sort_type`: string - 排序方式，如 `"UPDATE_TS_DESC_SORT_TYPE"`
- `next_cursor`: string（可选）- 翻页游标

**返回：** 内容列表，每项含 `media_id`、`title`、`introduction`、`source`、`type`（WECHAT_ARTICLE / WEB / IMG 等）。`is_end` 为 true 时表示无更多内容。

---

### mcp__ima-mcp__search_knowledge
在知识库中搜索内容。

**参数：**
- `knowledge_base_id`: string - 知识库 ID
- `query`: string - 搜索关键词
- `limit`: int - 返回数量

**返回：** 匹配的内容列表，含相关性排序。

---

### mcp__ima-mcp__fetch_media_content
获取指定资料的全文内容。

**参数：**
- `media_id`: string - 资料 ID
- `knowledge_base_id`: string - 所在知识库 ID

**返回：** 资料的完整文本内容，可用于 RAG 上下文。

---

### mcp__ima-mcp__add_knowledge
向知识库添加知识内容。

**参数：**
- `knowledge_base_id`: string - 目标知识库 ID
- `content`: string - 内容
- `title`: string - 标题

---

### mcp__ima-mcp__import_urls
批量导入网页 URL 到知识库。

**参数：**
- `knowledge_base_id`: string - 目标知识库 ID
- `urls`: array - URL 列表（最多 10 条/次）

---

### mcp__ima-mcp__create_media
创建媒体内容（上传文件）。

---

### mcp__ima-mcp__get_addable_knowledge_base_list
获取可添加内容的知识库列表。

---

## API 限制

| 操作 | 支持 | 说明 |
|------|------|------|
| 列出知识库 | ✅ | get_knowledge_base_list |
| 列出内容 | ✅ | get_knowledge_list，支持翻页 |
| 搜索内容 | ✅ | search_knowledge |
| 获取全文 | ✅ | fetch_media_content |
| 添加知识 | ✅ | add_knowledge |
| 导入 URL | ✅ | import_urls，最多 10 条/次 |
| 上传文件 | ✅ | create_media |
| **删除内容** | ❌ | 不支持，需在 IMA 客户端手动操作 |
| **移动内容** | ❌ | 不支持 |
| **创建文件夹** | ❌ | 不支持 |
| **打标签** | ❌ | 不支持 |
| **重命名知识库** | ❌ | 不支持 |

## 应对策略

因 IMA API 不支持物理整理（删除/移动/文件夹），本 skill 采用**逻辑分类**方案：
- 用本地 `tracker.json` 追踪每篇内容的分类归属
- 用 Word/Markdown 索引文档替代物理文件夹
- RAG 时通过 media_id 从 IMA 拉取全文，不依赖物理位置
