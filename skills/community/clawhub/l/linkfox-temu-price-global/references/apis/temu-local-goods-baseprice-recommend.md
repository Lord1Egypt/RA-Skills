# 推荐基础价/供货价估算 — `temu.local.goods.baseprice.recommend`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_price_baseprice_recommend.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`temu.local.goods.baseprice.recommend`，业务载荷放在 Body 的 `params` |

**Description:** Recommend baseprice（根据类目、规格、站外售价、尺寸重量等信息推荐/估算供货价）。

> **网关鉴权字段**（`type`、`app_key`、`access_token`、`sign`、`timestamp` 等）由本 skill 网关脚本处理，**不要**放进业务脚本的 `params`；业务参数见下方 `request`。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── language (STRING, 否)
    └── supplierPriceEstimateQry (OBJECT, 必填)
        ├── trademarkInfo (OBJECT, 否)
        │   ├── brandId (LONG, 否)
        │   └── trademarkId (LONG, 否)
        ├── goodsBasicInfo (OBJECT, 必填)
        │   ├── catId (LONG, 必填)
        │   ├── taxCode (STRING, 否)
        │   └── costTemplateId (STRING, 否)
        └── supplierPriceEstimateSkuQryList[] (OBJECT[], 必填)
            ├── specIdList[] (LONG[], 必填)
            ├── externPlatformPriceInfo (OBJECT, 必填)
            │   ├── amount (STRING, 否)
            │   └── currency (STRING, 否)
            └── productDimensionsInfo (OBJECT, 否)
                ├── weight (STRING, 否)
                ├── weightUnit (STRING, 否)
                ├── length (STRING, 否)
                ├── width (STRING, 否)
                ├── height (STRING, 否)
                └── dimensionUnit (STRING, 否)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | Language |
| supplierPriceEstimateQry | OBJECT | **是** | Supplier price estimate query |

### `supplierPriceEstimateQry`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| trademarkInfo | OBJECT | 否 | Brand information; if provided, will assist merchants in suggesting more accurate prices. |
| goodsBasicInfo | OBJECT | **是** | Goods basic information |
| supplierPriceEstimateSkuQryList | OBJECT[] | **是** | Supplier price estimate need info (per SKU/spec) |

### `trademarkInfo`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| brandId | LONG | 否 | Brand ID |
| trademarkId | LONG | 否 | Trademark ID |

### `goodsBasicInfo`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| catId | LONG | **是** | The ID of the category of this product. It must be a **leaf category** that corresponds to the category tree type specified in the category_version property. |
| taxCode | STRING | 否 | Product Tax code |
| costTemplateId | STRING | 否 | The ID of the delivery options available for your product, delimited by commas. Sellers can create ship configurations based on business needs; when listing product to create offer, seller selects one ship configuration for the product. The ship configuration will be used to retrieve the valid ship options on the website. |

### `supplierPriceEstimateSkuQryList[]` 元素

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| specIdList | LONG[] | **是** | Specification ID List |
| externPlatformPriceInfo | OBJECT | **是** | The selling price of the product on other platforms |
| productDimensionsInfo | OBJECT | 否 | Product dimensions message |

### `externPlatformPriceInfo`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| amount | STRING | 否 | The selling price of the product on other platforms |
| currency | STRING | 否 | Currency Code |

### `productDimensionsInfo`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| weight | STRING | 否 | The weight of the product. (**Brazil site is mandatory.**) |
| weightUnit | STRING | 否 | The unit of the weight. The weight unit for product in the **United States** is **`lb`** while in other countries it is **`kg`**. (**Brazil site is mandatory.**) |
| length | STRING | 否 | The length of the product. Length should be input with two decimal places. (**Brazil site is mandatory.**) |
| width | STRING | 否 | The width of the product. Width should be input with two decimal places. (**Brazil site is mandatory.**) |
| height | STRING | 否 | The height of the product. Height should be input with two decimal places. (**Brazil site is mandatory.**) |
| dimensionUnit | STRING | 否 | Dimension unit. The dimension unit for product in the **United States** is **`inch`** while in other countries it is **`cm`**. (**Brazil site is mandatory.**) |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "language": "en-US",
    "supplierPriceEstimateQry": {
      "trademarkInfo": {
        "brandId": 10001,
        "trademarkId": 20002
      },
      "goodsBasicInfo": {
        "catId": 12345,
        "taxCode": "TAX001",
        "costTemplateId": "100,101"
      },
      "supplierPriceEstimateSkuQryList": [
        {
          "specIdList": [9001, 9002],
          "externPlatformPriceInfo": {
            "amount": "29.99",
            "currency": "USD"
          },
          "productDimensionsInfo": {
            "weight": "1.20",
            "weightUnit": "lb",
            "length": "10.00",
            "width": "8.00",
            "height": "2.50",
            "dimensionUnit": "inch"
          }
        }
      ]
    }
  }
}
```

> 全球站尺寸/重量单位建议：`weightUnit=lb`、`dimensionUnit=inch`；`goodsBasicInfo.catId` 须为**叶子类目**。

---

## Response（Temu `body` 解析后）

官方 Response 字段表尚未提供；解析顺序与通用 Manage 接口一致：

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    └── （推荐价/估算结果字段以 Partner 文档与实网返回为准）
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Success |
| errorCode | INTEGER | Error code |
| errorMsg | STRING | Error message |
| result | OBJECT | Result payload（具体子字段待官方 Response 表补充） |

---

## 示例

```bash
python scripts/global_price_baseprice_recommend.py '{
  "accessToken": "TOKEN",
  "request": {
    "language": "en-US",
    "supplierPriceEstimateQry": {
      "goodsBasicInfo": { "catId": 12345 },
      "supplierPriceEstimateSkuQryList": [
        {
          "specIdList": [9001],
          "externPlatformPriceInfo": { "amount": "19.99", "currency": "USD" },
          "productDimensionsInfo": {
            "weight": "0.50",
            "weightUnit": "lb",
            "length": "6.00",
            "width": "4.00",
            "height": "1.00",
            "dimensionUnit": "inch"
          }
        }
      ]
    }
  }
}'
```
