---
name: linkfox-echotik-list-product
description: 搜索和分析TikTok 16个站点的商品销量、达人带货、定价及佣金等数据，用于TikTok Shop选品和商品表现分析。
---

# EchoTik TikTok 商品搜索

本技能用于搜索和分析 TikTok Shop 商品数据，帮助卖家和营销人员发现商品机会、评估销售表现、识别达人带货商品。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 按**关键词**搜索 TikTok Shop 商品，支持销量、GMV、价格、评分、评论数、佣金率、达人/视频/播放量等多维筛选与排序。
- 返回多周期销售数据（1d/7d/15d/30d/60d/90d/total）及对应 GMV、定价、评分、评论、佣金率、达人带货统计等明细。
- 覆盖 16 个 TikTok Shop 站点（US、ID、TH、PH、MY、VN、GB、MX、SG、SA、BR、ES、JP、DE、IT、FR）。

### ❌ 边界与限制

- **关键词语言**：`keyword` 须翻译为目标站点的当地语言；`categoryKeywordCN` 必须为中文。
- **佣金率**：以小数存储（0.05 表示 5%），用户给百分比时需先换算。
- **上架日期**：`firstCrawlDt` 为紧凑整数格式 `YYYYMMDD`（如 `20240101`）。
- **默认站点**：用户未指定站点时默认 `US`。
- **不在范围内**：TikTok 达人/创作者分析（粉丝数、互动率）；TikTok 视频表现分析（单条视频的播放、点赞、分享）；TikTok 广告/广告系列管理；Amazon、Shopee 等非 TikTok 平台数据；TikTok Shop 店铺级分析；Listing 创建或优化建议；物流、履约或发货分析。

## 核心概念

EchoTik 是一个 TikTok Shop 数据分析平台，跟踪多个 TikTok 站点的商品表现。本工具提供基于关键词的商品搜索与丰富的筛选能力，返回商品销量（1d/7d/15d/30d/60d/90d/total）、GMV、定价、评分、评论数、佣金率及达人带货统计等明细。

**销售指标**：商品包含多周期销售数据——1 天、7 天、15 天、30 天、60 天、90 天及总销量；GMV 同样按此粒度返回。

**佣金率**：以小数存储（0.05 表示 5%）。当用户指定百分比时，传入 API 前需先换算为小数。

**上架日期**：`firstCrawlDt` 字段使用紧凑整数格式 `YYYYMMDD`（如 `20240101` 表示 2024 年 1 月 1 日）。

## 调用方式

- **API 端点**：`POST /echotik/listProduct`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_list_product.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-list-product-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 基础关键词搜索 —— 查某关键词的热销商品**
```json
{
  "keyword": "phone case",
  "region": "US",
  "productSortField": 1,
  "sortType": 1,
  "pageSize": 20
}
```

**2. 高佣金商品发现 —— 佣金率 >= 10% 的商品**
```json
{
  "keyword": "beauty",
  "region": "US",
  "minProductCommissionRate": 0.10,
  "productSortField": 5,
  "sortType": 1
}
```

**3. 新品趋势 —— 近期上架且 30 天销量强劲**
```json
{
  "keyword": "gadget",
  "region": "US",
  "minFirstCrawlDt": 20250101,
  "minTotalSale30dCnt": 1000,
  "productSortField": 5,
  "sortType": 1
}
```

**4. 达人热推商品 —— 多达人推广的商品**
```json
{
  "keyword": "skincare",
  "region": "US",
  "minTotalIflCnt": 50,
  "minTotalViewsCnt": 1000000,
  "productSortField": 1,
  "sortType": 1
}
```

**5. 平价高销量 —— 低价 + 高销量**
```json
{
  "keyword": "accessories",
  "region": "US",
  "maxSpuAvgPrice": 10,
  "minTotalSaleCnt": 5000,
  "productSortField": 2,
  "sortType": 1
}
```

