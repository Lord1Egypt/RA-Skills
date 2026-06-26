# 预售状态编辑 — `temu.local.goods.pre.sale.status.edit`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_manage_pre_sale_status_edit.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`temu.local.goods.pre.sale.status.edit`，业务载荷放在 Body 的 `params` |

**Description:** 编辑商品 SKU 的预售状态（开启/关闭预售及预售库存、结束时间等）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── goodsId
    ├── targetPreSaleStatus
    └── skuInfoList[]              ← 必填，最多 100 条
        ├── skuId                  ← 必填
        ├── targetPreSaleStock
        └── preSaleEndTime
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | **是** | Goods Id |
| targetPreSaleStatus | INTEGER | **是** | 目标预售状态，见下表 |
| skuInfoList | OBJECT[] | **是** | SKU info List，**最多 100 条** |

#### `targetPreSaleStatus`

| 值 | 说明 |
|----|------|
| `1` | open（开启预售） |
| `2` | close（关闭预售） |

### `skuInfoList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| skuId | LONG | **是** | Product SKU ID |
| targetPreSaleStock | INTEGER | 否 | Target Pre Sale Stock（目标预售库存；开启预售时通常需填） |
| preSaleEndTime | LONG | 否 | Pre Sale End Time（预售结束时间，时间戳格式以 Partner/实网为准） |

> 商品级 **`targetPreSaleStatus`** 与 SKU 列表 **`skuInfoList`** 同时必填；关闭预售（`2`）时 `targetPreSaleStock` / `preSaleEndTime` 多为选填。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "targetPreSaleStatus": 1,
    "skuInfoList": [
      {
        "skuId": 58224724203874,
        "targetPreSaleStock": 100,
        "preSaleEndTime": 1735689600000
      }
    ]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "targetPreSaleStatus": 2,
    "skuInfoList": [
      { "skuId": 58224724203874 },
      { "skuId": 58224724203875 }
    ]
  }
}
```

> **勿**使用旧字段 `skuPreSaleList`、`productSkuId`、`preSaleStatus`、`preSaleDeliveryDays`。

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    ├── goodsId
    ├── code / msg              ← 商品级结果
    └── skuOperateResultInfoList[]
        ├── skuId
        ├── code
        └── msg
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Whether it was successful or not（请求级） |
| errorCode | INTEGER | Error code |
| errorMsg | STRING | Error message |
| result | OBJECT | Specific information |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods Id |
| code | INTEGER | 主错误码，`0` 表示成功 |
| msg | STRING | 主错误信息 |
| skuOperateResultInfoList | OBJECT[] | SKU operate result info list（逐 SKU 结果） |

### `result.skuOperateResultInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| skuId | LONG | Product SKU ID |
| code | INTEGER | SKU 错误码，`0` 表示该 SKU 成功 |
| msg | STRING | SKU 错误信息 |

> 批量编辑时需检查 **`result.code`**（整体）及每条 **`skuOperateResultInfoList[].code`**（单 SKU）。顶层 **`success`** 为 false 时以 `errorCode` / `errorMsg` 为准。

---

## 示例

```bash
python scripts/us_manage_pre_sale_status_edit.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "targetPreSaleStatus": 1,
    "skuInfoList": [
      {
        "skuId": 58224724203874,
        "targetPreSaleStock": 50,
        "preSaleEndTime": 1735689600000
      }
    ]
  }
}'
```

```bash
# 关闭多个 SKU 预售
python scripts/us_manage_pre_sale_status_edit.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "targetPreSaleStatus": 2,
    "skuInfoList": [
      { "skuId": 58224724203874 },
      { "skuId": 58224724203875 }
    ]
  }
}'
```
