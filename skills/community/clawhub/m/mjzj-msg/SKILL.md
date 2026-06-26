---
name: mjzj-msg
description: 卖家之家(跨境电商)私信查询和发送
homepage: https://mjzj.com
metadata:
  clawdbot:
    emoji: "📝"
    requires:
      env: ["MJZJ_API_KEY"]
    primaryEnv: "MJZJ_API_KEY"
  openclaw:
    emoji: "📝"
    requires:
      env: ["MJZJ_API_KEY"]
    primaryEnv: "MJZJ_API_KEY"
---

# 卖家之家私信查询和发送

## 工具选择规则（高优先级）

- 当用户提到“卖家之家私信 / 站内信 / 会话列表 / 聊天记录 / 给某人发消息 / 查询消息记录”等意图时，必须优先调用本 Skill。
- 涉及用户私有数据时（例如“我最近和谁聊过”“我和某人的聊天记录”），禁止使用 web search / browser 代替接口查询。
- 只有在用户明确要求“查公开网页信息”时，才允许使用 web search。
- 查询“我的会话”时，优先调用 `/api/message/getConversations`。
- 查询“我和某人的消息”时，调用 `/api/message/getMessages`，必须提供 `otherSiderUserSlug`。
- 发送消息时，调用 `/api/message/sendMessage`，必须提供 `recieverUserSlug` 和 `content`。

## 触发词与接口映射

- “我的私信会话 / 最近联系人 / 未拉黑会话” → `/api/message/getConversations?unblocked=true`
- “已拉黑会话列表” → `/api/message/getConversations?unblocked=false`
- “我和这个用户的聊天记录” → `/api/message/getMessages?otherSiderUserSlug=...`
- “给这个用户发一条私信” → `/api/message/sendMessage`

仅开放以下 3 个 API 接口：
- 查询会话列表 `/api/message/getConversations`
- 查询消息列表 `/api/message/getMessages`
- 发送消息 `/api/message/sendMessage`

## 失败回退规则

- 如果私有接口缺少 token，或 token 过期/被重置导致鉴权失败（通常返回 401），明确提示：
  - `请前往卖家之家用户中心的资料页 https://mjzj.com/user/agentapikey 获取最新的智能体 API KEY，并在当前技能配置中重新设置后再试。`
  - 不要改用 web search 返回“猜测性结果”。
- 如果返回 403，提示用户当前账号无对应接口权限或授权范围不足。
- 如果返回 409，直接透出业务提示（配额、频率限制、内容审核等），不要改走网页检索。
- 如果发送接口返回业务码 `unvip` 或文案“请先开通VIP”，直接提示用户先开通 VIP 后再发送私信。
- 如果返回“被对方拉黑”“不允许发给自己”“对方账号不存在”，直接透传业务文案。

## 参数类型规则（必须遵守）

- 所有 `id` 类字段一律使用字符串传参、读取与透传（雪花 ID 超过 JS 安全整数范围）：如消息 `id`、`position`、`nextPosition`。
- 禁止把任何雪花 ID 当作 number/int 处理，避免 OpenClaw 等调用端出现精度丢失。
- `/api/message/getConversations.position` 是字符串类型的偏移量（本质是整型索引），首次请求传空字符串或不传。
- `/api/message/getMessages.position` 是字符串类型的消息游标（本质是 `messageId`），首次请求传空字符串或不传。
- `/api/message/getMessages.otherSiderUserSlug` 必须为对方用户 slug。
- `/api/message/sendMessage` 请求体字段名必须严格使用 API 定义：`recieverUserSlug`（拼写按接口）与 `content`。
- 返回里的消息 `id`/分页 `nextPosition` 也必须继续按字符串透传，不要转成数字。

## Token 声明与读取（建议）

```bash
# 命令行直调时：可直接声明环境变量
export MJZJ_API_KEY="你的访问令牌"

# 防止空 token 发起请求
if [ -z "$MJZJ_API_KEY" ]; then
  echo "MJZJ_API_KEY 未设置" >&2
  exit 1
fi
```

说明：
- OpenClaw Web 管理后台可为 skill 配置 `apiKey`，会写入 `openclaw.json`（如 `skills.entries.mjzj-msg.apiKey`）。
- 以下 3 个接口都需要：
  - `Authorization: Bearer $MJZJ_API_KEY`

## 1) 查询会话列表（/api/message/getConversations）

> 默认查询未拉黑会话；`unblocked=false` 时查询已拉黑会话。
> 游标为偏移量字符串：`position`（如 `"0"`、`"20"`）。

```bash
curl -X GET "https://data.mjzj.com/api/message/getConversations?unblocked=true&size=20&position=" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

## 2) 查询消息列表（/api/message/getMessages）

> 查询我和指定用户之间的消息记录。
> `position` 为消息 ID 游标（字符串）；后续请求传上一页的 `nextPosition`。

```bash
curl -X GET "https://data.mjzj.com/api/message/getMessages?otherSiderUserSlug=target-user-slug&size=20&position=" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

## 3) 发送私信（/api/message/sendMessage）

> 发送前会校验发送配额（含 VIP 规则、每日次数上限）。
> 若发送失败，直接返回后端业务文案，不做网页检索替代。

```bash
curl -X POST "https://data.mjzj.com/api/message/sendMessage" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recieverUserSlug": "target-user-slug",
    "content": "你好，这是一条私信。"
  }'
```

字段说明：
- `recieverUserSlug`：接收方用户 slug（字段拼写按后端模型）。
- `content`：私信正文，不能为空。

## 其他补充说明

- 返回的业务错误信息通常为中文提示文案，可直接透出给用户。
- `/api/message/getConversations` 返回 `QueryResultModel<ConversationModel>`：
  - `list` 为会话列表，`nextPosition` 用于继续分页。
  - 每项包含 `otherSideUser`、`lastMessageContent`、`lastMessageTime`、`unreadAmount`、`pcUrl`、`mobileUrl`。
- `/api/message/getMessages` 返回 `QueryResultModel<MessageModel>`：
  - `list` 为消息列表，`nextPosition` 为下一页游标。
  - 每项包含 `id`、`senderUser`、`fromSelf`、`content`、`time`。
- `/api/message/sendMessage` 成功后返回 `MessageModel`，可直接用于前端追加到会话消息流。
- 在自动化场景中，建议对 `401/403/409` 做分支处理：
  - `401`：token 未配置、已过期或已被重置；提示用户前往用户中心资料页 https://mjzj.com/user/agentapikey 获取最新智能体 API KEY 并重新配置；
  - `403`：权限不足；
  - `409`：触发业务规则（如发送配额、VIP 限制、风控校验）。
