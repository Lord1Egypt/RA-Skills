---
name: linkfox-junglescout-keyword-share-of-voice
description: 利用Jungle Scout分析关键词在前3页的品牌声量占比（SOV），包含自然/广告分布、PPC竞价及TOP3 ASIN点击转化。
---

# Jungle Scout — 关键词市场份额 Share of Voice

本技能通过 Jungle Scout 数据源查询亚马逊关键词的 Share of Voice（SOV）数据，返回搜索结果前3页的品牌可见度分布，以及搜索量、PPC竞价估算和 TOP ASIN 点击/转化指标，覆盖10个亚马逊站点。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 分析亚马逊关键词搜索结果前3页的品牌声量占比（SOV），覆盖自然、广告、综合三个维度，各维度含基础 SOV 与加权 SOV 两种算法。
- 返回30天精确搜索量、PPC竞价中位数、TOP3 ASIN 点击量/转化量/转化率。
- 支持10个站点：us、uk、de、in、ca、fr、it、es、mx、jp。

### ❌ 边界与限制

- **覆盖范围**：仅分析亚马逊搜索结果前3页（通常约48–60个商品）。
- **单关键词**：每次 API 调用只分析一个关键词；多关键词对比需分别调用。
- **数据为快照**：反映抓取时点的状态，非历史趋势；本工具不提供 SOV 历史变化，搜索量历史趋势请用关键词历史工具。
- **不在范围内**：历史搜索量趋势（用关键词历史工具）；关键词建议/挖掘（用 ABA 或关键词探索工具）；商品级销量估算或评论分析；Listing 优化或文案建议；非亚马逊平台数据。

## 核心概念

Share of Voice 衡量**某个品牌在搜索结果中占据的版面比例**。Jungle Scout 分析亚马逊搜索结果前3页，从三个维度计算每个品牌的存在感：

- **自然 SOV**：自然（非广告）搜索结果位的品牌可见度
- **广告 SOV**：广告/赞助位的品牌可见度
- **综合 SOV**：合并自然与广告结果的整体品牌可见度

每个维度有两种算法：

- **基础 SOV**：简单商品数占比——某品牌商品数 ÷ 3页总商品数
- **加权 SOV**：按位置加权的占比，靠前位置权重更高，并考虑 Amazon's Choice 徽章等因素；这是竞争分析中更有意义的指标

工具还返回：

- **30天精确搜索量**：过去30天的预估搜索总量
- **PPC竞价中位数**：该关键词的建议竞价中位数，用于广告成本估算
- **TOP3 ASIN 点击与转化数据**：按点击量排名的 TOP3 ASIN，含点击量、转化量、转化率

## 调用方式

- **API 端点**：`POST /tool-jungle-scout/keywords/share-of-voice`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/junglescout_keyword_sov.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-junglescout-keyword-share-of-voice-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

只需两个参数：`marketplace` 和 `keyword`。

### 构建调用的原则

1. **站点映射**："美国站" → `us`，"日本站" → `jp`，"德国站" → `de`；未指定时默认 `us`
2. **关键词**：原样传入用户关键词（建议小写英文）
3. **每次一个关键词**：每个请求只分析一个关键词；多关键词对比需分别调用

### 常见查询场景

**1. 品牌垄断检查——这个词被谁占据？**
```json
{
  "marketplace": "us",
  "keyword": "portable charger"
}
```
关注 `combinedWeightedSov`，看哪些品牌主导搜索结果页。

**2. PPC竞争分析——这个词值不值得投？**
```json
{
  "marketplace": "us",
  "keyword": "wireless earbuds"
}
```
将 `exactSuggestedBidMedian` 与搜索量对比以衡量性价比，查看 `sponsoredWeightedSov` 了解竞品广告投入力度。

**3. TOP ASIN 的转化效率**
```json
{
  "marketplace": "de",
  "keyword": "kopfhörer kabellos"
}
```
查看 `topAsins` 数组，判断高点击商品是否转化良好。高点击 + 低转化率可能意味着机会。

**4. 识别市场空白——是否存在未被满足的位置？**
```json
{
  "marketplace": "jp",
  "keyword": "ヨガマット"
}
```
若没有任何品牌的 `combinedWeightedSov` 超过 0.15，说明该关键词市场分散，可能更易进入；结合搜索量评估市场规模。

**5. 对比自然与广告存在感**
```json
{
  "marketplace": "uk",
  "keyword": "running shoes"
}
```
某品牌 `sponsoredWeightedSov` 高但 `organicWeightedSov` 低，说明其高度依赖广告，可据此制定竞争策略。

## 展示规则

1. **品牌表**：按 `combinedWeightedSov` 降序展示品牌表，高亮**前5个品牌**便于快速把握
2. **SOV 显示为百分比**：SOV 值乘以100显示为百分比，如 0.152 → 15.2%
3. **上下文标题**：表格前展示该关键词的30天搜索量（`estimated30DaySearchVolume`）和 PPC 竞价中位数（`exactSuggestedBidMedian`）作为背景
4. **TOP ASIN 区块**：单独展示 TOP3 ASIN 表，含点击量、转化量、转化率
5. **竞争概况**：数据后给出简要竞争格局概述——该关键词是被少数品牌主导还是分散，并指出自然与广告存在感之间的大差距
6. **错误处理**：查询失败时根据错误响应说明原因，并建议调整参数

