# Temu 类目与关键词市场研究 API 参考

## 调用规范

- **请求地址（类目研究）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/categorySearch`
- **请求地址（关键词研究）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/keywordSearch`
- **请求地址（站点列表）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/siteList`
- **请求地址（品类列表）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/categoryList`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退到兼容键 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`（未设置时为空串）
- **超时**：150s

> 业务入口脚本默认仅缓存成功响应 24 小时，成功的空结果也可缓存；HTTP 或业务失败不缓存。`--inline` 不绕过缓存；`--no-cache` 跳过缓存读写并强制真实请求，类目/关键词搜索可能再次扣算力，站点/品类列表仅强制刷新。

> LinkFox 网关参数使用 `regionId`；应取自站点列表 `sites[].regionId`。不要把上游内部 `siteId` 或上游 GET 路径当作网关请求参数/地址。

## 端点

### 类目研究：`POST /geekbi/temu/categorySearch`

#### 请求

两个搜索端点的以下参数均为可选；空对象使用美国站和默认分页。

| 参数 | 类型 | 必填 | 默认值 / 约束 | 说明 |
|---|---|---:|---|---|
| `regionId` | integer | 否 | `211`；`>=1` | Temu 地区 ID，取自 `sites[].regionId` |
| `page` | integer | 否 | `1`；`>=1` | 页码 |
| `size` | integer | 否 | `20`；`1..200` | 每页数量；`page * size` 不得超过 10000 |
| `order` | string | 否 | `asc` / `desc`，不区分大小写 | 排序方向；网关没有默认值 |
| `sort` | string | 否 | 最大 100 字符 | 排序字段；只使用接口已确认支持的字段，不需要排序时省略 |

成对提供的所有 `*Min` / `*Max` 都必须满足 Min ≤ Max。

类目搜索和关键词搜索只共享以下 12 个范围参数。日/周/月销量、销售额、商品数、店铺数及增长率是响应指标，不是请求筛选字段。

| 参数组 | 类型 | 约束 / 单位 |
|---|---|---|
| `dsrMin`, `dsrMax` | number | 蓝海指数；只作供需综合信号 |
| `totalSoldMin`, `totalSoldMax` | integer | 历史累计销量，`>=0` |
| `avgPriceMin`, `avgPriceMax` | number | 平均价格，所选站点货币，`>=0` |
| `totalSalesMin`, `totalSalesMax` | number | 历史累计销售额，所选站点货币，`>=0` |
| `itemCountMin`, `itemCountMax` | integer | 关联商品数，`>=0` |
| `mallCountMin`, `mallCountMax` | integer | 关联店铺数，`>=0` |

| 参数 | 类型 | 必填 | 默认值 / 约束 | 说明 |
|---|---|---:|---|---|
| `keyword` | string | 否 | 最大 300 字符 | 类目中文名或英文名，模糊搜索 |

`categorySearch` 不接受 `catLevel` 或 `parentCatId`。需要按父级浏览类目树时调用 `categoryList`；`catLevel` 只可能出现在响应项中。

```bash
# 类目研究
curl -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/categorySearch" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"regionId":211,"keyword":"宠物","totalSoldMin":1000,"sort":"totalSold","order":"desc","page":1,"size":3}'
```

#### 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `errcode` | integer | 业务状态；真实成功为 `200` |
| `errmsg` | string | 状态文本；真实成功为 `ok` |
| `title` / `type` | string | 渲染标题与类型 |
| `total` | integer | 命中数；可能封顶为 10,000 |
| `page` / `size` | integer | 当前页与每页数量 |
| `regionId` | integer | 实际查询地区 |
| `sourceTool` / `sourceType` | string | 数据来源元数据 |
| `columns` | array | 渲染列定义，不是业务结果 |
| `items` | array | 类目或关键词结果；真实成功调用可返回非空 |

| 字段组 | 关键字段 | 说明 |
|---|---|---|
| 标识与层级 | `catId`, `optId`, `catName`, `catLevel`, `parentCatId`, `parentCatItems`, `isLeaf`, `regionId` | 类目 ID、名称与完整路径 |
| 展示 | `thumbnail` | 类目缩略图（可能缺失） |
| 累计市场 | `dsr`, `totalSold`, `totalSales`, `avgPrice`, `itemCount`, `mallCount` | 蓝海、需求、价格与供给 |
| 半托管供给 | `semiManagedItemCount`, `semiManagedMallCount` | 半托管商品和店铺数量 |
| 周期需求 | `day/week/monthSold`, `day/week/monthSales` 及各自 `Rate` | 日、周、月需求与增长 |
| 周期供给 | `day/week/monthItemCount`, `day/week/monthMallCount` 及各自 `Rate` | 商品/店铺变化量与增长率 |
| 时间 | `createTime`, `updateTime` | 上游字符串时间；原样保留 |

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "total": 231,
  "page": 1,
  "size": 3,
  "regionId": 211,
  "items": [
    {
      "catId": 1464,
      "catName": "宠物用品",
      "catLevel": 1,
      "totalSold": 81486617,
      "monthSold": 8346332,
      "avgPrice": 15.69,
      "itemCount": 26840,
      "mallCount": 11419
    }
  ]
}
```

