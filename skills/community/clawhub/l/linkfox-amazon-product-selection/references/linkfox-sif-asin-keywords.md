---
name: linkfox-sif-asin-keywords
description: 利用SIF数据反查亚马逊ASIN的流量词排名、搜索量、点击集中度及周/月时间窗表现。
---

# SIF-ASIN关键词分析（SIF ASIN Keyword Analysis）

本技能用于反查特定亚马逊 ASIN 的流量关键词，帮助卖家了解哪些关键词为产品带来流量以及产品在各关键词下的排名表现。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 反查单个亚马逊 ASIN 的流量关键词，查看每个关键词下的自然排名、SP 广告排名、周搜索量、流量占比等。
- 提供自然/付费流量得分、ABA TOP3 点击集中度、点击到购买转化率、搜索量同比涨跌等指标。
- 支持按关键词文本筛选、按多种条件过滤（自然词/广告词/出单词/转化流失词/新进词等）、按排名或搜索量排序。
- 支持最近 N 天、指定月、指定周三种时间窗，覆盖 13 个亚马逊站点。

### ❌ 边界与限制

- **单 ASIN 限制**：每次请求只能查询一个 ASIN；对比多个 ASIN 需分别调用。
- **分页上限**：单页最多 100 条，需翻页获取更多。
- **时间窗粒度**：`timePieceType=latelyDay` 仅支持 `timePieceValue=7` 或 `30`，不支持任意 N 天。
- **站点覆盖**：仅 13 个站点（US/UK/DE/CA/JP/FR/ES/IT/MX/AU/AE/BR/SA），IN/NL/SE/PL/TR/SG 已不可用；未指定站点时默认 US。
- **关键词语言**：`keyword` 筛选词尽量使用目标站点语言。
- **排名口径**：排名数值越小表示位置越靠前；"排名提升"指数值减小，"排名下降"指数值增大。
- **不在范围内**：不针对特定 ASIN 的广泛关键词调研（用 ABA 工具）；商品评论、Listing 文案；销量/收入估算；广告投放管理（出价、预算）；不带具体 ASIN 的品类级关键词趋势。

## 核心概念

SIF ASIN 关键词数据揭示为特定亚马逊商品（ASIN）带来流量的关键词。对每个关键词可查看商品的自然搜索排名、SP 广告排名、搜索量、流量占比、展示位置类型及各类表现标记，是 ASIN 反查关键词的首选工具。

**站点**：支持 13 个站点（US/UK/DE/CA/JP/FR/ES/IT/MX/AU/AE/BR/SA），默认 US；用户未指定站点时使用 US，站点码超出列表会被 API 拒绝。

**排名逻辑**：排名数值越小表示位置越靠前，排名 1 表示排在搜索结果首位。

## 调用方式

- **API 端点**：`POST /sif/asinKeywords`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sif_asin_keywords.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sif-asin-keywords-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 查询某 ASIN 在 US 站点的全部流量关键词**
```
asin: "B0XXXXXXXX", country: "US"
```

**2. 仅查询自然流量关键词**
```
asin: "B0XXXXXXXX", country: "US", conditions: "nfPosition"
```

**3. 查询包含 "charger" 的关键词并按搜索量升序排序**
```
asin: "B0XXXXXXXX", country: "US", keyword: "charger", sortBy: "estSearchesNum", desc: false
```

**4. 查询高转化关键词**
```
asin: "B0XXXXXXXX", country: "US", conditions: "isPurchaseKw,isQualityKw"
```

**5. 查询日本站点的 SP 广告关键词**
```
asin: "B0XXXXXXXX", country: "JP", conditions: "isSpAd", sortBy: "adLastRank", desc: false
```

**6. 查询稳定转化的精准长尾关键词**
```
asin: "B0XXXXXXXX", country: "US", conditions: "isAccurateTailKw,isStableKw"
```

**7. 查询 2026 年 4 月新进入的 SP 流量关键词**
```
asin: "B0XXXXXXXX", country: "US", timePieceType: "month", timePieceValue: "2026-04", conditions: "spKeywordCnt.in"
```

**8. 查询搜索量同比上升的关键词**
```
asin: "B0XXXXXXXX", country: "US", conditions: "isSearchVolUpKw", sortBy: "estSearchesNum", desc: true
```

## 展示规则

