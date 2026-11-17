---
name: linkfox-amazon-reviews-list
description: 获取并分析亚马逊 15 个站点的商品评论，支持按星级筛选，用于差评拆解、情感分析与产品改良建议。
---

# 亚马逊商品评论（Amazon Product Reviews）

本技能用于按 ASIN 获取并分析亚马逊商品评论，帮助卖家从买家反馈中提取可落地的洞察。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 按 ASIN 获取亚马逊商品真实买家评论，覆盖 **15 个站点**（含美国站）。
- 按星级（1-5 星）分别控制抓取数量，每星最多 100 条。
- 支持按关键词、评论者类型（含仅已验证购买）、媒体类型、格式类型筛选。
- 按最新或最有用排序。
- 用于差评拆解、好评挖掘、情感倾向识别与产品改良建议。

### ❌ 边界与限制

- **单次请求仅支持一个 ASIN**；多 ASIN 需分别调用。
- **每星上限**：每个星级单次最多返回 100 条评论。
- **无历史快照**：评论为实时抓取，不提供历史版本对比。
- **评论语言**：评论文本按原始语言返回，不做翻译。
- **不在范围内**：ABA 搜索词/关键词研究（用 ABA 工具）；销量估算或收入分析；Listing 文案或 A+ 内容创作；广告/PPC 策略；定价或利润计算。

## 核心概念

本工具按给定亚马逊 ASIN 检索真实买家评论，覆盖 **15 个站点**。可按星级（1-5 星，每星最多 100 条）控制抓取数量，按最新或有用量排序，并应用多种筛选条件。单次请求仅支持一个 ASIN；多 ASIN 需分别调用。

## 调用方式

- **API 端点**：`POST /amazon/reviews/list`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/amazon_reviews.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-reviews-list-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 支持站点

| 站点 | 代码 |
|------|------|
| 美国 | `com` |
| 加拿大 | `ca` |
| 英国 | `co.uk` |
| 德国 | `de` |
| 法国 | `fr` |
| 意大利 | `it` |
| 西班牙 | `es` |
| 日本 | `co.jp` |
| 印度 | `in` |
| 澳大利亚 | `com.au` |
| 巴西 | `com.br` |
| 墨西哥 | `com.mx` |
| 荷兰 | `nl` |
| 瑞典 | `se` |
| 阿联酋 | `ae` |

通过 `domainCode` 指定站点。每次调用前务必与用户确认目标站点。

## 使用示例

**1. 获取美国站评论**
```json
{"asin": "B08N5WRWNW", "domainCode": "com", "star1Num": 10, "star2Num": 10, "star3Num": 10, "star4Num": 10, "star5Num": 10, "sortBy": "recent"}
```

**2. 按关键词筛选差评（德国站）**
```json
{"asin": "B08N5WRWNW", "domainCode": "de", "star1Num": 30, "star2Num": 30, "filterByKeyword": "quality", "reviewerType": "avp_only_reviews"}
```

**3. 获取带图片/视频的 5 星好评（日本站）**
```json
{"asin": "B08N5WRWNW", "domainCode": "co.jp", "star5Num": 50, "star1Num": 0, "star2Num": 0, "star3Num": 0, "star4Num": 0, "sortBy": "helpful", "mediaType": "media_reviews_only"}
```

**4. 仅获取 3 星评论（显式星级模式）**
```json
{"asin": "B0FP5C63HZ", "domainCode": "com", "star3Num": 100}
```

## 展示规则

1. **清晰呈现数据**：按星级分组展示评论，包含评分、标题、正文、日期、是否已验证购买、有用数等关键字段。
2. **适时总结**：评论较多时，先给出主题/痛点摘要，再列出个体评论。
3. **突出可落地洞察**：在差评中点出反复出现的投诉；在好评中标注被赞美的卖点。
4. **Vine 与验证标签**：明确标注 Vine Voice 与已验证购买状态。
5. **媒体标识**：标注评论是否包含图片或视频。
6. **字段归一化**：当原始响应使用站点特定的文本格式时，对评分和有用数字段做归一化以保证展示一致。
7. **错误处理**：查询失败时根据响应信息说明原因，并建议调整参数。
8. **单 ASIN 限制**：用户询问多个 ASIN 时，分别发起请求。

## 用户表达与场景速查

**适用** —— 涉及亚马逊商品评论的任务：

