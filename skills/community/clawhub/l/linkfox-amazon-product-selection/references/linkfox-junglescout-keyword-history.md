---
name: linkfox-junglescout-keyword-history
description: 利用Jungle Scout查询亚马逊关键词的历史精确搜索量趋势（按7天周期），用于分析市场季节性和搜索量波动。
---

# Jungle Scout — 关键词历史搜索量

本技能通过 Jungle Scout 数据源查询亚马逊关键词的周维度精确匹配搜索量历史数据，用于分析季节性、趋势方向与波动幅度。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询指定关键词在一段时间内的**周维度精确匹配搜索量**历史数据（每 7 天一个数据点）。
- 覆盖美国、英国、德国、印度、加拿大、法国、意大利、西班牙、墨西哥、日本共 10 个亚马逊站点。
- 分析关键词的季节性规律、趋势方向（上升/下降/平稳）、波动幅度与节假日效应。

### ❌ 边界与限制

- **时间跨度上限**：单次查询 `startDate` 到 `endDate` 最长 366 天，超过需拆分查询。
- **数据粒度**：周维度（7 天一个数据点），非日维度。
- **搜索量类型**：精确匹配搜索量（Exact Match），非广泛匹配。
- **所有参数必填**：`marketplace`、`keyword`、`startDate`、`endDate` 缺一不可。
- **不在范围内**：关键词建议/拓词（需关键词挖掘工具）；实时/当前搜索量排名（需 ABA 或 SIF 工具）；关键词竞争度与 CPC 出价；商品销量与 listing 分析；非亚马逊平台的搜索量。

## 核心概念

Jungle Scout 关键词历史搜索量工具提供亚马逊各站点关键词的**周维度精确匹配搜索量**历史数据。卖家可通过查询指定时间范围内的搜索量变化判断：

- **季节性规律**：关键词在哪些月份是旺季/淡季
- **趋势方向**：搜索量是持续上升、下降还是平稳
- **波动幅度**：判断市场需求的稳定性
- **节假日效应**：大促、节日前后的搜索量飙升

**数据粒度**：每条记录代表一个 **7 天周期**，包含该周内的精确匹配搜索量估算值。默认站点为 `us`，用户未指定时使用 `us`。

## 调用方式

- **API 端点**：`POST /tool-jungle-scout/keywords/historical-search-volume`（完整参数/响应/错误码见 [references/api.md](references/api.md)）
- **Python 脚本**：`python scripts/junglescout_keyword_history.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-junglescout-keyword-history-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录；`<session>` 取自环境变量 `SESSION_ID`；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

所有四个参数均为**必填**：`marketplace`、`keyword`、`startDate`、`endDate`。日期格式为 `YYYY-MM-DD`，站点映射见 [references/api.md](references/api.md)。

**1. 查看关键词近半年搜索趋势**
```json
{"marketplace": "us", "keyword": "yoga mat", "startDate": "2025-10-01", "endDate": "2026-03-31"}
```

**2. 判断关键词季节性（查全年数据）**
```json
{"marketplace": "us", "keyword": "christmas decorations", "startDate": "2025-01-01", "endDate": "2025-12-31"}
```

**3. 对比旺季与淡季搜索量**

分两次调用：
- 淡季：`startDate=2025-02-01`, `endDate=2025-04-30`
- 旺季：`startDate=2025-10-01`, `endDate=2025-12-31`

**4. 多站点对比**

对同一关键词分别查询不同 marketplace（如 `us`、`de`、`jp`），比较各站搜索量规模。

**5. 验证市场需求是否增长**
```json
{"marketplace": "de", "keyword": "luftreiniger", "startDate": "2025-04-01", "endDate": "2026-03-31"}
```

## 展示规则

1. **趋势可视化优先**：建议以时间线/折线图方式展示搜索量变化，横轴为日期周期，纵轴为搜索量。
2. **表格辅助**：同时提供数据表格供精确查阅，列包括：周期开始日期、周期结束日期、搜索量。
3. **趋势总结**：在数据之后简要总结趋势方向（上升/下降/平稳/周期性波动），标注峰值和谷值周期。
4. **峰值标注**：高亮搜索量最高和最低的周期，便于用户快速判断旺淡季。
5. **错误处理**：查询失败时根据错误响应说明原因并建议调整参数（如日期范围超 366 天）。

## 用户表达与场景速查

**适用** —— 关键词搜索量历史趋势分析：

| 用户说 | 场景 |
|--------|------|
| "这个词搜索量怎么变化的" | 搜索量趋势查询 |
| "这个品类有没有季节性" | 全年数据判断季节规律 |
| "搜索量最近在涨还是跌" | 近期趋势判断 |
| "什么时候是旺季" | 峰值周期识别 |
| "去年 Q4 搜索量多少" | 指定时间段搜索量查询 |
| "这个词在德国站热不热" | 非美国站搜索量查询 |
| "对比两个时间段的搜索量" | 旺淡季/同比对比 |

不适用场景见上方【能力边界】。

> 边界判断：当用户说"搜索量""关键词热度""市场需求趋势"时，若想看某个关键词在一段时间内的搜索量变化（历史趋势），适用本技能；若想要当前排名或热门关键词列表，则不适用。

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

# Jungle Scout 关键词历史搜索量 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/tool-jungle-scout/keywords/historical-search-volume`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| marketplace | string | 是 | 目标市场代码。可选值：`us`、`uk`、`de`、`in`、`ca`、`fr`、`it`、`es`、`mx`、`jp` |
| keyword | string | 是 | 要查询的关键词 |
| startDate | string | 是 | 开始日期（格式：YYYY-MM-DD） |
| endDate | string | 是 | 结束日期（格式：YYYY-MM-DD）；与 startDate 间隔最大 366 天 |

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

| 字段 | 类型 | 说明 |
|------|------|------|
| costToken | integer | 消耗 token 数 |
| historicalSearchVolumeList | array | 历史搜索量周期列表 |

### historicalSearchVolumeList 数组中每个对象

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 数据周期标识（市场/关键词/日期范围） |
| estimateStartDate | string | 周期开始日期（YYYY-MM-DD，7天统计周期起点） |
| estimateEndDate | string | 周期结束日期（YYYY-MM-DD，7天统计周期终点） |
| estimatedExactSearchVolume | integer | 该周期内精确匹配搜索量（次/周） |
| type | string | 资源类型，固定值 `historical_keyword_search_volume` |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `historicalSearchVolumeList` |
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
curl -X POST https://tool-gateway.linkfox.com/tool-jungle-scout/keywords/historical-search-volume \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "keyword": "yoga mat", "startDate": "2025-10-01", "endDate": "2026-03-31"}'
```

## 响应示例

```json
{
  "costToken": 1,
  "historicalSearchVolumeList": [
    {
      "id": "us_yoga_mat_20251005_20251011",
      "estimateStartDate": "2025-10-05",
      "estimateEndDate": "2025-10-11",
      "estimatedExactSearchVolume": 85420,
      "type": "historical_keyword_search_volume"
    },
    {
      "id": "us_yoga_mat_20251012_20251018",
      "estimateStartDate": "2025-10-12",
      "estimateEndDate": "2025-10-18",
      "estimatedExactSearchVolume": 87650,
      "type": "historical_keyword_search_volume"
    }
  ]
}
```
