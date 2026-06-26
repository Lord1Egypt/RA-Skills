# SKU 列表搜索（Retrieve）— `temu.local.sku.list.retrieve`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_manage_sku_list_retrieve.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=9775b60761c54bf38022c77c717183a9 |
| **网关** | `POST /temu/proxy`，`type`=`temu.local.sku.list.retrieve`，业务载荷放在 Body 的 `params` |

**Description:** local sku list search（游标分页检索，与 `bg.local.goods.sku.list.query` 的页码分页模型不同）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageSize / pageToken          ← 游标分页（无 pageNo）
    ├── orderField / orderType
    ├── skuSearchType                 ← 必填（STRING 枚举）
    ├── goodsIdList / outGoodsSnList
    ├── skuIdList / outSkuSnList
    ├── catIdList
    ├── goodsName
    ├── goodsCreateTimeFrom / goodsCreateTimeTo
    ├── skuStatusChangeTimeFrom / skuStatusChangeTimeTo
    └── goodsSearchTags
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageSize | INTEGER | 否 | 每页条数，**上限 100**；文档亦提及可按 25 条/页 |
| pageToken | STRING | 否 | 翻页 token；多页结果时传上一页返回的 token 取下一页 |
| orderField | STRING | 否 | 排序属性，如 `create_time`（按创建时间） |
| orderType | INTEGER | 否 | `0` 降序（默认），`1` 升序 |
| skuSearchType | STRING | **是** | SKU 状态筛选，枚举见下表 |
| goodsIdList | STRING[] | 否 | Product ID 搜索，**最多 100** |
| outGoodsSnList | STRING[] | 否 | OutGoodsSn 搜索，**最多 100** |
| skuIdList | STRING[] | 否 | Sku ID 搜索，**最多 200** |
| outSkuSnList | STRING[] | 否 | OutSkuSn 搜索，**最多 200** |
| catIdList | STRING[] | 否 | Category id 搜索，**最多 100** |
| goodsName | STRING | 否 | 商品标题 |
| goodsCreateTimeFrom | LONG | 否 | 商品创建时间起，Unix **毫秒** |
| goodsCreateTimeTo | LONG | 否 | 商品创建时间止，Unix **毫秒** |
| skuStatusChangeTimeFrom | LONG | 否 | SKU 状态变更时间起，Unix **毫秒** |
| skuStatusChangeTimeTo | LONG | 否 | SKU 状态变更时间止，Unix **毫秒** |
| goodsSearchTags | INTEGER[] | 否 | `1` Low traffic，`4` Restricted traffic |

#### `skuSearchType` 枚举（STRING）

| 值 | 说明 |
|----|------|
| `ACTIVE` | 在售/可用 |
| `INACTIVE` | 不可用 |
| `INCOMPLETE` | 未完成 |
| `DRAFT` | 草稿 |
| `DELETED` | 已删除 |

> 与 `bg.local.goods.sku.list.query` 的 **`skuSearchType` 为 INTEGER（2/3）** 不同，勿混用。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "pageSize": 25,
    "skuSearchType": "ACTIVE"
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "pageSize": 50,
    "pageToken": "NEXT_PAGE_TOKEN_FROM_PREVIOUS_RESPONSE",
    "skuSearchType": "ACTIVE",
    "skuIdList": ["58224724203874"],
    "orderField": "create_time",
    "orderType": 0
  }
}
```

---

## Response（Temu `body` 解析后）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Specific information（子字段在 Partner 文档中展开） |

官方 Response 表中 `result` 为可展开对象；**未在提供的片段中列出子字段名**。游标分页接口通常会在 `result` 内返回 **SKU 列表** 与 **下一页 `pageToken`**，具体字段名以 Partner 后台为准。

SKU 列表项字段可能与 [bg.local.goods.sku.list.query](./bg-local-goods-sku-list-query.md) 的 `result.skuList[]` 相近（如 `goodsId`、`skuId`、`skuSn`、`goodsName`、`stock`、`price` 等），但**不可假定完全一致**，以实网返回为准。

---

## 与 `bg.local.goods.sku.list.query` 对比

| 项 | `temu.local.sku.list.retrieve` | `bg.local.goods.sku.list.query` |
|----|-------------------------------|-------------------------------|
| 分页 | `pageToken` + `pageSize` | `pageNo` + `pageSize` |
| `skuSearchType` | STRING（`ACTIVE` 等） | INTEGER（`2`/`3`） |
| ID 列表类型 | 多为 `STRING[]` | 多为 `LONG[]` |
| 必填筛选 | `skuSearchType`（STRING） | `skuSearchType` + `skuStatusFilterType`（INTEGER） |

---

## 示例

```bash
python scripts/us_manage_sku_list_retrieve.py '{
  "accessToken": "TOKEN",
  "request": {
    "pageSize": 25,
    "skuSearchType": "ACTIVE",
    "goodsIdList": ["123456"]
  }
}'
```
