---
name: linkfox-fastmoss-product-search
description: 基于FastMoss多维度搜索和筛选TikTok全球电商商品，支持类目、销量、佣金率及GMV等指标分析，用于爆款追踪。
---

# FastMoss - TikTok 商品搜索

本技能引导你使用 FastMoss 搜索与筛选 TikTok Shop 商品数据，帮助卖家和营销者发现商品机会、评估销售表现，并识别达人带货商品，覆盖全球 15 个 TikTok 市场。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 基于关键词搜索 TikTok Shop 商品，支持按类目、店铺类型、销量、佣金率、达人数等多维度筛选与排序。
- 返回商品多周期销量（7 天/28 天/90 天/总销量）、GMV、价格、评分、评论数、佣金率、达人带货统计、店铺信息等详细数据。
- 覆盖 15 个 TikTok 市场：US、GB、MX、ES、DE、IT、FR、ID、VN、MY、TH、PH、BR、JP、SG。

### ❌ 边界与限制

- **无必填参数**：所有参数均可选，但至少需提供 keyword 或 category 才能返回有意义结果。
- **分页上限**：每页最多 10 条。
- **类目语言**：`category` 须为英文类目名称，非英文需先翻译。
- **佣金率口径**：存储为小数（0.10 = 10%），展示时须转换为百分比。
- **不在范围内**：TikTok 达人/创作者分析（粉丝数、互动率）；TikTok 视频表现分析（播放、点赞、分享）；TikTok 广告/广告投放管理；Amazon、Shopee 等非 TikTok 平台数据；TikTok Shop 店铺级分析；Listing 创建或优化建议；物流、履约或发货分析。
- **边界判断**：当用户说"选品"或"在 TikTok 上卖什么"且涉及按销量、价格或佣金率搜索筛选 TikTok Shop 商品时适用；若涉及内容策略、视频创作或达人拓展，则不适用。

## 核心概念

FastMoss 是知名的 TikTok 电商平台数据追踪平台，覆盖多个 TikTok 市场。本工具提供基于关键词的商品搜索与丰富筛选能力，返回商品多周期销量（7 天/28 天/90 天/总销量）、GMV、价格、评分、评论数、佣金率、达人带货统计、店铺信息等详细数据。

**销量指标**：商品含多周期销量数据——7 天、28 天、90 天及总销量，GMV 同样按此粒度返回。

**佣金率**：以小数存储（0.10 表示 10%），展示时转换为百分比格式。

**店铺类型**：可按本地店铺（1）或跨境店铺（2）筛选；`isCrossBorder` 字段（1=跨境，0=本地）与 `isSShopText` 字段（TikTok 全托管店铺）提供额外店铺分类。

## 调用方式

- **API 端点**：`POST /fastmoss/productSearch`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/fastmoss_product_search.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-fastmoss-product-search-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 关键词搜索——找出热销商品**
```json
{
  "keyword": "phone case",
  "region": "US",
  "orderField": "total_units_sold",
  "pageSize": 10
}
```

**2. 高佣金商品发现——佣金率 ≥ 10% 的商品**
```json
{
  "keyword": "beauty",
  "region": "US",
  "commissionRateRange": {"min": 0.10},
  "orderField": "commission_rate"
}
```

**3. 跨境店铺商品——按店铺类型筛选**
```json
{
  "keyword": "gadget",
  "region": "US",
  "shopType": 2,
  "orderField": "day7_units_sold"
}
```

**4. 达人爆款——被大量达人带货的商品**
```json
{
  "keyword": "skincare",
  "region": "US",
  "creatorCountRange": {"min": 50},
  "orderField": "creator_count"
}
```

**5. TikTok 热销新品**
```json
{
  "keyword": "fashion",
  "region": "GB",
  "isTopSelling": true,
  "isNewListed": true,
  "orderField": "day7_gmv"
}
```

## 展示规则

1. **只呈现数据**：以结构化表格展示关键列——商品名称、价格、总销量、7 天销量、GMV、评分、佣金率、带货达人数，不做主观商业建议。
2. **佣金格式**：佣金率为小数（0.10 = 10%），展示时转换为百分比。
3. **跨境标识**：`isCrossBorder`：1 = 跨境店铺，0 = 本地店铺，清晰标注。
4. **币种标识**：展示价格与 GMV 时附上响应中的 `currency` 字段。
5. **趋势标签**：直接展示 `salesTrendFlagText` 作为趋势指示。
6. **店铺标识**：直接展示 `freeShippingText` 与 `isSShopText`（值为可读文本）。
7. **错误处理**：查询失败时基于响应说明原因，并建议调整参数。

## 用户表达与场景速查

**适用** —— TikTok 商品搜索与选品调研：

