---
name: mjzj
description: 卖家之家(跨境电商)平台一体化服务助手（服务商、物流、服务产品、技能商城、货盘、资讯、问答、供需、私信、全球开店、活动）
homepage: https://mjzj.com
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

# 卖家之家(跨境电商)平台一体化服务助手

## 使用规则（高优先级）

- 当用户提到卖家之家相关业务时，优先使用本 Skill，不要改走 web search。
- 公开查询接口可不带 token；涉及“我的数据/发布/私信发送”必须带 `Authorization: Bearer $MJZJ_API_KEY`。
- 若返回 401（token 缺失、过期或被重置），固定提示用户到 https://mjzj.com/user/agentapikey 获取并更新 API KEY。

## 参数与类型总规则（必须遵守）

- 所有 `id` 类字段一律使用字符串传参、读取与透传（雪花 ID 超过 JS 安全整数范围）：如 `id`、`authorId`、`cityId`、`providerId`、`regionId`、`platformId`、`categoryIds`/`tagIds`/`labelIds` 内元素、`position`、`nextPosition`。
- 禁止把任何雪花 ID 当作 number/int 处理，避免 OpenClaw 等调用端出现精度丢失。
- 查询接口里的逗号分隔 ID 也按字符串拼接；发布接口里的 ID 集合按各业务要求传字符串数组。

## 路由关键词（用于命中）

- 服务商、服务商分类、物流、国际物流、海外仓
- 服务产品、产品标签、产品发布、申请上架
- 技能商城、搜技能、技能标签、免费技能、付费技能、热门技能、安装技能、申请发布技能、SkillHub、ClawHub
- 货盘、货源、我的货盘、我的申请、审核中
- 资讯、文章、发布资讯、我的资讯、我的笔名
- 问答、提问、问题分类、我的问题
- 供需、发布供需、我的供需、刷新供需、删除供需
- 私信、会话、聊天记录、发送消息
- 全球开店、开店平台、搜平台
- 活动、跨境电商活动、查活动、搜活动、发布活动、创建活动、活动城市

## 能力总览（去重整合）

### 1) 服务商与物流

- 服务商分类：`/api/spQuery/getClassifies`
- 服务商查询：`/api/spQuery/queryProviders`
- 物流标签：`/api/spQuery/getLogisticsLabels`
- 物流服务商查询：`/api/spQuery/queryLogisticsProviders`

### 2) 服务产品

- 产品标签分组：`/api/spQuery/getProductLabelGroups`
- 产品查询：`/api/spQuery/queryProducts`
- 新建产品申请（审核）：`/api/spProduct/applyNewProduct`

### 3) 货盘

- 货盘标签分组：`/api/pallet/groupLabels`
- 货盘查询：`/api/pallet/query`
- 货盘发布申请（审核）：`/api/palletManage/applyNew`
- 我的货盘：`/api/palletManage/getPallets`
- 我的申请：`/api/palletManage/getApplications`

### 4) 技能商城

- 技能标签分组：`/api/skill/groupLabels`
- 技能查询：`/api/skill/query`
- 技能发布申请（审核）：`/api/skillManage/applyNew`

### 5) 资讯

- 资讯查询（公开）：`/api/article/search`
- 发布资讯：`/api/articleManage/create`
- 标签查询：`/api/articleManage/queryTags`
- 我的笔名：`/api/articleManage/getAuthors`
- 我的资讯：`/api/articleManage/queryMyArticles`

### 6) 问答

- 问答分类：`/api/ask/getCategories`
- 发布问题：`/api/ask/createQuestion`
- 问题查询：`/api/ask/queryQuestion`
- 我的问题：`/api/ask/queryMyQuestions`

### 7) 供需

