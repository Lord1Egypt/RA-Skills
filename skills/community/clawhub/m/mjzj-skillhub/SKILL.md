---
name: mjzj-skillhub
description: 卖家之家(跨境电商)技能商城(skillhub/clawhub/搜技能/热门技能/免费技能/付费技能)
homepage: https://skillhub.mjzj.com
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

# 卖家之家技能商城（SkillHub）

## 工具选择规则（高优先级）

- 当用户提到“技能商城 / 搜技能 / 技能标签筛选 / 免费技能 / 付费技能 / 热门技能 / 最新技能 / 安装某个技能 / 申请发布技能”等意图时，优先使用本 Skill。
- 公开查询统一使用 /api/skill/groupLabels 与 /api/skill/query，不要用 web search 代替业务接口。
- 涉及“申请发布技能、提交技能审核”时，必须使用带鉴权接口：/api/skillManage/applyNew。
- 若用户要自定义技能封面，必须先走 /api/common/applyUploadTempFile，再把返回的 path 传给 /api/skillManage/applyNew.coverFile。

## 触发词与接口映射

- 查技能标签分组 -> /api/skill/groupLabels
- 搜技能或筛选技能 -> /api/skill/query
- 申请发布技能或提交技能审核 -> /api/skillManage/applyNew
- 上传技能封面图（临时） -> /api/common/applyUploadTempFile

仅开放以下 4 个接口：
- /api/skill/groupLabels
- /api/skill/query
- /api/skillManage/applyNew
- /api/common/applyUploadTempFile

## 鉴权规则

- /api/skill/groupLabels、/api/skill/query：公开接口，可不带 token。
- /api/skillManage/applyNew、/api/common/applyUploadTempFile：需要
  - Authorization: Bearer $MJZJ_API_KEY

若缺少 token，或 token 过期/被重置导致 401，提示：

请前往卖家之家用户中心的资料页 https://mjzj.com/user/agentapikey 获取最新的智能体 API KEY，并在当前技能配置中重新设置后再试。

## 参数与类型规则（必须遵守）

- 所有雪花 ID 一律按字符串传参、读取与透传，如 `id`、`labelIds` 内元素、`nextPosition`；禁止当作 number/int 处理，避免精度丢失。
- /api/skill/query 的 labelIds 使用逗号分隔字符串，例如 `1001,1002,2003`。
- /api/skillManage/applyNew 的 labelIds 使用字符串数组，例如 `["2001", "2002"]`。
- /api/skillManage/applyNew 的 priceType 取值仅为：`free`、`freeAndPaid`、`paid`。
- /api/skillManage/applyNew 的 coverFile 传 COS 临时路径 path，不传 URL；若使用默认封面，传空字符串或不传。

## 查询参数关系（必须遵守）

### 1) /api/skill/groupLabels 与 /api/skill/query.labelIds

- /api/skill/groupLabels 返回技能标签分组，每个分组包含 labels[].id。
- /api/skill/query 的 labelIds 必须来自这个接口，多个 id 用逗号拼接。
- 筛选语义：同一分组内 OR，不同分组间 AND。

### 2) /api/skill/query 参数规则

- orderBy 仅使用：default、new、hot。
- position：字符串页码游标，首次可传空字符串或不传。
- pageIndex 最大 100；当 position 超过该范围时会按 100 处理。
- size：1 到 100，超范围会回退到 20。
- keywords：服务端会先 trim。
- payable=true：仅返回付费技能（PriceType != Free）。
- payable=false：仅返回免费技能（PriceType == Free）。
- payable 不传：不过滤付费类型。
- 返回 nextPosition 为空表示无下一页。

## 技能申请发布（/api/skillManage/applyNew）规则

### 入参约束（本 Skill 强制）

- name、description、sourceUrl、priceType 必填。
- coverFile 可选；自定义封面时传 COS 临时路径 path，若使用默认封面则传空字符串或不传。
- tags 可选；若传入则每项都必须是非空字符串。
- labelIds 仅可从 /api/skill/groupLabels 返回结果的 labels[].id 中选择。
- priceType 仅可传 `free`、`freeAndPaid`、`paid`。
- 不要在本 Skill 中暴露或传递 oldApplicationId。

