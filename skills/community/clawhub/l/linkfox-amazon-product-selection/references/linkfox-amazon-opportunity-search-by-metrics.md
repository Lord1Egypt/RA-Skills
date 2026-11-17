---
name: linkfox-amazon-opportunity-search-by-metrics
description: 基于 30+ 项商业指标进行亚马逊反向选品，筛选符合特定市场规模、竞争密度、人群画像及定价机会的细分赛道。
---

# 亚马逊机会指标反向筛选（Amazon Opportunity Screener by Metrics）

本技能引导你从历史机会报告沉淀的指标数据池中**反向检索**亚马逊赛道与关键词，把模糊的选品想法（低竞争、需求增长、蓝海、痛点机会等）转化为具体的候选赛道。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 基于商业维度（市场规模与增长、竞争密度、价格与档位、人群画像、产品特征、评论卖点/痛点）反向筛选亚马逊**赛道/关键词**级记录。
- 每条记录约 37 个字段，覆盖赛道快照：市场规模、增长、竞争、价格档位、人群、特征与评论主题。
- 支持按关键词文本片段、赛道名片段以及任意指标过滤字段组合检索，结果按采集时间倒序返回。

### ❌ 边界与限制

- **仅美国站**：当前仅支持美国市场（`amazonDomain` = `US`），其他站点暂不支持。
- **无分页**：无 `page` 参数，靠 `limit`（最大 200）扩大候选池，按采集时间倒序返回最近 N 条。
- **至少一个过滤条件**：未提供 `keyword` / `nicheName` 且无任何指标过滤字段的请求会被拒绝。
- **快照数据**：记录聚合自历史机会报告，新报告会逐步刷新数据池，但单条记录非实时。
- **赛道级粒度**：输出为赛道/关键词级，非 ASIN 级。如需钻取赛道内具体商品，转交 `linkfox-amazon-search`、`linkfox-keepa-product-search` 等。
- **不支持二次聚合**：结果供前端渲染、不入库，无法喂给 `@智能数据查询` 做分组统计。
- **不在范围内**：对单个关键词做多维度综合 AI 报告（用 `linkfox-amazon-opportunity-report`）；ASIN 级竞品/销量调研（用 SellerSprite / Keepa / Sorftime）；实时关键词排名与搜索词挖掘（用 ABA / SIF 工具）。

## 核心概念

本工具暴露一个可查询的**赛道级指标池**（每条记录约 37 个字段），蒸馏自历史亚马逊机会报告。它不是生成新报告（正向分析），而是让你按 30+ 项商业维度**反向过滤**已有数据池，返回匹配的 `(站点, 关键词)` 记录，按采集时间倒序。

记录粒度为**赛道/关键词**级，非 ASIN 级。每条记录代表一个赛道快照——其市场规模、增长、竞争、价格档位、人群画像、核心特征与评论主题。

**正向 vs 反向**：用户已有具体关键词、要一份综合 AI 报告时用 `linkfox-amazon-opportunity-report`；用户已有商业筛选条件、要发现哪些关键词/赛道符合时用本技能。

**筛选维度**：过滤参数分为六大商业维度——市场规模与增长、竞争密度、价格与档位、人群画像、产品特征、评论卖点/痛点。完整参数列表、类型与取值范围见 [references/api.md](references/api.md)。

## 调用方式

- **API 端点**：`POST /amazon/opportunity/searchByMetrics`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/amazon_opportunity_screener.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-opportunity-search-by-metrics-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 查询构建

用户用自然语言表达商业意图，你将其映射为**最小可行过滤集**。原则：

