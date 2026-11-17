---
name: linkfox-echotik-batch-product-detail
description: 批量查询 TikTok 商品的多周期销量、GMV、直播数据、带货达人、价格评分等详情。
---

# EchoTik TikTok 商品批量详情（Batch Product Detail）

本技能用于批量获取 TikTok 商品的详细表现指标，帮助卖家与运营人员并排对比候选商品的销售、GMV、直播、视频与达人数据。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过商品 ID 或 TikTok Shop 商品 URL 批量查询最多 1000 个商品的详情指标。
- 返回多周期（1d/7d/15d/30d/60d/90d/累计）销量、GMV、直播销量、直播 GMV、视频、达人、观看次数等数据。
- 返回价格（USD）、评分、评论数、佣金比例、上下架/全托管状态等。

### ❌ 边界与限制

- **批量上限**：单次请求最多 1000 个商品。
- **价格币种**：所有价格字段均为 USD。
- **数据口径**：销量、GMV、归因数据为分析估算值，非平台精确数据。
- **仅查询已知商品**：本工具不按关键词或类目搜索，只解析用户已有的 ID/URL。
- **不在范围内**：按关键词发现商品（用 `linkfox-echotik-product-search`）；新品/趋势商品排行（用 `linkfox-echotik-new-product-rank`）；商品关联带货视频（用 `linkfox-echotik-product-video`）；TikTok 视频下载链接解析（用 `linkfox-echotik-get-video-download-url`）；达人主页分析；非 TikTok 平台数据。

## 调用方式

- **API 端点**：`POST /echotik/batchProductDetail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_batch_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-batch-product-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按商品 ID 批量查询**
```json
{
  "productIds": ["1729382310407603945", "1729382310407603946"]
}
```

**2. 按商品 URL 批量查询**
```json
{
  "productUrls": [
    "https://shop.tiktok.com/us/pdp/phone-case/1729382310407603945",
    "https://shop.tiktok.com/us/pdp/case-for-phone/1729382310407603946"
  ]
}
```

**3. ID 与 URL 混合（服务端合并）**
```json
{
  "productIds": ["1729382310407603945"],
  "productUrls": ["https://shop.tiktok.com/us/pdp/phone-case/1729382310407603946"]
}
```

## 展示规则

1. **呈现对比表**：每商品一行，关键列含名称、价格（USD）、总销量、30 天销量、总 GMV、评分、评论数、佣金比例、带货达人数。
2. **多周期语境**：对比动量时，在累计值旁展示相关窗口（如 7d/30d），而非只看总量。
3. **币种**：价格为 USD，需标注 USD。
4. **佣金格式**：`productCommissionRate` 以百分比展示（如 `0.05` → "5%"）。
5. **趋势标识**：`salesTrendFlag` 渲染为稳定/上升/下降，便于快速扫描。
6. **状态徽标**：在相关位置标注 `isSShop`（全托管）、`offMark`（下架）、`freeShipping`，避免用户误把下架商品纳入对比。
7. **图片引用**：返回 `imageUrl` / `productImageUrls` 时说明图片可用。
8. **长描述**：`descDetail` 可能为较长 HTML/文本，做摘要或说明其可用性，而非整段倾倒。
9. **缺失商品处理**：若请求的商品无记录，列出无数据的 ID/URL 供用户核对。
10. **错误处理**：查询失败时根据 `errmsg`/`error` 字段说明原因，建议检查 ID/URL。

## 用户表达与场景速查

**适用** —— TikTok 商品批量详情查询：

| 用户说 | 场景 |
|--------|------|
| "查这些 TikTok 商品的详情" | 按商品 ID 批量详情 |
| "拉一下这些 TikTok 链接的销量" | 按商品 URL 批量详情 |
| "对比这些 TikTok 商品的 GMV" | 批量查询，展示 GMV 列 |
| "这些 TikTok 商品哪些在涨" | 批量查询，读 `salesTrendFlag` |
| "这些 TikTok 商品有下架/全托管吗" | 批量查询，读 `offMark` / `isSShop` |
| "查这些 TikTok 商品的直播销量" | 批量查询，展示直播销量/GMV |

不适用场景见上方【能力边界】。

### 边界判断

当用户说"分析这些 TikTok 商品"时，判断用户是否已有具体商品 ID 或 TikTok Shop URL（本技能），还是想按关键词/类目**发现**商品（搜索技能）。若用户粘贴了 ID/URL 列表并希望查看销量/GMV/直播详情，适用本技能；若用户问"该卖什么"或"找趋势商品"，则不适用。

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

# EchoTik-TikTok商品批量详情 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/batchProductDetail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productIds | array&lt;string&gt; | 否* | 商品ID列表（最多 1000 个）。示例：`["1729382310407603945", "1729382310407603946"]` |
| productUrls | array&lt;string&gt; | 否* | 商品URL列表（最多 1000 个），形如 `https://shop.tiktok.com/us/pdp/<slug>/<productId>?...`；后端会从每个URL中提取末尾的 `productId` 并合并到 `productIds`，与 `productIds` 不互斥 |

