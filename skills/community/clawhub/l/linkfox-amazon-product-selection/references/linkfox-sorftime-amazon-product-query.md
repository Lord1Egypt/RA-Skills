---
name: linkfox-sorftime-amazon-product-query
description: 基于Sorftime进行多维度亚马逊产品检索与对比，支持历史快照回看与类目/品牌分析。
---

# Sorftime 亚马逊产品搜索（Sorftime Product Search）

本技能通过 Sorftime 对亚马逊商品进行多维度搜索与筛选，帮助卖家发现商品、分析竞品、探索市场机会。完整参数、响应字段与错误码见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 跨 14 个亚马逊站点（US、GB、DE、FR、IN、CA、JP、ES、IT、MX、AE、AU、BR、SA）进行多维度产品检索。
- 提供 16 种查询类型，支持单条件查询（`queryMode=1`）与多条件且关系组合查询（`queryMode=2`）。
- 支持历史月份快照回看（`queryMonth`，2024 年 1 月至今），用于对比历史价格、排名、销量。
- 返回数据覆盖价格与利润（含 FBA 费用明细）、BSR 排名、月销量/月销售额、评分、上架信息、Buybox 卖家、Listing 特征（A+/视频/品牌店）等。

### ❌ 边界与限制

- **分页上限**：每页最多 100 个商品，最多 200 页。
- **历史回看范围**：2024 年 1 月至今（约 2 年）；US、GB、DE 支持完整回看，其他站点回看仅支持 Top 100 商品，AU、BR、IN 不支持回看。
- **销量预估**：非标准类目商品销量字段可能返回 -1（表示无法预估）。
- **ABA 关键词**：queryType=6 目前仅支持 ABA 关键词，不支持任意搜索词。
- **非结构化数据**：结果不支持通过 `_dataQuery_executeDynamicQuery` 进行二次分析。
- **不在范围内**：单个 ASIN 的详细趋势/历史曲线（用 Sorftime Product Detail 技能）；ABA 搜索词排名数据（用 ABA Data Explorer）；广告/PPC 策略；评论内容分析；专利或商标核查。

## 核心概念

Sorftime 商品搜索提供 16 种查询类型与两种查询模式，可灵活组合，并支持历史月份快照回看。

**查询模式**：
- **单条件查询**（`queryMode=1`）：指定 `queryType`（1-16）与对应格式的 `queryValue`。
- **多条件组合查询**（`queryMode=2`）：通过 `queryValue` 传入 JSON 数组，各条件之间为且（AND）关系。

**关键区分**：本工具用于跨商品搜索与筛选。若需某个 ASIN 的详细趋势数据（销量/价格/BSR 历史），请使用 Sorftime Product Detail 技能。

**支持的站点**：US、GB、DE、FR、IN、CA、JP、ES、IT、MX、AE、AU、BR、SA。默认 `us`。Sorftime 使用小写站点代码，英国为 `gb`（非 `uk`）。

**响应数据覆盖**（完整字段见 `references/api.md`）：基础信息（ASIN、标题、品牌、图片、父 ASIN、变体数、重量、尺寸）；价格与利润（当前价、到手价、划线价、Coupon、FBA 费用明细、平台佣金、利润额与利润率）；销量（月销量、月销售额、日销量、日销售额，-1 表示无法预估）；排名（BSR 大类与小类）；评分；上架信息；Buybox 卖家；Listing 特征（A+、视频、品牌店）。

## 调用方式

- **API 端点**：`POST /sorftime/amazon/productQuery`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sorftime_product_search.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sorftime-amazon-product-query-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 某 ASIN 的竞品**
```
queryMode: 1, queryType: 1, queryValue: B0CVM8TXHP, marketplace: us
```

**2. 浏览某类目热销商品**
```
queryMode: 1, queryType: 2, queryValue: 3743561, marketplace: us
```

