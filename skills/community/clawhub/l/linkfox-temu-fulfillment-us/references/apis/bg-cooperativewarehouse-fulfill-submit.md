# 提交合作仓履约 — `bg.cooperativewarehouse.fulfill.submit`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_co_warehouse_cooperativewarehouse_fulfill_submit.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fd19c5c9a430407a8c587d7f3e492c4a&sub_menu_code=d2d218ed9b8c4356aec5033744abe90b |
| **网关** | `POST /temu/proxy`，`type`=`bg.cooperativewarehouse.fulfill.submit`，业务载荷放在 Body 的 `params` |

**Description:** cooperativewarehouse_fulfill

（向合作仓服务商提交一笔**合作仓履约单**：指定合作仓、ERP 履约号、尾程发货方式及子订单 SKU/数量等；平台返回履约状态与合作仓履约号。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，且 **`managementType=semi-managed`**（本 skill 仅 Semi-managed）。  
> **前置依赖：**  
> - **`warehouseProviderCode`** 来自 [**`bg.cooperativewarehouse.provider.list`**](./bg-cooperativewarehouse-provider-list.md)。  
> - 若 **`authorizeType=0`**（默认），须已完成 [**`bg.cooperativewarehouse.token.authorization`**](./bg-cooperativewarehouse-token-authorization.md)，并填写 **`cwCustomerCode`**。  
> - 若 **`authorizeType=1`**，须填写 **`authorizeToken`**（及可选 **`authorizeKey`**）。  
> - **`orderSn`** / **`parentOrderSn`** 等通常来自 **`linkfox-temu-order-us`** 订单接口。  
> **后续：** 可用 **`bg.cooperativewarehouse.fulfill.query`** 查询履约结果（待接入）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── warehouseProviderCode (STRING, 必填)
    ├── authorizeType (INTEGER, 选填, 默认 0)
    ├── authorizeKey (STRING, 选填)
    ├── authorizeToken (STRING, 条件必填)
    ├── cwCustomerCode (STRING, 条件必填)
    ├── warehouseCode (STRING, 必填)
    ├── erpFulfillNo (STRING, 必填)
    ├── tailShippingMode (INTEGER, 选填)
    ├── logisticsProductCode (STRING, 条件必填)
    ├── packageSn (STRING, 条件必填)
    ├── shipCompanyId (LONG, 选填)
    ├── channelId (LONG, 选填)
    ├── channelVersionId (LONG, 选填)
    ├── shipCompanyName (STRING, 条件必填)
    ├── trackingNumber (STRING, 条件必填)
    ├── shippingLabelFileType (STRING, 条件必填)
    ├── shippingLabelFileBase64 (STRING, 条件必填)
    ├── shipLogisticsType (STRING, 条件必填)
    └── orderList[] (OBJECT[], 必填)
        ├── cwSkuCode (STRING, 必填)
        ├── productSkuId (LONG, 选填)
        ├── quantity (INTEGER, 必填)
        ├── orderSn (STRING, 必填)
        ├── parentOrderSn (STRING, 必填)
        └── skuId (LONG, 选填)
