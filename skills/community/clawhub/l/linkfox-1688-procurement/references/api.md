# 1688采购流程 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/alibaba1688/<endpoint>`，默认网关为 `https://tool-gateway.linkfox.com`
- **请求方式**：POST，Content-Type: `application/json; charset=utf-8`
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置，按 SKILL.md 的 **## 解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s
- **缓存**：本采购 Skill 不做 24h 响应缓存；授权、价格、库存、订单状态和物流以实时返回为准，高风险写操作不得缓存或自动重放。

Windows 推荐使用 `--payload-env` 或 `--payload-file`，避免 shell 转义破坏 JSON。

```powershell
$env:PAYLOAD = "{}"
python scripts/authorized_stores.py --payload-env PAYLOAD --inline
```

## API 与脚本

| 能力 | Path | Script | 风险 | OAuth 前置检查 | 确认字段 |
|---|---|---|---|---|---|
| 生成授权链接 | `/alibaba1688/authorizeUrl` | `authorize_url.py` | 低 | 否 | - |
| 查询已授权账号 | `/alibaba1688/authorizedStores` | `authorized_stores.py` | 低 | 否 | - |
| 查询收货地址 | `/alibaba1688/receiveAddressList` | `receive_address_list.py` | 低 | 是 | - |
| 查询 SKU | `/alibaba1688/sku` | `sku.py` | 低 | 是 | - |
| 下单预览 | `/alibaba1688/orderPreview` | `order_preview.py` | 中 | 是 | - |
| 创建订单 | `/alibaba1688/createOrder` | `create_order.py` | 高 | 是 | `confirmCreateOrder=true` |
| 获取支付链接 | `/alibaba1688/paymentUrl` | `payment_url.py` | 高 | 是 | `confirmGetPaymentUrl=true` |
| 查询订单状态 | `/alibaba1688/orderStatus` | `order_status.py` | 低 | 是 | - |
| 查询物流 | `/alibaba1688/logistics` | `logistics.py` | 低 | 是 | - |
| 查询物流轨迹 | `/alibaba1688/logisticsTrace` | `logistics_trace.py` | 低 | 是 | - |
| 确认收货 | `/alibaba1688/confirmReceive` | `confirm_receive.py` | 高 | 是 | `confirmReceive=true` |
| 取消订单 | `/alibaba1688/cancelOrder` | `cancel_order.py` | 高 | 是 | `confirmCancel=true` |
| 查询可开票金额 | `/alibaba1688/invoiceAmount` | `invoice_amount.py` | 低 | 是 | - |
| 申请开票 | `/alibaba1688/invoiceApply` | `invoice_apply.py` | 高 | 是 | `confirmApplyInvoice=true` |

`_alibaba1688_imageSearch` 由 `linkfox-1688-search-by-image` 独立承担，本 Skill 不包含图搜脚本。不要把 `/alibaba1688/proxy/callback`、`/alibaba1688/authorizeCallback`、`/alibaba1688/oauth/callback` 暴露为 Skill 能力。

## 请求参数

POST Body（JSON）：

