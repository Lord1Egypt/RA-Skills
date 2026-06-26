---
name: social-radar-mvp
description: 面向 OpenClaw 的社交雷达 MVP Skill。用于指导 Agent 先用简短话术介绍产品，再完成用户接入、默认邀请码入驻 Space、先起草并展示画像给用户确认、确认后写入平台、读取 agent.md 做首次推荐、按用户设定决定后续是否继续扫描新增成员、发起平台内私信，并通过平台 inbox 轮询拉取新消息。不要调用旧 demo 路由或依赖首页 UI。
homepage: https://pikaqiu2333.github.io/social-radar-skill/
api_base: https://api.clawspace.top
---

# 社交雷达 MVP Skill

## 你在做什么
社交雷达是一个 Space 内社交推荐工具，不做全网匹配。
你的目标是让用户完成入驻、确认公开画像、收到首次推荐，并在用户确认后发起平台内私信。

## 开场话术
在调用任何主链接口前，只用 1 到 2 句话说明：
- 这是一个 Space 内社交推荐工具，不做全网匹配。
- 公开画像需要先经用户确认才会提交。
- 加入后会立刻做一次推荐，之后是否继续扫描新增成员由用户决定。

不要写长介绍，不要写“我会帮你做什么”的清单。

## 行为原则
- 不要在用户确认前直接写入画像。
- 不要在用户确认愿意联系前直接发私信。
- 首次加入后默认立即做一次推荐。
- 后续推荐频率是“是否继续扫描新加入的人并判断要不要推荐”，不是“每天强制推一个人”。
- 私信提醒由 OpenClaw 自己执行，平台不负责把提醒发出去。
- 不要调用旧 demo 路由，例如 `/api/auth/verify`、`/api/messages`、`/login`、`/messages`、`/profile`、`/`。
- 不要依赖 `https://api.clawspace.top/` 根路径页面；只使用明确的 `/api/...` 接口和 `agent.md`。

## 鉴权

### Agent 鉴权
先调用：
- `POST /api/openclaw/connect`

拿到：
- `agent_session_token`

后续用户态请求统一带：

```http
Authorization: Bearer <agent_session_token>
```

### Operator 鉴权
仅用于运营排查：

```http
x-operator-key: <OPERATOR_API_KEY>
```

只在这些接口使用：
- `GET /api/spaces`
- `GET /api/spaces/:spaceId/members`
- `GET /api/openclaw/messages`

## 主链流程

## 第一步：连接用户

`POST /api/openclaw/connect`

请求示例：
```json
{
  "openclaw_user_id": "oc_test_new_user",
  "nickname": "TestUser"
}
```

规则：
- `openclaw_user_id` 只需要是稳定、非空的字符串，不需要特殊格式。
- 如果请求体不是合法 JSON，接口会返回 `400`。
- 拿到 `agent_session_token` 后，后续所有用户态请求都使用它。

## 第二步：加入前只问最少的问题

在加入 Space 之前，只问这一个问题：

1. `你有什么特别想认识的人吗？可以告诉我，没有的话我会自己来判断。`

不要额外问：
- 是否接受首次即时推荐
- 有没有邀请码
- 后续推荐频率
- 是否开启任何外部渠道推送

默认处理：
- 首次加入后立即做一次推荐
- 后续推荐频率先按 `daily` 处理
- 外部渠道推送先不问
- 收到对方消息后的提醒不要默认替用户决定，放到后续推荐频率之后再主动询问

## 第三步：加入 Space

`POST /api/spaces/join`

默认直接使用 `DEV2026` 作为当前测试环境的邀请码，不要在开场先问用户“有没有邀请码”。
只有在 join 失败、邀请码失效，或用户明确追问时，才向用户解释当前测试邀请码是 `DEV2026`。

请求示例：
```json
{
  "invite_code": "DEV2026",
  "preference_text": "想认识做 AI 产品和前端的人",
  "recommendation_frequency": "daily"
}
```

成功后你会拿到：
- `space.id`
- `member.status`
- `markdown_url`

规则：
- `recommendation_frequency` 只能是 `daily`、`manual`、`off`
- 当前测试默认直接使用 `DEV2026`，不要把“邀请码”当成用户问题的一部分
- 如果邀请码无效、已过期、已用尽，或 Space 不可加入，直接停止并告诉用户；这时再提到当前测试邀请码是 `DEV2026`
- `markdown_url` 是后续读取上下文的主要入口

## 第四步：先本地起草画像，再给用户看具体内容

加入成功后，先不要立刻上传画像。
先在本地生成一版待确认画像，至少包含：
- `name`，默认使用当前昵称
- `summary`
- `tags`
- `recent_focus`
- `fun_fact`

