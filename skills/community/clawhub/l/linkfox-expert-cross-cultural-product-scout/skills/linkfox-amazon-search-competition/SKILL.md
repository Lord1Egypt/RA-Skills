---
name: linkfox-amazon-search-competition
description: 亚马逊前台搜索首页或前3页自然结果竞争分析。用 linkfox-amazon-search 拉默认排序结果，去广告后重算 organic_rank；固定输出：6段格局（页流量/自然位集中度/价格/评分数/评分/是否含变体）+ 新品清单 + 类目上下文画像（标题vs主图关注点）+ 每条ASIN的title/image结构化增强 + JSON与动态对比表双交付。触发：前台搜索竞争分析、首页商品分析、前3页分析、搜索结果竞争格局、6段竞争分析、自然位集中度、竞品对比表、标题同质化、主图形态、偏题ASIN、SERP competitive landscape。唯一工具依赖 linkfox-amazon-search（分析前3页时3次调用共45积分；仅首页时1次15积分）。
---

# 亚马逊前台搜索竞争分析

输入一个关键词，用 `linkfox-amazon-search` 搜默认相关性排序的 **首页或前 3 页**，去广告并重算自然位后，**固定跑完整链路**（数据源相同，不再拆路由）：

1. **6 段格局** + **新品清单**
2. **类目上下文画像**（买家看标题 vs 主图各关心什么）
3. **每条 ASIN 增强**（title / imageUrl 结构化 + 对比维取值）
4. **双交付**：HTML 报告 + 增强 JSON / 动态对比表

> **重要**：已按接口实测能力收敛。不依赖 brand / fulfillment / sellerNation / availableDate。

## 核心特点

- **单一工具依赖**：只调 `linkfox-amazon-search`，无其他数据源
- **一套流程做完**：结构指标（价量位次）与供给表达（标题/主图/形态/偏题）同源一次算清
- **自然位重算**：`position` 为页内相对名次；按 page 顺序去广告后连续编号 `organic_rank`
- **月销缺失规则**：`monthlySalesUnits` 缺失记为 50；revenue 缺失用 `50 × extractedPrice` 估算
- **广告过滤**：分析基于自然结果，不含 `sponsored: true`
- **标题/主图必做**：按类目生成 context_profile，增强每个 ASIN，输出代码 + 表格

## 参数概览

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| keyword | string | 是 | 搜索关键词（需翻译为目标站点语言） | - |
| amazonDomain | string | 是 | 亚马逊站点域名（如 amazon.com） | - |
| language | string | 否 | 语言代码 | 按 amazonDomain 推断 |

**站点映射**：amazon.com→en_US，amazon.co.uk→en_GB，amazon.de→de_DE，amazon.fr→fr_FR，amazon.it→it_IT，amazon.es→es_ES，amazon.co.jp→ja_JP，amazon.ca→en_CA。

用户未指定站点时，用 `AskUserQuestion` 询问。

## 工作流程（固定全流程，不拆路由）

用户分析「首页」或「前三页」商品时，**以下步骤全部执行**。仅首页则只调 page=1；前三页则并行 1–3 页。

### Step 1 — 拉前台搜索

`sort: "relevanceblender"`。前 3 页示例（并行，各 15 积分）：

```json
{"keyword": "<关键词>", "amazonDomain": "<域名>", "language": "<语言>", "sort": "relevanceblender", "page": 1}
{"keyword": "<关键词>", "amazonDomain": "<域名>", "language": "<语言>", "sort": "relevanceblender", "page": 2}
{"keyword": "<关键词>", "amazonDomain": "<域名>", "language": "<语言>", "sort": "relevanceblender", "page": 3}
```

**必须保留每次请求的 page 号**，禁止用 position 反推页码。用户已提供 SERP JSON 时可跳过本步。

### Step 2 — 合并、去广告、重算 organic_rank

**禁止** `pos > 20 → 第2页` 等启发式（每页条数不固定，实测 16/22/52/60 均出现过）。

