---
name: linkfox-keepa-product-series
description: 通过Keepa查询亚马逊商品的历史时序数据，追踪价格变动、BSR排名、评分、卖家数量及购物车（Buy Box）趋势。
---

# Keepa-商品历史数据（Keepa Product Time-Series Data Explorer）

本技能用于查询亚马逊单个商品（ASIN）的历史时序数据，帮助卖家追踪价格走势、BSR 排名、评分、卖家数量及月销量随时间的变化。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询单个 ASIN 在指定亚马逊站点的历史时序数据，时间窗口最长 365 天。
- 覆盖价格（Buy Box、新品最低价、划线价、闪促价、Prime 专属价、FBA/FBM 价、优惠券价）、BSR（大类/小类）、评分与评分数、卖家数量、月销量。
- 支持美国、英国、德国、法国、日本、加拿大、意大利、西班牙、印度、墨西哥、巴西共 11 个亚马逊站点。

### ❌ 边界与限制

- **单 ASIN 限制**：每次请求只支持一个 ASIN；多 ASIN 比较需分别请求。
- **最长 365 天**：历史数据最多回溯 365 天。
- **数据粒度**：数据点按 Keepa 捕获变化的时刻分布，并非固定每日间隔。
- **不在范围内**：搜索词/关键词分析（用 ABA 数据）；广告/PPC 数据；Listing 文案优化；品类或市场整体聚合趋势（本工具仅针对单个 ASIN）；实时库存查询；评论文本与情感分析。

## 核心概念

本工具基于 Keepa 提供单个亚马逊商品（ASIN）的历史时序数据，返回带时间戳的指标数据点，支持在可配置时间窗口（最长 365 天）内做趋势分析。每次查询针对指定站点的单个 ASIN。

**时序格式**：所有数据序列均为 `{time, value}` 对象数组，`time` 为时间戳，`value` 为该时刻的指标值。BSR 数据额外含 `categoryName` 字段与 `points` 数组。

**BSR 含义**：BSR 数值越小代表销量排名越好，排名 1 即该类目最畅销商品。用户说"BSR 改善"指数值下降；"BSR 下降"指数值上升。

**可用数据序列**：

| 序列 | 启用参数 | 说明 |
|------|----------|------|
| Buy Box 价格 | *(默认返回)* | 购物车价格随时间变化 |
| 评分 | *(默认返回)* | 商品星级随时间变化 |
| 评分数 | *(默认返回)* | 评分数量随时间变化 |
| 月销量 | *(默认返回)* | 月度销量 |
| 小类 BSR | *(默认返回)* | 子类目畅销排名 |
| 新品最低价 | showPrice=1 | 市场最低新品价 |
| 划线价 | showPriceList=1 | 划线/标价 |
| 闪促价 | showPriceDeal=1 | 闪促价格 |
| Prime 专属价 | showPricePrime=1 | Prime 专属新品价 |
| FBA 价格 | showPriceFba=1 | 第三方 FBA 新品价 |
| FBM 价格 | showPriceFbm=1 | 第三方 FBM 新品价 |
| 优惠券价 | showPriceCoupon=1 | 优惠券后 Buy Box 价 |
| 大类 BSR | showBsrMain=1 | 主（根）类目畅销排名 |
| 卖家数 | showSellerCount=1 | 活跃卖家数量 |

**支持的站点**（domain 参数，完整说明见 [references/api.md](references/api.md)）：

| domain | 站点 |
|--------|------|
| 1 | Amazon.com（美国） |
| 2 | Amazon.co.uk（英国） |
| 3 | Amazon.de（德国） |
| 4 | Amazon.fr（法国） |
| 5 | Amazon.co.jp（日本） |
| 6 | Amazon.ca（加拿大） |
| 8 | Amazon.it（意大利） |
| 9 | Amazon.es（西班牙） |
| 10 | Amazon.in（印度） |
| 11 | Amazon.com.mx（墨西哥） |
| 12 | Amazon.com.br（巴西） |

用户未指定站点时默认 domain=1（美国）。

## 调用方式

- **API 端点**：`POST /keepa/productSeries`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/keepa_product_history.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-keepa-product-series-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 美国站商品基础价格历史**
```
asin: B0XXXXXXXX, domain: 1, days: 90
```

**2. 德国站长期 BSR 趋势（1 年）**
```
asin: B0XXXXXXXX, domain: 3, days: 365, showBsrMain: 1
```

**3. 跨履约渠道价格对比**
```
asin: B0XXXXXXXX, domain: 1, days: 30, showPriceFba: 1, showPriceFbm: 1, showPrice: 1
```

**4. 闪促与优惠券价格追踪**
```
asin: B0XXXXXXXX, domain: 1, days: 90, showPriceDeal: 1, showPriceCoupon: 1
```

**5. 商品健康度全面检查**
```
asin: B0XXXXXXXX, domain: 1, days: 90, showPrice: 1, showPriceList: 1, showPriceDeal: 1, showPricePrime: 1, showPriceFba: 1, showPriceFbm: 1, showPriceCoupon: 1, showBsrMain: 1, showSellerCount: 1
```

