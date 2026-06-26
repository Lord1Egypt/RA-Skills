# 商品查询 API — 参数参考

Partner US 菜单 **Product**（`menu_code=fb16b05f7a904765aac4af3a24b87d4a`）。经 `POST /temu/proxy` 转发，网关见 [api.md](./api.md)。

---

## 1. 商品列表查询 — `temu.goods.list.get`

- **sub_menu_code**：`c313f7e3983f407d82d0f7cd88ab5c62`
- **脚本**：`scripts/us_goods_list.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | integer | 是 | 页码，从 1 起 |
| pageSize | integer | 是 | 每页条数 |
| productName | string | 否 | 货品名称（模糊） |
| productSkcIds | array | 否 | SKC ID 列表 |
| skcExtCode | string | 否 | SKC 外部编码 |
| skuExtCodes | array | 否 | SKU 货号列表 |
| cat1Id … cat10Id | integer | 否 | 各级类目 ID 筛选 |
| bindSiteIds | array | 否 | 经营站点 ID 列表 |
| skcSiteStatus | integer | 否 | SKC 加站点状态：0 未加入，1 已加入 |
| matchJitMode | boolean | 否 | 是否 JIT 模式 |
| quickSellAgtSignStatus | integer | 否 | 快速售卖协议：0 未签，1 已签 |
| supportPersonalization | integer | 否 | 是否支持定制品 |
| createdAtStart | string | 否 | 创建时间起（`YYYY-MM-DD HH:mm:ss`） |
| createdAtEnd | string | 否 | 创建时间止 |

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| data | array | 商品列表，元素见 `entity.Goods` |
| totalCount | integer | 总条数 |

#### `data[]` 主要字段

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | integer | 货品 ID |
| productSkcId | integer | SKC ID |
| productName | string | 货品名称 |
| extCode | string | SKC 外部编码 |
| mainImageUrl | string | 主图 |
| leafCat | object | 叶子类目 `{ catId, catName }` |
| skcSiteStatus | integer | 站点上架状态 |
| productSkuSummaries | array | SKU 摘要（库存、规格等） |

### 示例

```bash
python scripts/us_goods_list.py '{
  "accessToken": "TOKEN",
  "page": 1,
  "pageSize": 20
}'
```

---

## 2. 商品详情查询 — `temu.goods.detail.get`

- **sub_menu_code**：`7ce116fe6b87443ba2a5320b25bf2b20`
- **脚本**：`scripts/us_goods_detail.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productId | integer | 是 | 货品 ID |

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | integer | 货品 ID |
| productName | string | 商品名称 |
| categories | object | 类目树 cat1…cat10、leafCat |
| goodsLayerDecorationList | array | 商详装饰楼层 |
| productWhExtAttr | object | 仓配扩展（如产地 `productOrigin`） |

### 示例

```bash
python scripts/us_goods_detail.py '{
  "accessToken": "TOKEN",
  "productId": 604269868588112
}'
```
