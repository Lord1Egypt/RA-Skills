---
name: linkfox-jiimore-get-niche-info
description: 基于极目数据查询亚马逊细分市场的核心指标、竞争格局、价格走势、断货率及市场增长趋势。
---

# 极目细分市场信息（Jiimore Niche Market Info）

本技能通过极目数据服务查询并分析亚马逊细分市场数据，帮助卖家深入了解特定细分市场的竞争、定价、评论与增长趋势。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过 `nicheId` 查询单个亚马逊细分市场的综合市场情报，涵盖市场概览、价格、搜索与转化、竞争集中度、商品上架、库存健康、卖家成熟度、评论洞察、广告与盈利等维度。
- 支持对比当前、90 天前、360 天前的时间快照，识别市场趋势。
- 支持美国（US）、日本（JP）、德国（DE）三个站点，默认 US。

### ❌ 边界与限制

- **单 ID 查询**：每次请求仅支持一个 `nicheId`，不支持批量查询；需对比多个细分市场时需分别调用。
- **三个站点**：仅支持 US、JP、DE，不支持其他站点。
- **需已知 nicheId**：本工具无法按关键词或品类搜索细分市场，用户须提供 `nicheId`。
- **不在范围内**：按关键词/品类搜索细分市场；单个 ASIN 级商品分析；ABA 搜索词数据（请用 ABA Data Explorer）；广告投放管理与 PPC 优化；Listing 文案撰写与评论管理。

## 核心概念

极目**细分市场**（niche market）代表亚马逊上一个细粒度的商品品类，每个细分市场由唯一的 `nicheId` 标识。本工具一次查询一个细分市场的综合市场情报，覆盖：

- **市场概览**：细分市场标题、需求评分、商品数、品牌数、销售伙伴数
- **价格**：均价、最低价、最高价
- **搜索与转化**：周/季度搜索量及增长率、搜索转化率、点击转化率、销量
- **竞争集中度**：前 5 / 前 20 商品与品牌点击份额（当前、90 天、360 天快照）
- **商品上架**：新上架商品数、90/180/360 天窗口的成功上架数
- **库存健康**：平均断货率趋势
- **卖家成熟度**：平均品牌年龄、平均销售伙伴年龄
- **评论洞察**：平均评论评分、平均评论数、正面/负面客户评论洞察
- **广告**：ACOS（广告销售成本比）、广告商品占比
- **盈利**：利润率 > 50% 的 SKU 占比、盈亏平衡比率、退货率

**支持站点**：US（美国）、JP（日本）、DE（德国），默认 **US**。

## 调用方式

- **API 端点**：`POST /jiimore/getNicheInfo`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/jiimore_get_niche_info.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-jiimore-get-niche-info-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 基础查询（US 站点）**
查询指定 nicheId 的美国站细分市场数据：
```
nicheId: "12345678"
countryCode: "US"
```

**2. 查询日本站细分市场**
```
nicheId: "87654321"
countryCode: "JP"
```

**3. 查询德国站细分市场**
```
nicheId: "11223344"
countryCode: "DE"
```

## 展示规则

1. **清晰呈现数据**：以结构化表格或分组区块展示查询结果，除非用户明确要求，否则不做主观商业建议。
2. **趋势对比**：当响应包含当前、90 天前、360 天前数据点时，并排展示以便用户识别趋势。
3. **百分比格式**：份额与比率值以百分比展示（如 0.35 显示为 35.0%）。
4. **评论洞察**：若存在正面/负面客户评论洞察，以列表形式呈现。
5. **图片展示**：若返回 `referenceAsinImageUrl`，展示或链接细分市场参考图片。
6. **错误处理**：查询失败时根据响应说明原因，并建议检查 nicheId 或 countryCode。
7. **结果组织建议**：按市场概览、价格与盈利、搜索与需求趋势、竞争格局、商品上架活动、评论与客户洞察、库存与运营等逻辑分组呈现。

## 用户表达与场景速查

**适用** —— 针对特定亚马逊细分市场的查询：

| 用户说 | 场景 |
|--------|------|
| "查一下这个细分市场"、"niche ID 信息" | 基础细分市场查询 |
| "这个细分市场竞争如何"、"品牌集中度" | 竞争分析 |
| "这个细分市场均价多少" | 价格情报 |
| "这个细分市场的搜索量"、"需求趋势" | 搜索与需求分析 |
| "上了多少新品"、"上架成功率" | 商品上架追踪 |
| "这个细分市场的评论评分"、"买家反馈洞察" | 评论分析 |
| "断货率"、"库存健康度" | 库存分析 |
| "这个细分市场值不值得做"、"细分市场机会" | 综合细分市场评估 |

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

