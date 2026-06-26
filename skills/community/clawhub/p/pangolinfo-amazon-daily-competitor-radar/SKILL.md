---
name: amazon-daily-competitor-radar
description: |
  Use when: user says "每日竞品监控" / "盯一下 ASIN X 的价格变化" / "今天我的排名怎么样" / "我的关键词排名跌了吗" / "竞品有动作吗" / "track ASIN X" / "daily radar" / "Buy Box 被抢了吗".
  Covers: ASIN 健康体检 + 贴身竞品 SERP 排位 + 类目新进入者扫描 + 主动给"防守/反击"动作建议。可写入基线对比"昨天 vs 今天"。
  NOT for: 从 0 到 1 找新 niche (use amazon-product-explorer) / 写 Listing 文案 (use amazon-listing-optimization) / 单点查询 ASIN (call get_amazon_product directly).
version: 3.1.0
mcp_tools_used:
  - pangolinfo_capabilities
  - search_amazon
  - get_amazon_product
  - list_bestsellers
  - list_new_releases
  - list_seller_products
  - get_amazon_reviews
  - search_amazon_alexa
  - ai_search
  - filter_niches
applies_to: [claude-code, cursor, cline, windsurf, hermes, codex, openclaw]
budget:
  fast: { duration: "≤ 60s", cost: "≤ 5 积点", calls: "≤ 4" }
  full: { duration: "≤ 3min", cost: "≤ 20 积点", calls: "≤ 10" }
baseline_storage: "~/.pangolinfo/baselines/<asin>.json"
---

# Amazon 每日竞品雷达 SOP

> 跑前必读：本文件末尾《核心规则 / Core Rules》章节（已内联，自包含）。
> 角色：Amazon 增长顾问。每天给一份"市场脉搏 + 立即动作"报告。

## 用户触发与档位

**Fast（默认 ≤60s）**：
- "盯一下 B09B8V1LZ3"
- "今天我的 ASIN 怎么样"
- "竞品有动作吗"

**Full（≤3min）**：
- "完整雷达扫描"
- "包括竞品差评对比"
- "深度监控报告"

**单工具直通**：
- "看 X 类目热销榜" → `list_bestsellers`
- "看新品榜" → `list_new_releases`

---

## ⏱ 基线机制（解决"对比昨天"）

MCP 是无状态的。AI 客户端按以下方式自管基线快照：

**存储位置**：`~/.pangolinfo/baselines/<asin>.json`

**快照结构**：
```jsonc
{
  "asin": "B09B8V1LZ3",
  "snapshotAt": "2026-05-19T09:00:00Z",
  "site": "amz_us",
  "price": "$49.99",
  "bsrTop": "#4 in Electronics > Headphones",
  "ratingStr": "(192514)",
  "buyBoxSeller": "Amazon.com",
  "couponPresent": false
}
```

**用法**：
- Fast 跑前：读 `<asin>.json`；不存在 → 首次跑，建快照，告诉用户"已建立基线，明天起就有'昨天 vs 今天'对比了"。
- Fast 跑后：写当天快照覆盖。
- 不依赖此机制时（用户没给主 ASIN，纯类目监控）跳过。

AI 客户端**没有文件系统**（如纯 MCP）→ 用 in-memory session-scoped 字典；告诉用户"对比基于本 session 内的快照，重启 session 会丢失"。

---

## Fast 档 SOP(3 回合 ≤ 60s)

适合:用户给了 1 个主 ASIN(关键词可选 —— 没给就靠下方"反向关键词工程"自动反推)。

```
回合 1 (5s)  get_amazon_product(主ASIN) | search_amazon(核心词/反推词)      ← 2 并发
回合 2 (5s)  list_bestsellers(类目slug) | get_amazon_product(贴身竞品1)     ← 2 并发
回合 3 (5s)  get_amazon_product(贴身竞品2)                                  ← 单发
              (回合 1 的 search_amazon 结果里挑紧邻用户 ASIN 前后位的 2 个)

LLM 整合 (~30s)
```

### 反向关键词工程(用户没给关键词时,R1 之前做 —— 不额外耗 tool)

用户常常**只给一个主 ASIN**。此时"核心词"要从 ASIN 自身反推,而不是逼用户提供:
1. R1 的 `get_amazon_product` 返回后,取 **leaf category 字符串**(`bestSellersRankItems[]` 最深一条的 name)+ 标题里的 **top 功能形容词**(如 "wireless" / "leakproof" / "desk")。
2. 组合成 2-3 个高概率"流量金词"(traffic money words),如 leaf="Earbuds" + 标题 "wireless"/"sport" → `wireless earbuds` / `sport earbuds`。
3. **过滤掉用户自有 brand 词**(否则 User ASIN 永远被自家品牌词命中,无 hijacker 信号)。
4. (可选,Full 档才做)用 `filter_niches(nicheTitle=<反推词>, marketplaceId="US")` 按 `searchVolumeT90` 降序锁 3-5 个词,确认这些词真有量。Fast 档为控时效,直接用反推的 2-3 个词跑 search_amazon 即可。

   **Extract**(`filter_niches`): `data.items.data[]` → 每个反推词取 `nicheTitle` / `searchVolumeT90`(90 天搜索量,用来排序选词) / `searchVolumeGrowthT90`(是否在涨) / `productCount`(竞争密度) / `top5ProductsClickShareT360`(头部集中度)。只留 `searchVolumeT90` 有量的词;返 0 的词丢弃。`marketplaceId` 用 ISO 站点码 `"US"`,不认 `categoryId`(那是 filter_categories 的)。

