# linkfox-os API 参考

`linkfox-os` 通过 LinkFox Agent 平台的 **AgentStudio 异步任务接口**（路由前缀 `/agent-studio/task`）提交 prompt 并轮询结果。

接口约定：
- 提交入参 `{prompt, modelId}`，返回任务 ID 字段为 **`id`**。
- 轮询返回 `MessageGetVo`，含 `message` + `eventList` + `eventTotal`；无 `status` / `progress` / `shareUrl` / `results[]` 字段。
- 终态判定：`message.stopReason` 非空（`end_turn` = 正常完成，其他值为异常终止）；结果在 `message.agentMessageChunks[].content`。

## 认证

- 环境变量：`LINKFOXAGENT_API_KEY`
- 请求头：
  - `Authorization: <LINKFOXAGENT_API_KEY>`
  - `Content-Type: application/json`
  - `User-Agent: linkfox-os-skill/1.0`

BASE_URL：默认 `https://agent-api.linkfox.com/`，可通过环境变量 `LINKFOXAGENT_BASE_URL` 覆盖。

## 响应外层包装（errcode / errmsg）

所有接口的响应体在业务字段之外还带统一的包装字段，两者**平铺在同一层**：

| 字段 | 说明 |
|---|---|
| `errcode` | 业务码。`200`（或 `0` / 缺省）= 成功；其他值 = 失败（如 `401` 用户中心鉴权失败、`500` 服务端异常）。**成功也是 HTTP 200 + `errcode:200`**，不是 HTTP 错误码。 |
| `errmsg` | 文案。成功为 `"ok"`；失败为错误描述。 |

脚本据此判断：`errcode` 非 200/0 时视为业务错误并报错；成功时原样返回（VO 字段 + `errcode/errmsg` 同层）。例：`create` 成功响应为 `{errcode:200, errmsg:"ok", id:"...", sessionId:"...", stopReason:"", agentMessageChunks:[], ...}`。

---

## 接口一：异步创建任务

`POST /agent-studio/task/create`

提交一个 prompt，立即返回任务 ID（pending 态），任务在服务端异步执行。

### 请求

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `prompt` | string | 是 | 提示词 / 任务描述 |
| `modelId` | string | 否 | 模型 ID，默认 `default` |

```json
{
  "prompt": "在亚马逊美国站搜索 usb charger cable，返回前 40 条",
  "modelId": "default"
}
```

### 响应：`PromptAsyncExecuteVo`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | **消息/任务 ID，用于后续 `/get` 查询**（注意字段名是 `id`，脚本内部转写为 `messageId` 落盘） |
| `sessionId` | string | 会话 ID |
| `stopReason` | string | 停止原因，**提交时为空**（任务完成后才填充，如 `end_turn`） |
| `agentMessageChunks` | list | Agent 消息分块，**提交时为空** |
| `userMessageChunks` | list | 用户消息分块 |
| `eventCount` | int | 事件数量 |
| `toolCount` | int | 工具调用次数 |
| `createdAt` | string | 创建时间 |
| `updatedAt` | string | 更新时间 |

提交成功后，把 `id` 当作 `messageId` 用于下面的查询接口。

---

## 接口二：查询任务

`POST /agent-studio/task/get`

按 `messageId` 查询任务执行结果与状态，返回聚合结构 `MessageGetVo`。

### 请求

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `messageId` | string | 是 | 任务 ID（即 create 返回的 `id`） |
| `fromIndex` | int | **是** | 增量拉取起点下标（从 0 开始）。首轮 poll 传 0，之后传"上一响应的 `eventTotal`"，服务端仅回 `eventList[fromIndex : eventTotal]` 切片，避免每次全量回传上百条事件。**目前后端注解为必填**，缺失会返回 `errcode=400 fromIndex 为必填参数`；负数由后端归一为 0 |

```json
{ "messageId": "uDqHg33fQeQfkNB5pj5LLA", "fromIndex": 12 }
```

