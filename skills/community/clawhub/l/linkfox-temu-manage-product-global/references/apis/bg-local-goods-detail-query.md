# 商品详情 — `bg.local.goods.detail.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_detail_query.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=9ebbd5d269014322ad4a6c123b1dfdae |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.detail.query`，业务载荷放在 Body 的 `params` |

**Description:** Query local goods detail.

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── language
    ├── goodsId              ← 必填
    └── versionQueryType     ← 查哪一版商品信息
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | Language |
| goodsId | LONG | **是** | goods id |
| versionQueryType | INTEGER | 否 | 拉取哪一版商品信息，默认 **`2`** |

#### `versionQueryType` 枚举

| 值 | 说明 |
|----|------|
| `1` | 拉取**当前审核中**的最新版本商品信息 |
| `2` | 拉取**线上在售**快照（编辑前的 live 版本），**默认** |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "versionQueryType": 2
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "language": "en",
    "goodsId": 123456,
    "versionQueryType": 1
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
    ├── catId
    ├── subStatus
    ├── goodsName
    ├── goodsDesc
    ├── bulletPoints
    ├── customized
    ├── productType
    ├── sourceSiteInfo
    ├── targetSiteInfo[]
    ├── goodsGallery
    ├── importDesignation
    ├── outGoodsSn
    ├── goodsServicePromise
    ├── goodsProperties[]
    ├── goodsTrademark
    ├── goodsSizeChartList
    ├── goodsSizeImage
    ├── goodsOriginInfo
    ├── secondHand
    ├── itemTaxCode
    ├── skuList[]
    └── saveModeStatus
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | 商品详情 |

### `result` 顶层字段（官方）

> **注意**：详情 **Response** 的 `result` 为**扁平结构**（字段直接在 `result` 下），与 **update 请求** 中包在 `request.goodsBasic` 内的层级**不同**。改商品时请按 [partial.update](./bg-local-goods-partial-update.md) / [update](./bg-local-goods-update.md) 的 **Request** 结构组装。

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Product ID |
| catId | LONG | 叶子类目 ID（须与 category version 对应类目树一致） |
| subStatus | INTEGER | Product Draft Status |
| goodsName | STRING | Product Name |
| goodsDesc | STRING | Goods Desc |
| bulletPoints | STRING[] | Product Selling Point |
| customized | BOOLEAN | Whether Customized Product |
| productType | INTEGER | `1` Normal，`2` Custom，`3` Made-to-order |
| sourceSiteInfo | OBJECT | Source site product ID（子字段见 Partner 展开） |
| targetSiteInfo | OBJECT[] | Target site Product ID（子字段见 Partner 展开） |
| goodsGallery | OBJECT | 图库/视频；最多 49 张图 URI、1 个视频 URI，顺序即 Temu 展示顺序，视频在画廊顶部 |
| importDesignation | STRING | 仅 USA：`Imported` / `Made in the USA` / `Made in the USA and Imported` / `Made in the USA or Imported` |
| outGoodsSn | STRING | 外部商品编码，店内唯一，最长 40 字符，勿首尾空格 |
| goodsServicePromise | OBJECT | Merchant Service Information → 结构同 [partial.update §goodsServicePromise](./bg-local-goods-partial-update.md#requestgoodsservicepromise) |
| goodsProperties | OBJECT[] | Product General Attributes（**非** `goodsProperty.goodsProperties`）→ 元素结构同 [partial.update §goodsProperties](./bg-local-goods-partial-update.md#requestgoodsproperty) |
| goodsTrademark | OBJECT | Trademark Information → 同 [partial.update §goodsTrademark](./bg-local-goods-partial-update.md#requestgoodstrademark) |
| goodsSizeChartList | OBJECT | 尺码表（套装可多套）→ 同 [partial.update §goodsSizeChartList](./bg-local-goods-partial-update.md#requestgoodssizechartlist) |
| goodsSizeImage | STRING[] | The URL of the size chart image |
| goodsOriginInfo | OBJECT | Goods Origin Information → 同 [partial.update §goodsOriginInfo](./bg-local-goods-partial-update.md#requestgoodsorigininfo) |
| secondHand | OBJECT | second hand info → 同 [partial.update §secondHand](./bg-local-goods-partial-update.md#requestsecondhand) |
| itemTaxCode | STRING | Tax Code |
| skuList | OBJECT[] | Sku Commit Query List → SKU 元素结构同 [partial.update §skuList](./bg-local-goods-partial-update.md#requestskulist) |
| saveModeStatus | INTEGER | Seller review status of products automatically published to Temu |

### `goodsGallery`（Response 常见子字段）

与编辑请求一致，见 [partial.update §goodsGallery](./bg-local-goods-partial-update.md#goodsbasicgoodsgallery)：`detailVideo`、`goodsCarouselImage`、`detailImage`、`carouselVideo`。

---

## 示例

```bash
# 查线上在售版本（默认 versionQueryType=2）
python scripts/global_manage_detail_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456
  }
}'

# 查审核中最新版本
python scripts/global_manage_detail_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "versionQueryType": 1
  }
}'
```
