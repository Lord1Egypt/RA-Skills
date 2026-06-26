# SKU 供货价列表查询 — `bg.local.goods.sku.list.price.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_price_sku_list_price_query.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=a9bd154c38384f2c99e57c2ebe271299 |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.sku.list.price.query`，业务载荷放在 Body 的 `params` |

**Description:** Query supplier/base price for goods SKUs by goodsId and skuIdList.

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。Partner 导出 HTML 中 **Response** 表多为折叠，下列 **Response** 按 **Response Example** 展开。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
    └── language (STRING)
    └── querySupplierPriceBaseList (OBJECT[] **必填**)
    └── querySupplierPriceBaseList[].goodsId (LONG **必填**)
    └── querySupplierPriceBaseList[].skuIdList (LONG[] **必填**)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | Language |
| querySupplierPriceBaseList | OBJECT[] | **是** | Query supplier price base list |

#### `request.querySupplierPriceBaseList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | **是** | Goods ID（商品 ID） |
| skuIdList | LONG[] | **是** | SKU ID list（SKU ID 列表） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "querySupplierPriceBaseList": [
      {
        "goodsId": 123456789,
        "skuIdList": [
          58224724203874,
          58224724203875
        ]
      }
    ],
    "language": "en"
  }
}
```

> Partner **Request Example** CURL 将 `querySupplierPriceBaseList` 写在顶层；经 LinkFox 网关请放在 **`params.request`**（或脚本接受的顶层 `request` 字段）。

---

## Response（Temu `body` 解析后）

```text
response
├── success (BOOLEAN)
├── errorCode (INTEGER)
├── errorMsg (STRING)
└── result (OBJECT)
    ├── openapiGoodsSupplierPriceDTOList[] (OBJECT[])
    ├── openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[] (OBJECT[])
    ├── openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[].supplierPrice (OBJECT)
    ├── openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[].supplierPrice.amount (STRING)
    ├── openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[].supplierPrice.currency (STRING)
    ├── openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[].skuId (INTEGER)
    ├── openapiGoodsSupplierPriceDTOList[].goodsId (INTEGER)
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | 当前请求是否成功 |
| errorCode | INTEGER | 错误码 |
| errorMsg | STRING | 错误信息 |
| result | OBJECT | 业务结果 |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| openapiGoodsSupplierPriceDTOList[] | OBJECT[] | Partner Response Example |
| openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[] | OBJECT[] | Partner Response Example |
| openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[].supplierPrice | OBJECT | Partner Response Example |
| openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[].supplierPrice.amount | STRING | Partner Response Example |
| openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[].supplierPrice.currency | STRING | Partner Response Example |
| openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[].skuId | INTEGER | Partner Response Example |
| openapiGoodsSupplierPriceDTOList[].goodsId | INTEGER | Partner Response Example |

#### `openapiGoodsSupplierPriceDTOList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| openapiSkuSupplierPriceDTOList[] | OBJECT[] | Partner Response Example |
| openapiSkuSupplierPriceDTOList[].supplierPrice | OBJECT | Partner Response Example |
| openapiSkuSupplierPriceDTOList[].supplierPrice.amount | STRING | Partner Response Example |
| openapiSkuSupplierPriceDTOList[].supplierPrice.currency | STRING | Partner Response Example |
| openapiSkuSupplierPriceDTOList[].skuId | INTEGER | Partner Response Example |
| goodsId | INTEGER | Partner Response Example |

#### `openapiGoodsSupplierPriceDTOList[].openapiSkuSupplierPriceDTOList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| supplierPrice | OBJECT | Partner Response Example |
| supplierPrice.amount | STRING | Partner Response Example |
| supplierPrice.currency | STRING | Partner Response Example |
| skuId | INTEGER | Partner Response Example |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_price_sku_list_price_query.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "querySupplierPriceBaseList": [       {         "goodsId": 123456789,         "skuIdList": [           58224724203874,           58224724203875         ]       }     ],     "language": "en"   } }'
```
