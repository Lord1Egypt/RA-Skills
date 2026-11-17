# API 参考

**Base URL**：`https://openapi.ihuadai.cn/open/api/v1`
**鉴权**：请求头 `Authorization: <HUADAI_API_KEY>`

所有业务 API 都返回统一 JSON。成功以 `code=200` 为准。

## 搜索笔记

```http
GET https://openapi.ihuadai.cn/open/api/v1/search?query={关键词}&page=1&size=10
Authorization: <HUADAI_API_KEY>
```

curl 示例：

```bash
curl -sS -G "https://openapi.ihuadai.cn/open/api/v1/search" \
  --data-urlencode "query=早起看书" \
  --data-urlencode "page=1" \
  --data-urlencode "size=10" \
  -H "Authorization: $HUADAI_API_KEY"
```

### 搜索响应结构

成功时返回 `code=200`，核心数据在 `data` 字段中：

```json
{
  "code": 200,
  "data": {
    "total": 5,
    "page": 1,
    "size": 10,
    "data": [
      {
        "unique_id": "b_1730000000_a1b2c3d4",
        "type": 1,
        "content": [{ "insert": "笔记正文内容..." }],
        "create_time": 1720000000,
        "update_time": 1720086400,
        "is_collect": 0,
        "is_todo": 0,
        "status": 1
      }
    ]
  }
}
```

**关键字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | int | 匹配总数 |
| `data[].unique_id` | string | 笔记唯一标识，用于更新和查详情 |
| `data[].type` | int | 笔记类型：1=文本、2=图片、3=语音、4=视频 |
| `data[].content` | array | Quill Delta ops 数组，从中提取 `insert` 拼接为文本摘要 |
| `data[].create_time` | int | Unix 秒时间戳 |
| `data[].update_time` | int | 最后更新时间（Unix 秒） |
| `data[].status` | int | 状态：1=正常 |

**提取内容摘要**：`content` 是 Quill Delta 数组，遍历每个 op，取 `insert` 字段拼接即可得到纯文本。

执行要求：

- 无结果时明确回复「未找到」。
- 更新笔记前，优先通过搜索结果确认目标 `unique_id`。
- 不要猜测或生成已有笔记的 `unique_id`。

## 获取笔记详情

```http
GET https://openapi.ihuadai.cn/open/api/v1/block/{unique_id}
Authorization: <HUADAI_API_KEY>
```

curl 示例：

```bash
curl -sS "https://openapi.ihuadai.cn/open/api/v1/block/b_1730000000_a1b2c3d4" \
  -H "Authorization: $HUADAI_API_KEY"
```

返回单条笔记的完整信息，包括 `content`、`attachment`、`children`（追记/子笔记）等字段。

执行要求：

- 在用户明确要求查看某条笔记详情，或更新前需要确认完整内容时调用。
- `unique_id` 必须来自搜索结果或用户明确提供。

## 新建笔记

```http
POST https://openapi.ihuadai.cn/open/api/v1/block/upload-block
Authorization: <HUADAI_API_KEY>
Content-Type: application/json
```

推荐请求体。`content` 可以直接传 Markdown 字符串：

```json
{
  "unique_id": "b_1730000000_a1b2c3d4",
  "type": 1,
  "content": "正文\n",
  "create_time": 1717142400,
  "status": 1,
  "is_collect": 0,
  "is_todo": 0
}
```

兼容请求体。`content` 也可以传 Quill Delta ops：

```json
{
  "unique_id": "b_1730000000_a1b2c3d4",
  "type": 1,
  "content": [
    {
      "insert": "正文\n"
    }
  ],
  "create_time": 1717142400,
  "status": 1
}
```

curl 示例：

```bash
curl -sS -X POST "https://openapi.ihuadai.cn/open/api/v1/block/upload-block" \
  -H "Authorization: $HUADAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"unique_id":"b_1730000000_a1b2c3d4","type":1,"content":"正文\n","create_time":1717142400,"status":1,"is_collect":0,"is_todo":0}'
```

执行要求：

- `unique_id` 必须是新生成的笔记 ID。
- 普通文本笔记使用 `type=1`。
- `create_time` 使用当前 Unix 秒。
- 只有响应 `code=200` 后，才能回复「已保存」。

## 更新笔记

```http
POST https://openapi.ihuadai.cn/open/api/v1/block/update-block
Authorization: <HUADAI_API_KEY>
Content-Type: application/json
```

推荐请求体。`unique_id` 必须来自搜索结果或用户明确提供，`content` 传更新后的完整 Markdown 正文：

```json
{
  "unique_id": "b_xxx",
  "type": 1,
  "content": "更新后的完整正文\n",
  "status": 1,
  "is_collect": 0,
  "is_todo": 0
}
```

兼容请求体：

```json
{
  "unique_id": "b_xxx",
  "type": 1,
  "content": [
    {
      "insert": "更新后的完整正文\n"
    }
  ],
  "status": 1
}
```

curl 示例：

```bash
curl -sS -X POST "https://openapi.ihuadai.cn/open/api/v1/block/update-block" \
  -H "Authorization: $HUADAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"unique_id":"b_xxx","type":1,"content":"更新后的完整正文\n","status":1,"is_collect":0,"is_todo":0}'
```

执行要求：

- 更新前必须确认目标 `unique_id`。
- 如果用户只描述「刚才那条」或「相关那条」，先搜索并确认。
- 请求体应包含更新后的完整正文，避免把增量补充误当成完整内容。
- 只有响应 `code=200` 后，才能回复「已更新」。

## 错误码

| code | 含义 | 处理方式 |
|------|------|----------|
| 200 | 成功 | 写操作可回复已保存/已更新 |
| 400001 | Key 无效 | 引导用户重新创建并配置 API Key |
| 400003 | 无权限 | 告知无权限访问该资源 |
| 400018 | 笔记不存在 | 提示重新搜索确认目标笔记 |
| 400024 | 需有效会员 | 引导用户在话袋开通对应权益 |
| 500000 | 系统错误 | 提示稍后重试 |

## 安全要求

- 不在对话中输出 `HUADAI_API_KEY`。
- 不把 API Key 写入笔记正文。
- 不在 API 调用失败时声称成功。
- 不编造搜索结果、笔记 ID、笔记内容。
