---
name: linkfox-sellersprite-traffic-keyword
description: 反查亚马逊ASIN的流量关键词，分析自然与广告词结构、转化类型及历史趋势。
---

# 卖家精灵-流量关键词（SellerSprite Traffic Keyword）

本技能用于按亚马逊 ASIN 反查其流量关键词，分析自然词与广告词结构、转化类型及历史趋势。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 以商品 ASIN 为输入，反查该商品获得流量的关键词列表。
- 分析关键词的流量占比类型（主要/精准/转化流失）、转化类型（优质/平稳/流失/无效）、曝光位置标签（自然搜索、AC 推荐、SP 广告等）。
- 查看关键词的自然位与广告位排名、月搜索量、月购买量、流量占比、PPC 竞价等指标。
- 支持历史月份（`yyyyMM`）查询与多维排序。

### ❌ 边界与限制

- 必填参数：`marketplace`、`asin`。
- 单次每页最多 100 条，最多查 2000 条。
- 历史查询需传 `month`（格式 `yyyyMM`），不传默认最近 30 天。
- **成本约束**：本工具消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需继续检索时先向用户说明会产生额外消耗。
- **不在范围内**：亚马逊关键词选品（用选品工具）；竞品店铺整体流量分析；广告投放优化与竞价策略建议；Listing 文案撰写。

## 核心概念

- **ASIN 反查词**：以商品 ASIN 为输入，查看该商品获得流量的关键词列表。
- **流量占比类型**（`trafficKeywordTypes`）：主要流量词、精准流量词、以及 schema 中的 `preciseLongTail`（工具文案为「转化流失词」）等。
- **转化类型**（`conversionKeywordTypes`）：如转化优质词、平稳词、流失词等。
- **词标签**（`badges`）：如自然搜索词、Amazon Choice 推荐词等。

## 调用方式

- **API 端点**：`POST /sellersprite/traffic/keyword`（完整参数/响应/错误码见 [references/api.md](references/api.md)）
- **Python 脚本**：`python scripts/sellersprite_traffic_keyword.py '<JSON 参数>' [--inline]`

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sellersprite-traffic-keyword-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 反查某 ASIN 的流量词（最近 30 天）**
```json
{
  "marketplace": "US",
  "asin": "B0XXXXXXXXX",
  "size": 50,
  "orderField": "rankPosition",
  "orderDesc": false
}
```

**2. 查询历史月份并按类型筛选**
```json
{
  "marketplace": "US",
  "asin": "B0XXXXXXXXX",
  "month": "202507",
  "trafficKeywordTypes": "primary,precise",
  "conversionKeywordTypes": "excellent,stable",
  "page": 1,
  "size": 100
}
```

## 展示规则

1. 结果优先展示：关键词、自然位、广告位、流量占比类型、转化类型。
2. 明确标注查询周期（最近 30 天或历史月份）。
3. 当存在分页时，告知总数与当前页。
4. 不输出与接口无关的主观商业建议，除非用户明确要求。

## 用户表达与场景速查

**适用** —— 按 ASIN 反查流量关键词：

| 用户说 | 场景 |
|--------|------|
| "反查这个 ASIN 的流量词"、"这个 ASIN 靠什么词出单" | ASIN 流量词反查 |
| "这个商品的自然词和广告词有哪些" | 自然/广告词结构分析 |
| "这个词的转化类型是什么" | 转化类型查看 |
| "查一下去年 7 月这个 ASIN 的流量词" | 历史月份流量词 |
| "按流量占比排一下这个 ASIN 的词" | 多维排序 |
| "SellerSprite traffic keyword"、"reverse ASIN keywords" | 英文触发表达 |

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

# 卖家精灵-流量词反查 API 参考

