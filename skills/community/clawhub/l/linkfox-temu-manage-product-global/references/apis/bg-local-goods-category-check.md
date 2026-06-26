# 类目预检 — `bg.local.goods.category.check`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_category_check.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.category.check`，业务载荷放在 Body 的 `params` |

**Description:** precheck category misplacement（类目错放预检）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── catId
    ├── hdThumbUrl
    ├── carouselImageList
    ├── language
    └── goodsName
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| catId | LONG | 否 | category id |
| hdThumbUrl | STRING | 否 | thumb url（高清缩略图） |
| carouselImageList | STRING[] | 否 | list of carousel images（轮播图 URL 列表） |
| language | STRING | 否 | Language |
| goodsName | STRING | 否 | goods name |

> 官方表中五项均为选填；实际预检时通常需传入 **`catId`** 及能描述商品的字段（如 **`goodsName`**、**`hdThumbUrl`** / **`carouselImageList`**），以提高准确度。以 Partner 文档与实网校验为准。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "catId": 12345,
    "goodsName": "Product Title",
    "language": "en"
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "catId": 12345,
    "goodsName": "Product Title",
    "hdThumbUrl": "https://example.com/thumb.jpg",
    "carouselImageList": [
      "https://example.com/1.jpg",
      "https://example.com/2.jpg"
    ]
  }
}
```

> **勿**使用旧文档中的 `goodsId`、`productPropertyReqs`；官方入参为 **`catId`** + 图片/标题/语言组合。

---

## Response（Temu `body` 解析后）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | result（子字段在 Partner 文档中展开） |

官方 Response 表中 **`result` 未在提供的片段中展开**，预检结论、建议类目等字段名以 Partner 后台为准。

---

## 示例

```bash
python scripts/global_manage_category_check.py '{
  "accessToken": "TOKEN",
  "request": {
    "catId": 12345,
    "goodsName": "Wireless Earbuds",
    "carouselImageList": ["https://example.com/main.jpg"],
    "language": "en"
  }
}'
```