**增量语义**：
- 服务端 `eventList` 由 AgentStudio 上游全量拉回（上游不支持增量），本层只做**切片返回**；
- 上游 acpEvent 会"后填充"（`tool_call` 的 `title` 由占位 `Skill` 解析成技能名、消息 chunk 的 `content.text` 分片追加），客户端建议每轮 `fromIndex = max(0, eventTotal - 5)` 保留几条重叠窗口，避免漏掉后填充；再按事件绝对下标做内容去重。
- `--poll` / `poll_result` 走增量；`--status` / `--watch` 是 stateless 场景，脚本主动传 `fromIndex=0`（拉全量事件用于快照 / progress 签名）。

### 响应：`MessageGetVo`

```json
{
  "message": { ... MessageItemVo ... },
  "eventList": [ ... AcpEventItemVo（切片） ... ],
  "eventTotal": 27
}
```

`eventTotal` 是服务端切片前的累计事件总数，客户端下次请求把这个值传回 `fromIndex` 即可继续增量拉取。

#### `message`：`MessageItemVo`（核心字段）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 消息 ID |
| `stopReason` | string | **停止原因——终态判断依据**。为空 = 任务仍在处理中；非空 = 任务结束（`end_turn`=正常完成，`max_tokens`/`error` 等其他值视情况判定） |
| `agentMessageChunks` | list | **Agent 消息分块——最终结果载体**。任务完成后填充，每项是 `{content: {type, ...}}`（见下） |
| `userMessageChunks` | list | 用户消息分块 |
| `usageUpdate` | map | 用量更新 |
| `toolCount` | int | 工具调用次数 |
| `eventCount` | int | 事件数量 |
| `createdAt` | string | 创建时间 |
| `updatedAt` | string | 更新时间 |

#### `eventList`：`AcpEventItemVo[]`（任务进行中过程事件）

后端调用 `app/agent/message/acpEvent/get`（`appMessageEventList`）拉取处理中事件放入此列表，供调用方展示思考/工具调用过程。当前后端**无条件**拉取（终态时也非空），但终态结果应以 `message.agentMessageChunks` 为准，`eventList` 仅供过程回放。

> 注意：`sessionUpdate` 是**类型标记字符串**（不是 map），真实内容在 `content` 或 tool_call 的平级字段。

| 字段 | 类型 | 说明 |
|---|---|---|
| `sessionUpdate` | string \| null | 事件类型标记：`agent_thought_chunk` / `agent_message_chunk` / `tool_call` 等；部分事件为 `null` |
| `content` | object | 事件内容（多态）：thought/message chunk 为 `{text, type}`；`tool_call` 为 `{}`（工具信息见平级字段） |
| `title` | string | tool_call 专用：工具/技能标题（如 `linkfox-amazon-search`） |
| `kind` | string | tool_call 专用：`execute` / `read` / `other` |
| `status` | string | tool_call 专用：`completed` / `in_progress` |
| `toolCallId` | string | tool_call 专用：工具调用 ID |
| `rawInput` | object | tool_call 专用：原始入参（如 `{skill, args}`） |
| `rawOutput` | object | tool_call 专用：原始输出 |
| `_meta` | object | tool_call 专用：元信息（agentId / agentStudio 等） |

---

## 终态判断与结果提取

### 终态
- `message.stopReason` 为空 → 任务进行中，继续轮询；进度信息从 `eventList[]` 提取（见下"进度提取"）。
- `message.stopReason` 非空 → 任务结束：
  - `end_turn` → 正常完成，读 `agentMessageChunks`。
  - `max_tokens` / `error` / 其他 → 异常终止，仍读 `agentMessageChunks`（可能有部分结果），并提示 stopReason。

### 进度提取（进行中）

`eventList[]` 每项是 `AcpEventItemVo`，按 `sessionUpdate` 类型取可读文本：

