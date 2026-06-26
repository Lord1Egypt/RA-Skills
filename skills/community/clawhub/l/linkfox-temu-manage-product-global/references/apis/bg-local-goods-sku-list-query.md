# SKU 列表 / Variants — `bg.local.goods.sku.list.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_sku_list_query.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=87a0d398417049bfbeb5b190f68a22b2 |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.sku.list.query`，业务载荷放在 Body 的 `params` |

**Description:** Get sku list, as well as get Variants（分页 SKU 列表查询，**不是**按单个 `goodsId` 查全量 SKU）。

> **勿**与 `bg.local.goods.detail.query` 的 `result.skuList`（单商品详情内 SKU）混淆；本接口为**列表检索**接口。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageNo / pageSize
    ├── orderField / orderType
    ├── skuSearchType          ← 必填
    ├── skuStatusFilterType    ← 必填（新版）
    ├── searchText
    ├── statusFilterType
    ├── crtFrom / crtTo
    ├── skuIdList / catIdList
    ├── skuSubStatusFilterType
    ├── skuStatusChangeTimeFrom / skuStatusChangeTimeTo
    └── goodsSearchTags
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNo | INTEGER | 否 | Page number |
| pageSize | INTEGER | 否 | Page size，**每页最多 100** |
| orderField | STRING | 否 | 排序：`goodsId`、`createTime`、`goodsName`、`outGoodsSn`、`quantity`、`price`；默认按创建时间 |
| orderType | INTEGER | 否 | `0` 降序（默认），`1` 升序 |
| skuSearchType | INTEGER | **是** | Product status：`2` Available for sale，`3` Not available for sale |
| searchText | STRING | 否 | 搜索：`goodsName`、`goodsId` 或 SKU code |
| statusFilterType | INTEGER | 否 | Subtype filter type |
| crtFrom | LONG | 否 | 创建时间起，13 位毫秒时间戳 |
| crtTo | LONG | 否 | 创建时间止，13 位毫秒时间戳 |
| skuIdList | LONG[] | 否 | sku id list |
| catIdList | LONG[] | 否 | 类目 ID 列表，支持叶子/非叶子，可批量 |
| skuStatusFilterType | INTEGER | **是** | Product status filter（**新版字段**） |
| skuSubStatusFilterType | INTEGER | 否 | Product sub-status filter（新版字段） |
| skuStatusChangeTimeFrom | LONG | 否 | SKU 状态变更时间起（时间戳） |
| skuStatusChangeTimeTo | LONG | 否 | SKU 状态变更时间止（时间戳） |
| goodsSearchTags | INTEGER[] | 否 | `1` Low traffic，`4` Restricted traffic |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 20,
    "skuSearchType": 2,
    "skuStatusFilterType": 0,
    "searchText": "keyword"
  }
}
```

> **勿**使用旧文档仅传 `goodsId` 的方式；官方入参为**分页 + 筛选**模型，无单独必填 `goodsId`（可用 `searchText` 或 `skuIdList` 定位）。

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
    └── skuList[]
        ├── goodsName / specName / thumbUrl
        ├── goodsId / skuId / skuSn
        ├── stock / price / retailPrice
        ├── crtTime / status4VO / subStatus4VO
        ├── goodsIsOnSale / currency
        ├── skuStatusChangeTime
        ├── volumeInfo / weightInfo
        ├── skuShowSubStatus4VO
        ├── specList[]
        ├── lowTrafficTag / restrictedTrafficTag
        └── ...
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Current request success status |
| errorCode | INTEGER | Error code |
| errorMsg | STRING | Error message |
| result.pageNo | INTEGER | Page number |
| result.total | LONG | Total count |
| result.skuList | OBJECT[] | Product list result |

### `result.skuList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsName | STRING | Product title |
| specName | STRING | Specification |
| thumbUrl | STRING | Preview image URL |
| goodsId | LONG | Product ID |
| skuId | LONG | SKU ID |
| skuSn | STRING | SKU code |
| stock | INTEGER | Stock quantity |
| price | STRING | Price |
| retailPrice | OBJECT | The selling price or retail price（子字段见 Partner 展开） |
| crtTime | LONG | Creation time in **seconds** |
| status4VO | INTEGER | Product status |
| subStatus4VO | INTEGER | Product sub-status |
| goodsIsOnSale | INTEGER | Product availability status |
| currency | STRING | Currency information |
| skuStatusChangeTime | STRING | SKU change time, timestamp format |
| volumeInfo | OBJECT | Product volume（子字段见 Partner 展开） |
| weightInfo | OBJECT | Product weight（子字段见 Partner 展开） |
| skuShowSubStatus4VO | INTEGER | Product sub-status filter（新版字段） |
| specList | OBJECT[] | spec list（规格列表，子字段见 Partner 展开） |
| lowTrafficTag | INTEGER | `1` low traffic，`2` not low traffic |
| restrictedTrafficTag | INTEGER | `1` restricted traffic，`2` not restricted traffic |

---

## 示例

```bash
python scripts/global_manage_sku_list_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 20,
    "skuSearchType": 2,
    "skuStatusFilterType": 0,
    "orderField": "createTime",
    "orderType": 0
  }
}'
```

```bash
# 按 SKU ID 列表筛选
python scripts/global_manage_sku_list_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 50,
    "skuSearchType": 2,
    "skuStatusFilterType": 0,
    "skuIdList": [58224724203874, 58224724203875]
  }
}'
```
