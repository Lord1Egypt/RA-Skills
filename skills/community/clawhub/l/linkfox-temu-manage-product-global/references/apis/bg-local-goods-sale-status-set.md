# 商品上下架 — `bg.local.goods.sale.status.set`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_sale_status_set.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.sale.status.set`，业务载荷放在 Body 的 `params` |

**Description:** 设置商品或 SKU 的上架/下架状态。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── goodsId              ← 必填
    ├── onsale               ← 必填（注意小写）
    ├── skuIdList            ← 选填；传入则仅对 SKU 上下架
    └── operationType        ← 选填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | **是** | Goods Id |
| onsale | INTEGER | **是** | 上下架状态：`0` 下架（off-shelf），`1` 上架（on-shelf） |
| skuIdList | LONG[] | 否 | 支持多个 SKU；**若传入，仅对列表内 SKU 执行上下架** |
| operationType | INTEGER | 否 | 操作维度，见下表 |

#### `onsale`

| 值 | 说明 |
|----|------|
| `0` | off-shelf（下架） |
| `1` | on-shelf（上架） |

#### `operationType`

| 值 | 说明 |
|----|------|
| 不传 / `null` | 按**商品**（goods）维度 |
| `1` | 按**商品**（goods）维度 |
| `2` | 按 **SKU** 维度（通常需配合 `skuIdList`） |

> 官方字段名为 **`onsale`**（全小写），勿写成 `onSale`。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "onsale": 1,
    "operationType": 1
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "onsale": 0,
    "skuIdList": [111, 222],
    "operationType": 2
  }
}
```

> **勿**使用旧字段 `onSale`、`bindSiteId`（除非 Partner 另有说明）；上下架以官方 **`request`** 内字段为准。

---

## Response（Temu `body` 解析后）

```text
response
├── success          ← 请求级
├── errorCode
├── errorMsg
└── result
    └── success      ← 业务修改是否成功
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | 当前请求是否成功（True 成功，False 失败） |
| errorCode | INTEGER | 错误码 |
| errorMsg | STRING | 错误信息 |
| result | OBJECT | result |
| result.success | BOOLEAN | Is Modification Successful（上下架修改是否成功） |

> 需同时关注 **`response.success`**（网关/接口调用）与 **`result.success`**（上下架操作结果）。`errorCode` / `errorMsg` 非 0 时以错误信息为准。

---

## 示例

```bash
# 整品上架
python scripts/global_manage_sale_status_set.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "onsale": 1,
    "operationType": 1
  }
}'
```

```bash
# 指定 SKU 下架
python scripts/global_manage_sale_status_set.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "onsale": 0,
    "skuIdList": [58224724203874, 58224724203875],
    "operationType": 2
  }
}'
```
