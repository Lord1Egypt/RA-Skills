---
name: linkfox-junglescout-keyword-by-asin
description: 利用Jungle Scout根据ASIN反查亚马逊关键词，获取竞品的流量词、搜索量、竞争度及PPC竞价数据，支持批量查询。
---

# Jungle Scout — 根据 ASIN 反查关键词

本技能通过 Jungle Scout 数据源查询与给定 ASIN 关联的关键词，返回搜索量、竞争度、PPC 竞价、排名位置及相关度等指标，覆盖 10 个亚马逊站点，单次最多 10 个 ASIN。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 输入竞品或目标 ASIN，反查这些 ASIN 在亚马逊搜索结果中出现的所有关键词及详细指标。
- 竞品关键词分析：查看竞品在哪些关键词下获得自然/广告排名。
- 关键词拓展：从已知 ASIN 反向挖掘高潜力关键词。
- 广告投放参考：获取关键词的 PPC 出价（精确/广泛匹配）与 SP 品牌广告出价。
- 竞争格局评估：通过 Ease of Ranking Score 和竞品排名数据判断关键词竞争难度。
- 流量结构解析：了解 ASIN 的流量来源关键词及其搜索量与排名。

### ❌ 边界与限制

- **ASIN 数量上限**：单次查询最多 10 个 ASIN，须为标准 10 位亚马逊 ASIN（以 B0 开头）。
- **必填参数**：`marketplace` 和 `asins` 缺一不可；未指定站点时默认 `us`。
- **数据时效**：数据定期更新，`updatedAt` 字段标注最后更新时间；排名非实时数据。
- **搜索量类型**：同时提供精确匹配与广泛匹配两种搜索量。
- **不在范围内**：关键词历史搜索量趋势（需关键词历史搜索量工具）；ABA 搜索词排名（需 ABA 工具）；商品销量估算、listing 优化建议；关键词广告投放执行（仅提供竞价参考数据）；非亚马逊平台的关键词数据。

## 核心概念

Jungle Scout ASIN 反查关键词工具通过输入竞品或目标 ASIN，获取这些 ASIN 在亚马逊搜索结果中出现的所有关键词及详细指标。每条记录代表一个关键词，包含搜索量、趋势、排名、竞价、竞争度等完整指标。

**支持站点**：`us`（美国）、`uk`（英国）、`de`（德国）、`in`（印度）、`ca`（加拿大）、`fr`（法国）、`it`（意大利）、`es`（西班牙）、`mx`（墨西哥）、`jp`（日本）。未指定时默认 `us`。

## 调用方式

