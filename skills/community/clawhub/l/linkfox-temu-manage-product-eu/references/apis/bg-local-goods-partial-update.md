# 部分字段编辑 — `bg.local.goods.partial.update`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_manage_partial_update.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=f25a3d4a2a884c97ada8944250fd176e |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.partial.update`，业务载荷放在 Body 的 `params` |

**Description:** Edit a subset of the product properties (e.g. description, brand, images, attributes).

> 仅传需要修改的字段。官方请求体为 **`request` 对象**；`goodsServicePromise`、`goodsProperty`、`skuList` 等与 **`goodsBasic` 同级**，均在 `request` 下，**不要**把这些字段塞进 `goodsBasic`。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── language
    ├── goodsId                    ← 必填
    ├── goodsBasic                 ← 仅基础信息（名称/图库/进口标识）
    ├── goodsServicePromise        ← 与 goodsBasic 同级
    ├── goodsProperty
    ├── goodsOriginInfo
    ├── bulletPoints
    ├── goodsDesc
    ├── guideFileInfo
    ├── goodsSizeChartList
    ├── goodsSizeImage
    ├── skuList
    ├── goodsTrademark
    ├── taxCodeInfo
    ├── goodsAssociationInfo
    ├── goodsVehiclePropertyRelation
    ├── secondHand
    ├── modifyId
    └── saveMode
```

### `request` 内字段一览

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | Language |
| goodsId | LONG | **是** | Product Number |
| goodsBasic | OBJECT | 否 | goods basic，见 [goodsBasic](#goodsbasic) |
| goodsServicePromise | OBJECT | 否 | goods service promise，见下 |
| goodsProperty | OBJECT | 否 | goods property，见下 |
| goodsOriginInfo | OBJECT | 否 | Country/region of Origin，见下 |
| bulletPoints | STRING[] | 否 | bullet points |
| goodsDesc | STRING | 否 | goods desc |
| guideFileInfo | OBJECT | 否 | guide file info，见下 |
| goodsSizeChartList | OBJECT | 否 | goods size chart list，见下 |
| goodsSizeImage | STRING[] | 否 | The URL of the size chart image |
| skuList | OBJECT[] | 否 | sku list，见下 |
| goodsTrademark | OBJECT | 否 | goods trademark，见下 |
| taxCodeInfo | OBJECT | 否 | tax code info，见下 |
| goodsAssociationInfo | OBJECT | 否 | goods association info，见下 |
| goodsVehiclePropertyRelation | OBJECT | 否 | Vehicle data，见下 |
| secondHand | OBJECT | 否 | second hand info，见下 |
| modifyId | STRING | 否 | Product information modification ID；goods 唯一，后续可凭此 ID 查审核结果 |
| saveMode | INTEGER | 否 | ERP product publish status：`1`=Submitted，`2`=Saved as draft |

### request.taxCodeInfo（EU 文档）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| itemTaxCode | STRING | 否 | Tax item code |

### request.goodsAssociationInfo（EU 文档）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| noChargerGoodsList | LONG[] | 否 | Associated goods without charger |

### 网关 `params` 写法

推荐与官方一致，整体放入 **`request`**：

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "goodsBasic": { "goodsName": "New Title" }
  }
}
```

若网关/Temu 要求展平，可将 `request` 内字段提到 `params` 顶层（`goodsId`、`goodsBasic`、`skuList` 等保持**同级**关系，仍不要把 `skuList` 放进 `goodsBasic`）。

---

## goodsBasic

仅包含 **goods basic** 相关字段（Partner 文档中 `goodsBasic` 子树）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsName | STRING | 否 | goods name |
| goodsGallery | OBJECT | 否 | goods gallery，见下 |
| importDesignation | STRING | 否 | `Imported` / `Made in the USA` / `Made in the USA and Imported` / `Made in the USA or Imported` |

### `goodsBasic.goodsGallery`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| detailVideo | OBJECT | 否 | Detail Video：`vid`、`videoUrl` |
| goodsCarouselImage | STRING[] | 否 | Product carousel images |
| detailImage | STRING[] | 否 | Product Detail Images |
| carouselVideo | OBJECT | 否 | Carousel Video：`vid`、`videoUrl` |

---

## request.goodsServicePromise

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| shipmentLimitDay | INTEGER | 否 | Stock Preparation Time - Days；可选 `1`、`2` |
| fulfillmentType | INTEGER | 否 | `1`=Self-Delivery，`2`=Platform Delivery |
| costTemplateId | STRING | 否 | Shipping Template ID |

---

