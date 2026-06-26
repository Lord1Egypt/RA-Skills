---
name: mjzj-activity
description: 卖家之家(跨境电商)活动查询与发布
homepage: https://mjzj.com/activity
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

# 卖家之家活动（查询与发布）

## 工具选择规则（高优先级）

- 当用户提到"卖家之家活动 / mjzj 活动 / 跨境电商活动 / 查活动 / 搜活动 / 发布活动 / 创建活动 / 活动城市"等意图时，必须优先调用本 Skill。
- 查询公开活动列表时，优先使用 `/api/activity/query`，该接口不需要用户登录。
- 涉及写操作时（如"发布活动""创建活动"），必须使用带鉴权的接口；不要用 web search 代替。
- 只有在用户明确要求"查公开网页信息"且不要求走业务接口时，才允许使用 web search / browser。

## 触发词与接口映射

- "查活动 / 搜活动 / 跨境电商活动 / 活动列表" → `/api/activity/query`
- "活动城市 / 城市列表" → `/api/activity/getActivityCities`
- "发布活动 / 创建活动" → `/api/activity/createActivity`
- "上传封面图或详情图（临时）" → `/api/common/applyUploadTempFile`

仅开放以下 4 个接口：
- `/api/activity/query`
- `/api/activity/getActivityCities`
- `/api/activity/createActivity`
- `/api/common/applyUploadTempFile`

## 鉴权规则

- `/api/activity/query`：公开接口，可不带 token。
- 其余 3 个接口：需要
  - `Authorization: Bearer $MJZJ_API_KEY`

若缺少 token，或 token 过期/被重置导致 401，提示：

`请前往卖家之家用户中心的资料页 https://mjzj.com/user/agentapikey 获取最新的智能体 API KEY，并在当前技能配置中重新设置后再试。`

## 参数与类型规则（必须遵守）

- 所有 `id` 类字段一律使用字符串传参（雪花 ID 超过 JS 安全整数范围）：如 `id`、`cityId`。
- 禁止把大整数 ID 作为 number 传递，避免精度丢失导致服务端查不到对象或出现空引用错误。
- `/api/activity/query.status`（可选，字符串）：`"recording"`=报名中、`"inProgress"`=进行中、`"end"`=已结束；不传则返回全部。
- `/api/activity/query.cityId`（可选，字符串），来源于 `/api/activity/getActivityCities` 返回的 `id`。
- `/api/activity/query.position` 为整数分页游标，首次传 `0` 或不传。
- `/api/activity/createActivity` 中：
  - `title`（必填）：活动标题。
  - `organizer`（必填）：主办方。
  - `address`：活动地址；线下活动时必填（`online=false`）。
  - `cityId`（可选，字符串）：活动城市 ID。
  - `isFree`（bool）：是否免费。
  - `price`（string）：票价文字，非免费时建议填写。
  - `online`（bool）：是否线上活动。
  - `imageFilePath`（必填）：活动封面图的 COS 临时路径（来自 `/api/common/applyUploadTempFile` 返回的 `path`）。
  - `introFilePaths`（必填，字符串数组，至少 1 项）：活动详情图的 COS 临时路径列表，每项来自 `/api/common/applyUploadTempFile` 返回的 `path`。
  - `recordEndTime`（DateTime，必填）：报名截止时间，必须大于当前时间。
  - `beginTime`（DateTime，必填）：活动开始时间，必须大于等于 `recordEndTime`。
  - `endTime`（DateTime，必填）：活动结束时间，必须大于等于 `beginTime`。
  - `externalRegisterUrl`（可选）：外部报名链接。
  - `registerFormFields`（可选数组）：自定义报名表单字段，每项包含 `key`（字段标识）、`fieldType`（传 `"text"` / `"radio"` / `"checkbox"`）、`name`（字段名）、`tips`（提示文字）、`required`（bool）、`options`（radio/checkbox 时的选项列表）。

## 发布活动标准流程（必须按顺序）

1. 调用 `/api/activity/getActivityCities` 获取城市列表，让用户选择 `cityId`（线上活动可跳过）。
2. 封面图处理：
   - 下载封面图文件，调用 `/api/common/applyUploadTempFile` 获取 `putUrl` 和 `path`。
   - 使用 `putUrl` 将图片 PUT 上传到 COS。
   - 将 `path` 作为 `createActivity.imageFilePath`。
3. 活动详情图处理（逐张执行）：
   - 对每张详情图分别下载文件。
   - 对每张图调用 `/api/common/applyUploadTempFile`，获取 `putUrl` 和 `path`。
   - 使用 `putUrl` 将图片上传到 COS。
   - 收集所有 `path` 作为 `createActivity.introFilePaths`。
4. 调用 `/api/activity/createActivity` 发布活动。