- **API 端点**：`POST /tool-jungle-scout/keywords/by-asin`（完整参数/响应/错误码见 [references/api.md](references/api.md)）
- **Python 脚本**：`python scripts/junglescout_keyword_by_asin.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**构建查询要点**：
1. **站点映射**：用户说"美国站"→ `us`，"日本站"→ `jp`，"德国站"→ `de`；未指定时默认 `us`。
2. **ASIN 格式**：标准 10 位亚马逊 ASIN（以 B0 开头），数组传入，最多 10 个。
3. **搜索量筛选**："搜索量大于1万"→ `minMonthlySearchVolumeExact: 10000`；"搜索量1000到5000"→ `min: 1000, max: 5000`。
4. **排序选择**：默认按精确搜索量降序（`-monthly_search_volume_exact`）；"按相关度排序"→ `sort: -relevancy_score`。
5. **结果数量**："给我前50个"→ `needCount: 50`；未指定时可设 30-100。
6. **变体包含**：关注变体流量时设 `includeVariants: true`。

**输出策略（脚本默认行为）**：
- 始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-junglescout-keyword-by-asin-<timestamp>.json`（`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout。
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段长度 + 前 3 条样本）。
- 加 `--inline` 强制全量打印到 stdout（同样落盘）。

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 查看竞品 ASIN 的核心流量词**
```json
{
  "marketplace": "us",
  "asins": ["B0XXXXXXXX"],
  "needCount": 50,
  "sort": "-monthly_search_volume_exact"
}
```

**2. 多个 ASIN 的共同关键词（竞品对比）**
```json
{
  "marketplace": "us",
  "asins": ["B0XXXXXXXX", "B0YYYYYYYY", "B0ZZZZZZZZ"],
  "needCount": 100,
  "sort": "-relevancy_score"
}
```

**3. 筛选高搜索量低竞争关键词**
```json
{
  "marketplace": "us",
  "asins": ["B0XXXXXXXX"],
  "minMonthlySearchVolumeExact": 5000,
  "maxOrganicProductCount": 500,
  "needCount": 50,
  "sort": "-ease_of_ranking_score"
}
```

**4. 查找长尾关键词（多词组合）**
```json
{
  "marketplace": "us",
  "asins": ["B0XXXXXXXX"],
  "minWordCount": 3,
  "minMonthlySearchVolumeExact": 500,
  "needCount": 80,
  "sort": "-monthly_search_volume_exact"
}
```

**5. 日本站竞品广告关键词分析**
```json
{
  "marketplace": "jp",
  "asins": ["B0XXXXXXXX"],
  "needCount": 50,
  "sort": "-ppc_bid_exact"
}
```

**6. 包含变体的全量关键词挖掘**
```json
{
  "marketplace": "de",
  "asins": ["B0XXXXXXXX"],
  "includeVariants": true,
  "needCount": 200,
  "sort": "-monthly_search_volume_exact"
}
```

## 展示规则

1. **表格展示为主**：以表格形式展示关键词列表，核心列包括：关键词、精确搜索量、自然排名、广告排名、相关度、PPC 出价。
2. **按需精简列**：根据用户意图选择展示列。竞品分析侧重排名和搜索量；广告分析侧重 PPC 出价和广告排名。
3. **排名高亮**：对自然排名前 10 和广告排名前 5 的关键词做标注，帮助用户快速识别核心流量词。
4. **趋势标注**：月/季度趋势为正时标注增长，为负时标注下降。
5. **竞品对比**：当输入多个 ASIN 时，展示各 ASIN 在关键词下的排名对比。
6. **错误处理**：查询失败时根据错误响应说明原因，并建议调整参数。只呈现数据，不做主观商业建议。

## 用户表达与场景速查

**适用** —— 通过 ASIN 反查和拓展关键词：

| 用户说 | 场景 |
|--------|------|
| "这个ASIN有哪些流量词" | 单个 ASIN 关键词反查 |
| "竞品用了哪些关键词" | 竞品关键词分析 |
| "帮我对比这几个ASIN的关键词" | 多 ASIN 关键词对比 |
| "这个产品搜什么词能搜到" | ASIN 反向搜索词查询 |
| "找一些搜索量大竞争小的词" | 高搜索量低竞争关键词筛选 |
| "这个ASIN的广告词有哪些" | ASIN 广告关键词分析 |
| "帮我拓展一下关键词" | 基于 ASIN 的关键词拓展 |

不适用场景见上方【能力边界】。边界判断：当用户提供具体 ASIN 并想知道这些 ASIN 在哪些关键词下有排名时适用本技能；若想按文本搜索关键词或查看历史搜索量趋势，应使用其他技能。

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

# Jungle Scout 根据 ASIN 反查关键词 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/tool-jungle-scout/keywords/by-asin`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

### 必填参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| marketplace | string | 是 | 目标市场代码。可选值：`us`、`uk`、`de`、`in`、`ca`、`fr`、`it`、`es`、`mx`、`jp` |
| asins | array\<string\> | 是 | ASIN 列表，最多 10 个 |

### 可选参数 — 结果控制

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| needCount | int | 否 | 返回的结果总数（内部自动分页） |
| includeVariants | boolean | 否 | 是否包含变体商品的关键词 |
| sort | string | 否 | 排序字段，默认 `-monthly_search_volume_exact`（精确搜索量降序）。可选值见下方排序字段表 |

### 可选参数 — 搜索量筛选

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minMonthlySearchVolumeExact | int | 否 | 最小月精确搜索量（1-999999） |
| maxMonthlySearchVolumeExact | int | 否 | 最大月精确搜索量（1-999999） |
| minMonthlySearchVolumeBroad | int | 否 | 最小月广泛搜索量（1-999999） |
| maxMonthlySearchVolumeBroad | int | 否 | 最大月广泛搜索量（1-999999） |

### 可选参数 — 关键词特征筛选

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minWordCount | int | 否 | 最小单词数（1-99999） |
| maxWordCount | int | 否 | 最大单词数（1-99999） |
| minOrganicProductCount | int | 否 | 最小自然搜索结果数（1-99999） |
| maxOrganicProductCount | int | 否 | 最大自然搜索结果数（1-99999） |

### 排序字段

| sort 值 | 说明 |
|---------|------|
| name / -name | 关键词名称 升序/降序 |
| dominant_category / -dominant_category | 主类目 升序/降序 |
| monthly_trend / -monthly_trend | 月趋势 升序/降序 |
| quarterly_trend / -quarterly_trend | 季度趋势 升序/降序 |
| monthly_search_volume_exact / -monthly_search_volume_exact | 精确搜索量 升序/降序（默认降序） |
| monthly_search_volume_broad / -monthly_search_volume_broad | 广泛搜索量 升序/降序 |
| recommended_promotions / -recommended_promotions | 推荐促销 升序/降序 |
| sp_brand_ad_bid / -sp_brand_ad_bid | SP品牌广告出价 升序/降序 |
| ppc_bid_broad / -ppc_bid_broad | PPC广泛出价 升序/降序 |
| ppc_bid_exact / -ppc_bid_exact | PPC精确出价 升序/降序 |
| ease_of_ranking_score / -ease_of_ranking_score | 排名难度分 升序/降序 |
| relevancy_score / -relevancy_score | 相关度分 升序/降序 |
| organic_product_count / -organic_product_count | 自然结果数 升序/降序 |

