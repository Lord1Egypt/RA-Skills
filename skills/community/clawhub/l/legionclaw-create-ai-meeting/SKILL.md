---
name: legionclaw-create-ai-meeting
version: 1.0.0
description: 在 LegionClaw 中为用户创建智能会议。
disable-model-invocation: false
---

# 创建智能会议

## 何时使用

- **技能名**：用户点名 `create-ai-meeting`，或需要**创建智能会议**。
- **常见说法**（不限于此）：创建会议、新建会议、帮我创建会议、我想新建一个会议、开个会、创建个会议、发起会议、快速会议、立即开会、马上开会、开个快速会议、创建智能会议。
- **运行前提**：面向 **LegionClaw 内执行的 Agent**；会话标识优先从**运行时注入**或 **LegionClaw 宿主/模型**查询获取，**不要**默认让用户粘贴整串会话标识。

## 目标

调用固定接口，为用户创建智能会议。`userId` 作为 **URL 查询参数**拼接在请求地址上。其中 **`userId`** 取值为 LegionClaw **会话标识串**按 `:` 拆分后的**第二段 `agentid`** 的**前 32 位**（若 agentid 不足 32 位，直接传完整 agentid）。解析规则见下文。成功后在对话正文中向用户展示会议号。

## LegionClaw 运行约定

本技能面向 **在 LegionClaw 内执行的 Agent**：会议与当前任务所绑定的 **agentid**（会话标识第二段）对应。

- **会话形态**：语义为 `agent:<agentid>:<渠道>:<用户 id>`。**渠道为空时**为三段 `agent:<agentid>:<用户 id>`（**无** `::`）；**有渠道时**为四段起。拆段后 **URL 查询参数 `userId` 的值仅允许为第 2 段 `agentid` 的前 32 位**（不足 32 位则传完整 agentid）。
- **成功判定**：以响应 JSON 的 **`code == "000000"`** 或 **`code == 0`** 为成功标志；**HTTP 状态码为 2xx 不代表业务成功**。
- **执行位置**：`curl` 或等价请求须在 **LegionClaw 下发任务时的运行环境**中发起。
- **对用户输出**：正常成功路径在消息正文中输出会议创建成功提示；**勿**默认回显完整会话标识串或内部 `agentid`，除非用户明确要求排查。

## 接口

- **URL**: `https://legion.tongfudun.com/im/meeting/saveMeeting/v1ForAi`
- **方法**: `POST`
- **查询参数**: `userId=<agentid前32位>`
- **完整请求地址示例**: `https://legion.tongfudun.com/im/meeting/saveMeeting/v1ForAi?userId=fe535f475db6471d81cf0a1fcd5566bd`

### 成功响应体（HTTP 2xx）

响应为 JSON，按以下结构解析：

| 字段 | 含义 |
|------|------|
| `code` | 业务状态码；成功为字符串 `"000000"` 或数值 `0`；其他值表示失败 |
| `message` | 业务提示信息 |
| `data.meetingId` | 会议唯一标识 |
| `data.callId` | 通话标识 |
| `data.code` | **会议号**（用户可见，格式如 `435 959 951`） |
| `data.imPin` | 会议 PIN 码 |

示例：

```json
{
  "code": "000000",
  "message": "成功",
  "data": {
    "meetingId": "0e0602fcd2414ca9ac93d276f2a10a03",
    "callId": "8cee7ace26cc4c35995b42da23daea6d",
    "code": "435 959 951",
    "imPin": "241796"
  }
}
```

### 回复用户的格式

在响应 JSON 中 **`code` 为 `"000000"` 或 `0`** 时，在**用户可见消息**中输出会议创建成功提示。

**固定格式**：`会议创建成功，会议号：<data.code>`

- **`data.code`** 是会议号，格式如 `435 959 951`
- **完整示例**：

```markdown
会议创建成功，会议号：435 959 951
```

- 若 **`data.code` 缺失或为空**：仍按成功处理，输出 `会议创建成功`（不显示会议号）。

