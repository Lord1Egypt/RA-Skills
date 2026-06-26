# 商品发布 API — 参数参考（V2 Recommended）

Partner US 菜单：**Product > Add Products > Recommended V2 Interfaces**。  
经 `POST /temu/proxy` 转发，网关与响应信封见 [api.md](./api.md)。

发品前请先调用 [category-spec-apis.md](./category-spec-apis.md) 中的属性与规格接口，并完成图片上传。

---

## 1. 发布商品 V2 — `temu.local.goods.v2.add`

- **Partner 文档分区**：`sub_menu_code=91657460a9be4a609df2eef01bc6deef`
- **脚本**：`scripts/us_goods_add.py`
- **用途**：在美国站创建新商品（V2 推荐发品接口）。与同族 `bg.local.goods.add`、`temu.goods.add` 载荷结构一致或为其超集。

### 网关 Body

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| site | string | 是 | 默认 `us` |
| managementType | string | 是 | 默认 `semi-managed` |
| accessToken / storeKey | string | 是 | 二选一 |
| tokenPurpose | string | 否 | 默认 `product-inventory` |
| type | string | 是 | 固定 `temu.local.goods.v2.add` |
| params | object | 是 | 发品载荷，见下文 |

### 业务参数（`params`）— 顶层

以下字段来自同族 `bg.local.goods.add` / `temu.goods.add` 发品模型；**具体必填项由类目属性接口返回的 `required` 决定**。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsBasic | object | 是 | 商品基础信息（标题、类目、轮播图等） |
| skuList | array | 是 | SKU 列表（价格、库存、规格、图片等） |
| certificationInfo | object | 否 | 合规/认证（证书、GPSR、实拍图等，类目要求时必填） |
| productPropertyReqs | array | 否 | 普通属性（亦可放在 `goodsBasic` 内，以官方字段为准） |
| productSpecPropertyReqs | array | 否 | 销售规格属性 |
| productSemiManagedReq | object | 否 | 半托管绑定站点等 |
| productShipmentReq | object | 否 | 半托管配送/运费模板 |
| addProductChannelType | integer | 是 | 发品渠道（同族接口必填） |

#### `goodsBasic` 常见字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| catId / leafCatId | integer | 是 | 叶子类目 ID（或 cat1Id…cat10Id 逐级类目，与同族 `temu.goods.add` 一致） |
| productName | string | 是 | 商品标题，通常 1–250 字符 |
| carouselImageUrls | array | 是 | 轮播图 URL 列表（须先 `image.v2.upload`），常 ≥5 张 |
| materialImgUrl | string | 否 | 素材图 URL |
| carouselImageI18nReqs | array | 否 | 多语言轮播图（非服饰类常必填） |
| productOuterPackageImageReqs | array | 否 | 外包装图 |
| productOuterPackageReq | object | 否 | 外包装信息 |
| productPropertyReqs | array | 是 | 类目属性值，元素见下表 |
| productSpecPropertyReqs | array | 条件 | 多规格时的规格属性 |
| productWhExtAttrReq | object | 是 | 仓配扩展（产地、重量体积等） |
| productSaleExtAttrReq | object | 否 | 销售扩展 |
| productSkcReqs | array | 是 | SKC 维度数据（含 SKU 列表） |
| sizeTemplateIds | array | 否 | 尺码表模板 ID，无尺码传 `[]` |
| showSizeTemplateIds | array | 否 | 展示用尺码表，至多 2 个 |
| goodsModelReqs | array | 否 | 模特信息 |
| productGuideFileReqs | array | 否 | 说明书文件 |
| goodsLayerDecorationReqs | array | 否 | 商详装饰模块 |
| personalizationSwitch | integer | 否 | 0 非定制品，1 定制品 |
| productCarouseVideoReqList | array | 否 | 主图视频 |
| materialMultiLanguages | array | 否 | 图片多语言 |
| addProductChannelType | integer | 是 | 发品渠道 |

#### `productPropertyReqs[]` 元素（发品回填属性）

| 字段 | 类型 | 说明 |
|------|------|------|
| pid | integer | 属性 ID（来自 attributes.get） |
| vid | integer | 属性值 ID |
| propName | string | 属性名 |
| propValue | string | 属性值文本 |
| templatePid | integer | 模板属性 ID |
| refPid | integer | 引用属性 ID |
| numberInputValue | string | 数值录入 |
| valueUnit | string | 单位 |

#### `skuList[]` 元素（同族 `bg.local.goods.add`）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| images | array | 是 | SKU 图片 URL 列表 |
| quantity | integer | 是 | 库存数量 |
| externalProductType | integer | 否 | 外部商品类型 |
| supplierPrice / price | object | 条件 | 供货价（金额 + 币种） |
| specIdList | array | 条件 | 规格 ID 列表（多规格） |
| outSkuSn / extCode | string | 否 | 商家 SKU 编码 |
| multiplePackage | object | 否 | 多件装：`numberOfPieces`、`individuallyPacked`、`skuClassification` 等 |

#### `certificationInfo` 常见块（合规类目）

