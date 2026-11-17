---
name: linkfox-amazon-search
description: 模拟亚马逊前台搜索，实时抓取关键词搜索结果页（SERP）数据，用于查询商品排名、价格对比和竞品监控。
---

# 亚马逊前端商品搜索（Amazon Product Search）

本技能模拟真实用户在亚马逊前台搜索，实时抓取关键词搜索结果页（SERP）数据，包括商品排位、价格、评分、评论数、品牌、配送信息、广告标识等。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 模拟亚马逊前台搜索，获取实时的搜索结果页（SERP）数据：商品列表及其排位、价格、评分、评论数、品牌、配送信息、广告标识等。
- 支持多站点（amazon.com、amazon.de、amazon.co.jp 等）、多设备（desktop/mobile/tablet）、类目范围、邮编模拟、多语言。
- 适用于竞品发现、关键词排位查询、价格对比、广告商品分析、新品监控。

### ❌ 边界与限制

- **仅实时数据**：返回的是当前真实搜索结果，非历史聚合数据。历史搜索词分析、搜索量趋势请用 ABA 数据。
- **关键词语言**：关键词须用目标站点对应语言（amazon.com 用英语、amazon.de 用德语、amazon.co.jp 用日语等）。
- **每页约 20 条**：每次请求返回约 20 个商品列表。
- **调用频率**：每次调用即模拟一次真实搜索请求，避免密集连续调用。
- **不在范围内**：广告投放管理与出价优化；评论分析与情感分析；销量预估与营收分析；Listing 优化与文案建议；库存与供应链数据。

## 核心概念

本工具模拟真实用户在亚马逊前台搜索，返回实时的搜索结果页（SERP）数据：商品列表及其排位、价格、评分、评论数、品牌、配送信息、广告标识等。这是直接来自亚马逊前端的**实时**数据，而非历史分析。

**与 ABA 数据的区别**：ABA 数据是聚合的历史搜索词分析；本工具返回的是用户此刻在亚马逊上搜索某关键词时实际看到的商品列表。

**关键词语言**：关键词须用目标站点对应语言。例如 amazon.com 用英语，amazon.de 用德语，amazon.co.jp 用日语。

## 调用方式

- **API 端点**：`POST /amazon/search`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/amazon_search.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-search-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 美国站基础关键词搜索**
> "搜一下亚马逊上 wireless earbuds"
```json
{"keyword": "wireless earbuds", "amazonDomain": "amazon.com"}
```

**2. 德国站德语关键词搜索**
> "在德国站搜 kabellose Kopfhörer"
```json
{"keyword": "kabellose Kopfhoerer", "amazonDomain": "amazon.de", "language": "de_DE"}
```

**3. 按价格从低到高排序**
> "亚马逊上 phone case 按价格从低到高排"
```json
{"keyword": "phone case", "amazonDomain": "amazon.com", "sort": "price-asc-rank"}
```

**4. 查某类目下的畅销商品**
> "亚马逊上 yoga mat 的畅销商品有哪些？"
```json
{"keyword": "yoga mat", "amazonDomain": "amazon.com", "sort": "exact-aware-popularity-rank"}
```

**5. 日本站最新上架**
> "日本站 USB充電器 最新上架的商品"
```json
{"keyword": "USB充電器", "amazonDomain": "amazon.co.jp", "language": "ja_JP", "sort": "date-desc-rank"}
```

**6. 多页搜索分析更深结果**
> "laptop stand 第二页结果"
```json
{"keyword": "laptop stand", "amazonDomain": "amazon.com", "page": 2}
```

**7. 移动端搜索模拟**
> "running shoes 在手机端的亚马逊搜索结果"
```json
{"keyword": "running shoes", "amazonDomain": "amazon.com", "device": "mobile"}
```

