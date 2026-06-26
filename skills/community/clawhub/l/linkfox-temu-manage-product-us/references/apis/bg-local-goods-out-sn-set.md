# 商品外部编码（Contribution SKU）— `bg.local.goods.out.sn.set`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_manage_out_sn_set.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.out.sn.set`，业务载荷放在 Body 的 `params` |

**Description:** Set contribution ID for goods（批量设置商品 Contribution SKU / 外部商品编码 `outGoodsSn`）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── modifyList[]          ← 最多 50 条
    │   ├── outGoodsSn
    │   └── goodsId
    └── language
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| modifyList | OBJECT[] | 否 | Contribution SKU modification List，**最多 50 条** |
| language | STRING | 否 | Language |

### `modifyList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| outGoodsSn | STRING | 否 | Contribution SKU（外部商品编码）；**单条长度不超过 40 字符** |
| goodsId | LONG | 否 | Goods id |

> 批量修改时，`modifyList` 中每项通常需同时提供 **`goodsId`** 与目标 **`outGoodsSn`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "modifyList": [
      {
        "goodsId": 123456789,
        "outGoodsSn": "MY-GOODS-001"
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
      { "goodsId": 111, "outGoodsSn": "SKU-A" },
      { "goodsId": 222, "outGoodsSn": "SKU-B" }
    ]
  }
}
```

> **勿**将 `goodsId`、`outGoodsSn` 仅放在 `params` 顶层（须放在 **`request.modifyList[]`** 内，除非网关另有兼容）。

---

## Response（Temu `body` 解析后）

```text
response
├── result
│   └── resultList[]
│       ├── outGoodsSn
│       ├── goodsId
│       ├── modifySuccess
│       └── duplicateGoodsId
├── success
├── errorCode
└── errorMsg
```

| 参数 | 类型 | 说明 |
|------|------|------|
| result | OBJECT | result |
| result.resultList | OBJECT[] | 逐条修改结果列表 |
| success | BOOLEAN | 当前请求是否成功 |
| errorCode | INTEGER | 错误码 |
| errorMsg | STRING | 错误信息 |

### `result.resultList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| outGoodsSn | STRING | Contribution SKU Code Modification List（本次提交的编码） |
| goodsId | LONG | Input Goods id（入参中的商品 ID） |
| modifySuccess | BOOLEAN | Is Modification Successful（该条是否修改成功） |
| duplicateGoodsId | LONG | Duplicate Goods id（若编码重复，冲突的商品 ID） |

> 批量调用时以 **`result.resultList[]`** 中每条 **`modifySuccess`** 为准判断是否成功；`duplicateGoodsId` 有值时表示 `outGoodsSn` 已被其他商品占用。

---

## 与 SKU 外部编码接口区分

| 项 | `bg.local.goods.out.sn.set`（本接口） | `bg.local.goods.sku.out.sn.set` |
|----|--------------------------------------|--------------------------------|
| 粒度 | 商品（goods） | SKU |
| 编码字段 | `outGoodsSn` | `outSkuSn` |
| 列表字段 | `modifyList[]` | 以 Partner 文档为准 |

---

## 示例

```bash
python scripts/us_manage_out_sn_set.py '{
  "accessToken": "TOKEN",
  "request": {
    "modifyList": [
      {
        "goodsId": 123456789,
        "outGoodsSn": "CONTRIBUTION-GOODS-001"
      }
    ]
  }
}'
```
