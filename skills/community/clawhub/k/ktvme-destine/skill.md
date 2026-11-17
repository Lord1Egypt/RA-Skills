---
name: km-desttine
description: |
  KTV包厢预订技能。帮助用户完成 KTV 包厢从选择门店到完成支付的完整预订流程，
  通过聚合接口一次性返回可预订的包厢时段与价格，简化调用链，
  并集成用户登录与订单支付子流程。

  当以下任一情况出现时必须调用本技能：
  1. 用户表达预订/订包厢/KTV/订位等意图（如"我想订个KTV"、"明天晚上有包厢吗"、"预订一个唱歌的地方"、"我想唱歌"、"订个包间"）
  2. 用户询问 KTV 门店、包厢、时段、价格等相关信息
  3. 用户已有订单号，要求支付、查询支付状态或重新支付
  4. 用户要求登录 K米 平台或检查登录状态
  5. 用户提到需要唱K、唱歌、聚会、团建等场景

  关键词：KTV、歌唱、唱歌、预订、订包厢、订位、订房、包厢、包间、唱K、欢聚、聚会、团建、支付、支付二维码、支付链接、登录、认证、包厢、时段
metadata:
  author: km-destine
  references:
    - name: subflow-login
      trigger:
        用户未登录、要求登录 K米 平台、发送验证码、手机号登录，或查询当前登录用户信息时调用；预订流程前置认证。完整流程定义详见
        reference/subflow-login.md
    - name: subflow-pay
      trigger:
        订单创建成功后展示支付二维码/链接，或用户超时未支付需重新支付时调用；roomHourCreateOrder
        直接返回支付信息，无需调用独立支付接口。完整流程定义详见 reference/subflow-pay.md
disable-model-invocation: false
---

# KTV包厢预订（km-saasktv-destine）

> ⚠️ **前置依赖检查**：本技能依赖 `km-bot` 工具。详见 [reference/cli-install.md](./reference/cli-install.md)
>
> 📖 **API 详细定义**：详见 `reference/` 目录下按功能拆分的 API 文件：
>
> - [api-overview.md](./reference/api-overview.md) — API概览、字段映射、通用约束
> - [api-store.md](./reference/api-store.md) — 门店API
> - [api-room.md](./reference/api-room.md) — 包厢API（含聚合查询）
> - [api-order.md](./reference/api-order.md) — 订单API（含下单返回的支付字段）
> - [api-session.md](./reference/api-session.md) — 会话API
>
> 🔐 **登录子流程**：详见 [reference/subflow-login.md](./reference/subflow-login.md)
>
> 💳 **支付子流程**：详见 [reference/subflow-pay.md](./reference/subflow-pay.md)
>
> ❓ **错误处理**：详见 [reference/error-handling.md](./reference/error-handling.md)

本技能覆盖 KTV 包厢预订的完整对话式流程，**核心是「先问清楚 → 再查 → 让用户选 → 下单」**：

> ① 确认城市/区域/商家名与预计到店时间 → ② 查询并选择门店 → ③ 聚合查询可预订时段并展示 → ④ 用户选择后下单 → ⑤ 支付

> ⚠️ **登录子流程**与 **支付子流程**的完整定义已下沉至 `reference/` 目录，本文件仅保留预订主流程。
>
> ⚠️ **重要约束**（必须遵守）：详见 [reference/api-overview.md](./reference/api-overview.md) 中的「⚠️ 绝对禁止事项」章节。

---

## ✨ 核心特性

### 🚀 聚合查询（核心简化点）

主流程使用 `queryRoomAvailability` 一次性返回门店在指定到店时间附近所有可预订的包厢时段：

- **hour_packages 结构**：返回 `hour_packages[]`，每一项是一个可直接下单的包厢时段（含 `room_id` / `begintime` / `endtime` / `charge` / `protocolcharge` / `activity_id`）
- **价格即最终价**：返回的 `charge` / `protocolcharge` 可直接用于下单，无需再调 `roomHourCheckPrice` 校准
- **已按 room_type 去重**：同一类型的多个房间合并展示，仅暴露 `available_room_count`，选项不重复
- **⚠️ 必须传时间参数**：`begintime` / `endtime` 实际必填，不传则返回空 `hour_packages: []`

