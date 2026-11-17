---
name: linkfox-junglescout-keyword-by-keyword
description: 利用Jungle Scout通过种子关键词拓展相关长尾词，提供搜索量、趋势、排名难度和PPC竞价等核心指标。
---

# Jungle Scout — 根据关键词扩展关键词信息（Keyword by Keyword）

本技能从一个种子关键词出发，通过 Jungle Scout 数据源扩展出大量相关关键词及其竞争指标。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 从单个种子关键词扩展出相关关键词列表，包含搜索量、趋势、PPC 竞价、排名难度等指标。
- 覆盖美国、英国、德国、印度、加拿大、法国、意大利、西班牙、墨西哥、日本共 10 个亚马逊站点。
- 支持长尾词挖掘（按词数筛选）、低竞争关键词发现、高搜索量词筛选、PPC 竞价研究等场景。
- 支持按搜索量、趋势、出价、排名难度、相关性等多字段排序与区间筛选。

### ❌ 边界与限制

- **单次单关键词**：`searchTerms` 仅接受一个种子关键词，多关键词需拆分多次调用。
- **数据周期**：搜索量为月均估算值，非实时数据。
- **站点限制**：仅覆盖 10 个亚马逊站点，不含澳大利亚、荷兰等。
- **排序字段固定**：仅支持预定义的排序字段，不支持自定义组合排序。
- **不在范围内**：关键词历史搜索量趋势（用 keyword-history 工具）；ABA 搜索词排名（用 ABA 工具）；商品搜索或 listing 分析；ASIN 反查关键词；非亚马逊平台的关键词数据。

## 核心概念

Jungle Scout Keyword by Keyword 工具从一个**种子关键词**出发，挖掘与之相关的大量关键词及其竞争指标。主要应用场景包括：

- **关键词拓展/发现**：输入核心词，获取数百个相关关键词，扩充 listing 关键词库。
- **长尾词挖掘**：通过 `minWordCount` 筛选 3+ 词的长尾关键词，发现低竞争高转化机会。
- **PPC 竞价研究**：查看精确/广泛匹配 PPC 出价和品牌广告出价，规划广告预算。
- **竞争度评估**：通过 `easeOfRankingScore` 和 `organicProductCount` 判断关键词排名难度。
- **趋势分析**：查看月度趋势和季度趋势百分比变化，识别增长型关键词。

## 调用方式

- **API 端点**：`POST /tool-jungle-scout/keywords/by-keyword`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/junglescout_keyword_by_keyword.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-junglescout-keyword-by-keyword-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

必填参数：`marketplace`、`searchTerms`（单个种子关键词字符串）。

**1. 扩展种子关键词 — 获取相关关键词列表**
```json
{
  "marketplace": "us",
  "searchTerms": "yoga mat"
}
```

**2. 挖掘长尾关键词（3+ 词）**
```json
{
  "marketplace": "us",
  "searchTerms": "yoga mat",
  "minWordCount": 3,
  "needCount": 50
}
```

**3. 低竞争关键词发现**
```json
{
  "marketplace": "us",
  "searchTerms": "yoga mat",
  "maxOrganicProductCount": 200,
  "minMonthlySearchVolumeExact": 1000,
  "sort": "-ease_of_ranking_score"
}
```

**4. 高搜索量关键词筛选**
```json
{
  "marketplace": "us",
  "searchTerms": "yoga mat",
  "minMonthlySearchVolumeExact": 10000,
  "sort": "-monthly_search_volume_exact",
  "needCount": 30
}
```

**5. PPC 竞价研究 — 按广泛出价排序**
```json
{
  "marketplace": "us",
  "searchTerms": "yoga mat",
  "minMonthlySearchVolumeExact": 500,
  "sort": "ppc_bid_broad",
  "needCount": 30
}
```

**6. 德国站广泛搜索量关键词**
```json
{
  "marketplace": "de",
  "searchTerms": "yogamatte",
  "minMonthlySearchVolumeBroad": 5000,
  "sort": "-monthly_search_volume_broad"
}
```

## 展示规则

1. **表格优先**：以表格展示关键词列表，核心列包括：关键词、精确搜索量、广泛搜索量、月度趋势、PPC 精确出价、排名难度。
2. **按需裁剪列**：根据用户意图决定展示列——PPC 研究场景侧重出价列，拓词场景侧重搜索量和趋势。
3. **趋势标注**：月度趋势和季度趋势为正值标注上升↑，负值标注下降↓。
4. **排名难度解读**：`easeOfRankingScore` 1-3 为困难，4-6 为中等，7-10 为容易。
5. **数据洞察**：在表格后提供简要总结，如高搜索量词集中在哪个类目、长尾词的竞争优势等。仅呈现数据，不做主观商业建议。
6. **错误处理**：查询失败时根据错误响应说明原因，并建议调整参数。

## 用户表达与场景速查

**适用** —— 关键词拓展与竞争分析：

| 用户说 | 场景 |
|--------|------|
| "帮我拓展这个关键词" | 种子词扩展 |
| "这个词有哪些相关关键词" | 相关词挖掘 |
| "找一些长尾词" | 长尾关键词筛选（minWordCount ≥ 3） |
| "竞争度低的词有哪些" | 低竞争关键词（排名难度 + 商品数量筛选） |
| "这个词的 PPC 出价多少" | PPC 竞价数据查询 |
| "搜索量大的相关词" | 高搜索量关键词筛选 |
| "德国站有什么相关词" | 非美国站关键词拓展 |
| "帮我做关键词调研" | 综合关键词研究 |