| 能力 | 参数 | 必填 | 说明 |
|---|---|---:|---|
| `authorizeUrl` | `accountName` | 是 | 授权账号展示名，用于标识本次 1688 OAuth 授权。 |
| `authorizedStores` | - | 否 | 通常传 `{}`。返回当前 LinkFox 用户的 1688 授权状态，不是全库账号列表。 |
| `receiveAddressList` | - | 否 | 通常传 `{}`。返回当前用户可用收货地址。 |
| `sku` | `offerId` | 是 | 1688 商品 ID，必须用字符串，避免 JS 大数精度丢失。 |
| `orderPreview` | `addressId` 或 `addressParam` | 条件必填 | 二选一。优先使用 `receiveAddressList` 返回的 `addressId`；`addressParam` 至少含 `fullName`、`mobile`、`address`。 |
| `orderPreview` | `cargoParamList` | 是 | 货品列表，每项含 `offerId`、可选 `specId`、`quantity`；`quantity >= 1`。 |
| `orderPreview` | `flow` | 是 | 下单流程类型。当前主流程为普通采购，默认 `general`；脚本缺省时会补 `general`，直接调 API 时必须显式传。仅当用户明确要求分销/精选货源分销时，才可透传 `fenxiao`/`boutiquefenxiao`；本 Skill 不提供分销专属校验或保障。 |
| `orderPreview` | `isvBizType` | 否 | 默认 `cross`；仅支持 `cross`、`cross_daigou`、`cross_distribution`。 |
| `createOrder` | `confirmCreateOrder` | 是 | 必须是 JSON boolean `true`。未传或 false 时不会调用 1688 下单。 |
| `createOrder` | 下单参数 | 是 | 与 `orderPreview` 保持一致，必须显式包含相同 `flow`；可额外传 `message`、`tradeType`、`shopPromotionId`、`useRedEnvelope`、`anonymousBuyer`、`outOrderId` 等。 |
| `createOrder` | `useRedEnvelope` | 否 | 是否使用红包，仅支持 `y`/`n`；默认 `n`。 |
| `paymentUrl` | `confirmGetPaymentUrl` | 是 | 必须是 JSON boolean `true`。只获取支付链接，不自动打开、不自动支付。 |
| `paymentUrl` | `orderIdList` | 是 | 1688 订单 ID 字符串数组。使用 `createOrder` 返回的 `orderId`。 |
| `orderStatus` | `aliOrderId` | 是 | 1688 订单 ID 字符串；可使用 `createOrder` 返回的 `orderId`。 |
| `logistics` | `aliOrderId` | 是 | 1688 订单 ID 字符串；可使用 `createOrder` 返回的 `orderId`。 |
| `logisticsTrace` | `aliOrderId` | 是 | 1688 订单 ID 字符串；可使用 `createOrder` 返回的 `orderId`。 |
| `logisticsTrace` | `logisticsId` | 否 | 物流订单 ID；多个物流单时建议从 `logistics` 返回中选择。 |
| `confirmReceive` | `aliOrderId` | 是 | 1688 订单 ID 字符串；可使用 `createOrder` 返回的 `orderId`。 |
| `confirmReceive` | `confirmReceive` | 是 | 必须是 JSON boolean `true`。确认收货不可逆，需用户单独中文确认。 |
| `cancelOrder` | `aliOrderId` | 是 | 1688 订单 ID 字符串；可使用 `createOrder` 返回的 `orderId`。 |
| `cancelOrder` | `confirmCancel` | 是 | 必须是 JSON boolean `true`。取消订单不可逆，需用户单独中文确认。 |
| `cancelOrder` | `cancelReason`、`remark` | 否 | 取消原因和备注，非空时透传。 |
| `invoiceAmount` | `orderIds` | 是 | 1688 订单 ID 字符串数组，至少 1 项，每项必须为数字字符串；可使用 `createOrder` 返回的 `orderId`。 |
| `invoiceApply` | `confirmApplyInvoice` | 是 | 必须是 JSON boolean `true`。申请开票高风险且不可逆，需用户单独中文确认。 |
| `invoiceApply` | `invoiceApplyModelList` | 是 | 开票申请列表，至少 1 项，每项见下「开票申请逐单模型」。 |
| `invoiceApply` | 逐单 `amount` | 是 | 必须通过 `invoiceAmount` 查到的可开票金额**原样传入**，不得自行计算；单位为分（1元=100分）。 |
| `invoiceApply` | 逐单 `invoiceType` | 是 | `VATAX_COMM`（增值税普通发票）/ `VATAX_SPEC`（增值税专用发票）。 |
| `invoiceApply` | 逐单 `purchaserInvoiceTitleModel` | 是 | 买家发票抬头，见下「开票抬头」。企业抬头建议经 1688 `trade.invoiceTitle.getPageList` 查到既有抬头后原样传入，避免手填不一致。 |

### 开票相关对象

`invoiceApplyModelList` 每项结构：

```json
{
  "orderId": "3309156590237728779",
  "amount": 30500,
  "invoiceType": "VATAX_COMM",
  "purchaserInvoiceTitleModel": {
    "titleType": "COMPANY",
    "title": "深圳某某科技有限公司",
    "taxpayerIdentify": "91440300MA5XXXXXX"
  }
}
```

`purchaserInvoiceTitleModel`（开票抬头）：

| 字段 | 必填 | 说明 |
|---|---|---|
| `titleType` | 是 | `PERSONAL`（个人和社会组织）/ `COMPANY`（企业） |
| `title` | 是 | 发票抬头 |
| `taxpayerIdentify` | 条件必填 | 纳税人识别号，**企业开票必填** |
| `bankName` | 条件必填 | 开户行，**企业开专票必填** |
| `bankAccountId` | 条件必填 | 银行账号，**企业开专票必填** |
| `registerAddress` | 条件必填 | 企业注册地址，**企业开专票必填** |
| `registerPhone` | 条件必填 | 企业电话，**企业开专票必填** |

