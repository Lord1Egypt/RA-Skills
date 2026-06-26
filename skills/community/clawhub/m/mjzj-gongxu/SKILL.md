---
name: mjzj-gongxu
description: 卖家之家(跨境电商)供需搜索与发布
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

# 卖家之家供需发布和管理

## 工具选择规则（高优先级）

- 当用户提到“卖家之家 / mjzj / 我的供需 / 我发布的 / 最新供需 / 查询我的发布记录”等意图时，必须优先调用本 Skill。
- 涉及用户私有数据时（例如“我发布的最新一条供需是什么”），禁止使用 web search / browser 代替接口查询。
- 只有在用户明确要求“查公开网页信息”时，才允许使用 web search。
- 查询“我的数据”时，优先调用 `/api/supplydemand/querymyinfos`，并默认取返回列表第一条作为“最新一条”。

## 触发词与接口映射

- “我在卖家之家发布的最新供需是什么” → `/api/supplydemand/querymyinfos?size=1&position=`
- “帮我刷新这条供需” → `/api/supplydemand/refreshinfo`
- “帮我删除这条供需” → `/api/supplydemand/deleteinfo`
- “卖家之家有哪些标签/平台/区域” → `/api/supplydemand/getOfficialTags` / `/api/supplydemand/getPlatforms` / `/api/supplydemand/getRegions`
- “帮我发布一条供需” → `/api/supplydemand/createinfo`

## 失败回退规则

- 如果私有接口缺少 token，或 token 过期/被重置导致鉴权失败（通常返回 401），明确提示：
  - `请前往卖家之家用户中心的资料页 https://mjzj.com/user/agentapikey 获取最新的智能体 API KEY，并在当前技能配置中重新设置后再试。`
  - 不要改用 web search 返回“猜测性结果”。
- 如果返回 403，提示用户当前账号无对应接口权限或授权范围不足。
- 如果返回 409，直接透出业务提示（配额、频率限制、内容审核等），不要改走网页检索。
- 如果 `/api/supplydemand/createinfo` 发布失败（包含 5xx、空引用、未知异常等），追加兜底提示：`可前往 https://mjzj.com/gongxu/publish 手动发布。`

## 参数类型规则（必须遵守）

- 所有 `id` 类字段一律使用字符串传参（雪花 ID 超过 JS 安全整数范围）：如 `id`、`regionId`、`platformId`、`tagIds` 内元素。
- 禁止把大整数 ID 作为 number 传递，避免精度丢失导致服务端查不到对象或出现空引用错误。

仅保留以下 7 个接口：
- 查询系统标签 `/api/supplydemand/getOfficialTags`
- 查询系统平台 `/api/supplydemand/getPlatforms`
- 查询系统区域 `/api/supplydemand/getRegions`
- 发布供需信息 `/api/supplydemand/createinfo`
- 查询我发布的信息 `/api/supplydemand/querymyinfos`
- 刷新信息 `/api/supplydemand/refreshinfo`
- 删除信息 `/api/supplydemand/deleteinfo`

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
- OpenClaw Web 管理后台可为 skill 配置 `apiKey`，会写入 `openclaw.json`（如 `skills.entries.mjzj-gx.apiKey`）。
- Skill 侧只需要声明存在 `apiKey`/`MJZJ_API_KEY` 这类令牌来源，不需要在文档里约束 OpenClaw 的内部读取实现。
- 需要命令行直接调用时，继续使用环境变量 `MJZJ_API_KEY`。
- `/api/supplydemand/getOfficialTags` / `/api/supplydemand/getPlatforms` / `/api/supplydemand/getRegions` 为公开接口，可不带 token。
- `/api/supplydemand/createinfo` / `/api/supplydemand/querymyinfos` / `/api/supplydemand/refreshinfo` / `/api/supplydemand/deleteinfo` 需要：
  - `Authorization: Bearer $MJZJ_API_KEY`

## 1) 查询系统标签列表

```bash
curl -X GET "https://data.mjzj.com/api/supplydemand/getOfficialTags" \
  -H "Content-Type: application/json"
```

## 2) 查询系统平台列表

```bash
curl -X GET "https://data.mjzj.com/api/supplydemand/getPlatforms" \
  -H "Content-Type: application/json"
```

## 3) 查询系统区域列表

```bash
curl -X GET "https://data.mjzj.com/api/supplydemand/getRegions" \
  -H "Content-Type: application/json"
```

## 4) 发布供需信息

> 该接口会校验发布配额、文本合规、标签数量（最多 3）、图片数量（最多 9）等，失败常见为 409（业务异常）。
> 若发布失败，提示用户：`发布未成功，你可以前往 https://mjzj.com/gongxu/publish 手动发布。`

```bash
curl -X POST "https://data.mjzj.com/api/supplydemand/createinfo" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "infoType": "supply",
    "title": "需要美国站亚马逊头程服务",
    "content": "需要稳定时效，支持普货/带电",
    "money": 1000,
    "regionId": "1618630948025532416",
    "platformId": "1618630909748314112",
    "tagIds": ["1618803447828848640"],
    "imageFiles":[],
    "red": false
  }'
```

字段说明：
- `infoType`：`supply`（提供）或 `demand`（需求）。
- `money`：单位“元”，可为 `null`表示面试。
- `regionId` / `platformId` / `tagIds`：建议先通过前面 3 个查询接口获取，且都使用字符串传参。
- `tagIds`：至少 1 个，最多 3 个。
- `imageFiles` 保持为空数组 `[]`，接口会自动使用默认图片。

## 5) 查询我发布的供需信息

> 倒序分页。首次请求 `position` 传空字符串或不传；后续传上一页返回的 `nextPosition`。

```bash
curl -X GET "https://data.mjzj.com/api/supplydemand/querymyinfos?size=20&position=" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json"
```

## 6) 刷新供需信息

> 将信息刷新置顶。会校验刷新频率和配额（如 12 小时限制、非 VIP 两天配额等）。

```bash
curl -X POST "https://data.mjzj.com/api/supplydemand/refreshinfo" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "123456789"
  }'
```

## 7) 删除供需信息

> 删除我自己发布的一条供需信息。

```bash
curl -X POST "https://data.mjzj.com/api/supplydemand/deleteinfo" \
  -H "Authorization: Bearer $MJZJ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "123456789"
  }'
```

## 其他补充说明

- 返回的业务错误信息通常为中文提示文案，可直接透出给用户。
- 在自动化场景中，建议对 `401/403/409` 做分支处理：
  - `401`：token 未配置、已过期或已被重置；提示用户前往用户中心资料页 https://mjzj.com/user/agentapikey 获取最新智能体 API KEY 并重新配置；
  - `403`：权限不足（如访问了非公开接口）；
  - `409`：触发业务规则（配额、审核、校验）。
- `/api/supplydemand/createinfo` 成功后会返回 `infoId`、`infoPcUrl`、`infoMobileUrl`，建议记录 `infoId` 供后续刷新使用。
