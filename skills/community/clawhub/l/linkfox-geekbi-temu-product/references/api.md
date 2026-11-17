# Temu 商品搜索与详情 API 参考

## 调用规范

- **请求地址（商品搜索）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/goodsSearch`
- **请求地址（商品详情）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/goodsDetail`
- **请求地址（站点列表）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/siteList`
- **请求地址（品类列表）**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/categoryList`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退到兼容键 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`（未设置时为空串）
- **超时**：150s

> 业务入口脚本默认仅缓存成功响应 24 小时，成功的空结果也可缓存；HTTP 或业务失败不缓存。`--inline` 不绕过缓存；`--no-cache` 跳过缓存读写并强制真实请求，商品搜索/详情可能再次扣算力，站点/品类列表仅强制刷新。

> 上述地址是 LinkFox 工具网关路由。服务端再调用 GeekBI 上游 GET API；客户端不得把上游 `/api/v1/temu/...` 路径当作网关地址。

## 网关公共成功字段

| 字段 | 类型 | 已验证成功值 | 说明 |
|---|---|---|---|
| `errcode` | integer | `200` | 网关业务状态码；仍须检查，不应只看 HTTP 200 |
| `errmsg` | string | `ok` | 网关业务状态消息 |

真实链路验证摘要：站点列表返回 33 个站点，其中美国站 `regionId=211`；一级品类返回 23 个节点，`parentCatId=27011` 的下一级返回 12 个节点；使用 `regionId=211`、`catIds=[27011]` 搜索返回 3 条样本（上游 `total=10000`），随后按首条 `goodsId` 查询详情，返回商品对象和 13 条历史记录。

以下示例按 2026-08-27 的真实成功响应确认字段层级，具体业务值仅用于说明；可空业务字段可能省略。

## 商品字段（搜索 `items[]` / 详情 `goods`）

| 字段组 | 字段 |
|---|---|
| 标识与文本 | `goodsId`, `mallId`, `thumbnail`, `goodsName`, `goodsNameCn`, `goodsNameEn`, `brand`, `sku` |
| 品类 | `catIds`, `catItems` |
| 销量与库存 | `sold`, `quantity`, `daySold`, `weekSold`, `monthSold`, `mallSold` |
| 金额 | `sales`, `minPrice`, `maxPrice`, `daySales`, `weekSales`, `monthSales` |
| 销量增长率 | `daySoldRate`, `weekSoldRate`, `monthSoldRate` |
| 销售额增长率 | `daySalesRate`, `weekSalesRate`, `monthSalesRate` |
| 供货价 | `supplyPrice`, `minSupplyPrice`, `medianSupplyPrice`, `maxSupplyPrice` |
| 评价 | `goodsScore`, `reviewNum` |
| 状态 | `hostingMode`, `status`, `isAd`, `isCustom`, `isPresale` |
| 时间 | `onSaleTime`, `mallOpenTime`, `createTime`, `updateTime` |
| 其他 | `similarNum`, `extraFields` |

`catItems[]` 包含 `catId`, `catLevel`, `catName`, `isLeaf`, `parentCatId`, `extraFields`。金额字段除供货价外均按当前站点货币解释。

## 商品搜索：`POST /geekbi/temu/goodsSearch`

### 请求

POST Body（JSON）。所有字段均可选；空对象 `{}` 使用 `regionId=211`、`page=1`、`size=20`、`matchMode=2`。

#### 分页、匹配、品类与状态

| 参数 | 类型 | 必填 | 默认值 / 约束 | 说明 |
|---|---|---:|---|---|
| `regionId` | integer | 否 | `211`；`>=1` | Temu 地区 ID；应取自站点列表 `sites[].regionId` |
| `page` | integer | 否 | `1`；`>=1` | 页码 |
| `size` | integer | 否 | `20`；`1..200` | 每页数量；`page * size` 不得超过 10000 |
| `keyword` | string | 否 | 最大 300 字符 | 匹配商品标题的关键词 |
| `matchMode` | integer | 否 | `2`；`1..2` | `1`=严格匹配，`2`=模糊匹配 |
| `catIds` | integer[] | 否 | - | 品类 ID 数组；元素取自品类列表 `categories[].catId` |
| `status` | integer[] | 否 | 元素为 `1`、`2`、`3` | `1`=正常，`2`=缺货，`3`=下架 |
| `hostingMode` | integer | 否 | `1..2` | `1`=全托管，`2`=半托管 |
| `sort` | string | 否 | 最大 100 字符 | 排序字段；只使用接口确认支持的字段 |
| `order` | string | 否 | `asc` 或 `desc` | 排序方向，不区分大小写 |

网关 JSON 中 `catIds` 和 `status` 必须传数组，例如 `{"catIds":[984,982],"status":[1,2]}`。服务端会把数组编码为上游单个英文逗号参数；不要在 JSON 中传逗号字符串，也不要传重复键。

#### 销量、销售额与增长率

| 参数组 | 类型 | 约束 / 单位 |
|---|---|---|
| `soldMin`, `soldMax` | integer | 历史累计总销量，`>=0` |
| `daySoldMin`, `daySoldMax` | integer | 平均日销量，`>=0` |
| `weekSoldMin`, `weekSoldMax` | integer | 平均周销量，`>=0` |
| `monthSoldMin`, `monthSoldMax` | integer | 平均月销量，`>=0` |
| `daySoldRateMin`, `daySoldRateMax` | number | 日销量增长率，百分比 |
| `weekSoldRateMin`, `weekSoldRateMax` | number | 周销量增长率，百分比 |
| `monthSoldRateMin`, `monthSoldRateMax` | number | 月销量增长率，百分比 |
| `salesMin`, `salesMax` | number | 历史累计销售额，当前站点货币，`>=0` |
| `daySalesMin`, `daySalesMax` | number | 平均日销售额，当前站点货币，`>=0` |
| `weekSalesMin`, `weekSalesMax` | number | 平均周销售额，当前站点货币，`>=0` |
| `monthSalesMin`, `monthSalesMax` | number | 平均月销售额，当前站点货币，`>=0` |
| `daySalesRateMin`, `daySalesRateMax` | number | 日销售额增长率，百分比 |
| `weekSalesRateMin`, `weekSalesRateMax` | number | 周销售额增长率，百分比 |
| `monthSalesRateMin`, `monthSalesRateMax` | number | 月销售额增长率，百分比 |

#### 价格、库存、店铺与评价

| 参数组 | 类型 | 约束 / 单位 |
|---|---|---|
| `quantityMin`, `quantityMax` | integer | 剩余库存，`>=0` |
| `mallSoldMin`, `mallSoldMax` | integer | 店铺历史累计总销量，`>=0` |
| `priceMin`, `priceMax` | number | 商品价格，当前站点货币，`>=0` |
| `supplyPriceMin`, `supplyPriceMax` | number | 供货价，人民币，`>=0` |
| `goodsScoreMin`, `goodsScoreMax` | number | 商品评分，`0..5` |
| `reviewNumMin`, `reviewNumMax` | integer | 历史累计评论数，`>=0` |

#### 时间范围

| 参数组 | 类型 | 说明 |
|---|---|---|
| `onSaleTimeMin`, `onSaleTimeMax` | string | 商品上架时间范围，ISO-8601 date-time，最大 40 字符 |
| `mallOpenTimeMin`, `mallOpenTimeMax` | string | 店铺开店时间范围，ISO-8601 date-time，最大 40 字符 |

所有成对的 `*Min` 都不得大于对应的 `*Max`。时间字段仍应始终使用 ISO-8601 date-time；服务端只在同组 Min/Max 同时提供时解析并比较时间，单独提供一个非法时间字符串时可能由上游拒绝。

#### curl 示例

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/goodsSearch" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"regionId":211,"keyword":"dress","catIds":[984],"page":1,"size":20,"sort":"sold","order":"desc"}'
```

