# 查询未发货包裹 — `bg.order.unshipped.package.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_buy_shipping_order_unshipped_package_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.order.unshipped.package.get`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.order.unshipped.package.get` interface is for sellers to query information about packages that have been fulfilled successfully by Temu-integrated channel.（卖家查询经 **Temu 集成物流** 已成功履约、但尚未完成发货确认的**未发货包裹**信息，含运单、承运商及包裹内可发/已取消订单行。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **关联能力：** 购标后包裹号来自 [**`bg.logistics.shipment.create`**](./bg-logistics-shipment-create.md)；订单号来自 **`linkfox-temu-order-global`**；确认发货见 [**`bg.logistics.shipped.package.confirm`**](./bg-logistics-shipped-package-confirm.md)。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageNumber          ← 必填
    ├── pageSize            ← 必填
    ├── parentOrderSnList[] ← 选填
    └── orderSnList[]       ← 选填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNumber | INTEGER | **是** | Page number（页码，从 **1** 起） |
| pageSize | INTEGER | **是** | Page size（每页条数） |
| parentOrderSnList | STRING[] | 否 | Parent order number list（父订单号列表；按父订单筛选未发货包裹） |
| orderSnList | STRING[] | 否 | Order number list（子订单号 / 订单号列表；按子订单筛选未发货包裹） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`pageNumber`**、**`pageSize`** 为必填。筛选时至少可传 **`parentOrderSnList`** 和/或 **`orderSnList`** 缩小范围；均不传时按分页返回店铺下符合条件的未发货包裹（以 Partner 与账号权限为准）。  
> Partner **Request Example** CURL 将字段写在顶层；经 LinkFox 网关时建议放在 **`params.request`**（与 Request 表一致）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 20,
    "parentOrderSnList": ["PO-20260101001"],
    "orderSnList": ["O-20260101001-1"]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 50
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；网关解析后通常直接见到 `success` / `errorCode` / `errorMsg` / `result`。  
**`result`** 子行在导出 HTML 中为折叠状态；下列层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    ├── totalItemNum (INTEGER)
    └── unshippedPackage[] (OBJECT[])
        ├── packageSn
        ├── mainPackageSn
        ├── subPackageSnList[] (STRING[])
        ├── subPackageType
        ├── trackingNumber
        ├── carrierId
        ├── carrierName
        └── packageDetail (OBJECT)
            ├── shippableOrders[] (OBJECT[])
            │   ├── semiUniqueId
            │   ├── quantity
            │   ├── orderSn
            │   ├── parentOrderSn
            │   └── mallId
            └── canceledOrders[] (OBJECT[])
                ├── semiUniqueId
                ├── quantity
                ├── orderSn
                ├── parentOrderSn
                └── mallId
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
| totalItemNum | INTEGER | Total item count（符合查询条件的未发货包裹总条数，用于分页） |
| unshippedPackage | OBJECT[] | Unshipped package list（未发货包裹列表；经 Temu 集成物流已成功履约的包裹） |

#### `unshippedPackage[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | Package SN（包裹号；与 **`bg.logistics.shipment.create`** 返回的 **`packageSnList`**、**`bg.logistics.shipment.result.get`** 等一致） |
| mainPackageSn | STRING | Main package SN（主包裹号；拆分子包裹时标识主包裹） |
| subPackageSnList | STRING[] | Sub-package SN list（子包裹号列表；一单多包裹/拆包场景） |
| subPackageType | STRING | Sub-package type（子包裹类型标识；具体枚举以 Partner 在线文档为准） |
| trackingNumber | STRING | Tracking number（物流运单号 / 跟踪号） |
| carrierId | INTEGER / LONG | Carrier ID（承运商 ID） |
| carrierName | STRING | Carrier name（承运商名称，展示用） |
| packageDetail | OBJECT | Package detail（包裹内订单行明细：可发货与已取消） |

##### `packageDetail` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| shippableOrders | OBJECT[] | Shippable orders in this package（本包裹内**仍可发货**的订单商品行） |
| canceledOrders | OBJECT[] | Canceled orders in this package（本包裹内**已取消**、不可再发的订单商品行） |

###### `shippableOrders[]` / `canceledOrders[]` 元素字段

> 两类数组元素结构相同；**`canceledOrders`** 为购标后订单被取消等场景，**`shippableOrders`** 为仍可继续发货确认的行。

| 参数 | 类型 | 说明 |
|------|------|------|
| semiUniqueId | STRING | Semi-unique ID（半托管订单行唯一标识；与 **`bg.logistics.shipment.result.get`** 的 **`orderSendInfoList[].semiUniqueId`** 等同系列字段） |
| quantity | INTEGER | Quantity（该行商品数量） |
| orderSn | STRING | Order number（子订单号 / 订单号） |
| parentOrderSn | STRING | Parent order number（父订单号） |
| mallId | INTEGER / LONG | Mall ID（店铺/商城 ID） |

> 调用成功时先判断 **`success === true`**，再根据 **`result.totalItemNum`** 与 **`pageNumber` / `pageSize`** 翻页；对每个 **`unshippedPackage`** 查看 **`trackingNumber`**、**`packageSn`** 及 **`packageDetail.shippableOrders`**，再调用 **`bg.logistics.shipped.package.confirm`** 等完成发货确认（待接入）。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 120011030 | Cooperative warehouse order fulfillment restricted. | 合作仓履约受限 |
| 120011072 | The request area is incorrect... US / global | 全球站请求区域须为 US |
| 120012016 | The parentOrder or Order is invalid... | 核对 **`parentOrderSnList`** / **`orderSnList`** 与订单是否存在、父子关系是否匹配 |

---

## 典型用法

```text
1. linkfox-temu-order-global                         → 待发货父/子订单号
2. bg.logistics.shipment.create                  → 购标，获得 packageSn
3. bg.logistics.shipment.result.get              → 确认面单状态成功
4. bg.order.unshipped.package.get（本接口）       → 列出已购标、待发货确认的包裹
5. bg.logistics.shipped.package.confirm          → 确认发货（待接入）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/global_buy_shipping_order_unshipped_package_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 20,
    "parentOrderSnList": ["PO-20260101001"]
  }
}'
```

```bash
python scripts/temu_global_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.order.unshipped.package.get",
  "params": {
    "request": {
      "pageNumber": 1,
      "pageSize": 20,
      "orderSnList": ["O-20260101001-1", "O-20260101001-2"]
    }
  }
}'
```