# 极目-亚马逊-细分市场洞察信息 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/jiimore/getNicheInfo`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| nicheId | string | 是 | 细分市场ID，最大长度1000字符，只支持单个ID查询 |
| countryCode | string | 否 | 国家编码，仅支持 `US`、`JP`、`DE`，默认 `US` |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 细分市场信息列表，每个元素为包含以下字段的对象 |
| columns | array | 渲染的列 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### `data` 元素关键字段

#### 市场概览

| 字段 | 类型 | 说明 |
|------|------|------|
| nicheId | string | 细分市场ID |
| nicheTitle | string | 细分市场标题 |
| translationZh | string | 细分市场标题(中文) |
| referenceAsinImageUrl | string | 细分市场参考图片地址 |
| marketplaceId | string | 市场ID |
| demand | integer | 细分市场得分 |
| categorieList | array | 商品品类列表 |

#### 商品与品牌数量

| 字段 | 类型 | 说明 |
|------|------|------|
| productCount | integer | 商品数量 |
| productCountNow | integer | 商品数量(当前) |
| productCountT90Before | integer | 商品数量(90天前) |
| productCountT360Before | integer | 商品数量(360天前) |
| brandCount | integer | 品牌数量 |
| brandCountNow | integer | 品牌数量(当前) |
| brandCountT90Before | integer | 品牌数量(90天前) |
| brandCountT360Before | integer | 品牌数量(360天前) |
| brandCountT360Now | integer | 品牌数量(360天统计)(当前) |
| brandCountT360T90Before | integer | 品牌数量(360天统计)(90天前) |
| brandCountT360T360Before | integer | 品牌数量(360天统计)(360天前) |
| sellingPartnerCountNow | integer | 销售伙伴数量(当前) |
| sellingPartnerCountT90Before | integer | 销售伙伴数量(90天前) |
| sellingPartnerCountT360Before | integer | 销售伙伴数量(360天前) |
| sellingPartnerCountT360Now | integer | 销售伙伴数量(360 天统计)(当前) |
| sellingPartnerCountT360T90Before | integer | 销售伙伴数量(360 天统计)(90天前) |
| sellingPartnerCountT360T360Before | integer | 销售伙伴数量(360 天统计)(360天前) |

#### 价格

| 字段 | 类型 | 说明 |
|------|------|------|
| avgPrice | number | 产品均价 |
| avgProductPriceNow | number | 产品均价(当前) |
| avgProductPriceT90Before | number | 产品均价(90天前) |
| avgProductPriceT360Before | number | 产品均价(360天前) |
| minimumPrice | number | 产品最低价 |
| maximumPrice | number | 产品最高价 |

#### 搜索与转化

| 字段 | 类型 | 说明 |
|------|------|------|
| searchVolumeWeekly | integer | 搜索量（周数据） |
| searchVolumeQuarterly | integer | 搜索量（季度数据） |
| searchVolumeGrowthWeekly | number | 搜索量增长率（周数据） |
| searchVolumeGrowthQuarterly | number | 搜索量增长率（季度数据） |
| searchConversionRateWeekly | number | 搜索转换率（周数据） |
| searchConversionRateQuarterly | number | 搜索转换率（季度数据） |
| clickCountWeekly | integer | 点击量（周数据） |
| clickCountQuarterly | integer | 点击量（季度数据） |
| clickConversionRateQuarterly | number | 点击转换率（季度数据） |
| clickToSaleConversionWeekly | number | 点击转换率（周数据） |
| unitsSoldWeekly | integer | 销售数量（周数据） |
| unitsSoldQuarterly | integer | 销售数量（季度数据） |

#### 竞争 - 商品点击份额

