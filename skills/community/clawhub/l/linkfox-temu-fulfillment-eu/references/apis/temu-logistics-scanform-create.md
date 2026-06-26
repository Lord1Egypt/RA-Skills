# 创建 Scan Form — `temu.logistics.scanform.create`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_buy_shipping_logistics_scanform_create.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.scanform.create`，业务载荷放在 Body 的 `params` |

**Description:** The `temu.logistics.scanform.create` interface is for sellers to create scanforms according to the check conditions after entering lists packages.

（卖家在录入**包裹号列表**后，按平台校验规则**创建 Scan Form（物流扫描单）**；常用于 **USPS** 等承运商的 **manifestation**，以便正常打印面单或交运。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：**  
> - **`packageSnList`** 中的包裹须已成功 **Buy-Shipping 购标**（错误码 **120016055**）。  
> - 仅支持 **USPS** 物流（**120016053**）；目的地区须为 **美国** 且一致（**120016059** / **120016051**）。  
> - **`warehouseId`**、**`shipCompanyId`** 须与所选包裹一致；若不一致，应重新调用 [**`temu.logistics.candidate.scanform.list.get`**](./temu-logistics-candidate-scanform-list-get.md) 获取可生成同一 Scan Form 的包裹列表（**120016060** / **120016061** / **120016062**）。  
> - 合作仓履约包裹**无需**生成 Scan Form（**120016063**）。  
> - 单次最多 **500** 个包裹（**120011067**）；生成同一 scanform 至少须包含平台要求的最少包裹数（**120011099**）。  
> - 邮寄日期须在**当日**至**当日+7 天（不含第 7 天）**之间（**120016054**）。  
> 购标与面单流程见 [**`bg.logistics.shipment.create`**](./bg-logistics-shipment-create.md)、[**`bg.logistics.shipment.document.get`**](./bg-logistics-shipment-document-get.md)。Scan Form 专项 skill：**`linkfox-temu-fulfillment-eu`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── packageSnList[] (STRING[], 必填)
    ├── shipCompanyId (LONG, 必填)
    └── warehouseId (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSnList | STRING[] | **是** | package number list（待纳入同一 Scan Form 的包裹号列表；须满足仓库、承运商、目的地、购标状态等一致性校验） |
| shipCompanyId | LONG | **是** | Ship company id（物流公司 ID；须与列表内包裹实际承运商一致，不一致时错误码 **120016060**） |
| warehouseId | STRING | **是** | Warehouse id（发货仓库 ID；须与列表内包裹仓库一致，不一致时错误码 **120016061**） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`packageSnList`**、**`shipCompanyId`**、**`warehouseId`** 均为必填。Partner **Request Example** CURL 将业务字段写在顶层；经 LinkFox 网关时建议放在 **`params.request`** 下（亦可与 `extract_business_params` 一致放在 `params` 顶层，由网关转发）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSnList": ["PKG-001", "PKG-002"],
    "shipCompanyId": 123456789,
    "warehouseId": "WH-US-001"
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSnList": ["PKG-001"],
    "shipCompanyId": 123456789,
    "warehouseId": "WH-US-001"
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
    └── scanFormInfoList[] (OBJECT[])
        ├── scanFormSn
        └── packageSnList[] (STRING[])
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
| scanFormInfoList | OBJECT[] | List of created scan form information（本次创建的 Scan Form 信息列表；一次请求可能因分组规则返回多条，每条对应一个 **`scanFormSn`** 及其关联包裹） |

#### `scanFormInfoList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| scanFormSn | STRING | Scan Form serial number（Scan Form 编号；用于后续 [**`temu.logistics.scanform.document.get`**](./temu-logistics-scanform-document-get.md) 获取文档 URL、交运对账等） |
| packageSnList | STRING[] | Package number list（本 Scan Form 关联的包裹号列表；为请求 **`packageSnList`** 的子集或分组结果） |

> 调用成功时先判断 **`response.success === true`**，再读取 **`result.scanFormInfoList`**。若部分包裹未能纳入 Scan Form，平台可能通过错误码整单失败；已关联其他 Scan Form 的包裹见 **120016056**。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 120016063 | The selected packages {*} are fulfilled by a cooperative warehouse. No scan form needs to be generated. | 合作仓包裹无需 Scan Form |
| 120011099 | At least {*} packages must be included in order to generate the corresponding scanform. | 增加 **`packageSnList`** 数量至平台要求下限 |
| 120016062 | The current packages cannot generate the same scan form... | 重新调用 [**`temu.logistics.candidate.scanform.list.get`**](./temu-logistics-candidate-scanform-list-get.md) |
| 120016061 | inconsistent warehouseId... | 统一 **`warehouseId`** 或按候选列表重选包裹 |
| 120016060 | inconsistent shipCompanyID... | 统一 **`shipCompanyId`** 或按候选列表重选包裹 |
| 120016056 | The selected packages {*} have been associated with other scan forms. | 勿重复创建；查已有 Scan Form |
| 120016054 | The mailing date must be between the current date and current date + 7 days (exclusive)... | 检查包裹邮寄日期窗口 |
| 120016055 | Shipping labels must be successfully bought for the packages... | 先完成购标 **`bg.logistics.shipment.create`** |
| 120016053 | Only USPS logistics is supported... | 仅 USPS 包裹可创建 Scan Form |
| 120016059 / 120016051 | destination region must be U.S. / consistent | 目的地须为美国且一致 |
| 120016052 | The {*} is invalid... | 核对 **`packageSn`**、站点与请求区域 |
| 120011067 | The selected packages exceed the maximum limit of 500. | 分批，每批 ≤500 |
| 120018010 | The packages {*} have been canceled... | 包裹已取消，需重新履约 |
| 120011001 / 120011002 | System abnormality / Invalid request parameters | 重试或修正参数 |

<details>
<summary>完整错误码列表（16 条，Partner 原文）</summary>

| 错误码 | 错误信息 |
|--------|----------|
| 120016063 | The selected packages {*} are fulfilled by a cooperative warehouse. No scan form needs to be generated. |
| 120011099 | At least {*} packages must be included in order to generate the corresponding scanform. |
| 120016062 | The current packages cannot generate the same scan form. Please request the "temu.logistics.candidate.scanform.list.get" interface again to obtain a list of package numbers that can generate the same scan form. |
| 120016061 | The current packages have inconsistent warehouseId. Please request the "temu.logistics.candidate.scanform.list.get" interface again to obtain a list of package numbers that can generate the same scan form. |
| 120016060 | The current packages have inconsistent shipCompanyID. Please request the "temu.logistics.candidate.scanform.list.get" interface again to obtain a list of package numbers that can generate the same scan form. |
| 120016056 | The selected packages {*} have been associated with other scan forms. |
| 120016054 | The mailing date must be between the current date and current date + 7 days (exclusive).Please check packages {*} |
| 120016055 | Shipping labels must be successfully bought for the packages.Please check packages {*} |
| 120016053 | Only USPS logistics is supported. Please check packages {*} |
| 120016059 | The destination region must be U.S.. |
| 120016051 | The destination region must be consistent. |
| 120016052 | The {*} is invalid. Please check the request area or if the packageSn is nonexistent. |
| 120011067 | The selected packages exceed the maximum limit of 500. |
| 120011001 | System abnormality, please check the data and try again |
| 120011002 | Invalid request parameters. |
| 120018010 | The packages {*} have been canceled. Please fulfill again by Temu non-integrated logistics or Temu integrated logistics. |

</details>

---

## 典型用法

```text
1. bg.logistics.shipment.create / result.get     → 购标成功，取得 packageSn
2. temu.logistics.candidate.scanform.list.get  →（推荐）获取可合并为同一 Scan Form 的包裹分组（见 [文档](./temu-logistics-candidate-scanform-list-get.md)）
3. temu.logistics.scanform.create              → 本接口，创建 Scan Form
4. temu.logistics.scanform.document.get        → 获取 Scan Form 文档 url
5. bg.logistics.shipment.document.get          → 购标面单（USPS 可能须 manifestation 后才可打印）
6. bg.logistics.shipped.package.confirm        → 确认发货
```

> [**`bg.logistics.shipment.document.get`**](./bg-logistics-shipment-document-get.md) 错误码 **120018012** 提示 USPS 面单须先完成 manifestation，可结合本接口或卖家中心 Scan Form 处理。

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_buy_shipping_logistics_scanform_create.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSnList": ["PKG-001", "PKG-002"],
    "shipCompanyId": 123456789,
    "warehouseId": "WH-US-001"
  }
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.logistics.scanform.create",
  "params": {
    "request": {
      "packageSnList": ["PKG-001", "PKG-002"],
      "shipCompanyId": 123456789,
      "warehouseId": "WH-US-001"
    }
  }
}'
```
