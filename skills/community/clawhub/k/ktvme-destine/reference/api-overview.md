# API 概览与通用约束

> ⚠️ **前置依赖**：本接口文档依赖 `km-bot` 工具。详见 [cli-install.md](./cli-install.md)

---

## 接口分类速查

| 接口                    | category | 用途                                 | 所属文件         | 主流程 |
| ----------------------- | -------- | ------------------------------------ | ---------------- | ------ |
| searchCompany           | saasktv  | 查询门店列表                         | api-store.md     | ✅     |
| switchCompany           | saasktv  | 切换当前门店                         | api-store.md     | ✅     |
| queryRoomAvailability   | saasktv | 包厢可预订情况聚合查询                  | api-room.md      | ✅     |
| roomHourCreateOrder     | saasktv  | 创建订单                             | api-order.md     | ✅     |
| cancelBookOrder         | saasktv  | 取消预订订单（释放锁房/触发退款）    | api-order.md     | ✅     |
| getOrderDetail          | saasktv  | 查询订单状态（支付状态轮询）         | api-order.md     | ✅     |
| sessionInfo             | saasktv  | 查询登录状态                         | api-session.md   | ✅     |
| sendVerifyCode          | saasktv  | 发送验证码                           | api-session.md   | ✅     |
| loginByCode             | saasktv  | 手机号验证码登录                     | api-session.md   | ✅     |

> 💳 **支付**：下单接口 `roomHourCreateOrder` 成功后**直接返回** `payment_link` / `qr_code` / `expire_time`，无需调用独立支付接口。详见 [api-order.md](./api-order.md)。

---

## 字段映射速查表

### 门店相关字段

| 业务含义 | 字段名           | 类型   | 用于                                  | 来源                                                 |
| -------- | ---------------- | ------ | ------------------------------------- | ---------------------------------------------------- |
| 商家编码 | `company_code`   | String | switchCompany 参数                    | searchCompany 返回的 `companycode`（数组，取第一个） |
| 商家ID   | `company_id`     | Number | 查询接口参数（queryRoomAvailability 等） | searchCompany 返回的 `companyid`                     |
| 商家名称 | `companyname`    | Array  | 展示给用户                            | searchCompany 返回                                   |
| 商家地址 | `companyaddress` | Array  | 展示给用户                            | searchCompany 返回                                   |

> ⚠️ **重要区分**：
>
> - `switchCompany` 使用 **`company_code`**（字符串，来自 `companycode` 数组）
> - 查询接口使用 **`company_id`**（数字，来自 `companyid`）
> - 下单接口（roomHourCreateOrder）**不传入** `company_id`，由后端自动识别

### 订单相关字段

| 业务含义     | 字段名            | 类型   | 格式/来源                                                 |
| ------------ | ----------------- | ------ | --------------------------------------------------------- |
| 包厢ID       | `roomid`          | Number | 来自 queryRoomAvailability 返回的 `room_id`               |
| 开始时间     | `begintime`       | String | 来自 queryRoomAvailability 返回的 `begintime`（yyyy-MM-dd HH:mm）|
| 结束时间     | `endtime`         | String | 来自 queryRoomAvailability 返回的 `endtime`（yyyy-MM-dd HH:mm）  |
| 售价         | `charge`          | String | 来自 queryRoomAvailability 返回的 `charge`（直接使用）    |
| 原价         | `protocolcharge`  | String | 来自 queryRoomAvailability 返回的 `protocolcharge`（直接使用）|
| 活动ID       | `id`              | Number | 来自 queryRoomAvailability 返回的 `activity_id`           |

### 下单返回的支付字段（roomHourCreateOrder 响应）

| 业务含义   | 字段名          | 类型   | 说明                                                                 |
| ---------- | --------------- | ------ | -------------------------------------------------------------------- |
| 订单号     | `operate_id`    | String | 订单号                                                               |
| 支付链接   | `payment_link`  | String | 支付页面 URL，必须展示成超链接，引导用户扫码或打开链接扫码支付          |
| 支付二维码 | `qr_code`       | String | 支付二维码url，直接在线展示，无需下载，无需思考，**直接展示扫码（≤ 200×200）**           |
| 有效期     | `expire_time`   | String | 锁定包厢 + 支付时间（yyyy-MM-dd HH:mm:ss），**超出无法下单**         |

> ⚠️ **超时由轮询自动处理**：展示二维码后启动 `poll_order_status.py` 后台轮询（5秒/次，最长6分钟），检测到已支付（status ∈ {1,2,3,4}）则展示成功页，超时未支付则展示超时提示并返回 Step 4 重新查询时段。

### getOrderDetail 响应（订单详情查询）