**3. 分析某品牌的产品组合**
```
queryMode: 1, queryType: 3, queryValue: Anker, marketplace: us
```

**4. 按 ABA 关键词搜索**
```
queryMode: 1, queryType: 6, queryValue: Power Bank, marketplace: us
```

**5. 发现季节性产品（Q4 高峰）**
```
queryMode: 1, queryType: 10, queryValue: 10,11,12, marketplace: us
```

**6. 历史与当前数据对比**
```
queryMonth: 2024-11, queryMode: 1, queryType: 2, queryValue: 3743561, marketplace: us
-> 与不带 queryMonth 的当前数据对比，查看价格/销量变化
```

**7. 多条件：新品 + 高销量 + FBA**
```
queryMode: 2
queryValue: [{"QueryType":11,"Content":"2024-06-01,"},{"QueryType":9,"Content":"300,"},{"QueryType":15,"Content":"FBA"}]
marketplace: us
```

**8. 查看某卖家的产品组合**
```
queryMode: 1, queryType: 4, queryValue: AnkerDirect, marketplace: us
```

参数格式与各 queryType 取值详见 [references/api.md](references/api.md)。

## 展示规则

1. **只呈现数据**：以清晰表格展示查询结果，不做主观商业建议。
2. **排名说明**：展示排名数据时，提醒用户数值越小排名越靠前。
3. **分页提示**：每页最多 100 个商品，最多 200 页。结果较多时展示重点并提醒可翻页。
4. **销量预估说明**：销量/销售额字段值为 `-1` 表示「无法预估」，应向用户说明而非直接展示 -1。
5. **错误处理**：查询失败时根据 `msg` 字段说明原因，并建议调整查询条件。

## 用户表达与场景速查

**适用** —— 亚马逊商品搜索与筛选：

| 用户说 | 场景 |
|--------|------|
| "找一下这个类目下卖得好的产品" | 类目探索 |
| "Anker 品牌有哪些热销产品" | 品牌分析 |
| "这个 ASIN 的竞品有哪些" | 竞品发现 |
| "帮我找一些季节性产品" | 季节性产品发现 |
| "新品中月销量超过 500 的有哪些" | 多条件筛选 |
| "去年双十一这个类目的价格快照" | 历史快照对比 |
| "这个卖家还卖了什么产品" | 卖家产品组合 |
| "帮我筛选利润率高于 30% 的 FBA 产品" | 利润导向筛选 |
| "月销量 1000 以上，评分 4 星以上的产品" | 多条件筛选 |
| "标题包含 wireless charger 的产品" | 标题关键词搜索 |

不适用场景见上方【能力边界】。

**边界判断**：当用户说「竞品分析」或「市场调研」时，若需要跨维度（类目、品牌、价格区间等）发现并对比商品，适用本技能；若需某个 ASIN 的历史趋势曲线，使用 Sorftime Product Detail 技能；若需关键词搜索量数据，使用 ABA Data Explorer。

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

# Sorftime 亚马逊产品搜索 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/sorftime/amazon/productQuery`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| marketplace | string | 是 | 亚马逊站点代码（小写）：us、gb、de、fr、in、ca、jp、es、it、mx、ae、au、br、sa。其中英国为 `gb`（非 `uk`），默认 `us` |
| queryMode | integer | 否 | 查询方式。`1`：单条件查询（默认）；`2`：多条件组合查询（且关系） |
| queryType | integer | 否 | 查询类型（1-16），仅当 queryMode=1 时生效。详见下方「查询类型」表 |
| queryValue | string | 否 | 查询条件值，格式根据 queryMode 和 queryType 不同而变化。详见下方「查询类型」与「多条件组合」说明 |
| page | integer | 否 | 分页页码，默认 1。每页最多 100 个产品，最多 200 页 |
| queryMonth | string | 否 | 回看历史月份，格式 `yyyy-MM`。不指定时查实时数据 |

### 查询类型（queryType，仅 queryMode=1 时生效）