```

> Partner **Request** 表在导出 HTML 中 **`orderList`** 子行未展开；上表 **`orderList[]`** 子字段按 **Request Example** 与 **Error Code**（170020024–170020027）补全。

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| warehouseProviderCode | STRING | **是** | cooperative warehouse provider code（合作仓服务商编码；与 [**provider.list**](./bg-cooperativewarehouse-provider-list.md) 中 **`warehouseProviderCode`** 一致） |
| authorizeType | INTEGER | 否 | Cooperation warehouse authorization methods（合作仓授权方式：**`0`** = 使用平台授权信息（using platform authorization information）；**`1`** = 直接上传授权信息（directly uploading authorization information）。未传时**默认为 `0`**） |
| authorizeKey | STRING | 否 | cooperative warehouse authorization app key（合作仓授权 App Key；部分服务商在 **`authorizeType=1`** 时与 **`authorizeToken`** 一并使用） |
| authorizeToken | STRING | 条件 | Cooperative Warehouse Authorization Token, mandatory when authorizeType is 1（合作仓授权 Token；**`authorizeType=1`** 时**必填**，错误码 **170020038**） |
| cwCustomerCode | STRING | 条件 | cooperative warehouse customer code, mandatory when authorizeType is 0（合作仓客户编码；**`authorizeType=0`**（含默认）时**必填**，错误码 **170020037**；须与已授权客户编码一致，见 **170020005**） |
| warehouseCode | STRING | **是** | cooperative warehouse code（合作仓仓库编码） |
| erpFulfillNo | STRING | **是** | erp fulfill number（ERP/WMS 侧履约单号；须唯一，重复提交见 **170020009**） |
| tailShippingMode | INTEGER | 否 | tail shipping mode（尾程发货模式；不同取值下条件必填字段见下表及错误码 **170020028**–**170020036**） |
| logisticsProductCode | STRING | 条件 | logistics product code（物流产品编码；**`tailShippingMode=0`** 时**必填**，错误码 **170020028**） |
| packageSn | STRING | 条件 | package sn（包裹号；**`tailShippingMode=1`** 时**必填**，错误码 **170020029**；包裹不存在见 **170020039**） |
| shipCompanyId | LONG | 否 | ship company id（承运商 ID；**`tailShippingMode=1`** 时**必填**，错误码 **170020034**；须与 **`shipCompanyName`** 映射一致，见 **170020011**） |
| channelId | LONG | 否 | channel id（渠道 ID；**`tailShippingMode=1`** 时**必填**，错误码 **170020035**；须与 **`shipCompanyName`**、**`shipLogisticsType`** 匹配，见 **170020041**） |
| channelVersionId | LONG | 否 | channel version id（渠道版本 ID） |
| shipCompanyName | STRING | 条件 | ship company name（承运商名称；**`tailShippingMode=1`** 时**必填**，错误码 **170020030**） |
| trackingNumber | STRING | 条件 | trackingNumber（运单号；**`tailShippingMode=1`** 时**必填**，错误码 **170020031**；须与包裹运单一致，见 **170020040**） |
| shippingLabelFileType | STRING | 条件 | ship label file type（面单文件类型；**`tailShippingMode=1`** 时**必填**，错误码 **170020032**；类型非法见 **170020007**） |
| shippingLabelFileBase64 | STRING | 条件 | shippingLabelFileBase64（面单文件 Base64 内容；**`tailShippingMode=1`** 时**必填**，错误码 **170020033**；内容非法见 **170020008**） |
| shipLogisticsType | STRING | 条件 | shipLogisticsType（物流类型；**`tailShippingMode=1`** 时**必填**，错误码 **170020036**） |
| orderList | OBJECT[] | **是** | sub order list（子订单列表；至少一条，错误码 **170020023**） |

#### `authorizeType` 与授权字段

| authorizeType | 含义 | 必填业务字段 |
|---------------|------|----------------|
| `0`（默认） | 使用平台授权信息 | **`cwCustomerCode`** |
| `1` | 直接上传授权 | **`authorizeToken`**（可选 **`authorizeKey`**） |

#### `tailShippingMode` 与尾程字段

| tailShippingMode | 含义（Partner 表仅写 tail shipping mode；条件必填以 Error Code 为准） | 条件必填字段 |
|------------------|------------------------------------------------------------------------|----------------|
| `0` | 合作仓/平台物流产品发货 | **`logisticsProductCode`** |
| `1` | 卖家/ERP 自带面单与运单 | **`packageSn`**、**`shipCompanyName`**、**`trackingNumber`**、**`shippingLabelFileType`**、**`shippingLabelFileBase64`**、**`shipCompanyId`**、**`channelId`**、**`shipLogisticsType`** |

> 尾程模式非法见 **170020006**；当前承运商不支持面单见 **170020010**。

### `orderList[]` 元素

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cwSkuCode | STRING | **是** | 合作仓 SKU 编码（Partner Request Example 字段；错误码 **170020026**） |
| productSkuId | LONG | 否 | 商品 SKU ID（Partner Request Example 示例为数值；Request 表未单独列出） |
| quantity | INTEGER | **是** | 发货数量（错误码 **170020027**） |
| orderSn | STRING | **是** | 子订单号（错误码 **170020024**；无效见 **170020012**） |
| parentOrderSn | STRING | **是** | 父订单号（错误码 **170020025**） |
| skuId | LONG | 否 | SKU ID（Partner Request Example 示例为数值；Request 表未单独列出） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "managementType": "semi-managed",
  "request": {
    "warehouseProviderCode": "PROVIDER_CODE",
    "authorizeType": 0,
    "cwCustomerCode": "YOUR_CW_CUSTOMER_CODE",
    "warehouseCode": "WAREHOUSE_CODE",
    "erpFulfillNo": "ERP_FULFILL_NO_001",
    "tailShippingMode": 0,
    "logisticsProductCode": "LOGISTICS_PRODUCT_CODE",
    "orderList": [
      {
        "cwSkuCode": "CW_SKU_001",
        "productSkuId": 1,
        "quantity": 1,
        "orderSn": "ORDER_SN",
        "parentOrderSn": "PARENT_ORDER_SN",
        "skuId": 1
      }
    ]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "managementType": "semi-managed",
  "request": {
    "warehouseProviderCode": "PROVIDER_CODE",
    "authorizeType": 1,
    "authorizeKey": "AUTHORIZE_KEY",
    "authorizeToken": "AUTHORIZE_TOKEN",
    "warehouseCode": "WAREHOUSE_CODE",
    "erpFulfillNo": "ERP_FULFILL_NO_002",
    "tailShippingMode": 1,
    "packageSn": "PACKAGE_SN",
    "shipCompanyId": 1,
    "channelId": 1,
    "channelVersionId": 1,
    "shipCompanyName": "CARRIER_NAME",
    "trackingNumber": "TRACKING_NUMBER",
    "shippingLabelFileType": "PDF",
    "shippingLabelFileBase64": "BASE64_LABEL_CONTENT",
    "shipLogisticsType": "LOGISTICS_TYPE",
    "orderList": [
      {
        "cwSkuCode": "CW_SKU_001",
        "quantity": 1,
        "orderSn": "ORDER_SN",
        "parentOrderSn": "PARENT_ORDER_SN"
      }
    ]
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；**`result`** 子行在导出 HTML 中为折叠状态，下列子层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    ├── fulfillStatus (INTEGER)
    ├── erpFulfillNo (STRING)
    └── cwFulfillNo (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | response result（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| fulfillStatus | INTEGER | 履约状态（Partner Response 表未展开；**Response Example** 示例值为 **`1`**，具体枚举以 Temu/合作仓文档为准） |
| erpFulfillNo | STRING | erp fulfill number（回显提交的 ERP 履约单号） |
| cwFulfillNo | STRING | 合作仓履约单号（合作仓侧生成的履约编号，用于后续查询/对账） |

> 调用成功时先判断 **`success === true`**，再读 **`result.fulfillStatus`**、**`result.cwFulfillNo`**。若需轮询或核对，使用 **`bg.cooperativewarehouse.fulfill.query`**（待接入）。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 170020021 | Parameter [warehouseProviderCode] is required but not provided in the input | 填写 **`warehouseProviderCode`** |
| 170020022 | Parameter [erpFulfillNo] is required but not provided in the input | 填写 **`erpFulfillNo`** |
| 170020023 | Parameter [orderList] is required but not provided in the input | 提供 **`orderList`** 且至少一条 |
| 170020024 | Parameter [orderSn] is required but not provided in the input | **`orderList[]`** 中填写 **`orderSn`** |
| 170020025 | Parameter [parentOrderSn] is required but not provided in the input | 填写 **`parentOrderSn`** |
| 170020026 | Parameter [cwSkuCode] is required but not provided in the input | 填写 **`cwSkuCode`** |
| 170020027 | Parameter [quantity] is required but not provided in the input | 填写 **`quantity`** |
| 170020028 | The [tailShippingMode] is 0, and the required parameter [logisticsProductCode] has not been filled in | **`tailShippingMode=0`** 时补 **`logisticsProductCode`** |
| 170020029 | The [tailShippingMode] is 1, and the required parameter [packageSn] has not been filled in | **`tailShippingMode=1`** 时补 **`packageSn`** |
| 170020030 | The [tailShippingMode] is 1, and the required parameter [shipCompanyName] has not been filled in | 补 **`shipCompanyName`** |
| 170020031 | [tailShippingMode] is 1, and the required parameter [trackingNumber] has not been filled in | 补 **`trackingNumber`** |
| 170020032 | The [tailShippingMode] is 1, and the required parameter [shippingLabelFileType] has not been filled in | 补 **`shippingLabelFileType`** |
| 170020033 | The [tailShippingMode] is 1, and the required parameter [shippingLabelFileBase64] has not been filled in | 补 **`shippingLabelFileBase64`** |
| 170020034 | The [tailShippingMode] is 1, and the required parameter [shipCompanyId] has not been filled in | 补 **`shipCompanyId`** |
| 170020035 | The [tailShippingMode] is 1, and the required parameter [channelId] has not been filled in | 补 **`channelId`** |
| 170020036 | The [tailShippingMode] is 1, and the required parameter [shipLogisticsType] has not been filled in | 补 **`shipLogisticsType`** |
| 170020037 | The [authorizeType] is 0, and the required parameter [cwCustomerCode] has not been filled in | **`authorizeType=0`** 时补 **`cwCustomerCode`** |
| 170020038 | The [authorizeType] is 1, and the required parameter [authorizeToken] has not been filled in | **`authorizeType=1`** 时补 **`authorizeToken`** |
| 170020039 | The package number does not exist. | 检查 **`packageSn`** |
| 170020040 | The tracking number corresponding to this package does not match the trackingNumber field. | **`trackingNumber`** 与包裹运单一致 |
| 170020041 | ChannelId, shipCompanyName and logisticType not match, please check! | 核对 **`channelId`** / **`shipCompanyName`** / **`shipLogisticsType`** |
| 170020001 | This ERP provider is not supported. | 更换支持的 **`warehouseProviderCode`** |
| 170020002 | This mall is not authorized to the cooperative warehouse service provider. | 先完成服务商授权 |
| 170020003 | The parameter is illegal, please check and try again. | 检查入参格式 |
| 170020005 | This cooperative warehouse customer code is not match the authorized customer code. | 修正 **`cwCustomerCode`** |
| 170020009 | This fulfillment order already exists, please submit another one. | 更换 **`erpFulfillNo`** |
| 170020006 | This fulfillment order has wrong tail shipping mode, please check and try again. | 修正 **`tailShippingMode`** 及关联字段 |
| 170020007 | This fulfillment order has wrong shipping label file type, please check and try again. | 修正 **`shippingLabelFileType`** |
| 170020008 | This fulfillment order has wrong shipping label file content, please check and try again. | 修正 **`shippingLabelFileBase64`** |
| 170020010 | The service provider does not support shipping label for the current shippingCompanyName... | 更换承运商或尾程方式 |
| 170020011 | This ship company id not match with the ship company name mapped. | **`shipCompanyId`** 与 **`shipCompanyName`** 一致 |
| 170020012 | The parentOrderSn in fulfill order is invalid. | 核对订单号 |
| 170020014 | The cooperative warehouse service provider returned: API authorization exception... | 刷新合作仓 Token |
| 170020016 | Your store has been restricted from using the function of logistics shipping by partner warehouse service providers... | 联系平台/服务商解除限制 |

<details>
<summary>完整错误码列表（Partner 原文，含占位符项）</summary>

| 错误码 | 错误信息 |
|--------|----------|
| 170020017 | Parameter {*} is required but not provided in the input. |
| 170020018 | The [authorizeType] is {*} , and the required parameter {*} has not been filled in. |
| 170020019 | The [tailShippingMode] is {*} and the required parameter {*} has not been filled in. |
| 170020004 | This fulfillment order not exists, please check if the fulfillment number is correct. |
| 170020013 | The service provider has not signed the DPA Agreement of the country and cannot perform the contract... |
| 170020015 | The current order does not support address query, please check! |

</details>

---

## 典型用法

```text
1. bg.cooperativewarehouse.provider.list      → warehouseProviderCode、warehouseCode
2. bg.cooperativewarehouse.token.authorization → authorizeType=0 时绑定 cwCustomerCode
3. bg.cooperativewarehouse.fulfill.submit      → 本接口：提交履约
4. bg.cooperativewarehouse.fulfill.query         → 查询履约结果（待接入）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_co_warehouse_cooperativewarehouse_fulfill_submit.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "managementType": "semi-managed",
  "request": {
    "warehouseProviderCode": "PROVIDER_CODE",
    "cwCustomerCode": "YOUR_CW_CUSTOMER_CODE",
    "warehouseCode": "WAREHOUSE_CODE",
    "erpFulfillNo": "ERP_FULFILL_NO_001",
    "tailShippingMode": 0,
    "logisticsProductCode": "LOGISTICS_PRODUCT_CODE",
    "orderList": [
      {
        "cwSkuCode": "CW_SKU_001",
        "quantity": 1,
        "orderSn": "ORDER_SN",
        "parentOrderSn": "PARENT_ORDER_SN"
      }
    ]
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.cooperativewarehouse.fulfill.submit",
  "params": {
    "request": {
      "warehouseProviderCode": "PROVIDER_CODE",
      "warehouseCode": "WAREHOUSE_CODE",
      "erpFulfillNo": "ERP_FULFILL_NO_001",
      "orderList": []
    }
  }
}'
```
