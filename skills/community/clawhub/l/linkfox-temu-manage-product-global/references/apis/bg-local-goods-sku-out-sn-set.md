# SKU 外部编码（Contribution SKU）— `bg.local.goods.sku.out.sn.set`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_sku_out_sn_set.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.sku.out.sn.set`，业务载荷放在 Body 的 `params` |

**Description:** Set contribution ID for SKU（批量设置 SKU 的 Contribution SKU / 外部 SKU 编码 `outSkuSn`）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── modifyList[]          ← Contribution SKU 修改列表
    │   ├── goodsId
    │   ├── outSkuSn
    │   └── skuId
    └── language
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| modifyList | OBJECT[] | 否 | Contribution SKU 修改列表；每项为一条 SKU 的外部编码设置 |
| language | STRING | 否 | Language（语言） |

### `modifyList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | 否 | Goods Id（商品 ID） |
| outSkuSn | STRING | 否 | Contribution SKU（外部 SKU 编码 / 贡献 SKU）；**单条编码字符长度不得超过 40 字符** |
| skuId | LONG | 否 | Goods Sku Id（商品 SKU ID） |

> 批量修改时，`modifyList` 中每项通常需同时提供 **`goodsId`**、**`skuId`** 与目标 **`outSkuSn`**，以唯一定位要修改的 SKU。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "modifyList": [
      {
        "goodsId": 123456789,
        "skuId": 58224724203874,
        "outSkuSn": "MY-SKU-001"
      }
    ],
    "language": "en"
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "modifyList": [
      { "goodsId": 111, "skuId": 1001, "outSkuSn": "SKU-A" },
      { "goodsId": 111, "skuId": 1002, "outSkuSn": "SKU-B" }
    ]
  }
}
```

> **勿**将 `goodsId`、`skuId`、`outSkuSn` 仅放在 `params` 顶层（须放在 **`request.modifyList[]`** 内，除非网关另有兼容）。

---

## Response（Temu `body` 解析后）

```text
response
├── result
│   └── resultList[]
│       ├── goodsId
│       ├── outSkuSn
│       ├── modifySuccess
│       ├── duplicateSkuId
│       ├── duplicateGoodsId
│       └── skuId
├── success
├── errorCode
└── errorMsg
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| result | OBJECT | result（业务结果对象） |
| success | BOOLEAN | 当前请求是否成功：成功返回 `true`，否则返回 `false` |
| errorCode | INTEGER | 错误码：用于对照下方错误码表，定位对应解决方案 |
| errorMsg | STRING | 错误信息：与 `errorCode` 对应的反馈内容 |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| resultList | OBJECT[] | resultList（逐条修改结果列表） |

### `result.resultList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods Id（商品 ID） |
| outSkuSn | STRING | Contribution SKU Code Modification List（本次提交/回显的外部 SKU 编码） |
| modifySuccess | BOOLEAN | Is Modification Successful（该条是否修改成功） |
| duplicateSkuId | LONG | Duplicate goodsId（官方字段名；若 `outSkuSn` 重复，冲突的 SKU ID，以实网返回为准） |
| duplicateGoodsId | LONG | Duplicate skuId（官方字段名；若 `outSkuSn` 重复，冲突的商品 ID，以实网返回为准） |
| skuId | LONG | Goods Sku Id（商品 SKU ID） |

> 批量调用时以 **`result.resultList[]`** 中每条 **`modifySuccess`** 为准判断是否成功；`duplicateSkuId` / `duplicateGoodsId` 有值时表示 `outSkuSn` 已被其他 SKU 或商品占用（含义以 Partner 实网返回为准）。

---

## 与商品外部编码接口区分

| 项 | `bg.local.goods.out.sn.set` | `bg.local.goods.sku.out.sn.set`（本接口） |
|----|------------------------------|------------------------------------------|
| 粒度 | 商品（goods） | SKU |
| 编码字段 | `outGoodsSn` | `outSkuSn` |
| 定位字段 | `goodsId` | `goodsId` + `skuId` |
| 列表字段 | `modifyList[]` | `modifyList[]` |

---

## 示例

```bash
python scripts/global_manage_sku_out_sn_set.py '{
  "accessToken": "TOKEN",
  "request": {
    "modifyList": [
      {
        "goodsId": 123456789,
        "skuId": 58224724203874,
        "outSkuSn": "CONTRIBUTION-SKU-001"
      }
    ]
  }
}'
```