| queryType | 名称 | queryValue 格式 | 示例 |
|-----------|------|-----------------|------|
| 1 | ASIN 同类 | ASIN | `B0CVM8TXHP` |
| 2 | 类目 | NodeId | `3743561` |
| 3 | 品牌 | 品牌名 | `Anker` |
| 4 | 卖家名称 | 店铺名 | `AnkerDirect` |
| 5 | 卖家ID | SellerId | `A294P4X9EWVXLJ` |
| 6 | ABA 关键词 | 关键词 | `Power Bank` |
| 7 | 标题/属性匹配 | 关键词 | `10,000mAh 30W` |
| 8 | 价格区间 | `min,max`（单位：分） | `1,1000`（=$0.01~$10） |
| 9 | 月销量区间 | `min,max` | `100,1000` |
| 10 | 季节性产品 | 月份列表 | `1,2,3`（1-3 月高峰） |
| 11 | 上架日期区间 | `start,end`（yyyy-MM-dd） | `2024-06-01,2024-12-01` |
| 12 | 评分区间 | `min,max` | `3,5` |
| 13 | 评论数区间 | `min,max` | `10,500` |
| 14 | 排名区间 | `bsr_min,bsr_max;sub_min,sub_max` | `500,5000;1,100` |
| 15 | 发货方式 | `FBA` / `FBM` | `FBA,FBM` |
| 16 | 变体数区间 | `min,max` | `1,50` |

**重要**：queryType=1（ASIN 同类）查找的是与给定 ASIN 相似的产品，而非该 ASIN 本身。查询单个商品详情请使用 Sorftime Product Detail 技能。

**区间格式约定**：省略一端表示开区间——`,1000` 表示「至多 1000」；`100,` 表示「不少于 100」。

**价格单位**：queryType=8（价格区间）使用分（cents）为单位，美元下 $19.99 = `1999`。

**ABA 关键词**：queryType=6 目前仅支持 ABA 关键词，不支持任意搜索词。

### 多条件组合（queryMode=2）

当 `queryMode=2` 时，`queryType` 无效；所有条件通过 `queryValue` 传入 JSON 数组，各条件之间为且（AND）关系：

```json
[{"QueryType":11,"Content":"2024-06-01,"},{"QueryType":8,"Content":"100,500"}]
```

当用户明确要求翻页时，调整 `page` 参数。

### 历史快照（queryMonth）

设置 `queryMonth`（格式 `yyyy-MM`）可查询某历史月份的产品数据快照，用于对比历史价格、排名、销量与当前数据。

- 支持范围：2024 年 1 月至今（约 2 年）
- US、GB、DE 支持完整「不限」回看模式
- 其他站点回看仅支持 Top 100 商品
- AU、BR、IN **不支持**回看

## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| code | integer | 响应码（200 表示成功） |
| msg | string | 响应消息 |
| total | integer | 结果总数 |
| page | integer | 当前页码 |
| pageCount | integer | 总页数（最多 200 页） |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗 Token 数量 |
| requestConsumed | integer | 消耗的请求数 |
| type | string | 渲染的样式 |
| columns | array | 渲染的列 |
| products | array | 产品列表（详见下方） |