### 会话级字段由后端自动识别（强制禁止传入）

**⚠️ 【严重警告】下单接口（roomHourCreateOrder）中一律不得传入以下字段，无论值是多少（即使是1或默认值）！**

这些字段由后端从当前会话自动识别，**前端传入会导致下单失败或数据混乱**：

| 绝对禁止字段                 | 说明        | 传入后果                               |
| ---------------------------- | ----------- | -------------------------------------- |
| `customer_id` / `customerid` | 用户ID      | 后端强制替换，可能导致订单绑定错误用户 |
| `phone` / `guesttel`         | 手机号      | 后端忽略或覆盖                         |
| `kmid`                       | 会员ID      | 后端强制替换                           |
| `xcxappid`                   | 小程序appid | 后端强制替换                           |
| `openid`                     | 微信openid  | 后端强制替换                           |
| `company_id` / `companyid`   | 商家ID      | 后端强制替换，可能导致订单属于错误商家 |

**✅ 正确示例**：

```json
// 正确！只传入业务必要字段
{
  "roomid": 62,
  "begintime": "2026-07-31 17:00",
  "endtime": "2026-07-31 18:00",
  "id": 1001,
  "charge": "10",
  "protocolcharge": "10",
  "source": 7
}
```

---

## 预订流程总览