\* `productIds` 与 `productUrls` 至少传其一，可同时传入；二者合并后最多 1000 个商品。

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| products | array | 商品详情列表（详见下方商品对象） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 商品对象字段

> 销量、GMV、直播、视频、达人、观看等指标均按 `1d / 7d / 15d / 30d / 60d / 90d` 多周期及累计（total）返回。价格字段单位均为 USD。

**基础信息**

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | string | 商品ID |
| productName | string | 商品名称 |
| imageUrl | string | 商品图片 |
| productImageUrls | array | 商品图片列表 |
| region | string | 区域代码 |
| sellerId | string | 卖家ID |
| categoryId | string | 一级分类ID |
| categoryL2Id | string | 二级分类ID |
| categoryL3Id | string | 三级分类ID |

**价格 / 评分 / 佣金**

| 字段 | 类型 | 说明 |
|------|------|------|
| minPrice | number | 最低SKU价格(USD) |
| maxPrice | number | 最高SKU价格(USD) |
| spuAvgPrice | number | SPU平均价格(USD) |
| productRating | number | 商品评分 |
| reviewCount | integer | 评论数量 |
| productCommissionRate | number | 商品佣金比例 |

**销量（多周期）**

| 字段 | 类型 | 说明 |
|------|------|------|
| totalSaleCnt | integer | 总销量 |
| totalSale1dCnt | integer | 近1天销量 |
| totalSale7dCnt | integer | 近7天销量 |
| totalSale15dCnt | integer | 近15天销量 |
| totalSale30dCnt | integer | 近30天销量 |
| totalSale60dCnt | integer | 近60天销量 |
| totalSale90dCnt | integer | 近90天销量 |

**销售额 GMV（多周期）**

| 字段 | 类型 | 说明 |
|------|------|------|
| totalSaleGmvAmt | number | 总销售额 |
| totalSaleGmv1dAmt | number | 近1天销售额 |
| totalSaleGmv7dAmt | number | 近7天销售额 |
| totalSaleGmv15dAmt | number | 近15天销售额 |
| totalSaleGmv30dAmt | number | 近30天销售额 |
| totalSaleGmv60dAmt | number | 近60天销售额 |
| totalSaleGmv90dAmt | number | 近90天销售额 |

**直播（多周期）**

| 字段 | 类型 | 说明 |
|------|------|------|
| totalLiveCnt | integer | 总直播数量 |
| totalLive1dCnt | integer | 近1天直播数量 |
| totalLive7dCnt | integer | 近7天直播数量 |
| totalLive15dCnt | integer | 近15天直播数量 |
| totalLive30dCnt | integer | 近30天直播数量 |
| totalLive60dCnt | integer | 近60天直播数量 |
| totalLive90dCnt | integer | 近90天直播数量 |