| 用户说 | 场景 |
|--------|------|
| "TikTok 上什么火"、"TikTok 趋势商品" | 按销量排序的关键词搜索 |
| "TikTok 高佣金商品" | 按佣金率范围筛选 |
| "TikTok Shop 美国什么好卖" | 按区域+销量的商品搜索 |
| "TikTok 跨境店铺商品" | 按 shopType=2 筛选 |
| "哪些商品很多达人在带货" | 按达人数范围筛选 |
| "TikTok 全托管店铺商品" | 用 isSshop=true 筛选 |
| "TikTok 东南亚选品" | 搜索指定东南亚区域 |
| "TikTok 热销新品" | 用 isTopSelling + isNewListed 标签 |
| "FastMoss 商品数据" | 直接平台查询 |

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

# FastMoss-TikTok商品搜索 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/fastmoss/productSearch`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 否 | 搜索关键词（商品标题模糊匹配） |
| region | string | 否 | 市场区域代码。可选值：US（美国）、GB（英国）、MX（墨西哥）、ES（西班牙）、DE（德国）、IT（意大利）、FR（法国）、ID（印度尼西亚）、VN（越南）、MY（马来西亚）、TH（泰国）、PH（菲律宾）、BR（巴西）、JP（日本）、SG（新加坡） |
| category | string | 否 | 英文类目名称，系统自动匹配TikTok类目ID。非英文需先翻译为英文 |
| shopType | integer | 否 | 店铺类型：1=本地店铺，2=跨境店铺 |
| isTopSelling | boolean | 否 | 仅筛选热销商品 |
| isNewListed | boolean | 否 | 仅筛选新上架商品 |
| isSshop | boolean | 否 | 仅筛选TikTok全托管（S-shop）商品 |
| isFreeShipping | boolean | 否 | 仅筛选包邮商品 |
| isLocalWarehouse | boolean | 否 | 仅筛选本地仓发货商品 |
| unitsSoldRange | object | 否 | 销量范围筛选，格式：`{"min": 100, "max": 5000}` |
| commissionRateRange | object | 否 | 佣金率范围筛选，格式：`{"min": 0.05, "max": 0.20}`（小数，0.10=10%） |
| creatorCountRange | object | 否 | 带货达人数范围筛选，格式：`{"min": 10, "max": 500}` |
| orderField | string | 否 | 排序字段：day7_units_sold（7天销量）、day7_gmv（7天GMV）、commission_rate（佣金率）、total_units_sold（总销量）、total_gmv（总GMV）、creator_count（达人数）。默认降序排列 |
| page | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，最大 10，默认 10 |

## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 符合条件的总记录数 |
| products | array | 商品信息列表（详见下方） |
| columns | array | 渲染列定义 |
| type | string | 渲染样式类型 |
| costToken | integer | 消耗 token 数 |

### 商品对象字段（products 数组）

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 商品标题 |
| productId | string | 商品唯一标识ID |
| region | string | 市场区域代码 |
| price | number | 商品价格 |
| minPrice | number | 最低价格 |
| maxPrice | number | 最高价格 |
| currency | string | 货币代码 |
| totalSaleCnt | integer | 累计总销量 |
| totalSale1dCnt | integer | 1天销量 |
| totalSale7dCnt | integer | 7天销量 |
| totalSale28dCnt | integer | 28天销量 |
| totalSale90dCnt | integer | 90天销量 |
| totalSaleGmvAmt | number | 累计总GMV |
| totalSaleGmv7dAmt | number | 7天GMV |
| totalSaleGmv28dAmt | number | 28天GMV |
| totalVideoCnt | integer | 带货视频数 |
| totalLiveCnt | integer | 直播带货数 |
| totalIflCnt | integer | 带货达人数 |
| productCommissionRate | number | 商品佣金比例（小数，0.10=10%） |
| productRating | number | 商品评分 |
| reviewCount | integer | 评论数量 |
| skuCount | integer | SKU数量 |
| shopName | string | 店铺名称 |
| shopSellerId | string | 卖家ID |
| shopTotalUnitsSold | integer | 店铺总销量 |
| isCrossBorder | integer | 是否跨境：1=跨境，0=本地 |
| isSShopText | string | 是否全托管店铺（是/否） |
| freeShippingText | string | 是否包邮（是/否） |
| availableDate | string | 上架时间 |
| categoryName | string | 商品品类名称 |
| salesTrendFlagText | string | 销售趋势标记 |
| tiktokUrl | string | TikTok商品链接 |
| fastmossUrl | string | FastMoss商品详情链接 |
| imageUrl | string | 商品图片URL |

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
curl -X POST https://tool-gateway.linkfox.com/fastmoss/productSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "phone case",
    "region": "US",
    "orderField": "day7_units_sold",
    "pageSize": 10
  }'
```

带范围筛选的示例：

```bash
curl -X POST https://tool-gateway.linkfox.com/fastmoss/productSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "beauty",
    "region": "US",
    "commissionRateRange": {"min": 0.10},
    "creatorCountRange": {"min": 50},
    "orderField": "commission_rate",
    "pageSize": 10
  }'
```