1. **把意图转为具体边界**："低竞争" → `nicheBrandCountLte: 20`；"快速增长" → `nicheSearchVolumeYoyChangePctAtLeastGte: 100`（同比 ≥100%）；"新人友好" → `featureNewAvgReviewCountAtLeastLte: 500`。
2. **先窄后宽**：首次通常用 2–4 个强过滤 + `limit=25`。若结果为空或过少，放宽最激进的过滤，而非新增过滤。
3. **配对互补信号**：品牌级 + 产品级集中度（`featureTop5BrandSharePctAtLeastLte` + `nicheTop5ProductClickSharePctAtLeastGte`）揭示"品牌分散但产品集中"——品牌延伸切入信号。
4. **标签字段用 snake_case 片段**：`featureEmergingTrendTagsContains`、`demoLifeStageTagsContains`、`reviewNegativeTop1Topic` 等接受 snake_case 词片段并做 LIKE 匹配。传一个词根（`size`、`parent`、`cordless`）即可覆盖归一化变体。
5. **忠于用户意图**：不要静默添加用户未提的过滤。用户只说"增长"就只过滤增长，除非其明确提到价格否则不要额外约束价格。

## 使用示例

**1. 按关键词反向追溯赛道**
> "反向查一下 whoop band 这个词的赛道"
```json
{"keyword": "whoop band", "limit": 25}
```

**2. 新人友好的低竞争赛道**
```json
{"nicheBrandCountLte": 20, "featureNewAvgReviewCountAtLeastLte": 500, "limit": 25}
```

**3. 高增长蓝海（同比 ≥100%，品牌尚未涌入）**
```json
{"nicheSearchVolumeYoyChangePctAtLeastGte": 100, "nicheBrandCountYoyChangePctAtLeastLte": 30, "limit": 25}
```

**4. 中档价格缺口（低价主导、中档稀缺）**
```json
{"priceEntryClickSharePctAtLeastGte": 70, "priceMidClickSharePctAtLeastLte": 5, "limit": 25}
```

**5. 痛点切入——尺码投诉强烈**
```json
{"reviewNegativeTop1Topic": "size", "reviewNegativeTop1PctAtLeastGte": 70, "limit": 25}
```

**6. 高端友好的女性主导赛道**
```json
{"demoGenderDominant": "female", "demoPrimaryIncomeTier": "high", "priceHighClickSharePctAtLeastGte": 25, "limit": 25}
```

**7. Q4 季节性赛道且峰值搜索 ≥10 万**
```json
{"nichePeakMonthGte": 11, "nichePeakMonthLte": 12, "nichePeakSearchVolumeAtLeastGte": 100000, "limit": 25}
```

**8. 追踪某竞品品牌周边赛道**
```json
{"featureTopBrandsContains": "WHOOP", "limit": 50}
```

## 展示规则

1. **只呈现数据**：把返回的赛道以干净对比表呈现——赛道名/关键词、市场规模、增长、品牌数、价格区间、关键标签。不做主观商业建议。
2. **回显当前筛选**：把你使用的过滤集回显出来便于用户调整（如"当前筛选：品牌数 ≤ 20 且搜索量同比 ≥ 100%"）。
3. **时间快照提示**：记录反映采集时点数据，非持续更新。当结果看起来过时或与用户外部认知冲突时说明这一点。
4. **空/少结果处理**：若 `data` 为空或很短，建议放宽最激进的过滤，而非从头再问用户。
5. **错误处理**：查询失败时基于 `msg` 字段说明原因（最常见是"参数全空"拦截），并建议至少添加一个过滤。
6. **不支持二次聚合**：结果供前端渲染、不入库，无法喂给 `@智能数据查询` 做进一步聚合。用户要跨赛道分组统计时，本地计算或先拉更大 `limit`。

## 用户表达与场景速查

**适用** —— 美国亚马逊市场赛道级反向选品：

| 用户说 | 场景 |
|--------|------|
| "低竞争赛道"、"新人友好"、"品牌少" | 品牌密度过滤 |
| "品牌在退出"、"老玩家在撤退" | 品牌数同比为负 |
| "高增长赛道"、"在涨"、"同比 ≥100%" | 搜索量同比过滤 |
| "中档蓝海"、"低价主导但中档稀缺" | 价格档位份额缺口 |
| "高端友好"、"高收入人群" | 收入档 + 高档份额 |
| "女性/男性/混合市场" | 性别主导过滤 |
| "宝妈/学生/退休人群/健身爱好者" | 生命阶段标签 |
| "尺码/质量/耐用性痛点强烈" | 差评主题 + 占比 |
| "舒适驱动"、"性价比卖家" | 好评主题 + 占比 |
| "追踪品牌 X 周边所有赛道" | `featureTopBrandsContains` |
| "Q4 季节性赛道"、"Prime Day 窗口" | 峰值月份 + 峰值量 |

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

