# 订单 API

> ⚠️ **前置依赖**：本接口文档依赖 `km-bot` 工具。详见 [cli-install.md](./cli-install.md)
>
> 📖 **通用约束**：字段映射规则和禁止事项详见 [api-overview.md](./api-overview.md)

---

## roomHourCreateOrder - 创建订单

**⚠️ 前置条件**：

1. 用户必须已登录（调用 `sessionInfo` 检查 `status=1`，未登录则先完成登录）
2. 字段直接取自 `queryRoomAvailability` 返回的 `hour_packages[]` 选定项，无需再调价格校准接口

**❌ 禁止传入的字段（强制约束）**

> ⚠️ **【严重警告】以下字段绝对禁止传入，无论值为多少（即使是1或默认值）！后端会强制替换这些字段，传入会导致订单绑定错误用户或商家。**

| 禁止字段                     | 说明        | 传入后果                               |
| ---------------------------- | ----------- | -------------------------------------- |
| `customer_id` / `customerid` | 用户ID      | 后端强制替换，可能导致订单绑定错误用户 |
| `phone` / `guesttel`         | 手机号      | 后端忽略或覆盖                         |
| `kmid`                       | 会员ID      | 后端强制替换                           |
| `xcxappid`                   | 小程序appid | 后端强制替换                           |
| `openid`                     | 微信openid  | 后端强制替换                           |
| `company_id` / `companyid`   | 商家ID      | 后端强制替换，可能导致订单属于错误商家 |

**调用方式**：

```bash
km-bot call saasktv roomHourCreateOrder "{\"roomid\":62,\"begintime\":\"2026-07-31 17:00:00\",\"endtime\":\"2026-07-31 18:00:00\",\"id\":1001,\"source\":7}"
```

> ⚠️ **begintime/endtime 必须带秒**：格式为 `yyyy-MM-dd HH:mm:ss`（如 `"2026-08-07 19:00:00"`）。queryRoomAvailability 返回的时间不带秒（如 `"2026-08-07 19:00"`），下单时**必须补 `:00` 秒**，否则会报"请求参数类型不匹配"错误。

**请求参数**：

| 字段               | 类型   | 必填   | 说明                                                                  |
| ------------------ | ------ | ------ | --------------------------------------------------------------------- |
| roomid             | Number | **是** | 包厢 id（来自 queryRoomAvailability 的 `room_id`）                    |
| begintime          | String | **是** | 开始时间（格式: yyyy-MM-dd HH:mm:**ss**，**必须带秒**，来自 queryRoomAvailability 返回值需补秒）        |
| endtime            | String | **是** | 结束时间（格式: yyyy-MM-dd HH:mm:**ss**，**必须带秒**，来自 queryRoomAvailability 返回值需补秒）        |
| source             | Number | 否     | 来源：固定传 `7`                                                      |

**字段映射**（queryRoomAvailability → roomHourCreateOrder）：

| 来源字段（queryRoomAvailability） | 目标字段（roomHourCreateOrder） |
| --------------------------------- | ------------------------------- |
| `room_id`                         | `roomid`                        |
| `begintime`                       | `begintime`                     |
| `endtime`                         | `endtime`                       |
| `activity_id`                     | `id`                            |
| `charge`                          | `charge`                        |
| `protocolcharge`                  | `protocolcharge`                |
| （固定值）                        | `source` = `7`                  |

> ⚠️ 价格字段直接使用 `queryRoomAvailability` 返回值，无需再调用任何价格校准接口。

**成功返回示例**：

```json
{
  "data": {
    "operate_id": "7608052439251950",
    "payment_link": "支付url，直接展示成超链接，点击去支付，必须展示",
    "qr_code": "支付二维码url,直接在线展示二维码，无需下载，无需思考，无需curl，必须展示",
    "expire_time": "2026-08-05 18:11:33"
  },
  "msg": "",
  "ret": 0
}
```

**返回字段说明**：

| 字段               | 类型   | 说明                                                                                       |
| ------------------ | ------ | ------------------------------------------------------------------------------------------ |
| ret                | Number | 错误码，0成功                                                                              |
| data.operate_id    | String | 订单号                                                                                     |
| data.payment_link  | String | 支付url，直接展示成超链接，点击去支付，必须展示                                  |
| data.qr_code       | String | 支付二维码url，直接在线展示，无需下载，无需思考（**直接按最合理的方式展示给用户扫码支付**                 |
| data.expire_time   | String | 有效期（格式: yyyy-MM-dd HH:mm:ss），即锁定包厢时间 + 支付时间，**超出则无法下单**         |

