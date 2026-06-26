# 面单列表查询 — `temu.logistics.label.list.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_buy_shipping_logistics_label_list_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.label.list.get`，业务载荷放在 Body 的 `params` |

**Description:** You can use this API to retrieve shipping label information fulfilled via Temu's platform. Please note that this API is only available for labels generated through the Temu platform.（查询经 **Temu 平台购标** 生成的物流面单信息列表；**仅适用于**在 Temu 平台下单购标的面单，不支持站外自填运单。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **关联能力：** **`packageSnList`** 来自 [**`bg.logistics.shipment.create`**](./bg-logistics-shipment-create.md)；面单文件 URL 见 [**`bg.logistics.shipment.document.get`**](./bg-logistics-shipment-document-get.md)；购标结果状态见 [**`bg.logistics.shipment.result.get`**](./bg-logistics-shipment-result-get.md)。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageNumber              ← 必填
    ├── pageSize                ← 必填
    ├── packageSnList[]         ← 选填
    ├── temuLabelStatus         ← 选填
    ├── printStatus             ← 选填
    ├── createAtStart           ← 选填
    ├── createAtEnd             ← 选填
    ├── trackingNumberList[]    ← 选填
    ├── shippingCompanyIdList[] ← 选填
    └── parentOrderSnList[]     ← 选填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNumber | INTEGER | **是** | current page number of the result（当前页码，从 **1** 起） |
| pageSize | INTEGER | **是** | page size for pagination（每页条数） |
| packageSnList | STRING[] | 否 | package sn list（包裹号列表；按 **`packageSn`** 筛选） |
| temuLabelStatus | INTEGER | 否 | Temu label status（Temu 面单/购标状态），见下表 |
| printStatus | INTEGER | 否 | Print status（面单打印状态），见下表 |
| createAtStart | INTEGER | 否 | call begin time（购标/下 call 开始时间；一般为 **Unix 秒级时间戳**，用于时间窗筛选） |
| createAtEnd | INTEGER | 否 | call end time（购标/下 call 结束时间；Unix 秒级时间戳，须不早于 **`createAtStart`**） |
| trackingNumberList | STRING[] | 否 | tracking number list（运单号列表） |
| shippingCompanyIdList | STRING[] | 否 | shipping company id list（物流公司 ID 列表；与 **`shipCompanyId`** / 承运商 ID 对应，Partner 示例为字符串数组） |
| parentOrderSnList | STRING[] | 否 | parent order sn list（父订单号列表） |

#### `temuLabelStatus`

| 值 | 说明 |
|----|------|
| `0` | Pending（进行中 / 待完成） |
| `1` | Successful（成功） |
| `2` | Failed（失败） |
| `3` | Canceled（已取消） |

> 与 [**`bg.logistics.shipment.result.get`**](./bg-logistics-shipment-result-get.md) 中 **`shippingLabelStatus`** 语义一致（0/1/2 等）。

#### `printStatus`

| 值 | 说明 |
|----|------|
| `0` | Not printed（未打印） |
| `1` | Printed（已打印） |

> 官方 Request 表为 **`printStatus`**；Response 中对应字段名为 **`labelPrintStatus`**（见出参）。

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`pageNumber`**、**`pageSize`** 为必填。筛选字段可组合使用；Partner **Request Example** CURL 将字段写在顶层，经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 20,
    "packageSnList": ["PKG-001"],
    "temuLabelStatus": 1,
    "printStatus": 0
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 50,
    "parentOrderSnList": ["PO-20260101001"],
    "createAtStart": 1717200000,
    "createAtEnd": 1717286400,
    "trackingNumberList": ["1Z999AA10123456784"]
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；**`result`** 说明为 **Specific information**。  
**`result`** 子行在导出 HTML 中为折叠状态；下列层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)                    ← Specific information
    ├── totalItemNum (INTEGER)
    └── shippingLabelInfoList[] (OBJECT[])
        ├── packageSn
        ├── cwFulfillNo
        ├── shippingLabelStatus
        ├── labelPrintStatus
        ├── createTime
        ├── warehouseInfo (OBJECT)
        │   ├── warehouseId
        │   └── warehouseName
        ├── trackingInfoList[] (OBJECT[])
        │   ├── trackingNumber
        │   ├── shippingCompanyId
        │   └── shippingCompanyName
        ├── orderInfoList[] (OBJECT[])
        │   ├── orderSn
        │   ├── parentOrderSn
        │   └── quantity
        └── packageDimensionInfo (OBJECT)
            ├── weight / weightUnit
            ├── extendWeight / extendWeightUnit
            ├── length / width / height
            └── dimensionUnit
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | Specific information（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| totalItemNum | INTEGER | Total item count（符合筛选条件的面单记录总条数，用于分页） |
| shippingLabelInfoList | OBJECT[] | Shipping label information list（面单信息列表） |

