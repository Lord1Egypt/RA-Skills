---
name: linkfox-jiimore-get-niche-review-from-keyword
description: 分析亚马逊细分市场的消费者评论，拆解好差评与舆情，以洞察用户痛点、需求和情感倾向。
---

# Jiimore 细分市场评论（Niche Review from Keyword）

本技能用于查询并分析亚马逊细分市场的消费者评论数据，帮助卖家从细分市场层面的产品评论中挖掘用户情感、痛点与真实需求。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 基于关键词识别相关亚马逊细分市场，聚合各细分市场中的消费者评论。
- 提取评论主题，按情感分类为正面评论（positive）与负面评论（negative）。
- 展示每个主题的被提及占比（`percentOfMentions`，0-1 比例，即 0%-100%），帮助卖家了解消费者喜欢什么、抱怨什么、有哪些改进机会。
- 支持按商品数量、品牌数量、销量、搜索量、转化率、退货率、新品成功率等多维筛选细分市场。

### ❌ 边界与限制

- **关键词语言**：`keyword` 必须使用目标站点的对应语言（US 用英文、DE 用德文、JP 用日文）。
- **站点覆盖**：仅支持 US（美国）、JP（日本）、DE（德国），默认 US。
- **评论粒度**：本工具工作在细分市场（niche）层面，不做单个 ASIN 的评论分析。
- **不在范围内**：纯关键词搜索量趋势（用 ABA 工具）、Listing 优化与文案撰写、广告策略与 PPC 管理、销量预估或收入预测。

## 核心概念

细分市场评论分析会聚合亚马逊某细分市场下各商品的消费者评论。给定关键词后，系统识别相关细分市场，提取评论主题，将其归类为正面或负面，并统计每个主题的被提及频率，帮助卖家理解消费者喜欢什么、抱怨什么、改进机会在哪里。

**评论类型**：每条评论条目分类为 `positive`（正面）或 `negative`（负面），反映该评论主题的整体情感倾向。

**提及占比**：`percentOfMentions` 取值 0-1（即 0%-100%），表示该主题在细分市场所有评论中的出现频率；占比越高表示越多消费者在谈论该主题。

**支持站点**：US（美国）、JP（日本）、DE（德国），默认 US。

## 调用方式

- **API 端点**：`POST /jiimore/getNicheReviewFromKeyword`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/jiimore_get_niche_review.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-jiimore-get-niche-review-from-keyword-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 关键词的基础细分市场评论查询**
> "分析美国站 yoga mat 相关细分市场的消费者评论"
参数：`{"keyword": "yoga mat", "countryCode": "US"}`

**2. 高搜索量细分市场的评论**
> "看下 wireless earbuds 7 天搜索量超过 10000 的细分市场评论"
参数：`{"keyword": "wireless earbuds", "countryCode": "US", "searchVolumeT7Min": 10000}`

**3. 低集中度细分市场的评论洞察**
> "找 pet bed 中前 5 品牌点击份额低于 30% 的细分市场评论"
参数：`{"keyword": "pet bed", "countryCode": "US", "top5BrandsClickShareMax": 0.3}`

**4. 日本站细分市场评论**
> "分析日本站 wireless earbuds 的细分市场评论"
参数：`{"keyword": "wireless earbuds", "countryCode": "JP"}`

**5. 按需求得分排序**
> "按需求得分降序展示 kitchen organizer 的细分市场评论"
参数：`{"keyword": "kitchen organizer", "sortField": "demand", "sortType": "desc"}`

**6. 按新品成功率筛选**
> "找 phone case 中 180 天新品发布成功率高于 20% 的细分市场"
参数：`{"keyword": "phone case", "launchRateT180Min": 0.2}`

**7. 低退货率细分市场**
> "展示 water bottle 退货率低于 5% 的细分市场评论主题"
参数：`{"keyword": "water bottle", "returnRateT360Max": 0.05}`

## 展示规则