**直播销量 / 直播销售额（多周期）**

| 字段 | 类型 | 说明 |
|------|------|------|
| totalLiveSale1dCnt | integer | 近1天直播销量 |
| totalLiveSale7dCnt | integer | 近7天直播销量 |
| totalLiveSale15dCnt | integer | 近15天直播销量 |
| totalLiveSale30dCnt | integer | 近30天直播销量 |
| totalLiveSale60dCnt | integer | 近60天直播销量 |
| totalLiveSale90dCnt | integer | 近90天直播销量 |
| totalLiveSaleGmv1dAmt | integer | 近1天直播销售额 |
| totalLiveSaleGmv7dAmt | integer | 近7天直播销售额 |
| totalLiveSaleGmv15dAmt | integer | 近15天直播销售额 |
| totalLiveSaleGmv30dAmt | integer | 近30天直播销售额 |
| totalLiveSaleGmv60dAmt | integer | 近60天直播销售额 |
| totalLiveSaleGmv90dAmt | integer | 近90天直播销售额 |

**视频（多周期）**

| 字段 | 类型 | 说明 |
|------|------|------|
| totalVideoCnt | integer | 总视频数量 |
| totalVideo1dCnt | integer | 近1天视频数量 |
| totalVideo7dCnt | integer | 近7天视频数量 |
| totalVideo15dCnt | integer | 近15天视频数量 |
| totalVideo30dCnt | integer | 近30天视频数量 |
| totalVideo60dCnt | integer | 近60天视频数量 |
| totalVideo90dCnt | integer | 近90天视频数量 |

**达人（多周期）**

| 字段 | 类型 | 说明 |
|------|------|------|
| totalIflCnt | integer | 总达人数量 |
| totalIflVideo1dCnt | integer | 近1天达人视频数量 |
| totalIflVideo7dCnt | integer | 近7天达人视频数量 |
| totalIflVideo15dCnt | integer | 近15天达人视频数量 |
| totalIflVideo30dCnt | integer | 近30天达人视频数量 |
| totalIflVideo60dCnt | integer | 近60天达人视频数量 |
| totalIflVideo90dCnt | integer | 近90天达人视频数量 |
| totalIflLive1dCnt | integer | 近1天达人直播数量 |
| totalIflLive7dCnt | integer | 近7天达人直播数量 |
| totalIflLive15dCnt | integer | 近15天达人直播数量 |
| totalIflLive30dCnt | integer | 近30天达人直播数量 |
| totalIflLive60dCnt | integer | 近60天达人直播数量 |
| totalIflLive90dCnt | integer | 近90天达人直播数量 |

**观看次数（多周期）**

| 字段 | 类型 | 说明 |
|------|------|------|
| totalViewsCnt | integer | 总观看次数 |
| totalViews1dCnt | integer | 近1天观看次数 |
| totalViews7dCnt | integer | 近7天观看次数 |
| totalViews15dCnt | integer | 近15天观看次数 |
| totalViews30dCnt | integer | 近30天观看次数 |
| totalViews60dCnt | integer | 近60天观看次数 |
| totalViews90dCnt | integer | 近90天观看次数 |

**状态标识与其它**

| 字段 | 类型 | 说明 |
|------|------|------|
| discount | string | 折扣信息 |
| freeShipping | integer | 是否免运费 |
| salesFlag | integer | 主要配送方式 |
| salesTrendFlag | integer | 销售趋势标识：0=稳定、1=上升、2=下降 |
| isSShop | integer | 是否全托管店铺 |
| offMark | integer | 商品下架标识 |
| firstCrawlDt | string | 首次爬取日期 |
| descDetail | string | 商品详情描述 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因（如商品ID不正确、商品不存在等） |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/echotik/batchProductDetail \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "productIds": ["1729382310407603945", "1729382310407603946"]
  }'
```
