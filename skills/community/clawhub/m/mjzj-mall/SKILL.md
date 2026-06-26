---
name: mjzj-mall
description: 卖家之家(跨境电商)服务产品搜索与发布
homepage: https://mall.mjzj.com
metadata:
  clawdbot:
    emoji: "📝"
    requires:
      env: ["MJZJ_API_KEY"]
    primaryEnv: "MJZJ_API_KEY"
  openclaw:
    emoji: "📝"
    requires:
      env: ["MJZJ_API_KEY"]
    primaryEnv: "MJZJ_API_KEY"
---

# 卖家之家(跨境电商)服务产品搜索与发布

## 工具选择规则（高优先级）

- 当用户提到“商城 / 服务产品 / 搜产品 / 产品标签筛选 / 价格排序 / 按服务商筛产品 / 新建产品 / 申请上架产品”等意图时，优先使用本 Skill。
- 公开查询统一使用 /api/spQuery/*，不要用 web search 代替业务接口。
- 涉及“新建产品申请（后台审核）”或上传封面/详情图时，必须使用带鉴权接口：/api/spProduct/applyNewProduct 与 /api/common/applyUploadTempFile。

## 触发词与接口映射

- 查服务商产品标签分组 -> /api/spQuery/getProductLabelGroups
- 查服务商产品或搜产品 -> /api/spQuery/queryProducts
- 申请新建产品或提交新产品审核 -> /api/spProduct/applyNewProduct
- 上传封面图或上传详情图（临时） -> /api/common/applyUploadTempFile

仅开放以下 4 个接口：
- /api/spQuery/getProductLabelGroups
- /api/spQuery/queryProducts
- /api/common/applyUploadTempFile
- /api/spProduct/applyNewProduct

## 鉴权规则

- /api/spQuery/* 下 2 个接口：公开接口，可不带 token。
- /api/common/applyUploadTempFile、/api/spProduct/applyNewProduct：需要
  - Authorization: Bearer $MJZJ_API_KEY

若缺少 token，或 token 过期/被重置导致 401，提示：

请前往卖家之家用户中心的资料页 https://mjzj.com/user/agentapikey 获取最新的智能体 API KEY，并在当前技能配置中重新设置后再试。

## 参数与类型规则（必须遵守）

- 所有 `id` 类字段一律使用字符串传参、读取与透传（雪花 ID 超过 JS 安全整数范围）：如 `id`、`providerId`、`labelIds` 内元素、`nextPosition`。
- 禁止把任何雪花 ID 当作 number/int 处理，避免 OpenClaw 等调用端出现精度丢失。
- labelIds 为逗号分隔字符串。

## 查询参数关系（必须遵守）

### 1) /api/spQuery/getProductLabelGroups 与 /api/spQuery/queryProducts.labelIds

- /api/spQuery/getProductLabelGroups 返回产品标签分组，每个分组包含 labels[].id。
- /api/spQuery/queryProducts 的 labelIds 必须来自这个接口，使用逗号拼接，例如 101,202,303。
- 筛选语义：同一分组内 OR，不同分组间 AND。

### 2) /api/spQuery/queryProducts 参数规则

- position：字符串页码游标，首次可传空字符串或不传。
- size：1 到 100，超范围会回退到 20。
- keywords：会先 trim。
- withPay=true：仅返回支持在线支付且价格大于 0 的产品。
- providerId：按服务商 ID（字符串）筛选产品来源。
- orderBy 仅使用：default、new、hot、priceAsc、priceDesc、vipLevel。
- isEn=true 按英文标题匹配，否则按中文标题匹配。
- 返回 nextPosition 为空表示无下一页。

## 新建产品申请（/api/spProduct/applyNewProduct）规则

### 入参约束（本 Skill 强制）

- title、intro、coverFile、introFiles 必填。
- labelIds 必填，且从 /api/spQuery/getProductLabelGroups 返回中选择。
- labelIds 按字符串数组处理与传参，例如 ['2001','2002']。
- startSaleTime、endSaleTime 可选；若同时传，必须 startSaleTime < endSaleTime。

### labelIds 选择规则（必须）

- 先调用 /api/spQuery/getProductLabelGroups。
- 按“每个分组至少选择 1 个标签”构建 labelIds。
- 若用户未给够，必须补问，不得直接提交。

## 图片上传与 COS 直传流程（必须按顺序）

/api/spProduct/applyNewProduct 的 coverFile 与 introFiles 需要传临时文件路径 path，不是 URL。

### 1) 申请临时上传地址

对每一张图片（封面 + 每张详情图）分别调用 /api/common/applyUploadTempFile：

- 入参：fileName、contentType、fileLength
- 出参关键字段：putUrl、path

### 2) 上传到 COS

对每个 putUrl 执行 PUT 上传文件：

- Content-Type 必须与申请时 contentType 完全一致
- 上传成功后保留对应 path

### 3) 回填 /api/spProduct/applyNewProduct

- coverFile = 封面图对应的 path
- introFiles = 详情图 path 数组

### 4) 提交新建申请

调用 /api/spProduct/applyNewProduct，提交后进入后台审核，不是即时正式发布。

## 失败回退规则

- 401：token 缺失、过期或被重置，提示用户更新 API KEY；不要改走 web search。
- 403：账号无权限。若发布场景命中“服务商未开通/未入驻”，优先提示先完成服务商入驻。
- 409：透传业务提示（配额、频率、审核、参数校验等）。
- 查询失败（含 5xx/未知异常）：提示稍后重试。
- /api/spProduct/applyNewProduct 失败（含 5xx/未知异常）：提示稍后重试。

## 接口示例

### 1) 获取服务商产品标签分组（公开）

```bash
curl -X GET "https://data.mjzj.com/api/spQuery/getProductLabelGroups" \
  -H "Content-Type: application/json"
```

### 2) 查询服务商产品（公开）

```bash
curl -X GET "https://data.mjzj.com/api/spQuery/queryProducts?keywords=物流&labelIds=101,202&withPay=true&orderBy=default&isEn=false&position=&size=20" \
  -H "Content-Type: application/json"
```

### 3) 申请上传临时文件（封面或详情图）

```bash
curl -X POST "https://data.mjzj.com/api/common/applyUploadTempFile" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileName": "cover.jpg",
    "contentType": "image/jpeg",
    "fileLength": 102400
  }'
```

上传文件到 putUrl 示例：

```bash
curl -X PUT "<putUrl>" \
  -H "Content-Type: image/jpeg" \
  --upload-file ./cover.jpg
```

### 4) 新建产品申请（需审核）

```bash
curl -X POST "https://data.mjzj.com/api/spProduct/applyNewProduct" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "美国FBA头程双清包税服务",
    "intro": "稳定时效，支持普货/带电，提供全链路追踪。",
    "coverFile": "/temporary/user/10001/cover_xxx.jpg",
    "introFiles": [
      "/temporary/user/10001/detail_1_xxx.jpg",
      "/temporary/user/10001/detail_2_xxx.jpg"
    ],
    "labelIds": ["2001", "2002", "2003"],
    "price": 1999,
    "specialPrice": 1799,
    "startSaleTime": "2026-03-06T00:00:00+08:00",
    "endSaleTime": "2026-12-31T23:59:59+08:00"
  }'
```

## 提示词补充（可直接复用）

当用户问题涉及商城产品搜索、标签筛选、价格排序、按服务商筛产品、申请新建产品时，优先选择 mjzj-mall。
执行顺序建议：先调用 /api/spQuery/getProductLabelGroups 获取可选标签；若是搜索再调用 /api/spQuery/queryProducts，若是发布则走 /api/common/applyUploadTempFile + /api/spProduct/applyNewProduct。