示例仅展示形状；字段值随实时数据变化，以脚本落盘 JSON 为准。

业务字段可能缺失或为 `null`。真实响应可能增加字段；调用方应保留未知扩展字段。

### 关键词研究：`POST /geekbi/temu/keywordSearch`

#### 请求

两个搜索端点的以下参数均为可选；空对象使用美国站和默认分页。

| 参数 | 类型 | 必填 | 默认值 / 约束 | 说明 |
|---|---|---:|---|---|
| `regionId` | integer | 否 | `211`；`>=1` | Temu 地区 ID，取自 `sites[].regionId` |
| `page` | integer | 否 | `1`；`>=1` | 页码 |
| `size` | integer | 否 | `20`；`1..200` | 每页数量；`page * size` 不得超过 10000 |
| `order` | string | 否 | `asc` / `desc`，不区分大小写 | 排序方向；网关没有默认值 |
| `sort` | string | 否 | 最大 100 字符 | 排序字段；只使用接口已确认支持的字段，不需要排序时省略 |

成对提供的所有 `*Min` / `*Max` 都必须满足 Min ≤ Max。

类目搜索和关键词搜索只共享以下 12 个范围参数。日/周/月销量、销售额、商品数、店铺数及增长率是响应指标，不是请求筛选字段。

| 参数组 | 类型 | 约束 / 单位 |
|---|---|---|
| `dsrMin`, `dsrMax` | number | 蓝海指数；只作供需综合信号 |
| `totalSoldMin`, `totalSoldMax` | integer | 历史累计销量，`>=0` |
| `avgPriceMin`, `avgPriceMax` | number | 平均价格，所选站点货币，`>=0` |
| `totalSalesMin`, `totalSalesMax` | number | 历史累计销售额，所选站点货币，`>=0` |
| `itemCountMin`, `itemCountMax` | integer | 关联商品数，`>=0` |
| `mallCountMin`, `mallCountMax` | integer | 关联店铺数，`>=0` |

| 参数 | 类型 | 必填 | 默认值 / 约束 | 说明 |
|---|---|---:|---|---|
| `keyword` | string | 否 | 最大 300 字符 | 中文或英文关键词；不应静默翻译或替换用户输入 |
| `catIds` | integer[] | 否 | 元素为可信类目 ID | 多个 ID 匹配任一类目，通常使用一级或二级 ID |
| `firstOnSaleTimeMin` | string | 否 | ISO-8601 date-time；最大 40 字符 | 关联商品最早上架时间下限 |
| `firstOnSaleTimeMax` | string | 否 | ISO-8601 date-time；最大 40 字符 | 关联商品最早上架时间上限 |

`firstOnSaleTime` 表示该词下最早商品的上架时间，不是关键词创建时间。

```bash
# 关键词研究（catIds 来自 categoryList/categorySearch）
curl -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/keywordSearch" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"regionId":211,"keyword":"dress","catIds":[27011],"totalSoldMin":1000,"sort":"totalSold","order":"desc","page":1,"size":3}'
```

#### 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `errcode` | integer | 业务状态；真实成功为 `200` |
| `errmsg` | string | 状态文本；真实成功为 `ok` |
| `title` / `type` | string | 渲染标题与类型 |
| `total` | integer | 命中数；可能封顶为 10,000 |
| `page` / `size` | integer | 当前页与每页数量 |
| `regionId` | integer | 实际查询地区 |
| `sourceTool` / `sourceType` | string | 数据来源元数据 |
| `columns` | array | 渲染列定义，不是业务结果 |
| `items` | array | 类目或关键词结果；真实成功调用可返回非空 |