# 亚马逊商业洞察反向选品 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazon/opportunity/searchByMetrics`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
- **User-Agent**：`LinkFox-Skill/1.0`

## 请求参数

POST Body（JSON）。所有参数均为可选，但**必须至少提供 `keyword` / `nicheName` 或任意一个指标过滤字段**，禁止全部为空。

### 站点与翻页

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| amazonDomain | string | 亚马逊站点代码（闭枚举），当前仅支持 `US`，未指定时默认仅查美国站 | `US` |
| limit | integer | 返回条数上限（1-200），默认 25。无 page 参数，按采集时间倒序返回最近 N 条 | `25` |

### 文本搜索

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| keyword | string | 搜索关键词文本片段（LIKE 模糊匹配） | `whoop band` |
| nicheName | string | 赛道归一化名称片段（LIKE，snake_case 小写），适合赛道时序对比 | `wired_ribbon` |

### 市场规模与增长

| 参数 | 类型 | 说明 |
|------|------|------|
| nicheRevenue360dMinUsdAtLeastGte | number | 360 天市场营收下界（USD）的最小值 |
| nicheRevenue360dMinUsdAtLeastLte | number | 360 天市场营收下界（USD）的最大值 |
| nicheRevenue360dMaxUsdAtLeastGte | number | 360 天市场营收上界（USD）的最小值 |
| nicheRevenue360dMaxUsdAtLeastLte | number | 360 天市场营收上界（USD）的最大值 |
| nichePeakSearchVolumeAtLeastGte | integer | 峰值月搜索量下界（非负整数） |
| nichePeakSearchVolumeAtLeastLte | integer | 峰值月搜索量上界（非负整数） |
| nicheSearchVolumeYoyChangePctAtLeastGte | number | 搜索量同比变化率下限（%，带符号） |
| nicheSearchVolumeYoyChangePctAtLeastLte | number | 搜索量同比变化率上限（%，带符号） |
| nichePeakMonthGte | integer | 搜索峰值月份下限（1-12） |
| nichePeakMonthLte | integer | 搜索峰值月份上限（1-12） |

### 竞争格局（品牌 / 产品集中度）

| 参数 | 类型 | 说明 |
|------|------|------|
| nicheBrandCountGte | integer | 活跃品牌数下限 |
| nicheBrandCountLte | integer | 活跃品牌数上限 |
| nicheBrandCountYoyChangePctAtLeastGte | number | 品牌数同比变化率下限（%，带符号） |
| nicheBrandCountYoyChangePctAtLeastLte | number | 品牌数同比变化率上限（%，带符号） |
| nicheTop5ProductClickSharePctAtLeastGte | number | Top5 产品点击份额下限（0-100） |
| nicheTop5ProductClickSharePctAtLeastLte | number | Top5 产品点击份额上限（0-100） |
| featureTop5BrandSharePctAtLeastGte | number | Top5 品牌合计份额下限（0-100） |
| featureTop5BrandSharePctAtLeastLte | number | Top5 品牌合计份额上限（0-100） |
| featureTopBrandsContains | string | Top3 品牌名片段（原文 LIKE，区分大小写） |

### 价格与档位