```
用户表达预订/查询空房意图
    ↓
┌─ Step 1: 确认意图与必要信息（对话式） ────────────────────┐
│  从用户消息提取并确认：                                    │
│   ① 城市区域  OR  商家名称（二选一或都有）                │
│   ② 预计到店日期                                          │
│   ③ 预计到店时间（如"下午5点"/"17:00"）                   │
│                                                            │
│  到店时间处理规则（二选一，禁止静默假设）：                │
│   • 询问用户：问清预计几点到店                             │
│   • 代选告知：为用户选一个合理到店时间，但必须明确告知      │
│     "我帮你查 XX:00 左右到店的情况"                        │
│                                                            │
│  ✅ 三要素齐全 → 进入 Step 2                              │
│  ⚠️ 缺任一要素 → 主动追问，不要擅自假设                   │
│  💡 用户已明确说"NEO KTV 明天下午5点"等完整信息 → 跳过追问 │
└───────────────────────────────────────────────────────────┘
    ↓
┌─ Step 2: 查询门店列表 (saasktv searchCompany) ─────────────┐
│  用 Step 1 提取的关键词（门店名 > 区域 > 城市）调用         │
│  ⚠️ 首次调用偶尔超时，等待 3-5 秒重试，最多 3 次           │
│  返回候选门店列表（含 companycode、companyid、companyphone）│
└───────────────────────────────────────────────────────────┘
    ↓
┌─ Step 3: 选择门店 + 切换会话 ─────────────────────────────┐
│  根据返回结果数量决策：                                    │
│   • 候选 = 0   → 提示无匹配，引导换关键词/区域，回到 Step 1│
│   • 候选 = 1   → 告知用户"只查到 1 家门店：XX"，然后自动选用│
│   • 候选 ≥ 2   → ⚠️ 必须让用户先选，禁止自动选择           │
│                 展示列表（名称+地址+距离感）等用户确认     │
│                                                            │
│  确定门店后立即调用 switchCompany 切换会话：               │
│   ⚠️ 【强制】必须自动调用，后端会话依赖此切换              │
│   ⚠️ 中途换店必须重置所有上下文（订单等）                  │
└───────────────────────────────────────────────────────────┘
    ↓
┌─ Step 4: 查询可预订情况 (saasktv queryRoomAvailability) ┐
│  ⚠️ 仅查询 Step 3 选定的那一家商家，禁止并行查其他商家做对比│
│     （除非用户明确要求对比多家）                            │
│  ⚠️ 必须传 begintime + endtime（Step 1 到店时间作为 begintime│
│     endtime 取到店时间 + 合理范围，如 +3小时 或营业结束时间）│
│     不传时间参数会返回空 hour_packages！                    │
│                                                            │
│  返回 hour_packages[]（可预订包厢时段列表）                 │
│  每项含：room_id / room_name / room_type_name /            │
│          begintime / endtime / charge / protocolcharge /    │
│          longtime / activity_id                            │
│  ✅ 价格即最终价，无需再调 roomHourCheckPrice 校准          │
│                                                            │
│  + Step 4.1: 展示可预订时段让用户选择（见下方展示规范）    │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─ Step 5: 创建订单 (saasktv roomHourCreateOrder) ───────────┐
│  [创建订单前检查登录状态 saasktv sessionInfo]              │
│  status=0（未登录）→ 调用 subflow-login 登录后继续         │
│                                                            │
│  使用 Step 4 用户选定项的字段直接下单：                    │
│   roomid = hour_package.room_id                            │
│   begintime / endtime = hour_package.begintime / endtime   │
│   charge / protocolcharge = hour_package.charge / ...      │
│   id = hour_package.activity_id                            │
│   source = 7                                               │
│                                                            │
│  ⚠️ 禁止传入会话级字段（customer_id / company_id 等）      │
│  返回：operate_id（订单号）+ payment_link（支付链接，必须展示）+     │
│        qr_code（支付二维码）+ expire_time（有效期）        │
│                                                            │
│  💡 如需放弃当前订单（时间冲突/更换门店），                │
│     可调用 cancelBookOrder 取消原订单后重新下单              │
└───────────────────────────────────────────────────────────┘
    ↓
┌─ Step 6: 展示支付二维码 (subflow-pay) ─────────────────────┐
│  【直接用预览面板在线展示，不要下载，用 `present_files` 展示即可扫码】 │
│  ⚠️ 不要用 curl 判断，直接传 URL 给 present_files              │
│  同时展示：超链接 payment_link（必须展示，必须展示）、订单号、expire_time       │
│  支付前最终确认（金额、时段、包厢）                         │
│  引导用户扫码或在微信/支付宝中打开链接完成支付              │
│                                                            │
│  ⚠️ 超过 expire_time 未支付：必须重新 queryRoomAvailability│
│     查询可选时段 → 用户重选 → 重新下单（禁止直接重新下单） │
└───────────────────────────────────────────────────────────┘
    ↓
┌─ Step 7: 支付状态轮询（阻塞等待，不可跳过）────────────────┐
│                                                            │
│  ⚠️ 【强制】Step 6 展示二维码后，必须执行 Step 7，        │
│     会话在收到支付结果前不得结束！                          │
│                                                            │
│  7.1 启动后台轮询：                                       │
│     Bash(run_in_background=true) 执行：                    │
│     python3 scripts/poll_order_status.py <operate_id>     │
│     记下返回的 task_id                                     │
│                                                            │
│  7.2 【强制】使用 TaskOutput(block=true) 阻塞等待轮询结果：│
│     系统会自动通知轮询完成（paid 或 timeout），             │
│     Agent 收到通知后用 TaskOutput 读取完整输出             │
│                                                            │
│  7.3 读取结果文件：                                       │
│     Read /tmp/poll_result_{order_id}.json                  │
│                                                            │
│  7.4 根据 poll_status 处理：                               │
│     ✅ poll_status=paid：                                  │
│        → 展示「预约成功」页面（订单号、包厢、时段、门店、预约电话等）,提醒按时到店     │
│        → 结束预订流程                                      │
│     ⏰ poll_status=timeout：                               │
│        → 展示「订单已超时取消，请重新下单」               │
│        → 返回 Step 4 重新查询时段                          │
│                                                            │
│  💡 用户中途说"取消订单"时：                                │
│     → 先调 cancelBookOrder 取消订单                        │
│     → 再用 TaskStop 停止轮询后台任务                       │
│                                                            │
└───────────────────────────────────────────────────────────┘
    ↓
完成
```

> 💡 **流程特点**：以「确认信息 → 查 → 选 → 下单」为对话主线，把信息确认前移到 Step 1，避免后面反复回头追问；Step 3 单结果告知后自动选用、多结果必须由用户确认（禁止自动选）；Step 4 只查选定商家，不并行对比；Step 4.1 用编号列表展示可预订时段，用户只需回复数字即可选择；Step 5 直接用聚合接口返回的字段下单，无需再调价格校准接口；**Step 5 下单成功直接返回支付二维码与链接，Step 6 直接展示扫码支付，Step 7 启动后台轮询后阻塞等待，会话不结束，直到收到支付结果再通知用户**。

