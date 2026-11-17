---
name: linkfox-aba-intelligent-query
description: 提供亚马逊ABA（品牌分析）搜索词数据的查询与分析，涵盖15个站点近3年的周维度数据，用于关键词挖掘与市场趋势分析。
---

# 亚马逊 ABA 数据挖掘（ABA Intelligent Query）

本技能用于查询和分析亚马逊 ABA（Amazon Brand Analytics）搜索词数据，帮助卖家从搜索词报告中挖掘关键词机会、排名趋势与市场洞察。完整请求参数、响应字段与错误码见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询亚马逊 ABA 搜索词数据，覆盖 15 个站点、近 3 年的**周维度**历史数据。
- 通过自然语言 `analysisDescription` 精确描述查询意图，后端转化为结构化查询。
- 支持关键词热度排名趋势、黑马词发现、蓝海词挖掘、季节性关键词、高点击低转化 ASIN 诊断、竞品流量分布等场景。
- 可按需生成 CSV 下载链接（最多 10,000 条）。

### ❌ 边界与限制

- **数据粒度**：仅周维度，无日维度数据；历史范围约 3 年。
- **结果上限**：下载链接单次最多 10,000 条记录。
- **站点范围**：仅支持 15 个亚马逊站点（US、DE、BR、CA、AU、JP、AE、ES、FR、IT、SA、TR、MX、SE、NL），不含其他电商平台。
- **默认站点**：用户未指定站点时默认 US。
- **不在范围内**：广告/PPC 出价与投放策略；商品评论、Listing 文案撰写；ASIN 销量估算；用户已有本地 ABA 文件处理；利润测算、定价策略与综合市场报告。
- **成本约束**：本工具消耗积分，同一会话同一参数组合默认只调用一次；失败/空结果不得自动换关键词、翻页或改邮编连续试探。

## 核心概念

ABA（Amazon Brand Analytics）搜索词报告是亚马逊官方搜索行为数据，反映消费者真实搜索活动。本工具持有近 3 年的**周维度**数据，覆盖 15 个亚马逊站点。

**排名逻辑**：`searchFrequencyRank` 数值越小代表搜索热度越高，排名 1 为最热门搜索词。此处易混淆——用户说"排名提升"指数值变小；"排名下降"指数值变大。

### 数据字段

| 字段 | API 名称 | 说明 | 示例 |
|------|----------|------|------|
| 搜索词 | searchTerm | 消费者搜索关键词 | rimel loreal |
| 报告起始日期 | reportStartDate | 数据采集周起始日 | 2025-10-26 |
| 站点 | region | 亚马逊站点代码 | US |
| 搜索频率排名 | searchFrequencyRank | 搜索热度排名（越小越优） | 82135 |
| 被点击 ASIN | clickedAsin | 被点击商品的 ASIN | B0XXXXXXXX |
| 被点击商品名 | clickedItemName | 被点击商品名称 | xxx |
| 点击占比排名 | clickShareRank | 该 ASIN 在该搜索词下的点击占比排名 | 1 |
| 点击占比 | clickShare | 该 ASIN 占据的点击份额（0~1） | 0.28 |
| 转化占比 | conversionShare | 该 ASIN 占据的转化份额（0~1） | 0.3333 |

### 支持站点

US（美国）、DE（德国）、BR（巴西）、CA（加拿大）、AU（澳大利亚）、JP（日本）、AE（阿联酋）、ES（西班牙）、FR（法国）、IT（意大利）、SA（沙特）、TR（土耳其）、MX（墨西哥）、SE（瑞典）、NL（荷兰）。

用户未指定站点时默认 **US**。

## 调用方式