### 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `items` | array | 当前页商品；每个业务字段都可能缺失或为 `null` |
| `columns` | array | 渲染列定义 |
| `total` | integer | 上游报告的匹配总数；服务只限制可访问窗口 `page * size <= 10000`，不会截断 `total`；上游缺失时回退为当前 `items` 长度 |
| `page` | integer | 当前页码 |
| `size` | integer | 每页数量 |
| `regionId` | integer | 本次请求使用的地区 ID |
| `title` | string | `Temu 数据查询` |
| `sourceType` | string | `temu` |
| `sourceTool` | string | `geekbi_temu` |
| `type` | string | `tableListWorkbenches` |

#### 响应示例

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "total": 1,
  "page": 1,
  "size": 20,
  "regionId": 211,
  "items": [
    {
      "goodsId": "601099512345678",
      "goodsName": "Example product",
      "catIds": [984],
      "sold": 12,
      "sales": 3.5
    }
  ],
  "columns": [],
  "title": "Temu 数据查询",
  "sourceType": "temu",
  "sourceTool": "geekbi_temu",
  "type": "tableListWorkbenches"
}
```

## 商品详情：`POST /geekbi/temu/goodsDetail`

### 请求

| 参数 | 类型 | 必填 | 默认值 / 约束 | 说明 |
|---|---|---:|---|---|
| `goodsId` | string | 是 | 非空；最大 100 字符 | Temu 商品 ID，通常来自搜索 `items[].goodsId` |
| `regionId` | integer | 否 | `211`；`>=1` | Temu 地区 ID；建议与搜索使用同一值 |

#### curl 示例

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/goodsDetail" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"goodsId":"601099512345678","regionId":211}'
```