本文档与工具 `_sellersprite_traffic_keyword` 的 `inputSchema` / `outputSchema`（见 `temp/tools20260430.txt`）对齐。

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/sellersprite/traffic/keyword`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

| 参数 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| marketplace | string | 是 | 见下表 | 市场站点，默认 `US` |
| asin | string | 是 | maxLength 1000 | 要反查的商品 ASIN |
| month | string | 否 | 正则 `^(19|20)\d{2}(0[1-9]|1[0-2])$` | 历史月份，格式 `yyyyMM`；不传默认最近 30 天 |
| page | integer | 否 | 默认 1 | 当前页 |
| size | integer | 否 | 默认 50，最小 1，最大 100；最多查 2000 条 | 每页条数 |
| keyword | string | 否 | maxLength 1000 | 关键词筛选 |
| badges | string | 否 | maxLength 1000，多值英文逗号分隔 | 流量词类型（曝光位置），见 [badges 枚举](#badges-枚举) |
| trafficKeywordTypes | string | 否 | maxLength 1000，多值英文逗号分隔 | 流量占比类型，见 [trafficKeywordTypes 枚举](#traffickeywordtypes-枚举) |
| conversionKeywordTypes | string | 否 | maxLength 1000，多值英文逗号分隔 | 流量转化类型，见 [conversionKeywordTypes 枚举](#conversionkeywordtypes-枚举) |
| orderField | string | 否 | maxLength 1000，默认 `rankPosition` | 排序字段，见 [orderField 可选值](#orderfield-可选值) |
| orderDesc | boolean | 否 | 默认 `false` | 排序是否倒序 |

### marketplace 可选值

| 取值 | 含义 |
|------|------|
| US | 美国站 USD($) |
| JP | 日本站 JPY(￥) |
| UK | 英国站 GBP(£) |
| DE | 德国站 EUR(€) |
| FR | 法国站 EUR(€) |
| IT | 意大利站 EUR(€) |
| ES | 西班牙站 EUR(€) |
| CA | 加拿大站 C$($) |
| IN | 印度站 INR(₹) |

### badges 枚举

多个值用英文逗号分隔。

| 取值 | 含义 |
|------|------|
| naturalSearching | 自然搜索词 |
| amazonChoice | AC 推荐词 |
| editorialRecommendations | ER 推荐词 |
| fourStar | 四星推荐词 |
| highlyRated | HR 推荐词 |
| sponsorBrand | 品牌推荐词 |
| sponsorVideo | 视频推荐词 |
| ads | SP 广告词 |

### trafficKeywordTypes 枚举

多个值用英文逗号分隔（与工具 schema 文案一致）。

| 取值 | 含义 |
|------|------|
| primary | 主要流量词 |
| precise | 精准流量词 |
| preciseLongTail | 转化流失词 |

### conversionKeywordTypes 枚举

多个值用英文逗号分隔。

| 取值 | 含义 |
|------|------|
| excellent | 转化优质词 |
| stable | 转化平稳词 |
| lost | 转化流失词 |
| invalid | 无效曝光词 |

### orderField 可选值

| 取值 | 含义 |
|------|------|
| rankPosition | 自然排名（默认） |
| adPosition | 广告排名 |
| createdTime | 创建时间 |
| searchesRank | 搜索量周排名 |
| searches | 月搜索量 |
| purchases | 月购买量 |
| purchaseRate | 购买率 |
| products | 商品数 |
| supplyDemandRatio | 供需比 |
| latest1daysAds | 广告竞品数 |
| bid | PPC 竞价 |
| trafficPercentage | 流量占比 |

## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总条数 |
| marketplace | string | 市场编码 |
| asin | string | 查询的 ASIN |
| data | array | 流量词列表（对应第三方 `data.items`） |
| summaryList | array | 高频词总结列表 |
| columns | array | 列定义 |
| costToken | integer | 消耗 token |
| type | string | 渲染的样式 |

### summaryList 元素

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总次数 |
| keywords | string | 词 |

### data[] 元素（单条流量词）

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | string | 关键词 |
| keywordCn | string | 关键词中文翻译 |
| trafficKeywordType | string | 流量占比类型 |
| conversionKeywordType | string | 流量转化类型 |
| badges | array | 曝光位置（流量词类型） |
| rankPosition | object | 自然排名位次信息，结构见 [排名对象](#排名对象-rankposition--adposition) |
| adPosition | object | 广告排名位次信息，结构同 [排名对象](#排名对象-rankposition--adposition) |
| searches | integer | 月搜索量 |
| searchesRank | integer | 周搜索量排名 |
| searchesRankTimeFrom | integer | 周搜索量排名时间范围起 |
| searchesRankTimeTo | integer | 周搜索量排名时间范围止 |
| purchases | integer | 月购买量 |
| purchaseRate | number | 购买率 |
| products | integer | 商品数 |
| supplyDemandRatio | number | 供需比 |
| trafficPercentage | number | 流量占比 |
| naturalRatio | number | 流量分布-自然占比 |
| adRatio | number | 流量分布-广告占比 |
| calculatedWeeklySearches | number | 预估周曝光量 |
| impressions | integer | 展示量 |
| clicks | integer | 点击量 |
| bid | number | PPC 竞价 |
| bidMin | number | PPC 竞价下限 |
| bidMax | number | PPC 竞价上限 |
| latest1daysAds | integer | 最近 1 天广告竞品数 |
| latest7daysAds | integer | 最近 7 天广告竞品数 |
| latest30daysAds | integer | 最近 30 天广告竞品数 |
| sprt | number | SP 相关比率 |
| monopolyClickRate | number | 垄断点击率 |
| top3ClickingRate | number | Top3 点击率 |
| top3ConversionRate | number | Top3 转化率 |
| titleDensity | number | 标题密度 |
| stats | array | 高频词，元素见下表 |
| updatedTime | integer | 更新时间 |

### stats[] 元素（高频词子项）

| 字段 | 类型 | 说明 |
|------|------|------|
| keywords | string | 词 |
| total | integer | 总条数 |
| rankPosition | object | 自然排名位次，结构见下 |
| adPosition | object | 广告排名位次，结构见下 |

### 排名对象（rankPosition / adPosition）

| 字段 | 类型 | 说明 |
|------|------|------|
| updatedTime | integer | 排名时间 |
| pageSize | integer | 每页多少条数据 |
| index | integer | 当前页排第几 |
| page | integer | 第几页 |
| position | integer | 总结果中排第几 |

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/sellersprite/traffic/keyword   -H "Authorization: $LINKFOXAGENT_API_KEY"   -H "Content-Type: application/json"   -d '{
    "marketplace": "US",
    "asin": "B0XXXXXXXXX",
    "page": 1,
    "size": 50
  }'
```
