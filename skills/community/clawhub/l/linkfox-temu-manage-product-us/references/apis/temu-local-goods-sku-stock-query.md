# SKU 库存查询 — `temu.local.goods.sku.stock.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_manage_sku_stock_query.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=f14a3f28b654441b80f90e76a0a77c6e |
| **网关** | `POST /temu/proxy`，`type`=`temu.local.goods.sku.stock.query`，业务载荷放在 Body 的 `params` |

**Description:** local-local goods SKU stock query.

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── language
    ├── outSkuSnList      ← 外部 SKU 编码列表
    ├── skuIdList         ← SKU ID 列表
    └── goodsId           ← 商品 ID
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | Language |
| outSkuSnList | STRING[] | 否 | External SKU Code List |
| skuIdList | LONG[] | 否 | sku id list |
| goodsId | LONG | 否 | goods id |

> 官方四项均为选填；实际调用时至少传一种筛选（`goodsId`、`skuIdList` 或 `outSkuSnList`），以 Partner 文档与实网校验为准。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "language": "en",
    "goodsId": 123456
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "skuIdList": [58224724203874, 58224724203875]
  }
}
```

---

## Response（Temu `body` 解析后）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | 当前请求是否成功 |
| errorCode | INTEGER | 错误码 |
| errorMsg | STRING | 错误信息 |
| result | OBJECT | Result |
| result.stockList | OBJECT[] | Stock Details |

### `result.stockList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods Id |
| skuStockInfoList | OBJECT[] | SKU Stock Details |

### `skuStockInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| skuId | LONG | SKU ID |
| outSkuSn | STRING | Out Sku Sn |
| selfOrdinaryStock | OBJECT | self ordinary stock，见下 |
| selfPreSaleStock | OBJECT | self Pre-sale Inventory，见下 |
| certOrdinaryStock | OBJECT | cert ordinary Inventory，见下 |

#### 库存块公共字段

三类库存对象结构相同（`selfPreSaleStock` 额外含预售字段）：

| 参数 | 类型 | 说明 |
|------|------|------|
| stockType | INTEGER | 库存类型：`0` self ordinary stock，`1` self Pre-sale stock，`2` cert ordinary stock |
| stock | LONG | Inventory quantity |

**仅 `selfPreSaleStock` 额外字段：**

| 参数 | 类型 | 说明 |
|------|------|------|
| preSaleEndTime | LONG | Pre-sale end time |
| mallPreSaleSkuNumLimit | INTEGER | Store-level pre-sale inventory limit |
| skuPreSaleStockLimit | LONG | SKU-level pre-sale inventory limit |

---

## 示例

```bash
python scripts/us_manage_sku_stock_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456
  }
}'
```

```bash
python scripts/us_manage_sku_stock_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "skuIdList": [58224724203874],
    "outSkuSnList": ["MY-SKU-001"]
  }
}'
```