> 注意 R1 的 `get_amazon_product` 与 `search_amazon` 名义上是 2 并发,但反向关键词依赖 PDP 返回。实操:若用户**已给**关键词 → 直接 2 并发;若**没给** → R1 先单发 `get_amazon_product` 反推词,再发 `search_amazon`(退化成 1.5 回合,仍 ≤60s)。

**总耗时**:~15s tool + 30s LLM ≈ **45s**
**总成本**:~5 积点
**总调用**:5 次 tool

**并发硬上限**: 2(实测 2026-05-28:3 并发会触发后端业务码 9200 "no content")。`pangolinfo_capabilities` 不算后端调用,可任意并发。

### R1 — 2 并发(自身 + SERP)

```jsonc
// (a) 自身 ASIN 健康
{ "name": "get_amazon_product",
  "arguments": { "asin": "<user_asin>", "site": "amz_us" }}

// (b) 核心词 SERP 排位
{ "name": "search_amazon",
  "arguments": { "keyword": "<core_keyword>", "site": "amz_us" }}
```

**参数约束**:
- `search_amazon` 参数名是 `keyword`(单数,REQUIRED),**不是** `keywords`(复数)
- 长尾词(3+ word)频繁返回 `results=[]` 但仍扣 1 积点,空结果时降一词重试

**Extract**:
- **自身 ASIN**: `data.json[0].data.results[0]` 取 `{price, star, rating, brand, seller.name, bestSellersRankItems[].link, breadCrumbs}` → 与基线对比,命中阈值即标预警
  - `star`(0-5 分数)vs `rating`(评分人数)是两个字段,别混。`sales`(月销字符串)替代旧 `monthlySoldVolume`(已不存在)
  - 头部 ASIN(Amazon 自营)有时 `bestSellersRankItems=[]` + `category_id=""` + `brand=""`,头部品 PDP 解析退化。遇到时不阻塞,从 SERP 返回里取 title/price/star/rating 替代
- **SERP**: `data.json[0].data.results[]` 找 user_asin 在第几个 → Organic Rank;前后 ±2 位的 = 贴身竞品候选
  - **±30% 价格带过滤**: 用户 ASIN 价格 ±30% 范围外的 ASIN 标"Outside Price Band — not tracked",不算贴身竞品
  - **过滤 User 自有品牌词**: 派生关键词时去掉用户自己的 brand,否则 User ASIN 永远会被自家品牌词命中,无 hijacker 信号意义

### R2 — 2 并发(类目脉搏 + 贴身竞品 1)

```jsonc
// (a) 类目脉搏
{ "name": "list_bestsellers",
  "arguments": { "categorySlug": "<推断 slug>", "site": "amz_us" }}

// (b) 贴身竞品 1
{ "name": "get_amazon_product",
  "arguments": { "asin": "<adjacent_competitor_1>", "site": "amz_us" }}
```

**Bestsellers 注意**:
- 实际返回 **Top-50**(后端硬上限,不是宣称的 Top-100)
- `twentyFourHourOldSalesRank` / `percentageChange` 字段可能为空字符串(后端未抓到 24h delta);不可依赖,改看 BSR 绝对值是否有 NEW 标
- 取前 10,对比基线看是否有新入榜

### R3 — 单发(贴身竞品 2)

```jsonc
{ "name": "get_amazon_product",
  "arguments": { "asin": "<adjacent_competitor_2>", "site": "amz_us" }}
```

**Extract** (R2 + R3 合并): 每个竞品取 `{price, star, rating, coupon, badge, aiReviewsSummary}` 用于对比卖点。

**Skip rule**: 自身 ASIN Organic Rank ≤ 3 且无价格异动 → 跳过 R3,直接给"市场健康"报告(但 Early Exit 受下方规则约束)。

### 类目新进入者扫描 = MANDATORY(早返也跑)

**关键语义**: 自身 ASIN 稳 ≠ 没有新人爬榜。R2 的 `list_bestsellers`(+ Full 档的 `list_new_releases`)**永远要跑**,即使 R1 判定自身健康。早返只能跳过"自身/贴身竞品深拆",**不能跳过类目雷达**。

### Early Exit 条件(必须全部满足)

只有以下三条 **同时** 成立时才能输出 `🟢 Marketplace Conditions Stable. No actionable anomalies detected.`:
1. R1 SERP 排位无负向位移(无 `↓` movers,vs 基线无掉排名)
2. R1 自身 ASIN 无价格 / Buy Box / coupon 异动(基于下方预警阈值表)
3. **类目雷达(R2 bestsellers,已 MANDATORY 跑过)无 NEW 入榜 + 无价格突变**

**任一条不满足 → 必须输出完整 4 段报告**。
- 若仅第 3 条不满足(自身稳但类目出现新进入者) → **不要输出 stable 行**,改出 Section 3"类目新动向"的爆款警报。
- 例外:如果 search_amazon_alexa 触发了双 502 fallback(Phase 2 AI 审计调用此工具时) → Early Exit **FORBIDDEN**,必须出 partial-report 模式。