> ⚠️ **下单即返回支付信息**：`roomHourCreateOrder` 成功后**直接返回支付链接和支付二维码**，无需再调用任何支付接口。包厢在 `expire_time` 前被锁定，用户须在此时间内完成支付。

### 支付信息展示规范

下单成功后，**直接向用户展示支付二维码**引导扫码支付：

1. **二维码展示尺寸**：最多 **200×200**，避免过大影响阅读
2. **同时展示补充信息**：超链接 payment_link（必须展示）、订单号、有效期 `expire_time`
3. **推荐输出话术**：

```
✅ 下单成功！请扫码完成支付

![支付二维码](data.qr_code)   <!-- 尺寸控制在 200×200 以内 -->

🔗 支付链接（必须展示）：
   {payment_link}

📋 订单号：{operate_id}
⏰ 支付有效期：{expire_time}

请在有效期内完成支付，逾期包厢将释放，需重新选择时段。
```

### ⚠️ 有效期超时处理（强制约束）

> **【严重约束】`expire_time` 是锁定包厢的时间，也是支付时间，超出后无法下单。**

如果用户**超过 `expire_time` 仍未完成支付**，禁止直接调用 `roomHourCreateOrder` 重新下单，必须：

1. 重新调用 `queryRoomAvailability` 查询当前可选时段（原时段可能已被他人预订）
2. 按展示规范重新展示可预订时段供用户选择
3. 用户选定后再调用 `roomHourCreateOrder` 创建新订单（返回新的支付信息）

```
用户未在 expire_time 内支付
    ↓
❌ 禁止：直接 roomHourCreateOrder 重新下单
✅ 正确：queryRoomAvailability 重新查时段 → 用户重选 → roomHourCreateOrder 下新单
```

**❌ 异常返回示例**：

```json
{
  "jsonrpc": "2.0",
  "id": "km_rpc_xxx",
  "error": {
    "code": -1,
    "message": "该时段已被预订"
  }
}
```

---

## cancelBookOrder - 取消预订订单

**用途**：取消已创建的预订订单，释放锁定的包厢资源或触发退款流程。

**调用方式**：

```bash
km-bot call saasktv cancelBookOrder "{\"opid\":\"7608052439251950\"}"
```

**请求参数**：

| 字段 | 类型   | 必填   | 说明                                                                                                                                |
| ---- | ------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| opid | String | **是** | 订单号（来自 `roomHourCreateOrder` 返回的 `operate_id`，**必须用字符串传递**） |

> ⚠️ **opid 必须用字符串类型传递**：`operate_id` 返回值是长数字字符串（如 `"7608052439251950"`），用 Number 类型传递会报"请求参数类型不匹配"错误。正确做法：`"opid":"7608052439251950"`（带引号）。

**成功返回示例**：

```json
{
  "result": {
    "ret": 0,
    "message": "退款申请成功",
    "msg": "退款申请成功"
  },
  "msg": "",
  "ret": 0
}
```

**返回字段说明**：

| 字段           | 类型   | 说明           |
| -------------- | ------ | -------------- |
| ret            | Number | 错误码，0成功  |
| result.msg    | String | 取消结果提示 `canceled`） |
| result.message   | String | 取消结果提示   |

### 使用场景

#### 场景1：用户下单未支付，锁定期内时间冲突

```
用户在锁定期（expire_time 之前）内修改了到店时间或更换了门店
    ↓
用户选择的新时段与原订单冲突（或直接需要放弃原订单）
    ↓
调用 cancelBookOrder 释放原订单锁定的包厢
    ↓
向用户确认是否要基于新的时间/门店重新查询并下单
```

**处理步骤**：
1. 调用 `cancelBookOrder(opid=原订单operate_id)` 取消原订单
2. 调用 `queryRoomAvailability` 按新的时间/门店查询可预订时段
3. 按展示规范展示新时段供用户选择
4. 用户选定后调用 `roomHourCreateOrder` 创建新订单

#### 场景2：用户已支付，未开房，主动取消

```
用户已完成支付但尚未到店开房，主动要求取消订单
    ↓
调用 cancelBookOrder 取消订单，触发退款流程
    ↓
告知用户"订单已取消，退款将按原支付渠道退回，预计 X 个工作日到账"
```