#### `shippingLabelInfoList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | Package SN（包裹号） |
| cwFulfillNo | STRING | Cooperative warehouse fulfillment number（合作仓履约单号；合作仓场景可能有值） |
| shippingLabelStatus | INTEGER | Shipping label status（面单/购标状态），见下表 |
| labelPrintStatus | INTEGER | Label print status（面单打印状态），见下表 |
| createTime | INTEGER | Create time（面单/购标创建时间；Partner 示例为数值时间戳，一般为 **Unix 秒**） |
| warehouseInfo | OBJECT | Warehouse information（发货仓库信息） |
| trackingInfoList | OBJECT[] | Tracking information list（运单/承运商信息列表；一单可能多段） |
| orderInfoList | OBJECT[] | Order information list（关联订单商品行） |
| packageDimensionInfo | OBJECT | Package dimension and weight（包裹尺寸与重量） |

##### `shippingLabelStatus`（出参）

| 值 | 说明 |
|----|------|
| `0` | Pending（进行中） |
| `1` | Successful（成功） |
| `2` | Failed（失败） |
| `3` | Canceled（已取消） |

> 与入参 **`temuLabelStatus`** 筛选枚举一致。

##### `labelPrintStatus`（出参）

| 值 | 说明 |
|----|------|
| `0` | Not printed（未打印） |
| `1` | Printed（已打印） |

> 与入参 **`printStatus`** 筛选枚举一致。

##### `warehouseInfo` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| warehouseId | STRING | Warehouse ID（仓库 ID） |
| warehouseName | STRING | Warehouse name（仓库名称） |

##### `trackingInfoList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| trackingNumber | STRING | Tracking number（运单号 / 跟踪号） |
| shippingCompanyId | INTEGER / LONG | Shipping company ID（物流公司 ID） |
| shippingCompanyName | STRING | Shipping company name（物流公司名称） |

##### `orderInfoList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| orderSn | STRING | Order number（子订单号 / 订单号） |
| parentOrderSn | STRING | Parent order number（父订单号） |
| quantity | INTEGER | Quantity（该行商品数量） |

##### `packageDimensionInfo` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| weight | STRING | Package weight（包裹重量） |
| weightUnit | STRING | Weight unit（重量单位，美国常为 **`lb`**） |
| extendWeight | STRING | Extended weight（扩展重量，美国本地盎司部分等） |
| extendWeightUnit | STRING | Extended weight unit（扩展重量单位，如 **`oz`**） |
| length | STRING | Package length（长度） |
| width | STRING | Package width（宽度） |
| height | STRING | Package height（高度） |
| dimensionUnit | STRING | Dimension unit（尺寸单位，美国常为 **`in`**） |

> 调用成功时先判断 **`success === true`**，按 **`totalItemNum`** 与 **`pageNumber` / `pageSize`** 翻页；对 **`shippingLabelStatus=1`** 的记录可调用 **`bg.logistics.shipment.document.get`** 获取面单 URL。

---

## 典型用法

```text
1. bg.logistics.shipment.create              → 购标，获得 packageSn
2. bg.logistics.shipment.result.get          → 确认 shippingLabelStatus=1
3. temu.logistics.label.list.get（本接口）   → 按包裹/订单/时间窗批量查面单摘要
4. bg.logistics.shipment.document.get        → 拉取面单 PDF/图片 URL
5. temu_eu_file_download                     → 下载面单文件
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_buy_shipping_logistics_label_list_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 20,
    "packageSnList": ["PKG-001"],
    "temuLabelStatus": 1,
    "printStatus": 0
  }
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.logistics.label.list.get",
  "params": {
    "request": {
      "pageNumber": 1,
      "pageSize": 20,
      "parentOrderSnList": ["PO-20260101001"],
      "shippingCompanyIdList": ["314439762"]
    }
  }
}'
```
