# 候选 Scan Form 包裹列表 — `temu.logistics.candidate.scanform.list.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_buy_shipping_logistics_candidate_scanform_list_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.candidate.scanform.list.get`，业务载荷放在 Body 的 `params` |

**Description:** The `temu.logistics.candidate.scanform.list.get` interface is for sellers to get lists of package numbers that can be used to generate a scanform based on shipCompanyId and warehouseId.

（卖家按 **`shipCompanyId`** 与 **`warehouseId`**，分页查询**可合并生成同一 Scan Form** 的候选包裹号分组列表；创建 Scan Form 前建议先调用本接口，避免 [**`temu.logistics.scanform.create`**](./temu-logistics-scanform-create.md) 因仓库/承运商不一致而失败。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：**  
> - **`shipCompanyId`**、**`warehouseId`** 通常来自 [**`bg.logistics.warehouse.list.get`**](./bg-logistics-warehouse-list-get.md) 与购标渠道（[**`bg.logistics.shipment.create`**](./bg-logistics-shipment-create.md) / [**`bg.logistics.shippingservices.get`**](./bg-logistics-shippingservices-get.md)）。  
> - 候选包裹须为已成功购标、满足 Scan Form 规则（如 **USPS**、美国目的地等，见 create 接口错误码）。  
> **后续：** 从返回的 **`checkBatchAddScanFormList[].packageSnList`** 选取一组，调用 [**`temu.logistics.scanform.create`**](./temu-logistics-scanform-create.md)；文档获取见 [**`temu.logistics.scanform.document.get`**](./temu-logistics-scanform-document-get.md)。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── shipCompanyId (LONG, 必填)
    ├── warehouseId (STRING, 必填)
    ├── pageNumber (INTEGER, 必填)
    └── pageSize (INTEGER, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| shipCompanyId | LONG | **是** | Ship Company ID（物流公司 ID；与待创建 Scan Form 的承运商一致） |
| warehouseId | STRING | **是** | Warehouse ID（发货仓库 ID；与待创建 Scan Form 的仓库一致） |
| pageNumber | INTEGER | **是** | Page number for pagination（当前页码，从 **1** 起） |
| pageSize | INTEGER | **是** | Page size for pagination, max is 500.（每页条数；**最大 500**） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但上述四个字段均为必填。Partner **Request Example** CURL 将业务字段写在顶层；经 LinkFox 网关时建议放在 **`params.request`** 下。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "shipCompanyId": 123456789,
    "warehouseId": "WH-US-001",
    "pageNumber": 1,
    "pageSize": 100
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "shipCompanyId": 123456789,
    "warehouseId": "WH-US-001",
    "pageNumber": 2,
    "pageSize": 500
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；网关解析后通常直接见到 `success` / `errorCode` / `errorMsg` / `result`。**`result`** 在导出 HTML 中为折叠状态，下列子层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    └── checkBatchAddScanFormList[] (OBJECT[])
        ├── packageSnList[] (STRING[])
        └── labelCount (INTEGER)
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Whether it was successful or not（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | Error code（错误码） |
| errorMsg | STRING | Error message（错误信息） |
| result | OBJECT | Specific information（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| checkBatchAddScanFormList | OBJECT[] | Batches of package numbers that can be used together to generate a scan form（可按批合并创建同一 Scan Form 的候选分组列表；每条为一组可一同提交的 **`packageSnList`**） |

#### `checkBatchAddScanFormList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSnList | STRING[] | Package number list（本批次内可生成同一 Scan Form 的包裹号列表；传给 [**`temu.logistics.scanform.create`**](./temu-logistics-scanform-create.md) 的 **`packageSnList`** 时应整组使用，勿混用不同批次或不同仓库/承运商的包裹） |
| labelCount | INTEGER | Label count（本批次关联的面单/标签数量；Partner Response Example 为整数，具体计数规则以平台为准，可用于核对批次规模） |

> 调用成功时先判断 **`response.success === true`**，再遍历 **`result.checkBatchAddScanFormList`**。若当前页无数据，可增大 **`pageNumber`** 翻页（**`pageSize`** ≤ 500）。Partner 导出 HTML 的 Response 表未单独列出分页总数字段；若后续版本增加 `total` 等字段，以 Partner 文档为准。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 120016059 | The destination region must be U.S.. | 仅美国目的地包裹可参与 Scan Form |
| 120016051 | The destination region must be consistent. | 目的地须一致 |
| 120011001 | System abnormality, please check the data and try again | 稍后重试 |
| 120011002 | Invalid request parameters. | 检查 **`shipCompanyId`**、**`warehouseId`**、分页参数 |

<details>
<summary>完整错误码列表（4 条，Partner 原文）</summary>

| 错误码 | 错误信息 |
|--------|----------|
| 120016059 | The destination region must be U.S.. |
| 120016051 | The destination region must be consistent. |
| 120011001 | System abnormality, please check the data and try again |
| 120011002 | Invalid request parameters. |

</details>

---

## 典型用法

```text
1. bg.logistics.warehouse.list.get              → warehouseId
2. bg.logistics.shipment.create / result.get    → 购标成功，已知 shipCompanyId
3. temu.logistics.candidate.scanform.list.get   → 本接口，取得可合并的 packageSnList 分组
4. temu.logistics.scanform.create               → 按某一组的 packageSnList 创建 Scan Form
5. temu.logistics.scanform.document.get         → 获取 Scan Form 文档（如需要）
6. bg.logistics.shipment.document.get           → 打印购标面单
```

> [**`temu.logistics.scanform.create`**](./temu-logistics-scanform-create.md) 错误码 **120016060** / **120016061** / **120016062** 均提示应重新调用本接口获取可生成同一 Scan Form 的包裹列表。

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_buy_shipping_logistics_candidate_scanform_list_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "shipCompanyId": 123456789,
    "warehouseId": "WH-US-001",
    "pageNumber": 1,
    "pageSize": 100
  }
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.logistics.candidate.scanform.list.get",
  "params": {
    "request": {
      "shipCompanyId": 123456789,
      "warehouseId": "WH-US-001",
      "pageNumber": 1,
      "pageSize": 100
    }
  }
}'
```
