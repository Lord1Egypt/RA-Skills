# 订单定制商品内容批量查询 — `bg.order.customization.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_order_customization_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.order.customization.get`，业务载荷放在 Body 的 `params` |

**Description:** Self developed sellers and third-party ISVs obtain **customized product content information in bulk** through Open API（自研卖家与第三方 ISV 通过 Open API **批量**获取订单的定制商品内容信息）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> 入参为**子订单号** `orderSn`（非 `parentOrderSn`），可从 `bg.order.list.v2.get` / `bg.order.detail.v2.get` 的 `orderList[].orderSn` 取得。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    └── orderSnList[] (STRING[], 否)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderSnList | STRING[] | 否 | orderSnList（子订单号列表）；**单次最多查询 10 个订单** |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "orderSnList": ["SO-001", "SO-002"]
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
└── result[] (OBJECT[])
    ├── orderSn
    ├── customizedType
    ├── customizedData          ← 仅 customizedType=2 时返回
    ├── previewList[]           ← 仅 customizedType=2 时返回
    │   ├── previewType
    │   ├── imageUrl
    │   ├── customizedText
    │   └── customizedAreaId
    ├── templateId
    ├── templateType
    ├── customizedText          ← 仅 customizedType=1 时返回（result 层级）
    └── customizedSvgList[]
        └── compressedFileUrl
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT[] | 各子订单的定制内容列表（与请求的 `orderSnList` 对应） |

### `result[]` 元素

| 参数 | 类型 | 说明 |
|------|------|------|
| orderSn | STRING | OrderSn corresponding to customized information（对应该定制信息的子订单号） |
| customizedType | INTEGER | Customized type（定制类型），见下表 |
| customizedData | STRING | Graphic customization content, in **json format**（图文定制内容，JSON 字符串）；**仅当 `customizedType=2` 时返回** |
| previewList | OBJECT[] | Graphic customization preview information（图文定制预览信息）；**仅当 `customizedType=2` 时返回** |
| templateId | LONG | Customization template ID when user created customized information（用户创建定制信息时的模板 ID）；商品无模板时为 `null` |
| templateType | INTEGER | Customization template type when user created customized information（定制模板类型）；商品无模板时为 `null`，见下表 |
| customizedText | STRING | Customization text（纯文本定制内容）；**仅当 `customizedType=1` 时返回**（位于 `result[]` 元素顶层，与 `previewList[].customizedText` 不同） |
| customizedSvgList | OBJECT[] | Customized information list in **SVG format**（SVG 格式定制信息列表） |

#### `customizedType`

| 值 | 说明 |
|----|------|
| `1` | pure text customization, no customized templates（纯文本定制，无定制模板） |
| `2` | customized graphics and text, with customized templates available（图文定制，有定制模板） |

#### `templateType`

| 值 | 说明 |
|----|------|
| `1` | only image（仅图片） |
| `2` | only text（仅文字） |
| `3` | text and image（文字 + 图片） |

> 商品无定制模板时，`templateId` / `templateType` 为 `null`。

### `previewList[]` 元素

| 参数 | 类型 | 说明 |
|------|------|------|
| previewType | INTEGER | type of preview item（预览项类型），见下表 |
| imageUrl | STRING | Image URL（图片 URL） |
| customizedText | STRING | Customized Text（预览项中的定制文字） |
| customizedAreaId | STRING | Customized Area ID（定制区域 ID）；**仅当 `templateType=3` 且 `previewType=3` 或 `4` 时返回** |

#### `previewType`

| 值 | 说明 |
|----|------|
| `1` | overall preview image（整体预览图；若商品未配置定制区域，则为商家上传的效果图） |
| `3` | user uploaded image（用户上传图片） |
| `4` | customized text（定制文字） |

### `customizedSvgList[]` 元素

| 参数 | 类型 | 说明 |
|------|------|------|
| compressedFileUrl | STRING | Image URL and Compression file URL（图片/压缩包下载 URL）；调用方需 **GET** 该 URL 拉取文件；**创建后 10 分钟内有效**，过期需重新调本接口获取新 URL |

#### 下载 `compressedFileUrl` 的 TOA 请求头

对 `compressedFileUrl` 发起 **GET** 时，需在 Header 携带以下公共参数（与 Partner 文档一致）：

| Header | 说明 |
|--------|------|
| `toa-app-key` | `${app_key}` |
| `toa-access-token` | `${access_token}` |
| `toa-random` | 32 位随机数字符串 |
| `toa-timestamp` | 时间戳 |
| `toa-sign` | 签名（见下） |

**`toa-sign` 计算逻辑：**

1. 将 Header 中参与签名的参数按参数名 **ASCII 升序**排序：`toa-app-key`、`toa-access-token`、`toa-random`、`toa-timestamp`
2. 按 `参数名 + 参数值` 依次拼接（中间**无**分隔符），得到长字符串
3. 在拼接结果**首尾**各拼接一次 `app_secret`，得到签名字符串
4. 对签名字符串做 **MD5**，再将密文转为**大写**，即为 `toa-sign`

> 实际 `app_key` / `access_token` / `app_secret` 以店铺授权与 Partner 应用配置为准；经 LinkFox 网关调用本 `type` 时，业务 JSON 仍走 `POST /temu/proxy`，**文件下载**为对上述 URL 的独立 GET + TOA 头。

---

## 字段返回条件速查

| 字段 | 返回条件 |
|------|----------|
| `customizedText`（`result[]` 顶层） | `customizedType=1` |
| `customizedData`、`previewList` | `customizedType=2` |
| `previewList[].customizedAreaId` | `templateType=3` 且 `previewType=3` 或 `4` |
| `templateId`、`templateType` | 有定制模板时；无模板为 `null` |

---

## 示例

```bash
python scripts/global_order_customization_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "orderSnList": ["SO-123456789", "SO-987654321"]
  }
}'
```

典型流程：`bg.order.detail.v2.get` 取得 `orderList[].orderSn` → 本接口批量拉定制内容（≤10 条）→ 若需 SVG/压缩包，用返回的 `compressedFileUrl` + TOA 头 GET 下载。