### Stateless 趋势箭头规则

`↑` / `↓` / `NEW` 等趋势箭头**仅当本 session 有基线快照(或用户在 prompt 里贴了 `historical_snapshot`)时才渲染**。首次跑(无基线)→ **不画任何箭头**,只输出当前绝对值整数,防止数据幻觉。

### Fast 预警阈值（基于基线对比）

| 指标 | 字段 | 黄色预警 | 红色预警 |
|---|---|---|---|
| 售价 | `price` | 单日降 5-15% | 单日降 >15% |
| BSR | `bestSellersRankItems[0]` 里的数字 | 24h 提升 20-50% | >50% 或进 Top 100 |
| Buy Box | `seller.name` | 7 日变 1 次 | 24h 变 ≥2 次或切品牌方 |
| 评论数 | `rating` 括号里的数 | 单日 +5 / 7 日 +20 | 单日 +15 / 7 日 +50 |
| Coupon | `coupon` 字段 | 新出 5-10% | 新出 ≥10% 或叠 Deal |

### Fast 报告 4 段

```
1. 📍 排位脉搏（一行）
   "<user_asin> Organic #<X>（昨日 #<Y>）/ BSR #<X> in <类目>"
   （首次跑则说"已建立基线"）

2. 🚨 预警（按红/黄分组）
   - 🔴 价格：竞品 B0XXX 降 18% → 建议：上 8% 防御 Coupon
   - 🟡 Buy Box：从 Amazon.com 切到 SellerXYZ → 建议：48h 观察

3. 🆕 类目新动向（仅当 Bestsellers 榜有新人）
   - 新入榜 ASIN B0XXX，#7 → 建议：48h 内拆解

4. 🛡 今日行动建议（≤3 条）
   - <action 1>
```

报告**末尾强制**问："要每天自动跑这份雷达吗？"
- Claude Code：调起 `CronCreate` 写一个 `0 9 * * *` 触发本 prompt
- 其他客户端：给 OS cron / n8n schedule 模板

---

## Full 档 SOP（追加 1-3 回合 ≤ 3min）

仅在用户明示"完整 / 详细 / 深度"时触发。先跑 Fast，再追加：

### R3.5 — 分页深度引擎(可选,仅当 Fast 没在 Page 1 定位到 user ASIN)

Fast 的 search_amazon 默认只看 page 1。若某个流量金词在 page 1 没找到 user ASIN(说明排位掉到第 2-3 页),Full 档逐页深挖确认真实排位:

```jsonc
// Round 2: 未定位的词查 page 2
{ "name": "search_amazon", "arguments": { "keyword": "<word>", "page": 2, "site": "amz_us" }}
// Round 3: 仍未定位的词查 page 3(最大深度,到此为止)
{ "name": "search_amazon", "arguments": { "keyword": "<word>", "page": 3, "site": "amz_us" }}
```

**Short-circuit**: 任一页定位到 user ASIN → 立即冻结该词的排位,不再翻下一页。**最大深度 = Page 3**(搜索位只统计 Amazon 自然位 + SP 位)。每页并发仍守 ≤2。

### R3.8 — AI 助手可见性审计 (Rufus / search_amazon_alexa) [CONDITIONAL]

**触发条件**: 仅当 Fast/R3.5 检测到 **掉排名 或 贴身竞品挤压** 时才跑(自身稳则跳过,省时省钱)。

**⏱ 这是长响应接口 —— 调用前必读**:
- `search_amazon_alexa` 是 Rufus 实时生成,**单 prompt 通常 60–90s,最大可达 ~200s**;计费 **6 积点/prompt**。
- **强制只传 1 个 prompt**: 多 prompt 是线性叠加(N prompt ≈ N×6 积点 + N×响应时间),极易突破 200s。本相位永远 `prompts` 数组只放 1 条。
- 调用前在用户消息里报:"将查 1 次 Rufus AI 可见性,约 6 积点 / 最长 ~200 秒,是否继续?"

```jsonc
{ "name": "search_amazon_alexa", "arguments": {
  "prompts": ["<由流量金词组成的 1 条干净复合名词短语,如 'wireless sport earbuds'>"]
}}
```
> 不要传 `marketplaceId`(此工具固定 amz_us,只接受 `prompts` + 可选 `screenshot`)。短语要干净,别塞整句对话或 URL。

**判定**: 在返回的 `products[].items[]` 里找 user ASIN → 🟢 在 AI 推荐池内 / 🔴 不在;记下出现的竞品 ASIN + Rufus 给它们打的卖点标签。

**双 502 resilience**: 502 / 超时 → retry 1 次(2s backoff)。仍失败 → 注入 `⚠️ Rufus 上游超时,本次 AI 可见性 UNKNOWN`,继续后续相位(**不阻塞**)。**注意: 一旦触发双 502 fallback,本次 cruise 的 Early Exit FORBIDDEN**,必须出 partial-report。

### R4 — 贴身竞品差评对比(**预算告知后**)

⚠️ "将抓贴身竞品 2 个差评页,约 10 积点 / ~15 秒,是否继续?"(get_amazon_reviews 实测 5pt/页)

```jsonc
{ "name": "get_amazon_reviews",
  "arguments": { "asin": "<competitor1>", "pageCount": 1,
                 "filterByStar": "critical", "sortBy": "recent" }}
{ "name": "get_amazon_reviews",
  "arguments": { "asin": "<competitor2>", "pageCount": 1,
                 "filterByStar": "critical", "sortBy": "recent" }}
```

