# 合作仓服务商列表 — `bg.cooperativewarehouse.provider.list`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_co_warehouse_cooperativewarehouse_provider_list.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fd19c5c9a430407a8c587d7f3e492c4a&sub_menu_code=e77d444a60b540039bfa1fc64e3cada7 |
| **网关** | `POST /temu/proxy`，`type`=`bg.cooperativewarehouse.provider.list`，业务载荷放在 Body 的 `params` |

**Description:** cooperate warehouse erp order（Partner 导出页 Description 原文；本接口用于查询**合作仓（Cooperative Warehouse）服务商/ERP** 列表及授权许可状态，供后续 [**`bg.cooperativewarehouse.token.authorization`**](./bg-cooperativewarehouse-token-authorization.md) 等合作仓履约流程使用。）

（查询当前店铺可用的**合作仓服务商**（Warehouse Provider）列表，包含服务商编码、品牌、支持的承运商、区域、客户编码及包裹配送类型等；**`permitsStatus`** 反映合作仓相关许可/授权状态。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，且 **`managementType=semi-managed`**（本 skill 仅 Semi-managed）。  
> **后续：** 授权绑定见 [**`bg.cooperativewarehouse.token.authorization`**](./bg-cooperativewarehouse-token-authorization.md)；履约提交见 [**`bg.cooperativewarehouse.fulfill.submit`**](./bg-cooperativewarehouse-fulfill-submit.md)；查询见 **`bg.cooperativewarehouse.fulfill.query`**（待接入）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── needAllPlatformProviders (BOOLEAN, 选填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| needAllPlatformProviders | BOOLEAN | 否 | needAllPlatformProviders（是否返回**全平台**合作仓服务商列表；Partner Request 表将该说明写在 Required 列。`true` 时通常返回平台侧全部可选服务商；`false` 或不传时返回与当前店铺/授权范围相关的服务商，以实际调通为准） |

> 官方 Request 表将 **`request`** 与 **`needAllPlatformProviders`** 均标为选填（False）。Partner **Request Example** CURL 将 **`needAllPlatformProviders`** 写在顶层，经 LinkFox 网关时建议放在 **`params.request.needAllPlatformProviders`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "managementType": "semi-managed",
  "request": {
    "needAllPlatformProviders": true
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "managementType": "semi-managed",
  "request": {}
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；**`result`** 在导出 HTML 中为折叠状态，下列子层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    ├── permitsStatus
    └── warehouseProviderList[] (OBJECT[])
        ├── warehouseProviderCode
        ├── warehouseProviderBrandName
        ├── supportNoCwCustomCode
        ├── cwCustomerCodeList[] (STRING[])
        ├── regionId[] (STRING[])
        ├── supportedPackageDeliveryType[] (INTEGER[])
        └── supportedShipCompany[] (OBJECT[])
            ├── shipCompanyName
            └── shipCompanyId
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
| permitsStatus | INTEGER | Permits / authorization status（合作仓相关许可或授权状态；Response Example 为 **`1`**；具体枚举含义以 Partner 在线 Response 表为准，可结合后续 **`bg.cooperativewarehouse.token.authorization`** 判断店铺是否已完成服务商授权） |
| warehouseProviderList | OBJECT[] | Warehouse provider list（合作仓服务商列表） |

#### `warehouseProviderList[]` 元素字段

> Partner **Response** 表中 **`result`** 子行在导出 HTML 中为折叠状态；下列字段与类型来自 **Response Example**，说明结合 Co-Warehouse 履约语义整理。若 Partner 在线文档 **Expand** 后有更完整枚举，以在线表为准。

| 参数 | 类型 | 说明 |
|------|------|------|
| warehouseProviderCode | STRING | Warehouse provider code（合作仓服务商编码；后续授权、履约接口中标识服务商） |
| warehouseProviderBrandName | STRING | Warehouse provider brand name（合作仓服务商品牌/展示名称） |
| supportNoCwCustomCode | INTEGER | Whether supports scenarios without cooperative warehouse custom code（是否支持无合作仓客户编码（cw custom code）的场景；Response Example 为 **`1`**，具体布尔语义以 Partner 为准） |
| cwCustomerCodeList | STRING[] | Cooperative warehouse customer code list（合作仓客户编码列表；绑定/授权后用于履约） |
| regionId | STRING[] | Region ID list（该服务商支持的发货/履约区域 ID 列表） |
| supportedPackageDeliveryType | INTEGER[] | Supported package delivery type list（支持的包裹配送类型列表；Response Example 为整数数组，具体类型枚举以 Partner 为准） |
| supportedShipCompany | OBJECT[] | Supported shipping company list（该合作仓服务商支持的物流公司/承运商列表） |

##### `warehouseProviderList[].supportedShipCompany[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| shipCompanyId | INTEGER | Ship company ID（物流公司/承运商 ID） |
| shipCompanyName | STRING | Ship company name（物流公司/承运商名称） |

> 调用成功时先判断 **`success === true`**，再读 **`result.permitsStatus`** 与 **`warehouseProviderList`**。选定 **`warehouseProviderCode`** 后，通常继续调用 [**`bg.cooperativewarehouse.token.authorization`**](./bg-cooperativewarehouse-token-authorization.md) 完成授权，再使用 **`bg.cooperativewarehouse.fulfill.submit`** 等提交合作仓履约。

---

## 典型用法

```text
1. bg.cooperativewarehouse.provider.list（本接口）  → 查询可选合作仓服务商、permitsStatus
2. bg.cooperativewarehouse.token.authorization      → 服务商 Token 授权（见 [文档](./bg-cooperativewarehouse-token-authorization.md)）
3. bg.cooperativewarehouse.fulfill.submit      → 提交合作仓履约
4. bg.cooperativewarehouse.fulfill.query       → 查询合作仓履约（待接入）
4. linkfox-temu-order-us                           → 订单状态刷新
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_co_warehouse_cooperativewarehouse_provider_list.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "managementType": "semi-managed",
  "request": {
    "needAllPlatformProviders": true
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "managementType": "semi-managed",
  "type": "bg.cooperativewarehouse.provider.list",
  "params": {
    "request": {}
  }
}'
```