1. **只呈现数据**：以清晰表格展示查询结果，不做主观商业建议。
2. **排名说明**：展示排名数据时提醒用户，数值越小表示位置越靠前。
3. **占比格式**：`trafficShare`、`naturalTrafficShare`、`paidTrafficShare`、`clickConcentrationShare` 按百分比展示（乘以 100），如 0.05 显示为 5%。
4. **点击集中度措辞**：`clickConcentrationShare` 衡量该关键词下点击是否集中在头部 ASIN，**不是转化率**，需清晰标注以免与 `clickToPurchaseConversionRate` 混淆。
5. **周期标注**：展示来自 `*.in`/`*.total` 过滤的计数或对比数据时，标注周期范围——默认最近 7 天；若设置了 `timePieceType=month` 或 `week`，展示解析后的周期（`periodEndDate` / `abaCreateDateWeek`）。
6. **标记翻译**：将标记数组翻译为可读标签，如 `["isMainKw", "isAccurateKw"]` 显示为"主要流量词、精准流量词"。
7. **展示位置翻译**：将展示位置类型数组翻译为可读标签：natural=自然搜索位、ac=Amazon's Choice、sp=SP 广告位、top=顶部品牌广告、bottom=底部品牌广告、er=编辑推荐、vedio=视频广告、tr=Top Rated、trfob=Top Rated Frequently Bought。
8. **分页提示**：结果有更多页时，告知总数并建议获取后续页。
9. **错误处理**：查询失败时根据 `msg` 字段说明原因并建议调整查询参数。
10. **多 ASIN 请求**：用户询问多个 ASIN 时，为每个 ASIN 分别调用并一起呈现结果。

## 用户表达与场景速查

**适用** —— 针对特定亚马逊商品的关键词分析：

| 用户说 | 场景 |
|--------|------|
| "这个 ASIN 排在哪些关键词下" | ASIN 反查关键词 |
| "看看 B0XXX 的流量关键词" | 流量关键词分析 |
| "这个产品的自然排名是多少" | 自然排名查询 |
| "这个产品在哪些关键词上投了广告" | 广告关键词分析 |
| "找这个 ASIN 的高转化关键词" | 转化关键词挖掘 |
| "这个产品的主要流量来源是什么" | 主要流量词识别 |
| "看看哪些关键词转化流失了" | 转化流失诊断 |
| "哪些关键词带 Amazon's Choice 标" | AC 关键词发现 |
| "对比我 ASIN 的关键词排名" | 关键词排名分析 |
| "这个 ASIN 上月新增了哪些 SP 关键词" | 新进周期关键词发现（`spKeywordCnt.in` + 月窗） |
| "哪些关键词搜索量同比上升" | 搜索量趋势筛选（`isSearchVolUpKw`） |
| "这个关键词点击集中度高吗" | ABA TOP3 点击集中度读取 |
| "关键词的点击到购买转化率" | 单关键词转化查询 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题
发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# SIF-ASIN的关键词 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/sif/asinKeywords`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| asin | string | 是 | ASIN码，最大长度1000字符。本工具一次只能查询一个ASIN |
| country | string | 否 | 国家站点，默认 `US`。可选值（共 13 个）：`US`、`UK`、`DE`、`CA`、`JP`、`FR`、`ES`、`IT`、`MX`、`AU`、`AE`、`BR`、`SA` |
| keyword | string | 否 | 关键词，最大长度1000。尽量翻译成对应国家站点的语言 |
| timePieceType | string | 否 | 时间片段类型，默认 `latelyDay`。可选值：`latelyDay`（最近N天）、`month`（某月）、`week`（某周） |
| timePieceValue | string | 否 | 时间片段值，默认 `7`，最大长度1000。`latelyDay` 时仅支持 `7` 或 `30`；`month` 时为 `YYYY-MM`（如 `2026-04`）；`week` 时为周开始日期 `YYYY-MM-DD`（如 `2026-04-13`） |
| conditions | string | 否 | 条件筛选，多个以英文逗号隔开。可选值：<br>**标志类**：`nfPosition`（自然流量词）、`isSpAd`（SP广告词）、`isBrandAd`（品牌广告词）、`isVedioAd`（视频广告词）、`isAC`（AC推荐词）、`isAccurateKw`（精准流量词）、`isAccurateTailKw`（精准长尾词）、`isPurchaseKw`（出单词）、`isQualityKw`（转化优质词）、`isStableKw`（转化平稳词）、`isLossKw`（转化流失词）、`isInvalidKw`（无效曝光词）、`isMultiVariantKw`（多变体自然位词）、`isSearchVolUpKw`（搜索量同比增长词）、`isSearchVolDownKw`（搜索量同比下降词）<br>**周期计数类（`.total` 全量 / `.in` 新进）**：`totalPeriod.in`、`nfKeywordCnt.total`、`nfKeywordCnt.in`、`adKeywordCnt.total`、`adKeywordCnt.in`、`allSpKeywordCnt.total`、`allSpKeywordCnt.in`、`spKeywordCnt.total`、`spKeywordCnt.in`、`recSpKeywordCnt.total`、`recSpKeywordCnt.in`、`allSbKeywordCnt.total`、`allSbKeywordCnt.in`、`sbKeywordCnt.total`、`sbKeywordCnt.in`、`sbvKeywordCnt.total`、`sbvKeywordCnt.in` |
| sortBy | string | 否 | 排序字段。可选值：`lastRank`（自然排名）、`adLastRank`（广告排名）、`updateTime`（关键词抓取时间）、`searchesRank`（搜索排名）、`estSearchesNum`（月搜索量）。空字符串为默认系统排序 |
| desc | boolean | 否 | 是否降序，默认 `true` |
| pageNum | integer | 否 | 页码，默认 `1` |
| pageSize | integer | 否 | 每页数量，最小10，最大100，默认 `100` |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 返回码 |
| msg | string | 消息 |
| total | integer | 本次实际返回的数据数量 |
| data | array | 返回数据数组（详见下方） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| title | string | 标题 |
| isParentAsin | boolean | 是否是父体（pasin） |
| hasVaiants | boolean | 是否有变体 |
| abaCreateDateWeek | string | 最新周 ABA 数据对应的周时间 |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗token |

### data 数组元素字段

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | string | 关键词 |
| translateKeyword | string | 关键词翻译，站点本地化译文 |
| asin | string | 商品ASIN |
| productNaturalRank | integer | 商品自然搜索排名。该商品在此关键词下的自然搜索结果中的位置排名，如1表示排在搜索结果第1位（首位） |
| naturalRankDisplay | string | 自然排名显示文本。自然搜索排名的字符串表示形式 |
| productAdRank | integer | 商品SP广告排名。该商品在此关键词下的Sponsored Products广告位中的排名位置，如3表示排在广告位第3位 |
| adRankDisplay | string | 广告排名显示文本。SP广告排名的字符串表示形式 |
| weeklySearchVolume | integer | 周搜索量。该关键词在亚马逊平台每周的预估搜索次数 |
| keywordPopularityRank | integer | 关键词搜索热度排名。该关键词的月搜索量在亚马逊所有关键词中的排名，数值越小表示搜索量越大 |
| totalSearchResultProductCount | integer | 该关键词下搜索结果商品总数（在售产品数） |
| trafficShare | number | 流量占比。该关键词为商品带来的流量占所有关键词总流量的比例，其中1表示100% |
| naturalTrafficShare | number | 自然流量得分占比。自然搜索流量得分 / 总得分 |
| paidTrafficShare | number | 付费广告流量得分占比。广告流量得分 / 总得分；广告合计 = sp + sb + sbv + recAd |
| naturalTrafficScore | number | 自然流量得分。该关键词为该 ASIN 带来的自然搜索曝光得分，0 = 无自然流量曝光 |
| sponsoredProductsScore | number | SP 广告常规得分。Sponsored Products 常规位的流量得分（不含 SP 推荐位） |
| brandAdScore | number | SB 品牌广告得分。Sponsored Brands 品牌广告的流量得分（常规 + 视频，总和） |
| videoAdScore | number | SBV 视频广告得分。Sponsored Brands Video 视频广告的流量得分 |
| sponsoredRecommendationScore | number | SP 推荐位得分。Trending now / Seen on social media / Customers frequently viewed / 4 stars and above 等合计得分 |
| sponsoredRecommendationBreakdown | array | SP 推荐位得分明细。每项 `{title, score, scoreRatio}` |
| clickConcentrationShare | number | ABA TOP3 点击集中度。衡量点击是否集中在头部 ASIN；注意**不是转化率** |
| clickToPurchaseConversionRate | number | 点击到购买的转化率（purchaseQty / clickQty） |
| displayPositionTypes | array | 商品展示位置类型数组。可能包含以下值：natural=自然搜索结果位；ac=Amazon's Choice推荐位；sp=Sponsored Products赞助商品广告位；top=页面顶部品牌广告位；bottom=页面底部品牌广告位；er=Editorial Recommendations编辑推荐位；vedio=视频广告位；tr=Top Rated高评分推荐位；trfob=Top Rated Frequently Bought高频购买推荐位 |
| trafficCharacteristicMarkers | array | 关键词流量特征标记数组。可能包含以下值：isMainKw=主要流量词；isAccurateKw=精准流量词；isAccurateAboveKw=精准大词；isAccurateTailKw=精准长尾词 |
| conversionPerformanceMarkers | array | 转化效果标记数组。可能包含以下值：isPurchaseKw=出单词；isQualityKw=转化优质词；isStableKw=转化平稳词；isLossKw=转化流失词；isInvalidKw=无效曝光词 |
| lastNaturalRankTime | string | 最近有效自然排名的时间 |
| lastAdRankTime | string | 最近有效SP广告排名的时间 |
| periodEndDate | string | 本周期（周粒度）结束日期 = 开始周 + 7 天（站点时间） |
| updateTime | string | 关键词数据更新时间 |

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
curl -X POST https://tool-gateway.linkfox.com/sif/asinKeywords \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0XXXXXXXX", "country": "US", "pageSize": 100, "sortBy": "estSearchesNum", "desc": true}'
```

### 带关键词筛选和条件的示例

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/asinKeywords \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0XXXXXXXX", "country": "US", "keyword": "charger", "conditions": "nfPosition,isPurchaseKw", "sortBy": "lastRank", "desc": false, "pageNum": 1, "pageSize": 50}'
```