1. 按 page = 1 → 2 → 3 顺序处理  
2. 每页内按 `position` 升序  
3. 跳过 `sponsored == true`  
4. 连续编号 `organic_rank = 1, 2, 3, …`  
5. 按 ASIN 去重，保留 `organic_rank` 最小的一条  
6. 写入合并 JSON，每条至少含：

```text
asin, title, extractedPrice, price, rating, ratings,
monthlySalesUnits, monthlySalesRevenue, options,
imageUrl, asinUrl, sponsored, page, page_position, organic_rank,
units_imputed（bool，缺失销量是否按50估算）
```

### Step 3 — 类目上下文画像 + ASIN 增强（与 6 段同源，必做）

数据已在 Step 2，直接：

1. 用 keyword + 样本标题（可选主图）生成 **context_profile**（见下文「上下文画像」）  
2. 为每条 ASIN 追加 **enrichment**（title_extract / image_extract / compare_values / off_topic）  
3. `imageUrl_large`：去掉 `._AC_UL320_` / `._AC_UY218_` 等 CDN 尺寸后缀；失败回退缩略图  
4. 无证据字段填 `null`，禁止幻觉  

### Step 4 — 运行 6 段聚合脚本

```bash
python scripts/aggregate_competition.py <merged_products.json>
python scripts/aggregate_competition.py <merged_products.json> --fixed-buckets
python scripts/aggregate_competition.py <merged_products.json> --buckets <buckets.json>
python scripts/aggregate_competition.py <merged_products.json> --inline
```

分桶优先级：`--buckets` > `--fixed-buckets` > 默认动态分桶（价格 / 评分数 / 评分值）。

### Step 5 — 交付（HTML + 代码 + 表格）

同一份结果出三种形态：

| 交付 | 内容 |
|------|------|
| **HTML 报告** | Header → 上下文画像摘要 → 6 段图表 → 新品清单 → 边界说明（chart-templates + inject_report） |
| **代码 JSON** | `meta` + `context_profile` + `products[].enrichment`（schema 见 schemas/） |
| **对比表** | 一行一 ASIN；列 = 身份字段 + **comparison_dimensions 动态列** + off_topic + title |

报告结构建议：

1. Header：关键词、站点、快照时间、样本说明（首页或前3页）  
2. 上下文画像：本类目标题/主图关注点与对比轴  
3. 6 段分析  
4. 动态对比表（或链到表文件）  
5. 附录：新品清单  
6. Footer + 数据边界  

## 6 段定义

| # | 名称 | 字段 | 图表 | 口径 | 商业含义 |
|---|------|------|------|------|----------|
| 1 | 页流量占比 | page, units, revenue | 表/柱 | 按真实 page 汇总销量与销额占比 | 首页是否垄断流量 |
| 2 | 自然位集中度 | organic_rank, units | 帕累托 | Top10 / 11-20 / 21-48 / 49+ 销量占比与累计 | 头部垄断还是长尾分散 |
| 3 | 价格分布 | extractedPrice, units | 柱+线双Y | 价带商品数占比 + 销量占比；附销量加权均价 | 货与量是否落在同一价带 |
| 4 | 评分数分布 | ratings, units | 柱+线双Y | 评分数分带的商品数与销量占比 | 评论门槛 |
| 5 | 评分分布 | rating, units | 柱+线双Y | 评分分带的商品数与销量占比 | 星级是否拉开差距 |
| 6 | 是否含变体 | options | 纯 KPI | options 非空视为含变体；商品数占比，可选销量占比 | 多变体链接占比（非复杂度） |

### 附录：新品清单（代理）

- **筛选**：自然结果中 `ratings < 100`（无 ratings 不进入）
- **排序**：`organic_rank` 升序
- **字段**：organic_rank, asin, price, rating, ratings, units（标记是否估算）, has_variant
- **说明**：数据源无上架时间，以低评分数作新品代理，可能含老品低评论链接

## 上下文画像与 ASIN 增强（主流程一部分）

买家下单前在标题与主图上的关注点，通常也是卖家会强化的点，直接作为对比轴。Schema / 样例：[`schemas/serp-context-comparison.schema.json`](schemas/serp-context-comparison.schema.json)、[`examples/`](examples/)。