### 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `goods` | object | 商品对象，字段与搜索 `items[]` 相同 |
| `history` | array | 最近 30 天历史记录；业务字段可缺失或为 `null` |
| `regionId` | integer | 本次请求使用的地区 ID |
| `title` | string | `Temu 商品详情` |
| `sourceType` | string | `temu` |
| `sourceTool` | string | `geekbi_temu` |
| `type` | string | `productWorkbenches` |
| `columns` | array | 商品详情渲染列 |

#### 商品历史 `history[]`

历史条目字段均可缺失或为 `null`：

`id`, `sold`, `sales`, `minPrice`, `maxPrice`, `quantity`, `goodsScore`, `reviewNum`, `daySold`, `weekSold`, `monthSold`, `daySales`, `weekSales`, `monthSales`, `daySoldRate`, `weekSoldRate`, `monthSoldRate`, `daySalesRate`, `weekSalesRate`, `monthSalesRate`, `createTime`, `extraFields`。

#### 响应示例

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "goods": {"goodsId": "601099512345678", "goodsName": "Example product"},
  "history": [{"sold": 12, "sales": 3.5, "createTime": "2026-08-25T00:00:00Z"}],
  "regionId": 211,
  "title": "Temu 商品详情",
  "sourceType": "temu",
  "sourceTool": "geekbi_temu",
  "type": "productWorkbenches",
  "columns": []
}
```

## 站点列表：`POST /geekbi/temu/siteList`

### 请求

无业务参数，Body 传 `{}`。只将非空且为正整数的 `sites[].regionId` 用于商品搜索和详情；`sites[].siteId` 是上游内部 ID，不得代替 `regionId`。如果没有有效 `regionId`，应停止链式调用并告知用户。

#### curl 示例

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

### 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `sites` | array | 支持的 Temu 站点 |
| `total` | integer | 站点数量 |
| `title` / `sourceType` / `sourceTool` / `type` | string | `Temu 站点列表` / `temu` / `geekbi_temu` / `tableListWorkbenches` |
| `columns` | array | 渲染列定义 |

`sites[]` 字段：`siteId`（内部 ID，不用于筛选）、`regionId`、`name`、`cnName`、`lang`、`currency`、`extraFields`。业务字段允许为空，链式调用前必须筛掉空 `regionId`。

#### 响应示例

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "sites": [{"siteId": 1, "regionId": 211, "name": "United States", "cnName": "美国", "lang": "en", "currency": "USD"}],
  "total": 1,
  "title": "Temu 站点列表",
  "sourceType": "temu",
  "sourceTool": "geekbi_temu",
  "type": "tableListWorkbenches",
  "columns": []
}
```

## 品类列表：`POST /geekbi/temu/categoryList`

