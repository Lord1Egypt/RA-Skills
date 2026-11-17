---
name: linkfox-fastmoss-product-rank-top-selling
description: 基于FastMoss数据，按日/周/月维度和品类分析TikTok全球电商市场的热销商品排行榜与GMV排名，用于爆品分析与选品调研。
---

# FastMoss TikTok 热销榜单（FastMoss Product Rank Top Selling）

本技能用于查询 TikTok Shop 全球电商市场的热销商品排行榜，帮助跨境卖家按日/周/月维度及类目维度发现爆品、分析销量与 GMV 排名。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询 TikTok Shop 9 个全球市场（US、GB、MX、ES、ID、VN、MY、TH、PH）的热销商品排行榜。
- 支持日、周、月三种时间粒度，可按销量、GMV、增长率等字段排序。
- 支持按类目筛选，查看特定类目下的热销商品。
- 返回商品价格、销量、GMV、增长率、佣金率、店铺信息等多维数据。

### ❌ 边界与限制

- **dateInfo 必填**：`type` 与 `value` 必须同时提供且格式严格匹配（day=`YYYY-MM-DD`，week=`YYYY-周数`如 `2025-18`，month=`YYYY-MM`）。
- **不支持关键词搜索**：本工具不支持按关键词搜索商品（请使用 linkfox-fastmoss-product-search）。
- **分页上限**：`pageSize` 最大 10，默认 10。
- **数据时效**：数据存在 T+1 统计延迟。
- **类目语言**：`category` 参数须为英文，非英文输入需先翻译。
- **不在范围内**：Amazon 选品与 ABA 关键词；TikTok 广告投放与广告管理；TikTok 内容创作与视频剪辑；商品评论与 Listing 文案；TikTok 关键词商品搜索（用 linkfox-fastmoss-product-search）；利润率计算与定价策略。

## 核心概念

TikTok 热销榜单追踪 TikTok Shop 在 9 个全球市场表现最佳的商品，反映其在销量、GMV、增长率上的领先情况，是 TikTok 选品、趋势分析与竞争情报的核心工具。

**数据范围**：覆盖 9 个 TikTok Shop 市场，支持日/周/月三种时间粒度（通过 `dateInfo` 参数控制）。每个商品包含销量、GMV、增长率、佣金率、店铺、类目等信息。

**dateInfo 格式（关键）**：
- type: `"day"` -> value: `"2025-02-01"`（YYYY-MM-DD）
- type: `"week"` -> value: `"2025-18"`（年-周数）
- type: `"month"` -> value: `"2025-02"`（年-月）

**分页**：使用 `page`（页码，从 1 开始）与 `pageSize`（每页条数，最大 10，默认 10）翻页。

## 支持市场

| 代码 | 市场 |
|------|------|
| US | 美国 |
| GB | 英国 |
| MX | 墨西哥 |
| ES | 西班牙 |
| ID | 印度尼西亚 |
| VN | 越南 |
| MY | 马来西亚 |
| TH | 泰国 |
| PH | 菲律宾 |

用户未指定市场时默认使用 **US**。

## 调用方式

- **API 端点**：`POST /fastmoss/productRankTopSelling`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/fastmoss_product_rank_top_selling.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-fastmoss-product-rank-top-selling-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 美国当日热销商品（日榜）**
查询美国市场某一天的热销商品。
```
region: "US", dateInfo: {"type": "day", "value": "2026-04-15"}
```

**2. 英国周榜热销**
查看英国市场的周度热销商品。
```
region: "GB", dateInfo: {"type": "week", "value": "2026-15"}
```

**3. 东南亚月度 GMV 领先商品**
查看印尼市场月度热销商品并按 GMV 排序。
```
region: "ID", dateInfo: {"type": "month", "value": "2026-03"}, orderby: {"field": "gmv", "order": "desc"}
```

**4. 指定类目排行**
查找特定类目下的热销商品。
```
region: "US", dateInfo: {"type": "day", "value": "2026-04-15"}, category: "Beauty"
```

## 展示规则