### Context profile（词级，每个 keyword 一份）

| 字段 | 含义 |
|------|------|
| `category_type` | parametric_electronics / apparel_functional / seasonal_decor / customizable / tool_accessory / other |
| `purchase_intent` | 一句话：用户为什么搜这个词 |
| `title_priorities[]` | 标题侧关注信号（weight 1–5） |
| `image_priorities[]` | 主图侧关注信号（weight 1–5） |
| `seller_likely_emphasize[]` | 卖家标题会堆的词 |
| `comparison_dimensions[]` | ≤8 维，`source` = title \| image \| both \| serp_field |
| `off_topic_risks[]` | 易混入的偏题形态 |

**经验法则**：可量化、可搜索 → 标题；外观、真形态、「是不是这类货」→ 主图。

| 类目 | 标题更关注 | 主图更关注 |
|------|------------|------------|
| 便携显示器 | 尺寸、分辨率、接口、刷新率、兼容设备 | 独立副屏 vs 夹式三屏、角标、支架/皮套 |
| 庭院旗 | 12×18、双面、节日/欢迎、套装 | 庭院旗 vs 手持小旗/旗杆、图案 |
| 功能服饰 | 内置短裤/胸垫、口袋、场景词 | 上身版型、是否偏题休闲款 |

### enrichment（挂在每条 ASIN 后，不覆盖原字段）

```text
enrichment:
  off_topic: bool
  units_imputed: bool
  title_extract: { brand, size, features, occasions, motif, ports, ... }
  image_extract: { product_form, title_image_match, on_image_claims, ... }
  compare_values: { ... 仅 comparison_dimensions 中的 dim ... }
```

- 6 段看价量位次；画像+增强看同质化、形态、偏题  
- 高权重维同质化高 → 结论中提示需差异化  
- `off_topic=true` 仍保留在表中可筛，不计入本品形态需求

## 字段可用性（按实测）



**稳定可用**：asin, title, extractedPrice/price, rating, ratings, sponsored, position, currency, asinUrl, imageUrl；monthlySalesUnits/Revenue 约 60%–90% 有值。

**禁止依赖（长期为空）**：brand, fulfillment, sellerNation, availableDate, dimension, weight, tags, priceUnit。

**特殊**：

- `position`：页内相对名次，不是全局 rank
- `monthlySalesRevenue`：字符串，需 safe_float
- `options`：多为 `"See options"`，仅作有/无变体二值
- `delivery` / `badges` / `offers`：有则可用，不保证

## 展示规则

- 所有位次分析使用 `organic_rank`，不用原始 `position` 跨页排序
- 帕累托累计占比单调递增，右 Y 轴最大 100%
- 分布图：柱=商品数，线=销量占比%
- 数字千分位，百分比 1 位小数
- 色板：`['#4f46e5','#06b6d4','#8b5cf6','#f59e0b','#10b981','#ef4444','#ec4899','#6366f1']`

## 报告必须披露的边界

- 样本 = 默认排序前 3 页自然结果（已去广告）
- 自然位次 = 按页序去广告后连续编号，**非**亚马逊官方 rank / BSR
- 月销缺失按 50 件计；销额缺失按 50×现价估算；注明原始销量覆盖率
- 是否含变体仅依据接口是否返回 options；未返回不代表一定无变体
- 每页条数不固定；新品清单为评分数&lt;100 的代理口径

## 限制

- 每次 3 页，45 积分
- 每页条数不固定，过滤广告后自然结果数量随词变化
- 实时前台快照，非历史聚合
- 无品牌 / 履约 / 属地 / 上架时间分析能力

## 适用与不适用

**适用**：关键词首页或前 3 页自然竞争结构；定价带与销量是否错位；自然位集中度；低评论新品扫描；标题/主图同质化与偏题形态；按类目对齐的 ASIN 对比表（JSON + 表）。

**不适用**：品牌份额、FBA 结构、卖家国家、上架趋势、官方 rank/BSR、全类目份额 → 换其它数据源 skill。
