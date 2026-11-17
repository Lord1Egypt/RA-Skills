---
name: linkfox-amazon-search-by-image
description: 支持亚马逊 8 个站点的以图搜图，通过图片 URL 跨站点检索外观相似的商品与同款竞品。
---

# 亚马逊-以图搜图（Amazon Search by Image）

本技能用于通过图片 URL 在亚马逊 8 个站点进行视觉商品搜索，帮助亚马逊卖家与调研人员跨站点发现外观相似的商品与同款竞品。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过公开可访问的图片 URL 在亚马逊 8 个站点检索外观相似的商品。
- 返回商品 ASIN、标题、图片、价格、评分、评论数、品牌等核心字段。
- 支持按价格、评分、评论数排序，支持指定站内收货邮编或站外收货国家代码。
- 可选聚合 Keepa 数据（销售排名、月销量、FBA 费用、尺寸等）。

### ❌ 边界与限制

- **图片要求**：必须提供公开可访问的图片 URL；本地图片需先上传获取公开链接（见下方「本地图片上传」）。
- **排序限制**：仅支持 `default`、`price-asc-rank`、`price-desc-rank`、`rating-asc-rank`、`rating-desc-rank`、`ratings-asc-rank`、`ratings-desc-rank`；不在列表内的排序不得尝试其他变通方式，应告知用户支持的排序选项。
- **邮编与国家代码互斥**：`deliveryZip`（站内邮编）与 `countryOrAreaCode`（站外国家代码）不能同时指定；印度站不支持站外收货。
- **不在范围内**：基于关键词的文本搜索（用关键词搜索工具）；ABA 搜索词数据分析；评论分析与 Listing 优化；无源图片的销量估算；图片编辑或生成；本地图片文件直接搜索。

## 核心概念

亚马逊以图搜图（视觉搜索）允许提交商品图片 URL，返回亚马逊上外观相似的商品列表，适用于竞品分析、找同款、识别仿品与基于外观的市场机会发现。

**支持站点**：

| 站点 | 域名 | 默认邮编 |
|------|------|----------|
| 美国 | amazon.com | 10001 |
| 英国 | amazon.co.uk | EC1A 1BB |
| 德国 | amazon.de | 10115 |
| 法国 | amazon.fr | 75001 |
| 意大利 | amazon.it | 00100 |
| 西班牙 | amazon.es | 28001 |
| 日本 | amazon.co.jp | 100-0001 |
| 印度 | amazon.in | 110034 |

默认站点为 **amazon.com**（美国），用户未指定时使用美国站。

## 调用方式

- **API 端点**：`POST /amazon/searchByImage`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/amazon_search_by_image.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-search-by-image-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 本地图片上传

本工具要求**公开可访问的图片 URL**。若用户提供的是本地图片文件路径（如 `C:\Users\...\photo.png`、`/home/.../image.jpg`），需先上传以获取公开链接。

运行上传脚本：
```bash
python scripts/upload_image.py /path/to/local/image.png
```

脚本会返回一个公开 URL（有效期 24 小时），可用作 `imageUrl` 参数。

## 使用示例

**1. 美国站基础图片搜索**
```
用这张图在亚马逊美国站找外观相似的商品：
https://m.media-amazon.com/images/I/61pAlIX8SZL._AC_SY575_.jpg
```

**2. 指定站点找同款**
```
在亚马逊德国站（amazon.de）用这张图找外观相似的商品：
https://example.com/product-photo.jpg
```

**3. 按价格从低到高排序**
```
在亚马逊美国站用这张图找相似商品，按价格从低到高排序：
https://example.com/my-product.jpg
```

**4. 聚合 Keepa 数据**
```
在亚马逊美国站用这张图找相似商品，并包含 Keepa 销售数据：
https://example.com/competitor-product.jpg
```

**5. 站外收货搜索**
```
在亚马逊日本站用这张图找相似商品，收货地址设为中国：
https://example.com/item.jpg
```

