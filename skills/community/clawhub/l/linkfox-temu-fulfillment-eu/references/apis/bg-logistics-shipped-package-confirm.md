# 确认包裹已发货 — `bg.logistics.shipped.package.confirm`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_buy_shipping_logistics_shipped_package_confirm.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.shipped.package.confirm`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.logistics.shipped.package.confirm` interface is for sellers to support batch conversion of packages that have been fulfilled successfully by Temu-integrated channel but not shipped to shipped, and will be automatically converted to shipped if not converted within 48 hours.

（卖家将已通过 **Temu 集成物流** 成功履约、但状态仍为**未发货确认**的包裹，批量确认为**已发货**；若 **48 小时内**未手动确认，系统将自动转为已发货。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：**  
> - **`packageSn`**、**`trackingNumber`** 通常来自 [**`bg.logistics.shipment.create`**](./bg-logistics-shipment-create.md) / [**`bg.logistics.shipment.result.get`**](./bg-logistics-shipment-result-get.md) 或 [**`bg.order.unshipped.package.get`**](./bg-order-unshipped-package-get.md)。  
> - 打印面单后出库前调用；**`trackingNumber`** 须与 **`packageSn`** 匹配（错误码 **120014002**）。  
> - 合作仓包裹可能禁止手动确认发货（**120018087**）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── packageSendInfoList[] (OBJECT[], 必填)
        ├── packageSn
        ├── trackingNumber
        └── packageDetail[] (OBJECT[])
            ├── orderSn
            ├── parentOrderSn
            └── quantity
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSendInfoList | OBJECT[] | **是** | This field is used to confirm the list of packages that have been transitioned to the shipped status（待确认为**已发货**状态的包裹列表；支持批量） |

#### `packageSendInfoList[]` 元素字段

> Partner Request 表中 `packageSendInfoList` 子行在导出 HTML 中为折叠状态；下列字段来自 **Request Example** 与错误码说明。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSn | STRING | **是** | Package SN（包裹号；购标/履约成功后由平台分配，见 **`bg.logistics.shipment.create`** 等返回） |
| trackingNumber | STRING | **是** | Tracking Number（物流运单号；须与 **`packageSn`** 对应，错误码 **120014002**） |
| packageDetail | OBJECT[] | **是** | Package detail / order lines in this package（本包裹内要确认发货的商品行明细；数量须与包裹内实际一致，错误码 **120013002**） |

##### `packageSendInfoList[].packageDetail[]` 元素字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent Order Number（父订单号） |
| orderSn | STRING | **是** | Order Number（子订单号 / 订单号） |
| quantity | INTEGER | **是** | Quantity（本行商品数量；须与包裹内该订单行数量一致，错误码 **120013002**） |

