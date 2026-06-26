# 库存编辑 — `bg.local.goods.stock.edit`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_manage_stock_edit.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=429ffa60b265451d9421cd5a2004eeef |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.stock.edit`，业务载荷放在 Body 的 `params` |

**Description:** Edit product stock with full-update and diff-update.

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── goodsId                      ← 必填
    ├── stockType                    ← 库存类型，默认 0
    ├── skuStockChangeList[]         ← 增量：stock += stockDiff
    ├── skuStockTargetList[]         ← 全量：覆盖到 stockTarget
    └── requestUniqueKey             ← 幂等键
```

两种改库存方式**二选一**（或按 Partner 文档组合规则）：

| 方式 | 字段 | 说明 |
|------|------|------|
| **增量（diff）** | `skuStockChangeList` | 成功后执行 `stock += stockDiff` |
| **全量（target）** | `skuStockTargetList` | 将 SKU 库存更新为 `stockTarget` |

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | **是** | Goods Id |
| stockType | INTEGER | 否 | Stock type：`0` self ordinary stock（默认），`1` self Pre-sale stock |
| skuStockChangeList | OBJECT[] | 否 | 按 diff 改库存，见下 |
| skuStockTargetList | OBJECT[] | 否 | 按目标值全量改库存，见下 |
| requestUniqueKey | STRING | 否 | Unique Request Id；重复请求将被拒绝 |

### `skuStockChangeList[]`（增量）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| skuId | LONG | **是** | Goods Sku Id |
| stockDiff | INTEGER | **是** | Diff stock；成功则 `stock += stockDiff`（正增负减） |

### `skuStockTargetList[]`（全量）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| skuId | LONG | **是** | Goods Sku Id |
| stockTarget | INTEGER | **是** | 目标库存；SKU 库存将更新为该值 |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "stockType": 0,
    "skuStockChangeList": [
      { "skuId": 58224724203874, "stockDiff": 10 }
    ]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "stockType": 0,
    "skuStockTargetList": [
      { "skuId": 58224724203874, "stockTarget": 100 }
    ],
    "requestUniqueKey": "uuid-once-001"
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
    ├── goodsId
    ├── skuStockEditStatusInfoList[]
    │   ├── skuId
    │   ├── stockEditStatus
    │   ├── errorCode
    │   └── errorMsg
    ├── operateResult          ← 在 result 下，与列表同级
    └── msg                    ← 在 result 下，与列表同级
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | 当前请求是否成功 |
| errorCode | INTEGER | 错误码 |
| errorMsg | STRING | 错误信息 |
| result.goodsId | LONG | Goods Id |
| result.skuStockEditStatusInfoList | OBJECT[] | 各 SKU 改库存状态 |
| result.operateResult | BOOLEAN | Stock change result；`true` 表示成功（**result 顶层**） |
| result.msg | STRING | Result detail information（**result 顶层**） |

### `result.skuStockEditStatusInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| skuId | LONG | Goods Sku Id |
| stockEditStatus | BOOLEAN | `true` 表示该 SKU 库存修改成功 |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |

---

## 示例

### 增量改库存

```bash
python scripts/us_manage_stock_edit.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "skuStockChangeList": [
      { "skuId": 58224724203874, "stockDiff": 5 }
    ]
  }
}'
```

### 全量设为目标库存

```bash
python scripts/us_manage_stock_edit.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "stockType": 1,
    "skuStockTargetList": [
      { "skuId": 58224724203874, "stockTarget": 50 }
    ]
  }
}'
```