不适用场景见上方【能力边界】。

**边界判断**：当用户说"关键词""拓词""关键词研究"时，若需求是从种子关键词扩展出带指标的相关关键词列表，则适用本技能；若想查看单个关键词的历史搜索量随时间变化的趋势，请改用 keyword-history 技能。

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

# Jungle Scout 根据关键词扩展关键词信息 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/tool-jungle-scout/keywords/by-keyword`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

### 必填参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| marketplace | string | 是 | 目标市场代码。可选值：`us`、`uk`、`de`、`in`、`ca`、`fr`、`it`、`es`、`mx`、`jp`。默认 `us` |
| searchTerms | string | 是 | 种子关键词（单个关键词字符串） |

### 可选参数 — 结果控制

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| needCount | int | 否 | 返回结果总数 |
| sort | string | 否 | 排序字段，默认 `-monthly_search_volume_exact`（精确搜索量降序） |

### 可选参数 — 搜索量筛选

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minMonthlySearchVolumeExact | int | 否 | 精确搜索量下限 |
| maxMonthlySearchVolumeExact | int | 否 | 精确搜索量上限 |
| minMonthlySearchVolumeBroad | int | 否 | 广泛搜索量下限 |
| maxMonthlySearchVolumeBroad | int | 否 | 广泛搜索量上限 |

### 可选参数 — 其他筛选

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minWordCount | int | 否 | 关键词最少词数（用于筛选长尾词） |
| maxWordCount | int | 否 | 关键词最多词数 |
| minOrganicProductCount | int | 否 | 自然排名商品数下限 |
| maxOrganicProductCount | int | 否 | 自然排名商品数上限 |

### sort 可选值

| 值 | 说明 |
|----|------|
| name / -name | 关键词名称 升序/降序 |
| dominant_category / -dominant_category | 主类目 升序/降序 |
| monthly_trend / -monthly_trend | 月度趋势 升序/降序 |
| quarterly_trend / -quarterly_trend | 季度趋势 升序/降序 |
| monthly_search_volume_exact / -monthly_search_volume_exact | 精确搜索量 升序/降序（默认降序） |
| monthly_search_volume_broad / -monthly_search_volume_broad | 广泛搜索量 升序/降序 |
| recommended_promotions / -recommended_promotions | 推荐促销 升序/降序 |
| sp_brand_ad_bid / -sp_brand_ad_bid | 品牌广告出价 升序/降序 |
| ppc_bid_broad / -ppc_bid_broad | PPC广泛出价 升序/降序 |
| ppc_bid_exact / -ppc_bid_exact | PPC精确出价 升序/降序 |
| ease_of_ranking_score / -ease_of_ranking_score | 排名难度 升序/降序 |
| relevancy_score / -relevancy_score | 相关性评分 升序/降序 |
| organic_product_count / -organic_product_count | 自然商品数 升序/降序 |

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
| name | string | 关键词名称 |
| country | string | 市场代码 |
| monthlySearchVolumeExact | integer | 月均精确匹配搜索量 |
| monthlySearchVolumeBroad | integer | 月均广泛匹配搜索量 |
| monthlyTrend | number | 月度搜索量变化百分比 |
| quarterlyTrend | number | 季度搜索量变化百分比 |
| dominantCategory | string | 搜索结果中占比最高的品类 |
| relevancyScore | integer | 与种子词的相关性评分 |
| easeOfRankingScore | integer | 排名容易度评分（越高越容易排名） |
| organicProductCount | integer | 自然排名商品数量 |
| sponsoredProductCount | integer | 广告商品数量 |
| ppcBidExact | number | 精确匹配 PPC 建议出价（美元） |
| ppcBidBroad | number | 广泛匹配 PPC 建议出价（美元） |
| spBrandAdBid | number | Sponsored Brand 广告建议出价（美元） |
| recommendedPromotions | integer | 推荐促销赠品数量 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `keywordInfoList` |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | 积分/余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
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
curl -X POST https://tool-gateway.linkfox.com/tool-jungle-scout/keywords/by-keyword \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "searchTerms": "yoga mat", "needCount": 20}'
```

## 响应示例

```json
{
  "costToken": 1,
  "keywordInfoList": [
    {
      "name": "yoga mat thick",
      "country": "us",
      "monthlySearchVolumeExact": 45000,
      "monthlySearchVolumeBroad": 120000,
      "monthlyTrend": 15.3,
      "quarterlyTrend": -5.2,
      "dominantCategory": "Sports & Outdoors",
      "relevancyScore": 856,
      "easeOfRankingScore": 3,
      "organicProductCount": 342,
      "sponsoredProductCount": 28,
      "ppcBidExact": 1.25,
      "ppcBidBroad": 0.89,
      "spBrandAdBid": 2.50,
      "recommendedPromotions": 150
    },
    {
      "name": "yoga mat non slip",
      "country": "us",
      "monthlySearchVolumeExact": 38000,
      "monthlySearchVolumeBroad": 95000,
      "monthlyTrend": 8.1,
      "quarterlyTrend": 12.4,
      "dominantCategory": "Sports & Outdoors",
      "relevancyScore": 920,
      "easeOfRankingScore": 2,
      "organicProductCount": 510,
      "sponsoredProductCount": 35,
      "ppcBidExact": 1.58,
      "ppcBidBroad": 1.12,
      "spBrandAdBid": 3.10,
      "recommendedPromotions": 200
    }
  ]
}
```
