# 搜索笔记（Search）

## 何时使用

- 用户要“搜一下/找一下/有哪些相关笔记”
- 用户记不清笔记标题或 ID，希望按语义描述找相关内容

## 接口（本页覆盖）

- `GET /open/api/v1/search`

## 通用请求头（必须）

见 [配置（必须先完成）](config.md#你需要准备什么)：

- `USER-UUID: <user_unique_id>`
- `Authorization: <api_key>`

---

## 全文检索

```
GET {BASE_URL}/search?query=...&page=1&size=10
```

Query 参数（常用）：

| 参数 | 类型 | 说明 |
|------|------|------|
| `query` | string | 搜索关键词（可为空） |
| `page` | int | 页码，默认 1 |
| `size` | int | 每页数量，默认 10，最大 100 |
| `search_type` | string | `keyword` / `script` / `custom`（默认 `custom`） |
| `sort_by` | string | `_score` / `create_time` / `update_time` |
| `sort_order` | string | `asc` / `desc` |
| `enable_highlight` | bool | 是否高亮 |

返回结构（概览）：

```json
{
  "code": 200,
  "message": "请求成功",
  "data": {
    "total": 0,
    "page": 1,
    "size": 10,
    "total_pages": 0,
    "data": []
  }
}
```

---

## 结果呈现建议（对用户）

- 默认展示前 5 条
- 每条至少包含：
  - `title`
  - `created_at`
  - `content` 片段
  - `note_id`（当 `note_type=NOTE` 时才可用于后续调详情）

## 空结果

- 必须明确告知“未找到”
- 给出下一步：换关键词、缩短 query、或增加限定词

## 常见错误

见 [话袋笔记 API 详细参考 · 错误码表](api-details.md#错误码表code)：

- `400000`：参数/业务校验失败
- `400003`：无权限
- `500000`：系统错误

