# 查询 Scan Form 详情 — `temu.logistics.scanform.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_buy_shipping_logistics_scanform_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.scanform.get`，业务载荷放在 Body 的 `params` |

**Description:** The `temu.logistics.scanform.get` interface is for sellers to get detail information of scanforms such as status of the scanform.（卖家按分页与筛选条件查询 Scan Form（物流扫描单）的详情信息，例如创建状态等。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **关联能力：** 创建 Scan Form 见 [**`temu.logistics.scanform.create`**](./temu-logistics-scanform-create.md)；获取 Scan Form 文档见 **`temu.logistics.scanform.document.get`**（若已接入）。购标与包裹号见 [**`bg.logistics.shipment.create`**](./bg-logistics-shipment-create.md)。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageNumber                  ← 必填
    ├── pageSize                    ← 必填（最大 10）
    ├── scanFormSnList[]            ← 选填
    ├── shipCompanyIdList[]         ← 选填
    ├── warehouseIdList[]           ← 选填
    ├── scanFormCreateStatus        ← 选填
    ├── scanFormCreateTimeStart     ← 选填
    ├── scanFormCreateTimeEnd       ← 选填
    └── trackingNumberList[]        ← 选填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNumber | INTEGER | **是** | Page number for pagination（分页页码） |
| pageSize | INTEGER | **是** | Page size for pagination, max is 10.（每页条数；**最大为 10**，超出将报错 **120016057**） |
| scanFormSnList | STRING[] | 否 | Scan form serial number list, the lists of the unique identification field when creating a scan form.（Scan Form 序列号列表；为创建 Scan Form 时返回的唯一标识字段列表，用于按单号筛选） |
| shipCompanyIdList | LONG[] | 否 | Ship company id list（物流公司 ID 列表；与购标/Scan Form 创建时的 **`shipCompanyId`** 对应） |
| warehouseIdList | STRING[] | 否 | Warehouse id list（仓库 ID 列表；来自 **`bg.logistics.warehouse.list.get`** 的 **`warehouseId`**） |
| scanFormCreateStatus | INTEGER | 否 | The status of scan form（Scan Form 创建/处理状态），见下表 |
| scanFormCreateTimeStart | INTEGER | 否 | Start time for querying scan form creating time with second-level timestamp.（查询 Scan Form **创建时间**的起始时间；**秒级 Unix 时间戳**） |
| scanFormCreateTimeEnd | INTEGER | 否 | End time for querying scan form creating time with second-level timestamp.（查询 Scan Form **创建时间**的结束时间；**秒级 Unix 时间戳**，应不早于 **`scanFormCreateTimeStart`**） |
| trackingNumberList | STRING[] | 否 | Tracking number list（运单号/跟踪号列表；按包裹运单号反查关联 Scan Form） |

#### `scanFormCreateStatus`

| 值 | 说明 |
|----|------|
| `1` | under creation（创建中） |
| `2` | successful（成功） |
| `3` | failed（失败） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`pageNumber`**、**`pageSize`** 为必填。筛选字段可组合使用。Partner **Request Example** CURL 将业务字段写在 JSON 顶层，经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 10,
    "scanFormSnList": ["SCANFORM-SN-001"],
    "scanFormCreateStatus": 2,
    "warehouseIdList": ["WH-001"],
    "shipCompanyIdList": [314439762],
    "scanFormCreateTimeStart": 1717200000,
    "scanFormCreateTimeEnd": 1717286400,
    "trackingNumberList": ["1Z999AA10123456784"]
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；**`result`** 在表内标注为 **Specific information**。  
**`result`** 子行在导出 HTML 中为折叠状态；下列层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)                    ← Specific information
    ├── total (INTEGER)
    └── scanFormInfoList[] (OBJECT[])
        ├── scanFormSn
        ├── scanFormNumber
        ├── scanFormCreateStatus
        ├── scanFormCreateTime
        ├── warehouseId
        ├── shipCompanyId
        ├── shippingCompanyName
        ├── labelCount
        ├── failReason
        └── scanFormPackageList[] (OBJECT[])
            ├── packageSn
            └── trackingNumber
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Whether it was successful or not（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | Error code（错误码） |
| errorMsg | STRING | Error message（错误信息） |
| result | OBJECT | Specific information（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| total | INTEGER | Total count（符合当前筛选条件的 Scan Form 记录总条数，用于配合 **`pageNumber`** / **`pageSize`** 分页） |
| scanFormInfoList | OBJECT[] | Scan form information list（Scan Form 详情列表） |

