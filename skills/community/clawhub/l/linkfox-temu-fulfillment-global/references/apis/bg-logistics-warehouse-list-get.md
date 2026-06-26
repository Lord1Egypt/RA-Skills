# 店铺仓库列表 — `bg.logistics.warehouse.list.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_buy_shipping_logistics_warehouse_list_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.warehouse.list.get`，业务载荷放在 Body 的 `params` |

**Description:** Sellers can use this API to obtain the shop's warehouse information（获取店铺仓库信息；购标前筛选支持 Temu 面单的仓库、取 `warehouseId` / `selfShippingWarehouseId` 等）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> 下游 **`linkfox-temu-fulfillment-global`** 的 `bg.logistics.shipment.v2.confirm` 等接口中的 **`selfShippingWarehouseId`** 可来自本接口返回的 **`warehouseId`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── returnEnableBuyShippingLabelOnly    ← 选填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| returnEnableBuyShippingLabelOnly | BOOLEAN | 否 | 是否仅返回支持购买 Temu 物流面单（Buy Shipping Label）的仓库，见下表 |

#### `returnEnableBuyShippingLabelOnly`

| 值 / 行为 | 说明 |
|-----------|------|
| `true` | Only warehouses that support purchasing Temu shipping labels will be returned（仅返回支持购买 Temu 物流面单的仓库） |
| `false` | All warehouses will be returned (regardless of Temu shipping label support)（返回全部仓库，不论是否支持 Temu 面单） |
| 不传（默认） | Default behavior: all warehouses will be returned (same as `false`)（默认与 `false` 相同，返回全部仓库） |

> 官方表将顶层 **`request`** 标为选填（False）；筛选购标仓库时建议显式传 **`returnEnableBuyShippingLabelOnly: true`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "returnEnableBuyShippingLabelOnly": true
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {}
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
    └── warehouseList[] (OBJECT[])
        ├── defaultWarehouse
        ├── pushOrderToOpenPlatform
        ├── warehouseId
        ├── cooperativeWarehouseAuthorizationStatus
        ├── warehouseBrand
        ├── supportsUspsGroundAdvantage
        ├── regionId1
        ├── warehouseName
        ├── warehouseManagementType
        └── enableBuyShippingLabel
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
| warehouseList | OBJECT[] | 店铺仓库列表 |

#### `warehouseList[]` 元素字段

> 下列字段来自 Partner **Response Example** 与接口结构；若 Partner 在线文档 Response 表有补充说明，以在线表为准。

| 参数 | 类型 | 说明 |
|------|------|------|
| defaultWarehouse | BOOLEAN | 是否为默认仓库 |
| pushOrderToOpenPlatform | BOOLEAN | 是否将订单推送到开放平台 |
| warehouseId | STRING | Warehouse ID（仓库 ID；自发货确认等接口中的 **`selfShippingWarehouseId`** 通常使用此值） |
| cooperativeWarehouseAuthorizationStatus | BOOLEAN | 合作仓授权状态 |
| warehouseBrand | STRING | Warehouse brand（仓库品牌/品牌名） |
| supportsUspsGroundAdvantage | BOOLEAN | 是否支持 USPS Ground Advantage |
| regionId1 | INTEGER | Region ID（区域 ID，一级区域编码） |
| warehouseName | STRING | Warehouse name（仓库名称） |
| warehouseManagementType | INTEGER | Warehouse management type（仓库管理类型；具体枚举以 Partner 文档为准） |
| enableBuyShippingLabel | BOOLEAN | 是否支持购买 Temu 物流面单（Buy Shipping Label）；与入参 **`returnEnableBuyShippingLabelOnly=true`** 筛选逻辑相关 |

> 调用成功时先判断 **`response.success === true`**，再遍历 **`result.warehouseList`**。购标流程可优先选择 **`enableBuyShippingLabel === true`** 的仓库。

---

## 典型用法

```text
1. bg.logistics.warehouse.list.get（returnEnableBuyShippingLabelOnly=true）→ 可选仓库 warehouseId
2. [bg.logistics.shippingservices.get](./bg-logistics-shippingservices-get.md) → 选渠道 / channelId
3. [bg.logistics.shipment.create](./bg-logistics-shipment-create.md) → 购标
4. linkfox-temu-fulfillment-global → selfShippingWarehouseId 取自 warehouseId
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

# 仅返回支持购标的仓库
python scripts/global_buy_shipping_logistics_warehouse_list_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "returnEnableBuyShippingLabelOnly": true
  }
}'
```

```bash
# 返回全部仓库（默认行为）
python scripts/global_buy_shipping_logistics_warehouse_list_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {}
}'
```

```bash
python scripts/temu_global_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.logistics.warehouse.list.get",
  "params": {
    "request": {
      "returnEnableBuyShippingLabelOnly": true
    }
  }
}'
```