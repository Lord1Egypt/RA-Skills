---
name: linkfox-amazon-product-detail
description: 通过 ASIN 获取亚马逊商品的完整详情，包括标题、五点描述、规格参数、价格、变体、A+页面及图片等结构化数据。
---

# 亚马逊-前端商品详情（Amazon Product Detail Lookup）

本技能通过 ASIN 获取亚马逊商品的完整详情，帮助亚马逊卖家与研究人员从商品页面提取结构化数据，覆盖 22 个亚马逊站点。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过 ASIN 获取亚马逊商品页面的结构化详情：标题、主图与附图、五点描述（About This Item）、商品规格、A+ 内容描述、价格、评分分布、变体结构。
- 支持单次最多 40 个 ASIN 批量查询（逗号分隔）。
- 支持 22 个亚马逊站点（美、英、德、法、意、西、日、加、澳、巴、印、荷、瑞典、波兰、新、沙、阿联酋、土耳其、墨、埃及、中、比利时）。
- 可选返回「经常一起购买」「相关商品」「作者评论」数据。

### ❌ 边界与限制

- **按 ASIN 计费**：成本高于搜索类工具，引导用户仅查询真正需要的 ASIN，避免大批量试探性查询。
- **当前快照**：仅返回当前商品页面数据，不含历史价格追踪、销量估算或收入计算。
- **非页面数据**：关键词/搜索词分析（用 ABA 工具）、搜索结果排名、广告/PPC 数据、库存管理与 FBA 费用分析、评论情感 NLP（仅返回原始评论文本）均不在范围内。
- **ASIN 有效性**：查询失败时需检查 ASIN 是否有效、站点域名是否正确。
- 同一会话同一参数组合默认只调用一次；失败/空结果不得自动换关键词、翻页或改邮编连续试探。

## 核心概念

本工具通过前端模拟亚马逊商品页面，提取结构化详情数据，返回商品标题、主图、附图、五点描述、商品规格、A+ 内容描述、价格、评分分布、变体结构，并可选返回「经常一起购买」与「相关商品」数据。

**批量支持**：单次请求最多 40 个 ASIN，以逗号分隔字符串传入。

## 调用方式