#### `scanFormInfoList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| scanFormSn | STRING | Scan form serial number, the unique identification field when creating a scan form（Scan Form 序列号；创建时的唯一标识，用于 [**`temu.logistics.scanform.document.get`**](./temu-logistics-scanform-document-get.md) 的 **`scanFormSn`**） |
| scanFormNumber | STRING | Scan form number（Scan Form 业务编号/承运商侧编号，Partner 示例为字符串） |
| scanFormCreateStatus | INTEGER | The status of scan form（Scan Form 状态），见下表（与入参 **`scanFormCreateStatus`** 枚举一致） |
| scanFormCreateTime | STRING | Scan form creating time（Scan Form 创建时间；Partner **Response Example** 为字符串，一般为时间戳字符串） |
| warehouseId | STRING | Warehouse id（发货仓库 ID） |
| shipCompanyId | INTEGER / LONG | Ship company id（物流公司 ID） |
| shippingCompanyName | STRING | Shipping company name（物流公司名称） |
| labelCount | INTEGER | Label count（该 Scan Form 关联的面单/标签数量） |
| failReason | STRING | Fail reason（失败原因；当 **`scanFormCreateStatus=3`** 时有值，可配合本接口排查 [**`temu.logistics.scanform.document.get`**](./temu-logistics-scanform-document-get.md) 报错 **120016058**） |
| scanFormPackageList | OBJECT[] | Package list included in this scan form（本 Scan Form 包含的包裹列表） |

##### `scanFormCreateStatus`（出参）

| 值 | 说明 |
|----|------|
| `1` | under creation（创建中） |
| `2` | successful（成功） |
| `3` | failed（失败） |

##### `scanFormPackageList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | Package SN（包裹号；来自购标 [**`bg.logistics.shipment.create`**](./bg-logistics-shipment-create.md)） |
| trackingNumber | STRING | Tracking number（运单号/跟踪号） |

> 调用成功时先判断 **`success === true`**，再读取 **`result.total`** 与 **`scanFormInfoList`**。分页查询须配合 **`pageNumber`** / **`pageSize`**（**`pageSize` ≤ 10**）。状态为 **`2`** 时可调用 **`temu.logistics.scanform.document.get`** 获取文档 URL。

---

## Error Code（Partner 表）

| errorCode | errorMsg | 处理建议 |
|-----------|----------|----------|
| 120016057 | The pageSize exceeds the maximum limit of 10. | 将 **`pageSize`** 调整为 **≤ 10** |
| 120011001 | System abnormality, please check the data and try again | 检查入参后重试；持续失败联系平台 |
| 120011002 | Invalid request parameters. | 核对 **`request`** 字段类型、必填项与时间窗 |

---

## 典型用法

```text
1. temu.logistics.scanform.create              → 创建 Scan Form，获得 scanFormSn
2. temu.logistics.scanform.get（本接口）       → 按单号/状态/时间窗/运单号查询 Scan Form 详情与状态
3. temu.logistics.scanform.document.get        → 获取 Scan Form 文档 URL（若已接入）
4. temu_eu_file_download                       → 下载 Scan Form PDF（若返回加签 URL）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_buy_shipping_logistics_scanform_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 10,
    "scanFormSnList": ["SCANFORM-SN-001"],
    "scanFormCreateStatus": 2
  }
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.logistics.scanform.get",
  "params": {
    "request": {
      "pageNumber": 1,
      "pageSize": 10,
      "trackingNumberList": ["1Z999AA10123456784"],
      "scanFormCreateTimeStart": 1717200000,
      "scanFormCreateTimeEnd": 1717286400
    }
  }
}'
```
