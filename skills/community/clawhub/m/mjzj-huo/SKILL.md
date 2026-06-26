---
name: mjzj-huo
description: 卖家之家(跨境电商)货盘搜索与发布
homepage: https://mjzj.com/gongxu
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

# 卖家之家(跨境电商)货盘查询与发布

## 工具选择规则（高优先级）

- 当用户提到“货盘 / 货源 / 查货盘 / 搜货盘 / 货盘标签 / 货盘价格排序 / 发布货盘 / 我的货盘 / 我的申请 / 审核中的货盘申请”等意图时，优先使用本 Skill。
- 公开查询统一使用 /api/pallet/*，不要用 web search 代替业务接口。
- 涉及“申请发布货盘、查询我的货盘、查询我的申请”时，必须使用带鉴权接口：/api/palletManage/applyNew、/api/palletManage/getPallets、/api/palletManage/getApplications。
- 申请发布涉及图片时，必须先走 /api/common/applyUploadTempFile 获取临时上传地址并直传 COS。

## 触发词与接口映射

- 查货盘标签分组 -> /api/pallet/groupLabels
- 查货盘或搜货盘 -> /api/pallet/query
- 申请发布货盘 -> /api/palletManage/applyNew
- 查询我的货盘 -> /api/palletManage/getPallets
- 查询我的申请（审核中） -> /api/palletManage/getApplications
- 审核中申请口语（如“查询我的货盘申请（审核中）/查我审核中的申请/我的货盘审核进度”）-> /api/palletManage/getApplications（结果过滤 auditState == null）
- 上传封面图或介绍图（临时） -> /api/common/applyUploadTempFile

仅开放以下 6 个接口：
- /api/pallet/groupLabels
- /api/pallet/query
- /api/palletManage/applyNew
- /api/palletManage/getPallets
- /api/palletManage/getApplications
- /api/common/applyUploadTempFile

## 鉴权规则

- /api/pallet/* 下 2 个接口：公开接口，可不带 token。
- /api/palletManage/applyNew、/api/palletManage/getPallets、/api/palletManage/getApplications、/api/common/applyUploadTempFile：需要
  - Authorization: Bearer $MJZJ_API_KEY

若缺少 token，或 token 过期/被重置导致 401，提示：

请前往卖家之家用户中心的资料页 https://mjzj.com/user/agentapikey 获取最新的智能体 API KEY，并在当前技能配置中重新设置后再试。

## 参数与类型规则（必须遵守）

- 所有 `id` 类字段一律使用字符串传参、读取与透传（雪花 ID 超过 JS 安全整数范围）：如 `id`、`labelIds` 内元素、`oldApplicationId`、`nextPosition`。
- 禁止把任何雪花 ID 当作 number/int 处理，避免 OpenClaw 等调用端出现精度丢失。
- labelIds 为逗号分隔字符串。
- 发布入参中的 labelIds 按字符串数组组织（服务端会转换为 long 列表）。

## 查询参数关系（必须遵守）

### 1) /api/pallet/groupLabels 与 /api/pallet/query.labelIds

- /api/pallet/groupLabels 返回货盘标签分组，每个分组包含 labels[].id。
- /api/pallet/query 的 labelIds 必须来自这个接口，使用逗号拼接，例如 101,202,303。
- 筛选语义：同一分组内 OR，不同分组间 AND。

### 2) /api/pallet/query 参数规则

- position：字符串页码游标，首次可传空字符串或不传。
- size：1 到 100，超范围会回退到 20。
- keywords：会先 trim；匹配 name 或 tags。
- orderBy 仅使用：default、new、hot、priceAsc、priceDesc、vipLevel。
- 返回 nextPosition 为空表示无下一页。

### 3) 货盘上架状态规则（服务端内置）

- 查询结果仅包含当前在售货盘：onSale=true，且 startSaleTime < now 且 endSaleTime > now。

## 货盘发布申请（/api/palletManage/applyNew）规则

### 入参约束（本 Skill 强制）

- name、description、coverFile、introFiles 必填。
- price、stock 可选；若传入必须大于 0。
- labelIds 必填，且从 /api/pallet/groupLabels 返回中选择。
- tags 固定传空数组 []（不要传自定义标签）。
- startSaleDate、endSaleDate 必填，且必须 startSaleDate < endSaleDate。
- oldApplicationId 可选，用于替换旧申请。

### 发布配额与账号状态（服务端校验）

- 发布时会校验当前可发布数量上限，不同用户/服务商等级配额不同。
- 若超出配额，会返回业务错误（通常按 409 处理）。

## 图片上传与 COS 直传流程（必须按顺序）

/api/palletManage/applyNew 的 coverFile 与 introFiles 需要传临时文件路径 path，不是 URL。

### 1) 申请临时上传地址

对封面图与每张介绍图分别调用 /api/common/applyUploadTempFile：

- 入参：fileName、contentType、fileLength
- 出参关键字段：putUrl、path

### 2) 上传到 COS

对每个 putUrl 执行 PUT 上传：

- Content-Type 必须与申请时 contentType 完全一致
- 上传成功后保留对应 path

### 3) 回填 /api/palletManage/applyNew

- coverFile = 封面图 path
- introFiles = 介绍图 path 数组
- tags = []

### 4) 提交发布申请

调用 /api/palletManage/applyNew 提交审核，非即时上架。

## 我的数据查询规则

### 1) 查询我的货盘：/api/palletManage/getPallets

- onSale 可选：
  - true 仅在售
  - false 仅下架
  - 不传返回全部

### 2) 查询我的申请：/api/palletManage/getApplications

- type 可选，不传表示全部类型申请。
- 该接口返回的是未审核通过的申请（服务端为 auditState != true）。
- 若用户表达“审核中”（包括口语如“查询我的货盘申请（审核中）/查我审核中的申请/我的货盘审核进度”），从结果中过滤 auditState == null。

## 失败回退规则

- 查询失败（含 5xx/未知异常）：提示稍后重试。
- 参数格式错误（如 labelIds 非法）时，提示用户按逗号分隔字符串重新输入。
- 403：账号无权限或未登录态授权范围不足。
- 409：透传业务提示（配额限制、参数校验、审核规则等）。
- /api/palletManage/applyNew 失败（含 5xx/未知异常）：提示稍后重试。
- 不要在失败时改走 web search。

## 接口示例

### 1) 获取货盘标签分组（公开）

```bash
curl -X GET "https://data.mjzj.com/api/pallet/groupLabels" \
  -H "Content-Type: application/json"
```

### 2) 查询货盘（公开）

```bash
curl -X GET "https://data.mjzj.com/api/pallet/query?keywords=美国专线&labelIds=101,202&orderBy=default&position=&size=20" \
  -H "Content-Type: application/json"
```

### 3) 申请上传临时文件（封面或介绍图）

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

### 4) 申请发布货盘（需审核）

```bash
curl -X POST "https://data.mjzj.com/api/palletManage/applyNew" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "美国FBA头程散货拼箱",
    "description": "稳定时效，支持普货/带电，提供轨迹查询",
    "price": 199,
    "stock": 100,
    "coverFile": "/temporary/user/10001/cover_xxx.jpg",
    "introFiles": [
      "/temporary/user/10001/detail_1_xxx.jpg",
      "/temporary/user/10001/detail_2_xxx.jpg"
    ],
    "labelIds": ["2001", "2002"],
    "tags": [],
    "startSaleDate": "2026-03-13T00:00:00+08:00",
    "endSaleDate": "2026-12-31T23:59:59+08:00"
  }'
```

### 5) 查询我的货盘（需鉴权）

```bash
curl -X GET "https://data.mjzj.com/api/palletManage/getPallets?onSale=true" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

### 6) 查询我的申请（需鉴权）

```bash
curl -X GET "https://data.mjzj.com/api/palletManage/getApplications" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

## 提示词补充（可直接复用）

当用户问题涉及货盘搜索、货盘标签分组、申请发布货盘、查询我的货盘、查询我的申请（含“审核中”口语表达）时，优先选择 mjzj-huo。
执行顺序建议：
- 搜索场景：先调用 /api/pallet/groupLabels，再调用 /api/pallet/query。
- 发布场景：先调用 /api/pallet/groupLabels 选标签，再调用 /api/common/applyUploadTempFile + PUT 上传，最后调用 /api/palletManage/applyNew。
- 我的数据：调用 /api/palletManage/getPallets 和 /api/palletManage/getApplications。