**用途**：识别"竞品在测款"信号——近 14 天差评激增 = 新版本翻车，可乘机抢。

### R5 — list_new_releases 看类目新进入者

```jsonc
{ "name": "list_new_releases",
  "arguments": { "categorySlug": "<slug>", "site": "amz_us" }}
```

**用途**：识别"竞品在测款"另一个信号——新入榜的同类 ASIN（30 天内上市）。

### R6 — 竞品卖家店铺监控 (list_seller_products) [CONDITIONAL]

**触发条件**: 仅当发现 Buy Box 被某第三方卖家抢占、或某贴身竞品疑似"多 SKU 铺货打法"时跑。用来看这个对手卖家在售多少 SKU、是否在同类目快速扩品。

```jsonc
{ "name": "list_seller_products", "arguments": {
  "sellerId": "<从竞品 PDP 的 seller.id 拿>", "site": "amz_us",
  "pageCount": 1
}}
```

**前提**: `sellerId` 来自前面某个 `get_amazon_product` 返回的 `seller.id`（"sold by" 链接），不是凭空给。`pageCount` 可一次累计前 N 页（≤3，跨页合并）；想按类目过滤该卖家商品可加 `categoryId`。Amazon 自营 `sellerId="ATVPDKIKX0DER"`。

**Extract**: `data.json[0].data.{results[], maxPage, nextPage}` → `results[]` 每行 `asin/title/price/star/rating/rank/img`。统计该卖家 SKU 总数、同类目新品占比 → 判断对手是"单品深耕"还是"批量铺货"。

### R7 — 站外口碑/舆情监控 (ai_search) [CONDITIONAL]

**触发条件**: 仅当 Full 档检测到自身或竞品有重大异动（评分骤跌、差评激增、突发促销）、需要确认是否有站外舆情发酵时跑。Fast 档禁用（`ai_search` overview ~30s）。

```jsonc
{ "name": "ai_search", "arguments": {
  "query": "\"<brand 或 product>\" (review OR complaint OR recall OR problem) -site:amazon.com",
  "mode": "overview"
}}
```

**前提**: 只用 `mode="overview"`（单次 ~30s）；**禁用 `ai_mode`**（30-60s，超 Full 时效）。`query` 必填，是字符串。

**Extract**: `data.json.items[]` 里 `type="ai_overview"` 的 `content[]`(AI 摘要) + `references[].{title,url,domain}`(来源链接) + `type="organic"` 的 `items[].{title,url,text}`。提炼"站外是否有负面发酵/竞品被吐槽点"，作为防守/反击判断的旁证。AI Overview 不一定触发，缺失时降级用 organic（R-2 不编造）。

### Full 报告（在 Fast 4 段基础上扩 3 段）

```
5. 🤖 AI 助手可见性审计(仅当 R3.8 触发时渲染,否则隐藏)
   提示短语种子: `<传入 search_amazon_alexa 的复合名词短语>`
   - User ASIN 识别状态: 🟢 在 AI 推荐池 / 🔴 不在 / ⚠️ Rufus 双 502 超时,本次未知
   - AI 引擎里出现的竞品 ASIN: B0XXX — <Rufus 推它的卖点标签>
   - 战术拦截点: <1 句:改哪条五点/QA 去抢 AI 流量份额>

6. 🧪 测款/促销识别
   - 测款信号：竞品 B0XXX 近期差评激增 + 主图变 → 高概率新版翻车
   - 促销信号：B0YYY 降价 12% + Coupon 5% + BSR 跳升 → 7 天促销窗口

7. 🎯 行动复核时点
   - 48h：复查 Buy Box 是否归位
   - 7 天：复查竞品促销是否撤
```

---

## 报告输出规范

- 每条预警 ≤ 5 段：等级 / 触发指标 / 场景判定 / 影响评估 / 建议动作
- 一份报告 ≤ 3 条行动建议（卖家执行力有限）
- 报告语气中性，禁"必跌""碾压"
- 数字带来源 tool 名

## 与其他 SKILL 的协同

- 🔄 用户问"为什么我的 BSR 降了" → 引导 `amazon-listing-optimization` 看 Listing 是否要改
- 🔄 用户问"换 niche 试试" → 引导 `amazon-product-explorer`
- 🔄 自身评分跌破 4.0 → 主动提示 `amazon-listing-optimization` Step 1 拉差评

## 反模式