- **API 端点**：`POST /aba/intelligentQuery`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/aba_query.py '<JSON 参数>' [--inline]`
- **成本约束**：同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-aba-intelligent-query-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 查询构建

调用本工具的关键参数是 `analysisDescription`——用自然语言描述要查询的数据。该描述会在后端转化为结构化查询，因此需要**精确、具体**。

### analysisDescription 编写原则

1. **明确站点**：在开头说明站点，如"筛选美国站"。
2. **用精确筛选条件**：用具体数值区间而非模糊描述，"排名在5万以内"远优于"排名较好"。
3. **明确时间范围**：用具体时间描述，如"过去12周"、"2024年1-9月"、"近3个月"。
4. **明确对比基线**：做趋势分析时清楚说明对比的时间点，如"4周前的排名比8周前提升30%"。
5. **处理去重逻辑**：同一搜索词 + ASIN 组合有多条记录时，说明保留哪条，如"相同搜索词相同ASIN值保留最新的一个"。
6. **忠实用户意图**：不要曲解或过度扩展用户需求，准确反映其本意。

### 常见场景示例

**1. 搜索词热度趋势**
```
筛选美国站，关键词"gift"在过去12周的搜索热度排名。
```

**2. 上升黑马关键词**
```
筛选美国站，关键词包含"gift"，2025年Q1和全年的平均搜索排名都大于50万，但最新排名冲进5万-10万的搜索词。
```

**3. 持续增长趋势发现**
```
筛选美国站，最新排名在20万以内，且4周前的排名比8周前提升30%，本周的排名比4周前提升30%的搜索词。
```

**4. 市场机会发现（高搜索量、低垄断）**
```
筛选美国站，筛选当前搜索排名在20000以内，近三个月点击占比Top 1的Asin的转化率占比低于5%的搜索词。相同搜索词相同Asin值保留最新的一个。
```

**5. 季节性/节日关键词定位**
```
筛选美国站，包含"cup"的关键词中，去年（2024年）1-9月份排名未进入50万，10-11月份连续进入20万的词。
```

**6. 高点击低转化 ASIN 挖掘**
```
筛选美国站关键词包含"hat"的，最新搜索排名在5万-20万之间，且近3个月来点击占比大于20%，转化占比小于10%的ASIN。相同搜索词和ASIN仅保留点击占比和转化占比的比例最小数据。
```

**7. 高 ROAS 长尾蓝海词**
```
筛选美国站，关键词包含"charger"的，当前排名在20万开外的，近2个月的平均转化占比大于平均转化占比1.5倍的关键词，以及相应的ASIN。
```

**8. 新市场词与新兴需求探测**
```
找到美国站"charger"的长尾词中，近一个月才进入排名榜单，且当前排名在50万以内的所有词。
```

**9. 利基趋势/变体增长捕捉**
```
筛选美国站中"table"的长尾词中，排名在10万-30万之间，且近4周的搜索排名增长50%以上的搜索词。
```

## 展示规则

1. **只呈现数据**：以清晰表格展示查询结果，不做主观商业建议。
2. **排名澄清**：展示排名数据时提醒用户数值越小排名越优。
3. **体量提示**：结果较大时展示核心数据并提醒用户可通过下载链接获取完整数据。
4. **下载引导**：响应含 `downloadUrl` 时明确告知下载地址；用户需要全量数据但未请求下载时，主动建议生成下载链接。
5. **错误处理**：查询失败时依据 `msg` 字段说明原因，并建议调整查询条件。

## 用户表达与场景速查

**适用** —— 围绕亚马逊搜索词的数据查询：

| 用户说 | 场景 |
|--------|------|
| "XX 关键词搜索量/热度怎么样" | 排名趋势 |
| "最近火的词"、"新冒出来的词" | 黑马/新词探测 |
| "蓝海词"、"低竞争词" | 市场机会发现 |
| "哪些词转化好"、"高转化长尾" | 高 ROAS 关键词库 |
| "季节性词"、"旺季爆发的词" | 季节性关键词 |
| "流量被谁占了"、"有没有垄断" | 点击占比/垄断分析 |
| "高点击低转化的 ASIN" | 高点击低转化诊断 |

不适用场景见上方【能力边界】。

**边界判断**：用户说"选品"、"竞品分析"、"有没有市场机会"时，若本质是搜索词级数据查询（找蓝海词、分析关键词下竞品流量分布），则适用本技能；若问利润空间、定价策略或综合市场报告，则不适用。

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

# ABA 智能查询 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/aba/intelligentQuery`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| analysisDescription | string | 是 | 精确描述查询意图的自然语言 |
| region | string | 否 | 站点代码，默认 `US`。可选值：US、DE、BR、CA、AU、JP、AE、ES、FR、IT、SA、TR、MX、SE、NL |
| createDownloadUrl | boolean | 否 | 是否生成CSV下载链接，默认 `false` |

- 当用户明确要求"下载"、"导出"、"生成文件"时，将 `createDownloadUrl` 设为 `true`

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| success | boolean | 是否查询成功 |
| tables | array | 结果数据数组，每个元素包含 `data`（数据行）、`columns`（列定义）、`name`（Sheet名称） |
| total | integer | 结果总数 |
| downloadUrl | string | 当 `createDownloadUrl` 为 true 时返回CSV文件地址 |
| msg | string | 附加消息 |
| downloadNote | string | 下载相关提示 |
| code | string | 返回码 |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗token |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `tables` / `data` 等业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
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
curl -X POST https://tool-gateway.linkfox.com/aba/intelligentQuery \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"analysisDescription": "筛选美国站，关键词gift在过去12周的搜索热度排名", "region": "US"}'
```