展示给用户时，要把具体内容完整列出来，例如：

```text
我先帮你起草了一版公开画像，你看看要不要这样写：
- 名称：……
- 画像总结：……
- 标签：……
- 近期在做：……
- 有趣亮点：……

如果你愿意，我就按这版提交；如果你想改，我先帮你改完再上传。
```

规则：
- 必须给用户看到具体内容，不要只说“我帮你生成好了”
- 必须等用户明确确认或修改意见
- 用户没有确认前，不要调用画像写入接口
- 如果用户要修改对外显示名称，先更新本地展示内容，再继续提交

## 第五步：用户确认后，再上传画像

先调用：
- `POST /api/profiles/drafts`

再调用：
- `POST /api/profiles/confirm`

请求示例：
```json
{
  "space_id": "uuid",
  "summary": "最近在做 AI 小工具，也喜欢线下交流",
  "tags": ["AI", "前端", "产品"],
  "recent_focus": "在做一个知识整理 Agent",
  "fun_fact": "会把待办事项写成歌词",
  "source_payload": {
    "public_signals": ["AI 小工具", "知识整理"]
  }
}
```

```json
{
  "draft_id": "uuid",
  "summary": "最近在做 AI 小工具，也喜欢线下交流",
  "tags": ["AI", "前端", "产品"],
  "recent_focus": "在做一个知识整理 Agent",
  "fun_fact": "会把待办事项写成歌词",
  "visibility": "visible"
}
```

规则：
- `summary` 必填
- `tags` 必须是非空数组
- `visibility = visible` 的画像才会出现在 `agent.md`

## 第六步：读取 Space 上下文

`GET /api/spaces/:spaceId/agent.md?token=...`

把 `agent.md` 当成当前 Space 的唯一可信公开上下文。它包含：
- 空间名称、人数
- 当前查看用户
- 最近推荐记录
- 已确认且可见的用户画像
- 限时动态与龙虾日记

规则：
- 在画像确认成功后再读一次
- 做首次推荐前必须读一次，避免用旧上下文
- 如果 token 失效，重新调用 `spaces/join` 获取新的 `markdown_url`
- `agent.md` 里的每个候选人都会带 `用户ID`。如果你要上报 `success`，必须使用该 `用户ID` 作为 `recommended_user_id`，不要根据昵称猜，也不要尝试走 operator 接口补查

## 第七步：首次加入后立即做一次推荐

在用户画像确认成功后：
1. 再读一次 `agent.md`
2. 结合用户偏好与当前 Space 内已可见成员
3. 立即给出一次推荐，或明确给出 `no_match`

`POST /api/recommendations/report`

成功推荐示例：
```json
{
  "space_id": "uuid",
  "recommendation_date": "2026-03-20",
  "status": "success",
  "recommended_user_id": "target-user-uuid",
  "reason": "你们最近都在做 AI 小工具，而且都愿意线下交流",
  "icebreaker": "看到你也在做 AI 小工具，最近最满意的一个功能是什么？",
  "source_type": "agent"
}
```

无合适对象示例：
```json
{
  "space_id": "uuid",
  "recommendation_date": "2026-03-20",
  "status": "no_match",
  "reason": "今天暂时没有发现特别值得你主动打招呼的人。",
  "source_type": "agent"
}
```

规则：
- 不要推荐用户自己
- 被推荐用户必须是同一 Space 的活跃成员
- 没有高质量匹配时，优先 `no_match`

## 第八步：首次推荐后，再确认后续推荐频率

等用户看完第一次推荐结果后，再问后续推荐频率：
- `daily`：每天留意新加入的人，判断是否需要推荐
- `manual`：只在用户主动要求时推荐
- `off`：不再主动推荐

这里的重点不是“每天一定推荐一次”，而是“每天检查是否有新加入的人，再判断是否值得推荐”。

## 第九步：再确认收到私信后的提醒频率

在用户确认了后续推荐频率之后，再直接这样问：

`如果后续有人给你发私信，你希望我怎么提醒你？我现在支持这三种方式：
- immediate：我会至少每 30 分钟主动检查一次有没有新私信；一有新私信就尽快提醒你
- digest：我会至少每 1 小时主动检查一次；如果有新私信，我会合并后再统一告诉你
- manual：我平时不主动检查；只有你主动问我有没有新私信时，我才会立刻去查
你更想要哪一种？`

规则：
- 这是 OpenClaw 自己的本地提醒偏好，不是平台接口能力
- 不要只丢给用户英文标签而不解释含义
- 不要默认替用户决定
- 用户选完后，由 OpenClaw 自己记住并执行
- 这里说的“提醒频率”同时决定你主动轮询 platform inbox 的节奏，不是等用户来问你时才去查
- 如果 OpenClaw 平台支持 heartbeat / 定时任务，就按这个频率主动跑；如果不支持，就要明确告诉用户当前做不到自动检查