---

## 📋 可预订时段展示规范（Step 4.1）

为了让用户**少输入、易选择**，Step 4.1 展示 `hour_packages[]` 时必须遵循以下规范：

### 展示原则

1. **编号选择**：每项分配一个序号（1、2、3...），用户只需回复数字即可选定，无需输入包厢名/时段
2. **按包厢类型分组**：相同 `room_type_name` 的项归为一组，组内按 `begintime` 升序
3. **关键信息一行展示**：序号 + 包厢类型 + 时段 + 价格，让用户一眼看清差异
4. **价格对比直观**：同时展示售价（`charge`）和原价（`protocolcharge`），有优惠时划线展示
5. **去冗余**：同一包厢类型同时段多个房间合并为一项，附 `available_room_count` 体现余量

### 标准展示格式

```
为您查询到以下可预订时段（回复序号即可选择）：

【5D包厢】
  ① 17:00-18:00（60分钟）  ¥10  原价¥10  剩2间
  ② 18:00-19:00（60分钟）  ¥12  原价¥15  剩1间

【中包】
  ③ 17:00-18:00（60分钟）  ¥20  原价¥30  剩1间
  ④ 18:00-19:00（60分钟）  ¥25  原价¥30  剩3间

请回复序号选择，或告知希望调整的时间。
```

### 展示规则细则

| 场景                         | 处理方式                                                                    |
| ---------------------------- | --------------------------------------------------------------------------- |
| 仅 1 项可选                  | 直接告知"仅有 1 个可预订时段：① ..."，询问是否下单                          |
| 多项可选                     | 按上述标准格式分组展示，让用户回复序号                                      |
| 用户回复"1" / "①" / "第一个" | 识别为选择第 1 项，直接进入 Step 5                                          |
| 用户回复"17点的"             | 在可选时段中匹配 begintime=17:00 的项，若唯一则自动选用，多项则再确认       |
| 用户回复"5D包厢"             | 在可选时段中匹配 room_type_name=5D包厢 的项，若唯一则自动选用，多项则再确认 |
| 同包厢类型同时段多间房       | 合并为一项，标注"剩N间"，不暴露具体 room_name 让用户选                      |
| 售价 = 原价                  | 只展示售价，不重复展示原价                                                  |
| 售价 < 原价                  | 同时展示，原价可用 ~~划线~~ 或括号标注                                      |
| 列表超过 8 项                | 优先展示与用户到店时间最接近的 8 项，并提示"更多时段可告知具体时间"         |
| hour_packages 为空           | 提示无可用时段，引导用户调整时间或更换门店                                  |

### 用户选择后的确认

用户选定后，**简洁复述选定项**即进入 Step 5，**无需再次追问**：

```
已选：① 5D包厢 17:00-18:00 ¥10
正在为您下单...
```

---

## 详细步骤说明