**6. 竞品同款发现**
```
我在竞品 listing 上看到这张产品图，在亚马逊英国站帮我找所有外观相似的商品：
https://example.com/competitor.jpg
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示搜索结果，优先列：商品图片、标题、ASIN、价格、评分、评论数、品牌。
2. **图片展示**：响应中含 `imageUrl` 时内联展示，便于直观对比。
3. **价格与币种**：价格始终带币种代码（如 $29.99 USD、24.99 EUR）。
4. **Keepa 数据**：启用 `aggregateByKeepaData` 且存在 Keepa 字段时，在展开区或附加列展示月销量、销售排名、FBA 费用等补充数据。
5. **结果总数**：始终告知用户找到的结果总数（`total` / `totalCount`）。
6. **错误处理**：查询失败时说明原因，并建议检查图片 URL 是否有效且公开可访问。
7. **排序限制**：用户请求的排序不在支持列表内时，明确说明可用的排序选项，不尝试未支持的变通方式。
8. **不做二次处理**：本工具结果不入库，无法进行二次 SQL 处理。

## 用户表达与场景速查

**适用** —— 亚马逊视觉商品搜索场景：

| 用户说 | 场景 |
|--------|------|
| "用这张图找相似商品" | 基础图片搜索 |
| "以图搜图"、"亚马逊反向图片搜索" | 视觉搜索 |
| "找竞品同款"、"找同款商品" | 按外观做竞品分析 |
| "亚马逊上有什么商品长得像这个" | 商品发现 |
| "找长得一样但更便宜的替代品" | 基于价格的视觉对比 |
| "在亚马逊日/德/英站用这张产品图搜" | 跨站点视觉搜索 |
| "看下相似商品的 Keepa 数据" | 聚合数据的视觉搜索 |
| "用这张照片找相似商品，按评分排序" | 排序视觉搜索 |

不适用场景见上方【能力边界】。

**边界判断**：当用户说"找相似商品"或"竞品分析"时，若提供了图片 URL 且意图是找外观相似的亚马逊商品，则适用本技能；若是要基于关键词的搜索、销量数据分析或无图片的商品调研，则不适用。

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

# 亚马逊-以图搜图 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazon/searchByImage`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| imageUrl | string | 是 | 图片URL地址，请确保图片URL地址有效。最大长度：1000 |
| amazonDomain | string | 是 | 亚马逊站点，仅支持以下站点：美国(`amazon.com`)、英国(`amazon.co.uk`)、德国(`amazon.de`)、法国(`amazon.fr`)、意大利(`amazon.it`)、西班牙(`amazon.es`)、日本(`amazon.co.jp`)、印度(`amazon.in`)。默认 `amazon.com` |
| sort | string | 否 | 排序，支持价格、评分、评论数排序。可选值：`default`（默认）、`price-asc-rank`（价格从低到高）、`price-desc-rank`（价格从高到低）、`rating-asc-rank`（评分从低到高）、`rating-desc-rank`（评分从高到低）、`ratings-asc-rank`（评论数从低到高）、`ratings-desc-rank`（评论数从高到低） |
| deliveryZip | string | 否 | 站内收货地址邮编或城市，如果用户未指定，则取站点（国家）的默认邮编。最大长度：1000。各站点默认邮编：美国=10001、英国=EC1A 1BB、德国=10115、法国=75001、意大利=00100、西班牙=28001、日本=100-0001、印度=110034 |
| countryOrAreaCode | string | 否 | 站外收货的国家代码（如 CN、JP、KR、TW、HK、MO、SG、TH、VN、PH、MY）。站内邮编地址和站外国家地区代码不能同时指定。注意：印度站不支持设置站外国家或地区收货。最大长度：1000 |
| aggregateByKeepaData | boolean | 否 | 是否聚合Keepa数据（销售排名、月销量、FBA费用、尺寸等） |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总行数 |
| totalCount | integer | 总数量 |
| perPage | integer | 每页数量 |
| currentPage | integer | 当前页码 |
| type | string | 渲染的样式 |
| sourceType | string | 来源类型 |
| columns | array | 渲染的列 |
| costToken | integer | 消耗token |
| products | array | 商品列表（详见下方商品字段） |

### 商品字段

每个商品返回的核心字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN |
| title | string | 商品标题 |
| imageUrl | string | 图片URL（请求地址） |
| asinUrl | string | 亚马逊ASIN的详情网址 |
| price | number | 当前价格（单位：元，如美元/欧元等） |
| oldPrice | number | 划线价格 |
| currency | string | 币种 |
| rating | number | 当前评分（0.0-5.0，如4.5星） |
| ratings | integer | 评分数量 |
| brand | string | 品牌 |
| sourceTool | string | 来源工具 |
| sourceType | string | 来源类型 |

