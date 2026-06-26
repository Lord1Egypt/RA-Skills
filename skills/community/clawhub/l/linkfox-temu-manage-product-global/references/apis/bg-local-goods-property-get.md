# 商品属性获取 — `bg.local.goods.property.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_property_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.property.get`，业务载荷放在 Body 的 `params` |

**Description:** Get Temu goods attributes（按商品信息/类目等获取属性，与发品侧「类目属性模板」接口不同，见文末说明）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── goodsName                 ← 必填
    ├── catId
    ├── language / goodsDesc
    ├── thirdPartyErpType / thirdPartyMall / thirdPartyCatName
    └── goodsPropList[]
        ├── propName
        └── values
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | language |
| goodsName | STRING | **是** | Goods name |
| catId | LONG | 否 | Leaf category ID（叶子类目 ID） |
| goodsDesc | STRING | 否 | goods description |
| thirdPartyErpType | INTEGER | 否 | third party type |
| thirdPartyMall | STRING | 否 | third party mall |
| thirdPartyCatName | STRING | 否 | third party cat name |
| goodsPropList | OBJECT[] | 否 | Goods Prop List，见下表 |

### `goodsPropList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| propName | STRING | 否 | Product property name in English（属性名，英文） |
| values | STRING[] | 否 | Product property values in English（属性值列表，英文） |

> `goodsPropList` 为**英文属性名 + 英文属性值**的简单结构，**不是** `bg.local.goods.partial.update` 中 `goodsProperty.goodsProperties[]` 的 `vid` / `templatePid` / `refPid` 模型。用于传入第三方或已知属性片段，辅助平台匹配/推荐 Temu 属性。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsName": "Wireless Bluetooth Earbuds",
    "catId": 12345,
    "language": "en"
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsName": "Wireless Bluetooth Earbuds",
    "catId": 12345,
    "goodsDesc": "Noise cancelling in-ear headphones",
    "thirdPartyMall": "amazon",
    "thirdPartyCatName": "Electronics > Headphones",
    "goodsPropList": [
      {
        "propName": "Material",
        "values": ["Plastic", "Metal"]
      },
      {
        "propName": "Color",
        "values": ["Black"]
      }
    ]
  }
}
```

> **勿**仅传 `catId` 而不传 **`goodsName`**（官方必填）。**勿**与仅传 `catId` 的类目模板接口 `temu.local.product.attributes.get` / `bg.goods.attrs.get`（发品 skill）混用。

---

## Response（Temu `body` 解析后）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | 当前请求是否成功 |
| errorCode | INTEGER | 错误码 |
| errorMsg | STRING | 错误信息 |
| result | OBJECT | result（子字段在 Partner 文档中展开） |

官方 Response 表中 **`result` 未在提供的片段中展开**；返回的属性列表/推荐字段以 Partner 后台为准。

---

## 与发品「类目属性模板」接口区分

| 项 | `bg.local.goods.property.get`（本接口） | `temu.local.product.attributes.get` / `bg.goods.attrs.get` |
|----|----------------------------------------|----------------------------------------------------------|
| 所在 skill | manage-product-us | add-product-us |
| 典型入参 | **`goodsName` 必填**，可选 `catId`、`goodsPropList`（英文 propName/values）、第三方信息 | 通常 **`catId` 必填** |
| 属性值形态 | `goodsPropList[].propName` + `values[]`（英文） | `properties[]` 模板 + 发品 `productPropertyReqs`（pid/vid） |
| 用途 | 按商品信息获取/推荐属性 | 按叶子类目拉取属性**模板** |

---

## 示例

```bash
python scripts/global_manage_property_get.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsName": "Stainless Steel Water Bottle 32oz",
    "catId": 67890,
    "language": "en",
    "goodsPropList": [
      { "propName": "Capacity", "values": ["32 oz"] },
      { "propName": "Material", "values": ["Stainless Steel"] }
    ]
  }
}'
```