| 块 | 说明 |
|----|------|
| certificateInfo | 证书类型、文件 URL、authCode 等 |
| extraTemplate | 合规模板扩展字段 |
| actualPhoto | 实拍图（`skuPhotoInfoList`、`position`） |
| gpsrInfo | 欧盟 GPSR：制造商、责任人 |
| repInfo | 代表信息 |

完整嵌套字段以 Partner 后台 **Add Product V2** 文档为准；上表覆盖 EU 同族 `bg.local.goods.add` 公开示例中的主要块。

### 响应（`result` 常见结构）

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | integer | 新建货品 ID |
| goodsId | integer | 商品 ID（部分接口命名） |
| productSkcList | array | `{ productSkcId }` |
| productSkuList | array | `{ productSkuId, productSkcId, extCode, skuSpecList[] }` |

### 示例

```bash
python scripts/us_goods_add.py '{
  "accessToken": "YOUR_TOKEN",
  "params": {
    "goodsBasic": {
      "catId": 12345,
      "productName": "Example Product",
      "carouselImageUrls": ["https://..."],
      "productPropertyReqs": [{ "pid": 1, "vid": 100 }],
      "addProductChannelType": 0
    },
    "skuList": [{
      "images": ["https://..."],
      "quantity": 99,
      "supplierPrice": { "amount": "19.99", "currency": "USD" }
    }]
  }
}'
```

---

## 2. 商品图片上传 V2 — `temu.local.goods.image.v2.upload`

- **Partner 文档分区**：`sub_menu_code=37d470d8c6e149f78953311aa0b0296d`
- **脚本**：`scripts/us_goods_image_upload.py`
- **用途**：上传商品图片（Base64），返回可用于 `goods.v2.add` 的 URL。与同族 `bg.goods.image.upload.global` 一致。

### 网关 Body

网关字段同 §1，`type` 固定为 `temu.local.goods.image.v2.upload`。

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | string | 是 | 图片 **Base64**（支持 jpg/jpeg、png 等） |
| imageBizType | integer | 否 | `0` 默认；`1` 外包装专用 URL |
| options | object | 否 | 裁剪/增强选项，见下表 |

#### `options`

| 字段 | 类型 | 说明 |
|------|------|------|
| boost | boolean | 是否 AI 清晰度提升 |
| doIntelligenceCrop | boolean | 是否智能裁剪（true 时可能返回 1 原图 + 3 裁剪图） |
| cateId | integer | 叶子类目 ID（`doIntelligenceCrop=true` 时生效） |
| sizeMode | integer | `0` 原图；`1` 800×800；`2` 1350×1800 |

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| imageUrl | string | 原图链接 |
| url | string | 单张 AI 裁图链接 |
| urls | array | 多张 AI 裁图链接 |

将 `imageUrl` 或 `urls[]` 填入 `goods.v2.add` 的 `carouselImageUrls`、`skuList[].images`、`materialImgUrl` 等。

### 示例

```bash
python scripts/us_goods_image_upload.py '{
  "accessToken": "YOUR_TOKEN",
  "params": {
    "image": "<BASE64>",
    "options": {
      "doIntelligenceCrop": true,
      "cateId": 12345,
      "sizeMode": 1
    }
  }
}'
```

### 网关响应示例（结构）

```json
{
  "body": "{\"success\":true,\"errorCode\":1000000,\"result\":{\"imageUrl\":\"https://...\",\"url\":\"https://...\",\"urls\":[\"https://...\"]}}"
}
```

---

## 3. 发布商品（半托管/跨境）— `temu.goods.add`

- **sub_menu_code**：`1b99296745854ae08d39a7bbe1e4f7a8`
- **脚本**：`scripts/us_goods_add_legacy.py`
- **说明**：非 V2 发品接口；美国站 Partner US 发品优先用 **§1** `temu.local.goods.v2.add`。载荷与同族 `temu.goods.add` 一致。

### 业务参数（`params`）

与 [§1](#1-发布商品-v2--temulocalgoodsv2add) 类似，主要块包括：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cat1Id … cat10Id | integer | 是 | 各级类目（至少到叶子） |
| productName | string | 是 | 商品标题 |
| carouselImageUrls | array | 是 | 轮播图 URL，通常 ≥5 张 |
| productPropertyReqs | array | 是 | 类目属性 |
| productSkcReqs | array | 是 | SKC/SKU 结构 |
| addProductChannelType | integer | 是 | 发品渠道 |

完整字段见 §1 `goodsBasic` / `skuList` 说明。

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | integer | 新建货品 ID |
| productSkcList | array | `{ productSkcId }` |
| productSkuList | array | `{ productSkuId, extCode, skuSpecList }` |

### 示例

```bash
python scripts/us_goods_add_legacy.py '{
  "accessToken": "TOKEN",
  "params": { "...": "同 temu.goods.add 文档结构" }
}'
```

---

## 相关文档

- [类目属性与规格](./category-spec-apis.md)
- [商品查询](./product-query-apis.md)
- [商品编辑](./product-edit-apis.md)
- [API 调用规范](./api.md)
- [接口目录](./partner-us-catalog.md)