- 系统标签：`/api/supplydemand/getOfficialTags`
- 系统平台：`/api/supplydemand/getPlatforms`
- 系统区域：`/api/supplydemand/getRegions`
- 发布供需：`/api/supplydemand/createinfo`
- 我的供需：`/api/supplydemand/querymyinfos`
- 刷新供需：`/api/supplydemand/refreshinfo`
- 删除供需：`/api/supplydemand/deleteinfo`

### 8) 私信

- 会话列表：`/api/message/getConversations`
- 消息列表：`/api/message/getMessages`
- 发送私信：`/api/message/sendMessage`

### 9) 全球开店

- 开店平台查询：`/api/global/queryPlatform`

### 10) 活动

- 活动查询（公开）：`/api/activity/query`
- 活动城市：`/api/activity/getActivityCities`
- 发布活动（审核）：`/api/activity/createActivity`

### 跨模块联动：服务商查询 → 私信

- `/api/spQuery/queryProviders` 和 `/api/spQuery/queryLogisticsProviders` 返回的每个服务商都包含 `userSlug` 字段。
- 当用户想联系某个服务商时，可直接将该 `userSlug` 作为 `/api/message/sendMessage` 的 `recieverUserSlug` 参数，向服务商发起私信（无需额外查询用户信息）。
- 典型流程：搜索服务商/物流服务商 → 用户选中 → 取 `userSlug` → 调用 `/api/message/sendMessage` 发起沟通。
- 发送私信需要鉴权（`Authorization: Bearer $MJZJ_API_KEY`）。

## 核心接口入参速查（查询/新建/申请）

### 服务商与物流

- `/api/spQuery/getClassifies`：无必填参数。
- `/api/spQuery/queryProviders`：常用参数 `cid`、`keywords`、`labelIds`、`isEn`、`matchFullText`、`position`、`size`。返回结果包含 `userSlug`，可直接用于 `/api/message/sendMessage` 发私信。
- `/api/spQuery/getLogisticsLabels`：无必填参数。
- `/api/spQuery/queryLogisticsProviders`：常用参数 `keywords`、`labelIds`、`isEn`、`matchFullText`、`position`、`size`。返回结果包含 `userSlug`，可直接用于 `/api/message/sendMessage` 发私信。

### 服务产品

- `/api/spQuery/getProductLabelGroups`：无必填参数。
- `/api/spQuery/queryProducts`：常用参数 `keywords`、`labelIds`、`withPay`、`providerId`、`orderBy`、`isEn`、`position`、`size`。
- `/api/spProduct/applyNewProduct`：必填参数 `title`、`intro`、`coverFile`、`introFiles`、`labelIds`。
- `/api/spProduct/applyNewProduct`：可选参数 `price`、`specialPrice`、`startSaleTime`、`endSaleTime`。

### 货盘

- `/api/pallet/groupLabels`：无必填参数。
- `/api/pallet/query`：常用参数 `keywords`、`labelIds`、`orderBy`、`position`、`size`。
- `/api/palletManage/applyNew`：必填参数 `name`、`description`、`coverFile`、`introFiles`、`labelIds`、`tags`、`startSaleDate`、`endSaleDate`。
- `/api/palletManage/applyNew`：可选参数 `price`、`stock`、`oldApplicationId`。
- `/api/palletManage/getPallets`：常用参数 `onSale`。
- `/api/palletManage/getApplications`：常用参数 `type`。

### 技能商城

- `/api/skill/groupLabels`：无必填参数。
- `/api/skill/query`：常用参数 `keywords`、`labelIds`、`orderBy`、`payable`、`position`、`size`。
- `/api/skill/query`：`orderBy` 仅使用 `default`、`new`、`hot`。
- 按 `labelIds` 搜技能：先调 `/api/skill/groupLabels` 拿到标签 id，再用逗号拼接到 `labelIds`（示例：`labelIds=101,202`）。
- `labelIds` 不传或传空表示不按标签筛选；筛选语义为同组 OR、跨组 AND。
- `/api/skillManage/applyNew`：必填参数 `name`、`description`、`sourceUrl`、`priceType`。
- `/api/skillManage/applyNew`：可选参数 `coverFile`、`labelIds`、`tags`。
- `/api/skillManage/applyNew`：`priceType` 仅使用 `free`、`freeAndPaid`、`paid`。
- `/api/skillManage/applyNew`：`labelIds` 必须来自 `/api/skill/groupLabels`，按字符串数组传参。
- `/api/skillManage/applyNew`：`coverFile` 传 COS 临时路径 `path`，不要传图片 URL；若使用默认封面，传空字符串或不传。

