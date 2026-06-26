---
name: mjzj-article
description: 卖家之家(跨境电商)资讯搜索与发布
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

# 卖家之家资讯（搜索与发布）

## 工具选择规则（高优先级）

- 当用户提到“卖家之家资讯 / mjzj 资讯 / 文章 / 跨境电商资讯 / 搜索资讯 / 查询资讯 / 搜文章 / 我发布的文章 / 发布资讯”等意图时，必须优先调用本 Skill。
- 查询公开资讯列表时，优先使用 `/api/article/search`，该接口不需要用户登录。
- 涉及用户私有数据或写操作时（如“我发布的资讯”“发布文章”“查询我的笔名”），必须使用带鉴权的接口；不要用 web search 代替。
- 只有在用户明确要求“查公开网页信息”且不要求走业务接口时，才允许使用 web search / browser。

## 触发词与接口映射

- “查资讯 / 搜文章 / 跨境电商资讯” → `/api/article/search`
- “发布资讯 / 发布文章” → `/api/articleManage/create`
- “查标签 / 资讯标签” → `/api/articleManage/queryTags`
- “查我的笔名 / 我有哪些作者身份” → `/api/articleManage/getAuthors`
- “我发布的文章 / 我的资讯列表” → `/api/articleManage/queryMyArticles`
- “上传封面图（临时）” → `/api/common/applyUploadTempFile`
- “上传正文图片（正式 URL）” → `/api/common/editorApplyUploadFile`

仅开放以下 7 个接口：
- `/api/article/search`
- `/api/articleManage/create`
- `/api/articleManage/queryTags`
- `/api/articleManage/getAuthors`
- `/api/articleManage/queryMyArticles`
- `/api/common/applyUploadTempFile`
- `/api/common/editorApplyUploadFile`

## 鉴权规则

- `/api/article/search`：公开接口，可不带 token。
- 其余 6 个接口：需要
  - `Authorization: Bearer $MJZJ_API_KEY`

若缺少 token，或 token 过期/被重置导致 401，提示：

`请前往卖家之家用户中心的资料页 https://mjzj.com/user/agentapikey 获取最新的智能体 API KEY，并在当前技能配置中重新设置后再试。`

## 参数与类型规则（必须遵守）

- 所有 `id` 类字段一律使用字符串传参、读取与透传（雪花 ID 超过 JS 安全整数范围）：如 `id`、`authorId`、`tagIds` 内元素、`position`、`nextPosition`。
- 禁止把任何雪花 ID 当作 number/int 处理，避免 OpenClaw 等调用端出现精度丢失。
- `/api/articleManage/create.authorId` 必须按字符串传参，值需可解析为 `int64` 且大于 0。
- `/api/articleManage/create.tagIds` 必须按**字符串数组**传参（例如 `['2001','2002']`），至少 1 个，避免 long 在部分调用端精度丢失。
- `/api/articleManage/create.content` 必须是 **HTML 格式**。
- `/api/articleManage/create.coverFilePath` 可空 **临时文件路径 path**（来自 `/api/common/applyUploadTempFile` 返回的 `path`），不是 URL。
- 若正文 HTML 内有图片，所有图片都必须先走 `/api/common/editorApplyUploadFile` 上传，使用返回的 `url` 替换到 HTML 对应位置（不要直接用外链）。
- `/api/articleManage/create.publishTime` 必须大于或等于当天日期。
- `/api/articleManage/queryMyArticles.position` 为字符串游标，首次可传空字符串或不传。

## 发布资讯标准流程（必须按顺序）

1. 调用 `/api/articleManage/getAuthors`，让用户选择 `authorId`。
2. 调用 `/api/articleManage/queryTags` 选择 `tagIds`：优先自动从文章中提取 2-4 个相关关键词并匹配标签；若匹配不足再让用户补选（至少 1 个）。
3. 封面处理：
  - 如果文章中有图片：下载图片文件，调用 `/api/common/applyUploadTempFile` 获取 `putUrl` 和 `path`，再使用 `putUrl` 上传到 COS，最后将该 `path` 作为 `/api/articleManage/create.coverFilePath`。
  - 如果文章没有图片：`/api/articleManage/create.coverFilePath` 传空。
4. 处理正文图片（逐张执行）：
  - 先解析正文 HTML，找出所有图片地址（包含 `img data-src`、`img src`、`srcset`）；同一 `img` 若同时存在 `data-src` 与 `src`，优先使用 `data-src`（`src` 作为兜底）；
  - 对每一张图片分别下载文件；
  - 对每个图片文件调用 `/api/common/editorApplyUploadFile`，获取该图片对应的 `putUrl` 和 `url`；
  - 使用该 `putUrl` 将图片文件上传到 COS；
  - 上传成功后，统一将新地址写入 `img src`；若原标签有 `data-src`/`srcset`，不再保留其外站地址（可清空或移除），避免系统继续读取旧地址；
  - 替换时只需保留原 `style`，避免样式丢失；
  - 建议在全部图片替换完成后，再提交 `/api/articleManage/create`。
5. 调用 `/api/articleManage/create` 发布文章（`content` 为 HTML，`coverFilePath` 用 path，`tagIds` 按字符串数组传参，`authorId` 按字符串传参，且 `publishTime` 合法）。

## 发布前检查建议（推荐）

- 如果正文检测到图片 URL，建议先完成“逐张上传 + 逐张替换”后再发布。
- 建议检查：`发现的图片数量` 与 `成功替换数量` 是否一致，避免遗漏替换。
- 若某张图片下载或上传失败，建议先提示失败图片与原因，再决定是否继续发布。

