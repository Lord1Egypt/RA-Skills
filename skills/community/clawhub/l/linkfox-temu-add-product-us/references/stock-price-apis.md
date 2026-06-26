# 库存与价格 API — 参数参考

经 `POST /temu/proxy` 转发，网关见 [api.md](./api.md)。

---

## 1. 虚拟库存查询 — `bg.btg.goods.stock.quantity.get`

- **sub_menu_code**：`d72b66d07b1f499bbd80720367e58e1f`
- **脚本**：`scripts/us_goods_stock_get.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productSkcId | integer | 是 | 货品 SKC ID |

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 条数 |
| productSkuStockList | array | SKU 库存列表 |

#### `productSkuStockList[]`

| 字段 | 类型 | 说明 |
|------|------|------|
| productSkuId | integer | SKU ID |
| skuStockQuantity | integer | 虚拟库存（不可查看时为 null） |
| warehouseId | string | 仓库 ID（欧区可分仓） |
| shippingMode | integer | 1 卖家自发货，2 认证仓 |
| tempLockQuantity | integer | 未支付锁定库存 |

### 示例

```bash
python scripts/us_goods_stock_get.py '{
  "accessToken": "TOKEN",
  "productSkcId": 123456789
}'
```

---

## 2. 虚拟库存更新 — `bg.btg.goods.stock.quantity.update`

- **sub_menu_code**：`e84f651da04f4fedb85d37e375a4e2d8`
- **脚本**：`scripts/us_goods_stock_update.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| quantityChangeMode | integer | 是 | `1` 增减变更；`2` 覆盖变更（默认 1） |
| productSkcId | integer | 否 | SKC ID |
| skuStockChangeList | array | 是 | 库存调整项 |

#### `skuStockChangeList[]`

| 字段 | 类型 | 条件 | 说明 |
|------|------|------|------|
| productSkuId | integer | 是 | SKU ID |
| warehouseId | string | 是 | 发货仓 ID |
| stockDiff | integer | mode=1 | 增减量（正增负减） |
| targetStockAvailable | integer | mode=2 | 覆盖后的目标库存（≥0） |
| currentShippingMode | integer | 否 | 当前发货模式 |
| currentStockAvailable | integer | 否 | 当前库存 |

### 示例

```bash
python scripts/us_goods_stock_update.py '{
  "accessToken": "TOKEN",
  "quantityChangeMode": 1,
  "skuStockChangeList": [{
    "productSkuId": 58224724203874,
    "warehouseId": "WH001",
    "stockDiff": 10
  }]
}'
```

---

## 3. 供货价列表 — `temu.goods.price.list.get`

- **sub_menu_code**：`a084faecbad64d7f93c485378b5bd9bf`
- **脚本**：`scripts/us_goods_price_list.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productSkuIds | array | 是 | 货品 SKU ID 列表 |

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| productSkuSupplierPriceList | array | 供货价列表 |

#### `productSkuSupplierPriceList[]`

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | integer | 货品 ID |
| productSkcId | integer | SKC ID |
| productSkuId | integer | SKU ID |
| supplierPrice | number | 供货价 |
| currencyType | string/number | 币种 |
| siteSupplierPrices | array | 分站点供货价（半托管） |

### 示例

```bash
python scripts/us_goods_price_list.py '{
  "accessToken": "TOKEN",
  "productSkuIds": [58224724203874, 58224724203875]
}'
```