> ⚠️ **API 详细定义与参数说明**：请参阅 `reference/` 目录下对应的 API 文件
>
> - **Step 1 (信息确认)** → 纯对话，无 API
> - **Step 2 (门店查询)** → [reference/api-store.md](./reference/api-store.md)
> - **Step 3 (门店选择 + 切换)** → [reference/api-store.md](./reference/api-store.md)
> - **Step 4 (查询可预订时段)** → [reference/api-room.md](./reference/api-room.md#queryroomavailability)
> - **Step 5 (创建订单 / 取消)** → [reference/api-order.md](./reference/api-order.md#roomhourcreateorder---创建订单) / [reference/api-order.md](./reference/api-order.md#cancelbookorder---取消预订订单)
> - **Step 6 (支付)** → [reference/subflow-pay.md](./reference/subflow-pay.md)
> - **登录检查** → [reference/subflow-login.md](./reference/subflow-login.md)
> - **通用约束** → [reference/api-overview.md](./reference/api-overview.md)

### 快速步骤索引

| 步骤     | 接口                              | 输入                                                                  | 输出                                                               | 关键约束                                                                                                                       |
| -------- | --------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| Step 1   | （无，纯对话）                    | 用户消息                                                              | 城市区域/商家名 + 日期 + 到店时间                                  | 三要素缺一不可；到店时间必须明确或代选并告知；齐全则跳过追问                                                                   |
| Step 2   | searchCompany                     | keyword                                                               | companycode, companyid, companyphone                               | 关键词优先级：门店名 > 地址 > 城市；首次可能超时需重试                                                                         |
| Step 3   | switchCompany                     | company_code                                                          | -                                                                  | 0 结果引导重查；1 结果告知后自动选用；**多结果必须用户选，禁止自动选**；切换后重置上下文                                       |
| Step 4   | **queryRoomAvailability**         | company_id, use_date, **begintime, endtime**（实际必填）              | hour_packages[]（含 room_id/charge/protocolcharge/activity_id 等） | **主流程首选**；**仅查 Step 3 选定商家，不并行对比**；必须传 begintime/endtime；价格即最终价；无需传 people                    |
| Step 4.1 | 展示+选择                         | hour_packages[]                                                       | room_id + activity_id + charge 等                                  | **按编号列表展示**（见展示规范）；用户回复序号即选定；支持模糊匹配（包厢类型/时段）                                            |
| Step 5   | roomHourCreateOrder               | roomid, begintime, endtime, charge, protocolcharge, source, (id 可选) | operate_id + payment_link + qr_code + expire_time                  | 字段直接取 Step 4 选定项；**禁止传入会话级字段**；无需再调 roomHourCheckPrice；id 部分门店不返回可省略；**下单即返回支付信息** |
| Step 6   | （展示支付信息，无 API）          | roomHourCreateOrder 返回的 qr_code / payment_link / expire_time       | —                                                                  | **直接用预览面板在线展示展示qr_code二维码（≤ 200×200）+ 超链接 payment_link(必须展示) + 有效期**；引导扫码或打开链接支付       |
| Step 7   | poll_order_status.py + TaskOutput | order_id（来自 operate_id）                                           | /tmp/poll*result*{order_id}.json（paid/timeout）                   | **Bash(run_in_background)启动 → TaskOutput(block=true)阻塞等待** → Read结果文件 → 按poll_status展示                            |

### 关键约束速查

#### 字段区分

| 字段           | 类型   | 用途                                   |
| -------------- | ------ | -------------------------------------- |
| `company_code` | String | switchCompany 参数（来自 companycode） |
| `company_id`   | Number | 查询接口参数（来自 companyid）         |

#### 会话级字段（禁止传入下单接口）

> ⚠️ **【强制约束】以下字段绝对禁止传入下单接口（roomHourCreateOrder），即使值为1或默认值也必须省略！**

- ❌ `customer_id` / `customerid` — 用户ID，由后端从会话识别，传入会导致订单绑定错误用户
- ❌ `phone` / `guesttel` — 手机号，由后端从会话识别
- ❌ `kmid` / `xcxappid` / `openid` — 会员ID/小程序ID/OpenID，由后端从会话识别
- ❌ `company_id` / `companyid` — 商家ID，由后端从会话识别，传入会导致订单属于错误商家

#### 下单字段映射（Step 4 → Step 5）

聚合接口 `queryRoomAvailability` 返回的 `hour_packages[]` 字段直接映射到 `roomHourCreateOrder` 入参：

| queryRoomAvailability 返回字段 | roomHourCreateOrder 入参 | 说明                       |
| ------------------------------ | ------------------------ | -------------------------- |
| `room_id`                      | `roomid`                 | 包厢ID                     |
| `begintime`                    | `begintime`              | 开始时间                   |
| `endtime`                      | `endtime`                | 结束时间                   |
| `charge`                       | `charge`                 | 售价（直接使用，无需校准） |
| `protocolcharge`               | `protocolcharge`         | 原价（直接使用，无需校准） |
| `activity_id`                  | `id`                     | 活动ID                     |
| （固定值）                     | `source`                 | 来源：7                    |

> ✅ **价格无需校准**：聚合接口返回的 `charge` / `protocolcharge` 即为最终下单价格，可直接使用，无需再调用 `roomHourCheckPrice`。

---

## 使用场景

### 场景1：完整预订流程（4+1 步标准对话）

```
用户："我想明天下午5点在长沙订个KTV包厢"
    ↓
Step 1: 确认信息
  从消息提取：城市=长沙、日期=明天、到店时间=下午5点
  ✅ 三要素齐全 → 进入 Step 2
  （若用户只说"想订KTV" → 主动追问"哪个城市/哪家店？哪天？大概几点到店？"）
    ↓
Step 2: searchCompany（keyword="长沙"）
  ⚠️ 首次可能超时 → 重试最多 3 次
  返回 N 家候选门店
    ↓
Step 3: 选择门店
  • N=1 → 告知用户"只查到 1 家门店：XX"，然后自动选用
  • N≥2 → ⚠️ 必须让用户先选，禁止自动选
  • N=0 → 提示无匹配，引导换关键词
  选定后调用 switchCompany（强制）
    ↓
Step 4: queryRoomAvailability
  ⚠️ 仅查询 Step 3 选定的那一家，不并行查其他商家对比
  ⚠️ 必须传 begintime + endtime（Step 1 到店时间作为 begintime，endtime 取 +2小时）！
  如到店 17:00 → begintime: "2026-07-30 17:00:00", endtime: "2026-07-30 19:00:00"
  返回 hour_packages[]（含 room_id/charge/protocolcharge/activity_id 等）
  ↓
  Step 4.1: 按编号列表展示可预订时段（按包厢类型分组）→ 用户回复序号选择
    ↓
Step 5: 创建订单（先 sessionInfo 检查登录）
  使用 Step 4 选定项字段直接调 roomHourCreateOrder
  返回 operate_id + payment_link + qr_code + expire_time
    ↓
Step 6: 直接用预览面板在线展示展示qr_code二维码（≤ qr_code 展示成二维码(无需curl校验等操作，直接展示成图片)，同时 必须展示超链接 payment_link 在对话中，引导点击跳转支付
    ↓
Step 7: 启动轮询 + 阻塞等待结果
  ① Bash(run_in_background=true) 启动 poll_order_status.py <operate_id>
  ② TaskOutput(block=true, task_id=<返回的task_id>) 阻塞等待
  ⚠️ 此处会话不结束，等待系统通知轮询完成
  ③ 收到通知后，TaskOutput 读取完整输出
  ④ Read /tmp/poll_result_{order_id}.json 获取结果：
    ✅ poll_status=paid → 展示「预约成功」页（订单号/包厢/时段等），结束
    ⏰ poll_status=timeout → 展示「订单已超时取消，请重新下单」→ 返回 Step 4
```

### 场景2：用户信息不全

用户只说"想订KTV"时，**不要直接调用 searchCompany**，先追问城市/商家名 + 日期 + 预计到店时间，三要素齐全后再进入 Step 2。

### 场景4：仅登录

用户要求登录/检查登录状态时，调用 [reference/subflow-login.md](./reference/subflow-login.md) 子流程。

### 场景5：重新下单（时间冲突/修改信息）

> ⚠️ 当用户在锁定期内（未支付）需要修改到店时间、更换门店，或已支付但未开房要求取消时，需调用 `cancelBookOrder` 处理原订单。

#### 子场景 A：未支付订单 → 取消后重新下单

```
用户："刚才订的时间不合适，换成明天下午6点"
    ↓
1. 调用 cancelBookOrder(opid=operate_id) 取消原订单，释放锁房
2. 按新时间/门店重新调用 queryRoomAvailability 查询可预订时段
3. 用户重选后调用 roomHourCreateOrder 创建新订单
4. 展示新的支付二维码引导扫码支付
```

#### 子场景 B：已支付订单 → 取消退款

```
用户："我不想订了，帮我取消"
    ↓
1. 先确认取消意图："确认要取消订单 {opid} 吗？已支付金额将原路退回。"
2. 用户确认后调用 cancelBookOrder(opid=operate_id)
3. 告知用户取消成功、退款到账时间（如 1-7 个工作日）
4. 询问是否需要重新预订（如需则走正常下单流程）
```

### 场景6：支付超时（TaskOutput 收到通知后 Agent 处理）

> ⚠️ 本场景由 Agent 在收到 TaskOutput 通知后主动处理。

当 `poll_order_status.py` 检测到 6 分钟内未支付（脚本 exit(2)）时：

1. TaskOutput(block=true) 收到脚本完成通知
2. 读取 `/tmp/poll_result_{order_id}.json` 获取超时结果
3. 向用户展示「订单已超时取消，请重新下单」
4. 返回 Step 4（重新查询时段）

```
轮询结果 poll_status=timeout
    ↓
读取 /tmp/poll_result_{order_id}.json
    ↓
展示："⏰ 订单已超时未支付，包厢已释放。请重新选择时段。"
    ↓
返回 Step 4: queryRoomAvailability 重新查时段
```

### 场景7：预约成功展示

当 `poll_order_status.py` 检测到已支付（`poll_status=paid`）时：

1. 读取 `/tmp/poll_result_{order_id}.json` 获取完整订单信息
2. 展示「✅ 预约成功」页面，包含：
   - 订单号
   - 门店名称
   - 包厢类型和名称
   - 预订时段
   - 支付金额
   - 到店时间提示

**推荐展示话术**：

```
✅ 支付成功！预约已确认

📋 订单号：{operate_id}
👤 预订人：{guest_name}
🎁 套餐：{buy_break_name}
⏰ 时段：{used_date} {used_begin_time} - {used_end_time}
💰 金额：¥{charge}

请按时到店，期待您的光临！
```

> 💡 **说明**：展示字段来自 `getOrderDetail` 接口返回，真实字段名见 [reference/api-order.md](./reference/api-order.md#getorderdetail---查询订单详情)

---

## 异常处理与容错

> 详见 [reference/error-handling.md](./reference/error-handling.md)

- 订单创建失败（如时段已被预订）：根据 `roomHourCreateOrder` 错误信息向用户说明，引导更换时段/包厢
- 支付超时（超过 `expire_time` 未支付）：由 **Step 7 阻塞等待自动处理**，Agent 收到 TaskOutput 通知后读取 `/tmp/poll_result_{order_id}.json` 展示超时结果
- 轮询脚本异常：检查脚本是否正确执行，确认 Python 环境和 km-bot 可用性，必要时手动调用 `getOrderDetail` 查询
- 轮询结果文件不存在：等待 2-3 秒后重试读取 `/tmp/poll_result_{order_id}.json`，仍不存在则视为超时处理
- 订单已锁定/时间冲突（需改期）：调用 `cancelBookOrder` 取消原订单后，再重新查询时段并下单
- 用户主动要求取消订单（已支付）：先确认意图 → 调用 `cancelBookOrder` → 告知退款到账时间
- `cancelBookOrder` 失败（如已开房/已过期）：按返回的错误提示告知用户无法取消
- 会话过期：重新引导用户完成登录后继续流程
- 接口调用失败：给出清晰的解决建议，引导用户调整参数或稍后重试

---

## 🔧 故障排查指南

### 问题1：queryRoomAvailability 返回空 hour_packages

**最常见原因**：未传 `begintime` / `endtime` 参数。

```
❌ 错误：km-bot call saasktv queryRoomAvailability "{\"company_id\":1265,\"use_date\":\"2026-07-29\"}"
   → 返回 {"hour_packages": [], "use_date": "2026-07-29"}

✅ 正确：km-bot call saasktv queryRoomAvailability "{\"company_id\":1265,\"use_date\":\"2026-07-29\",\"begintime\":\"2026-07-29 16:00:00\",\"endtime\":\"2026-07-29 17:00:00\"}"
   → 返回完整的 hour_packages
```

**处理步骤**：

1. 确认已传入 `begintime` 和 `endtime`（格式 YYYY-MM-DD HH:mm:ss）
2. 如果用户只说了"明天下午5点"，用 17:00 作为 begintime，endtime 取 +2小时
3. 确认已执行 `switchCompany` 切换到目标门店
4. 仍为空 → 该门店确实未发布该日期的可预订资源，建议致电门店

### 问题3：searchCompany 超时

`searchCompany` 接口偶尔会超时，尤其是在首次调用时。

**处理策略**：

1. 等待 3-5 秒后重试，最多重试 3 次
2. 使用 `sleep 3 && km-bot call ...` 方式重试
3. 持续超时 → 检查网络连接，提示用户稍后再试

### 问题4："当前未选择操作门店" 提示

km-bot 输出中可能包含 "当前未选择操作门店" 的提示信息，这通常是 km-bot 工具的预检查警告，**不影响实际 API 调用结果**。

**判断方法**：查看 `status` 字段，如果为 `"success"` 则 API 调用成功，忽略该提示即可。

### 问题5：所有查询均返回空

当 `queryRoomAvailability` 全部返回空时：

1. **确认门店已发布房态**：部分门店可能未在系统中发布线上可预订资源
2. **尝试不同日期**：系统可能尚未发布远期日期的房态
3. **致电门店**：提供门店电话（来自 `searchCompany` 返回的 `companyphone`）让用户直接联系

---

## 注意事项

1. **信息确认前置（Step 1）**：用户消息缺城市/商家名、日期、预计到店时间任一项时，**必须先追问**，不要直接调 searchCompany；信息齐全则跳过追问直接进入 Step 2
2. **到店时间必须明确（Step 1）**："晚上"/"下午"等模糊表述不算具体时间；必须二选一：①询问用户预计几点到店；②为用户代选一个合理到店时间并明确告知"我帮您查 XX:00 左右到店的情况"。**禁止静默假设时间**
3. **多商家禁止自动选择（Step 3）**：searchCompany 返回多个候选时，**必须让用户先选**，禁止自动选择；仅当候选为 1 时，告知用户"只查到 1 家"后可自动选用
4. **不并行对比多家商家（Step 4）**：只查询 Step 3 选定/自动选用的那一家商家的可预订情况，**禁止并行查询其他商家做对比**，除非用户明确要求对比
5. **登录状态检查必须贯穿全流程**：预订前、创建订单前均建议检查
6. **切换门店必须执行 switchCompany + 重置上下文**
7. **会话级字段前端不传入**：`company_id` / `customer_id` / `phone` / `kmid` / `xcxappid` / `openid` 等由后端从当前会话自动识别，下单接口中一律不传入
8. **支付前最终确认**：展示支付二维码前复述订单关键信息（金额、时段、包厢）
9. **⚠️ queryRoomAvailability 必须传 begintime/endtime**：不传则返回空 hour_packages；begintime 取 Step 1 到店时间，endtime 取到店时间 + 合理范围
10. **⚠️ 下单字段直接取自聚合接口**：roomHourCreateOrder 的 roomid/begintime/endtime/charge/protocolcharge/id 直接取自 Step 4 选定项，无需再调 roomHourCheckPrice 校准
11. **⚠️ searchCompany 可能超时**：首次调用偶尔超时，等待 3-5 秒重试，最多 3 次
12. **可预订时段按编号列表展示**：Step 4.1 必须按「展示规范」用编号列表展示 `hour_packages[]`，用户回复序号即选定，减少用户输入；支持模糊匹配（包厢类型/时段）
13. **⚠️ 下单即返回支付信息**：`roomHourCreateOrder` 成功后直接返回 `payment_link` / `qr_code` / `expire_time`；直接展示二维码（**尺寸最多 200×200**）给用户扫码支付
14. **⚠️ 支付后必须阻塞等待轮询结果**：展示二维码后，立即启动 `poll_order_status.py`（run_in_background=true），然后用 `TaskOutput(block=true)` 阻塞等待脚本完成；**在收到支付结果前，会话不得结束**
15. **⚠️ 轮询结果处理流程**：收到 TaskOutput 通知 → Read `/tmp/poll_result_{order_id}.json` → `poll_status=paid` 展示预约成功页；`poll_status=timeout` 展示超时提示并返回 Step 4
16. **⚠️ 原订单需放弃时先 cancelBookOrder**：用户修改时间/更换门店导致原订单冲突，或已支付订单需取消时，**先调用 `cancelBookOrder` 取消原订单**，再重新查询时段下单
17. **API 详情查阅**：
    - [reference/api-overview.md](./reference/api-overview.md) — API概览与通用约束
    - [reference/subflow-login.md](./reference/subflow-login.md) — 登录子流程
    - [reference/subflow-pay.md](./reference/subflow-pay.md) — 支付子流程
    - `reference/api-*.md` — 各API详细定义