1. **只呈现数据**：以清晰表格展示查询结果，不做主观商业建议。
2. **增长率**：增长率为百分比，展示时带 % 符号。
3. **佣金率**：佣金率为基点（1000 = 10%），展示时换算为百分比。
4. **币种**：不同市场币种不同，价格须始终附带币种展示。
5. **dateInfo 格式**：校验并提醒用户所选时间粒度的正确格式。
6. **下架状态**：`offShelvesText` 值 "是" 表示已下架，"否" 表示在售，需向用户说明。

## 用户表达与场景速查

**适用** —— TikTok 热销商品排行与趋势分析：

| 用户说 | 场景 |
|--------|------|
| "TikTok 上什么最火"、"TikTok 热销榜" | 热销排行查询 |
| "TikTok 本周爆款"、"TikTok Shop 热门商品" | 周/日榜查询 |
| "TikTok GMV 排名"、"TikTok 收入最高的商品" | 按 GMV 排序的排行 |
| "TikTok 类目热销"、"TikTok 美妆热销榜" | 指定类目排行 |
| "TikTok 选品周报"、"月度热销榜" | 时间维度分析 |
| "FastMoss 热销"、"FastMoss 排行数据" | 直接数据源引用 |
| "TikTok 上增长最快的商品" | 按增长率排序的排行 |

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

# FastMoss-TikTok热销榜单 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/fastmoss/productRankTopSelling`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region | string | 是 | 市场区域代码。可选值：US（美国）、GB（英国）、MX（墨西哥）、ES（西班牙）、ID（印度尼西亚）、VN（越南）、MY（马来西亚）、TH（泰国）、PH（菲律宾） |
| dateInfo | object | 是 | 日期规格对象，包含 `type` 和 `value` 两个字段 |
| dateInfo.type | string | 是 | 时间粒度：`day`（日）、`week`（周）、`month`（月） |
| dateInfo.value | string | 是 | 日期值：day 格式 `YYYY-MM-DD`，week 格式 `YYYY-周数`（如 `2025-18`），month 格式 `YYYY-MM` |
| category | string | 否 | 商品类目名称（英文），会匹配到 TikTok 类目 ID。非英文输入需先翻译为英文 |
| orderby | object | 否 | 排序规则对象，包含 `field` 和 `order` 两个字段 |
| orderby.field | string | 否 | 排序字段：`units_sold`（销量）、`gmv`（销售额）、`total_units_sold`（总销量）、`total_gmv`（总销售额）、`growth_rate`（增长率） |
| orderby.order | string | 否 | 排序方向：`desc`（降序）、`asc`（升序），默认 `desc` |
| page | integer | 否 | 页码，默认 `1` |
| pageSize | integer | 否 | 每页条数，最大 `10`，默认 `10` |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| products | array | 热销商品列表（见下方商品对象） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗 token |

### 商品对象

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 商品名称 |
| productId | string | 商品 ID |
| region | string | 区域代码 |
| price | number | 商品价格 |
| minPrice | number | 最低价格 |
| maxPrice | number | 最高价格 |
| currency | string | 货币 |
| totalSaleCnt | integer | 总销量 |
| totalSale1dCnt | integer | 近1天销量（dateType=day 时返回） |
| totalSale7dCnt | integer | 近7天销量（dateType=week 时返回） |
| totalSale30dCnt | integer | 近30天销量（dateType=month 时返回） |
| totalSaleGmvAmt | number | 总销售额 |
| totalSaleGmv1dAmt | number | 近1天销售额（dateType=day 时返回） |
| totalSaleGmv7dAmt | number | 近7天销售额（dateType=week 时返回） |
| totalSaleGmv30dAmt | number | 近30天销售额（dateType=month 时返回） |
| growthRate | number | 增长率（百分比） |
| shopName | string | 店铺名称 |
| shopTotalUnitsSold | integer | 店铺总销量 |
| shopSellerId | string | 店铺卖家 ID |
| categoryName | string | 商品类目 |
| productCommissionRate | number | 商品佣金比例（基点，1000=10%） |
| imageUrl | string | 商品图片 URL |
| offShelvesText | string | 是否下架（"是"=已下架，"否"=在售） |

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
curl -X POST https://tool-gateway.linkfox.com/fastmoss/productRankTopSelling \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"region": "US", "dateInfo": {"type": "day", "value": "2026-04-15"}, "page": 1, "pageSize": 10}'
```
