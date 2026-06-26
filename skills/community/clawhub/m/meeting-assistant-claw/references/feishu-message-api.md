# 飞书消息 API 速查

## 认证

获取 tenant_access_token：

```bash
curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"'"$FEISHU_APP_ID"'","app_secret":"'"$FEISHU_APP_SECRET"'"}' \
  | jq -r '.tenant_access_token'
```

Token 有效期 2 小时，建议缓存复用。

## 发送消息

**端点：** `POST /im/v1/messages?receive_id_type=open_id`

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxxxxxxxxxxxxxxx",
    "msg_type": "text",
    "content": "{\"text\":\"你好\"}"
  }'
```

### msg_type 支持类型

| 类型 | content 格式 | 说明 |
|------|-------------|------|
| `text` | `{"text":"内容"}` | 纯文本 |
| `interactive` | `{飞书卡片 JSON}` | 富文本卡片 |
| `post` | `{飞书富文本 JSON}` | 富文本帖子 |

### 飞书卡片模板（待办通知）

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "📋 会议待办通知"},
    "template": "blue"
  },
  "elements": [
    {
      "tag": "div",
      "fields": [
        {"is_short": true, "text": {"tag": "lark_md", "content": "**来源会议**\n产品评审"}},
        {"is_short": true, "text": {"tag": "lark_md", "content": "**日期**\n3月26日"}}
      ]
    },
    {"tag": "hr"},
    {
      "tag": "div",
      "text": {"tag": "lark_md", "content": "**待办事项：**\n完成 XX 功能的技术方案文档"}
    },
    {
      "tag": "div",
      "text": {"tag": "lark_md", "content": "**截止时间：**\n3月30日前"}
    },
    {"tag": "hr"},
    {
      "tag": "note",
      "elements": [
        {"tag": "plain_text", "content": "由会议助理虾自动提取并发送"}
      ]
    }
  ]
}
```

多条待办卡片：用多个 `elements` 数组中的 `div` 重复待办条目。

## 查找用户 open_id

### 方法 1：按部门搜索（推荐）

```bash
# 搜索根部门（department_id=0）下的所有用户
curl -s -X GET "https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50&user_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN"
```

响应中 `.data.items[]` 包含每个用户的 `name` 和 `open_id`，用 jq 过滤：

```bash
curl -s "..." | jq -r '.data.items[] | select(.name=="张三") | .open_id'
```

### 方法 2：已知 open_id 直接发

如果从消息上下文或其他渠道已知 open_id，直接用于 `receive_id`。

### 方法 3：批量获取

```bash
POST /contact/v3/users/batch_get_id
{
  "user_ids": ["user_id_1", "user_id_2"],
  "user_id_type": "open_id"
}
```

## 消息类型参考

### 纯文本消息

```json
{
  "msg_type": "text",
  "content": "{\"text\":\"请在本周五前提交方案。\"}"
}
```

### @某人（在群聊中）

```json
{
  "msg_type": "text",
  "content": "{\"text\":\"<at user_id=\\\"ou_xxx\\\">张三</at> 请在本周五前提交方案。\"}"
}
```

## 错误码

| code | 含义 |
|------|------|
| 0 | 成功 |
| 99991668 | 没有对应应用的发送消息权限 |
| 99991672 | 接收者不是应用可见范围内的用户 |
| 99991673 | 接收者已禁用 |
| 99991664 | 内容过长 |
| 2238 | 群已解散 |

## 注意事项

- `content` 字段是**转义后的 JSON 字符串**（双重编码），发送时注意转义
- `receive_id_type` 可选：`open_id`、`user_id`、`union_id`、`chat_id`
- 单个用户每天发送上限约 500 条（应用维度）
- 飞书卡片内容需为合法 JSON，注意特殊字符转义