### 站点映射

| 站点 | marketplace 值 |
|------|---------------|
| 美国 | us |
| 英国 | uk |
| 德国 | de |
| 印度 | in |
| 加拿大 | ca |
| 法国 | fr |
| 意大利 | it |
| 西班牙 | es |
| 墨西哥 | mx |
| 日本 | jp |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| costToken | integer | 消耗 token 数 |
| keywordInfoList | array | 关键词信息列表 |

### keywordInfoList 数组中每个对象

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 关键词 |
| country | string | 市场代码 |
| monthlySearchVolumeExact | integer | 月精确匹配搜索量 |
| monthlySearchVolumeBroad | integer | 月广泛匹配搜索量 |
| monthlyTrend | float | 月环比趋势（%） |
| quarterlyTrend | float | 季度趋势（%） |
| dominantCategory | string | 主要类目 |
| relevancyScore | integer | 关键词与 ASIN 的相关度（0-100） |
| easeOfRankingScore | integer | 排名容易程度（0-100，越高越容易排名） |
| organicRank | integer | ASIN 的自然搜索排名 |
| sponsoredRank | integer | ASIN 的广告排名 |
| overallRank | integer | 综合排名位置 |
| organicProductCount | integer | 自然搜索结果中的商品总数 |
| sponsoredProductCount | integer | 广告位商品总数 |
| ppcBidExact | float | 精确匹配 PPC 建议出价（USD） |
| ppcBidBroad | float | 广泛匹配 PPC 建议出价（USD） |
| spBrandAdBid | float | SP 品牌广告建议出价（USD） |
| recommendedPromotions | integer | 推荐促销量 |
| primaryAsin | string | 该关键词下排名最高的 ASIN |
| relativeOrganicPosition | float | 查询 ASIN 的自然排名相对位置 |
| relativeSponsoredPosition | float | 查询 ASIN 的广告排名相对位置 |
| organicRankingAsinsCount | integer | 有自然排名的查询 ASIN 数量 |
| sponsoredRankingAsinsCount | integer | 有广告排名的查询 ASIN 数量 |
| avgCompetitorOrganicRank | float | 查询 ASIN 的平均自然排名 |
| avgCompetitorSponsoredRank | float | 查询 ASIN 的平均广告排名 |
| variationLowestOrganicRank | integer | 变体中最佳自然排名 |
| variationLowestSponsoredRank | integer | 变体中最佳广告排名 |
| competitorOrganicRank | array | 各 ASIN 的自然排名，元素为 `{asin, organicRank}` |
| competitorSponsoredRank | array | 各 ASIN 的广告排名，元素为 `{asin, sponsoredRank}` |
| updatedAt | string | 数据最后更新时间 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `keywordInfoList` |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
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
curl -X POST https://tool-gateway.linkfox.com/tool-jungle-scout/keywords/by-asin \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "asins": ["B0DXXXXXXX"], "needCount": 50, "sort": "-monthly_search_volume_exact"}'
```

## 响应示例

```json
{
  "costToken": 10,
  "keywordInfoList": [
    {
      "name": "yoga mat",
      "country": "us",
      "monthlySearchVolumeExact": 85420,
      "monthlySearchVolumeBroad": 125000,
      "monthlyTrend": 12.5,
      "quarterlyTrend": 8.3,
      "dominantCategory": "Sports & Outdoors",
      "relevancyScore": 95,
      "easeOfRankingScore": 42,
      "organicRank": 5,
      "sponsoredRank": 3,
      "overallRank": 4,
      "organicProductCount": 2000,
      "sponsoredProductCount": 48,
      "ppcBidExact": 1.25,
      "ppcBidBroad": 0.95,
      "spBrandAdBid": 2.10,
      "recommendedPromotions": 5,
      "primaryAsin": "B0DXXXXXXX",
      "relativeOrganicPosition": 0.12,
      "relativeSponsoredPosition": 0.08,
      "organicRankingAsinsCount": 1,
      "sponsoredRankingAsinsCount": 1,
      "avgCompetitorOrganicRank": 5.0,
      "avgCompetitorSponsoredRank": 3.0,
      "variationLowestOrganicRank": 3,
      "variationLowestSponsoredRank": 2,
      "competitorOrganicRank": [{"asin": "B0DXXXXXXX", "organicRank": 5}],
      "competitorSponsoredRank": [{"asin": "B0DXXXXXXX", "sponsoredRank": 3}],
      "updatedAt": "2026-04-10"
    }
  ]
}
```