- ❌ 一回合并发 ≥ 3 个 scrapeApi → 实测会触发业务码 9200,降级串行
- ❌ Fast 档调 get_amazon_reviews → 5pt/页太贵,Fast 档预算 ≤5 积点
- ❌ 用 search_amazon 抓 BSR / New Releases → 用 list_bestsellers / list_new_releases
- ❌ 无基线就声称"价格降了 X%" → 必须有基线快照才能比,没有要明说"首次跑"
- ❌ 跑满 Full 档即使 Fast 已是"市场健康"
- ❌ 用 `bsr_category_path` 字段 → 不存在;用 `bestSellersRankItems[]` + `category_id`
- ❌ 用 `monthlySoldVolume` 字段 → 不存在;用 search_amazon 的 `sales` 字符串字段
- ❌ 用 `keywords`(复数)调 search_amazon → 真实参数 `keyword`(单数,REQUIRED)
- ❌ `search_amazon_alexa` 传 `marketplaceId` → 此工具固定 amz_us,只接受 `prompts` + `screenshot`
- ❌ `search_amazon_alexa` 一次传多个 prompt → 长响应接口(单 prompt 60–90s,最大 ~200s),多 prompt 线性叠加易超时;**永远只传 1 条**
- ❌ Fast 档调 `search_amazon_alexa` → 长响应 + 6 积点,只在 Full 档 R3.8(检测到掉排名/挤压)才调
- ❌ `wipo_search(source="USTM")` → 后端不支持文字商标,只 `USID` 设计专利;文字查询走 `ai_search`
- ❌ `marketplaceId="ATVPDKIKX0DER"` → 这是 Amazon merchant ID,不是 filter_niches/filter_categories 入参;后者要 ISO 站点码 `"US"`/`"UK"`/`"DE"`
- ❌ R3.8 search_amazon_alexa 双 502 时触发 Early Exit → 必须 FORBIDDEN,改出 partial-report 模式
- ❌ 跳过类目雷达(list_bestsellers)→ 自身稳 ≠ 没新人爬榜,类目扫描是 MANDATORY,早返也跑
- ❌ 派生关键词时不过滤 User 自有品牌词 → User ASIN 永远会被自家品牌词命中
- ❌ 先凭直觉说"做不到"再实测可查 → 违反 R-11,先调 `pangolinfo_capabilities` 再下结论

---

# 核心规则 / Core Rules（本 skill 自包含，无需外部文件）

> 以下规则对所有 Pangolinfo skill 通用。本文件已内联，单独加载即生效。

## R-1 鉴权与默认值

### API Key（两套，别混）
Pangolinfo 有**两套独立的 key 注入路径**，对应两种运行形态：

- **Skill 侧（本文件所在形态）**：AI 从**环境变量 `PANGOLINFO_API_KEY`** 读取 key。这是 skill 默认的 key 来源——由用户在运行环境里设好，AI **直接读、不要反复追问用户**。
- **MCP server 侧**：key 走 MCP 配置（CLI `--api-key=pgl_xxx` / 同名 env `PANGOLINFO_API_KEY` / `~/.pangolinfo/config.json` / hosted URL `?api_key=pgl_xxx` 或 HTTP 头 `Authorization: Bearer pgl_xxx`）。

两者**互相独立**：skill 侧改 env var 不会影响已连上的 MCP server，反之亦然。key 前缀均为 **`pgl_`**。

### First-time setup（工具没注册 / 首次 AUTH 失败时）
若 `pangolinfo_capabilities` 探针发现工具**未注册**，或任一 tool 直接返回 **AUTH**，说明 key 尚未配好。此时**停止跑 SOP**，引导用户：

1. 到 **https://www.pangolinfo.com** 登录，复制 API Key（`pgl_` 开头；新用户有免费额度）。
2. 配置 key：
   - Skill 形态 → 设环境变量 `export PANGOLINFO_API_KEY="pgl_xxx"`。
   - MCP 形态 → 写进 `~/.pangolinfo/config.json`，或 MCP URL `?api_key=pgl_xxx`，或头 `Authorization: Bearer pgl_xxx`。
3. **重启 / 重连**（env var 与 MCP 配置都不热加载）。
4. 让用户配好后再来。AI **不能**替用户改配置或重连。

### 默认值
- 默认市场：`marketplaceId: "US"` / `site: "amz_us"`；US 邮编默认 `"10041"`（纽约）。除非用户明示其他站点。
- 报告语言**与用户提问语言一致**；但 Listing 正文（Title / Bullets / Backend）始终用目标市场语言（默认英文）。

## R-2 数据真实

- **只用 MCP 返回的硬数据**。**绝不编造**搜索量、排名、月销、评论数、Buy Box 卖家等。
- 数据缺失时明确告知用户"该字段后端未返回"或"需手动补充"。不要尾随免责声明、不要写"约""大概"。
- 每个数字必须可回溯到具体 tool 调用与字段路径（如 `get_amazon_product.data.json[0].data.results[0].star`）。

## R-3 调用前先看能力

第一次接入时调一次 `pangolinfo_capabilities { detail: "summary" }`（0 积点 / 2ms），拿到**当前**的 tool 清单 + workflows + tips。工具数量与名称会随版本变化，**以本次返回为准，不要钉死数字、不要凭旧记忆调 tool**。该调用同时是连接健康探针：工具未注册或返回 AUTH → 转 R-1 first-time setup。

## R-4 时效性硬规则（**最重要**）

### R-4a 双档模式

每个 SOP 强制提供两档：

| 档位 | 触发条件 | 总耗时 | 总积点 | 总 tool 调用次数 |
|---|---|---|---|---|
| **Fast** | 默认 / 用户没明说"详细/深度/完整报告" | **≤ 90 秒** | **≤ 8 积点** | **≤ 6 次** |
| **Full** | 用户明说"详细 / 完整 / 深度 / 全面" | ≤ 5 分钟 | ≤ 30 积点 | ≤ 15 次 |

