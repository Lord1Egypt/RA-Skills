---
name: linkfox-keepa-product-request
description: 通过Keepa获取亚马逊商品结构化详情，包括基本属性、价格、FBA费用、变体销量及近12个月的月销趋势。
---

# Keepa 商品详情（Keepa Product Request）

本技能通过 Keepa 商品请求 API 获取亚马逊商品结构化详情，帮助亚马逊卖家与分析师针对一个或多个 ASIN、跨多个亚马逊站点获取结构化商品数据。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过 Keepa 获取一个或多个亚马逊 ASIN 的结构化商品详情，覆盖价格、标题、主图、上架日期、材质、重量、尺寸、销售排名、月销量（含近12个月历史）、FBA费用、评分、评论数、类目树等。
- 支持单 ASIN 查询与批量查询（最多 5 个 ASIN），覆盖美/英/德/法/日/加/意/西/印/墨/巴等多个亚马逊站点。
- 支持返回历史销量趋势数据（近12个月月销量、30/90/180天平均销售排名）。

### ❌ 边界与限制

- **不含商品描述与评论内容**：API 不返回商品描述文本或评论内容。
- **单次最多 5 个 ASIN**：批量查询上限 5 个，`asin` 参数最大长度 300 字符。
- **历史数据可选**：月销量历史仅在 `history` 设为 `1` 时返回。
- **数据时效**：`lastUpdate` 字段标识商品数据最后刷新时间。
- **不在范围内**：关键词/搜索词分析（用 ABA 数据工具）；广告/PPC 数据；卖家账号或店铺级分析；无明确 ASIN 的选品调研（如"找厨房类目趋势商品"）；价格历史曲线或 Buy Box 历史走势（仅返回当前与平均排名数据）。
- **边界判断**：用户说"选品调研"或"竞品分析"时，若持有具体 ASIN 且想要结构化商品数据（价格、销量、尺寸、类目），适用本技能；若需要关键词级分析、无 ASIN 的市场趋势或广告指标，不适用。

## 核心概念

Keepa Product Request API 经由 Keepa 返回亚马逊商品详情数据。给定一个或多个 ASIN 与站点，返回价格、标题、主图、上架日期、材质、重量、尺寸、销售排名、月销量（当前及近12个月历史）、FBA费用、评分、评论数、类目树等信息。

**关键要点**：
- 单次请求最多查询 **5 个 ASIN**，用英文逗号分隔。
- `domain` 参数为数字站点 ID（如 `1` = Amazon.com 美国站），不是国家代码。
- `history` 设为 `1` 时包含历史销量数据（近12个月月销量、30/90/180天平均销售排名）；设为 `0` 仅返回当前商品信息。
- 响应**不包含**商品描述或评论内容。

## 调用方式

- **API 端点**：`POST /keepa/productRequest`（完整参数/响应/错误码见 [references/api.md](references/api.md)）
- **Python 脚本**：`python scripts/keepa_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-keepa-product-request-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 单 ASIN 查询（美国站，基础信息）**
```json
{"asin": "B0088PUEPK", "domain": "1"}
```

**2. 单 ASIN 含历史销量数据**
```json
{"asin": "B0088PUEPK", "domain": "1", "history": 1}
```

**3. 批量查询多个 ASIN（德国站）**
```json
{"asin": "B0088PUEPK,B00U26V4VQ,B07M68S376", "domain": "3", "history": 1}
```

**4. 日本站商品查询**
```json
{"asin": "B09V3KXJPB", "domain": "5", "history": 0}
```

**5. 多 ASIN 竞品对比（美国站，含销量历史）**
```json
{"asin": "B0CXYZ1234,B0CXYZ5678,B0CXYZ9012,B0CXYZABCD", "domain": "1", "history": 1}
```

## 展示规则

1. **清晰呈现数据**：以结构良好的表格展示商品详情，相关字段分组（如尺寸归组、销量数据归组）便于阅读。
2. **价格与币种**：始终同时显示价格与币种（如 "$29.99 USD"）。响应中的 `currency` 字段标明本地币种。
3. **销量趋势**：含历史数据时，以表格呈现12个月销量趋势，或描述走势（上升/下降/平稳），帮助用户快速判断动量。
4. **尺寸与重量**：适时将毫米换算为更直观的单位（如同时展示 mm 与英寸，或 mm 与 cm）。注意重量单位为克。
5. **不可用数据**：值为 `0` 或 `-1` 的字段表示数据不可用，不要作为实际测量值展示，标注"N/A"或省略。
6. **图片展示**：返回 `imageUrl` 时展示商品图片，便于直观识别。
7. **错误处理**：查询失败时根据响应说明原因并建议修正（如 ASIN 格式无效、站点不支持）。
8. **批量结果**：批量查询多个 ASIN 时，先展示汇总表，再按需提供个别商品详情。

## 用户表达与场景速查

**适用** —— 按 ASIN 获取商品数据：

| 用户说 | 场景 |
|--------|------|
| "查一下这个 ASIN"、"获取 B0XXXXXXXX 的商品详情" | 单 ASIN 查询 |
| "这个亚马逊商品多少钱" | 价格查询 |
| "这个商品每月卖多少件" | 月销量查询 |
| "对比这几个 ASIN"、"批量查这些商品" | 多 ASIN 对比 |
| "看下这个 ASIN 的销量趋势" | 历史销量分析 |
| "这个商品属于什么类目" | 类目/分类查询 |
| "商品尺寸"、"有多重" | 规格查询 |
| "这个商品的 FBA 费用" | 费用估算 |
| "这个商品什么时候上架的"、"上架日期" | 上架时间查询 |
| "这个商品是 FBA 还是 FBM" | 配送方式查询 |

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

# Keepa-亚马逊-商品详情 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/keepa/productRequest`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| asin | string | 是 | 亚马逊标准识别号(ASIN)，多个ASIN用英文逗号分隔，最多5个，最大长度300字符。示例：`B0088PUEPK` 或 `B0088PUEPK,B00U26V4VQ,B07M68S376` |
| domain | string | 是 | 亚马逊域名ID。可选值：`1`（美国）、`2`（英国）、`3`（德国）、`4`（法国）、`5`（日本）、`6`（加拿大）、`8`（意大利）、`9`（西班牙）、`10`（印度）、`11`（墨西哥）、`12`（巴西） |
| history | integer | 否 | 返回值是否包含历史数据、历史销量。`1` = 包含价格历史、销售排名、历史销量等时间序列数据（前几个月的销量），`0` = 仅返回基本商品信息。默认：`0` |


## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总行数 |
| perPage | integer | 每页数量 |
| sourceType | string | 来源类型：keepa |
| columns | array | 渲染的列 |
| costToken | integer | 消耗token |
| totalCount | integer | 总数量 |
| currentPage | integer | 当前页码 |
| type | string | 渲染的样式 |
| products | array | 商品列表（详见下方） |

### 商品对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN |
| title | string | 商品标题 |
| brand | string | 品牌 |
| manufacturer | string | 制造商 |
| model | string | 型号 |
| color | string | 颜色 |
| material | string | 产品的材质，指其构造中使用的主要材料 |
| price | number | 当前价格（单位：元，如美元/欧元等） |
| primePrice | number | prime价格 |
| currency | string | 币种 |
| rating | number | 当前评分（0.0-5.0，如4.5星） |
| ratings | integer | 评分数量 |
| reviewCount | integer | 评论数量 |
| salesRank | integer | 销售排名 |
| salesRank30 | integer | 近30天平均销售排名 |
| salesRank90 | integer | 近90天平均销售排名 |
| salesRank180 | integer | 近180天平均销售排名 |
| monthlySalesUnits | integer | 月销量 |
| monthlySalesRevenue | number | 月销售额 |
| monthlySalesUnits1MonthAgo | integer | 1月前月销量 |
| monthlySalesUnits2MonthsAgo | integer | 2月前月销量 |
| monthlySalesUnits3MonthsAgo | integer | 3月前月销量 |
| monthlySalesUnits4MonthsAgo | integer | 4月前月销量 |
| monthlySalesUnits5MonthsAgo | integer | 5月前月销量 |
| monthlySalesUnits6MonthsAgo | integer | 6月前月销量 |
| monthlySalesUnits7MonthsAgo | integer | 7月前月销量 |
| monthlySalesUnits8MonthsAgo | integer | 8月前月销量 |
| monthlySalesUnits9MonthsAgo | integer | 9月前月销量 |
| monthlySalesUnits10MonthsAgo | integer | 10月前月销量 |
| monthlySalesUnits11MonthsAgo | integer | 11月前月销量 |
| monthlySalesUnits12MonthsAgo | integer | 12月前月销量 |
| availableDate | string | 上架时间（yyyy-MM-dd HH:mm:ss） |
| lastUpdate | string | 最后更新时间（yyyy-MM-dd HH:mm:ss） |
| imageUrl | string | 图片URL（请求地址） |
| productImageUrls | array | 商品图片列表 |
| asinUrl | string | 亚马逊asin的详情网址 |
| urlSlug | string | URL Slug |
| itemLength | integer | 商品长度，单位为毫米，不可用时为0或-1 |
| itemWidth | integer | 商品宽度，单位为毫米，不可用时为0或-1 |
| itemHeight | integer | 商品高度，单位为毫米，不可用时为0或-1 |
| dimension | string | 尺寸 |
| dimensionsType | string | 尺寸类型 |
| weight | string | 重量（克） |
| packageLength | integer | 包装长度（毫米） |
| packageWidth | integer | 包装宽度（毫米） |
| packageHeight | integer | 包装高度（毫米） |
| packageWeight | string | 包装重量（克） |
| packageDimensions | string | 包装尺寸 |
| packageQuantity | integer | 包装中商品的数量，不可用时为0或-1 |
| fulfillment | string | 配送方式(AMZ,FBA,FBM) |
| fbaFees | number | FBA配送费（单位：元） |
| referralFeePercentage | number | 推荐费百分比 |
| profit | number | 利润率（百分比，如25.5表示25.5%） |
| buyBoxSellerId | string | 购买按钮卖家ID |
| sellerNum | integer | 卖家数 |
| variationNum | integer | 变体数量 |
| parentAsin | string | 父ASIN |
| rootCategory | integer | 根类目ID |
| categoryTree | string | 类目树 |
| categoryTreeId | string | 类目树Id |
| subcategories | array | 子类目列表，每个元素包含 `code`（类目ID）、`rank`（排名）、`label`（类目名称） |
| isAdultProduct | boolean | 是否为成人产品 |
| isHazmat | boolean | 是否为危险品 |
| sourceType | string | 来源类型：keepa |
| sourceTool | string | 来源工具 |

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
curl -X POST https://tool-gateway.linkfox.com/keepa/productRequest \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0088PUEPK", "domain": "1", "history": 1}'
```

### 批量查询示例

```bash
curl -X POST https://tool-gateway.linkfox.com/keepa/productRequest \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0088PUEPK,B00U26V4VQ,B07M68S376", "domain": "1", "history": 0}'
```