| `sessionUpdate` | 取值位置 | 示例 |
|---|---|---|
| `agent_thought_chunk` / `agent_message_chunk` | `content.text`（或 `content.value`） | `"The user wants to search for..."` |
| `tool_call` | 平级字段 `title` + `rawInput.args` | `[Tool] linkfox-amazon-search (keyword=wireless earbuds site=US)` |
| `null`（消息片段） | `content.text` | `"Launching skill: linkfox-amazon-search"` |

> `sessionUpdate` 本身只是类型标记字符串，**不是** map，不要从中 `.get(key)` 取进度。脚本 `parse_progress` / `extract_progress` 据此实现。

### 结果提取：`agentMessageChunks[].content`

每个 chunk 形如 `{content: {type, ...}}`，按 `type` 解析：

| `content.type` | 关键字段 | 处理方式 |
|---|---|---|
| `text` | `content.text`（或 `content.value`） | 直接作为文本结果输出 |
| `resource_link` | `content.uri` | 资源公开 URL，原样输出 |
| `tool_call` | `content.name` 等 | 工具调用摘要，输出 `[Tool: <name>]` |
| 其他 | — | 一行 JSON 摘要兜底 |

> `resource_link` 的 `uri` 已由后端从 `file://` 转为可直接访问的 HTTP 公开 URL。转换结果按 `(groupId, memberId, fileUri)` 在 Redis 缓存 2h，同一 fileUri 短时间内重复查询直接命中，不回源上游。

---

## 错误处理

- HTTP 401/403 → `LINKFOXAGENT_API_KEY` 失效或未设置，脚本会提示获取并重新配置。
- 提交返回中无 `id` → 视为发起失败，脚本退出码 1 并打印服务器原始响应。
- 轮询超时（超过 `--timeout`）→ 返回 timeout 错误，建议用 `--status` 单次查询或加大 `--timeout` 继续 `--poll`。

---

## 接口三：取消任务

`POST /agent-studio/task/cancel`

取消一个正在执行中的任务。

### 请求

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `messageId` | string | 是 | 任务 ID（即 create 返回的 `id`） |

```json
{ "messageId": "uDqHg33fQeQfkNB5pj5LLA" }
```

### 响应

服务端返回原始 JSON 字符串。成功时 `errcode` 为 200。

---

## 接口四：获取任务的工作台分享链接

`POST /agent-studio/task/getShareUrl`

任务达到终态（`stopReason` 非空）后，返回该任务所属会话的**公开分享 URL**，可直接把链接发给别人（无需登录）查看工作台里的完整过程与结果。

### 请求

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `messageId` | string | 是 | 任务 ID |

```json
{ "messageId": "uDqHg33fQeQfkNB5pj5LLA" }
```

### 响应：`CreateWorkspaceShareVo`

```json
{
  "shareId": "aaXXXXXX",
  "shareUrl": "https://agent.linkfox.com/workspace/share/aaXXXXXX"
}
```

### 越权护栏（三重）

1. **入口 API Token 校验**：`checkApiToken` 核对 apiKey 一致性（沿用 get/cancel 同一套鉴权）。
2. **消息归属校验**：`assertMessageOwnership` 断言 `messageId` 归属当前 `memberId`，跨用户 `messageId` 直接拒。
3. **sessionId 服务端反查**：`sessionId` 不接受调用方传入，服务端从 create 阶段落库的 `messageId → sessionId` Redis 映射反查；同时 DB 查询 `getWorkspaceShareBySessionId` 按 memberId 过滤，杜绝伪造 sessionId 越权。

### 终态门禁

只有任务终态（`stopReason` 非空）才允许生成分享链接——运行中的会话中间态不对外暴露。服务端会额外调一次 `message/get` 精确判定，非终态直接抛"任务尚未完成"错误。

### Get-or-Create 语义

- 该会话已存在启用中的分享 → 复用，若过期则续期到 1 年后；
- 无 → 以调用方 `userId / memberId / groupId` 新建 `ShareWorkspaceEntity`，过期时间默认 1 年。

与 `/agent-studio/workspace/share/create`（User Token 类型）复用同一套 DB 逻辑，不重复实现。