1. **清晰呈现数据**：以结构化表格展示细分市场名称、评论类型（正面/负面）、主题、提及占比及评论样例。
2. **百分比格式**：将 0-1 比例值转为百分比展示（如 0.15 显示为 15%）。
3. **情感区分**：呈现结果时分组或明确标注正面与负面评论，便于用户快速识别机会与痛点。
4. **客观呈现数据**：展示数据时遵循「只呈现数据，不做主观商业建议」原则；可客观标注高占比负面评论对应的潜在改进点、高占比正面评论对应的产品特征。
5. **大结果提示**：结果较多时优先展示最相关数据，并提示用户可翻页。
6. **错误处理**：查询失败时说明原因，并建议调整关键词或筛选条件。
7. **语言提醒**：用户提供的关键词与目标站点语言不符时，提醒使用站点对应语言（US 英文、DE 德文、JP 日文）。

## 用户表达与场景速查

**适用** —— 亚马逊细分市场的消费者评论与情感分析：

| 用户说 | 场景 |
|--------|------|
| "XX 的消费者怎么说"、"XX 客户评价" | 细分市场评论主题查询 |
| "XX 的客户痛点" | 负面评论分析 |
| "XX 买家喜欢什么功能" | 正面评论分析 |
| "XX 细分市场评论情感" | 整体情感拆解 |
| "XX 的消费者需求洞察" | 从评论中提取需求信号 |
| "XX 产品常见抱怨" | 负面主题挖掘 |
| "XX 产品为什么受欢迎" | 正面主题挖掘 |
| "细分市场评论分析" | 通用细分市场评论探索 |

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

# 极目-亚马逊-细分市场评论 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/jiimore/getNicheReviewFromKeyword`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

### 必填参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 关键词（必填，请使用对应站点的语言，如美国站用英文，德国站用德文），最大长度1000字符 |

### 站点与分页

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| countryCode | string | 否 | US | 国家编码，可选值：`US`（美国）、`JP`（日本）、`DE`（德国） |
| page | integer | 否 | 1 | 页码（从1开始） |
| pageSize | integer | 否 | 50 | 每页返回数量（10-100） |

### 排序

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| sortField | string | 否 | unitsSoldT7 | 排序字段，可选值：`clickConversionRateT7`（7天点击转化率）、`demand`（需求得分）、`avgPrice`（商品均价）、`maximumPrice`（商品最高价）、`minimumPrice`（商品最低价）、`productCount`（商品数量）、`searchConversionRateT7`（7天搜索转化率）、`searchVolumeT7`（7天搜索量）、`unitsSoldT7`（7天销量）、`searchVolumeGrowthT7`（搜索增长率）、`clickCountT90`（90天点击量）、`clickCountT7`（周点击量）、`brandCount`（品牌数量）、`top5BrandsClickShare`（TOP5品牌份额）、`newProductsLaunchedT180`（180d新品成功率-发布数）、`successfulLaunchesT180`（180d新品成功率-新品数）、`launchRateT180`（180d新品成功率-发布率）、`top5ProductsClickShare`（top5商品点击份额）、`returnRateT360`（退货率）、`clickConversionRateT90`（90天点击转化率）、`searchConversionRateT90`（90天搜索转化率）、`searchVolumeT90`（90天搜索量）、`unitsSoldT90`（90天销量）、`unitsSoldGrowthT90`（90天销量增长率）、`searchVolumeGrowthT90`（90天搜索增长率）、`acos`、`profitRate50`（50%自然单的利润率） |
| sortType | string | 否 | desc | 排序方式，可选值：`desc`（降序）、`asc`（升序） |

### 细分市场筛选（均为选填）

**商品与品牌指标**：

| 参数 | 类型 | 说明 |
|------|------|------|
| productCountMin | integer | 商品数量（当前）最小值 |
| productCountMax | integer | 商品数量（当前）最大值 |
| brandCountMin | integer | 品牌数量最小值 |
| brandCountMax | integer | 品牌数量最大值 |
| avgPriceMin | number | 平均价格（当前）最小值 |
| avgPriceMax | number | 平均价格（当前）最大值 |

**销量与搜索量**：

| 参数 | 类型 | 说明 |
|------|------|------|
| unitsSoldT7Min | integer | 销售量（7天统计）最小值 |
| unitsSoldT7Max | integer | 销售量（7天统计）最大值 |
| searchVolumeT7Min | integer | 搜索量（7天统计）最小值 |
| searchVolumeT7Max | integer | 搜索量（7天统计）最大值 |
| clickCountT7Min | integer | 点击量（7天统计）最小值 |
| clickCountT7Max | integer | 点击量（7天统计）最大值 |

**转化率**（数值范围为0-1，代表0%-100%）：

