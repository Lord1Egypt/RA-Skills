---
name: mjzj-ask
description: 卖家之家(跨境电商)问答搜索
homepage: https://mjzj.com/ask
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

# 卖家之家问答查询和发布

## 工具选择规则（高优先级）

- 当用户提到“卖家之家问答 / mjzj ask / 提问 / 问题分类 / 搜索问题 / 我发布的问题 / 我的问答”等意图时，必须优先调用本 Skill。
- 涉及用户私有数据时（例如“我发布的最新问题”），禁止使用 web search / browser 代替接口查询。
- 只有在用户明确要求“查公开网页信息”时，才允许使用 web search。
- 查询“我的问题”时，优先调用 `/api/ask/queryMyQuestions`，并默认取返回列表第一条作为“最新一条”。

## 触发词与接口映射

- “卖家之家问答有哪些分类 / 问答分类列表” → `/api/ask/getCategories`
- “帮我发一个问题 / 帮我提问” → `/api/ask/createQuestion`
- “搜一下问答 / 查找问题 / 查询有无回答的问题” → `/api/ask/queryQuestion`
- “我发布的问题 / 我的问答记录 / 我最近发的问题” → `/api/ask/queryMyQuestions`

仅开放以下 4 个 API 接口：
- 查询问答分类 `/api/ask/getCategories`
- 发布问题 `/api/ask/createQuestion`
- 查询问题列表 `/api/ask/queryQuestion`
- 查询我发布的问题 `/api/ask/queryMyQuestions`

## 失败回退规则

- 如果私有接口缺少 token，或 token 过期/被重置导致鉴权失败（通常返回 401），明确提示：
  - `请前往卖家之家用户中心的资料页 https://mjzj.com/user/agentapikey 获取最新的智能体 API KEY，并在当前技能配置中重新设置后再试。`
  - 不要改用 web search 返回“猜测性结果”。
- 如果返回 403，提示用户当前账号无对应接口权限或授权范围不足。
- 如果返回 409，直接透出业务提示（配额、频率限制、内容审核等），不要改走网页检索。
- 如果 `/api/ask/createQuestion` 发布失败（包含 5xx、空引用、未知异常等），追加兜底提示：`可前往 https://mjzj.com/ask/create 手动发布。`

## 参数类型规则（必须遵守）

- 所有 `id` 类字段一律使用字符串传参、读取与透传（雪花 ID 超过 JS 安全整数范围）：如 `id`、`categoryIds` 内元素、`position`、`nextPosition`。
- 禁止把任何雪花 ID 当作 number/int 处理，避免 OpenClaw 等调用端出现精度丢失。
- `/api/ask/createQuestion.categoryIds` 必须按字符串数组传参（例如 `["1001","1002"]`），服务端再解析为 `long`，且每项必须大于 0。
- `/api/ask/queryQuestion.categoryIds` 使用 query 参数传逗号分隔字符串：`categoryIds=1001,1002,1003`。
- `/api/ask/queryMyQuestions.position` 使用字符串游标；首次请求传空字符串或不传。

## Token 声明与读取（建议）

```bash
# 命令行直调时：可直接声明环境变量
export MJZJ_API_KEY="你的访问令牌"

# 防止空 token 发起请求
if [ -z "$MJZJ_API_KEY" ]; then
  echo "MJZJ_API_KEY 未设置" >&2
  exit 1
fi
```

说明：
- OpenClaw Web 管理后台可为 skill 配置 `apiKey`，会写入 `openclaw.json`（如 `skills.entries.mjzj-ask.apiKey`）。
- `/api/ask/getCategories`、`/api/ask/queryQuestion` 为公开接口，可不带 token。
- `/api/ask/createQuestion`、`/api/ask/queryMyQuestions` 需要：
  - `Authorization: Bearer $MJZJ_API_KEY`

## 1) 查询问答分类列表（/api/ask/getCategories）

```bash
curl -X GET "https://data.mjzj.com/api/ask/getCategories" \
  -H "Content-Type: application/json"
```

## 2) 发布问题（/api/ask/createQuestion）

> 该接口会校验发布配额、文本合规、分类数量（最多 3）、图片数量（最多 9）等，失败常见为 409（业务异常）。
> 若发布失败，提示用户：`发布未成功，你可以前往 https://mjzj.com/ask/create 手动发布。`

```bash
curl -X POST "https://data.mjzj.com/api/ask/createQuestion" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "categoryIds": ["1001", "1002"],
    "title": "亚马逊新店如何快速起量？",
    "content": "预算有限，想优先做低风险投放和内容优化，请给建议。",
    "imageFiles": [],
    "bountyMoney": 20.5,
    "watchMoney": 1.0,
    "anonymous": false,
    "endTime": "2026-03-15T00:00:00+08:00"
  }'
```

字段说明：
- `categoryIds`：至少 1 个，最多 3 个；每个 ID 都按字符串传参，且值必须大于 0。
- `bountyMoney`：单位元，必须大于等于 0。
- `watchMoney`：单位元，必须大于 0。
- `endTime`：截止日期需至少晚于当前日期 7 天。
- `imageFiles`：最多 9 张；无图可传空数组 `[]`。

## 3) 查询问题列表（/api/ask/queryQuestion）

```bash
curl -X GET "https://data.mjzj.com/api/ask/queryQuestion?keywords=亚马逊&hadAnswer=true&pageIndex=0&pageSize=20&categoryIds=1001,1002" \
  -H "Content-Type: application/json"
```

参数说明：
- `keywords`：关键字（可选）。
- `hadAnswer`：是否已有回答（可选，`true/false`）。
- `pageIndex`：页码，从 0 开始，默认 0。
- `pageSize`：每页数量，默认 20，最大 100。
- `categoryIds`：可选，逗号分隔分类 ID。

## 4) 查询我发布的问题（/api/ask/queryMyQuestions）

> 倒序游标分页。首次请求 `position` 传空字符串或不传；后续传上一页返回的 `nextPosition`。

```bash
curl -X GET "https://data.mjzj.com/api/ask/queryMyQuestions?size=20&position=" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

## 其他补充说明

- 返回的业务错误信息通常为中文提示文案，可直接透出给用户。
- 查询接口（如 `/api/ask/queryQuestion`、`/api/ask/queryMyQuestions`）返回问答信息时，需同时给出可访问链接，格式为：`https://mjzj.com/ask/question/{id}`。
  - 例如：问题 `id=1927616463812960256`，链接为 `https://mjzj.com/ask/question/1927616463812960256`。
- 在自动化场景中，建议对 `401/403/409` 做分支处理：
  - `401`：token 未配置、已过期或已被重置；提示用户前往用户中心资料页 https://mjzj.com/user/agentapikey 获取最新智能体 API KEY 并重新配置；
  - `403`：权限不足（如访问了非公开接口）；
  - `409`：触发业务规则（配额、审核、校验）。
- `/api/ask/createQuestion` 成功后会返回 `id`、`pcUrl`、`mobileUrl`，以及可能存在的 `bountyPayOrder`（当悬赏金额大于 0 时）。