> **不支持子包裹单独确认**（错误码 **120011046** Sub package not allowed）。已发货订单重复提交无效（**120012004**）。无匹配可发订单时返回 **120012012**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSendInfoList": [
      {
        "packageSn": "PKG-001",
        "trackingNumber": "1Z999AA10123456784",
        "packageDetail": [
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
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSendInfoList": [
      {
        "packageSn": "PKG-001",
        "trackingNumber": "1Z999AA10123456784",
        "packageDetail": [
          {
            "parentOrderSn": "PO-20260101001",
            "orderSn": "O-20260101001-1",
            "quantity": 2
          },
          {
            "parentOrderSn": "PO-20260101001",
            "orderSn": "O-20260101001-2",
            "quantity": 1
          }
        ]
      },
      {
        "packageSn": "PKG-002",
        "trackingNumber": "9400111899223857123456",
        "packageDetail": [
          {
            "parentOrderSn": "PO-20260101002",
            "orderSn": "O-20260101002-1",
            "quantity": 1
          }
        ]
      }
    ]
  }
}
```

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`packageSendInfoList`** 为必填。Partner **Request Example** CURL 将 **`packageSendInfoList`** 写在顶层；经 LinkFox 网关时建议放在 **`params.request.packageSendInfoList`**。

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；网关解析后通常直接见到 `success` / `errorCode` / `errorMsg` / `result`。**`result`** 在导出 HTML 中为折叠状态，下列子层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    └── warningMessage[] (OBJECT[])
        ├── packageSn
        └── warningMessage
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | result（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| warningMessage | OBJECT[] | Per-package warning messages（按包裹返回的警告信息；部分包裹确认成功、部分有提示时非空） |

#### `warningMessage[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | Package SN（关联的包裹号） |
| warningMessage | STRING | Warning message text（该包裹的警告说明；具体文案以 Temu 返回为准） |

> 调用成功时先判断 **`response.success === true`**。若 **`result.warningMessage`** 非空，须逐条检查哪些 **`packageSn`** 未完全确认成功。无警告通常表示请求列表中的包裹均已处理完成（仍建议用 **`bg.order.unshipped.package.get`** 或订单接口复核状态）。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 120018027 | The packageSn is invalid... | 核对 **`packageSn`** 与站点 |
| 120014002 | The field trackingNumber {*} does not match packageSn {*}. | **`trackingNumber`** 与 **`packageSn`** 必须匹配 |
| 120012004 | The order has been shipped. This submission is not effective for the shipped order. | 订单已发货，无需重复确认 |
| 120012012 | There are no shippable orders matching the item. | 包裹内无可发订单行 |
| 120013002 | Item quantity does not match. | **`packageDetail[].quantity`** 与包裹实际数量不一致 |
| 120011046 | Sub package not allowed. | 不支持对子包裹单独确认 |
| 120018087 | The current package {*} is shipped from a cooperative warehouse and manual confirmation of shipment is prohibited | 合作仓包裹禁止手动确认发货 |
| 120011030 | Cooperative warehouse order fulfillment restricted. | 合作仓履约受限 |
| 120018010 / 120018015 | The package(s) {*} have been canceled... | 包裹/订单已取消，需重新履约 |
| 120012007 / 120012016 | The parentOrder or Order is invalid... | 父子订单号无效或不匹配 |
| 120018025 | Orders exist after-sales applications... | 先处理售后申请 |
| 120011072 | The request area is incorrect... US / global | 欧洲站请求区域须为 US |

<details>
<summary>完整错误码列表（16 条，Partner 原文）</summary>

| 错误码 | 错误信息 |
|--------|----------|
| 120018087 | The current package {*} is shipped from a cooperative warehouse and manual confirmation of shipment is prohibited |
| 120018010 | The packages {*} have been canceled. Please fulfill again by Temu non-integrated logistics or Temu integrated logistics. |
| 120014002 | The field trackingNumber {*} does not match packageSn {*}. Please check the matching relationship between the two fields. |
| 120011030 | Cooperative warehouse order fulfillment restricted. |
| 120018015 | The package has been canceled, please fulfill again by Temu non-integrated logistics or Temu integrated logistics. |
| 120012012 | There are no shippable orders matching the item. |
| 120012004 | The order has been shipped. This submission is not effective for the shipped order. |
| 120013002 | Item quantity does not match. |
| 120011046 | Sub package not allowed. |
| 120015026 | A large items template has been used for the items in this package. Only specified logistics providers can be used for shipping. |
| 120015027 | A large items template has been used for the items in this package. Only special channels can be used for shipping. |
| 120018025 | Orders exist after-sales applications, please complete the processing before operation |
| 120011072 | The request area is incorrect. Please check the request area and replace it with the correct request area. The request area for the United States is US, and the request area for other non-European countries is global. |
| 120012007 | The parentOrder or Order is invalid. Please check if the parentOrder matches the Order, the parentOrder or Order is nonexistent etc. |
| 120012016 | The parentOrder or Order is invalid. Please check if the parentOrder matches the Order, the parentOrder or Order is nonexistent etc. |
| 120018027 | The packageSn is invalid. Please check the request area or if the packageSn is nonexistent etc. |

</details>

---

## 典型用法

```text
1. bg.logistics.shipment.create / result.get     → 购标成功，取得 packageSn、trackingNumber
2. bg.logistics.shipment.document.get           → 打印面单
3. bg.order.unshipped.package.get（可选）        → 列出待确认发货的包裹
4. bg.logistics.shipped.package.confirm         → 批量确认已发货（本接口）
5. linkfox-temu-order-eu                        → 刷新订单状态
```

> 若 **48 小时内**未调用本接口，平台可能自动将符合条件的包裹转为已发货；仍建议在出库后主动确认，便于与 **`packageDetail`** 数量、运单一致。

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_buy_shipping_logistics_shipped_package_confirm.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSendInfoList": [
      {
        "packageSn": "PKG-001",
        "trackingNumber": "1Z999AA10123456784",
        "packageDetail": [
          {
            "parentOrderSn": "PO-20260101001",
            "orderSn": "O-20260101001-1",
            "quantity": 1
          }
        ]
      }
    ]
  }
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.logistics.shipped.package.confirm",
  "params": {
    "request": {
      "packageSendInfoList": [
        {
          "packageSn": "PKG-001",
          "trackingNumber": "1Z999AA10123456784",
          "packageDetail": [
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