### 请求

| 参数 | 类型 | 必填 | 约束 | 说明 |
|---|---|---:|---|---|
| `parentCatId` | integer | 否 | `>=0` | 不传时返回一级品类；传某个 `categories[].catId` 时查询其下一级 |

品类搜索依赖：先用 `{}` 获取一级节点；需要下钻时只把非空且为非负整数的 `catId` 作为下一次请求的 `parentCatId`；需要筛选商品时只把有效 `catId` 放入商品搜索的 `catIds` 数组。如果没有有效 `catId`，应停止链式调用并告知用户。传 `0` 合法，但源码没有证明它与省略 `parentCatId` 等价。

#### curl 示例

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/categoryList" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"parentCatId":100}'
```

### 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `categories` | array | 指定父级下的品类节点 |
| `total` | integer | 返回节点数量 |
| `parentCatId` | integer / omitted | 本次查询的父级 ID；真实一级查询省略该字段，传父级查询时返回对应 ID |
| `title` / `sourceType` / `sourceTool` / `type` | string | `Temu 品类列表` / `temu` / `geekbi_temu` / `tableListWorkbenches` |
| `columns` | array | 渲染列定义 |

`categories[]` 字段：`catId`, `catName`, `catLevel`, `parentCatId`, `isLeaf`, `extraFields`。业务字段允许为空；其中仅非空有效 `catId` 可用于商品搜索 `catIds` 或下一次 `parentCatId`。

#### 响应示例

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "categories": [{"catId": 984, "catName": "Women Clothing", "catLevel": 2, "parentCatId": 100, "isLeaf": false}],
  "total": 1,
  "parentCatId": 100,
  "title": "Temu 品类列表",
  "sourceType": "temu",
  "sourceTool": "geekbi_temu",
  "type": "tableListWorkbenches",
  "columns": []
}
```

## `columns[]` 结构

每个列定义通常包含 `field`, `title`, `cellType`, `sortable`, `filterable`；`cellType` 为 `number` 或 `text`。

## 错误码

入口脚本会原样回显网关 JSON 错误，不会以 Python 堆栈替代业务错误。

| HTTP / 业务码 | 含义 | 处理建议 |
|---|---|---|
| 200 且无失败业务码 | 成功 | 按对应顶层结构解析；仍需检查是否为空结果或包含异常消息 |
| HTTP 200 + `errcode=30001` | 上游业务拒绝 | 按错误消息停止或修正参数；不得当作成功响应解析 |
| HTTP 200 + `errcode=30005` | 上游授权失败 | 停止调用并联系工具管理员；不得当作成功响应解析 |
| 400 | 参数校验失败 | 根据消息修正字段；不要自动改关键词、翻页或站点连续重试 |
| 401 | 认证失败 | 检查 `LINKFOX_AGENT_API_KEY` 或兼容键 `LINKFOXAGENT_API_KEY`，并按 `SKILL.md` 的认证引导处理 |
| 402 | 算力或余额不足 | 停止调用并按认证/算力引导处理 |
| 403 | 无权限 | 停止调用并联系工具管理员；不要按充值问题处理 |
| 429 | 请求过于频繁 | 停止连续调用，稍后再试 |
| 502 / 503 / 504 | 网关或上游异常 | 付费搜索/详情不自动重试；说明可能再次扣费并取得用户确认后，才可按原参数重试一次。免费的站点/品类辅助接口可按原参数重试 1–2 次 |

商品搜索还会拒绝：`regionId<1`、`page<1`、`size` 不在 1–200、`page*size>10000`、非法 `status/hostingMode/order`，以及任意最小值大于最大值。`catIds` 中的空值会被过滤，`status` 中的空值会被拒绝；调用方应只传有效整数。商品详情会拒绝空 `goodsId` 或非法 `regionId`；只复用搜索结果中非空的 `items[].goodsId`。

未携带 `Authorization` 的真实网关响应为 HTTP 401：

```json
{"errcode":401,"errmsg":"authorized error"}
```

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-geekbi-temu-product",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-geekbi-temu-product`)
- `sentiment`: Choose ONE - `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE - `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
