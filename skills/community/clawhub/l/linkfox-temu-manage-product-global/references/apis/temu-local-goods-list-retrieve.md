# 商品列表搜索（Retrieve）— `temu.local.goods.list.retrieve`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_goods_list_retrieve.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=9775b60761c54bf38022c77c717183a9 |
| **网关** | `POST /temu/proxy`，`type`=`temu.local.goods.list.retrieve`，业务载荷放在 Body 的 `params` |

**Description:** local goods list search（游标分页检索，与 `bg.local.goods.list.query` 的页码分页模型不同）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageSize / pageToken          ← 游标分页（无 pageNo）
    ├── orderField / orderType
    ├── goodsSearchType               ← 必填（STRING 枚举）
    ├── goodsIdList / outGoodsSnList
    ├── skuIdList / outSkuSnList
    ├── catIdList
    ├── goodsName
    ├── goodsCreateTimeFrom / goodsCreateTimeTo
    ├── goodsStatusChangeTimeFrom / goodsStatusChangeTimeTo
    └── goodsSearchTags
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageSize | INTEGER | 否 | 每页条数，**上限 100**；文档亦提及可按 25 条/页 |
| pageToken | STRING | 否 | 翻页 token；多页结果时传上一页返回的 token 取下一页 |
| orderField | STRING | 否 | 排序属性，如 `create_time`（按创建时间） |
| orderType | INTEGER | 否 | `0` 降序（默认），`1` 升序 |
| goodsSearchType | STRING | **是** | 商品状态筛选，枚举见下表 |
| goodsIdList | STRING[] | 否 | Product ID，支持批量，**最多 100** |
| outGoodsSnList | STRING[] | 否 | Out Goods Sn，支持批量，**最多 100** |
| skuIdList | STRING[] | 否 | Sku ID，支持批量，**最多 200** |
| outSkuSnList | STRING[] | 否 | OutSkuSn 搜索，**最多 200** |
| catIdList | STRING[] | 否 | Category id 搜索，**最多 100** |
| goodsName | STRING | 否 | 商品标题 |
| goodsCreateTimeFrom | LONG | 否 | 商品创建时间起，Unix **毫秒** |
| goodsCreateTimeTo | LONG | 否 | 商品创建时间止，Unix **毫秒** |
| goodsStatusChangeTimeFrom | LONG | 否 | 商品状态变更时间起，Unix **毫秒** |
| goodsStatusChangeTimeTo | LONG | 否 | 商品状态变更时间止，Unix **毫秒** |
| goodsSearchTags | INTEGER[] | 否 | `1` Low traffic，`4` Restricted traffic |

#### `goodsSearchType` 枚举（STRING）

| 值 | 说明 |
|----|------|
| `ALL` | ALL = Active + InActive |
| `ACTIVE` | Active（在售/可用） |
| `INACTIVE` | InActive（不可用） |
| `INCOMPLETE` | Incomplete（未完成） |
| `DRAFT` | Draft（草稿） |
| `DELETED` | Deleted（已删除） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "pageSize": 25,
    "goodsSearchType": "ACTIVE"
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "pageSize": 50,
    "pageToken": "NEXT_PAGE_TOKEN_FROM_PREVIOUS_RESPONSE",
    "goodsSearchType": "ALL",
    "goodsIdList": ["123456789"],
    "orderField": "create_time",
    "orderType": 0
  }
}
```

> **勿**使用旧字段 `page`、`keyword`、`goodsStatus`、`goodsIds`、`sortField`/`sortOrder`；官方为 **`pageToken`** + **`goodsSearchType`**（STRING）+ **`request`** 包装。

---

## Response（Temu `body` 解析后）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Specific information（子字段在 Partner 文档中展开） |

官方 Response 表中 **`result` 未在提供的片段中展开**。游标分页列表接口通常会在 `result` 内返回 **商品列表** 与 **下一页 `pageToken`**，具体字段名以 Partner 后台为准。

列表项字段可能与 [bg.local.goods.list.query](./bg-local-goods-list-query.md) 的 `result.goodsList[]` 相近，但**不可假定完全一致**（尤其 ID 类型多为 STRING、状态字段命名可能不同），以实网返回为准。

---

## 与 `bg.local.goods.list.query` 对比

| 项 | `temu.local.goods.list.retrieve` | `bg.local.goods.list.query` |
|----|----------------------------------|-----------------------------|
| 分页 | `pageToken` + `pageSize` | `pageNo` + `pageSize`（均必填） |
| 主状态筛选 | `goodsSearchType`（STRING：`ALL`/`ACTIVE`/…） | `goodsSearchType`（INTEGER 1/4/5/6） |
| 新版状态 | — | `goodsStatusFilterType`（必填） |
| 创建时间 | `goodsCreateTimeFrom` / `To`（毫秒） | `crtFrom` / `crtTo`（毫秒） |
| 状态变更时间 | `goodsStatusChangeTimeFrom` / `To` | `goodsStatusChangeTimeFrom` / `To` |
| ID 列表 | `goodsIdList`（STRING[]） | `goodsIdList`（LONG[]） |
| 搜索 | `goodsName` | `searchText`（goodsName 或 goodsId） |

## 与 `temu.local.sku.list.retrieve` 对比

| 项 | `temu.local.goods.list.retrieve` | `temu.local.sku.list.retrieve` |
|----|----------------------------------|-------------------------------|
| 检索粒度 | 商品（goods） | SKU |
| 必填状态字段 | `goodsSearchType` | `skuSearchType` |
| 状态变更时间 | `goodsStatusChangeTimeFrom` / `To` | `skuStatusChangeTimeFrom` / `To` |
| `goodsSearchType` 含 `ALL` | 是 | SKU 侧为 ACTIVE/INACTIVE 等（无 ALL） |

---

## 示例

```bash
python scripts/global_manage_goods_list_retrieve.py '{
  "accessToken": "TOKEN",
  "request": {
    "pageSize": 25,
    "goodsSearchType": "ACTIVE",
    "goodsName": "keyword"
  }
}'
```

```bash
# 翻页
python scripts/global_manage_goods_list_retrieve.py '{
  "accessToken": "TOKEN",
  "request": {
    "pageSize": 25,
    "pageToken": "TOKEN_FROM_LAST_PAGE",
    "goodsSearchType": "ALL"
  }
}'
```
