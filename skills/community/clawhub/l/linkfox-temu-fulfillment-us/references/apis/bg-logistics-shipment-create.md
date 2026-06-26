# 在线下单购标 — `bg.logistics.shipment.create`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_buy_shipping_logistics_shipment_create.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=1eadab72ed8041318604b163dd75cdac |
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.shipment.create`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.logistics.shipment.create` interface is for sellers to place online logistics orders and receive package numbers, which enables sellers to effortlessly place logistics orders with selected carriers online.（卖家在线向 Temu 集成承运商下单购标，创建包裹并获取 **packageSn**；是 Buy-Shipping 购标核心接口。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：** `warehouseId` 来自 **`bg.logistics.warehouse.list.get`**；`channelId` / `shipCompanyId` / `shipLogisticsType` / `signServiceId` 等来自 **`bg.logistics.shippingservices.get`** 或 **`temu.logistics.shiplogisticstype.get`**；`parentOrderSn` / `orderSn` / `quantity` 来自 **`linkfox-temu-order-us`**。  
> **异步说明：** 部分场景下单为异步处理；若返回成功但无运单，请用 [**`bg.logistics.shipment.result.get`**](./bg-logistics-shipment-result-get.md) 按 **`packageSnList`** 查询结果（错误码 `120012013`）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── sendType                    ← 必填
    ├── sendRequestList[]           ← 选填（Package List Information；实际购标须传）
    │   ├── warehouseId
    │   ├── weight / weightUnit / extendWeight / extendWeightUnit
    │   ├── length / width / height / dimensionUnit
    │   ├── shipCompanyId
    │   ├── channelId               ← 与 shipLogisticsType 二选一履约方式
    │   ├── shipLogisticsType       ← 与 channelId 二选一履约方式
    │   ├── signServiceId
    │   ├── pickupStartTime / pickupEndTime
    │   ├── orderSendInfoList[]
    │   │   ├── parentOrderSn
    │   │   ├── orderSn
    │   │   ├── goodsId
    │   │   ├── skuId
    │   │   └── quantity
    │   ├── confirmAcceptance[]
    │   ├── splitSubPackage
    │   ├── sendSubRequestList[]    ← splitSubPackage=true 时必填
    │   │   └── （附属包裹：尺寸/重量/渠道/仓库等，结构见下）
    │   ├── interlineShipCompanyList[]  ← 联运/分段渠道时必填
    │   │   ├── shipStageType
    │   │   ├── shipLogisticsType
    │   │   ├── shipCompanyId
    │   │   └── channelId
    │   ├── cooperativeWarehouseShipment
    │   ├── uspsMailingDateOffset
    │   └── autoConfirmAfterPickup
    ├── shipLater                   ← 选填
    └── shipLaterLimitTime          ← 选填（shipLater=true 时按订单标签传）
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sendType | INTEGER | **是** | SendType（发货方式），见下表 |
| sendRequestList | OBJECT[] | 否* | Package List Information（包裹列表信息；购标时**须传**至少一个包裹） |
| shipLater | BOOLEAN | 否 | Ship Later（是否稍后发货），见下表 |
| shipLaterLimitTime | STRING | 否 | 稍后发货截止时间（小时数，字符串形式），见下表 |

\* Partner Request 表将 **`sendRequestList`** 标为选填（False），但购标业务**必须**传入有效包裹明细。

#### `sendType`

| 值 | 说明 |
|----|------|
| `0` | All the products in **one parent order** are shipped in **one package** with **one tracking number**（同一父订单全部商品，一个包裹、一个运单号） |
| `1` | **Partial** products in one parent order are shipped in **multiple packages** with multiple tracking numbers; **all products in that parent order must be submitted in one API call**（同一父订单部分商品拆多包裹；该父订单下所有待发商品须在一次调用中全部提交） |
| `2` | All the products in **multiple parent orders** are shipped in **one package** with **one tracking number**（多个父订单合并为一个包裹、一个运单号） |

#### `shipLater`