Keepa 聚合字段（当 `aggregateByKeepaData` 为 true 时返回）：

| 字段 | 类型 | 说明 |
|------|------|------|
| salesRank | integer | 销售排名(keepa) |
| salesRank30 | integer | 近30天平均销售排名(keepa) |
| salesRank90 | integer | 近90天平均销售排名(keepa) |
| salesRank180 | integer | 近180天平均销售排名(keepa) |
| monthlySalesUnits | integer | 月销量(keepa) |
| monthlySalesRevenue | number | 月销售额(keepa) |
| monthlySalesUnits1MonthAgo ~ monthlySalesUnits12MonthsAgo | integer | 1~12月前月销量(keepa) |
| reviewCount | integer | 评论数量(keepa) |
| fbaFees | number | FBA配送费(keepa)（单位：元） |
| profit | number | 利润率(keepa)（利润率百分比，如25.5表示25.5%） |
| referralFeePercentage | number | 推荐费百分比(keepa) |
| fulfillment | string | 配送方式(AMZ, FBA, FBM)(keepa) |
| primePrice | number | Prime价格(keepa) |
| buyBoxSellerId | string | 购买按钮卖家ID(keepa) |
| sellerNum | integer | 卖家数(keepa) |
| variationNum | integer | 变体数量(keepa) |
| parentAsin | string | 父ASIN(keepa) |
| availableDate | string | 上架时间(keepa)（yyyy-MM-dd HH:mm:ss） |
| lastUpdate | string | 最后更新时间(keepa)（yyyy-MM-dd HH:mm:ss） |
| manufacturer | string | 制造商(keepa) |
| model | string | 型号(keepa) |
| color | string | 颜色(keepa) |
| material | string | 产品的材质(keepa)，指其构造中使用的主要材料 |
| weight | string | 重量（克）(keepa) |
| dimension | string | 尺寸(keepa) |
| itemLength | integer | 商品长度(keepa)，单位为毫米，不可用时为0或-1 |
| itemWidth | integer | 商品宽度(keepa)，单位为毫米，不可用时为0或-1 |
| itemHeight | integer | 商品高度(keepa)，单位为毫米，不可用时为0或-1 |
| packageLength | integer | 包装长度（毫米）(keepa) |
| packageWidth | integer | 包装宽度（毫米）(keepa) |
| packageHeight | integer | 包装高度（毫米）(keepa) |
| packageWeight | string | 包装重量（克）(keepa) |
| packageDimensions | string | 包装尺寸(keepa) |
| packageQuantity | integer | 包装中商品的数量(keepa)，不可用时为0或-1 |
| dimensionsType | string | 尺寸类型(keepa) |
| categoryTree | string | 类目树(keepa) |
| categoryTreeId | string | 类目树ID(keepa) |
| rootCategory | integer | 根类目ID(keepa) |
| isAdultProduct | boolean | 是否为成人产品(keepa) |
| isHazmat | boolean | 是否为危险品(keepa) |
| urlSlug | string | URL Slug(keepa) |
| productImageUrls | array | 商品图片列表(keepa) |

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
curl -X POST https://tool-gateway.linkfox.com/amazon/searchByImage \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "imageUrl": "https://m.media-amazon.com/images/I/61pAlIX8SZL._AC_SY575_.jpg",
    "amazonDomain": "amazon.com",
    "sort": "default"
  }'
```

### 聚合 Keepa 数据示例

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/searchByImage \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "imageUrl": "https://m.media-amazon.com/images/I/61pAlIX8SZL._AC_SY575_.jpg",
    "amazonDomain": "amazon.com",
    "sort": "price-asc-rank",
    "aggregateByKeepaData": true
  }'
```

### 站外收货示例

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/searchByImage \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "imageUrl": "https://m.media-amazon.com/images/I/61pAlIX8SZL._AC_SY575_.jpg",
    "amazonDomain": "amazon.co.jp",
    "countryOrAreaCode": "CN"
  }'
```