## 用户表达与场景速查

**适用** —— 亚马逊搜索结果的品牌市场份额与竞争分析：

| 用户说 | 场景 |
|--------|------|
| "这个词谁占的份额最大" | 品牌垄断分析 |
| "这个关键词竞争激不激烈" | 竞争格局评估 |
| "广告位都被谁占了" | 广告 SOV 分析 |
| "有没有品牌垄断这个词" | 垄断检测 |
| "这个词的PPC出价大概多少" | PPC竞价估算 |
| "搜索结果里哪些品牌排前面" | 品牌可见度排名 |
| "这个词的转化率高不高" | TOP ASIN 转化分析 |

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

# Jungle Scout 关键词市场份额 Share of Voice API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/tool-jungle-scout/keywords/share-of-voice`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| marketplace | string | 是 | 目标市场代码。可选值：`us`、`uk`、`de`、`in`、`ca`、`fr`、`it`、`es`、`mx`、`jp` |
| keyword | string | 是 | 要查询的关键词 |

### 站点映射

| 站点 | marketplace 值 |
|------|---------------|
| 美国 | us |
| 英国 | uk |
| 德国 | de |
| 印度 | in |
| 加拿大 | ca |
| 法国 | fr |
| 意大利 | it |
| 西班牙 | es |
| 墨西哥 | mx |
| 日本 | jp |

## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| costToken | integer | 消耗 token 数 |
| shareOfVoice | object | Share of Voice 数据主体 |

### shareOfVoice 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 资源标识 |
| type | string | 固定值 `share_of_voice` |
| estimated30DaySearchVolume | integer | 过去 30 天精确匹配搜索量 |
| exactSuggestedBidMedian | number | PPC 竞价中位数（美元） |
| productCount | integer | 前 3 页搜索结果中的商品总数 |
| updatedAt | string | 数据更新时间 |
| topAsinsModelStartDate | string | TOP ASIN 点击/转化数据窗口起始日期 |
| topAsinsModelEndDate | string | TOP ASIN 点击/转化数据窗口结束日期 |
| brands | array | 品牌 SOV 明细列表 |
| topAsins | array | TOP 3 ASIN 点击转化列表 |

### brands 数组中每个对象

| 字段 | 类型 | 说明 |
|------|------|------|
| brand | string | 品牌名称 |
| organicProducts | integer | 自然搜索结果中的商品数量 |
| sponsoredProducts | integer | 广告位中的商品数量 |
| combinedProducts | integer | 综合商品数量 |
| organicBasicSov | number | 自然搜索基础 SOV（0–1） |
| organicWeightedSov | number | 自然搜索加权 SOV（0–1） |
| sponsoredBasicSov | number | 广告搜索基础 SOV（0–1） |
| sponsoredWeightedSov | number | 广告搜索加权 SOV（0–1） |
| combinedBasicSov | number | 综合基础 SOV（0–1） |
| combinedWeightedSov | number | 综合加权 SOV（0–1） |
| organicAveragePosition | number | 自然搜索平均排名位置 |
| sponsoredAveragePosition | number | 广告搜索平均排名位置 |
| combinedAveragePosition | number | 综合平均排名位置 |
| organicAveragePrice | number | 自然搜索商品平均价格 |
| sponsoredAveragePrice | number | 广告搜索商品平均价格 |
| combinedAveragePrice | number | 综合商品平均价格 |

### topAsins 数组中每个对象

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN 编号 |
| name | string | 商品名称 |
| brand | string | 品牌名称 |
| clicks | integer | 点击量（30 天窗口） |
| conversions | integer | 转化量（30 天窗口） |
| conversionRate | number | 转化率（0–1） |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `shareOfVoice` 对象 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | 积分/余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
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
curl -X POST https://tool-gateway.linkfox.com/tool-jungle-scout/keywords/share-of-voice \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "keyword": "portable charger"}'
```

## 响应示例

```json
{
  "costToken": 1,
  "shareOfVoice": {
    "id": "us_portable_charger",
    "type": "share_of_voice",
    "estimated30DaySearchVolume": 125000,
    "exactSuggestedBidMedian": 1.25,
    "productCount": 60,
    "updatedAt": "2026-04-10T00:00:00",
    "topAsinsModelStartDate": "2026-03-11",
    "topAsinsModelEndDate": "2026-04-10",
    "brands": [
      {
        "brand": "Anker",
        "organicProducts": 5,
        "sponsoredProducts": 3,
        "combinedProducts": 8,
        "organicBasicSov": 0.083,
        "organicWeightedSov": 0.112,
        "sponsoredBasicSov": 0.15,
        "sponsoredWeightedSov": 0.18,
        "combinedBasicSov": 0.133,
        "combinedWeightedSov": 0.152,
        "organicAveragePosition": 12.4,
        "sponsoredAveragePosition": 5.0,
        "combinedAveragePosition": 9.5,
        "organicAveragePrice": 29.99,
        "sponsoredAveragePrice": 25.99,
        "combinedAveragePrice": 28.49
      }
    ],
    "topAsins": [
      {
        "asin": "B09V3KXJPB",
        "name": "Anker Portable Charger 10000mAh",
        "brand": "Anker",
        "clicks": 15200,
        "conversions": 4560,
        "conversionRate": 0.30
      }
    ]
  }
}
```
