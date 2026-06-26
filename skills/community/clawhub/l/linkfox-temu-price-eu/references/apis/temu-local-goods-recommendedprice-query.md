# 推荐供货价查询 — `temu.local.goods.recommendedprice.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_price_recommendedprice_query.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=dfff38c23adf498d8a7cd55052bd3648（`sub_menu_code` 请在 Partner EU 后台按 `temu.local.goods.recommendedprice.query` 打开） |
| **网关** | `POST /temu/proxy`，`type`=`temu.local.goods.recommendedprice.query`，业务载荷放在 Body 的 `params` |

**Description:** Support merchants in querying the recommended supply prices（支持商家查询推荐供货价）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── language
    ├── recommendedPriceType    ← 必填
    └── goodsIdList[]           ← 必填，1～100 个
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | Language（语言） |
| recommendedPriceType | INTEGER | **是** | Recommended price type（推荐价类型） |
| goodsIdList | LONG[] | **是** | Search param: list of Goods ID（商品 ID 列表），**列表长度须在 1～100 之间** |

#### `recommendedPriceType`

| 值 | 说明 |
|----|------|
| `10` | Low traffic（低流量） |
| `20` | Restricted traffic（限流/受限流量） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "language": "en",
    "recommendedPriceType": 10,
    "goodsIdList": [123456789, 123456790]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "recommendedPriceType": 20,
    "goodsIdList": [111111111]
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
    └── goodsList[]
        ├── goodsId
        └── skuList[]
            ├── skuId
            └── recommendedSupplyPrice
                ├── amount
                └── currency
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Whether it was successful or not（当前请求是否成功） |
| errorCode | INTEGER | Error code（错误码） |
| errorMsg | STRING | Error message（错误信息） |
| result | OBJECT | Specific information（业务结果） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsList | OBJECT[] | Goods recommended price info list（商品推荐供货价信息列表） |

### `result.goodsList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods ID（商品 ID） |
| skuList | OBJECT[] | SKU recommended price info list（SKU 推荐供货价信息列表） |

### `result.goodsList[].skuList[]`

| 参数 | 类型 | 说明 |
|------|------|------|------|
| skuId | LONG | SKU ID |
| recommendedSupplyPrice | OBJECT | Recommended supply price（推荐供货价） |

### `recommendedSupplyPrice`

| 参数 | 类型 | 说明 |
|------|------|------|
| amount | STRING | Amount（金额） |
| currency | STRING | Currency（币种） |

### 响应示例（结构示意）

```json
{
  "success": true,
  "errorCode": 0,
  "errorMsg": "",
  "result": {
    "goodsList": [
      {
        "goodsId": 123456789,
        "skuList": [
          {
            "skuId": 58224724203874,
            "recommendedSupplyPrice": {
              "amount": "12.99",
              "currency": "EUR"
            }
          }
        ]
      }
    ]
  }
}
```

---

## 与相关接口区分

| 接口 | 场景 |
|------|------|
| `temu.local.goods.recommendedprice.query`（本接口） | 按**已存在商品** `goodsIdList` 查询平台**推荐供货价**（低流量/限流等类型） |
| `temu.local.goods.baseprice.recommend` | 发品/改价前按**类目+规格+站外价**等**估算**推荐基础价 |
| `bg.local.goods.priceorder.query` | 白名单商家查询定价单/报价列表（含 `supplierPrice` 等） |

---

## 示例

```bash
python scripts/eu_price_recommendedprice_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "recommendedPriceType": 10,
    "goodsIdList": [123456789]
  }
}'
```
