# 定价单列表查询 — `bg.local.goods.priceorder.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_price_priceorder_query.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=dfff38c23adf498d8a7cd55052bd3648（`sub_menu_code` 请在 Partner EU 后台按 `bg.local.goods.priceorder.query` 打开） |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.priceorder.query`，业务载荷放在 Body 的 `params` |

**Description:** Support merchants within the **white list** to query the price offer list（支持白名单商家查询定价单/报价列表）。

> 须在 Temu 白名单内方可调用；非白名单店铺可能返回业务错误。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── page
    ├── size
    ├── priceOrderType
    ├── priceOrderSubType
    ├── goodsName
    ├── goodsId
    ├── priceOrderSnList[]
    ├── orderBy
    ├── orderByType
    ├── goodsCreateTimeFrom / goodsCreateTimeTo
    ├── priceOrderCreateTimeFrom / priceOrderCreateTimeTo
    ├── goodsIdList[]
    └── status
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | INTEGER | 否 | Page number（页码） |
| size | INTEGER | 否 | Page size（每页条数），**须小于 100** |
| priceOrderType | INTEGER | 否 | Pricing type（定价单类型）；**默认**为定价评估报价 |
| priceOrderSubType | INTEGER | 否 | price order sub type（定价单子类型） |
| goodsName | STRING | 否 | Search param: goodsName（按商品名搜索） |
| goodsId | STRING | 否 | Search param: goodsId（按商品 ID 搜索） |
| priceOrderSnList | STRING[] | 否 | search param: list of price order sn（定价单编号列表） |
| orderBy | STRING | 否 | 排序字段；**默认** `order_create_time` |
| orderByType | INTEGER | 否 | 排序方向；**默认** `0`（DESC） |
| goodsCreateTimeFrom | LONG | 否 | Search param: The starting time of goods creation（商品创建起始时间） |
| goodsCreateTimeTo | LONG | 否 | Search param: The end time of goods creation（商品创建结束时间） |
| priceOrderCreateTimeFrom | LONG | 否 | Search param: The starting time of price order creation（定价单创建起始时间） |
| priceOrderCreateTimeTo | LONG | 否 | Search param: The end time of price order creation（定价单创建结束时间） |
| goodsIdList | STRING[] | 否 | goodsIdList（商品 ID 列表） |
| status | INTEGER | 否 | price order status（定价单状态） |

#### `priceOrderType`

| 值 | 说明 |
|----|------|
| 不传 / 默认 | offer for pricing assessment（定价评估报价，默认） |
| `1` | offer for pricing assessment（定价评估报价） |
| `2` | offer for pricing opportunities or modification（定价机会或改价报价） |

#### `priceOrderSubType`

| 值 | 说明 |
|----|------|
| `2002` | base price increase invitations（基础价上调邀请） |
| `2003` | sales boost（销量提升） |

#### `orderBy`

| 值 | 说明 |
|----|------|
| `goods_create_time` | 按商品创建时间排序 |
| `order_create_time` | 按定价单创建时间排序（**默认**） |

#### `orderByType`

| 值 | 说明 |
|----|------|
| `0` | DESC（降序，**默认**） |
| `1` | ASC（升序） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "page": 1,
    "size": 20,
    "priceOrderType": 1,
    "orderBy": "order_create_time",
    "orderByType": 0
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "page": 1,
    "size": 50,
    "goodsId": "123456789",
    "priceOrderSubType": 2002,
    "status": 1
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "priceOrderSnList": ["PO-SN-001", "PO-SN-002"],
    "goodsIdList": ["111", "222"]
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    ├── pageNum
    ├── total
    └── priceAuditList[]          ← Price offer list
        ├── priceOrderId
        ├── goodsId
        ├── pricingType
        ├── specName[]
        ├── skuIdList[]
        ├── status
        ├── suggestSupplierPrice
        ├── targetSupplierPrice
        ├── sourceSupplierPrice
        ├── supplierPrice
        ├── reason
        ├── rejectTypeDesc
        ├── priceCommitId
        └── priceCommitVersion
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Is success（当前请求是否成功） |
| errorCode | INTEGER | Error code（错误码） |
| errorMsg | STRING | Error message（错误信息） |
| result | OBJECT | Return specific information（业务结果） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| pageNum | INTEGER | Page number（当前页码） |
| total | LONG | Total（总记录数） |
| priceAuditList | OBJECT[] | Price offer list（定价单/报价列表） |

### `result.priceAuditList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| priceOrderId | LONG | Pricing ID（定价单 ID） |
| goodsId | LONG | Goods ID（商品 ID） |
| pricingType | INTEGER | pricing type，见下表 |
| specName | STRING[] | Specification Name（规格名称列表） |
| skuIdList | LONG[] | SKU id list（SKU ID 列表） |
| status | INTEGER | Status of price offer（报价/定价单状态） |
| suggestSupplierPrice | OBJECT | Reference Base Price（参考基础价/建议供货价） |
| targetSupplierPrice | OBJECT | New Base Price（目标新基础价） |
| sourceSupplierPrice | OBJECT | source supplier price（原供货价） |
| supplierPrice | OBJECT | Final Base Price（最终基础价/供货价） |
| reason | STRING | Rejection Reason（拒绝原因） |
| rejectTypeDesc | STRING | Rejection Type Description（拒绝类型描述） |
| priceCommitId | LONG | Price commit id（价格提交 ID） |
| priceCommitVersion | INTEGER | Price commit version（价格提交版本） |

#### `pricingType`（响应字段，与入参 `priceOrderType` 枚举略有差异）

| 值 | 说明 |
|----|------|
| `0` | offer for pricing assessment（定价评估报价） |
| `1` | offer for pricing opportunities（定价机会报价） |
| `2` | offer for pricing modification（改价报价） |

### 价格对象结构（`suggestSupplierPrice` / `targetSupplierPrice` / `sourceSupplierPrice` / `supplierPrice`）

| 参数 | 类型 | 说明 |
|------|------|------|
| amount | STRING | Amount（金额） |
| currency | STRING | Currency Type（币种） |

### 响应示例（结构示意）

```json
{
  "success": true,
  "errorCode": 0,
  "errorMsg": "",
  "result": {
    "pageNum": 1,
    "total": 2,
    "priceAuditList": [
      {
        "priceOrderId": 90001,
        "goodsId": 123456789,
        "pricingType": 0,
        "specName": ["Color: Red", "Size: M"],
        "skuIdList": [58224724203874],
        "status": 1,
        "suggestSupplierPrice": { "amount": "12.00", "currency": "EUR" },
        "targetSupplierPrice": { "amount": "10.99", "currency": "EUR" },
        "sourceSupplierPrice": { "amount": "13.50", "currency": "EUR" },
        "supplierPrice": { "amount": "10.99", "currency": "EUR" },
        "reason": "",
        "rejectTypeDesc": "",
        "priceCommitId": 80001,
        "priceCommitVersion": 1
      }
    ]
  }
}
```

---

## 与相关接口区分

| 接口 | 场景 |
|------|------|
| `bg.local.goods.priceorder.query`（本接口） | **白名单**商家分页查询定价单/报价列表 |
| `bg.local.goods.priceorder.change.sku.price` | **白名单**商家批量修改 SKU 基础价 |
| `linkfox-temu-add-product-us` `temu.goods.price.list.get` | 半托管侧按 `productSkuIds` 查供货价 |

---

## 示例

```bash
python scripts/eu_price_priceorder_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "page": 1,
    "size": 20,
    "priceOrderType": 1,
    "orderBy": "order_create_time",
    "orderByType": 0
  }
}'
```