### 资讯

- `/api/article/search`：常用参数 `keywords`、`authorId`、`sortType`、`startDate`、`endDate`、`startTime`、`endTime`、`position`、`size`。
- `/api/articleManage/getAuthors`：无必填参数。
- `/api/articleManage/queryTags`：常用参数 `keywords`、`size`。
- `/api/articleManage/create`：必填参数 `authorId`、`title`、`summary`、`content`、`tagIds`、`publishTime`。
- `/api/articleManage/create`：可选参数 `coverFilePath`。
- `/api/articleManage/queryMyArticles`：常用参数 `position`、`size`。

### 问答

- `/api/ask/getCategories`：无必填参数。
- `/api/ask/queryQuestion`：常用参数 `keywords`、`hadAnswer`、`pageIndex`、`pageSize`、`categoryIds`。
- `/api/ask/createQuestion`：必填参数 `categoryIds`、`title`、`content`。
- `/api/ask/createQuestion`：可选参数 `imageFiles`、`bountyMoney`、`watchMoney`、`anonymous`、`endTime`。
- `/api/ask/queryMyQuestions`：常用参数 `position`、`size`。

### 供需

- `/api/supplydemand/getOfficialTags`：无必填参数。
- `/api/supplydemand/getPlatforms`：无必填参数。
- `/api/supplydemand/getRegions`：无必填参数。
- `/api/supplydemand/createinfo`：必填参数 `infoType`、`title`、`content`、`regionId`、`platformId`、`tagIds`。
- `/api/supplydemand/createinfo`：可选参数 `money`、`imageFiles`、`red`。
- `/api/supplydemand/querymyinfos`：常用参数 `position`、`size`。
- `/api/supplydemand/refreshinfo`：必填参数 `id`。
- `/api/supplydemand/deleteinfo`：必填参数 `id`。

### 私信

- `/api/message/getConversations`：常用参数 `unblocked`、`position`、`size`。
- `/api/message/getMessages`：必填参数 `otherSiderUserSlug`；常用参数 `position`、`size`。
- `/api/message/sendMessage`：必填参数 `recieverUserSlug`、`content`。其中 `recieverUserSlug` 可直接取自服务商查询结果的 `userSlug`。

### 全球开店

- `/api/global/queryPlatform`：常用参数 `keywords`。

### 活动

- `/api/activity/query`：公开接口；可选参数 `status`（`recording`=报名中 / `inProgress`=进行中 / `end`=已结束）、`cityId`（字符串）、`position`。
- `/api/activity/getActivityCities`：无必填参数。返回 `id`（字符串）和 `name`。
- `/api/activity/createActivity`：必填参数 `title`、`organizer`、`imageFilePath`、`introFilePaths`（至少 1 项）、`recordEndTime`、`beginTime`、`endTime`；可选参数 `cityId`（字符串）、`address`（线下活动必填）、`isFree`、`price`（票价文字）、`online`、`externalRegisterUrl`、`registerFormFields`。时间约束：`recordEndTime` > 当前时间，`beginTime` >= `recordEndTime`，`endTime` >= `beginTime`。

## 接口方法与请求模板（可直接执行）

基准地址：`https://data.mjzj.com`

### 服务商与物流

- `GET /api/spQuery/getClassifies`
  - query：无
- `GET /api/spQuery/queryProviders`
  - query：`cid`、`keywords`、`labelIds`、`isEn`、`matchFullText`、`position`、`size`