| 字段 | 类型 | 说明 |
|------|------|------|
| top5ProductsClickShare | number | 排名前 5 位的商品点击份额 |
| top5ProductsClickShareNow | number | 前5个商品所占细分市场的点击量份额(当前) |
| top5ProductsClickShareT90Before | number | 前5个商品所占细分市场的点击量份额(90天前) |
| top5ProductsClickShareT360Before | number | 前5个商品所占细分市场的点击量份额(360天前) |
| top5ProductsClickShareT360Now | number | 排名前 5 位的商品点击份额（360天统计）(当前) |
| top5ProductsClickShareT360T90Before | number | 排名前 5 位的商品点击份额（360天统计）(90天前) |
| top5ProductsClickShareT360T360Before | number | 排名前 5 位的商品点击份额（360天统计）(360天前) |
| top20ProductsClickShareNow | number | 前20个商品所占细分市场的点击量份额（当前) |
| top20ProductsClickShareT90Before | number | 前20个商品所占细分市场的点击量份额（90天前) |
| top20ProductsClickShareT360Before | number | 前20个商品所占细分市场的点击量份额（360天前) |
| top20ProductsClickShareT360Now | number | 排名前20位的商品点击份额(360 天统计)(当前) |
| top20ProductsClickShareT360T90Before | number | 排名前20位的商品点击份额(360 天统计)(90天前) |
| top20ProductsClickShareT360T360Before | number | 排名前20位的商品点击份额(360 天统计)(360天前) |

#### 竞争 - 品牌点击份额

| 字段 | 类型 | 说明 |
|------|------|------|
| top5BrandsClickShare | number | 前5个品牌所占细分市场的点击量份额 |
| top5BrandsClickShareNow | number | 前5个品牌所占细分市场的点击量份额(当前) |
| top5BrandsClickShareT90Before | number | 前5个品牌所占细分市场的点击量份额(90天前) |
| top5BrandsClickShareT360Before | number | 前5个品牌所占细分市场的点击量份额(360天前) |
| top5BrandsClickShareT360Now | number | 前5个品牌所占细分市场的点击量份额(360 天统计)(当前) |
| top5BrandsClickShareT360T90Before | number | 前5个品牌所占细分市场的点击量份额(360 天统计)(90天前) |
| top5BrandsClickShareT360T360Before | number | 前5个品牌所占细分市场的点击量份额(360 天统计)(360天前) |
| top20BrandsClickShareNow | number | 前20个品牌所占细分市场的点击量份额(当前) |
| top20BrandsClickShareT90Before | number | 前20个品牌所占细分市场的点击量份额(90天前) |
| top20BrandsClickShareT360Before | number | 前20个品牌所占细分市场的点击量份额(360天前) |
| top20BrandsClickShareT360Now | number | 前20个品牌所占细分市场的点击量份额(360天统计)（当前) |
| top20BrandsClickShareT360T90Before | number | 前20个品牌所占细分市场的点击量份额(360天统计)（90天前) |
| top20BrandsClickShareT360T360Before | number | 前20个品牌所占细分市场的点击量份额(360天统计)（360天前) |

#### 商品上架