> 条件必填规则：`titleType=COMPANY`（不论普票/专票）须填 `taxpayerIdentify`；`titleType=COMPANY` 且 `invoiceType=VATAX_SPEC`（企业开专票）须再填 `bankName`/`bankAccountId`/`registerAddress`/`registerPhone` 四项；`titleType=PERSONAL` 以上条件字段可不填。违反返回错误码 `1002` 且不调用 1688。

### 常用对象

`cargoParamList` 示例：

```json
[
  {
    "offerId": "1234567890123456789",
    "specId": "456789012345678901",
    "quantity": 2
  }
]
```

`addressParam` 示例：

```json
{
  "fullName": "张三",
  "mobile": "13800000000",
  "provinceText": "广东省",
  "cityText": "深圳市",
  "areaText": "南山区",
  "address": "科技园示例路 1 号"
}
```

## 响应结构

| 能力 | 关键响应字段 | 说明 |
|---|---|---|
| `authorizeUrl` | `authorizeUrl` | 1688 授权链接。给用户手动打开，不自动打开，不返回 token。 |
| `authorizedStores` | `stores[].accountName/status/expired` | 继续采购必须满足 `status=ACTIVE` 且 `expired=false`。`expired=true` 表示当前授权不可用，通常是 refreshToken 为空、失效或刷新失败；accessToken 普通过期会由后端在调用 `authorizedStores` 或业务接口时自动刷新，不需要重新授权。即使后端响应包含 token 过期时间，也只作内部判断，不要展示给用户。 |
| `receiveAddressList` | `items[].addressId/fullName/mobile/provinceText/cityText/areaText/address/isDefault` | 多地址时让用户明确选择；展示手机号和详细地址时注意脱敏。 |
| `sku` | `offerId`、`skuList[].specId/skuId/price/amountOnSale/attributes/skuImageUrl` | 多 SKU 商品下单时使用 `specId`。SKU 价格和库存仅作规格选择参考，真实可购性、最终价格、运费和优惠以 `orderPreview` 为准。 |
| `orderPreview` | `status`、`message`、`sumPayment`、`sumCarriage`、`discountFee`、`cargoList`、`tradeModelList`、`payChannelInfos`、`shopPromotionList` | `sumPayment/sumCarriage/discountFee` 单位为分；`cargoList.finalUnitPrice/amount` 单位为元，展示时不要混算。支付渠道有可读名称时展示可读名称；只有编码时原样展示，不要猜测含义。 |
| `orderPreview` 业务失败 | `errcode=200` 但 `status=false`、`message`、金额为 0、交易/支付/优惠列表为空 | 收到预览返回不代表可以下单。停止创建订单，展示上游 `message`，并复核 SKU/规格、起批量、售卖单位、`quantity` 和收货地址。 |
| `createOrder` | `success`、`orderId`、`message`、`code` | `orderId` 是 1688 订单号；后续 `paymentUrl` 用它组成订单号数组，状态/物流/取消/确认收货可将它作为 `aliOrderId` 使用。 |
| `paymentUrl` | `success`、`payUrl`、`errorMessage`、`errorCode` | 支付链接只展示给用户手动打开；不要自动打开、自动支付或无必要重复展示。 |
| `orderStatus` | `aliOrderId`、`aliStatus`、`normalizedStatus` | 用于判断订单当前履约阶段。 |
| `logistics` | `aliOrderId`、`logisticsOrders[].logisticsId/logisticsBillNo/logisticsCompanyName/status` | `logisticsId` 可用于查询轨迹。 |
| `logisticsTrace` | `aliOrderId`、`logisticsId`、`traceList[].traceTime/location/traceDescription/traceStatus` | 轨迹时间按 Asia/Shanghai 展示。 |
| `confirmReceive` | `success`、`aliOrderId` | 确认收货结果。 |
| `cancelOrder` | `success`、`aliOrderId`、`orderId`、`message` | 仅表示尝试取消 1688 订单的结果；不是退款或售后申请，不保证退款。是否允许取消由 1688 根据订单状态判断。`orderId` 是兼容出参；后续请求仍按各接口要求使用 `aliOrderId` 或 `orderIdList`。 |
| `invoiceAmount` | `success`、`code`、`message`、`subCode`/`subMessage`、`retCodes[]`、`orderInvoiceAmountModelList[].{orderId, amount}` | `amount` 单位为**分**，须原样传入 `invoiceApply`，不得换算或自行计算；逐单返回码 `retCodes` 与列表逐项对应。`success=false`（如订单不存在/已取消/不可开票）时 HTTP 仍 200，属业务结果，非错误；下游据 `retCodes`/列表判断各订单是否可取到金额。 |
| `invoiceApply` | `success`、`code`、`message`、`subCode`/`subMessage`、`successList[]`、`failedList[]` | 批量逐单成败独立，须遍历 `successList`/`failedList` 处理，不要只看顶层 `success`。逐单结果含 `orderId`、`outBizId`、`result`、`tradeOrderCompleted`、`errorCode`、`errorDesc`。`INVOICE_ALREADY_APPLIED`（落在 `failedList`）表示该订单历史已开过票，按「已开票」语义处理，不必报错。业务失败 HTTP 仍 200，仅 `code=1003` 或 4xx/5xx 才视为传输异常。开票成功不可在系统侧回滚，红冲需联系商家。 |