| 参数 | 类型 | 说明 |
|------|------|------|
| priceMinUsdGte | number | 赛道最低商品价格下限（USD） |
| priceMinUsdLte | number | 赛道最低商品价格上限（USD） |
| priceMaxUsdGte | number | 赛道最高商品价格下限（USD） |
| priceMaxUsdLte | number | 赛道最高商品价格上限（USD） |
| priceSweetSpotMinUsdGte | number | Sweet Spot 下限的下界（USD） |
| priceSweetSpotMinUsdLte | number | Sweet Spot 下限的上界（USD） |
| priceSweetSpotMaxUsdGte | number | Sweet Spot 上限的下界（USD） |
| priceSweetSpotMaxUsdLte | number | Sweet Spot 上限的上界（USD） |
| priceEntryClickSharePctAtLeastGte | number | 入门档点击份额下限（0-100） |
| priceEntryClickSharePctAtLeastLte | number | 入门档点击份额上限（0-100） |
| priceMidClickSharePctAtLeastGte | number | 中档点击份额下限（0-100） |
| priceMidClickSharePctAtLeastLte | number | 中档点击份额上限（0-100） |
| priceHighClickSharePctAtLeastGte | number | 高端档点击份额下限（0-100） |
| priceHighClickSharePctAtLeastLte | number | 高端档点击份额上限（0-100） |

### 客户画像（年龄 / 性别 / 收入 / 生命阶段）

| 参数 | 类型 | 说明 |
|------|------|------|
| demoPrimaryAgeMinGte | integer | 主人群年龄下界的最小值（0-120 岁） |
| demoPrimaryAgeMinLte | integer | 主人群年龄下界的最大值（0-120 岁） |
| demoPrimaryAgeMaxGte | integer | 主人群年龄上界的最小值（0-120 岁） |
| demoPrimaryAgeMaxLte | integer | 主人群年龄上界的最大值（0-120 岁） |
| demoGenderDominant | string | 性别主导（闭枚举）：`female` / `male` / `mixed` / `unspecified` |
| demoPrimaryIncomeTier | string | 收入档（闭枚举）：`low` / `middle_low` / `middle` / `middle_upper` / `upper_middle` / `high` |
| demoLifeStageTagsContains | string | 生命阶段标签片段（snake_case，LIKE）：`parent`、`student`、`retiree`、`athlete` 等 |

### 产品特征（成熟度 / 趋势 / 差异化 / 搜索形态）

| 参数 | 类型 | 说明 |
|------|------|------|
| featureNewAvgReviewCountAtLeastGte | integer | 新品平均评论量下限（非负整数） |
| featureNewAvgReviewCountAtLeastLte | integer | 新品平均评论量上限（非负整数） |
| featureEstablishedAvgReviewCountAtLeastGte | integer | 成熟老品平均评论量下限（非负整数） |
| featureEstablishedAvgReviewCountAtLeastLte | integer | 成熟老品平均评论量上限（非负整数） |
| featureEmergingTrendTagsContains | string | 新兴趋势特征标签片段（snake_case，LIKE）：`cordless`、`portable`、`smart` 等 |
| featureUncommonFeatureTagsContains | string | 稀有差异化特征标签片段（snake_case，LIKE）：`hema_free`、`medical_grade_silicone` 等 |
| searchTopCategory1Label | string | 搜索流量第一类目标签片段（snake_case，LIKE）：`core_product_terms`、`set_kit_configurations` 等 |

### 评论卖点 / 痛点

| 参数 | 类型 | 说明 |
|------|------|------|
| reviewPositiveTop1Topic | string | 好评 #1 主题片段（snake_case，LIKE）：`comfort`、`quality_overall_generic` 等 |
| reviewPositiveTop1PctAtLeastGte | number | 好评 #1 主题占比下限（0-100，正面评论中占比） |
| reviewPositiveTop1PctAtLeastLte | number | 好评 #1 主题占比上限（0-100） |
| reviewNegativeTop1Topic | string | 差评 #1 主题片段（snake_case，LIKE）：`size`、`quality`、`durability` 等 |
| reviewNegativeTop1PctAtLeastGte | number | 差评 #1 主题占比下限（0-100，负面评论中占比） |
| reviewNegativeTop1PctAtLeastLte | number | 差评 #1 主题占比上限（0-100） |
| reviewNegativeTop2Topic | string | 差评 #2 主题片段（snake_case，LIKE） |
| reviewStrategicInsightTagsContains | string | 评论策略建议标签片段（snake_case，LIKE）：`sizing_clarity`、`material_transparency` 等 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 响应码，`200` 为成功 |
| msg | string | 提示信息，成功为 `ok`，失败为错误描述 |
| data | array | 关键词指标记录数组，每条对应一个 (站点, 关键词) 组合，约 37 个字段，按采集时间倒序 |

