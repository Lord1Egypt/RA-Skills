# Temu 店铺研究 API 参考

## 调用规范

- **请求地址（店铺搜索）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/mallSearch`
- **请求地址（站点列表）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/siteList`
- **请求地址（品类列表）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/categoryList`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退到兼容键 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`（未设置时为空串）
- **超时**：150s

> 业务入口脚本默认仅缓存成功响应 24 小时，成功的空结果也可缓存；HTTP 或业务失败不缓存。`--inline` 不绕过缓存；`--no-cache` 跳过缓存读写并强制真实请求，店铺搜索可能再次扣算力，站点/品类列表仅强制刷新。

> 上述地址是 LinkFox 工具网关路由。服务端再调用上游 GET API；客户端不得把上游 `/api/v1/temu/...` 路径当作网关地址。

## 公共响应字段

| 字段 | 类型 | 已验证成功值 | 说明 |
|---|---|---|---|
| `errcode` | integer | `200` | 网关业务状态码；仍须检查，不应只看 HTTP 成功 |
| `errmsg` | string | `ok` | 网关业务状态消息 |

真实链路验证摘要：站点列表返回 33 个站点；一级品类返回 23 个节点；使用 `regionId=211`、`page=1`、`size=3`、`mallStarMin=4` 搜索返回 3 条非空店铺，上游 `total=10000`。

每个列定义通常包含 `field`, `title`, `cellType`, `sortable`, `filterable`；`cellType` 常见为 `number` 或 `text`。

## 端点

### 店铺搜索：`POST /geekbi/temu/mallSearch`

#### 请求

POST Body（JSON）。所有字段均可选；空对象 `{}` 使用 `regionId=211`、`page=1`、`size=20`。

##### 分页、关键词、品类与托管模式

| 参数 | 类型 | 必填 | 默认值 / 约束 | 说明 |
|---|---|---:|---|---|
| `regionId` | integer | 否 | `211`；`>=1` | Temu 地区 ID；应取自站点列表 `sites[].regionId` |
| `page` | integer | 否 | `1`；`>=1` | 页码 |
| `size` | integer | 否 | `20`；`1..200` | 每页数量；`page * size` 不得超过 10000 |
| `keyword` | string | 否 | 最大 300 字符 | 匹配店铺名关键词 |
| `catIds` | integer[] | 否 | - | 品类 ID 数组；元素取自品类列表 `categories[].catId` |
| `hostingMode` | integer | 否 | `1..2` | `1`=全托管，`2`=半托管 |
| `sort` | string | 否 | 最大 100 字符 | 排序字段；仅使用接口确认支持的字段 |
| `order` | string | 否 | `asc` 或 `desc` | 排序方向，不区分大小写 |

网关 JSON 中 `catIds` 必须传数组，例如 `{"catIds":[1,27011]}`。服务端会把数组编码为上游单个英文逗号参数；不要在 JSON 中传逗号字符串，也不要传重复键。

##### 店铺指标范围

| 参数组 | 类型 | 约束 / 单位 |
|---|---|---|
| `mallSoldMin`, `mallSoldMax` | integer | 店铺历史累计总销量，`>=0` |
| `mallSalesMin`, `mallSalesMax` | number | 店铺历史累计总销售额，当前站点货币，`>=0` |
| `mallStarMin`, `mallStarMax` | number | 店铺评分，`0..5` |
| `reviewNumMin`, `reviewNumMax` | integer | 店铺历史累计评论数，`>=0` |
| `goodsNumMin`, `goodsNumMax` | integer | 店铺在售商品数，`>=0` |
| `followerNumMin`, `followerNumMax` | integer | 店铺粉丝数，`>=0` |
| `avgPriceMin`, `avgPriceMax` | number | 店铺平均客单价，当前站点货币，`>=0` |

所有成对的 `*Min` 都不得大于对应的 `*Max`。

##### 开店时间

| 参数组 | 类型 | 说明 |
|---|---|---|
| `mallOpenTimeMin`, `mallOpenTimeMax` | string | 店铺开店时间范围，ISO-8601 date-time，最大 40 字符 |

当最小和最大时间同时提供时，二者都必须为合法 ISO-8601 date-time，且最小值不得晚于最大值。

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/mallSearch" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"regionId":211,"page":1,"size":3,"mallStarMin":4}'
```

#### 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `items` | array | 当前页店铺；每个业务字段都可能缺失或为 `null` |
| `columns` | array | 渲染列定义；真实响应为 49 个定义 |
| `total` | integer | 上游报告的匹配总数；服务限制可访问窗口 `page * size <= 10000` |
| `page` | integer | 当前页码 |
| `size` | integer | 每页数量 |
| `regionId` | integer | 本次请求使用的地区 ID |
| `title` | string | `Temu 数据查询` |
| `sourceType` | string | `temu` |
| `sourceTool` | string | `geekbi_temu` |
| `type` | string | `tableListWorkbenches` |

##### 店铺字段 `items[]`

| 字段组 | 字段 |
|---|---|
| 标识与基础信息 | `id`, `mallId`, `mallLogo`, `mallName`, `regionId`, `hot` |
| 品类 | `catIds`, `catItems` |
| 核心表现 | `mallStar`, `reviewNum`, `goodsNum`, `followerNum`, `mallSold`, `mallSales`, `avgPrice` |
| 托管与时间 | `hostingMode`, `mallOpenTime`, `createTime`, `updateTime` |
| 粉丝变化 | `dayFollower`, `weekFollower`, `monthFollower` 及对应 `*Rate` |
| 商品数变化 | `dayItemCount`, `weekItemCount`, `monthItemCount` 及对应 `*Rate` |
| 销售额 | `daySales`, `weekSales`, `monthSales` 及对应 `*Rate` |
| 动销 | `daySellthroughCount`, `weekSellthroughCount`, `monthSellthroughCount` 及对应 `*Rate` |
| 销量 | `daySold`, `weekSold`, `monthSold` 及对应 `*Rate` |
| 上游扩展 | `extraFields`；仅上游出现尚未进入固定契约的字段时返回 |

`catItems[]` 可含 `catId`, `catLevel`, `catName`, `isLeaf`, `parentCatId`, `extraFields`。金额字段按当前站点货币解释；时间字段保持上游字符串格式；所有业务字段均允许缺失或为 `null`。

以下示例按 2026-08-27 的真实成功响应确认字段层级，具体业务值仅用于说明；可空字段可能省略。

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "total": 10000,
  "page": 1,
  "size": 3,
  "regionId": 211,
  "items": [
    {
      "mallId": "634418224987870",
      "mallName": "cazan",
      "mallStar": 4.6,
      "mallSold": 5817,
      "mallSales": 101534.72,
      "followerNum": 25,
      "goodsNum": 2,
      "hostingMode": 2,
      "catIds": []
    }
  ],
  "columns": [],
  "title": "Temu 数据查询",
  "sourceType": "temu",
  "sourceTool": "geekbi_temu",
  "type": "tableListWorkbenches"
}
```