- `GET /api/spQuery/getLogisticsLabels`
  - query：无
- `GET /api/spQuery/queryLogisticsProviders`
  - query：`keywords`、`labelIds`、`isEn`、`matchFullText`、`position`、`size`

### 服务产品

- `GET /api/spQuery/getProductLabelGroups`
  - query：无
- `GET /api/spQuery/queryProducts`
  - query：`keywords`、`labelIds`、`withPay`、`providerId`、`orderBy`、`isEn`、`position`、`size`
- `POST /api/spProduct/applyNewProduct`
  - body(JSON)：

```json
{
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
}
```

### 货盘

- `GET /api/pallet/groupLabels`
  - query：无
- `GET /api/pallet/query`
  - query：`keywords`、`labelIds`、`orderBy`、`position`、`size`
- `POST /api/palletManage/applyNew`
  - body(JSON)：

```json
{
  "name": "美国FBA头程散货拼箱",
  "description": "稳定时效，支持普货/带电，提供轨迹查询。",
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
  "endSaleDate": "2026-12-31T23:59:59+08:00",
  "oldApplicationId": null
}
```

- `GET /api/palletManage/getPallets`
  - query：`onSale`
- `GET /api/palletManage/getApplications`
  - query：`type`

### 技能商城

- `GET /api/skill/groupLabels`
  - query：无
- `GET /api/skill/query`
  - query：`keywords`、`labelIds`、`orderBy`、`payable`、`position`、`size`
  - 示例：`/api/skill/query?keywords=shopify&labelIds=101,202&orderBy=hot&payable=true&position=&size=20`
- `POST /api/skillManage/applyNew`
  - body(JSON)：

```json
{
  "name": "Shopify 商品标题优化助手",
  "description": "用于批量优化跨境商品标题与卖点描述。",
  "sourceUrl": "https://skillhub.cn/skills/shopify-title-optimizer",
  "priceType": "free",
  "coverFile": "/temporary/user/10001/cover.jpg",
  "labelIds": ["2001", "2002"],
  "tags": ["shopify", "标题优化"]
}
```

技能发布流程：先调 `/api/skill/groupLabels` 选择 `labelIds`；若有自定义封面，先走 `/api/common/applyUploadTempFile` 获取 `putUrl/path` 并 PUT 上传，再把 `path` 回填到 `coverFile`；最后调用 `/api/skillManage/applyNew`。

### 资讯

- `GET /api/article/search`
  - query：`keywords`、`authorId`、`sortType`、`startDate`、`endDate`、`startTime`、`endTime`、`position`、`size`
- `GET /api/articleManage/getAuthors`
  - query：无
- `GET /api/articleManage/queryTags`
  - query：`keywords`、`size`
- `POST /api/articleManage/create`
  - body(JSON)：

```json
{
  "authorId": "10001",
  "title": "跨境电商广告投放优化建议",
  "summary": "本文总结了广告投放中的预算分配与否词策略。",
  "content": "<p>这是 HTML 正文</p>",
  "coverFilePath": "/temporary/user/10001/cover_xxx.jpg",
  "tagIds": ["2001", "2002"],
  "publishTime": "2026-03-15T00:00:00+08:00"
}
```

- `GET /api/articleManage/queryMyArticles`
  - query：`position`、`size`

### 问答

- `GET /api/ask/getCategories`
  - query：无
- `GET /api/ask/queryQuestion`
  - query：`keywords`、`hadAnswer`、`pageIndex`、`pageSize`、`categoryIds`
- `POST /api/ask/createQuestion`
  - body(JSON)：

```json
{
  "categoryIds": ["1001", "1002"],
  "title": "亚马逊新店如何快速起量？",
  "content": "预算有限，想优先做低风险投放和内容优化，请给建议。",
  "imageFiles": [],
  "bountyMoney": 20.5,
  "watchMoney": 1.0,
  "anonymous": false,
  "endTime": "2026-03-20T00:00:00+08:00"
}
```