### 失败返回口径（统一规则）

出现以下任一情况时，按以下优先级返回（**对用户不要暴露 URL/IP/端口**）：

1. 若响应中存在非空 **`message`** 字段：基于 `message` 原意做简短、友好的用户提示。
2. 若存在非空 **`msg`** 而无可用 **`message`**：可基于 `msg` 原意做简短友好提示。
3. 若无可用 **`message`** 与 **`msg`**：返回固定回复 `创建会议失败，请联系管理员。`

适用场景包括但不限于：

- 返回值格式错误（例如非 JSON、JSON 解析失败）
- `code` 不为 `"000000"` 或 `0` 的业务失败

## 获取会话标识串

**不要依赖用户手动粘贴整串会话标识**作为默认流程。

1. **优先**：使用运行时已注入的「当前会话标识」或等价字段（环境变量、LegionClaw 任务/会话上下文字段等；名称以实际平台为准，例如 `OPENCLAW_SESSION_ID`）。
2. **主路径**：若上下文中没有该串，**通过 LegionClaw 宿主侧能力获取**——例如调用 LegionClaw 提供的会话/元数据查询接口，或**与当前 LegionClaw 大模型（宿主）交互**，让其返回**当前会话标识串**（完整 `agent:...`）。**不要**把「请用户手动粘贴整串会话标识」作为默认或首选步骤。
3. **例外**：仅当用户**主动**提供 **agentid** 或与后端一致的 `userId` 值时，校验非空后可直接作为请求体 `userId`（不要求 `agent:` 前缀）；这不替代从 LegionClaw 自动取会话标识的常规流程。

## 从会话标识解析 agentid

LegionClaw **会话标识串**的语义为：

`agent:<agentid>:<渠道>:<用户 id>`

**渠道省略（为空）时**，实际传输格式为**三段**（**不会**用 `::` 占位），第三段**直接**是用户 id：

`agent:<agentid>:<用户 id>`

**有渠道时**为**四段**（第三段为渠道名，第四段为用户 id），例如：

`agent:<agentid>:openai-user:<用户 id>`

按英文冒号 `:` 拆段后：

| 形态 | 段数（典型） | 第 1 段 | 第 2 段 **`agentid`** | 第 3 段 | 第 4 段 |
|------|-------------|---------|----------------------|---------|---------|
| 有渠道 | 4 | `agent` | **`agentid`**，只取此段 | 渠道 | 用户 id |
| 无渠道 | 3 | `agent` | **`agentid`**，只取此段 | 用户 id（**不是**渠道占位） | — |

**与旧规则一致**：无论三段或四段，**`agentid` 一律为拆段后的第 2 段**；不要把第 3 段（无渠道时的用户 id）误当 `agentid`。