| 值 | 说明 |
|----|------|
| `true` | Apply to create the package and tracking numbers from Temu-integrated carriers online; mark this package as **「ship later」**（在线购标并创建运单，包裹标记为稍后发货）。带 **「Y2_advance_sale」** 标签的订单购标时**必须**设为 `true`（错误码 `120015534`） |
| `false` | Apply to create the package and tracking numbers online, **ship the package immediately** and mark as shipped（在线购标、创建运单并立即发货）。**COD 订单**不允许 `shipLater=true`（错误码 `120011053`） |

#### `shipLaterLimitTime`

| 订单标签 | 可选值（小时，字符串） |
|----------|------------------------|
| **无** `Y2_advance_sale` 标签 | `24`, `48`, `72`, `96`, `120` |
| **有** `Y2_advance_sale` 标签 | `144`, `168`, `192`, `216`, `240`, `264`, `288`, `312`, `336`, `360` |

> 无效枚举将报错 `120015532`。与 **`shipLater=true`** 配合使用，表示稍后发货的截止时间。

#### `sendRequestList[]` 元素字段

> Partner Request 表中 `sendRequestList` 子行在导出 HTML 中为折叠状态；下列字段、类型与说明来自 **Request 表**（顶层）、**Request Example**、**Response Example** 关联字段及 Partner **Error Code** 表。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| warehouseId | STRING | **是** | Warehouse ID（发货仓库 ID；来自 **`bg.logistics.warehouse.list.get`** 的 **`warehouseId`**） |
| weight | STRING | **是** | 包裹重量。美国本地：整数**磅**写在 **`weight`**，小数/盎司部分写在 **`extendWeight`**（单位 **`oz`**）；须为整数时见错误码 `120015521` |
| weightUnit | STRING | **是** | 重量单位。美国包裹：**`lb`**；其他国家：**`kg`** |
| extendWeight | STRING | 否 | 扩展重量（美国本地订单的小数/盎司部分） |
| extendWeightUnit | STRING | 否 | 扩展重量单位。美国本地：**`oz`** |
| length | STRING | **是** | 包裹长度，保留两位小数 |
| width | STRING | **是** | 包裹宽度，保留两位小数 |
| height | STRING | **是** | 包裹高度，保留两位小数 |
| dimensionUnit | STRING | **是** | 尺寸单位。美国：**`in`**；其他国家：**`cm`** |
| shipCompanyId | INTEGER / LONG | **是** | Shipping company ID（物流公司 ID；与 **`bg.logistics.shippingservices.get`** 返回的 **`shipCompanyId`** 一致） |
| channelId | INTEGER / LONG | 条件 | Channel ID（物流渠道 ID；与 **`bg.logistics.shippingservices.get`** 返回的 **`channelId`** 一致）。与 **`shipLogisticsType`** **二选一**作为履约方式（错误码 `120015032`） |
| shipLogisticsType | STRING | 条件 | Ship logistics type（物流类型标识；来自 **`temu.logistics.shiplogisticstype.get`** 或查价返回）。选定后 Temu 可自动匹配推荐 **`channelId`**。与 **`channelId`** **二选一** |
| signServiceId | INTEGER | 否 | Signature service ID（签收/签名服务 ID；来自查价 **`onlineChannelDtoList[].signServiceId`**） |
| pickupStartTime | INTEGER | 条件 | Pickup window start time（预约上门揽收开始时间；**需要预约揽收的渠道**必填，见 **`pickupRules`** / **`availablePickupTimeSlotList`**） |
| pickupEndTime | INTEGER | 条件 | Pickup window end time（预约上门揽收结束时间；须晚于 **`pickupStartTime`**） |
| orderSendInfoList | OBJECT[] | **是** | Product list in this package（本包裹内要发货的商品行） |
| confirmAcceptance | STRING[] | 否 | Confirmation matters for this shipment（本批发货需确认的异常/预警事项），见下表 |
| splitSubPackage | BOOLEAN | 否 | 是否为**单件 SKU 拆多包裹**（`true`：单件 SKU 多包裹；`false`/不传：否）。为 `true` 时 **`quantity` 须为 1**（`120011045`），且须传 **`sendSubRequestList`** |
| sendSubRequestList | OBJECT[] | 条件 | Attached sub-packages for single-SKU multi-package scenario（单件 SKU 多包裹时的**附属包裹**列表；**最多 10 个**，`120011044`）。**COD 订单**不允许（`120011051`） |
| interlineShipCompanyList | OBJECT[] | 条件 | Interline / split-channel shipping legs（联运/分段渠道信息；使用分段渠道时**必填**，`120011111`） |
| cooperativeWarehouseShipment | BOOLEAN | 否 | Whether fulfillment uses **cooperative warehouse** mode（合作仓发货；部分渠道强制合作仓，`120018085`） |
| uspsMailingDateOffset | INTEGER | 条件 | USPS mailing date offset（USPS 邮寄日期偏移；部分 USPS 渠道禁止为 `0`，`120018086`） |
| autoConfirmAfterPickup | BOOLEAN | 否 | Auto-confirm shipment after pickup（揽收后自动确认发货） |

