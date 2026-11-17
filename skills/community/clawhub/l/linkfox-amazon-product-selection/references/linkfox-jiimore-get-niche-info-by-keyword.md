---
name: linkfox-jiimore-get-niche-info-by-keyword
description: 通过关键词深度评估亚马逊细分市场的竞争格局，包括行业垄断度、品牌集中度、新品成功率及市场机会评分。
---

# Jiimore 关键词细分市场（Niche Info by Keyword）

本技能用于按关键词查询并分析亚马逊细分市场数据，帮助卖家评估细分市场的竞争强度、品牌成熟度、价格结构与入场机会。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 按关键词查询亚马逊细分市场，返回搜索量、销量、点击率、品牌数量、头部品牌集中度、新品成功率、CPC 预估及综合需求得分等多维分析数据。
- 支持按商品数量、价格、搜索量、销量、点击量、转化率、品牌指标、卖家指标、广告竞争、新品与退货等多维条件筛选与排序。
- 覆盖 **US**、**JP**、**DE** 三个站点。

### ❌ 边界与限制

- **站点限制**：仅支持 US、JP、DE，其他国家编码会被拒绝。
- **关键词必填**：每次查询必须包含 `keyword`，且应使用目标站点语言（US 用英文、JP 用日文、DE 用德文）；用户提供其他语言时需先翻译再调用。
- **分页上限**：每页最多返回 100 条。
- **百分比值域**：所有比率/份额参数使用 0-1 区间（非 0-100），构造筛选时需注意取值。
- **不在范围内**：单个 ASIN 表现或销量预估；搜索词排名趋势（用 ABA 数据工具）；广告投放管理与竞价优化；商品评论分析与 Listing 优化；货源采购与物流规划。

## 核心概念

**细分市场（niche）**是亚马逊上共享同一关键词主题的商品集合。本工具为每个细分市场返回搜索量、销量、点击率、品牌数量、头部品牌集中度、新品成功率、CPC 预估及综合需求得分等丰富分析维度。

- **关键词必填**：每次查询必须包含 `keyword`，并使用目标站点语言。用户提供其他语言时，先翻译为目标站点语言再调用。
- **百分比字段**：部分参数与响应字段使用 0-1 小数表示 0%-100%；展示给用户时换算为百分比（如 0.35 -> 35%）。
- **需求得分**：`demand` 字段是每个细分市场的综合机会评分，数值越高表示市场需求潜力越大。

## 调用方式

- **API 端点**：`POST /jiimore/getNicheInfoByKeyword`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/jiimore_get_niche_info_by_keyword.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-jiimore-get-niche-info-by-keyword-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 基础细分市场探索**
查询美国市场与 "wireless earbuds" 相关的细分市场，按周销量排序：
```json
{
  "keyword": "wireless earbuds",
  "countryCode": "US",
  "sortField": "unitsSoldT7",
  "sortType": "desc"
}
```

**2. 低竞争细分市场发现**
查找 "yoga mat" 下前 5 品牌点击份额低于 50%、品牌数超过 20 的细分市场：
```json
{
  "keyword": "yoga mat",
  "countryCode": "US",
  "top5BrandsClickShareMax": 0.5,
  "brandCountMin": 20,
  "sortField": "demand",
  "sortType": "desc"
}
```

**3. 高需求高转化细分市场**
查找 "phone case" 下周搜索量大于 10000、点击转化率高于 10% 的细分市场：
```json
{
  "keyword": "phone case",
  "countryCode": "US",
  "searchVolumeT7Min": 10000,
  "clickConversionRateT7Min": 0.1,
  "sortField": "searchVolumeT7",
  "sortType": "desc"
}
```

**4. 新品机会分析**
查找 "LED light" 下新品成功率高于 20%、退货率低于 5% 的细分市场：
```json
{
  "keyword": "LED light",
  "countryCode": "US",
  "launchRateT180Min": 0.2,
  "returnRateT360Max": 0.05,
  "sortField": "launchRateT180",
  "sortType": "desc"
}
```