| 字段 | 类型 | 说明 |
|------|------|------|
| newProductsLaunchedSemiannual | integer | 已发布新产品的数量（半年数据） |
| newProductsLaunchedT180Now | integer | 已发布新产品的数量(180天统计)(当前) |
| newProductsLaunchedT180T90Before | integer | 已发布新产品的数量(180天统计)(90天前) |
| newProductsLaunchedT180T360Before | integer | 已发布新产品的数量(180天统计)(360天前) |
| newProductsLaunchedT360Now | integer | 新上架商品数(360天统计)(当前) |
| newProductsLaunchedT360T90Before | integer | 新上架商品数(360天统计)(90天前) |
| newProductsLaunchedT360T360Before | integer | 新上架商品数(360天统计)(360天前) |
| successfulLaunchedSemiannual | integer | 成功发布商品的数量（半年数据） |
| launchRateSemiannual | number | 发布商品的成功率（半年数据） |
| successfulLaunchesT90Now | integer | 成功上架数(90天统计)(当前） |
| successfulLaunchesT90T90Before | integer | 成功上架数(90天统计)(90天前) |
| successfulLaunchesT90T360Before | integer | 成功上架数(90天统计)(360天前) |
| successfulLaunchesT180Now | integer | 成功发布商品的数量（180 天统计）(当前) |
| successfulLaunchesT180T90Before | integer | 成功发布商品的数量（180 天统计）(90天前) |
| successfulLaunchesT180T360Before | integer | 成功发布商品的数量（180 天统计）(360天前) |
| successfulLaunchesT360Now | integer | 成功发布商品的数量（360 天统计）(当前) |
| successfulLaunchesT360T90Before | integer | 成功发布商品的数量（360 天统计）(90天前) |
| successfulLaunchesT360T360Before | integer | 成功发布商品的数量（360 天统计）(360天前) |

#### 库存与运营

| 字段 | 类型 | 说明 |
|------|------|------|
| avgOOSRateNow | number | 平均缺货率(当前) |
| avgOOSRateT90Before | number | 平均缺货率(90天前) |
| avgOOSRateT360Before | number | 平均缺货率(360天前) |
| avgOOSRateT360Now | number | 平均缺货率(360天统计)(当前) |
| avgOOSRateT360T90Before | number | 平均缺货率(360天统计)(90天前) |
| avgOOSRateT360T360Before | number | 平均缺货率(360天统计)(360天前) |
| primeProductsPercentageNow | number | prime商品的百分比(当前) |
| primeProductsPercentageT90Before | number | prime商品的百分比(90天前) |
| primeProductsPercentageT360Before | number | prime商品的百分比(360天前) |
| primeProductsPercentageT360Now | number | prime商品的百分比(360 天统计）(当前) |
| primeProductsPercentageT360T90Before | number | prime商品的百分比(360 天统计）(90天前) |
| primeProductsPercentageT360T360Before | number | prime商品的百分比(360 天统计）(360天前) |

#### 评论与评分

| 字段 | 类型 | 说明 |
|------|------|------|
| avgReviewRatingNow | number | 平均评论评分(当前) |
| avgReviewRatingT90Before | number | 平均评论评分(90天前) |
| avgReviewRatingT360Before | number | 平均评论评分(360天前) |
| avgReviewCountNow | number | 平均评论数(当前) |
| avgReviewCountT90Before | number | 平均评论数(90天前) |
| avgReviewCountT360Before | number | 平均评论数(360天前) |
| positiveCustomerReviewInsights | array | 正面客户评论见解信息 |
| negativeCustomerReviewInsights | array | 负面客户评论见解信息 |
| productStarRatingImpact | array | 产品星级影响力信息 |

#### 卖家成熟度

| 字段 | 类型 | 说明 |
|------|------|------|
| avgBrandAgeNow | number | 平均品牌年龄(当前) |
| avgBrandAgeT90Before | number | 平均品牌年龄(90天前) |
| avgBrandAgeT360Before | number | 平均品牌年龄(360天前) |
| avgBrandAgeQuarterly | number | 平均品牌年龄(季度数据) |
| avgBrandAgeT360Now | number | 平均品牌年龄(360 天统计)(当前) |
| avgBrandAgeT360T90Before | number | 平均品牌年龄(360 天统计)(90天前) |
| avgBrandAgeT360T360Before | number | 平均品牌年龄(360 天统计)(360天前) |
| avgSellingPartnerAgeNow | number | 平均销售伙伴年龄(当前) |
| avgSellingPartnerAgeT90Before | number | 平均销售伙伴年龄(90天前) |
| avgSellingPartnerAgeT360Before | number | 平均销售伙伴年龄(360天前) |
| avgBestSellerRankNow | number | 平均BestSeller排名(当前) |
| avgBestSellerRankT90Before | number | 平均BestSeller排名(90天前) |
| avgBestSellerRankT360Before | number | 平均BestSeller排名(360天前) |

#### 广告与盈利

| 字段 | 类型 | 说明 |
|------|------|------|
| acos | number | （ACOS）广告销售成本比 |
| sponsoredProductsPercentageNow | number | 已进行商品推广的商品的百分比(当前) |
| sponsoredProductsPercentageT90Before | number | 已进行商品推广的商品的百分比(90天前) |
| sponsoredProductsPercentageT360Before | number | 已进行商品推广的商品的百分比(360天前) |
| sponsoredProductsPercentageT360Now | number | 已进行商品推广的商品的百分比(360 天统计)(当前) |
| sponsoredProductsPercentageT360T90Before | number | 已进行商品推广的商品的百分比(360 天统计)(90天前) |
| sponsoredProductsPercentageT360T360Before | number | 已进行商品推广的商品的百分比(360 天统计)(360天前) |
| profitMarginGt50PctSkuRatio | number | 利润率大于50%的商品比例 |
| breakEvenRatio | number | 盈亏平衡比率 |
| returnRateAnnual | number | 退货率（全年数据） |
| cpc | object | CPC（每次点击费用）数据 |

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
curl -X POST https://tool-gateway.linkfox.com/jiimore/getNicheInfo \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"nicheId": "12345678", "countryCode": "US"}'
```