| 字段组 | 关键字段 | 说明 |
|---|---|---|
| 关键词 | `id`, `keyword`, `cnKeyword`, `thumbnail`, `regionId` | 关键词标识、文本与地区 |
| 关联类目 | `catIds`, `catItems` | 类目 ID 与路径；列表可能含重复叶子 ID，展示时可去重但不得改写原始数据 |
| 累计市场 | `dsr`, `totalSold`, `totalSales`, `avgPrice`, `itemCount`, `mallCount` | 蓝海、需求、价格与供给 |
| 半托管供给 | `semiManagedItemCount`, `semiManagedMallCount` | 半托管商品和店铺数量 |
| 周期需求/供给 | 与类目结果相同的日、周、月 `Sold`、`Sales`、`ItemCount`、`MallCount` 及 `Rate` | 趋势与供给变化 |
| 时间 | `firstOnSaleTime`, `createTime`, `updateTime` | 最早关联商品上架时间及上游时间 |

业务字段可能缺失或为 `null`。真实响应可能增加字段；调用方应保留未知扩展字段。

### 站点列表：`POST /geekbi/temu/siteList`

#### 请求

请求体固定为 `{}`。从 `sites[]` 中选择与用户国家匹配的记录，并将其非空正整数 `regionId` 传给两个搜索端点；不要使用 `siteId`。

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

- 两个辅助端点的公共字段是 `errcode`、`errmsg`、`title`、`type`、`sourceType`、`sourceTool` 和渲染元数据 `columns`；它们不继承搜索响应的 `page`、`size`、`regionId` 或 `items`。
- 站点列表另含 `total` + `sites[]`。站点项包含 `regionId`, `siteId`, `name`, `cnName`, `lang`, `currency`。

业务字段可能缺失或为 `null`。真实响应可能增加字段；调用方应保留未知扩展字段。

### 品类列表：`POST /geekbi/temu/categoryList`

#### 请求

| 参数 | 类型 | 必填 | 默认值 / 约束 | 说明 |
|---|---|---:|---|---|
| `parentCatId` | integer | 否 | 省略；`>=0` | 省略时返回顶级品类；传已知 `catId` 时返回直接子级 |

从 `categories[].catId` 取值。逐级下钻时仅复用真实返回的 ID。

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/categoryList" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"parentCatId":27011}'
```

#### 响应

- 两个辅助端点的公共字段是 `errcode`、`errmsg`、`title`、`type`、`sourceType`、`sourceTool` 和渲染元数据 `columns`；它们不继承搜索响应的 `page`、`size`、`regionId` 或 `items`。
- 品类列表另含 `total` + `categories[]`，传父级时还可包含 `parentCatId`。品类项包含 `catId`, `catName`, `catLevel`, `parentCatId`, `isLeaf`。

业务字段可能缺失或为 `null`。真实响应可能增加字段；调用方应保留未知扩展字段。

## 错误码

| HTTP / 字段 | 含义 | 处理 |
|---|---|---|
| HTTP 400 | 参数类型、范围或 Min/Max 关系错误 | 修正当前参数；不要自动改条件连续试探 |
| HTTP 401 / `errcode=401` | API Key 无效或未配置 | 使用 `onboarding.md` |
| HTTP 402 / `errcode=402` | 算力或余额不足 | 使用 `onboarding.md` |
| HTTP 403 | 当前凭证无权限 | 停止并说明，不按认证/计费流程重试 |
| HTTP 5xx / `error` | 网关或上游异常 | 付费类目/关键词搜索不自动重试；说明可能再次扣费并取得用户确认后，才可按原参数重试一次。免费的站点/品类辅助接口可按原参数重试 1–2 次 |

入口脚本会把 HTTP 错误回显为 JSON。已验证非法 `size: 0` 返回 `{"error":"HTTP 400: Bad Request","details":"...size 必须为整数[1,200]..."}`，不会打印 Python 堆栈。

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-geekbi-temu-market-research",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-geekbi-temu-market-research`)
- `sentiment`: Choose ONE - `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE - `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
