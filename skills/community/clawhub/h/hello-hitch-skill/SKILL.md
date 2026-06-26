---
name: hello-hitch-skill
description: 哈啰顺风车乘客助手——覆盖询价比价、下单、邀请车主、行程追踪、确认上车/到达的完整拼车流程。识别"顺风车""拼座""独享""帮我叫车""查订单""取消""司机在哪"等指令，也能从"明天去机场""下班回家"等日常表达中推断出行意图并主动响应。仅处理真实出行场景，不介入应用开发、导航软件操作或非出行类咨询。
---

# 哈啰顺风车出行技能

乘客侧顺风车全链路能力：搜索地点 → 询价比价 → 选运力下单 → 邀请车主 → 实时追踪 → 确认上车/到达。

---

## 接入配置

**获取 Key**：访问 [哈啰 AI 开放平台](https://aiopen.hellobike.com) 注册获取。

**OpenClaw 一键配置**：

```bash
openclaw mcp set hitch-ai-platform '{"url":"https://hellohitchapi.hellobike.com/ai-openplatform/mcp","headers":{"Authorization":"YOUR_API_KEY"},"transport":"streamable-http"}'
openclaw gateway restart
```

配置写入后需要重启 Gateway 才能生效。

**手动编辑配置文件**：

也可以直接编辑 `~/.openclaw/openclaw.json`，在 `mcpServers` 下添加：

```json
{
  "mcpServers": {
    "hitch-ai-platform": {
      "url": "https://hellohitchapi.hellobike.com/ai-openplatform/mcp",
      "headers": {
        "Authorization": "YOUR_API_KEY"
      },
      "transport": "streamable-http"
    }
  }
}
```

| 字段 | 说明 |
|------|------|
| `hitch-ai-platform` | MCP 服务器名称（可自定义） |
| `url` | MCP 服务端点 |
| `headers.Authorization` | API Key（从哈啰 AI 开放平台获取） |
| `transport` | 传输方式，填 `streamable-http` |

**试一试**：
```
你: 顺风车去杭州东站
你: 从西溪湿地到灵隐寺多少钱
你: 帮我看看附近有哪些车主
```

---

## 场景速查

| 用户意图 | 说法示例 | Agent 执行路径 |
|----------|----------|----------------|
| 叫顺风车 | "顺风车去[地点]"、"回家"、"上班" | 搜索 → 询价 → 选运力 → 下单 |
| 查价格 | "从 A 到 B 多少钱" | 搜索 → 询价 → 展示运力列表 |
| 邀请车主 | "帮我看看有哪些司机" | 查询可邀请车主 → 展示 → 用户选择 → 发送邀请 |
| 查订单 | "查询订单"、"订单状态" | 查询并展示订单信息 |
| 司机定位 | "司机在哪"、"多久到" | 查询司机实时位置 |
| 预约出行 | "明天9点去机场" | 平台预约或 cron 定时触发 |
| 取消订单 | "取消"、"不去了" | 二次确认后执行取消 |
| 生成链接 | "给我个支付链接" | 生成 App/微信小程序跳转链接 |

---

## Agent 执行手册

以下内容为 AI Agent 执行参考，用户无需阅读。

### 文件按需加载

技能文件拆分存储，按场景按需读取，避免一次性加载全部内容。

| 文件 | 内容 | 加载时机 |
|------|------|----------|
| **本文件** | 触发判断、场景路由、交互约束 | 每次触发必读 |
| `references/operations.md` | 各场景的操作命令与步骤详情 | 需要具体执行命令时查阅 |
| `references/api.md` | 工具签名、参数定义、返回字段、错误码 | 调用工具前务必核对 |


### 核心约束

以下规则贯穿所有场景，不可违反。

**坐标获取**：每次都通过 `maps_textsearch` 实时查询，不复用对话上下文中出现过的旧坐标。用户的物理位置随时可能发生变化。

**参数类型**：经纬度、城市编码等数字参数一律以字符串传入（加引号），否则 API 会拒绝请求。

**询价前置**：`hitch_create_order` 强依赖 `hitch_estimate_price` 返回的 `priceTraceId`。该 ID 有有效期，超时后需重新询价获取。

**幂等保护**：所有会产生实际变更的操作都需传入 `idempotencyKey`，防止网络重试导致重复执行。总原则：同一意图首次生成、重试复用、新意图重新生成。

| 操作 | idempotencyKey 生成方式 |
|------|----------------------|
| `hitch_create_order` | 生成唯一随机值；超时重试时复用，换路线重新生成 |
| `hitch_cancel_order` | 生成唯一随机值；重试时复用 |
| `hitch_invite_driver` | 推荐 `{orderGuid}-{driverId}` 拼接；邀请不同车主时自然产生新值 |
| `hitch_pax_confirm_get_on_car` | 直接使用 `orderGuid` 即可（一个订单只确认一次上车） |
| `hitch_pax_confirm_reach_destination` | 直接使用 `orderGuid` 即可 |

**以工具返回为准**：当 API 返回的数据与用户描述存在矛盾时（例如用户说"大概 30 块"但询价返回 58 元），必须引用实际数据向用户说明差异，由用户决定是否继续，不能忽略冲突默默执行。

### 地址处理

当用户未给出完整起终点时，直接询问用户，不要猜测。

**用户纠正地址后的处理**：当用户否定了搜索结果或给出更正（"不是这个，是 XX 路那个""换一个起点"），必须用新地址重新走 `maps_textsearch` 获取坐标。如果之前已经询价了，也需要用新坐标重新询价——旧的 `priceTraceId` 绑定的是旧路线，不可继续使用。

### 交互确认要求

顺风车涉及真实出行费用，以下场景必须在用户明确回复后才执行：

| 场景 | 要求 |
|------|------|
| 运力选择 | 展示全部可选运力及价格，由用户选择后才能下单。Agent 不得替用户做决定 |
| 邀请车主 | 展示车主信息（昵称、评分、车型、顺路度），用户指定后才发送邀请 |
| 取消订单 | 即便用户主动说了"取消"，仍需回复"确定要取消这个订单吗？"等待用户二次确认 |
| 地址确认 | 通过别名推断的地址、或搜索到多个候选地点时，先确认再继续流程 |
| 意图升级 | 用户从"先看看价格"切换到"就这个，帮我下单"时，仍需完成运力选择和确认流程，不能因为之前展示过价格就直接跳到下单 |
| 模糊地点 | 用户给出的地点描述不够精确（如"人民广场附近""那个商场"）时，必须追问具体位置或展示搜索候选，不要自行猜测取第一条结果 |

---

### 场景一：叫顺风车（主流程）

这是最常见的场景，完整流程如下：

```
搜索地点 → 确认起终点 → 询价 → 用户选运力 → 确认等待时长 → 下单 → 展示结果 → 邀请车主 → 创建状态回查任务
```

**第 1 步 — 搜索地点**

调用 `maps_textsearch` 分别解析起点和终点。必须提取 lat、lon、cityCode、adCode、address、cityName 六个字段，后续询价和下单均需使用。

**第 2 步 — 确认起终点**

如果地址是从别名推断的，或搜索返回了多个候选，必须向用户确认。用户直接给出的明确地名且搜索唯一匹配的，无需确认。

**第 3 步 — 询价**

调用 `hitch_estimate_price`，保存返回的 `priceTraceId` 和 `capacities` 运力列表。

**第 4 步 — 用户选运力**

向用户展示编号列表，等用户选择：
```
从 [起点] 到 [终点]，约 XX 公里，以下运力可选：
1. 拼座 — 约 XX 元
2. 独享 — 约 XX 元
3. 特惠独享 — 约 XX 元
请回复编号选择（可多选如"1 3"，或回复"全选"）
```

支持：编号选择（"1 3"）、全选（"全选"/"都要"）、名称匹配（"独享"）。

**第 5 步 — 确认等待时长**

询问用户愿意等待多久。默认 10 分钟，最长 180 分钟。用户不指定则用默认值。

**第 6 步 — 创建订单**

调用 `hitch_create_order`，传入完整起终点六要素、priceTraceId、selectedCapacities、waitMinutes、idempotencyKey。

**第 7 步 — 展示结果并处理支付引导**

展示订单基本信息：
```
✅ 顺风车订单已发出！

📋 订单号: [orderGuid]
📍 [起点] → [终点]
🎫 运力: [拼座/独享]
💰 预估: 约 XX 元
⏳ 等待时长: XX 分钟
```

然后检查响应中的 `needAppPayment` 和 `nextAction` 字段：

| 响应条件 | Agent 动作 |
|----------|-----------|
| `needAppPayment` 为 `true` 或 `nextAction` 含支付相关标识（如 `go_app_pay`） | **立即调用** `hitch_generate_wechat_link` 生成小程序跳转链接，附在订单信息下方，并引导用户完成支付 |
| `needAppPayment` 为 `false` 且无支付引导 | 展示等待匹配提示，不主动生成链接 |

**支付引导话术注意**：未支付不影响订单发布，车主可以正常看到订单。但完成支付后车主的接单意愿会更强，建议引导用户尽早支付以提高匹配效率。**不要说"不支付车主看不到订单"**——这与事实不符。

无论哪种情况，都要在末尾附上操作提示：
```
💡 随时问我「订单怎么样了」查看最新状态
💡 也可以说「帮我看看有没有司机」主动邀请车主
```

**第 8 步 — 邀请车主（可选）**

调用 `hitch_invite_driver_list` 获取附近顺路车主列表，展示给用户选择后调用 `hitch_invite_driver`。

**第 9 步 — 创建状态回查任务（必做）**

下单成功后，必须创建一个延迟 5 分钟的回查任务（模板见下方「定时任务模板」章节）。此步不可省略。

---

### 场景二：邀请车主

触发词：`帮我看看有哪些司机` / `邀请车主` / `有没有顺路的`

1. 调用 `hitch_invite_driver_list`，传入当前订单号
2. 展示车主列表，包含昵称、评分、车型、顺路度
3. 用户选择后调用 `hitch_invite_driver`，传入对应的 driverOrderGuid、driverId、hitchPercent

---

### 场景三：订单管理

**查询订单**

触发词：`查询订单` / `订单怎么样了` / `订单状态`

订单号来源优先级：用户明确给出 → 当前对话最近创建的订单号 → 不传 orderGuid（返回进行中列表）。

根据返回的 `statusCode` + `status` 决定展示内容和下一步引导：

| 订单状态 | 必须展示的信息 | 下一步引导 |
|----------|---------------|-----------|
| 等待接单 | 起终点、价格、已等时长 | 引导查看可邀请车主列表，主动邀请缩短等待 |
| 司机已接单 | 车主姓名、车型、车牌号（响应中 driverInfo 对象）、预计到达时间 | 提示可随时查询车主实时位置 |
| 司机已到达上车点 | 车主姓名、车牌号、上车点名称 | 提醒尽快前往，到车后确认上车 |
| 行程进行中 | 当前进度（如果有）、终点名称 | 到达后引导确认到达 |
| 到达目的地 | 终点、费用 | 引导确认到达以完成行程 |
| 已完成 | 起终点、实际费用、行程时长（如果有） | 无需操作 |
| 已取消 / 系统取消 | 取消原因（如果有） | 如果用户仍有出行需求，询问是否重新叫车 |

> 注意：响应中的 `actionHint` 字段会给出平台侧的操作建议，可作为引导话术的参考，但不要原样照搬——用自然语言重新表达。

**取消订单**

触发词：`取消` / `不去了` / `取消订单`

无论用户怎么表达取消意图，都必须先二次确认后才调用 `hitch_cancel_order`。

---

### 场景四：预约出行

两种实现方式：

**方式一：平台预约**

通过 `hitch_create_order` 的 `planDepartureTime` 参数传入出发时间（毫秒时间戳），平台侧处理预约匹配。最大支持当前时间 +10 天。

**方式二：定时任务触发**

通过 cron 一次性任务，到时间后由独立 Agent 会话自动执行完整叫车流程。详见下方「定时任务模板」。

---

### 行程操作

**查询司机位置**：调用 `hitch_get_driver_location`，展示距离和预计到达时间。

**确认上车**：调用 `hitch_pax_confirm_get_on_car`。

**确认到达**：调用 `hitch_pax_confirm_reach_destination`。

**生成跳转链接**：
- App 深链：`hitch_generate_app_link`——不依赖订单，有起终点坐标即可生成
- 微信小程序：`hitch_generate_wechat_link`——需要 orderGuid，根据订单状态自动跳转到对应页面

链接生成有两种触发方式：
1. **主动触发**：下单成功后，如果响应指示需要 App 内支付（`needAppPayment: true`），Agent 应自动生成微信小程序链接
2. **被动触发**：用户主动要求"给我个链接""帮我生成跳转链接"时生成

---

### 异常处理

工具调用失败时，按以下原则回应用户。核心原则：**如实反馈，不美化、不猜测、不把异常包装成正常结论。**

| 失败场景 | Agent 应对 |
|----------|-----------|
| `maps_textsearch` 返回多条结果 | 列出候选地点让用户选择，不要自动取第一条 |
| `maps_textsearch` 无结果 | 提示用户换个关键词或补充城市信息重试 |
| `hitch_estimate_price` 失败 | 保留已解析的起终点，告知用户当前无法获取报价，建议稍后重试或通过 App 深链查看 |
| `hitch_create_order` 失败 | 明确说明下单未成功及失败原因，绝不能暗示"订单已创建" |
| `hitch_invite_driver` 失败 | 告知邀请未发出，可尝试邀请列表中的其他车主 |
| `hitch_cancel_order` 失败 | 明确告知取消未生效，提供失败原因，引导用户到 App 中操作 |
| 任意工具请求超时 | 说明服务暂时不可用，不要将超时解读为业务结果（如"没有可用车主"） |
| `priceTraceId` 过期（下单报错） | 自动重新调用 `hitch_estimate_price` 获取新的 traceId，然后重试下单 |

---

### 定时任务模板

**预约叫车**

```bash
openclaw cron add \
  --name "hitch-reserve:$(date +%s)" \
  --at "TIME_VALUE" \
  --session isolated \
  --message "自动叫顺风车：从「ORIGIN」到「DESTINATION」。依次完成地址解析、询价、创建订单。订单创建成功后输出订单信息，并创建 5 分钟延迟的状态回查任务。" \
  --announce \
  --channel CHANNEL_NAME \
  --to "CHAT_ID"
```

**订单状态回查**

```bash
openclaw cron add \
  --name "hitch-status:ORDER_GUID" \
  --at "5m" \
  --session isolated \
  --message "查询顺风车订单 ORDER_GUID 的最新状态。若已有车主接单，输出车主信息和预计到达时间；若仍在等待，建议用户尝试邀请车主。" \
  --announce \
  --channel CHANNEL_NAME \
  --to "CHAT_ID"
```

**时间值填写**：
- 相对时间直接用 duration 格式：`15m`、`2h`、`1h30m`
- 绝对时间用带时区的 ISO 8601：`YYYY-MM-DDTHH:MM:SS+08:00`

绝对时间需要在 shell 中计算时，注意 GNU date 和 BSD date 语法差异：

```bash
# 判断当前系统类型后生成 ISO 时间戳
if date --version >/dev/null 2>&1; then
  # GNU (Linux)
  TARGET_TIME=$(TZ=Asia/Shanghai date -d 'tomorrow 09:00' '+%Y-%m-%dT%H:%M:%S+08:00')
else
  # BSD (macOS)
  TARGET_TIME=$(TZ=Asia/Shanghai date -j -v+1d -f '%H:%M' '09:00' '+%Y-%m-%dT%H:%M:%S+08:00')
fi
```

建议 Agent 直接用上述 if/else 结构，避免因系统差异导致 cron 创建失败。

**占位符说明**：
- `TIME_VALUE` — 触发时间
- `ORIGIN` / `DESTINATION` — 起终点全称（含城市前缀）
- `ORDER_GUID` — 订单号
- `CHANNEL_NAME` — 会话 metadata 的 channel 字段（如 feishu、telegram），不加引号
- `CHAT_ID` — 会话 metadata 的 chat_id 字段

**注意事项**：
- isolated session 无历史上下文，message 中必须包含完整的起终点信息
- 无法获取当前会话 metadata 时不要创建 cron，改为提醒用户稍后主动查询
- 创建失败时必须明确告知用户

---

### 典型交互参考

以下示例展示 Agent 在各场景中的预期行为模式，帮助理解交互节奏。

**场景 A：叫车（含支付引导）**

> **用户**：帮我叫个顺风车从西溪湿地到杭州东站
> **Agent**：（maps_textsearch × 2 → hitch_estimate_price）从 西溪湿地 到 杭州东站，约 12 公里，以下运力可选：
> 1. 拼座 — 约 28 元
> 2. 独享 — 约 45 元
> 请回复编号选择
> **用户**：1
> **Agent**：愿意等多久？默认 10 分钟
> **用户**：默认就行
> **Agent**：（hitch_create_order，检查响应：needAppPayment=true → 调用 hitch_generate_wechat_link → 创建 cron 回查）
> 订单已发出！建议尽早完成支付，支付后车主接单意愿会更强。点击下方链接可跳转小程序支付：
> 🔗 [微信小程序链接]
> 正在匹配顺路车主，要帮你看看附近可邀请的车主吗？

**场景 B：查订单 + 邀请车主**

> **用户**：订单怎么样了
> **Agent**：（hitch_query_order）订单仍在等待接单，已等 3 分钟。要查看附近可邀请的车主吗？
> **用户**：好的
> **Agent**：（hitch_invite_driver_list）找到 2 位顺路车主：
> 1. 周师傅 ⭐4.9 | 白色比亚迪汉 | 顺路 92%
> 2. 陈师傅 ⭐4.7 | 黑色大众帕萨特 | 顺路 78%
> 要邀请哪位？
> **用户**：1
> **Agent**：（hitch_invite_driver）已向周师傅发送邀请，等待确认中

**场景 C：预约 + 行程中查位置**

> **用户**：明天早上 8 点叫个顺风车去机场
> **Agent**：从哪里出发？
> **用户**：家
> **Agent**：（确认地址后）好的，将在明天 08:00 自动为您发起从 XX小区 到 XX机场 的顺风车订单
> （创建 cron 定时任务）
> ——次日 08:00——
> **Agent**：（cron 触发，自动完成搜索→询价→下单）顺风车订单已发出，订单号 xxx
> **用户**：司机到哪了？
> **Agent**：（hitch_get_driver_location）车主距您约 1.2 公里，预计 3 分钟到达上车点

---

### 凭证与鉴权

API Key 通过 MCP Server 配置中的 `Authorization` Header 传递，Agent 无需额外管理凭证。

**用户反馈鉴权失败时**：
> 请访问 [哈啰 AI 开放平台](https://aiopen.hellobike.com) 检查 API Key 是否有效，并确认 MCP Server 配置中的 Authorization Header 值为你的 API Key（无需加 Bearer 前缀）。

---

### 可用工具一览

**地图**：`maps_textsearch`

**顺风车**：`hitch_estimate_price` · `hitch_create_order` · `hitch_query_order` · `hitch_cancel_order` · `hitch_get_driver_location` · `hitch_invite_driver_list` · `hitch_invite_driver` · `hitch_pax_confirm_get_on_car` · `hitch_pax_confirm_reach_destination` · `hitch_generate_app_link` · `hitch_generate_wechat_link`