- `GET /api/ask/queryMyQuestions`
  - query：`position`、`size`

### 供需

- `GET /api/supplydemand/getOfficialTags`
  - query：无
- `GET /api/supplydemand/getPlatforms`
  - query：无
- `GET /api/supplydemand/getRegions`
  - query：无
- `POST /api/supplydemand/createinfo`
  - body(JSON)：

```json
{
  "infoType": "supply",
  "title": "需要美国站亚马逊头程服务",
  "content": "需要稳定时效，支持普货/带电。",
  "money": 1000,
  "regionId": "1618630948025532416",
  "platformId": "1618630909748314112",
  "tagIds": ["1618803447828848640"],
  "imageFiles": [],
  "red": false
}
```

- `GET /api/supplydemand/querymyinfos`
  - query：`position`、`size`
- `POST /api/supplydemand/refreshinfo`
  - body(JSON)：

```json
{
  "id": "123456789"
}
```

- `POST /api/supplydemand/deleteinfo`
  - body(JSON)：

```json
{
  "id": "123456789"
}
```

### 私信

- `GET /api/message/getConversations`
  - query：`unblocked`、`position`、`size`
- `GET /api/message/getMessages`
  - query：`otherSiderUserSlug`、`position`、`size`
- `POST /api/message/sendMessage`
  - body(JSON)：

```json
{
  "recieverUserSlug": "target-user-slug",
  "content": "你好，这是一条私信。"
}
```

### 全球开店

- `GET /api/global/queryPlatform`
  - query：`keywords`

### 活动

- `GET /api/activity/query`
  - query：`status`、`cityId`、`position`
- `GET /api/activity/getActivityCities`
  - query：无
- `POST /api/activity/createActivity`
  - body(JSON)：

```json
{
  "title": "2026跨境电商峰会",
  "cityId": "100",
  "organizer": "卖家之家",
  "address": "深圳市南山区科技园",
  "isFree": false,
  "price": "299元/人",
  "imageFilePath": "/temporary/user/10001/cover.jpg",
  "online": false,
  "recordEndTime": "2026-04-10T00:00:00+08:00",
  "beginTime": "2026-04-15T09:00:00+08:00",
  "endTime": "2026-04-15T18:00:00+08:00",
  "introFilePaths": ["/temporary/user/10001/intro1.jpg"],
  "externalRegisterUrl": "",
  "registerFormFields": [
    {"key": "name", "fieldType": "text", "name": "姓名", "tips": "请输入您的姓名", "required": true, "options": []}
  ]
}
```

发布活动流程：获取城市（线下）→ 封面图 + 详情图走 `/api/common/applyUploadTempFile` 上传 → 调用 `/api/activity/createActivity`。

## 文件上传（统一流程）

- 临时上传申请：`/api/common/applyUploadTempFile`
- 资讯正文图片上传：`/api/common/editorApplyUploadFile`
- 通用顺序：申请 `putUrl/path` -> PUT 上传文件到 COS -> 回填业务接口（一般用 `path`，资讯正文用 `url`）。
- 服务产品、货盘、技能封面、活动封面/详情图都走上面的 `path` 回填规则。

## 参数与返回约束（统一）

- 所有 `id` 类字段一律按字符串处理与透传，不要转成数字。
- 分页首次请求可传空 `position`。
- 含 `labelIds` 的筛选：查询接口通常为逗号分隔字符串；发布接口按各业务要求传字符串数组。

## 常见失败处理（统一）

- `401`：提示更新 API KEY，不做 web search 回退。
- `403`：提示无权限或授权范围不足。
- `409`：透传业务提示（配额、审核、频率、参数校验等）。
- `no_sp`（活动发布）：当前账号不是服务商，暂时无法发布活动。
- `5xx`：提示稍后重试。