| 用户说 | 场景 |
|--------|------|
| "看下这个 ASIN 的评论" | 直接评论查询 |
| "获取 B08N5WRWNW 的美国站评论" | 指定站点查询 |
| "买家都在抱怨什么" | 差评分析 |
| "把 1 星评论都拉出来" | 按星级筛选 |
| "差评里有什么共性问题" | 痛点挖掘 |
| "买家喜欢这个产品的什么" | 好评分析 |
| "找提到'电池'的评论" | 关键词筛选 |
| "看带图的评论" | 媒体筛选 |
| "只要已验证购买的评论" | 评论者类型筛选 |
| "帮我分析竞品评论" | 竞品评论研究 |
| "从评论里提炼产品改良建议" | 可落地洞察提取 |

不适用场景见上方【能力边界】。

**边界判断**：若"产品调研"或"竞品分析"实质是读取特定 ASIN 的买家评论，则适用本技能；若涉及搜索量、关键词排名、销量估算或市场规模，则不适用。

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

# 亚马逊商品评论 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazon/reviews/list`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| asin | string | 是 | 亚马逊商品 ASIN |
| domainCode | string | 否 | 亚马逊域名代码，默认 `com`。可选值：`com`、`ca`、`co.uk`、`in`、`de`、`fr`、`it`、`es`、`co.jp`、`com.au`、`com.br`、`nl`、`se`、`com.mx`、`ae`。美国站使用 `com` |
| star1Num | integer | 否 | 1 星评论数量，默认获取 10 条，最多 100 条 |
| star2Num | integer | 否 | 2 星评论数量，默认获取 10 条，最多 100 条 |
| star3Num | integer | 否 | 3 星评论数量，默认获取 10 条，最多 100 条 |
| star4Num | integer | 否 | 4 星评论数量，默认获取 10 条，最多 100 条 |
| star5Num | integer | 否 | 5 星评论数量，默认获取 10 条，最多 100 条 |
| filterByKeyword | string | 否 | 按关键词筛选评论，最大长度 1000 字符 |
| sortBy | string | 否 | 评论排序方式：`recent`（最新评论）或 `helpful`（最有用评论），默认 `recent` |
| reviewerType | string | 否 | 评论者类型：`all_reviews`（所有评论）或 `avp_only_reviews`（仅已验证购买），默认 `all_reviews` |
| mediaType | string | 否 | 媒体类型：`all_contents`（所有内容）或 `media_reviews_only`（仅包含媒体的评论），默认 `all_contents` |
| formatType | string | 否 | 格式类型：`all_formats`（所有格式）或 `current_format`（当前格式），默认 `all_formats` |

说明：若 `star1Num` ~ `star5Num` 均未传，则 1~5 星默认各抓取 `10` 条；若已传任意一个星级数量，则其它未传星级默认 `0`。

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总评论数 |
| data | array | 评论列表（详见下方评论对象） |
| columns | array | 渲染的列 |
| costToken | integer | 总 Token 消耗 |
| type | string | 渲染的样式 |

### 评论对象

| 字段 | 类型 | 说明 |
|------|------|------|
| reviewId | string | 评论 ID |
| asin | string | 产品 ASIN |
| title | string | 评论标题 |
| text | string | 评论内容 |
| rating | string | 评分 |
| date | string | 评论日期 |
| userName | string | 评论者名称 |
| verified | boolean | 是否已验证购买 |
| vine | boolean | 是否 Vine Voice 评论 |
| numberOfHelpful | integer | 有用数量 |
| imageUrlList | array | 评论图片列表 |
| videoUrlList | array | 评论视频列表 |
| domainCode | string | 国家代码 |
| productTitle | string | 产品标题 |
| productRating | string | 产品评分 |
| countRatings | integer | 产品评分数量 |
| countReviews | integer | 产品评论数量 |
| variationId | string | 变体 ID |
| variationList | array | 变体列表 |
| profilePath | string | 评论者个人资料路径 |
| currentPage | integer | 当前页码 |
| sortStrategy | string | 排序策略 |
| statusCode | integer | 状态码 |
| statusMessage | string | 状态消息 |
| locale | object | 区域信息 |
| reviewSummary | object | 评论摘要数据 |
| filters | object | 已应用的筛选条件 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非 200 值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例（美国站）

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/reviews/list \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "asin": "B08N5WRWNW",
    "domainCode": "com",
    "star1Num": 10,
    "star2Num": 10,
    "star3Num": 0,
    "star4Num": 0,
    "star5Num": 0,
    "sortBy": "recent",
    "reviewerType": "all_reviews"
  }'
```
