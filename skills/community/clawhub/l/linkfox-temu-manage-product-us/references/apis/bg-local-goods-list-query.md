# 商品列表 — `bg.local.goods.list.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_manage_list_query.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=d2a836cf1711473ba1f83597a1b52fb0 |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.list.query`，业务载荷放在 Body 的 `params` |

**Description:** 分页查询商品列表（页码分页，与 `temu.local.goods.list.retrieve` 的游标分页不同）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageNo / pageSize              ← 均必填
    ├── orderField / orderType
    ├── goodsSearchType                ← 必填（INTEGER 枚举）
    ├── goodsStatusFilterType          ← 必填（新版）
    ├── goodsSubStatusFilterType       ← 选填（新版）
    ├── searchText / statusFilterType
    ├── crtFrom / crtTo
    ├── goodsIdList / catIdList
    ├── goodsStatusChangeTimeFrom / goodsStatusChangeTimeTo
    └── goodsSearchTags
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNo | INTEGER | **是** | 页码，用于分页 |
| pageSize | INTEGER | **是** | 每页条数，**上限 100** |
| orderField | STRING | 否 | 排序字段：`goodsId`、`createTime`、`goodsName`、`outGoodsSn`、`quantity`、`price`；默认按创建时间 |
| orderType | INTEGER | 否 | `0` 降序（默认），`1` 升序 |
| goodsSearchType | INTEGER | **是** | 商品状态筛选，见下表 |
| searchText | STRING | 否 | 搜索文本，支持按 **goodsName** 或 **goodsId** |
| statusFilterType | INTEGER | 否 | 子状态筛选类型，参见 Partner「Goods status description」 |
| crtFrom | LONG | 否 | 创建时间起，13 位毫秒时间戳 |
| crtTo | LONG | 否 | 创建时间止，13 位毫秒时间戳 |
| goodsIdList | LONG[] | 否 | Goods Id 列表 |
| catIdList | LONG[] | 否 | 类目 ID 列表，支持叶子/非叶子类目，可批量 |
| goodsStatusFilterType | INTEGER | **是** | 商品状态筛选（**新版字段**），具体取值见 Partner 文档 |
| goodsSubStatusFilterType | INTEGER | 否 | 商品子状态筛选（**新版字段**） |
| goodsStatusChangeTimeFrom | LONG | 否 | 商品状态变更时间起（时间戳） |
| goodsStatusChangeTimeTo | LONG | 否 | 商品状态变更时间止（时间戳） |
| goodsSearchTags | INTEGER[] | 否 | `1` Low traffic，`4` Restricted traffic |

#### `goodsSearchType` 枚举

| 值 | 说明 |
|----|------|
| `1` | Available / off the shelf（在售/下架） |
| `4` | Not yet published（尚未发布） |
| `5` | Draft（草稿） |
| `6` | Deleted（已删除） |

> 官方同时标记 **`goodsSearchType`** 与 **`goodsStatusFilterType`** 为必填；调用时需同时传入（`goodsStatusFilterType` 取值以 Partner「Goods status description」为准）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 20,
    "goodsSearchType": 1,
    "goodsStatusFilterType": 0,
    "searchText": "keyword"
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 50,
    "goodsSearchType": 1,
    "goodsStatusFilterType": 0,
    "goodsIdList": [123456789],
    "catIdList": [1001, 1002],
    "orderField": "createTime",
    "orderType": 0,
    "crtFrom": 1704067200000,
    "crtTo": 1735689600000
  }
}
```

> **勿**使用旧字段名 `createTimeFrom`/`createTimeTo`（官方为 **`crtFrom`/`crtTo`**）；**勿**用单值 `catId`（官方为 **`catIdList`**）。

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    ├── pageNo
    ├── total
    └── goodsList[]
        ├── goodsId / goodsName / specName / thumbUrl
        ├── outGoodsSn / status4VO / subStatus4VO
        ├── currency / marketPrice / listPrice / price / retailPrice
        ├── outSkuSnList / skuIdList / skuInfoList
        ├── quantity / crtTime / goodsStatusChangeTime
        ├── catId / brandId / trademarkId
        ├── costTemplateId / shipmentLimitSecond
        ├── goodsShowSubStatus / lowTrafficTag / restrictedTrafficTag
        └── ...
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | 当前请求是否成功 |
| errorCode | INTEGER | 错误码 |
| errorMsg | STRING | 错误信息 |
| result | OBJECT | result |
| result.pageNo | INTEGER | 结果集当前页码 |
| result.total | LONG | 结果集总条数 |
| result.goodsList | OBJECT[] | 商品列表 |

### `result.goodsList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | 商品唯一 ID |
| goodsName | STRING | 商品标题 |
| specName | STRING | 规格/类型 |
| thumbUrl | STRING | 缩略图 URL |
| outGoodsSn | STRING | 外部商品编码 |
| status4VO | INTEGER | 商品状态（如 `1` 在售、`4` 未发布等） |
| subStatus4VO | INTEGER | 商品子状态（含义依业务） |
| currency | STRING | 价格币种 |
| marketPrice | LONG | 市场价/建议零售价 |
| listPrice | OBJECT | 市场价/建议零售价（结构化，子字段见 Partner 展开） |
| price | STRING | 售价/零售价 |
| retailPrice | OBJECT | 售价/零售价（结构化，子字段见 Partner 展开） |
| outSkuSnList | STRING[] | 外部 SKU 编码列表 |
| skuIdList | LONG[] | SKU ID 列表 |
| quantity | INTEGER | 库存数量 |
| crtTime | LONG | 创建时间，Unix **秒** |
| goodsStatusChangeTime | STRING | 商品状态变更时间（时间戳格式） |
| catId | LONG | 类目 ID |
| brandId | LONG | 品牌 ID |
| trademarkId | LONG | 商标 ID |
| costTemplateId | STRING | 配送选项 ID，逗号分隔 |
| shipmentLimitSecond | LONG | 接单至可发货间隔（秒） |
| skuInfoList | OBJECT[] | SKU 信息列表（子字段见 Partner 展开） |
| goodsShowSubStatus | INTEGER | 商品展示子状态（**新版字段**） |
| lowTrafficTag | INTEGER | `1` low traffic，`2` not low traffic |
| restrictedTrafficTag | INTEGER | `1` restricted traffic，`2` not restricted traffic |

> 响应中状态字段为 **`status4VO` / `subStatus4VO`**，勿写成 `status` / `subStatus`。`listPrice`、`retailPrice`、`skuInfoList` 在 Partner 文档中为可展开对象，子字段以官方为准。

---

## 与 `temu.local.goods.list.retrieve` 对比

| 项 | `bg.local.goods.list.query` | `temu.local.goods.list.retrieve` |
|----|----------------------------|----------------------------------|
| 分页 | `pageNo` + `pageSize`（均必填） | `pageToken` + `pageSize` |
| 主状态筛选 | `goodsSearchType`（INTEGER 1/4/5/6） | 游标检索侧字段以 Partner 为准 |
| 新版状态 | `goodsStatusFilterType`（必填） | — |
| 创建时间 | `crtFrom` / `crtTo` | 多为 `goodsCreateTimeFrom` / `To` |
| ID 列表 | `goodsIdList`（LONG[]） | 多为 STRING[] |

---

## 示例

```bash
python scripts/us_manage_list_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 20,
    "goodsSearchType": 1,
    "goodsStatusFilterType": 0
  }
}'
```