### coverFile 上传规则（必须）

- 若用户未提供自定义封面，`coverFile` 直接传空字符串或不传。
- 若用户提供自定义封面，先调用 /api/common/applyUploadTempFile 获取 `putUrl` 和 `path`。
- 用 `PUT` 直传图片到 `putUrl`，且 `Content-Type` 必须与申请上传时一致。
- 上传成功后，把返回的 `path` 回填到 `coverFile`；不要传图片 URL。

### labelIds 选择规则（必须）

- 先调用 /api/skill/groupLabels。
- 从返回分组中选择标签，并把选中的 labels[].id 组装为 labelIds 字符串数组。
- 不要自行猜测或硬编码标签 ID。

### 提交流程

- 先调用 /api/skill/groupLabels 获取可选标签。
- 若需要自定义封面，先调用 /api/common/applyUploadTempFile 并完成 COS PUT 上传，拿到 `coverFile` 所需的 `path`。
- 组装 /api/skillManage/applyNew 请求体。
- 调用 /api/skillManage/applyNew 提交后进入后台审核，不是即时正式发布。

## 返回字段使用建议

- source：技能来源（clawhub 或 skillhub），由 sourceUrl 解析得到。
- slug：从 sourceUrl 提取的技能标识（通常是 URL 最后一个 path segment）。
- installSkillPrompt：后端已生成安装提示文案；用户问“怎么安装这个技能”时，优先直接复用该字段。

## 失败回退规则

- 401：token 缺失、过期或被重置，提示用户更新 API KEY；不要改走 web search。
- 403：账号无权限或未登录态授权范围不足。
- 409：透传业务提示（参数校验、审核规则等）。
- 400（参数错误，如 position 非数字）：提示用户修正参数后重试。
- 查询失败（含 5xx/未知异常）：提示稍后重试。
- /api/common/applyUploadTempFile 失败（含 5xx/未知异常）：提示稍后重试。
- /api/skillManage/applyNew 失败（含 5xx/未知异常）：提示稍后重试。

## 接口示例

### 1) 获取技能标签分组（公开）

```bash
curl -X GET "https://data.mjzj.com/api/skill/groupLabels" \
  -H "Content-Type: application/json"
```

### 2) 查询技能列表（公开）

```bash
curl -X GET "https://data.mjzj.com/api/skill/query?keywords=shopify&labelIds=101,202&orderBy=hot&payable=true&position=&size=20" \
  -H "Content-Type: application/json"
```

分页示例（继续下一页）：

```bash
curl -X GET "https://data.mjzj.com/api/skill/query?keywords=shopify&labelIds=101,202&orderBy=hot&payable=true&position=1&size=20" \
  -H "Content-Type: application/json"
```

### 3) 申请发布技能（需审核）

自定义封面时，先申请上传临时文件：

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

上传文件到 `putUrl`：

```bash
curl -X PUT "<putUrl>" \
  -H "Content-Type: image/jpeg" \
  --upload-file ./cover.jpg
```

然后把返回的 `path` 作为 `coverFile` 提交：

```bash
curl -X POST "https://data.mjzj.com/api/skillManage/applyNew" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Shopify 商品标题优化助手",
    "description": "用于批量优化跨境商品标题与卖点描述。",
    "sourceUrl": "https://skillhub.cn/skills/shopify-title-optimizer",
    "priceType": "free",
    "coverFile": "/temporary/user/10001/cover.jpg",
    "labelIds": ["2001", "2002"],
    "tags": ["shopify", "标题优化"]
  }'
```

## 提示词补充（可直接复用）

当用户问题涉及技能商城搜索、标签筛选、热门/最新排序、免费/付费筛选、技能安装引导、申请发布技能时，优先选择 mjzj-skillhub。
执行顺序建议：搜索场景先调用 /api/skill/groupLabels 获取可选标签，再调用 /api/skill/query；发布场景先调用 /api/skill/groupLabels 选标签，若有自定义封面则调用 /api/common/applyUploadTempFile + PUT 上传，最后调用 /api/skillManage/applyNew；若用户要安装某个技能，优先使用返回结果中的 installSkillPrompt 给出安装指引。