**解析规则**：将整串按 `:` 拆分；若第一段为 `agent` 且**至少两段**（`NF >= 2`）且第二段非空，则 **`agentid` = 第二段**。然后取 **agentid 的前 32 位**作为 URL 查询参数 `userId`（若 agentid 长度不足 32 位，则使用完整 agentid）。否则视为无效格式，不要猜测；应**重新按「[获取会话标识串](#获取会话标识串)」**从 LegionClaw 侧取得合法串后再解析。若用户主动提供了可与 `userId` 同用的 **agentid** 值，校验非空后可直接用作查询参数（不再要求 `agent:` 前缀）。

**典型示例**（有渠道，四段）：

- 整串：`agent:fe535f475db6471d81cf0a1fcd5566bd1684487565205:openai-user:703f56dd37f84fa682266a8471f26984`
- **`agentid`**：`fe535f475db6471d81cf0a1fcd5566bd1684487565205`
- **`userId`（前 32 位）**：`fe535f475db6471d81cf0a1fcd5566bd`

**渠道为空**（三段，**无双冒号**）：

- 整串：`agent:fe535f475db6471d81cf0a1fcd5566bd1684487565205:703f56dd37f84fa682266a8471f26984`
- **`agentid`**：`fe535f475db6471d81cf0a1fcd5566bd1684487565205`
- **`userId`（前 32 位）**：`fe535f475db6471d81cf0a1fcd5566bd`

**更多示例**:

| 会话标识串（整串） | agentid | userId（前 32 位） |
|-------------------|---------|-------------------|
| `agent:fe535f475db6471d81cf0a1fcd5566bd1684487565205:openai-user:703f56dd37f84fa682266a8471f26984` | `fe535f475db6471d81cf0a1fcd5566bd1684487565205` | `fe535f475db6471d81cf0a1fcd5566bd` |
| `agent:fe535f475db6471d81cf0a1fcd5566bd1684487565205:703f56dd37f84fa682266a8471f26984` | `fe535f475db6471d81cf0a1fcd5566bd1684487565205` | `fe535f475db6471d81cf0a1fcd5566bd` |
| `agent:test_001:main` | `test_001` | `test_001`（不足 32 位，传完整） |
| `agent:alice:worker` | `alice` | `alice`（不足 32 位，传完整） |

## 执行步骤

1. 按「[获取会话标识串](#获取会话标识串)」取得整串；若用户主动提供了 **agentid** 或已与后端约定一致的 **`userId` 取值**，可直接采用。再按上文规则解析出 **agentid**，截取**前 32 位**作为 URL 查询参数 **`userId`**。
2. 执行下方 `curl`（将 `USER_ID` 替换为解析结果）：

```bash
curl -sS -X POST "https://legion.tongfudun.com/im/meeting/saveMeeting/v1ForAi?userId=${USER_ID}"
```

可用一行从环境变量中的会话标识串解析 **agentid** 并截取前 32 位（示例变量名 `OPENCLAW_SESSION_ID`，以实际运行时提供的变量名为准）：

```bash
AGENTID=$(echo "${OPENCLAW_SESSION_ID}" | awk -F: '$1=="agent" && NF>=2 && length($2)>0 {print $2; exit}')
USER_ID=$(echo "${AGENTID}" | cut -c1-32)
curl -sS -X POST "https://legion.tongfudun.com/im/meeting/saveMeeting/v1ForAi?userId=${USER_ID}"
```

3. 根据调用的 HTTP 与业务结果处理：
   - **HTTP 非 2xx**：不要向用户回显原始 URL；用简短说明（如无法访问服务器、服务暂时不可用）。
   - **HTTP 2xx 且 body 为 JSON**：若 **`code` 为字符串 `"000000"` 或数值 `0`**，视为成功；否则按失败口径处理。
4. 成功后按「[回复用户的格式](#回复用户的格式)」输出会议创建成功提示及会议号。

## 错误处理

- **连接失败 / 超时**：提示检查**当前 LegionClaw 运行环境**到**服务器**的网络与防火墙（不要在用户可见报错中暴露具体 IP、端口或完整请求 URL）。
- **会话标识格式不对**：不要先让用户粘贴核对；应再次从 LegionClaw 运行时或宿主大模型侧获取会话标识串，确认拆段后第一段为 `agent`、第二段非空。若用户主动提供的 **agentid** / `userId` 仍无效，再说明语义格式为 `agent:<agentid>:<渠道>:<用户 id>`；**渠道为空时线上为三段** `agent:<agentid>:<用户 id>`（**无** `::`），**不要**把第 3 段用户 id 当成 `agentid`。
- **400/422**：对照后端要求检查 URL 查询参数 `userId` 是否为空或含非法字符。
- **返回值格式错误或业务失败**：按「[失败返回口径（统一规则）](#失败返回口径统一规则)」处理。

通用安全输出要求：

- 任何服务报错场景下，用户可见文案中**不要出现具体 IP 地址、端口或完整请求 URL**；统一使用「服务器」等泛化称呼。

## 变更接口时

若 URL、字段名、成功响应 JSON 结构或会话标识格式变更，请同步更新本文件，避免 agent 与真实服务不一致。