## 发布前检查建议（推荐）

- 检查时间顺序：`recordEndTime` < `beginTime` < `endTime`，且 `recordEndTime` 大于当前时间。
- 线下活动时 `address` 不能为空。
- `introFilePaths` 至少包含 1 项，且不含空字符串。
- 建议检查：`发现的详情图数量` 与 `成功上传数量` 是否一致。

## 失败回退规则

- `401`：token 缺失、过期或被重置，按上文提示用户更新 API KEY；不要改走 web search。
- `403`：账号无接口权限或授权范围不足。
- `no_sp`：当前账号不是服务商，无权限发布活动。请提示：`当前账号不是服务商，暂时无法发布活动。`
- 发布接口失败（含 5xx/未知异常）：提示用户稍后重试，并可在卖家之家活动页面手动发布。

## 权限提示模板（建议直接复用）

- 当发布接口返回 `no_sp` 时，固定提示：
  - `当前账号不是服务商，暂时无法发布活动。`

## 接口示例

### 1) 查询活动（公开）

```bash
curl -X GET "https://data.mjzj.com/api/activity/query?status=recording&cityId=&position=" \
  -H "Content-Type: application/json"
```

可选参数：`status`（传 `recording` / `inProgress` / `end`）、`cityId`（字符串）、`position`（分页游标）。

返回字段说明：
- `list`：活动列表，每项包含 `id`（字符串）、`title`、`cityId`（字符串）、`cityName`、`organizer`、`address`、`isFree`、`price`、`url`（PC 详情链接）、`mobileUrl`（移动端链接）、`imageUrl`（封面图）、`online`（是否线上）、`status`（`recording`=报名中 / `inProgress`=进行中 / `end`=已结束 / `recordEnd`=报名已结束）、`statusName`、`recordEndTime`、`beginTime`、`endTime`。
- `nextPosition`：下一页游标，为 `null` 时表示没有更多数据。

### 2) 查询活动城市

```bash
curl -X GET "https://data.mjzj.com/api/activity/getActivityCities" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

返回字段：每项包含 `id`（城市 ID，字符串）和 `name`（城市名称）。

### 3) 申请上传临时文件（封面 / 详情图）

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

返回中的 `path` 用于 `createActivity.imageFilePath` 或 `createActivity.introFilePaths`。

上传文件到 `putUrl` 示例：

```bash
curl -X PUT "<putUrl>" \
  -H "Content-Type: image/jpeg" \
  --upload-file ./cover.jpg
```

### 4) 发布活动

```bash
curl -X POST "https://data.mjzj.com/api/activity/createActivity" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
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
    "introFilePaths": ["/temporary/user/10001/intro1.jpg", "/temporary/user/10001/intro2.jpg"],
    "externalRegisterUrl": "",
    "registerFormFields": [
      {
        "key": "name",
        "fieldType": "text",
        "name": "姓名",
        "tips": "请输入您的姓名",
        "required": true,
        "options": []
      },
      {
        "key": "company",
        "fieldType": "text",
        "name": "公司名称",
        "tips": "请输入公司名称",
        "required": false,
        "options": []
      }
    ]
  }'
```

## COS 上传注意事项

- `/api/common/applyUploadTempFile` 返回 `putUrl` 后，上传时使用 `PUT` 直传该 `putUrl`。
- `PUT` 请求头 `Content-Type` 必须与申请上传时的 `contentType` 完全一致。
- 上传成功后，发布接口传 `path`，不要传 `url`。
- 如果出现 `SignatureDoesNotMatch`，优先检查 `Content-Type` 是否一致。

## 提示词补充

### Part 1：意图路由提示词（让 Agent 选中本 Skill）

当用户问题涉及"卖家之家活动、跨境电商活动、活动查询、活动发布、活动城市"时，优先选择 `mjzj-activity`。
若是公开活动检索，先调用 `/api/activity/query`；若涉及发布操作，必须走 `/api/activity/createActivity` 并携带 token，不要改用网页搜索替代。

### Part 2：发布流程执行提示词（让 Agent 按正确步骤调用）

执行"发布活动"时，请直接遵循上文 `发布活动标准流程（必须按顺序）`。
执行要点：
- 线下活动先通过 `/api/activity/getActivityCities` 选城市。
- 封面图走 `/api/common/applyUploadTempFile`（`putUrl` 上传、`path` 回填 `imageFilePath`）。
- 详情图逐张走 `/api/common/applyUploadTempFile`，收集所有 `path` 回填 `introFilePaths`。
- 时间约束：`recordEndTime` > 当前时间，`beginTime` >= `recordEndTime`，`endTime` >= `beginTime`。
- `PUT` 上传时 `Content-Type` 与申请值一致。