- **API 端点**：`POST /amazon/product/detail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/amazon_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-product-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 基础单个 ASIN 查询**
```
查一下美国站 ASIN B072MQ5BRX 的详情。
```
参数：`{"asins": "B072MQ5BRX"}`

**2. 多 ASIN 批量查询**
```
查 B072MQ5BRX 和 B08N5WRWNW 的商品详情。
```
参数：`{"asins": "B072MQ5BRX,B08N5WRWNW"}`

**3. 非美国站查询**
```
查德国站 B09V3KXJPB 的商品信息。
```
参数：`{"asins": "B09V3KXJPB", "amazonDomain": "amazon.de"}`

**4. 含评论与经常一起购买**
```
查日本站 B08N5WRWNW 的完整详情，包含评论和经常一起购买。
```
参数：`{"asins": "B08N5WRWNW", "amazonDomain": "amazon.co.jp", "returnBoughtTogether": true, "returnAuthorsReviews": true}`

**5. 竞品 Listing 对比**
```
对比这 3 个 ASIN 的五点描述和价格：B072MQ5BRX, B08N5WRWNW, B09V3KXJPB。
```
参数：`{"asins": "B072MQ5BRX,B08N5WRWNW,B09V3KXJPB"}`

**6. 移动端商品页检查**
```
看看英国站 B072MQ5BRX 在移动端的展示。
```
参数：`{"asins": "B072MQ5BRX", "amazonDomain": "amazon.co.uk", "device": "mobile"}`

## 展示规则

1. **清晰呈现数据**：用结构化格式展示商品详情——规格与价格对比用表格，五点描述用列表。
2. **图片处理**：响应含图片 URL（`productImageUrls`、`thumbnail`、`imageUrl`）时，按场景以可点击链接或内嵌图片展示。
3. **多 ASIN 结果**：查询多个 ASIN 时，按 ASIN 与标题清晰分隔并标注每个商品。
4. **价格格式**：价格须带币种符号/代码；有折扣时同时展示现价与原价以突出优惠。
5. **评分拆解**：存在 `customerReviews` 数据时，展示星级分布（5 星到 1 星占比）及总评分与评论数。
6. **变体展示**：存在变体时，按变体维度（颜色、尺寸等）分组用紧凑表格展示。
7. **错误处理**：查询失败时说明原因，并建议检查 ASIN 是否有效、站点域名是否正确。
8. **成本提醒**：提示用户本工具按 ASIN 计费，仅批量查询真正需要的 ASIN。

## 用户表达与场景速查

**适用** —— 需要亚马逊商品页面结构化数据的任务：

| 用户说 | 场景 |
|--------|------|
| "查一下这个 ASIN"、"获取……的商品详情" | 单个/批量 ASIN 详情查询 |
| "这个商品的五点描述是什么" | Listing 内容提取 |
| "看看竞品的 Listing" | 多 ASIN 对比 |
| "这个 ASIN 在德国站多少钱" | 跨站点价格查询 |
| "这个商品有多少评论" | 评分与评论分析 |
| "这个商品有哪些变体" | 变体结构查看 |
| "获取 A+ 内容/商品描述" | 商品描述获取 |
| "这个 ASIN 的主图是什么" | 商品图片提取 |
| "这个商品是否支持 Prime" | 资格/徽章检查 |
| "商品规格/尺寸是什么" | 规格查询 |

不适用场景见上方【能力边界】。

**边界判断**：用户说"分析这个商品"或"调研这个 ASIN"时，若本质是获取当前商品页面数据（标题、价格、五点、图片、评论、变体），则适用本技能；若需要历史趋势、销量估算或广告洞察，则不适用。

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

# 亚马逊前端-商品详情 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazon/product/detail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| asins | string | 是 | ASIN列表，支持批量查询，最多40个ASIN。格式：`^[A-Z0-9]+(,[A-Z0-9]+){0,39}$`。示例：`B072MQ5BRX,B08N5WRWNW` |
| amazonDomain | string | 否 | 亚马逊各个国家站点，默认 `amazon.com`。可选值：`amazon.com`、`amazon.co.uk`、`amazon.de`、`amazon.fr`、`amazon.it`、`amazon.es`、`amazon.co.jp`、`amazon.ca`、`amazon.com.au`、`amazon.com.br`、`amazon.in`、`amazon.nl`、`amazon.se`、`amazon.pl`、`amazon.sg`、`amazon.sa`、`amazon.ae`、`amazon.com.tr`、`amazon.com.mx`、`amazon.eg`、`amazon.cn`、`amazon.com.be` |
| language | string | 否 | 语言。示例：`en_US`、`de_DE`、`fr_FR`、`ja_JP`、`it_IT`、`es_ES`、`pt_BR`、`en_GB`、`zh_CN` |
| deliveryZip | string | 否 | 配送邮编，用于获取配送相关定价。示例：`10001`（美国纽约）、`10115`（德国柏林）、`EC1A 1BB`（英国伦敦） |
| device | string | 否 | 设备类型：`desktop`（默认）、`mobile`、`tablet` |
| returnBoughtTogether | boolean | 否 | 是否返回经常一起购买的商品（boughtTogether），默认 `false` |
| returnRelatedProducts | boolean | 否 | 是否返回相关商品列表（relatedProducts），默认 `false` |
| returnAuthorsReviews | boolean | 否 | 是否返回作者评论列表（authorsReviews），默认 `false` |

## 响应结构

顶层字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总行数 |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |
| products | array | 产品列表（详见下方） |

### 产品对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN编码 |
| title | string | 商品标题 |
| brand | string | 品牌 |
| price | number | 价格 |
| extractedPrice | number | 提取的价格 |
| oldPrice | number | 原价 |
| extractedOldPrice | number | 提取的原价 |
| currency | string | 币种 |
| discount | string | 折扣 |
| saveWithCoupon | string | 优惠券节省金额 |
| rating | number | 评分 |
| ratings | integer | 评论数 |
| prime | boolean | 是否Prime商品 |
| stock | string | 库存状态 |
| delivery | string | 配送信息 |
| link | string | 商品链接 |
| linkClean | string | 纯净链接 |
| asinUrl | string | 链接 |
| imageUrl | string | 缩略图 |
| thumbnail | string | 缩略图 |
| productImageUrls | array | 商品图片链接列表 |
| aboutItem | array | 五点描述 |
| productDescription | string | 商品描述列表 |
| description | string | 商品描述 |
| dimension | string | 商品尺寸 |
| weight | string | 重量 |
| tags | string | 标签列表 |
| badges | string | 徽章列表 |
| climatePledgeFriendly | boolean | 是否气候友好 |
| snapEbtEligible | boolean | 是否支持SNAP EBT |
| boughtLastMonth | string | 上月购买数（字符串） |
| boughtLastMonthCount | integer | 上月购买数（数字） |
| reviewsSummary | string | 评论摘要 |
| reviewsImages | array | 评论图片列表 |
| sourceTool | string | 来源工具 |
| sourceType | string | 来源类型：amazon |
| pageFileUrl | string | 完整页面文件url |

### 嵌套对象

**productDetails** -- 商品详细规格信息：

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN编码 |
| manufacturer | string | 制造商 |
| productDimensions | string | 商品尺寸 |
| upc | string | UPC编码 |
| units | string | 单位 |
| rating | number | 评分 |
| review | integer | 评论数 |

**customerReviews** -- 星级评分分布：

| 字段 | 类型 | 说明 |
|------|------|------|
| fiveStar | integer | 五星评论数 |
| fourStar | integer | 四星评论数 |
| threeStar | integer | 三星评论数 |
| twoStar | integer | 二星评论数 |
| oneStar | integer | 一星评论数 |

**variants** -- 商品变体列表（数组）：

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 变体标题（如颜色、尺寸） |
| items | array | 变体项列表，每项包含 `name`（名称）、`asin`（ASIN编码）、`position`（位置）、`selected`（是否已选择） |

**itemSpecifications** -- 商品规格（动态键值）。

**itemIngredients** -- 商品成分列表（数组）。

**reviewsImages** -- 评论图片列表（数组）。

### 可选嵌套数组（按需返回）

**boughtTogether**（当 `returnBoughtTogether: true` 时返回）：

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN编码 |
| title | string | 标题 |
| price | string | 价格 |
| extractedPrice | number | 提取的价格 |
| priceUnit | string | 单价 |
| extractedPriceUnit | number | 提取的单价 |
| thumbnail | string | 缩略图 |
| link | string | 链接 |
| linkClean | string | 纯净链接 |
| stock | string | 库存状态 |
| delivery | array | 配送信息 |
| position | integer | 位置 |

**relatedProducts**（当 `returnRelatedProducts: true` 时返回）：

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN编码 |
| title | string | 标题 |
| price | string | 价格 |
| extractedPrice | number | 提取的价格 |
| oldPrice | string | 原价 |
| extractedOldPrice | number | 提取的原价 |
| priceUnit | string | 单价 |
| extractedPriceUnit | number | 提取的单价 |
| rating | number | 评分 |
| reviews | integer | 评论数 |
| thumbnail | string | 缩略图 |
| link | string | 链接 |
| linkClean | string | 纯净链接 |
| prime | boolean | 是否Prime商品 |
| sponsored | boolean | 是否赞助商品 |
| climatePledgeFriendly | boolean | 是否气候友好 |
| discount | string | 折扣 |
| badges | array | 徽章列表 |
| position | integer | 位置 |

**authorsReviews**（当 `returnAuthorsReviews: true` 时返回）：

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 标题 |
| text | string | 评论内容 |
| author | string | 作者 |
| authorImage | string | 作者头像 |
| authorLink | string | 作者链接 |
| rating | integer | 评分 |
| date | string | 日期 |
| verifiedPurchase | boolean | 是否已验证购买 |
| helpfulVotes | string | 有用投票数 |
| productSize | string | 商品尺寸 |
| productFlavorName | string | 商品口味名称 |
| position | integer | 位置 |

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
curl -X POST https://tool-gateway.linkfox.com/amazon/product/detail \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asins": "B072MQ5BRX,B08N5WRWNW", "amazonDomain": "amazon.com"}'
```

### 包含可选参数

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/product/detail \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "asins": "B072MQ5BRX",
    "amazonDomain": "amazon.de",
    "language": "de_DE",
    "deliveryZip": "10115",
    "returnBoughtTogether": true,
    "returnAuthorsReviews": true
  }'
```