**8. 类目范围并指定配送邮编**
> "office chair 配送到纽约 10001 的搜索结果"
```json
{"keyword": "office chair", "amazonDomain": "amazon.com", "deliveryZip": "10001"}
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示搜索结果关键字段——排位、ASIN、标题、价格、评分、评论数、品牌。
2. **突出广告商品**：明确标注哪些是赞助商广告结果，哪些是自然结果。
3. **价格格式**：按站点币种显示价格，带正确货币符号。
4. **排位语境**：提醒用户排位反映的是搜索结果页上的实际排名。
5. **分页提示**：结果跨多页时告知总条数，并建议按需继续翻页。
6. **错误处理**：查询失败时根据错误响应说明原因，并建议调整参数。
7. **图片链接**：如有图片 URL，可提及但不内联渲染，除非用户要求。

## 用户表达与场景速查

**适用** —— 实时亚马逊搜索结果查询：

| 用户说 | 场景 |
|--------|------|
| "在亚马逊上搜 XX" | 基础商品搜索 |
| "关键词 XX 下会出现哪些商品" | 关键词 SERP 分析 |
| "我的 ASIN 在 XX 关键词下排第几" | 排位/排名查询 |
| "看看 XX 关键词的顶部结果" | 竞争格局 |
| "XX 的价格区间是多少" | 价格对比 |
| "XX 关键词下有赞助商商品吗" | 广告商品分析 |
| "XX 关键词的新品" | 新品监控 |
| "在亚马逊德国/日本/英国站搜 XX" | 跨站点搜索 |
| "XX 关键词下哪些是畅销品" | 畅销品发现 |
| "对比移动端和 PC 端搜索结果" | 设备差异 SERP |

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

# 亚马逊前端搜索模拟 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazon/search`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 否 | 关键词；请尽量翻译为对应国家的语言，比如美国用英语关键词，德国用德语关键词等等（最大长度1024） |
| amazonDomain | string | 否 | 亚马逊各个国家站点，默认 `amazon.com` |
| node | string | 否 | 亚马逊类目节点（最大长度1000） |
| language | string | 否 | 语言区域代码，如 en_US、de_DE、ja_JP、fr_FR（最大长度1000） |
| sort | string | 否 | 排序方式：`relevanceblender`（精选，默认）、`price-asc-rank`（价格从低到高）、`price-desc-rank`（价格从高到低）、`review-rank`（平均客户评价）、`date-desc-rank`（最新到货）、`exact-aware-popularity-rank`（畅销商品） |
| page | integer | 否 | 页码（从1开始，每页大概20条），默认 `1` |
| deliveryZip | string | 否 | 配送地邮编，用于模拟亚马逊前台地址，建议使用目标国家主要城市的常用邮编，如美国站常用纽约邮编 10001（最大长度1000） |
| device | string | 否 | 设备类型：`desktop`、`mobile`、`tablet`，默认 `desktop`（最大长度1000） |

### 支持的 amazonDomain 值

| 域名 | 国家 |
|------|------|
| amazon.com | 美国 |
| amazon.co.uk | 英国 |
| amazon.de | 德国 |
| amazon.fr | 法国 |
| amazon.it | 意大利 |
| amazon.es | 西班牙 |
| amazon.co.jp | 日本 |
| amazon.ca | 加拿大 |
| amazon.com.au | 澳大利亚 |
| amazon.com.br | 巴西 |
| amazon.in | 印度 |
| amazon.nl | 荷兰 |
| amazon.se | 瑞典 |
| amazon.pl | 波兰 |
| amazon.sg | 新加坡 |
| amazon.sa | 沙特阿拉伯 |
| amazon.ae | 阿联酋 |
| amazon.com.mx | 墨西哥 |
| amazon.com.tr | 土耳其 |
| amazon.com.be | 比利时 |
| amazon.cn | 中国 |
| amazon.eg | 埃及 |

### 常用 language 值