## request.goodsProperty

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsProperties | OBJECT[] | 否 | Product Attribute List |

**`goodsProperties[]`**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| vid | LONG | 否 | 非自定义规格值时须传 vid |
| value | STRING | 否 | Attribute Value |
| valueUnit | STRING | 否 | Attribute Value Unit |
| valueUnitId | LONG | 否 | Attribute Value Unit ID |
| templatePid | LONG | 否 | Template Attribute Id |
| parentSpecId | LONG | 否 | 非销售属性可不填 |
| specId | LONG | 否 | 非销售属性可不填 |
| note | STRING | 否 | Note |
| imgUrl | STRING | 否 | Image URL |
| groupId | INTEGER | 否 | Attribute Value Group ID |
| refPid | LONG | 否 | Reference Property ID |
| numberInputValue | STRING | 否 | Numeric Input |

---

## request.goodsOriginInfo

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| originRegion1 | STRING | 否 | Primary Address（country or region） |
| originRegion2 | STRING | 否 | Secondary Address；**Primary=China 时必填** |
| agreeDefaultOriginRegion | BOOLEAN | 否 | 默认 `false` |
| proofImageUrls | STRING[] | 否 | 产地标签实拍 |
| labelManufacturerProofImageUrls | STRING[] | 否 | 标签特写，最多 5 张 |

---

## request.guideFileInfo

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| lang2GuideFileUrl | MAP | 否 | language → PDF URL；**须含英文** |

---

## request.goodsSizeChartList

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsSizeChartList | OBJECT[] | 否 | 多套尺码表（套装） |

**数组元素：** `classId`、`meta`、`groups[]`（`id`、`name`、`elements[]`、`records[]`、`values[]`）、`bodyMeta`、`bodyRecords[]`。

---

## request.skuList[]

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| skuId | LONG | 条件 | **修改 SKU 必填**；**新增 SKU 勿传** |
| basePrice | OBJECT | 条件 | **修改勿传**；**新增必填** `{ amount, currency }` |
| listPrice | OBJECT | 否 | 须高于 basePrice |
| listPriceType | INTEGER | 否 | 空或 `0` 时必须填 listPrice |
| quantity | LONG | 条件 | **修改勿传**；**新增必填** |
| specIdList | LONG[] | 条件 | **修改勿传**；**新增必填** |
| outSkuSn | STRING | 否 | 修改时可选；不传保留，传 `""` 清空 |
| weight | STRING | **是** | weight |
| weightUnit | STRING | **是** | weight unit |
| length / width / height | STRING | **是** | 尺寸 |
| volumeUnit | STRING | **是** | volume unit |
| images | STRING[] | **是** | images |
| multiplePackage | OBJECT | 否 | `skuClassification`、`mixedSetType`、`numberOfPieces`、`pieceUnitCode`、`originNetContentNumber`、`originTotalNetContentNumber`、`netContentUnitCode`、`individuallyPacked` |

---

## request.goodsTrademark

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| brandId | LONG | 否 | Brand ID |
| trademarkId | LONG | 否 | Trademark ID |
| noTrademark | BOOLEAN | 否 | 默认 `false` |

---

## request.goodsVehiclePropertyRelation

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| relationId | LONG | 否 | relationType=`1` 时查兼容车型库 |
| ktype | LONG[] | 否 | K-type 映射 |
| leafPropertyValueDependencyIdList | LONG[] | 否 | 末级属性值 dependency id |

---

## request.secondHand

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| secondHandGoods | BOOLEAN | 否 | whether it's second hand |
| level | INTEGER | 否 | condition |

---

## Response

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result.goodsId | LONG | Product ID |
| result.productType | INTEGER | `1` Normal，`2` Custom，`3` Made-to-order |
| result.skuInfoList | OBJECT[] | Sku information list |
| result.skuInfoList[].skuId | LONG | Sku id |
| result.skuInfoList[].outSkuSn | STRING | External sku code |
| result.skuInfoList[].specList | OBJECT[] | `{ specId, parentSpecId }` |

---

## 示例

### 只改标题

```bash
python scripts/eu_manage_partial_update.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "goodsBasic": {
      "goodsName": "Updated Title"
    }
  }
}'
```

### 改轮播图 + 提交状态

```bash
python scripts/eu_manage_partial_update.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
    "language": "en",
    "goodsBasic": {
      "goodsGallery": {
        "goodsCarouselImage": ["https://..."]
      }
    },
    "saveMode": 1
  }
}'
```

### 修改已有 SKU（`skuList` 与 `goodsBasic` 同级）

```bash
python scripts/eu_manage_partial_update.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456,
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
