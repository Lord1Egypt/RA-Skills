# 类目、属性与规格 API — 参数参考

Partner US 菜单 **Product**（`menu_code=fb16b05f7a904765aac4af3a24b87d4a`）。经 `POST /temu/proxy` 转发，网关见 [api.md](./api.md)。

- **§1–§2**：Add Products **V2 Recommended**（`temu.local.*`）
- **§3–§7**：标准商品类目/属性/规格/品牌/映射接口

---

## 1. 获取类目属性模板 — `temu.local.product.attributes.get`

- **Partner 文档分区**：`sub_menu_code=1ecd9ad752a14d5e9f5297edfd6c8848`
- **脚本**：`scripts/us_goods_attrs.py`
- **用途**：按**叶子类目 ID** 获取发品所需属性模板（必填/选填、控件类型、属性值列表等）。发品前必须先调用。

### 网关 Body

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| site | string | 是 | 默认 `us` |
| managementType | string | 是 | 默认 `semi-managed` |
| accessToken / storeKey | string | 是 | 二选一 |
| tokenPurpose | string | 否 | 默认 `product-inventory` |
| type | string | 是 | 固定 `temu.local.product.attributes.get` |
| params | object | 是 | 见下表 |

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| catId | integer | 是 | **叶子类目 ID**（须选到最细子类目，与同族 `bg.goods.attrs.get` 一致） |

### 响应（`result` 常见结构）

与同族 `bg.goods.attrs.get` 返回的类目属性模板一致，顶层字段示例：

| 字段 | 类型 | 说明 |
|------|------|------|
| inputMaxSpecNum | integer | 允许的自定义规格数量上限 |
| chooseAllQualifySpec | boolean | 限定规格是否须全选 |
| singleSpecValueNum | integer | 单个自定义规格值数量上限 |
| properties | array | 属性模板列表，见下表 |

#### `properties[]` 元素

| 字段 | 类型 | 说明 |
|------|------|------|
| pid | integer | 基础属性 ID |
| templatePid | integer | 模板属性 ID |
| refPid | integer | 引用属性 ID |
| name | string | 属性名称 |
| lang2Name | string | 第二语言名称 |
| required | boolean | 是否必填 |
| isSale | boolean | 是否销售属性（规格维度） |
| mainSale | integer | 是否主销售属性 |
| controlType | integer | 控件类型（输入/勾选/时间/尺码选择器等） |
| propertyValueType | integer | 属性值类型（文本/数值/日期等） |
| valueRule | integer | 数值规则 |
| chooseMaxNum | integer | 最大可勾选数 |
| inputMaxNum | integer | 最大可输入数；0 表示不可输入 |
| valuePrecision | integer | 小数精度；0 表示不允许小数 |
| maxValue | string | 输入上限 |
| valueUnit | array | 属性值单位列表 |
| parentSpecId | integer | 父规格 ID（销售属性相关） |
| parentTemplatePid | integer | 模板父属性 ID |
| values | array | 可选属性值，见下表 |
| showCondition | array | 按父属性展示条件 `{ parentRefPid, parentVids[] }` |

#### `properties[].values[]` 元素

| 字段 | 类型 | 说明 |
|------|------|------|
| vid | integer | 属性值 ID（发品时填入 `productPropertyReqs`） |
| value | string | 展示值 |
| specId | integer | 规格 ID（部分销售属性） |
| group | string | 分组 |
| extendInfo | string | 扩展信息 |
| parentVidList | array | 父属性值 ID 列表 |

### 示例

```bash
python scripts/us_goods_attrs.py '{
  "accessToken": "YOUR_TOKEN",
  "params": { "catId": 12345 }
}'
```

### 网关响应示例（结构）

```json
{
  "body": "{\"success\":true,\"errorCode\":1000000,\"errorMsg\":\"\",\"requestId\":\"us-xxx\",\"result\":{\"inputMaxSpecNum\":2,\"properties\":[{\"pid\":1,\"name\":\"Color\",\"required\":true,\"isSale\":true,\"values\":[{\"vid\":100,\"value\":\"Red\"}]}]}}"
}
```

---

## 2. 获取商品规格 — `temu.local.product.variation.get`

- **Partner 文档分区**：`sub_menu_code=d23bfec96065492ebe8290c6fe867a19`
- **脚本**：`scripts/us_goods_variation.py`
- **用途**：获取指定类目支持的 **Variation / 规格维度**（如颜色、尺码）及可选值，供 `temu.local.goods.v2.add` 组装 `productSpecPropertyReqs` / `skuList`。

### 网关 Body

网关字段同 §1，`type` 固定为 `temu.local.product.variation.get`。

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| catId | integer | 是 | 叶子类目 ID |

> 若官方文档另有 `parentSpecId`、`siteId` 等字段，按 Partner 后台该接口说明追加；多数场景仅需 `catId`。

### 响应（`result` 常见结构）

与同族规格查询接口一致，常见为「父规格 + 子规格值」或「可售规格维度列表」：

| 字段 | 类型 | 说明 |
|------|------|------|
| parentSpecList / variationList / specList | array | 规格维度列表（命名以实网为准） |

#### 规格维度元素（典型）