## 展示规则

1. **清晰呈现数据**：以表格展示时序数据或描述趋势；除非用户明确要求，不做主观商业建议。
2. **BSR 说明**：展示 BSR 数据时提醒用户数值越小代表销量排名越好。
3. **价格格式**：按站点匹配正确币种符号（美国 `$`、德/法/西/意 `EUR`、英国 `GBP`、日本 `JPY` 等）。
4. **时间格式**：时间戳以人类可读日期格式呈现。
5. **趋势总结**：序列较长时总结整体趋势（如"90 天内价格从 $29.99 降至 $24.99"），并突出显著变化（价格跳水、BSR 飙升、评分变动）。
6. **错误处理**：查询失败时说明原因并建议修正（如校验 ASIN 是否有效、检查 domain 是否正确）。
7. **单 ASIN 限制**：用户询问多个 ASIN 时，告知需逐个查询，依次发起多次调用。

## 用户表达与场景速查

**适用** —— 亚马逊商品级历史数据查询：

| 用户说 | 场景 |
|--------|------|
| "这个 ASIN 的价格历史"、"价格走势" | 价格趋势分析 |
| "看下 BSR 趋势"、"排名怎么样" | BSR 追踪 |
| "最近降价了吗"、"有没有秒杀" | 降价/秒杀检测 |
| "这个 Listing 有多少卖家" | 卖家数趋势 |
| "评分趋势"、"评论数变化" | 评分/评论追踪 |
| "FBA 和 FBM 价格"、"谁拿了 Buy Box" | 履约价格对比 |
| "这个商品月销多少" | 销量趋势 |
| "这个 ASIN 有没有价格战" | 竞争定价分析 |
| "看下 Keepa 图"、"Keepa 数据" | 明确的 Keepa 数据请求 |

不适用场景见上方【能力边界】。

**边界判断**：用户说"选品调研"或"竞品分析"时，若落脚点是查看某个具体 ASIN 的历史价格、BSR 或销量数据，则适用本技能；若需要关键词数据、市场整体趋势或广告指标，则不适用。

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

# Keepa-亚马逊价格历史 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/keepa/productSeries`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| asin | string | 是 | 亚马逊标准识别号(ASIN)，只支持单个ASIN，最大长度1000 |
| domain | string | 是 | 亚马逊域名ID。可选值：`1`（美国）、`2`（英国）、`3`（德国）、`4`（法国）、`5`（日本）、`6`（加拿大）、`8`（意大利）、`9`（西班牙）、`10`（印度）、`11`（墨西哥）、`12`（巴西） |
| days | integer | 否 | 限制历史数据天数，默认 `90` 天，最大 `365` |
| showPrice | integer | 否 | 设为 `1` 返回市场最低新品价曲线 |
| showPriceList | integer | 否 | 设为 `1` 返回划线价/标价曲线 |
| showPriceDeal | integer | 否 | 设为 `1` 返回闪促价格曲线 |
| showPricePrime | integer | 否 | 设为 `1` 返回Prime专属新品价曲线 |
| showPriceFba | integer | 否 | 设为 `1` 返回第三方FBA新品价曲线 |
| showPriceFbm | integer | 否 | 设为 `1` 返回第三方FBM新品价曲线 |
| showPriceCoupon | integer | 否 | 设为 `1` 返回优惠券后买盒价曲线 |
| showBsrMain | integer | 否 | 设为 `1` 返回大类BSR曲线 |
| showSellerCount | integer | 否 | 设为 `1` 返回卖家数曲线 |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN |
| buyboxPrice | array | Buybox价格（time=时间，value=Buybox价格） |
| price | array | 价格（time=时间，value=价格） |
| priceList | array | 划线价（time=时间，value=划线价格） |
| priceDeal | array | Deal价格（time=时间，value=Deal价格） |
| pricePrime | array | Prime价格（time=时间，value=Prime价格） |
| priceFba | array | FBA价格（time=时间，value=FBA价格） |
| priceFbm | array | FBM价格（time=时间，value=FBM价格） |
| priceCoupon | array | coupon价格（time=时间，value=coupon价格） |
| bsrMain | array | 大类BSR，每个元素包含 `categoryName`（类目名称）和 `points`（time=时间，value=排名） |
| bsrSub | array | 小类BSR，每个元素包含 `categoryName`（类目名称）和 `points`（time=时间，value=排名） |
| sellerCount | array | 卖家数（time=时间，value=卖家数） |
| rating | array | 评分（time=时间，value=评分） |
| ratingCount | array | 评分数（time=时间，value=评分数） |
| monthlySold | array | 子体销量（time=时间，value=销量） |
| costToken | integer | 消耗token |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | - | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
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
curl -X POST https://tool-gateway.linkfox.com/keepa/productSeries \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0DFRJ7WSX", "domain": "1", "days": 90, "showBsrMain": 1, "showPrice": 1, "showSellerCount": 1}'
```