## 失败回退规则

- `401`：token 缺失、过期或被重置，按上文提示用户更新 API KEY；不要改走 web search。
- `403`：账号无接口权限或授权范围不足。
- `409`：直接透出业务提示（配额、频率、审核或参数校验）。
- 发布场景命中业务码时，优先按业务码提示：
  - `not_editor`：当前账号没有专栏发布权限。请明确提示：`您还没有专栏权限，请先入驻专栏：https://mjzj.com/user/authorapplication`。
  - `not_editor_of_author`：当前账号不是该笔名的编辑，提示用户切换已绑定笔名或先完成授权。
- `/api/articleManage/create` 失败（含 5xx/未知异常）：提示用户稍后重试，并可在卖家之家资讯发布页面手动发布。

## 发布权限提示模板（建议直接复用）

- 当发布接口返回“无专栏权限”或业务码 `not_editor` 时，固定提示：
  - `当前账号没有专栏发布权限，暂时无法发布资讯。请先入驻专栏：https://mjzj.com/user/authorapplication`
- 当返回业务码 `not_editor_of_author` 时，提示：
  - `您没有权限为该笔名发布文章，请选择您已绑定的笔名后重试。`

## 接口示例

### 1) 查询资讯（公开）

```bash
curl -X GET "https://data.mjzj.com/api/article/search?keywords=亚马逊&size=20&position=" \
  -H "Content-Type: application/json"
```

可选参数示例：`authorId`、`sortType`、`startDate`、`endDate`、`startTime`、`endTime`。

### 2) 查询我的笔名

```bash
curl -X GET "https://data.mjzj.com/api/articleManage/getAuthors" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

### 3) 查询标签

```bash
curl -X GET "https://data.mjzj.com/api/articleManage/queryTags?keywords=&size=15" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

### 4) 申请上传临时文件（封面）

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

返回中的 `path` 用于 `/api/articleManage/create.coverFilePath`。

上传文件到 `putUrl` 示例：

```bash
curl -X PUT "<putUrl>" \
  -H "Content-Type: image/jpeg" \
  --upload-file ./cover.jpg
```

### 5) 编辑人员上传正式文件（正文图片）

```bash
curl -X POST "https://data.mjzj.com/api/common/editorApplyUploadFile" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileName": "content-image.png",
    "contentType": "image/png",
    "fileLength": 102400
  }'
```

返回中的 `url` 可插入正文 HTML。

说明：正文 HTML 中出现的图片，应统一先上传到 `/api/common/editorApplyUploadFile`，再使用返回 `url` 替换原图片地址。

### 6) 发布资讯（内容必须为 HTML）

```bash
curl -X POST "https://data.mjzj.com/api/articleManage/create" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "authorId": "10001",
    "title": "跨境电商广告投放优化建议",
    "summary": "本文总结了广告投放中的预算分配与否词策略。",
    "content": "<p>这是 HTML 正文</p><p><img src=\"https://xxx.example.com/a.png\" /></p>",
    "coverFilePath": "/temporary/user/10001/abc.jpg",
    "tagIds": ["2001", "2002"],
    "publishTime": "2026-03-05T00:00:00+08:00"
  }'
```

### 7) 查询我发布的资讯

```bash
curl -X GET "https://data.mjzj.com/api/articleManage/queryMyArticles?size=20&position=" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

## COS 上传注意事项（封面）

- `/api/common/applyUploadTempFile` 返回 `putUrl` 后，上传时使用 `PUT` 直传该 `putUrl`。
- `PUT` 请求头 `Content-Type` 必须与申请上传时的 `contentType` 完全一致（例如申请 `image/jpeg`，上传也必须是 `image/jpeg`）。
- 上传成功后，发布接口 `/api/articleManage/create.coverFilePath` 传 `path`，不要传 `url`。
- 如果出现 `SignatureDoesNotMatch`，优先检查 `Content-Type` 是否一致。

## 提示词补充（两部分，可直接复用）

### Part 1：意图路由提示词（让 Agent 选中本 Skill）

当用户问题涉及“卖家之家资讯、跨境电商资讯、文章查询、文章发布、我发布的资讯、我的笔名、资讯标签”时，优先选择 `mjzj-article`。  
若是公开资讯检索，先调用 `/api/article/search`；若涉及我的数据或发布操作，必须走 `/api/articleManage/*` 与 `/api/common/*` 对应接口并携带 token，不要改用网页搜索替代。

### Part 2：发布流程执行提示词（让 Agent 按正确步骤调用）

执行“发布资讯”时，请直接遵循上文 `发布资讯标准流程（必须按顺序）`。  
执行要点：
- 标签尽量自动从文章提取 2-4 个关键词匹配；不足再请用户补选。
- 封面有图则走 `/api/common/applyUploadTempFile`（`putUrl` 上传、`path` 回填 `coverFilePath`），无图则 `coverFilePath` 为空。
- 正文HTML如有 `<img>` 图片标签：需识别 `img data-src`、`img src`、`srcset`；同一 `img` 同时存在时优先取 `data-src`，逐张转存到 COS 后用返回 `url` 替换该标签图片地址；替换后统一写回 `img src`，并避免保留外站 `data-src/srcset`，需保留原标签的 `style`。
- 发布前建议检查图片“发现数量”和“替换数量”是否一致。
- 入参约束保持不变：`content` 为 HTML，`tagIds` 用字符串数组，`PUT` 上传时 `Content-Type` 与申请值一致。