### 商品对象字段（products 数组元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN |
| title | string | 商品标题 |
| brand | string | 品牌 |
| asinUrl | string | 商品链接，亚马逊 Listing 详情页 URL |
| imageUrl | string | 主图 URL |
| productImageUrls | array | 主图列表（所有商品图片 URL） |
| parentAsin | string | 父 ASIN，有子体时为父级 ASIN，无子体时为 null |
| variationNum | integer | 变体数 |
| weight | string | 重量，单位 g |
| size | array | 尺寸，外包装 [最长边,第二长边,最短边]，单位 cm |
| price | number | 当前价格，未扣 Coupon，单位为当地货币（如美元） |
| oldPrice | number | 划线价，单位为当地货币（如美元） |
| salesPrice | number | 到手价，扣除 Coupon 后的实际售价，单位为当地货币（如美元） |
| coupon | integer | Coupon 政策。值 >=0 为抵扣金额（如 500=$5），值 <0 为折扣百分比（如 -10=10% 折扣） |
| fbaFees | number | FBA 费用，单位为当地货币（如美元） |
| fbaDetail | array | FBA 明细。首项为配送费，后续为 月份:仓储费，如 `[475,"1-9:5","10-12:15"]` |
| platformFee | number | 平台佣金，单位为当地货币（如美元） |
| profitAmount | number | 利润，到手价-FBA 费-佣金，单位为当地货币（如美元） |
| profitRate | number | 利润率，例 25.83 表示 25.83% |
| monthlySalesUnits | integer | 月销量，近 30 日 Listing 维度不区分子体，推荐用于评估销量，值为 -1 表示无法预估 |
| monthlySalesRevenue | number | 月销售额，预估值，单位为当地货币（如美元），值为 -1 表示无法预估 |
| listingSalesVolumeOfDaily | integer | 日销量，Listing 维度不区分子体，值为 -1 表示无法预估 |
| listingSalesOfDaily | number | 日销售额，单位为当地货币（如美元），值为 -1 表示无法预估 |
| salesRank | integer | BSR 排名，大类排名 |
| category | array | 大类，[大类名称, NodeId] |
| bsrCategory | array | 小类排名列表，每项包含 nodeId（节点 ID）、name（类目名称）、rank（排名）、date（日期，格式 yyyyMMdd） |
| rating | number | 当前评分（0.0-5.0，如 4.8） |
| ratings | integer | 评分数量 |
| availableDate | string | 上架时间，格式 yyyy-MM-dd |
| onlineDays | integer | 上架天数 |
| buyboxSeller | string | Buybox 卖家名称 |
| buyBoxSellerId | string | Buybox 卖家 ID |
| buyboxSellerAddress | string | 卖家所在地，Buybox 卖家国籍（二字码如 CN、US），亚马逊自营时为 null |
| isFBA | boolean | 是否 FBA，Buybox 卖家是否使用 FBA 物流 |
| sellerNum | integer | 卖家数 |
| aPlus | boolean | 有 A+ |
| hasVideo | boolean | 有视频 |
| hasBrandStore | boolean | 有品牌店 |


## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 code 字段区分（code = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errcode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `products` 等业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非 200 值 | 业务异常 | 参考 `msg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

**单条件 - ASIN 同类产品：**

```bash
curl -X POST https://tool-gateway.linkfox.com/sorftime/amazon/productQuery \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "queryMode": 1, "queryType": 1, "queryValue": "B0CVM8TXHP"}'
```

**单条件 - 类目浏览：**

```bash
curl -X POST https://tool-gateway.linkfox.com/sorftime/amazon/productQuery \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "queryMode": 1, "queryType": 2, "queryValue": "3743561"}'
```

**单条件 - 品牌热销产品：**

```bash
curl -X POST https://tool-gateway.linkfox.com/sorftime/amazon/productQuery \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "queryMode": 1, "queryType": 3, "queryValue": "Anker"}'
```

**单条件 - 历史快照回看：**

```bash
curl -X POST https://tool-gateway.linkfox.com/sorftime/amazon/productQuery \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "queryMode": 1, "queryType": 2, "queryValue": "3743561", "queryMonth": "2024-11"}'
```

**多条件组合 - 新品+高销量+FBA：**

```bash
curl -X POST https://tool-gateway.linkfox.com/sorftime/amazon/productQuery \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "queryMode": 2, "queryValue": "[{\"QueryType\":11,\"Content\":\"2024-06-01,\"},{\"QueryType\":9,\"Content\":\"300,\"},{\"QueryType\":15,\"Content\":\"FBA\"}]"}'
```