| 业务含义   | 字段名               | 类型   | 说明                                                                 |
| ---------- | -------------------- | ------ | -------------------------------------------------------------------- |
| 订单id     | `operate_id`         | String | 订单id                                                               |
| 来源名称   | `source_name`        | String | 来源名称（如"美团团购"）                                              |
| 用户名称   | `guest_name`         | String | 用户名称                                                             |
| 用户电话   | `guest_tel`          | String | 用户电话                                                             |
| 下单时间   | `destine_date_time`  | String | 下单时间                                                             |
| 营业日     | `used_date`          | String | 营业日                                                               |
| 开始时间   | `used_begin_time`    | String | 开始时间                                                             |
| 结束时间   | `used_end_time`      | String | 结束时间                                                             |
| 状态名称   | `status_name`        | String | 状态名称（如"待支付"/"已支付"等）                                    |
| 订单金额   | `charge`             | Number | 订单金额                                                             |
| 状态码     | `status`             | String | **String 类型**，"0":待支付 / "1-4":已支付（轮询成功条件）/ "-1":已取消 / "-2":已退款 |
| 预订渠道   | `source`             | String | 预订渠道                                                             |
| 批次id     | `parent_order_id`    | String | 批次id（续单关联）                                                   |
| 套餐名称   | `buy_break_name`     | String | 套餐名称                                                             |
| 开房开始   | `open_begin_time`    | String | 开房开始时间                                                         |
| 开房结束   | `open_end_time`      | String | 开房结束时间                                                         |
| VIP卡描述  | `ecard_desc`         | String | VIP卡描述                                                            |
| VIP卡金额  | `ecard_charge`       | String | VIP卡金额                                                            |

### 会话相关字段

| 业务含义 | 字段名        | 类型   | 说明                               |
| -------- | ------------- | ------ | ---------------------------------- |
| 登录状态 | `status`      | Number | 0:未登录 1:已登录                  |
| 用户ID   | `customer_id` | String | 仅供前端识别，**不可作为接口参数** |
| 手机号   | `phone`       | String | 仅供前端展示，**不可作为接口参数** |

---

## ⚠️ 绝对禁止事项（必须遵守）

### 1. 下单接口禁止传入的字段（强制约束）

> ⚠️ **【严重警告】以下字段绝对禁止传入 `roomHourCreateOrder` 接口，即使值为1、0或默认值也必须省略！后端会强制替换这些字段，传入会导致订单绑定错误用户或商家。**

**禁止字段清单**：

| 禁止字段                     | 说明        | 传入后果                               |
| ---------------------------- | ----------- | -------------------------------------- |
| `customer_id` / `customerid` | 用户ID      | 后端强制替换，可能导致订单绑定错误用户 |
| `phone` / `guesttel`         | 手机号      | 后端忽略或覆盖                         |
| `kmid`                       | 会员ID      | 后端强制替换                           |
| `xcxappid`                   | 小程序appid | 后端强制替换                           |
| `openid`                     | 微信openid  | 后端强制替换                           |
| `company_id` / `companyid`   | 商家ID      | 后端强制替换，可能导致订单属于错误商家 |

**适用接口**：`roomHourCreateOrder`

**✅ 正确示例**：

```json
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

### 2. 用户未登录时禁止创建订单

**前置检查**：调用 `sessionInfo` 检查 `status`

**正确流程**：

```
sessionInfo → status=1 → 创建订单
sessionInfo → status=0 → 先调用 subflow-login 完成登录 → 再创建订单
```

### 3. 用户选择门店后必须调用 switchCompany

> ⚠️ **【强制要求】每次用户选择门店后必须调用 switchCompany**
>
> **未调用此接口导致的后果**：
>
> - 后端会话上下文不会切换到新门店
> - 后续所有接口调用（queryRoomAvailability/创建订单等）将在错误的门店上下文中执行
> - 用户预订失败或预订到错误的门店

**正确流程**：

```
searchCompany → 用户选择门店 → switchCompany(company_code) → 后续接口调用
```

**⚠️ 特别注意**：

> 即使用户直接指定门店名称（如"预订NEO KTV"），模型仍需：
>
> 1. 调用 `searchCompany(keyword="NEO KTV")` 确认门店存在
> 2. 从返回结果中获取对应的 `companycode`
> 3. 再调用 `switchCompany(company_code)`
>
> **原因**：`companycode` 是内部编码（如 "01171"），用户不会直接提供，模型无法自行确定。必须通过 `searchCompany` 确认和获取。

### 4. 验证码发送必须遵守频率限制

| 限制项       | 值    | 超出后的错误提示                           |
| ------------ | ----- | ------------------------------------------ |
| 发送间隔     | ≥60秒 | "验证码发送过于频繁，请60秒后再尝试"       |
| 24小时上限   | 5次   | "今日验证码发送次数已达上限，请明日再尝试" |
| 验证码有效期 | 5分钟 | 超时需重新获取                             |
| 验证码一次性 | 是    | 验证成功后立即失效                         |

---

## 通用错误处理原则

详见 `error-handling.md`

### 常见错误处理策略

| 错误类型                         | 处理策略                              |
| -------------------------------- | ------------------------------------- |
| 网络超时                         | 等待1秒后重试，最多3次                |
| searchCompany 超时               | 等待3-5秒后重试，最多3次（首次调用偶尔超时）|
| queryRoomAvailability 返回空     | 检查是否传了 begintime/endtime（不传必返回空）|
| 参数校验失败                     | 检查 api-overview.md 中的字段要求     |
| 业务逻辑错误（如时段的包厢已满） | 向用户说明情况，询问是否更换时段/包厢 |
| 会话过期（status=0）             | 调用 subflow-login 完成登录后重试     |

---

## 快速导航

- 预订主流程 → [SKILL.md](../SKILL.md)
- 登录子流程 → [subflow-login.md](./subflow-login.md)
- 支付子流程 → [subflow-pay.md](./subflow-pay.md)
- 门店API → [api-store.md](./api-store.md)
- 包厢API → [api-room.md](./api-room.md)
- 订单API → [api-order.md](./api-order.md)（含下单返回的支付字段）
- 会话API → [api-session.md](./api-session.md)
- 错误处理 → [error-handling.md](./error-handling.md)