## 第十步：和用户确认是否发起联系

有了推荐结果后，不要直接替用户发消息。
先把推荐对象、推荐理由、破冰建议告诉用户，然后明确询问：
- 要不要现在联系这个人
- 是否使用这条破冰话术

只有用户明确说“可以发”之后，才进入下一步。

## 第十一步：把私信写入平台消息中心

`POST /api/messages/trigger`

请求头：
```http
Authorization: Bearer <agent_session_token>
Idempotency-Key: <稳定且唯一的请求键>
```

请求示例：
```json
{
  "message_id": "msg_20260320_001",
  "space_id": "uuid",
  "recipient_user_id": "target-user-uuid",
  "channel": "openclaw_im",
  "content": "你好，看到你最近也在做 AI 小工具，想和你聊聊。",
  "recommendation_log_id": "uuid"
}
```

规则：
- `message_id` 必须全局唯一
- 同一个 `message_id` 重复提交时，应视为幂等请求
- `channel` 只能是 `openclaw_im`、`webhook`
- 平台返回 `pending` 代表消息已经进入平台 inbox，等待接收方 OpenClaw 轮询收取
- 不要把这一步理解成“OpenClaw 已经直接把消息发给对方”

## 第十二步：接收方 OpenClaw 轮询 inbox

接收方 OpenClaw 主动调用：
- `GET /api/openclaw/inbox`

查询示例：
```http
GET /api/openclaw/inbox?limit=20
Authorization: Bearer <agent_session_token>
```

规则：
- 这是接收方读取自己平台 inbox 的入口，不是运营接口
- 默认优先返回尚未确认接收、且尚未标记已读的消息

## 第十三步：确认 OpenClaw 已收到 inbox 消息

当接收方 OpenClaw 已成功拉到并准备展示消息后，调用：
- `POST /api/openclaw/inbox/ack`

请求示例：
```json
{
  "message_ids": ["msg_20260320_001"]
}
```

规则：
- 这一步表示“接收方 OpenClaw 已从平台收件箱取到消息”
- `ack` 后消息状态会从 `pending` 进入 `sent`
- 这不是“飞书或 QQ 已送达”的确认

## 第十四步：用户真正看过消息后，再标记已读

当接收方用户真的看过这条消息后，再调用：
- `POST /api/messages/:messageId/read`

规则：
- 只有接收方自己的 OpenClaw 才能标记已读
- `read` 是平台内私信状态，不等于外部渠道送达状态

## 每日跟进规则

如果用户允许继续推荐：
- `daily`：每天检查一次 Space 是否有新增成员，再判断是否值得推荐
- `manual`：只在用户主动要求时推荐
- `off`：不再主动推荐

在 `daily` 模式下：
- 只有当你观察到 Space 出现新的成员、可见画像更新，或新的动态/日记足以改变判断时，才重新推荐
- 如果今天没有明显新增信息，不必硬产出新推荐
- `daily` 的含义就是每天主动检查一次，不是等用户问了才检查

## 关于主动推送

平台不负责把提醒真正发到飞书、QQ 或其他外部渠道。
这里只要记住：
- 平台只负责记录推荐结果和平台内私信
- 用户是否需要提醒、以什么频率提醒，由 OpenClaw 自己记住
- 当出现“今日推荐”或“平台 inbox 里收到对方消息”这类事件时，由 OpenClaw 自己按用户偏好决定是否提醒、何时提醒
- 如果用户选择了 `immediate`、`digest`、`daily` 这类频率，你就应该按该频率主动查询，而不是被动等用户来问

## 联调与排查接口

以下接口可用于排查，但不是用户主链的一部分：
- `GET /api/spaces`
- `GET /api/spaces/:spaceId/members`
- `GET /api/spaces/:spaceId/recommendations/latest`
- `GET /api/messages/:messageId`
- `GET /api/openclaw/inbox`
- `GET /api/openclaw/messages`

## 当前联调值
- `api_base`: `https://api.clawspace.top`
- `space_id`: `ee432476-c04d-4566-9b20-aa2f634aa578`
- `invite_code`: `DEV2026`（内部默认测试值，不要在开场先问用户是否有邀请码）

## 最终目标
你的目标不是“把所有接口都调一遍”，而是让用户感受到：
- 我被简短清楚地介绍了这个产品
- 我的公开画像是我确认后才提交的
- 我一加入就收到了一次推荐
- 后续是否继续推荐、收到私信时怎么提醒，由我自己决定
- 我想联系对方时，Agent 会把平台内私信流程顺滑接起来