**5. 日本市场细分调研**
探索日本市场与耳机相关的细分市场，按需求得分排序：
```json
{
  "keyword": "ヘッドホン",
  "countryCode": "JP",
  "sortField": "demand",
  "sortType": "desc"
}
```

**6. 价格区间细分分析**
查找 "backpack" 下均价在 20-50 美元、广告饱和度较低的细分市场：
```json
{
  "keyword": "backpack",
  "countryCode": "US",
  "avgPriceMin": 20,
  "avgPriceMax": 50,
  "sponsoredProductsPercentageMax": 0.3,
  "sortField": "unitsSoldT7",
  "sortType": "desc"
}
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示结果，将小数比率换算为百分比（如 0.25 -> 25%）。
2. **突出关键指标**：将细分市场标题、需求得分、周搜索量、周销量、品牌数量、前 5 品牌点击份额作为主列展示。
3. **翻译细分市场标题**：当 `translationZh` 字段存在且用户偏好中文时，与原 `nicheTitle` 并列展示。
4. **分页提示**：`total` 超出当前页大小时，告知总数并建议是否继续翻页。
5. **错误处理**：查询失败时根据响应消息说明原因，并建议调整筛选条件（如放宽区间、检查关键词）。
6. **CPC 展示**：存在 CPC 数据时，同时展示低、中、高三档，给出完整广告成本图景。
7. **不做主观建议**：客观呈现数据，不主动附加商业建议；仅在用户明确要求解读时才提供。

## 用户表达与场景速查

**适用** —— 按关键词的细分市场级市场调研：

| 用户说 | 场景 |
|--------|------|
| "XX 市场有没有机会" | 细分市场机会评估 |
| "XX 关键词竞争有多激烈" | 垄断/品牌集中度 |
| "给 XX 找低竞争细分市场" | 蓝海细分市场发现 |
| "XX 的新品成功率是多少" | 新入场可行性 |
| "看下 XX 的细分市场数据" | 通用细分市场探索 |
| "XX 哪些细分市场需求高" | 需求驱动细分市场排名 |
| "XX 细分市场的 CPC/广告成本" | 广告成本分析 |
| "找 XX 高转化的细分市场" | 转化导向细分市场 |
| "XX 市场的品牌集中度" | 品牌主导度评估 |

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

# 极目-亚马逊-细分市场信息 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/jiimore/getNicheInfoByKeyword`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

### 必填参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 关键词（必填，并根据所选国家，翻译关键词为对应国家的语言），最大长度1000字符 |

### 站点与分页

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| countryCode | string | 否 | US | 国家编码，可选值：`US`（美国）、`JP`（日本）、`DE`（德国） |
| page | integer | 否 | 1 | 页码（从1开始） |
| pageSize | integer | 否 | 50 | 每页返回数量（10-100） |
| sortField | string | 否 | unitsSoldT7 | 排序字段（见下方排序选项） |
| sortType | string | 否 | desc | 排序方式：`desc`（降序）或 `asc`（升序） |

### 筛选参数（均为可选）

**商品与价格**：

| 参数 | 类型 | 说明 |
|------|------|------|
| productCountMin | integer | 商品数量（当前）最小值 |
| productCountMax | integer | 商品数量（当前）最大值 |
| avgPriceMin | number | 平均价格（当前）最小值 |
| avgPriceMax | number | 平均价格（当前）最大值 |

**搜索与销售（7天统计）**：

| 参数 | 类型 | 说明 |
|------|------|------|
| searchVolumeT7Min | integer | 搜索量（7天统计）最小值 |
| searchVolumeT7Max | integer | 搜索量（7天统计）最大值 |
| unitsSoldT7Min | integer | 销售量（7天统计）最小值 |
| unitsSoldT7Max | integer | 销售量（7天统计）最大值 |
| clickCountT7Min | integer | 点击量（7天统计）最小值 |
| clickCountT7Max | integer | 点击量（7天统计）最大值 |
| clickConversionRateT7Min | number | 点击转换率（7天统计）最小值，数值范围为0-1，代表0%-100% |
| clickConversionRateT7Max | number | 点击转换率（7天统计）最大值，数值范围为0-1，代表0%-100% |