## 高风险校验

用户侧只需要用中文自然语言做单独明确确认，例如“确认”“确认创建这个订单”“确认获取这个订单的支付链接”“确认取消这个订单”“确认收货”。只有当上一条消息已明确复述一个具体高风险动作和对象时，单独回复“确认”才算有效；不要要求用户输入英文参数名或 `=true`，也不要向普通用户展示内部确认字段、请求字段名或实现细节。

Agent 在收到中文确认后，调用脚本时必须自动加入对应 JSON boolean 安全字段。字符串 `"true"`、数字 `1`、大小写变体都不算确认。这些字段只用于脚本调用和排错，不属于用户可见流程文案。

| 脚本 | 本地拒绝条件 |
|---|---|
| `create_order.py` | 缺少 JSON boolean `confirmCreateOrder=true` |
| `payment_url.py` | 缺少 JSON boolean `confirmGetPaymentUrl=true` |
| `confirm_receive.py` | 缺少 JSON boolean `confirmReceive=true` |
| `cancel_order.py` | 缺少 JSON boolean `confirmCancel=true` |
| `invoice_apply.py` | 缺少 JSON boolean `confirmApplyInvoice=true` |

## 错误码

| errcode / error | 含义 | 处理建议 |
|---|---|---|
| 200 | 请求已有返回 | 是否可继续下单以具体预览结果、订单结果或提示信息为准 |
| 401 / authorized error | 认证失败 | 按 SKILL.md 的 **## 解决认证和算力问题** 处理 |
| 402 | 算力或余额不足 | 按 SKILL.md 的 **## 解决认证和算力问题** 处理 |
| `authorization_required` | 当前用户没有 ACTIVE 且未过期的 1688 授权 | 先运行 `authorize_url.py`，用户授权后再运行 `authorized_stores.py` 验证 |
| `confirmation_required` | 高风险确认字段缺失或不是 JSON boolean `true` | 停止并让用户单独中文确认；不要自动补字符串 `"true"` |
| 1002 | 参数缺失或不合法 | 检查字段名、必填项、枚举值、订单号是否为数字字符串 |
| 1003 | 上游调用或业务失败 | 不要自动重试高风险写操作；向用户说明失败原因 |
| 1005 | 1688 授权缺失或失效 | 重新走授权检查/授权流程 |

错误响应示例：

```json
{
  "error": "authorization_required",
  "message": "1688 OAuth authorization is required before this procurement operation."
}
```

## curl 示例

### 查询授权状态

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/authorizedStores \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{}'
```

### 查询 SKU

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/sku \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{"offerId":"1234567890123456789"}'
```

### 下单预览

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/orderPreview \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "flow": "general",
    "addressId": "987654321012345678",
    "cargoParamList": [
      {
        "offerId": "1234567890123456789",
        "specId": "456789012345678901",
        "quantity": 2
      }
    ]
  }'
```

### 获取支付链接

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/paymentUrl \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "confirmGetPaymentUrl": true,
    "orderIdList": ["1234567890123456789"]
  }'
```

### 查询可开票金额

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/invoiceAmount \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{"orderIds": ["1234567890123456789"]}'
```

### 申请开票

高风险、不可逆，必须显式传 `confirmApplyInvoice=true`。`amount` 取自上一步 `invoiceAmount` 返回值，原样传入。

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/invoiceApply \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "confirmApplyInvoice": true,
    "invoiceApplyModelList": [
      {
        "orderId": "1234567890123456789",
        "amount": 30500,
        "invoiceType": "VATAX_COMM",
        "purchaserInvoiceTitleModel": {
          "titleType": "COMPANY",
          "title": "深圳某某科技有限公司",
          "taxpayerIdentify": "91440300MA5XXXXXX"
        }
      }
    ]
  }'
```

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-1688-procurement",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-1688-procurement`)
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise. Do not include API keys, tokens, full addresses, phone numbers, or payment URLs.