**6. 东南亚市场探索**
```json
{
  "keyword": "fashion",
  "region": "TH",
  "minTotalSale30dCnt": 500,
  "productSortField": 7,
  "sortType": 1
}
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示关键列——商品名称、价格、总销量、30 天销量、GMV、评分、佣金率、推广达人数。
2. **币种感知**：展示价格和 GMV 时附上响应中的货币字段。
3. **佣金格式**：佣金率以百分比展示便于阅读（如 0.05 显示为「5%」）。
4. **数据量提示**：当结果 `total` 较大时，展示当前页数据并告知可用总数；建议调整筛选或翻页以继续浏览。
5. **图片引用**：若返回 `imageUrl` 或 `coverUrl`，提示用户商品图片可用。
6. **错误处理**：查询失败时依据响应说明原因，并建议调整参数。
7. **关键词翻译提醒**：当用户面向非英语站点时，提醒关键词应使用该站点的当地语言以获得更好结果。

## 用户表达与场景速查

**适用** —— TikTok 商品搜索与表现分析：

| 用户说 | 场景 |
|--------|------|
| "TikTok 上什么火"、"TikTok 热销品" | 按销量排序的关键词搜索 |
| "TikTok 高佣金商品" | 按佣金率筛选 |
| "TikTok Shop 美国站什么卖得好" | 按区域搜索销量商品 |
| "TikTok 新爆品" | 按上架日期 + 销量筛选 |
| "哪些商品很多达人在推" | 按达人数筛选 |
| "TikTok 便宜又高销量的商品" | 按价格 + 销量筛选 |
| "东南亚 TikTok 选品" | 搜索指定东南亚区域 |
| "TikTok 上好评多的商品" | 按评分 + 评论数筛选 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# EchoTik-TikTok商品搜索 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/listProduct`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 否 | 商品关键词（请翻译为当地语言）。最大长度 1000 |
| region | string | 否 | 区域，默认 `US`。可选值：US（美国）、ID（印度尼西亚）、TH（泰国）、PH（菲律宾）、MY（马来西亚）、VN（越南）、GB（英国）、MX（墨西哥）、SG（新加坡）、SA（沙特阿拉伯）、BR（巴西）、ES（西班牙）、JP（日本）、DE（德国）、IT（意大利）、FR（法国） |
| categoryKeywordCN | string | 否 | 商品分类（请输入中文）。最大长度 1000 |
| minTotalSaleCnt | integer | 否 | 总销量（最小值） |
| maxTotalSaleCnt | integer | 否 | 总销量（最大值） |
| minTotalSale30dCnt | integer | 否 | 30天销量（最小值） |
| maxTotalSale30dCnt | integer | 否 | 30天销量（最大值） |
| minTotalSaleGmvAmt | string | 否 | 商品交易总额（最小值）。最大长度 1000 |
| maxTotalSaleGmvAmt | string | 否 | 商品交易总额（最大值）。最大长度 1000 |
| minTotalSaleGmv30dAmt | string | 否 | 商品交易总额（30天）（最小值）。最大长度 1000 |
| maxTotalSaleGmv30dAmt | string | 否 | 商品交易总额（30天）（最大值）。最大长度 1000 |
| minSpuAvgPrice | number | 否 | SPU平均价格（最小值） |
| maxSpuAvgPrice | number | 否 | SPU平均价格（最大值） |
| minProductRating | number | 否 | 商品评分（最小值） |
| maxProductRating | number | 否 | 商品评分（最大值） |
| minReviewCount | integer | 否 | 商品评价数（最小值） |
| maxReviewCount | integer | 否 | 商品评价数（最大值） |
| minProductCommissionRate | number | 否 | 商品佣金比例（最小值），输入值为百分比时自动转成小数，例如：5%->0.05 |
| maxProductCommissionRate | number | 否 | 商品佣金比例（最大值），输入值为百分比时自动转成小数，例如：5%->0.05 |
| minTotalIflCnt | integer | 否 | 带货达人数（最小值） |
| maxTotalIflCnt | integer | 否 | 带货达人数（最大值） |
| minTotalVideoCnt | integer | 否 | 带货视频数（最小值） |
| maxTotalVideoCnt | integer | 否 | 带货视频数（最大值） |
| minTotalViewsCnt | integer | 否 | 带货播放数（最小值） |
| maxTotalViewsCnt | integer | 否 | 带货播放数（最大值） |
| minFirstCrawlDt | integer | 否 | 商品上架时间（最小值），格式 YYYYMMDD（例如：20200101 代表 2020-01-01） |
| maxFirstCrawlDt | integer | 否 | 商品上架时间（最大值），格式 YYYYMMDD |
| saleDays | integer | 否 | 商品上架销售天数，单位是天 |
| productSortField | integer | 否 | 排序字段：1=总销量、2=商品交易总额、3=SPU平均价格、4=7天销量、5=30天销量、6=7天商品交易额、7=30天商品交易额。默认 `1` |
| sortType | integer | 否 | 排序方式：0=升序（asc）、1=降序（desc）。默认 `1` |
| pageNum | integer | 否 | 分页页码。默认 `1` |
| pageSize | integer | 否 | 每页条数。默认 `50` |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| products | array | 产品信息列表（详见下方） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 产品对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | string | 商品唯一标识ID |
| productName | string | 商品名称 |
| title | string | 商品名称 |
| imageUrl | string | 商品图片URL |
| coverUrl | string | 封面图URL列表 |
| productImageUrls | array | 商品图片URL列表 |
| categoryName | string | 商品类目名称 |
| categoryIds | array | 商品类目ID列表 |
| region | string | 区域代码 |
| currency | string | 货币 |
| price | number | 商品价格 |
| minPrice | number | 最低价格 |
| maxPrice | number | 最高价格 |
| spuAvgPrice | number | SPU平均价格 |
| productRating | number | 商品评分 |
| reviewCount | integer | 评论数量 |
| ratings | integer | 评论数 |
| productCommissionRate | number | 商品佣金比例 |
| totalSaleCnt | integer | 总销量 |
| totalSale1dCnt | integer | 1天内总销量 |
| totalSale7dCnt | integer | 7天内总销量 |
| totalSale15dCnt | integer | 15天内总销量 |
| totalSale30dCnt | integer | 30天内总销量 |
| totalSale60dCnt | integer | 60天内总销量 |
| totalSale90dCnt | integer | 90天内总销量 |
| monthlySalesUnits | integer | 月销量 |
| totalSaleGmvAmt | number | 总销售额 |
| totalSaleGmv1dAmt | number | 1天内总销售额 |
| totalSaleGmv7dAmt | number | 7天内总销售额 |
| totalSaleGmv15dAmt | number | 15天内总销售额 |
| totalSaleGmv30dAmt | number | 30天内总销售额 |
| totalSaleGmv60dAmt | number | 60天内总销售额 |
| totalSaleGmv90dAmt | number | 90天内总销售额 |
| firstCrawlDt | integer | 上架日期 |
| availableDate | string | 上架时间(时间戳) |
| discount | string | 折扣信息 |
| freeShippingText | string | 是否包邮 |
| offMarkText | string | 是否有优惠标记 |
| salesFlagText | string | 带货方式 |
| salesTrendFlagText | string | 销售趋势标记 |
| isSShopText | string | 是否S店 |
| salePropsInfo | array | 销售属性信息（商品规格） |
| sourceTool | string | 来源工具 |
| sourceType | string | 商品来源 |
| asin | string | 产品ID |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/echotik/listProduct \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "phone case",
    "region": "US",
    "minTotalSale30dCnt": 1000,
    "productSortField": 5,
    "sortType": 1,
    "pageSize": 20
  }'
```