跑 Fast 档时**禁止**调下列慢/贵 tool：
- ❌ `get_amazon_reviews`(5pt/页 + 10s/次)
- ❌ `ai_search` mode='ai_mode'（30-60s）
- ✅ `ai_search` mode='overview' 最多 1 次

跑 Full 档时各项上限：
- `get_amazon_reviews` ≤ 3 个 ASIN × pageCount=1
- `ai_search` ai_mode ≤ 1 次，overview ≤ 2 次
- `wipo_search` ≤ 3 次

### R-4b 并行调用（最关键的加速手段）

**独立的 tool 调用应在同一回合并发发送**，但受 scrapeApi 速率限制约束。

#### 后端速率：实测 **2 QPS 稳定**(3 QPS 会触发 9200 "no content")

- ✅ 同一回合**最多并发 2 个** scrapeApi 调用（含 search_amazon / get_amazon_product / list_* / filter_* / search_categories / get_category_* / get_amazon_reviews / wipo_search / ai_search / keyword_trends / search_local_maps）— 2026-05-28 真实压测确认 3 并发会被后端拒
- ✅ `pangolinfo_capabilities` 不走后端，可任意并发
- ❌ 一次同时发 3 个 `search_amazon` 会有至少 1 个返回业务码 `9200 "Scrape failed: no content returned"`

#### 推荐节奏

| 总调用数 N | 节奏 |
|---|---|
| N ≤ 2 | 一回合 2 并发 |
| 3 ≤ N ≤ 6 | 分多回合：每回合 2 并发,回合之间间隔 ~1s |
| N ≥ 7 | 重新设计 SOP，先早返再决定是否继续 |

#### 并行 vs 串行判定

- 不依赖上一步返回字段 → 并行(但不超 2)
- 依赖上一步字段 → 串行
- 同种 tool 的批量调用(如 2 个 ASIN 详情) → 一回合 2 并发;3+ ASIN 分批

#### 遇到 RATE_LIMIT 怎么办

收到 `[RATE_LIMIT]` 错误：等 ~1s 重试该 1 个 tool（不要全部重试），其余已成功的别动。连续 2 次 RATE_LIMIT 或业务码 9200 说明 QPS 节流,降到每回合 1 并发(完全串行)。

### R-4c 早返

任一步骤拿到"足够下结论"的数据后**立即生成报告**，不要为凑齐 SOP 强跑：

| 触发 | 立即返回 |
|---|---|
| `filter_niches` 返回 0 条 | "无符合条件的 niche，建议放宽 X、Y 参数" + 给出参数建议清单 |
| `wipo_search` 命中红线（status='ACT' 且 hol 是大公司）| 该方向淘汰，跳过后续单品深拆 |
| 用户主 ASIN 在 SERP Top 3 + 无新 BSR 异动 | 给"健康"判定，跳过评论挖掘 |
| `get_amazon_product` upstream 404 ("url not found") | 告知 ASIN 失效，跳过后续 |

### R-4d 慢操作前先打预算

调下列 tool 前**必须**在用户消息里报"将花 X 积点 / 约 Y 秒"，让用户有机会取消：

- `get_amazon_reviews`(5pt/页)
- 同一回合并发 ≥ 3 个 tool 调用(超过 2 并发的批次)
- `ai_search` ai_mode（30-60s）

## R-5 不暴露原始 JSON

AI 的回答里**不要**贴原始 tool 返回。结构化呈现：

- 列表 → 表格（每行一个 ASIN/niche/类目）
- 单品 → 卡片（关键字段分组：标识 / 价格 / 流量 / 评价 / 卖家）
- 趋势 → 用简短描述（"上升 12% / 12 个月趋势平稳 / Q4 季节性")
- 报告 → 各 SKILL 自己的固定段落结构

## R-6 单工具直通

用户问简单单步查询时**不要强行跑完整 SOP**，直接调对应单 tool 给结果：

| 用户说 | 直接调 | 不要跑 SOP |
|---|---|---|
| "查 ASIN B0XXX" | `get_amazon_product` | ❌ product-discovery |
| "X 类目 best sellers" | `list_bestsellers` | ❌ |
| "Apple 在美国的专利" | `wipo_search source=USID hol='Apple'` | ❌ ip-clearance SOP |
| "wireless earbuds 热度趋势" | `keyword_trends` | ❌ |
| "B0XXX 的差评" | `get_amazon_reviews filterByStar=critical pageCount=1` | ❌ amazon-listing-optimization |

## R-7 不推荐外部工具

不主动提 Keepa / SellerSprite / Helium 10 / Jungle Scout 等竞品。用户问起再说"本工具不直接提供 X 能力，可考虑 ..."。

## R-8 报告语气

- 中性，可执行
- 禁用"必跌""碾压""稳赚""绝对蓝海"等绝对化承诺词
- 禁用情绪词"令人震惊""惊喜"
- 每个建议带"为什么"（基于哪个数据）和"做什么"（具体动作）

## R-9 错误处理

MCP server 已把每个错误渲染成结构化三行（`[CODE]` + 可否重试 + 用户动作）。AI 的职责是**按 CODE 语义正确反应，别瞎重试、别原地打转**。6 类错误：