**品牌指标**：

| 参数 | 类型 | 说明 |
|------|------|------|
| brandCountMin | integer | 品牌数量最小值 |
| brandCountMax | integer | 品牌数量最大值 |
| top5BrandsClickShareMin | number | 前5个品牌所占细分市场的点击量份额最小值，数值范围为0-1，代表0%-100% |
| top5BrandsClickShareMax | number | 前5个品牌所占细分市场的点击量份额最大值，数值范围为0-1，代表0%-100% |
| avgBrandAgeMin | number | 平均品牌年龄（当前）最小值 |
| avgBrandAgeMax | number | 平均品牌年龄（当前）最大值 |
| avgBrandAgeQoqMin | number | 平均品牌年龄（90天统计）最小值 |
| avgBrandAgeQoqMax | number | 平均品牌年龄（90天统计）最大值 |
| avgBrandAgeYoyMin | number | 平均品牌年龄（360天统计）最小值 |
| avgBrandAgeYoyMax | number | 平均品牌年龄（360天统计）最大值 |

**卖家指标**：

| 参数 | 类型 | 说明 |
|------|------|------|
| avgSellingPartnerAgeMin | number | 平均销售伙伴年龄最小值 |
| avgSellingPartnerAgeMax | number | 平均销售伙伴年龄最大值 |
| avgSellingPartnerAgeQoqMin | number | 平均销售伙伴年龄（90天统计）最小值 |
| avgSellingPartnerAgeQoqMax | number | 平均销售伙伴年龄（90天统计）最大值 |
| avgSellingPartnerAgeYoyMin | number | 平均销售伙伴年龄（360天统计）最小值 |
| avgSellingPartnerAgeYoyMax | number | 平均销售伙伴年龄（360天统计）最大值 |

**竞争与广告**：

| 参数 | 类型 | 说明 |
|------|------|------|
| top5ProductsClickShareMin | number | 排名前5位的商品点击份额（当前）最小值，数值范围为0-1，代表0%-100% |
| top5ProductsClickShareMax | number | 排名前5位的商品点击份额（当前）最大值，数值范围为0-1，代表0%-100% |
| sponsoredProductsPercentageMin | number | SP广告占比最小值，数值范围为0-1，代表0%-100% |
| sponsoredProductsPercentageMax | number | SP广告占比最大值，数值范围为0-1，代表0%-100% |
| cpcMediumMin | number | CPC（当前）最小值 |
| cpcMediumMax | number | CPC（当前）最大值 |

**新品与退货**：

| 参数 | 类型 | 说明 |
|------|------|------|
| launchRateT180Min | number | 发布商品的成功率（180天统计）最小值，数值范围为0-1，代表0%-100% |
| launchRateT180Max | number | 发布商品的成功率（180天统计）最大值，数值范围为0-1，代表0%-100% |
| newProductRateT180 | number | 新商品占比（180天统计）最小值，数值范围为0-1，代表0%-100% |
| returnRateT360Min | number | 退货率（360天统计）最小值，数值范围为0-1，代表0%-100% |
| returnRateT360Max | number | 退货率（360天统计）最大值，数值范围为0-1，代表0%-100% |

### 排序选项