### 站点列表：`POST /geekbi/temu/siteList`

#### 请求

无业务参数，Body 传 `{}`。只将非空且为正整数的 `sites[].regionId` 用于店铺搜索；`sites[].siteId` 是上游内部 ID，不得代替 `regionId`。如果没有有效 `regionId`，应停止链式调用并告知用户。

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/siteList" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{}'
```

#### 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `sites` | array | 支持的 Temu 站点 |
| `total` | integer | 站点数量 |
| `title` / `sourceType` / `sourceTool` / `type` | string | `Temu 站点列表` / `temu` / `geekbi_temu` / `tableListWorkbenches` |
| `columns` | array | 渲染列定义 |

`sites[]` 字段：`siteId`（内部 ID，不用于筛选）、`regionId`、`name`、`cnName`、`lang`、`currency`、`extraFields`。业务字段允许为空，链式调用前必须筛掉空 `regionId`。

### 品类列表：`POST /geekbi/temu/categoryList`

#### 请求

| 参数 | 类型 | 必填 | 约束 | 说明 |
|---|---|---:|---|---|
| `parentCatId` | integer | 否 | `>=0` | 不传时返回一级品类；传某个 `categories[].catId` 时查询其下一级 |

先用 `{}` 获取一级节点；需要下钻时，只把非空且为非负整数的 `catId` 作为下一次请求的 `parentCatId`；筛选店铺时，只把有效 `catId` 放入 `catIds` 数组。传 `0` 合法，但没有证据证明它与省略 `parentCatId` 等价。

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/categoryList" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"parentCatId":1}'
```

#### 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `categories` | array | 指定父级下的品类节点 |
| `total` | integer | 返回节点数量 |
| `parentCatId` | integer / omitted | 本次查询的父级 ID；一级查询时可能省略 |
| `title` / `sourceType` / `sourceTool` / `type` | string | `Temu 品类列表` / `temu` / `geekbi_temu` / `tableListWorkbenches` |
| `columns` | array | 渲染列定义 |

`categories[]` 字段：`catId`, `catName`, `catLevel`, `parentCatId`, `isLeaf`, `extraFields`。其中仅非空有效 `catId` 可用于店铺搜索 `catIds` 或下一次 `parentCatId`。

## 错误码

入口脚本会原样回显网关 JSON 错误；如果 HTTP 错误体不是 JSON，则包装为 `error` 与 `details` 字段，不会以 Python 堆栈替代业务错误。真实非法参数 `{"regionId":0,"page":1,"size":3}` 返回 `error="HTTP 400: Bad Request"`，`details` 中含网关 `errcode=400` 与参数消息。

| HTTP / 业务码 | 含义 | 处理建议 |
|---|---|---|
| 200 且 `errcode=200` | 成功 | 按对应顶层结构解析；仍需检查是否为空结果 |
| HTTP 200 + 非成功业务码 | 上游业务拒绝 | 按错误消息停止或修正参数；不得当作成功响应解析 |
| 400 | 参数校验失败 | 修正字段；不要自动改关键词、翻页或站点连续重试 |
| 401 | 认证失败 | 检查 `LINKFOX_AGENT_API_KEY` 或兼容键 `LINKFOXAGENT_API_KEY`，并按 `SKILL.md` 的认证引导处理 |
| 402 | 算力或余额不足 | 停止调用并按认证/算力引导处理 |
| 403 | 无权限 | 停止调用并联系工具管理员；不要按充值问题处理 |
| 429 | 请求过于频繁 | 停止连续调用，稍后再试 |
| 502 / 503 / 504 | 网关或上游异常 | 付费店铺搜索不自动重试；说明可能再次扣费并取得用户确认后，才可按原参数重试一次。免费的站点/品类辅助接口可按原参数重试 1–2 次 |

店铺搜索会拒绝：`regionId<1`、`page<1`、`size` 不在 1–200、`page*size>10000`、非法 `hostingMode/order`、`mallStar` 不在 0–5，以及任意最小值大于最大值。`catIds` 中空值会被过滤；调用方应只传有效整数。

未携带 `Authorization` 时，网关通常返回 HTTP 401：

```json
{"errcode":401,"errmsg":"authorized error"}
```

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-geekbi-temu-shop",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-geekbi-temu-shop`)
- `sentiment`: Choose ONE - `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE - `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