| Code | 可否重试 | 处理 |
|---|---|---|
| `AUTH` | ❌ terminal | key 无效/缺失/过期。**用同一个 key 重试一定还失败 → 绝不重试**。停止 SOP，按 R-1 first-time setup 引导用户：复制正确 key（https://www.pangolinfo.com）→ 写进 env `PANGOLINFO_API_KEY` 或 MCP 配置 → **重启/重连**（不热加载）。AI 无法替用户改配置或重连。⚠️ 坑：invalid key 在后端是 bizCode **1004**（不是 HTTP 401），别因为"不是 401"就误判成别的错。 |
| `QUOTA` | ❌ terminal | 积分不足 / 套餐过期，重试无用。提示用户去 https://www.pangolinfo.com 充值或升级，停止本次 SOP。 |
| `BAD_INPUT` | ❌ terminal | 参数有误，**重试相同参数无用**。检查参数名/值（`marketplaceId` 非 `marketplace_id`、ASIN、zipcode、parserName 等，见 R-10），修正后才重试。 |
| `RATE_LIMIT` | ✅ 临时 | 含业务码 `9200`("no content")/`4029`/`4030`。等 ~1-5s 重试**该一个**请求；同时降回合并发到 1。连续 2 次仍失败则跳过本步。 |
| `SERVER` | ✅ 临时 | 服务端临时错误（含 9100/9101）。重试 1 次；仍失败告知用户跳过本步，继续 SOP。 |
| `NETWORK` | ✅ 临时 | 网络异常。提示用户检查到 www.pangolinfo.com 的连接后重试。 |

**总则**：terminal 类（AUTH/QUOTA/BAD_INPUT）重试是浪费，直接停或修参数；transient 类（RATE_LIMIT/SERVER/NETWORK）才重试，且只重试失败的那一个、别全批重发。

## R-10 字段名速查（最常踩的坑）

| ❌ 错（直觉常写的） | ✅ 对（真实字段）|
|---|---|
| `marketplace_id` | `marketplaceId` (值是 ISO 站点码 "US"/"UK"/"DE",不是 Amazon merchant ID `ATVPDKIKX0DER`) |
| `niche_title` | `nicheTitle` |
| `search_volume_t90_min` | `searchVolumeT90Min` |
| `top5_brands_click_share_max` | `top5ProductsClickShareT360Max`（products 不是 brands）|
| `return_rate_t360_max` | `returnRateT360Max` |
| `monthly_sales_min` | （不存在）→ 用 `minimumUnitsSoldT360` |
| `opportunity_score` | （不存在）→ 自己算 |
| `category_id` | `browseNodeId`（amzscope 系列）|
| `categories[]` | `data.items.data[]` |
| `products[].organic_rank` | `results[].rank` |
| `products[].sp_rank` | `results[].sponsored` |
| `negative_reviews_top5` | 不存在 → 用 `get_amazon_reviews filterByStar='critical'` |
| `positive_reviews_top5` | 不存在 → 用 `get_amazon_reviews filterByStar='positive'` |
| `bullet_points` | `features[]` |
| `a_plus_modules` | `productDescription[]` |
| `selling_rank` | `bestSellersRankItems[]` |
| `category_path` | `breadCrumbs` |
| `buy_box_seller` | `seller.name` |
| `search_amazon` 抓 BSR | ❌ → 用 `list_bestsellers` |
| `search_amazon` 抓 New Releases | ❌ → 用 `list_new_releases` |
| `search_amazon` 传 `limit` | ❌ 没有，分页用 `page` |
| `search_amazon_alexa` 传 `marketplaceId` | ❌ 不支持,固定 amz_us;只接受 `prompts: string[]` + 可选 `screenshot` |
| `bsr_category_path` | ❌ 不存在;用 `bestSellersRankItems[]` 数组 + `category_id` 顶层字段 |
| `monthlySoldVolume` | ❌ 不存在;`search_amazon` 用 `sales` 字段(live 月销字符串)|

完整字段对照见 MCP 各 tool 的 `Returns:` 段落，或调 `pangolinfo_capabilities { detail: "full" }`。

## R-11 不要凭直觉判定"做不到"

在告诉用户"这个数据拿不到""这个是付费功能""只能估算"之前,**必须**先调 `pangolinfo_capabilities { detail: "summary" }`(免费,0 积点)或翻看具体 tool 的 description / inputSchema 确认。Pangolinfo MCP 实际能筛/能返回的字段超出大多数 AI 训练时的常识范围,包括但不限于:

- **退货率**: `filter_niches.returnRateT360Max` 筛选 + 返回字段 `returnRateT360` (具体数值)
- **GMV/月销额**: `filter_categories.netShippedGmsSum` + niche 维度可用 `unitSoldSum × avgPrice` 推算
- **品牌集中度**: `top5ProductsClickShareT360` / `top20BrandsClickShareT360`
- **新品入场率**: `newBrandCountT90` / `newProductsLaunchedT180`
- **广告 CPC**: `avgAdSpendPerClick`

**凭直觉先说"做不到"再实际能查到 → 用户直接失去信任**。先查 capabilities,再下结论。

## R-12 通用防呆速查（跨 tool 硬护栏 — 调用前自检）

下面是所有 Pangolinfo MCP tool 的**通用防呆清单**，每条都对应一个真实会被后端拒/扣冤枉积点的坑。调任何 tool 前对照一遍。

### R-12a 参数护栏（传错就被拒 / 扣冤枉积点）