| 值 | 说明 |
|------|------|
| unitsSoldT7 | 7天销量 |
| searchVolumeT7 | 7天搜索量 |
| demand | 需求得分 |
| avgPrice | 商品均价 |
| maximumPrice | 商品最高价 |
| minimumPrice | 商品最低价 |
| productCount | 商品数量 |
| searchConversionRateT7 | 7天搜索转化率 |
| clickConversionRateT7 | 7天点击转化率 |
| searchVolumeGrowthT7 | 搜索增长率 |
| clickCountT7 | 周点击量 |
| clickCountT90 | 90天点击量 |
| brandCount | 品牌数量 |
| top5BrandsClickShare | TOP5品牌份额 |
| top5ProductsClickShare | top5商品点击份额 |
| newProductsLaunchedT180 | 180d新品成功率-发布数 |
| successfulLaunchesT180 | 180d新品成功率-新品数 |
| launchRateT180 | 180d新品成功率-发布率 |
| returnRateT360 | 退货率 |
| clickConversionRateT90 | 90天点击转化率 |
| searchConversionRateT90 | 90天搜索转化率 |
| searchVolumeT90 | 90天搜索量 |
| unitsSoldT90 | 90天销量 |
| unitsSoldGrowthT90 | 90天销量增长率 |
| searchVolumeGrowthT90 | 90天搜索增长率 |
| acos | 广告销售成本比 |
| profitRate50 | 50%自然单的利润率 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总数 |
| data | array | 细分市场信息列表（见下方细分市场对象字段） |
| columns | array | 渲染的列 |
| title | string | 标题 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 细分市场对象字段（`data` 数组内）

| 字段 | 类型 | 说明 |
|------|------|------|
| nicheId | string | 细分市场ID |
| nicheTitle | string | 细分市场标题 |
| translationZh | string | 细分市场标题(中文) |
| demand | integer | 细分市场得分 |
| productCount | integer | 商品数量 |
| avgPrice | number | 产品均价 |
| minimumPrice | number | 产品最低价 |
| maximumPrice | number | 产品最高价 |
| searchVolumeWeekly | integer | 搜索量（周数据） |
| searchVolumeQuarterly | integer | 搜索量（季度数据） |
| searchVolumeGrowthWeekly | number | 搜索量增长率（周数据） |
| searchVolumeGrowthQuarterly | number | 搜索量增长率（季度数据） |
| unitsSoldWeekly | integer | 销售数量（周数据） |
| unitsSoldQuarterly | integer | 销售数量（季度数据） |
| clickCountWeekly | integer | 点击量（周数据） |
| clickCountQuarterly | integer | 点击量（季度数据） |
| clickToSaleConversionWeekly | number | 点击转换率（周数据） |
| clickConversionRateQuarterly | number | 点击转换率（季度数据） |
| searchConversionRateWeekly | number | 搜索转换率（周数据） |
| searchConversionRateQuarterly | number | 搜索转换率（季度数据） |
| brandCount | integer | 品牌数量 |
| top5BrandsClickShare | number | 前5个品牌所占细分市场的点击量份额 |
| top5ProductsClickShare | number | 排名前5位的商品点击份额 |
| avgBrandAgeNow | number | 平均品牌年龄(当前) |
| avgBrandAgeQuarterly | number | 平均品牌年龄(季度数据) |
| newProductsLaunchedSemiannual | integer | 已发布新产品的数量（半年数据） |
| successfulLaunchedSemiannual | integer | 成功发布商品的数量（半年数据） |
| launchRateSemiannual | number | 发布商品的成功率（半年数据） |
| returnRateAnnual | number | 退货率（全年数据） |
| acos | number | （ACOS）广告销售成本比 |
| profitMarginGt50PctSkuRatio | number | 利润率大于50%的商品比例 |
| breakEvenRatio | number | 盈亏平衡比率 |
| cpc | object | CPC数据：`{ high（最高价）, medium（中间价）, low（最低价） }` |
| categorieList | array | 商品类目列表 |
| referenceAsinImageUrl | string | 细分市场参考图片地址 |

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
curl -X POST https://tool-gateway.linkfox.com/jiimore/getNicheInfoByKeyword \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "wireless earbuds",
    "countryCode": "US",
    "sortField": "demand",
    "sortType": "desc",
    "page": 1,
    "pageSize": 20
  }'
```

### 带筛选条件的查询示例

```bash
curl -X POST https://tool-gateway.linkfox.com/jiimore/getNicheInfoByKeyword \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "yoga mat",
    "countryCode": "US",
    "top5BrandsClickShareMax": 0.5,
    "brandCountMin": 20,
    "searchVolumeT7Min": 5000,
    "sortField": "unitsSoldT7",
    "sortType": "desc",
    "page": 1,
    "pageSize": 50
  }'
```
