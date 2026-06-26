# 批量修改 SKU 基础价（定价单）— `bg.local.goods.priceorder.change.sku.price`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_price_priceorder_change_sku_price.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.priceorder.change.sku.price`，业务载荷放在 Body 的 `params` |

**Description:** Support merchants within the **white list** to modify SKU base prices in batches.

> 须在 Temu 白名单内方可调用；非白名单店铺可能返回业务错误。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── goodsId (LONG, 必填)
    ├── changeSkuPriceDTOList[] (OBJECT[], 必填)
    │   ├── reason (STRING, 否)
    │   └── skuChangePriceBaseDTOList[] (OBJECT[], 必填)
    │       ├── skuId (LONG, 必填)
    │       └── newSupplierPrice (OBJECT, 必填)
    │           ├── amount (STRING, 否)
    │           └── currency (STRING, 否)
    └── rejectSkuPricing (BOOLEAN, 否)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | **是** | Goods Id |
| changeSkuPriceDTOList | OBJECT[] | **是** | SKU information and reason that adjust price |
| rejectSkuPricing | BOOLEAN | 否 | Reject if price order is wait merchant confirm |

### `changeSkuPriceDTOList[]` 元素

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reason | STRING | 否 | The reason of adjust price |
| skuChangePriceBaseDTOList | OBJECT[] | **是** | SKU information |

### `skuChangePriceBaseDTOList[]` 元素

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| skuId | LONG | **是** | SKU ID |
| newSupplierPrice | OBJECT | **是** | Base price (new supplier price) |

### `newSupplierPrice`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| amount | STRING | 否 | Amount |
| currency | STRING | 否 | Currency Type |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "rejectSkuPricing": true,
    "changeSkuPriceDTOList": [
      {
        "reason": "Cost adjustment",
        "skuChangePriceBaseDTOList": [
          {
            "skuId": 58224724203874,
            "newSupplierPrice": {
              "amount": "18.99",
              "currency": "USD"
            }
          },
          {
            "skuId": 58224724203875,
            "newSupplierPrice": {
              "amount": "19.99",
              "currency": "USD"
            }
          }
        ]
      }
    ]
  }
}
```

> 同一 `goodsId` 下可在一个 `changeSkuPriceDTOList` 项里放多个 SKU；也可按调价原因拆成多项，每项带各自的 `reason` 与 `skuChangePriceBaseDTOList`。

---

## Response（Temu `body` 解析后）

```text
response
├── success (BOOLEAN)
├── errorCode (INTEGER)
├── errorMsg (STRING)
└── result (OBJECT)
    ├── successSkuList[] (LONG)
    ├── failedSkuList[] (LONG)
    ├── failedSkuReasonMap (MAP)
    │   ├── $key (STRING)   → SKU ID
    │   └── $value (STRING) → Fail reason
    └── successPriceOrderList[] (OBJECT[])
        ├── priceOrderSn (STRING)
        └── skuIdList[] (LONG)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Is success |
| errorCode | INTEGER | Error code |
| errorMsg | STRING | Error message |
| result | OBJECT | Return specific information |
| result.successSkuList | LONG[] | SKU list with successfully changed prices |
| result.failedSkuList | LONG[] | SKU list with failed change price |
| result.failedSkuReasonMap | MAP | Reasons for price adjustment failure；**key** 为 SKU ID（字符串），**value** 为失败原因 |
| result.successPriceOrderList | OBJECT[] | List of price orders that request for changing price successfully |

### `successPriceOrderList[]` 元素

| 参数 | 类型 | 说明 |
|------|------|------|
| priceOrderSn | STRING | Price order Sn |
| skuIdList | LONG[] | List of SKUs corresponding to price order |

### `failedSkuReasonMap` 示例

```json
{
  "58224724203875": "Price order pending merchant confirm"
}
```

---

## 示例

```bash
python scripts/global_price_priceorder_change_sku_price.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "rejectSkuPricing": true,
    "changeSkuPriceDTOList": [
      {
        "reason": "Promo",
        "skuChangePriceBaseDTOList": [
          {
            "skuId": 58224724203874,
            "newSupplierPrice": { "amount": "15.99", "currency": "USD" }
          }
        ]
      }
    ]
  }
}'
```

改价后可用 `bg.local.goods.priceorder.query` 核对 `priceAuditList` 中的 `supplierPrice`，或再次调用本接口查看 `successSkuList` / `failedSkuList`。
