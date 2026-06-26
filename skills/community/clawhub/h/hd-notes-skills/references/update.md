# 更新笔记（Update）

## 何时使用

- 用户需要对已有笔记进行更新（正文/属性等）

## 接口（本页覆盖）

本页以话袋后端原生接口为准：统一使用 `/v1` 前缀。

- `POST /open/api/v1/block/update-block`：更新 Block 笔记（内容/属性）

## 通用请求头（必须）

见 [配置（必须先完成）](config.md#你需要准备什么)：

- `USER-UUID: <user_unique_id>`
- `Authorization: <api_key>`
- `Content-Type: application/json`（仅 POST 且 body 为 JSON 时需要）

---

## 更新笔记（Block）

```
POST {BASE_URL}/block/update-block
Content-Type: application/json
```

请求体（字段详解见 [话袋笔记 API 详细参考 · 更新笔记（Block）](api-details.md#更新笔记block)）：

```json
{
  "unique_id": "b_xxx",
  "type": 1,
  "content": [],
  "attr": {}
}
```

返回说明：
- 同步完成：返回 `code=200`

---

## 成功判定（必须）

- 必须以 API 返回 `code=200` 为准；未拿到明确成功响应前，禁止回复“已更新”

## 常见错误

见 [话袋笔记 API 详细参考 · 错误码表](api-details.md#错误码表code)：

- `400000`：参数/业务校验失败
- `400003`：无权限
- `400018`：笔记不存在（部分场景会返回业务 message）
- `500000`：系统错误

