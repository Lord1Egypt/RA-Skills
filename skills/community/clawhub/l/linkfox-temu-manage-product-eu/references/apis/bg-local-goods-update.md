# 全量编辑 — `bg.local.goods.update`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_manage_goods_update.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=9ec69ff253ff4403bed421ca114144ef |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.update`，业务载荷放在 Body 的 `params` |

**Description:** Edit all properties (e.g. description, brand, images, attributes) of a product.

> 与 [partial.update](./bg-local-goods-partial-update.md) 共用同一 **`request` 顶层结构**（`goodsBasic` 与 `skuList` 等**同级**）。全量更新须提交**完整**商品数据，且 **`skuList` 必填**；建议先 `bg.local.goods.detail.query` 拉详情再改。  
> `goodsBasic`、`goodsProperty`、`skuList[]` 等**嵌套字段定义**见 [partial.update](./bg-local-goods-partial-update.md) 对应章节（结构一致）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── language
    ├── goodsId                    ← 必填
    ├── goodsBasic
    ├── goodsServicePromise
    ├── goodsProperty
    ├── goodsOriginInfo
    ├── bulletPoints
    ├── goodsDesc
    ├── guideFileInfo
    ├── goodsSizeChartList
    ├── goodsSizeImage
    ├── skuList                    ← 必填（全量）
    ├── goodsTrademark
    ├── goodsVehiclePropertyRelation
    ├── secondHand
    └── modifyId
```

与 **partial.update** 的差异：

| 字段 | partial.update | goods.update（本接口） |
|------|----------------|------------------------|
| `skuList` | 选填，可只传要改的 SKU | **必填**，须传完整 SKU 列表 |
| `saveMode` | 有 | **无**（官方入参未列出） |

### `request` 内字段一览

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | Language |
| goodsId | LONG | **是** | Product Number |
| goodsBasic | OBJECT | 否 | goods basic → [goodsBasic](./bg-local-goods-partial-update.md#goodsbasic) |
| goodsServicePromise | OBJECT | 否 | goods service promise → [partial 文档](./bg-local-goods-partial-update.md#requestgoodsservicepromise) |
| goodsProperty | OBJECT | 否 | goods property → [partial 文档](./bg-local-goods-partial-update.md#requestgoodsproperty) |
| goodsOriginInfo | OBJECT | 否 | Country/region of Origin → [partial 文档](./bg-local-goods-partial-update.md#requestgoodsorigininfo) |
| bulletPoints | STRING[] | 否 | bullet points |
| goodsDesc | STRING | 否 | goods desc |
| guideFileInfo | OBJECT | 否 | guide file info → [partial 文档](./bg-local-goods-partial-update.md#requestguidefileinfo) |
| goodsSizeChartList | OBJECT | 否 | goods size chart list → [partial 文档](./bg-local-goods-partial-update.md#requestgoodssizechartlist) |
| goodsSizeImage | STRING[] | 否 | The URL of the size chart image |
| skuList | OBJECT[] | **是** | sku list → [partial 文档](./bg-local-goods-partial-update.md#requestskulist) |
| goodsTrademark | OBJECT | 否 | goods trademark → [partial 文档](./bg-local-goods-partial-update.md#requestgoodstrademark) |
| goodsVehiclePropertyRelation | OBJECT | 否 | Vehicle data → [partial 文档](./bg-local-goods-partial-update.md#requestgoodsvehiclepropertyrelation) |
| secondHand | OBJECT | 否 | second hand info → [partial 文档](./bg-local-goods-partial-update.md#requestsecondhand) |
| modifyId | STRING | 否 | Product information modification ID；goods 唯一，后续可凭此 ID 查审核结果 |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "goodsBasic": { "goodsName": "Full Title", "goodsGallery": { "goodsCarouselImage": ["https://..."] } },
    "goodsProperty": { "goodsProperties": [{ "vid": 100, "value": "Cotton" }] },
    "skuList": [{ "skuId": 999, "weight": "500", "weightUnit": "g", "length": "10", "width": "10", "height": "10", "volumeUnit": "cm", "images": ["https://..."] }]
  }
}
```

> **勿**使用发品接口字段名（`productName`、`carouselImageUrls`、`productPropertyReqs` 等）。`skuList` 放在 `request` 下，**不要**放进 `goodsBasic`。

---

## Response（Temu `body` 解析后）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result.goodsId | LONG | Product ID |
| result.productType | INTEGER | `1` Normal product，`2` Custom product，`3` Made-to-order product |
| result.skuInfoList | OBJECT[] | Sku information list |

**`result.skuInfoList[]`**

| 参数 | 类型 | 说明 |
|------|------|------|
| skuId | LONG | Sku id |
| outSkuSn | STRING | External sku code |
| specList | OBJECT[] | Specification information |
| specList[].specId | LONG | Specification id |
| specList[].parentSpecId | LONG | Parent Specification id |

---

## 示例

```bash
# 先查详情，再组完整 request
python scripts/eu_manage_detail_query.py '{"accessToken":"TOKEN","goodsId":123456}'

python scripts/eu_manage_goods_update.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "language": "en",
    "goodsBasic": {
      "goodsName": "Updated Full Product",
      "goodsGallery": {
        "goodsCarouselImage": ["https://..."],
        "detailImage": ["https://..."]
      }
    },
    "goodsDesc": "Updated description",
    "skuList": [{
      "skuId": 58224724203874,
      "weight": "500",
      "weightUnit": "g",
      "length": "10",
      "width": "10",
      "height": "10",
      "volumeUnit": "cm",
      "images": ["https://..."]
    }]
  }
}'
```