##### `orderSendInfoList[]` 元素字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent Order Number（父订单号） |
| orderSn | STRING | **是** | Order Number（子订单号）；每项**不可缺失**（`120011113`） |
| goodsId | LONG | **是** | Goods ID（商品 ID） |
| skuId | LONG | **是** | SKU ID |
| quantity | INTEGER | **是** | Quantity of the product（本行发货数量；**splitSubPackage=true** 时须为 1） |

##### `confirmAcceptance[]` 枚举值

| 值 | 说明 |
|----|------|
| `DENY_CANCELLATION` | Reject the cancellation request and proceed with shipment（拒绝取消申请后继续发货；订单存在待处理取消时，`120012030`） |
| `DENY_ADDRESS_CHANGE` | Reject the address change request and proceed（拒绝改地址申请后继续发货；`120012023`） |
| `DENY_PARENT_RISK_WARNING` | Reject/acknowledge parent order risk warning and proceed（确认父订单风控预警后继续发货；`120012031` / `120012061`） |
| `SUCCESSFUL_RETRY` | Confirm retry after a previous successful call（前次下 call 已成功后的再次请求确认） |
| `NO_DELIVERY_ON_SATURDAY` | Confirm Saturday non-delivery is acceptable（确认允许周六不派送） |

> 仅当订单存在对应待处理事项且商家选择继续发货时传入。

##### `sendSubRequestList[]` 元素字段

> 单件 SKU 拆多包裹时，主包裹 + 附属包裹共同完成发货；附属包裹**不含** `orderSendInfoList`（商品行在主包裹 **`sendRequestList`** 元素上）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| warehouseId | STRING | **是** | Warehouse ID（附属包裹发货仓库） |
| weight | STRING | **是** | 包裹重量 |
| weightUnit | STRING | **是** | 重量单位（美国 **`lb`**） |
| extendWeight | STRING | 否 | 扩展重量 |
| extendWeightUnit | STRING | 否 | 扩展重量单位（美国 **`oz`**） |
| length | STRING | **是** | 包裹长度 |
| width | STRING | **是** | 包裹宽度 |
| height | STRING | **是** | 包裹高度 |
| dimensionUnit | STRING | **是** | 尺寸单位（美国 **`in`**） |
| shipCompanyId | INTEGER / LONG | **是** | Shipping company ID |
| channelId | INTEGER / LONG | **是** | Channel ID |
| shipLogisticsType | STRING | 否 | Ship logistics type（若渠道按类型履约） |
| signServiceId | INTEGER | 否 | Signature service ID |
| pickupStartTime | INTEGER | 条件 | Pickup start time |
| pickupEndTime | INTEGER | 条件 | Pickup end time |
| interlineShipCompanyList | OBJECT[] | 条件 | Interline legs（结构同主包裹） |
| confirmAcceptance | STRING[] | 否 | Confirmation matters |

