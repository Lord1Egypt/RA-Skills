# 查询购标/在线下单结果 — `bg.logistics.shipment.result.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_buy_shipping_logistics_shipment_result_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.shipment.result.get`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.logistics.shipment.result.get` interface is for sellers to query the result of placing online logistics orders, with the shipping label status including in-progress{0}, successful{1}, and failed{2}.

（卖家查询**在线物流下单/购标**结果；**`shippingLabelStatus`** 表示面单状态：**0**=进行中、**1**=成功、**2**=失败。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：** **`packageSnList`** 中的包裹号通常来自 **`bg.logistics.shipment.create`** 或订单/包裹相关接口返回的 **`packageSn`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── packageSnList[] (STRING[], 选填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSnList | STRING[] | 否 | Package number list（包裹号列表；传入一个或多个 **`packageSn`** 批量查询购标/在线下单结果） |

> 官方 Request 表将 **`request`** 与 **`packageSnList`** 均标为选填（False）；实际查询须传入有效 **`packageSn`**（错误码 **120018027**）。Partner **Request Example** CURL 将 **`packageSnList`** 写在顶层，经 LinkFox 网关时建议放在 **`params.request.packageSnList`**（与 Partner Request 表一致）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSnList": ["PKG-001", "PKG-002"]
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；网关解析后通常直接见到 `success` / `errorCode` / `errorMsg` / `result`。**`result`** 在导出 HTML 中为折叠状态，下列子层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    └── packageInfoResultList[] (OBJECT[])
        ├── packageSn
        ├── shippingLabelStatus
        ├── failReasonText
        ├── trackingNumber
        ├── channelId
        ├── shipLogisticsType
        ├── shipCompanyId
        ├── shippingCompanyName
        ├── warehouseId
        ├── warehouseName
        ├── mainPackageSn
        ├── subPackageSnList[]
        ├── subPackageType
        ├── cwFulfillNo
        ├── reservationSn
        ├── estimatedText
        ├── estimatedAmount
        ├── estimatedCurrencyCode
        ├── solutionText
        ├── packageDeliveryType
        ├── dimensionUnit
        ├── length
        ├── width
        ├── height
        ├── weight
        ├── weightUnit
        ├── extendWeight
        ├── extendWeightUnit
        ├── pickupStartTime
        ├── pickupEndTime
        ├── shipLabelPrintableTime
        ├── isConfirmAfterPickup
        ├── canChangeToManualSend
        ├── signServiceId
        ├── uspsMailingDateOffset
        ├── warningMessage[]
        ├── interlineShipCompanyList[] (OBJECT[])
        │   ├── shipLogisticsType
        │   ├── shipStageType
        │   ├── shippingCompanyName
        │   ├── channelId
        │   └── shipCompanyId
        ├── shippingInfoList[] (OBJECT[])
        │   ├── shipLogisticsType
        │   ├── shipStageType
        │   ├── shippingCompanyName
        │   ├── trackingNumber
        │   └── shipCompanyId
        └── orderSendInfoList[] (OBJECT[])
            ├── semiUniqueId
            ├── quantity
            ├── orderSn
            ├── parentOrderSn
            ├── goodsId
            ├── mallId
            └── skuId
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | result（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageInfoResultList | OBJECT[] | 按 **`packageSnList`** 查询得到的包裹购标/在线下单结果列表（与请求包裹号一一对应或按平台规则返回） |

#### `packageInfoResultList[]` 元素字段

> Partner **Response** 表中 **`result`** 子行在导出 HTML 中为折叠状态；下列字段与类型来自 **Response Example**，说明结合接口 Description 与 Buy-Shipping 流程整理。若 Partner 在线文档 **Expand** 后有更完整枚举，以在线表为准。

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | Package number（包裹号；与请求 **`packageSnList`** 元素对应） |
| shippingLabelStatus | INTEGER | Shipping label status（物流面单/购标状态）：**0**=in-progress（进行中），**1**=successful（成功），**2**=failed（失败） |
| failReasonText | STRING | Failure reason text（购标/下单失败原因文案；**`shippingLabelStatus=2`** 时关注） |
| trackingNumber | STRING | Tracking number（运单号/追踪号；成功后可用于物流跟踪） |
| channelId | INTEGER | Channel ID（物流渠道 ID；与 **`bg.logistics.shippingservices.get`** / **`bg.logistics.shipment.create`** 一致） |
| shipLogisticsType | STRING | Ship logistics type（发货物流类型编码） |
| shipCompanyId | INTEGER | Ship company ID（物流公司/承运商 ID） |
| shippingCompanyName | STRING | Shipping company name（物流公司/承运商名称） |
| warehouseId | STRING | Warehouse ID（发货仓库 ID） |
| warehouseName | STRING | Warehouse name（发货仓库名称） |
| mainPackageSn | STRING | Main package number（主包裹号；拆分子包裹场景下的主单号） |
| subPackageSnList | STRING[] | Sub package number list（子包裹号列表） |
| subPackageType | STRING | Sub package type（子包裹类型） |
| cwFulfillNo | STRING | Cooperative warehouse fulfill number（合作仓履约单号/履约编号） |
| reservationSn | STRING | Reservation SN（预约/预留单号，如取件预约相关） |
| estimatedText | STRING | Estimated delivery time text（预计送达/时效展示文案） |
| estimatedAmount | STRING | Estimated shipping amount（预估运费金额，字符串形式保留精度） |
| estimatedCurrencyCode | STRING | Currency code for **estimatedAmount**（预估运费币种代码） |
| solutionText | STRING | Solution / service description text（方案或服务说明文案） |
| packageDeliveryType | INTEGER | Package delivery type（包裹配送类型；具体枚举以 Partner 文档为准） |
| dimensionUnit | STRING | Dimension unit（长宽高单位，如 **`in`** / **`cm`**） |
| length | STRING | Package length（包裹长度，通常保留两位小数） |
| width | STRING | Package width（包裹宽度） |
| height | STRING | Package height（包裹高度） |
| weight | STRING | Package weight（包裹重量） |
| weightUnit | STRING | Weight unit（重量单位，如 **`lb`** / **`kg`**） |
| extendWeight | STRING | Extended weight portion（扩展重量，如美国本地订单盎司部分） |
| extendWeightUnit | STRING | Extended weight unit（扩展重量单位，如 **`oz`**） |
| pickupStartTime | INTEGER | Pickup window start time（取件窗口开始时间，Unix 秒级时间戳） |
| pickupEndTime | INTEGER | Pickup window end time（取件窗口结束时间，Unix 秒级时间戳） |
| shipLabelPrintableTime | INTEGER | Ship label printable time（面单可打印时间，Unix 秒级时间戳；**`shippingLabelStatus=1`** 后用于 **`bg.logistics.shipment.document.get`** 等） |
| isConfirmAfterPickup | BOOLEAN | Whether shipment is confirmed after pickup（是否在取件后确认发货） |
| canChangeToManualSend | BOOLEAN | Whether seller can switch to manual send（是否允许改为卖家自发货/手动发货） |
| signServiceId | INTEGER | Signature service ID（签名/签收服务 ID） |
| uspsMailingDateOffset | INTEGER | USPS mailing date offset（USPS 邮寄日期偏移量，USPS 渠道相关） |
| warningMessage | STRING[] | Warning messages（警告信息列表，非致命提示） |
| interlineShipCompanyList | OBJECT[] | Interline shipping company list（联运/分段物流承运商列表） |
| shippingInfoList | OBJECT[] | Shipping info list by stage（分段物流信息列表，含各段运单号） |
| orderSendInfoList | OBJECT[] | Orders included in this package（本包裹关联的订单发货信息列表） |

#### `interlineShipCompanyList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| shipLogisticsType | STRING | Ship logistics type（该段物流类型编码） |
| shipStageType | STRING | Ship stage type（运输阶段类型，如干线/末端等；枚举以 Partner 为准） |
| shippingCompanyName | STRING | Shipping company name（该段承运商名称） |
| channelId | INTEGER | Channel ID（该段渠道 ID） |
| shipCompanyId | INTEGER | Ship company ID（该段物流公司 ID） |

#### `shippingInfoList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| shipLogisticsType | STRING | Ship logistics type（该段物流类型编码） |
| shipStageType | STRING | Ship stage type（运输阶段类型） |
| shippingCompanyName | STRING | Shipping company name（该段承运商名称） |
| trackingNumber | STRING | Tracking number（该段运单号） |
| shipCompanyId | INTEGER | Ship company ID（该段物流公司 ID） |

#### `orderSendInfoList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| semiUniqueId | STRING | Semi-managed unique identifier（半托管业务侧唯一标识） |
| quantity | INTEGER | Quantity of the product（本行商品发货数量） |
| orderSn | STRING | Order number（子订单号） |
| parentOrderSn | STRING | Parent order number（父订单号） |
| goodsId | LONG | Goods ID（商品 ID） |
| mallId | LONG | Mall ID（店铺/商城 ID） |
| skuId | LONG | SKU ID（SKU ID） |

> 调用成功时先判断 **`success === true`**，再按 **`packageSn`** 在 **`result.packageInfoResultList`** 中查看 **`shippingLabelStatus`**：**1** 表示购标成功，可继续取面单；**0** 可轮询本接口；**2** 查看 **`failReasonText`**。

---

## Error Code（Partner 摘录）

| Error Code | Error Message |
|------------|---------------|
| 120018027 | The packageSn is invalid. Please check the request area or if the packageSn is nonexistent etc. |

---

## 典型用法

```text
1. bg.logistics.shippingservices.get     → 选渠道
2. [bg.logistics.shipment.create](./bg-logistics-shipment-create.md) → 购标，获得 packageSnList
3. bg.logistics.shipment.result.get      → 本接口：轮询购标结果 / shippingLabelStatus
4. bg.logistics.shipment.document.get    → 下载面单（待接入）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_buy_shipping_logistics_shipment_result_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSnList": ["PKG-001"]
  }
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.logistics.shipment.result.get",
  "params": {
    "request": {
      "packageSnList": ["PKG-001", "PKG-002"]
    }
  }
}'
```
