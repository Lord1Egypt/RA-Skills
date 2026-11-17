---
name: linkfox-sellersprite-market-statistics
description: 提供亚马逊类目节点的市场统计看板，快速评估头部商品均价、销量及市场竞争格局。
---

# 卖家精灵-市场统计（SellerSprite Market Statistics）

本技能通过卖家精灵按亚马逊类目节点输出市场统计看板，帮助快速判断某类目的市场质量与竞争格局。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 按类目节点（`nodeIdPath`）输出聚合统计看板，不返回完整商品明细。
- 覆盖头部 Listing 平均星级、均价、BSR、月均销量/销售额、卖家数、品牌数、新品相关指标。
- 支持按 `topN` 自定义头部样本数量、按 `newProduct` 自定义新品口径、按 `month` 选择最近 30 天或具体月份。

### ❌ 边界与限制

- 必填参数：`marketplace`、`nodeIdPath`。
- `nodeIdPath` 必须为合法节点路径（如 `1064954:1069242:...`）。
- 月份查询受第三方历史范围限制，`yyyyMM` 最多支持当前月往前共 24 个月内的月份。
- **不在范围内**：商品级明细与 Listing 内容分析；关键词搜索与选词；竞品 Listing 监控；店铺级分析；类目定位（用户未给 `nodeIdPath` 时需先做类目定位）。

## 核心概念

- **节点统计**：对指定类目节点做聚合统计，不返回完整商品明细。
- **TopN 口径**：`topN` 决定头部商品统计样本数量（默认 10）。
- **新品定义**：`newProduct` 指定“新品”按最近 N 个月定义（默认 6）。

## 调用方式

- **API 端点**：`POST /sellersprite/market/statistics`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sellersprite_market_statistics.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sellersprite-market-statistics-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

```json
{
  "marketplace": "US",
  "nodeIdPath": "172282:281407",
  "month": "nearly",
  "topN": 10,
  "newProduct": 6
}
```

## 展示规则

1. 明确展示统计口径：`topN`、`newProduct`、时间范围。
2. 先输出关键总览指标，再输出扩展字段。
3. 若用户未给 `nodeIdPath`，先引导用户提供节点路径或先做类目定位。

## 用户表达与场景速查

**适用** —— 类目市场统计与基础盘评估：

| 用户说 | 场景 |
|--------|------|
| "类目市场统计"、"选市场看板" | 节点聚合统计 |
| "市场基础盘评估" | 类目整体规模与竞争格局 |
| "头部商品统计"、"头部 Listing 均价" | 头部样本指标 |
| "新品占比"、"新品销量" | 新品相关指标 |
| "SellerSprite market statistics" | 卖家精灵市场统计 |

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

# 卖家精灵-选市场统计 API 参考

本文档与工具 `_sellersprite_market_statistics` 的 `inputSchema` / `outputSchema`（见 `temp/tools20260430.txt`）对齐。

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/sellersprite/market/statistics`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置，按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

| 参数 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| marketplace | string | 是 | maxLength 1000，默认 `US` | 站点编码，见 [marketplace 可选值](#marketplace-可选值) |
| nodeIdPath | string | 是 | maxLength 1000 | 节点 ID 路径字符串，如 `1064954:1069242:1069784:1069820:1069838:1069828` |
| month | string | 否 | 见 [month](#month) | 筛选日期：`nearly` 或 `yyyyMM` |
| topN | integer | 否 | 默认 `10` | 头部 Listing 数量（用于头部相关指标口径） |
| newProduct | integer | 否 | 默认 `6` | 新品定义（月） |

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

### month

- **格式**：正则 `^(nearly|(19|20)\d{2}(0[1-9]|1[0-2]))$`
- **`nearly`**：最近 30 天
- **`yyyyMM`**：具体月份（如 `202507`）；最多支持**当前月往前共 24 个月内**的月份

## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总条数 |
| marketplace | string | 站点编码 |
| data | array | 统计结果列表（对应第三方 `data`） |
| columns | array | 渲染的列 |
| costToken | integer | 消耗 token |
| type | string | 渲染的样式 |

### data[] 元素（单条节点统计）

工具 schema 中 `hl*` 表示 **头部 Listing 前 N 名**（N 由请求参数 `topN` 决定）。

#### 节点与站点

| 字段 | 类型 | 说明 |
|------|------|------|
| nodeIdPath | string | 节点 ID 路径 |
| nodeLabelPath | string | 节点名称路径 |
| nodeLabelLocale | string | 节点名称翻译 |
| nodeLabelPathLocale | string | 节点名称路径翻译 |
| marketplace | string | 市场标志 |
| countryCode | string | 国家二简码 |
| currency | string | 该市场的货币类型 |

#### 规模与样本

| 字段 | 类型 | 说明 |
|------|------|------|
| totalProducts | integer | 商品总数 |
| products | integer | 样品商品数 |
| sellers | integer | 卖家数 |
| brands | integer | 品牌数 |
| avgSellers | number | 平均卖家数 |
| hlProducts | integer | 头部 Listing 前 N 名商品样本数 |

#### 市场整体指标

| 字段 | 类型 | 说明 |
|------|------|------|
| avgUnits | integer | 月均销量 |
| avgRevenue | number | 月均销售额 |
| avgPrice | number | 平均价格 |
| avgRating | number | 平均星级 |
| avgRatings | integer | 平均评分数 |
| avgRatingsCv | integer | 月评论平均增长数 |
| avgBsr | integer | 平均 BSR |
| avgProfit | number | 平均利润率 |
| avgWeight | number | 平均重量(pound) |
| baseAvgWeight | number | 平均重量(g) |
| avgVolume | number | 平均体积(in³) |
| baseAvgVolume | number | 平均体积(cm³) |

#### 头部 Listing（前 N 名，N = topN）

| 字段 | 类型 | 说明 |
|------|------|------|
| hlAvgUnits | integer | 头部 Listing 前 N 名商品月均销量 |
| hlAvgRevenue | number | 头部 Listing 前 N 名商品月均销售额 |
| hlAvgPrice | number | 头部 Listing 前 N 名商品平均价格 |
| hlAvgRating | number | 头部 Listing 前 N 名商品平均星级 |
| hlAvgRatings | integer | 头部 Listing 前 N 名商品平均评论数 |
| hlAvgRatingsCv | integer | 头部 Listing 前 N 名商品月评论平均增长数 |
| hlAvgBsr | integer | 头部 Listing 前 N 名商品平均 BSR |

#### 新品（口径由 newProduct 定义）

| 字段 | 类型 | 说明 |
|------|------|------|
| newProducts | integer | 新品数量 |
| newProductProportion | number | 新品数量占比 |
| newAvgUnits | integer | 新品月均销量 |
| newAvgRevenue | number | 新品月均销售额 |
| newAvgPrice | number | 新品平均价格 |
| newAvgRating | number | 新品平均星级 |
| newAvgRatings | integer | 新品平均评分数 |
| minNewRatings | integer | 最低新品评分数 |
| maxNewRatings | integer | 最高新品评分数 |

#### 上架时间

| 字段 | 类型 | 说明 |
|------|------|------|
| firstShelfDate | string | 商品首次上架日期 |
| lastShelfDate | string | 商品最新上架日期 |

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/sellersprite/market/statistics \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "marketplace": "US",
    "nodeIdPath": "172282:281407",
    "month": "nearly",
    "topN": 10,
    "newProduct": 6
  }'
```