##### `interlineShipCompanyList[]` 元素字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| shipStageType | STRING | **是** | Shipping stage type（运输段类型，如首程/末程；与 **`bg.logistics.shippingservices.get`** 的 **`interlineChannelInfoList[].shipStageType`** 一致） |
| shipLogisticsType | STRING | **是** | Logistics type for this stage（该段物流类型标识） |
| shipCompanyId | INTEGER / LONG | **是** | Shipping company ID for this stage |
| channelId | INTEGER / LONG | **是** | Channel ID for this stage |

### 网关 `params` 写法（`sendType=0` 单包裹购标示例）

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "sendType": 0,
    "shipLater": false,
    "sendRequestList": [
      {
        "warehouseId": "WH-001",
        "length": "12.00",
        "width": "8.00",
        "height": "4.00",
        "dimensionUnit": "in",
        "weight": "2",
        "weightUnit": "lb",
        "extendWeight": "8",
        "extendWeightUnit": "oz",
        "shipCompanyId": 314439762,
        "channelId": 19409681780736,
        "orderSendInfoList": [
          {
            "parentOrderSn": "PO-20260101001",
            "orderSn": "O-20260101001-1",
            "goodsId": 6017592186252451,
            "skuId": 281474976920151,
            "quantity": 1
          }
        ]
      }
    ]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "sendType": 0,
    "shipLater": true,
    "shipLaterLimitTime": "48",
    "sendRequestList": [
      {
        "warehouseId": "WH-001",
        "shipLogisticsType": "USPS_GROUND_ADVANTAGE",
        "length": "12.00",
        "width": "8.00",
        "height": "4.00",
        "dimensionUnit": "in",
        "weight": "2",
        "weightUnit": "lb",
        "shipCompanyId": 314439762,
        "signServiceId": 1001,
        "pickupStartTime": 1717200000,
        "pickupEndTime": 1717203600,
        "orderSendInfoList": [
          {
            "parentOrderSn": "PO-20260101001",
            "orderSn": "O-20260101001-1",
            "goodsId": 6017592186252451,
            "skuId": 281474976920151,
            "quantity": 1
          }
        ],
        "confirmAcceptance": ["DENY_CANCELLATION"]
      }
    ]
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    ├── packageSnList[] (STRING[])
    ├── warningMessage[] (STRING[])
    └── shipLaterLimitTime (STRING)
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | result（业务结果对象） |

### `result` 内字段

> Partner Response 表中 `result` 子行在导出 HTML 中为折叠状态；下列字段来自 **Response Example** 与购标后续流程约定。

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSnList | STRING[] | Package SN list（本次下单创建的**包裹号**列表；用于 **`bg.logistics.shipment.result.get`** 查询下单结果、**`bg.logistics.shipment.document.get`** 拉取面单） |
| warningMessage | STRING[] | Warning messages（警告信息列表；非阻塞提示，购标仍可能成功） |
| shipLaterLimitTime | STRING | Ship-later limit time returned when applicable（若请求 **`shipLater=true`**，可能返回确认的稍后发货截止时间/小时配置） |