| 区域代码 | 说明 |
|----------|------|
| en_US | 美国站 英语 |
| en_GB | 英国站 英语 |
| de_DE | 德国站 德语 |
| fr_FR | 法国站 法语 |
| it_IT | 意大利站 意大利语 |
| es_ES | 西班牙站 西班牙语 |
| ja_JP | 日本站 日语 |
| en_CA | 加拿大站 英语 |
| fr_CA | 加拿大站 法语 |
| en_AU | 澳大利亚站 英语 |
| pt_BR | 巴西站 葡萄牙语 |
| en_IN | 印度站 英语 |
| hi_IN | 印度站 印地语 |
| nl_NL | 荷兰站 荷兰语 |
| sv_SE | 瑞典站 瑞典语 |
| pl_PL | 波兰站 波兰语 |
| en_SG | 新加坡站 英语 |
| ar_AE | 阿联酋/沙特阿拉伯/埃及站 阿拉伯语 |
| en_AE | 阿联酋/沙特阿拉伯/埃及站 英语 |
| tr_TR | 土耳其站 土耳其语 |
| nl_BE | 比利时站 荷兰语 |
| fr_BE | 比利时站 法语 |
| zh_CN | 中国站 中文 |
| pt_MX | 墨西哥站 西班牙语 |

### 常用 deliveryZip 值

| 国家 | 城市 | 邮编 |
|------|------|------|
| 美国 | 纽约 | 10001 |
| 英国 | 伦敦 | EC1A 1BB |
| 德国 | 柏林 | 10115 |
| 法国 | 巴黎 | 75001 |
| 意大利 | 罗马 | 00100 |
| 西班牙 | 马德里 | 28001 |
| 日本 | 东京 | 100-0001 |
| 加拿大 | 多伦多 | M5A 1A1 |
| 澳大利亚 | 悉尼 | 2000 |
| 巴西 | 圣保罗 | 01000-000 |
| 印度 | 新德里 | 110001 |
| 荷兰 | 阿姆斯特丹 | 1012 |
| 瑞典 | 斯德哥尔摩 | 111 22 |
| 波兰 | 华沙 | 00-001 |
| 新加坡 | 新加坡 | 018989 |
| 沙特阿拉伯 | 利雅得 | 11564 |
| 阿联酋 | 阿布扎比 | 00000 |
| 墨西哥 | 墨西哥城 | 01000 |
| 土耳其 | 伊斯坦布尔 | 34349 |
| 比利时 | 布鲁塞尔 | 1000 |
| 中国 | 北京 | 100000 |
| 埃及 | 开罗 | 11511 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总行数 |
| keyword | string | 搜索关键词 |
| type | string | 渲染的样式 |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| products | array | 搜索结果列表（详见下方） |

### products 商品对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN |
| title | string | 标题 |
| brand | string | 品牌 |
| price | number | 价格 |
| extractedPrice | number | 解析后的价格 |
| oldPrice | number | 划线价格 |
| extractedOldPrice | number | 解析后的划线价格 |
| currency | string | 币种 |
| priceUnit | string | 价格单位 |
| extractedPriceUnit | number | 解析后的价格单位 |
| rating | number | 评分 |
| ratings | integer | 评分数 |
| position | integer | 位置 |
| sponsored | boolean | 是否赞助商 |
| imageUrl | string | 缩略图 |
| asinUrl | string | 链接 |
| delivery | string | 配送信息 |
| fulfillment | string | 配送信息（如 FBA） |
| availableDate | string (date) | 上架时间 |
| monthlySalesUnits | integer | 月销量 |
| monthlySalesRevenue | string | 月销售额 |
| sellerNation | string | 卖家国籍 |
| dimension | string | 尺寸 |
| weight | string | 重量 |
| options | string | 选项 |
| offers | string | 优惠信息 |
| badges | string | 亚马逊前台搜索标识 |
| tags | string | 标签 |
| snapEbtEligible | boolean | SNAP/EBT资格 |
| sourceType | string | 来源类型：amazon |
| sourceTool | string | 来源工具 |
| keyword | string | 关键词 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 `errcode` 字段区分（`errcode = 200` 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 `errcode` 也是 401。

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
curl -X POST https://tool-gateway.linkfox.com/amazon/search \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "wireless earbuds", "amazonDomain": "amazon.com", "page": 1}'
```