| 字段 | 类型 | 说明 |
|------|------|------|
| parentSpecId | integer | 父规格 ID |
| parentSpecName | string | 父规格名称（如 Color、Size） |
| specId | integer | 子规格/规格值 ID |
| specName | string | 规格值名称 |
| values | array | 可选规格值列表 `{ specId, specName }` |

多规格发品时，SKU 的 `skuSpecList` 需引用此处返回的 `specId` / `parentSpecId`。

### 示例

```bash
python scripts/us_goods_variation.py '{
  "accessToken": "YOUR_TOKEN",
  "params": { "catId": 12345 }
}'
```

---

## 3. 商品类目树 — `bg.goods.cats.get`

- **sub_menu_code**：`7f9ded1bfce7485798c3862467d5c30e`
- **脚本**：`scripts/us_goods_cats.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| siteId | integer | 是 | 站点 ID，当前固定传 `1` |
| parentCatId | integer | 否 | 父类目 ID，查顶级类目可不传 |
| showHidden | boolean | 否 | 是否展示隐藏类目，默认 false |

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| categoryDTOList | array | 类目列表 |

#### `categoryDTOList[]`

| 字段 | 类型 | 说明 |
|------|------|------|
| catId | integer | 类目 ID |
| catName | string | 类目名称 |
| catLevel | integer | 层级 |
| parentCatId | integer | 父类目 ID |
| isLeaf | boolean | 是否叶子类目 |
| catType | integer | 1=服饰，其它=非服饰 |
| isHidden | boolean | 是否隐藏 |

### 示例

```bash
python scripts/us_goods_cats.py '{
  "accessToken": "TOKEN",
  "parentCatId": 0,
  "showHidden": false
}'
```

---

## 4. 类目属性模板（跨境 type）— `bg.goods.attrs.get`

- **sub_menu_code**：`2b42b46f51c348b69bf8f69c5397279e`
- **脚本**：`scripts/us_goods_attrs_bg.py`
- **说明**：与 §1 `temu.local.product.attributes.get` 返回结构相同，**type 不同**；半托管跨境发品常用此 type。

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| catId | integer | 是 | 叶子类目 ID |

响应字段见 **§1** `properties[]` 表。

### 示例

```bash
python scripts/us_goods_attrs_bg.py '{
  "accessToken": "TOKEN",
  "catId": 12345
}'
```

---

## 5. 父规格列表 — `bg.glo.goods.parentspec.get`

- **sub_menu_code**：`8a6a6e8b14814d518fe8f004f35b2192`
- **脚本**：`scripts/us_goods_parent_spec.py`
- **说明**：无业务入参，返回平台支持的父规格维度。

### 业务参数（`params`）

无，传 `{}` 即可。

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| parentSpecDTOS | array | 父规格列表 |

#### `parentSpecDTOS[]`

| 字段 | 类型 | 说明 |
|------|------|------|
| parentSpecId | integer | 父规格 ID |
| parentSpecName | string | 父规格名称 |

### 示例

```bash
python scripts/us_goods_parent_spec.py '{"accessToken": "TOKEN"}'
```

---

## 6. 可绑定品牌 — `bg.glo.goods.brand.get`

- **sub_menu_code**：`f8065a07b2d6441f9f33c2d808dcc593`
- **脚本**：`scripts/us_goods_brand.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | integer | 是 | 页码 |
| pageSize | integer | 是 | 每页条数 |
| vid | integer | 否 | 搜索的属性 ID |
| BrandName | string | 否 | 品牌名称（注意大小写） |

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总数 |
| pageItems | array | 品牌列表 |

#### `pageItems[]`

| 字段 | 类型 | 说明 |
|------|------|------|
| brandId | integer | 品牌 ID |
| brandNameEn | string | 品牌英文名 |
| pid | integer | 基础属性值 ID |
| vid | integer | 属性值 ID |
| regSerialCode | string | 注册序列号 |

### 示例

```bash
python scripts/us_goods_brand.py '{
  "accessToken": "TOKEN",
  "page": 1,
  "pageSize": 20,
  "BrandName": "Nike"
}'
```

---

## 7. 商品类目映射 — `bg.goods.category.mapping`

- **sub_menu_code**：`3f15de61844e4a989d042767a385d8f5`
- **脚本**：`scripts/us_goods_category_mapping.py`
- **用途**：根据中英文商品名推荐类目。

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsName | string | 是 | 商品中文名 |
| goodsNameEn | string | 是 | 商品英文名 |

### 响应（`result`）

| 字段 | 类型 | 说明 |
|------|------|------|
| categoryId | integer | 推荐类目 ID（字段名以实网为准，亦可能为 `catId`） |

### 示例

```bash
python scripts/us_goods_category_mapping.py '{
  "accessToken": "TOKEN",
  "goodsName": "测试商品",
  "goodsNameEn": "Test Product"
}'
```

---

## 相关文档

- [商品发布](./product-publish-apis.md)
- [商品查询](./product-query-apis.md)
- [商品编辑](./product-edit-apis.md)
- [库存与价格](./stock-price-apis.md)
- [API 调用规范](./api.md)
- [接口目录](./partner-us-catalog.md)