> 调用成功时先判断 **`response.success === true`**，再使用 **`result.packageSnList`** 走结果查询与面单下载。若 **`warningMessage`** 非空，建议记录并人工确认是否影响发货。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文摘要） | 处理建议 |
|--------|----------------------|----------|
| 120012013 | Already requested by Temu integrated logistics; check via result.get | 调用 **`bg.logistics.shipment.result.get`** 确认是否已成功 |
| 120015032 | Choose channelId **or** shipLogisticsType | 二选一履约，勿同时乱填 |
| 120011111 | Split channel requires **interlineShipCompanyList** | 补全联运分段渠道 |
| 120011110 | No eligible channelId | 核对渠道参数或重新 **shippingservices.get** |
| 120011112 | Missing **shipCompanyId** | 补全物流公司 ID |
| 120011113 | **orderSendInfoList** missing orderSn | 每项商品行须有 **orderSn** |
| 120013002 | Item quantity does not match | 核对 **quantity** 与订单待发数量 |
| 120012015 | Combined delivery: addresses differ | 合并发货时地址须一致 |
| 120015032 | channelId or shipLogisticsType | 见上 |
| 120011053 | COD: shipLater must be FALSE | COD 勿稍后发货 |
| 120011051 | COD: no sub-packages | COD 勿拆子包裹 |
| 120011057 / 120018028 | COD vs PPD cannot mix in one request | 勿混 COD 与预付订单 |
| 120012037 | Before earliestTimeBuyShippingLabel | 未到可购标时间 |
| 120015534 | Y2_advance_sale: shipLater=true required | 预售标签订单须稍后发货 |
| 120015532 | shipLaterLimitTime invalid | 按订单标签选合法小时数 |
| 120015533 | Y2_advance_sale cannot mix with normal orders | 勿混预售与普通订单 |
| 120011043 | Missing **sendSubRequestList** | splitSubPackage 场景补子包裹 |
| 120011044 | Max 10 attached packages | 子包裹 ≤ 10 |
| 120011045 | splitSubPackage: quantity must be 1 | 拆包场景数量为 1 |
| 120018084 | Cooperative warehouse: no split sub package | 合作仓不支持拆子包裹 |
| 120018086 | USPSMailingDateOffset cannot be 0 | 调整 USPS 偏移 |
| 120019009 / 120019019 | Invalid pickup time | 按 **pickupRules** 重选时段 |
| 120015507 | Wrong package information | 检查重量尺寸单位 |
| 120015521 | Weight should be integer (US) | 美国 **weight** 用整数磅 |
| 120011006 | warehouseId invalid | 用 **warehouse.list.get** 有效 ID |
| 120012007 / 120012016 | parentOrder/order invalid | 核对父子订单 |
| 120015528 | COD orders: Temu Label only | COD 仅 Temu 面单 |
| 120018063 | Funds reserved; Buy shipping disabled | 账户资金受限 |
| 120012061 / 120012031 | Risk control alert on parent order | 评估是否继续发货 |

> 完整错误码以 Partner 文档 **Error Code** 表为准（导出 HTML 含 70+ 条）。

---

## 典型用法

```text
1. bg.logistics.warehouse.list.get          → warehouseId
2. linkfox-temu-order-us                    → parentOrderSn、orderSn、quantity、earliestTimeBuyShippingLabel
3. bg.logistics.shippingservices.get        → channelId / shipCompanyId / signServiceId / pickup 时段
   （或 temu.logistics.shiplogisticstype.get → shipLogisticsType）
4. bg.logistics.shipment.create              → packageSnList（本接口）
5. [bg.logistics.shipment.result.get](./bg-logistics-shipment-result-get.md) → 确认异步下单结果
6. [bg.logistics.shipment.document.get](./bg-logistics-shipment-document-get.md) → 面单 URL
7. [bg.order.unshipped.package.get](./bg-order-unshipped-package-get.md) → 未发货包裹列表
7. bg.logistics.shipped.package.confirm      → 确认已发货（待接入）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_buy_shipping_logistics_shipment_create.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "sendType": 0,
    "shipLater": false,
    "sendRequestList": [
      {
        "warehouseId": "WH-001",
        "length": "12.00",
        "width": "8.00",
        "height": "4.00",
        "dimensionUnit": "in",
        "weight": "2",
        "weightUnit": "lb",
        "shipCompanyId": 314439762,
        "channelId": 19409681780736,
        "orderSendInfoList": [
          {
            "parentOrderSn": "PO-20260101001",
            "orderSn": "O-20260101001-1",
            "goodsId": 6017592186252451,
            "skuId": 281474976920151,
            "quantity": 1
          }
        ]
      }
    ]
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.logistics.shipment.create",
  "params": {
    "request": {
      "sendType": 0,
      "shipLater": false,
      "sendRequestList": [
        {
          "warehouseId": "WH-001",
          "length": "12.00",
          "width": "8.00",
          "height": "4.00",
          "dimensionUnit": "in",
          "weight": "2",
          "weightUnit": "lb",
          "shipCompanyId": 314439762,
          "channelId": 19409681780736,
          "orderSendInfoList": [
            {
              "parentOrderSn": "PO-20260101001",
              "orderSn": "O-20260101001-1",
              "quantity": 1
            }
          ]
        }
      ]
    }
  }
}'
```