| 参数 | 类型 | 说明 |
|------|------|------|
| clickConversionRateT7Min | number | 点击转换率（7天统计）最小值 |
| clickConversionRateT7Max | number | 点击转换率（7天统计）最大值 |

**市场集中度**（数值范围为0-1，代表0%-100%）：

| 参数 | 类型 | 说明 |
|------|------|------|
| top5BrandsClickShareMin | number | 前5个品牌所占细分市场的点击量份额最小值 |
| top5BrandsClickShareMax | number | 前5个品牌所占细分市场的点击量份额最大值 |
| top5ProductsClickShareMin | number | 排名前5位的商品点击份额（当前）最小值 |
| top5ProductsClickShareMax | number | 排名前5位的商品点击份额（当前）最大值 |
| sponsoredProductsPercentageMin | number | SP广告占比最小值 |
| sponsoredProductsPercentageMax | number | SP广告占比最大值 |

**品牌年龄**：

| 参数 | 类型 | 说明 |
|------|------|------|
| avgBrandAgeMin | number | 平均品牌年龄（当前）最小值 |
| avgBrandAgeMax | number | 平均品牌年龄（当前）最大值 |
| avgBrandAgeQoqMin | number | 平均品牌年龄（90天统计）最小值 |
| avgBrandAgeQoqMax | number | 平均品牌年龄（90天统计）最大值 |
| avgBrandAgeYoyMin | number | 平均品牌年龄（360天统计）最小值 |
| avgBrandAgeYoyMax | number | 平均品牌年龄（360天统计）最大值 |

**销售伙伴年龄**：

| 参数 | 类型 | 说明 |
|------|------|------|
| avgSellingPartnerAgeMin | number | 平均销售伙伴年龄最小值 |
| avgSellingPartnerAgeMax | number | 平均销售伙伴年龄最大值 |
| avgSellingPartnerAgeQoqMin | number | 平均销售伙伴年龄（90天统计）最小值 |
| avgSellingPartnerAgeQoqMax | number | 平均销售伙伴年龄（90天统计）最大值 |
| avgSellingPartnerAgeYoyMin | number | 平均销售伙伴年龄（360天统计）最小值 |
| avgSellingPartnerAgeYoyMax | number | 平均销售伙伴年龄（360天统计）最大值 |

**新品与退货指标**（数值范围为0-1，代表0%-100%）：

| 参数 | 类型 | 说明 |
|------|------|------|
| launchRateT180Min | number | 发布商品的成功率（180天统计）最小值 |
| launchRateT180Max | number | 发布商品的成功率（180天统计）最大值 |
| newProductRateT180 | number | 新商品占比（180天统计）最小值 |
| returnRateT360Min | number | 退货率（360天统计）最小值 |
| returnRateT360Max | number | 退货率（360天统计）最大值 |

**广告**：

| 参数 | 类型 | 说明 |
|------|------|------|
| cpcMediumMin | number | CPC（当前）最小值 |
| cpcMediumMax | number | CPC（当前）最大值 |

**系统字段**（可忽略，由系统自动处理）：


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总数 |
| data | array | 细分市场评论列表（详见下方数据项字段） |
| columns | array | 渲染的列 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |
| title | string | 标题 |

### 数据项字段

| 字段 | 类型 | 说明 |
|------|------|------|
| nicheId | string | 细分市场ID |
| nicheName | string | 细分市场名称 |
| keyword | string | 关键词 |
| reviewType | string | 评论类型（值范围为【正面评论】、【负面评论】） |
| topic | string | 评论主题 |
| percentOfMentions | number | 占比（数值范围为0-1，代表0%-100%） |
| reviewExample | string | 评论样例 |

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
curl -X POST https://tool-gateway.linkfox.com/jiimore/getNicheReviewFromKeyword \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "yoga mat",
    "countryCode": "US",
    "pageSize": 20,
    "sortField": "unitsSoldT7",
    "sortType": "desc"
  }'
```

### 带筛选条件的示例

```bash
curl -X POST https://tool-gateway.linkfox.com/jiimore/getNicheReviewFromKeyword \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "wireless earbuds",
    "countryCode": "US",
    "searchVolumeT7Min": 5000,
    "top5BrandsClickShareMax": 0.5,
    "sortField": "demand",
    "sortType": "desc",
    "page": 1,
    "pageSize": 50
  }'
```