**处理步骤**：
1. 先向用户确认取消意图（避免误操作）："确认要取消订单 {opid} 吗？已支付金额将原路退回。"
2. 用户确认后调用 `cancelBookOrder(opid=operate_id)`
3. 告知用户取消成功并说明退款到账时间

**❌ 异常返回示例**：

```json
// 订单已开房，不可取消
{
  "result": {
    "ret": 10,
    "message": "订单已入店消费，无法取消",
    "msg": "订单已入店消费，无法取消"
  },
  "msg": "",
  "ret": 0
}

// 订单已自动取消
{
  "result": {
    "ret": 25,
    "message": "订单已自动取消",
    "msg": "订单已自动取消"
  },
  "msg": "",
  "ret": 0
}

// 订单已过期
{
  "ret": -2,
  "msg": "订单已过期，无法取消",
  "data": null
}
```

---

## getOrderDetail - 查询订单详情

**用途**：查询订单的当前详情（支付状态、消费状态等），用于支付状态轮询。

**调用方式**：

```bash
km-bot call saasktv getOrderDetail "{\"oid\":\"7608052439251950\"}"
```

**请求参数**：

| 字段 | 类型   | 必填   | 说明                                                              |
| ---- | ------ | ------ | ----------------------------------------------------------------- |
| oid | String | **是** | 订单号（来自 `roomHourCreateOrder` 返回的 `operate_id`） |

**成功返回示例**：

```json
{
  "data": {
    "operate_id": "7608052439251950",
    "source_name": "美团团购",
    "guest_name": "张三",
    "guest_tel": "13800138000",
    "destine_date_time": "2026-08-06 18:05:24",
    "used_date": "2026-08-06",
    "used_begin_time": "19:00",
    "used_end_time": "21:00",
    "status_name": "已支付",
    "charge": 120,
    "status": "1",
    "source": "7",
    "parent_order_id": "",
    "buy_break_name": "欢唱3小时套餐",
    "open_begin_time": "19:05",
    "open_end_time": "",
    "ecard_desc": "",
    "ecard_charge": ""
  },
  "msg": "",
  "ret": 0
}
```

**返回字段说明**：

| 字段                    | 类型   | 说明                                                              |
| ----------------------- | ------ | ----------------------------------------------------------------- |
| ret                     | Number | 错误码，0成功                                                    |
| data.operate_id         | String | 订单id                                                            |
| data.source_name        | String | 来源名称（如"美团团购"）                                          |
| data.guest_name         | String | 用户名称                                                          |
| data.guest_tel          | String | 用户电话                                                          |
| data.destine_date_time  | String | 下单时间                                                          |
| data.used_date          | String | 营业日                                                            |
| data.used_begin_time    | String | 开始时间                                                          |
| data.used_end_time      | String | 结束时间                                                          |
| data.status_name        | String | 状态名称（如"待支付"/"已支付"等）                                 |
| data.charge             | Number | 订单金额                                                          |
| data.status             | String | 订单状态码（**String 类型**，如 "0", "1", "2", "3", "4" 等）      |
| data.source             | String | 预订渠道                                                          |
| data.parent_order_id    | String | 批次id（续单关联）                                                |
| data.buy_break_name     | String | 套餐名称                                                          |
| data.open_begin_time    | String | 开房开始时间                                                      |
| data.open_end_time      | String | 开房结束时间                                                      |
| data.ecard_desc         | String | VIP卡描述                                                          |
| data.ecard_charge       | String | VIP卡金额                                                          |

### 订单状态码说明（status 为 String 类型）
| status | 含义     | 备注                                     |
| ------ | -------- | ---------------------------------------- |
| "0"    | 待支付   | 用户下单但未支付                         |
| "1"    | 已支付   | **轮询成功判定条件之一**                 |
| "2"    | 确认中   | 支付确认中，视为已支付                   |
| "3"    | 已确认   | 支付已确认，视为已支付                   |
| "4"    | 开房中   | 已入店消费，视为已支付                   |
| "5"    | 未付款已撤单   | 未付款已自动取消                               |
| "6"   | 已退款   | 用户已退款                           |
| "7"   | 已撤单   | 已退款                                   |

> ⚠️ **轮询成功判定**：`status ∈ {"1", "2", "3", "4"}` 均视为**已支付**，应立即结束轮询并展示预约成功页面。
