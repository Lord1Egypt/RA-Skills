---
name: linkfox-echotik-list-new-product-rank
description: TikTok Shop 新品排行查询。基于 EchoTik 数据发现多区域市场的短视频电商热销爆品与新兴商品趋势。
---

# EchoTik - TikTok 新品排行（New Product Ranking）

本技能用于通过 EchoTik 数据源查询和分析 TikTok Shop 新品排行数据，帮助跨境电商卖家在 TikTok 区域市场识别热门新品。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询 TikTok Shop 16 个区域市场的新品排行数据，获取每日新品快照。
- 展示新品的价格、销量、销售额、带货达人数、关联视频/直播数、佣金率、评分等指标。
- 支持按 `region` 切换市场、按 `pageNum` / `pageSize` 翻页浏览大结果集。

### ❌ 边界与限制

- **日期必填**：`date` 参数必填，格式 `YYYY-MM-DD`，无默认日期。
- **日粒度数据**：为每日快照，不提供周榜/月榜或跨多月的长期趋势。
- **分页**：单次请求不会返回全部商品，需用 `pageNum`、`pageSize` 翻页。
- **不在范围内**：Amazon 选品与关键词分析（用 ABA 工具）；TikTok 广告投放与广告管理；TikTok 内容创作或视频剪辑；商品评价与 Listing 文案撰写；利润率计算与定价策略。

## 核心概念

TikTok 新品排行追踪在 TikTok Shop 近期上架且表现上升的新品，揭示哪些新品卖得好、其定价、销量、达人覆盖与直播活跃度，是短视频电商选品、趋势分析与竞品情报的必备工具。

**数据范围**：覆盖 16 个 TikTok Shop 市场，提供每日新品快照及其表现指标（销量、销售额、达人数、视频数、直播数、佣金率、评分等）。

**分页**：结果分页返回，用 `pageNum`（页码，从 1 开始）与 `pageSize`（每页条数，默认 50）浏览。

## 调用方式

- **API 端点**：`POST /echotik/listNewProductRank`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_list_new_product_rank.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换 region、翻页或改 date 连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-list-new-product-rank-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 当日美国市场热门新品**
查询美国市场当前日期，查看哪些新品正在上升。
```
date: "2025-06-15", region: "US"
```

**2. 发掘东南亚热门新品**
查看印尼或泰国市场的新品机会。
```
date: "2025-06-15", region: "ID"
```

**3. 浏览英国市场新品排行**
考察英国 TikTok Shop 的新晋热门商品。
```
date: "2025-06-15", region: "GB"
```

**4. 翻页浏览大结果集**
获取美国市场每页 20 条的第 2 页。
```
date: "2025-06-15", region: "US", pageNum: 2, pageSize: 20
```

## 展示规则

1. **只呈现数据**：以清晰表格展示查询结果，不做主观商业建议。
2. **销量趋势说明**：展示销量趋势时，将数值标识翻译为可读标签：0 = 平稳，1 = 上升，2 = 下降。
3. **币种标注**：价格须带币种代码，不同市场币种不同。
4. **大结果提示**：结果较多时展示头部商品摘要，并提醒用户可翻页获取更多。
5. **图片处理**：返回 `imageUrl` 时提及但不内联渲染，除非环境支持。
6. **错误处理**：查询失败时说明原因，并建议调整 `date` 或 `region` 参数。

## 用户表达与场景速查

**适用** —— TikTok Shop 新品发现与趋势分析：

| 用户说 | 场景 |
|--------|------|
| "TikTok 上什么新品火" | 新品排行查询 |
| "TikTok 今日热销"、"TikTok Shop 爆品" | 每日排行查询 |
| "东南亚 TikTok 新品机会" | 区域市场考察 |
| "TikTok 英国卖得好的新品" | 区域排行 |
| "TikTok 选品"、"短视频电商趋势" | 通用商品发现 |
| "TikTok 上升的新品" | 趋势筛选排行 |
| "TikTok 达人推的货"、"TikTok 创作者在卖什么" | 达人驱动商品发现 |

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

# EchoTik-TikTok新品榜 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/listNewProductRank`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 日期，格式为 `YYYY-MM-DD` |
| region | string | 否 | 区域，默认 `US`。可选值：US（美国）、ID（印度尼西亚）、TH（泰国）、PH（菲律宾）、MY（马来西亚）、VN（越南）、GB（英国）、MX（墨西哥）、SG（新加坡）、SA（沙特阿拉伯）、BR（巴西）、ES（西班牙）、JP（日本）、DE（德国）、IT（意大利）、FR（法国） |
| pageNum | integer | 否 | 分页页码，默认 `1` |
| pageSize | integer | 否 | 每页条数，默认 `50` |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| products | array | 最新商品列表（见下方商品对象） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 商品对象

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 商品名称 |
| asin | string | 商品ID |
| region | string | 区域代码 |
| price | number | SPU平均价格 |
| minPrice | number | 最低价格 |
| maxPrice | number | 最高价格 |
| currency | string | 货币 |
| totalSaleCnt | integer | 总销量 |
| totalSale30dCnt | integer | 近30天销量 |
| totalSaleGmvAmt | number | 总销售额 |
| totalSaleGmv30dAmt | number | 近30天销售额 |
| salesTrendFlagText | string | 销售趋势标识，0=平稳 1=上升 2=下降 |
| totalVideoCnt | integer | 视频总数 |
| totalLiveCnt | integer | 直播总数 |
| totalIflCnt | integer | 总达人数 |
| productCommissionRate | number | 商品佣金比例 |
| productRating | number | 商品评分 |
| reviewCount | integer | 评论数量 |
| availableDate | string (date) | 首次爬取日期 |
| categoryId | string | 商品分类ID |
| imageUrl | string | 商品图片 |
| productImageUrls | array | 商品图片URL列表 |
| sourceTool | string | 来源工具 |
| sourceType | string | 商品来源 |

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
curl -X POST https://tool-gateway.linkfox.com/echotik/listNewProductRank \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-06-15", "region": "US", "pageNum": 1, "pageSize": 50}'
```