`data[]` 主要字段（节选）：

| 字段 | 类型 | 说明 |
|------|------|------|
| amazonDomain | string | 站点代码（当前固定 `US`） |
| keyword | string | 原始搜索关键词 |
| nicheName | string | 赛道归一化名称（snake_case） |
| nicheRevenue360dMinUsdAtLeast / nicheRevenue360dMaxUsdAtLeast | number | 近 360 天市场营收下界 / 上界（USD） |
| nichePeakSearchVolumeAtLeast | integer | 峰值月搜索量 |
| nichePeakMonth | integer | 搜索峰值月份（1-12） |
| nicheSearchVolumeYoyChangePctAtLeast | number | 搜索量同比变化率（%，带符号） |
| nicheBrandCount / nicheBrandCountYoyChangePctAtLeast | integer / number | 活跃品牌数及其同比变化率 |
| nicheTop5ProductClickSharePctAtLeast | number | Top5 产品点击份额（0-100） |
| featureTop5BrandSharePctAtLeast | number | Top5 品牌合计份额（0-100） |
| featureTopBrands | array | Top 3 品牌名列表（原文） |
| priceMinUsd / priceMaxUsd | number | 赛道整体最低 / 最高商品价 |
| priceSweetSpotMinUsd / priceSweetSpotMaxUsd | number | Value Sweet Spot 价格区间下界 / 上界 |
| priceEntryClickSharePctAtLeast / priceMidClickSharePctAtLeast / priceHighClickSharePctAtLeast | number | 入门 / 中 / 高档点击份额（0-100） |
| demoPrimaryAgeMin / demoPrimaryAgeMax | integer | 核心人群年龄下界 / 上界 |
| demoGenderDominant | string | 性别主导（`female` / `male` / `mixed` / `unspecified`） |
| demoPrimaryIncomeTier | string | 核心人群收入档 |
| demoLifeStageTags | array | 生命阶段标签列表 |
| featureNewAvgReviewCountAtLeast / featureEstablishedAvgReviewCountAtLeast | integer | 新品 / 成熟老品平均评论量 |
| featureEmergingTrendTags / featureUncommonFeatureTags | array | 新兴趋势 / 稀有差异化特征标签 |
| searchTopCategory1Label | string | 流量第一类目归一化标签 |
| reviewPositiveTop1Topic / reviewPositiveTop1PctAtLeast | string / number | 好评 #1 主题及在正面评论中的占比 |
| reviewNegativeTop1Topic / reviewNegativeTop1PctAtLeast / reviewNegativeTop2Topic | string / number / string | 差评 #1 主题、占比及次因 |
| reviewStrategicInsightTags | array | 评论策略建议标签 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 `code` 字段区分；未授权时 HTTP 状态码为 401。

| 错误码 | 含义 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | 正常解析 `data` 数组并展示给用户 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非 200 值 | 业务异常 | 参考 `msg` 字段获取具体错误原因，常见为参数全空或参数取值非法 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

按品牌密度低 + 同比高增长筛选新人友好赛道：

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/opportunity/searchByMetrics \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/1.0" \
  -d '{
    "nicheBrandCountLte": 20,
    "nicheSearchVolumeYoyChangePctAtLeastGte": 100,
    "featureNewAvgReviewCountAtLeastLte": 500,
    "limit": 25
  }'
```

按关键词反向追溯赛道历史：

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/opportunity/searchByMetrics \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/1.0" \
  -d '{"keyword": "whoop band", "limit": 50}'
```

按差评痛点 + 中档稀缺锁定切入机会：

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/opportunity/searchByMetrics \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/1.0" \
  -d '{
    "reviewNegativeTop1Topic": "size",
    "reviewNegativeTop1PctAtLeastGte": 70,
    "priceMidClickSharePctAtLeastLte": 5,
    "priceEntryClickSharePctAtLeastGte": 70
  }'
```