| 坑 | ❌ 错 | ✅ 对 |
|---|---|---|
| 市场码 | `marketplaceId="ATVPDKIKX0DER"`(merchant id) | ISO 站点码 `"US"`/`"UK"`/`"DE"` |
| 邮编跨国 | `amz_jp` + 美国邮编 `10001` | 邮编必须匹配 `site` 国家(amz_us→美国邮编 / amz_jp→日本邮编);不确定就**别传**,后端按国家随机挑 |
| 关键词参数 | `keywords`(复数) | `search_amazon.keyword`(单数,REQUIRED) |
| 分页 | `search_amazon` 传 `limit` | 用 `page`(无 limit 参数) |
| filter 系列 size | `size: 50` | `filter_categories`/`filter_niches` 的 `size`/`page` **后端硬上限 10**(filter_niches 默认 3),超出被截 |
| filter 必填 | `filter_categories` 漏 `timeRange`/`sampleScope` | 二者**必填**(常用 `l7d` + `all_asin`);`filter_niches` 必填 `marketplaceId` |
| filter_niches 入参 | 传 `categoryId` | 只认 `nicheId`/`nicheTitle`;0-1 小数字段(`top5ProductsClickShareT360Max`/`returnRateT360Max`)别传整数 |
| alexa | `search_amazon_alexa` 传 `marketplaceId` | 固定 amz_us,只接受 `prompts: string[]` + 可选 `screenshot`;**强制每次 1 条 prompt**(6 积点/条,60-90s,多条线性叠加可能 >200s) |
| scrape_url | 同时传 / 都不传 `content` 和 `url` | **二选一(互斥)**;筛选/排序/翻页**只能**走 `url` 模式;`parserName` 必须匹配页面类型 |
| wipo_search | `source="USTM"` 查文字商标 / 漏 `source` | `source` 必填;文字商标走 `ai_search`,设计专利用 `source="USID"`;**CNID + `hol`/`prod` 模糊查必须再配 `id`/`rd`/`status`/`lcs` 之一**(否则后端拒全表扫);USID 无 `status` 字段 |
| ai_search | 一次塞 >5 个 followups | `query` 必填(min 1);`followups` ≤5;Fast 档禁 `ai_mode`(30-60s) |
| keyword_trends | 把 0-100 当绝对搜索量 / 传 1 个词 | 那是相对热度;一次 ≤5 词;绝对量去 `filter_niches` |

### R-12b 错误闭环（拿到返回先自检，别盲目往下走）

| 返回情形 | 防呆动作 |
|---|---|
| `results=[]` / `recsList` 空 / niche 0 条 | 空结果**不一定扣积点**但 search 系列扣;按各 SOP 早返(剥词重试 / 放宽筛选 / 换站点),别空手编数据(R-2) |
| 业务码 `9200` "no content"(含 Akamai 挑战) | 归 SERVER/RATE_LIMIT,可重试:等 1-5s 重试**该一个**,降并发到 1;连续 2 次失败跳过本步 |
| `recsList`(bestsellers/new_releases) | 它是 **JSON 字符串数组**,必须**二次 `JSON.parse`**,别当普通数组用 |
| `get_amazon_product` 头部自营品 PDP 退化 | `bestSellersRankItems=[]`+`brand=""`+`category_id=""` → 不阻塞,从 `search_amazon` 的 `title/price/star/rating/sales/badge` 兜底 |
| `twentyFourHourOldSalesRank`/`percentageChange` 空串 | 后端没抓到 24h delta,**不可依赖**,改看 BSR 绝对值 |
| AI Overview 未触发 | SGE 不是每次都有,缺失时降级 organic 结果,别硬编引文 |
| upstream 404 / "url not found" | ASIN/页面失效,告知用户跳过,别重试 |

### R-12c api_key 无效判断（别原地打转）

- key 来源**两套**:skill 侧读 env var `PANGOLINFO_API_KEY`;MCP 侧走 CLI/config/URL(`?api_key=pgl_xxx` 或 `Authorization: Bearer pgl_xxx`)。前缀均 `pgl_`。
- **AUTH 是 terminal**:同 key 重试一定再失败 → **绝不重试**。坑:invalid key 在后端是 bizCode **1004**(不是 HTTP 401),别因"不是 401"误判成 SERVER。
- 处理:停 SOP → 引导用户到 `https://www.pangolinfo.com` 拿 key → 写 env/config → **重启/重连**(不热加载;agent 无法替用户改配置或重连)。详见 R-1 / R-9。

### R-12d 路由防呆（别用错 skill / 用错 tool）

- 单步查询走单 tool,别强跑整 SOP(R-6):查 ASIN→`get_amazon_product`;类目榜→`list_bestsellers`;趋势→`keyword_trends`;差评→`get_amazon_reviews filterByStar=critical`。
- tool 间别越界:要 BSR/新品榜别用 `search_amazon`(用 `list_bestsellers`/`list_new_releases`);要 niche 别用 `filter_categories`(用 `filter_niches`);要具体商品别用 filter 系列(用 `list_category_products`/`search_amazon`)。
- skill 间别越界:选品→`amazon-product-explorer`;日常监控→`amazon-daily-competitor-radar`;写 Listing→`amazon-listing-optimization`;站内抓取→`pangolinfo-amazon-scraper`;Google/SGE→`pangolinfo-ai-serp`;类目利基→`pangolinfo-amazon-niche`。
