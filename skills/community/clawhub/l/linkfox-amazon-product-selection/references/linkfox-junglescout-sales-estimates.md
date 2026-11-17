---
name: linkfox-junglescout-sales-estimates
description: 利用Jungle Scout查询指定亚马逊ASIN的每日预估销量与最新价格走势，实现对竞品销量的精准监控。
---

# Jungle Scout — ASIN 销售估算

本技能通过 Jungle Scout 数据源查询指定亚马逊 ASIN 在一段时间内的每日预估销量与最近已知价格，返回日维度数据点，覆盖 10 个亚马逊站点。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询单个亚马逊 ASIN 在指定日期范围内的**每日预估销量**与**最近已知价格**。
- 覆盖美国、英国、德国、印度、加拿大、法国、意大利、西班牙、墨西哥、日本共 10 个站点。
- 用于监控竞品日销量、验证选品机会、追踪季节性规律、评估定价影响、追踪新品爬升曲线。

### ❌ 边界与限制

- **endDate 不可包含今天及未来**：`endDate` 必须早于当前日期，不能查询今天及未来的销量。
- **单次单 ASIN**：每次调用只能查询一个 ASIN；对比多个 ASIN 需分多次调用。
- **所有参数必填**：`marketplace`、`asin`、`startDate`、`endDate` 缺一不可。
- **价格为美元**：`lastKnownPrice` 单位为 USD，非本地货币。
- **数据有滞后**：不含实时/当前时刻销量。
- **不在范围内**：关键词搜索量（用关键词历史搜索量工具）、BSR 排名历史（用 BSR 追踪工具）、类目整体销量/市场规模、非亚马逊平台的销量数据。

## 核心概念

Jungle Scout ASIN 销售估算工具提供亚马逊各站点单个 ASIN 的**日维度预估销量**及**最近已知价格**。

- **监控竞品销量**：了解竞品每日出单量，评估其市场份额
- **验证选品机会**：用实际销量数据验证产品需求是否足够大
- **追踪季节性规律**：观察产品在不同月份的销量波动，判断旺淡季
- **评估定价影响**：结合价格与销量的变化关系，辅助定价决策
- **新品表现跟踪**：追踪新品上架后的销量爬升曲线

**数据粒度**：每条记录代表 1 天，包含该日的预估售出件数和最近已知价格（美元）。

**支持站点**：`us`、`uk`、`de`、`in`、`ca`、`fr`、`it`、`es`、`mx`、`jp`，默认 `us`。

## 调用方式

- **API 端点**：`POST /tool-jungle-scout/sales-estimates/query`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/junglescout_sales_estimates.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-junglescout-sales-estimates-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录；`<session>` 取自环境变量 `SESSION_ID`；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

四个参数均为**必填**：`marketplace`、`asin`、`startDate`、`endDate`。

**查询构建原则**：
1. **站点映射**：用户说"美国站"→ `us`，"日本站"→ `jp`，"德国站"→ `de`；未指定时默认 `us`
2. **日期格式**：必须为 `YYYY-MM-DD`，如 `2026-03-01`
3. **endDate 限制**：`endDate` 必须早于当前日期（不能包含今天及未来日期）
4. **ASIN 格式**：标准亚马逊 ASIN，通常以 B0 开头，共 10 位
5. **常用时间推算**：
   - "过去30天" → endDate 取昨天，startDate 取 30 天前
   - "上个月" → 上月 1 日到上月末日
   - "Q3 vs Q4" → 分两次调用，分别查 7-9 月和 10-12 月

**1. 查看竞品最近30天的销量**
```json
{
  "marketplace": "us",
  "asin": "B0CXXX1234",
  "startDate": "2026-03-18",
  "endDate": "2026-04-16"
}
```

**2. 对比 Q3 与 Q4 销量表现**

分两次调用：
- Q3：`startDate=2025-07-01`, `endDate=2025-09-30`
- Q4：`startDate=2025-10-01`, `endDate=2025-12-31`

**3. 验证选品机会——查看产品全年销量**
```json
{
  "marketplace": "us",
  "asin": "B0CXXX5678",
  "startDate": "2025-04-01",
  "endDate": "2026-03-31"
}
```

**4. 追踪新品上架表现**
```json
{
  "marketplace": "de",
  "asin": "B0DYYY9999",
  "startDate": "2026-01-15",
  "endDate": "2026-04-15"
}
```

**5. 监控大促期间销量变化（如 Prime Day）**
```json
{
  "marketplace": "us",
  "asin": "B0CXXX1234",
  "startDate": "2025-07-01",
  "endDate": "2025-07-21"
}
```

## 展示规则

1. **折线图优先**：建议以折线图展示每日销量变化，横轴为日期，纵轴为预估日销量；如有价格数据可叠加第二 Y 轴显示价格走势
2. **表格辅助**：同时提供数据表格供精确查阅，列包括：日期、预估销量、最近已知价格
3. **汇总统计**：在数据之后汇总关键指标——总销量、日均销量、预估总收入（总销量 × 均价）
4. **趋势总结**：简要总结趋势方向（上升/下降/平稳/周期性波动），标注销量峰值和谷值日期
5. **错误处理**：查询失败时根据错误响应说明原因，并建议调整参数（如 endDate 不能包含今天或未来日期）

## 用户表达与场景速查

**适用** —— ASIN 销售估算与销量趋势分析：

| 用户说 | 场景 |
|--------|------|
| "这个ASIN一天能卖多少" | 查询近期日销量估算 |
| "竞品最近卖得怎么样" | 监控竞品近30天销量 |
| "这个产品有没有季节性" | 全年销量数据判断季节规律 |
| "帮我看看这个品的销量趋势" | 指定时间段的销量走势 |
| "Q4旺季销量如何" | 特定季度销量查询 |
| "这个产品值不值得做" | 通过历史销量验证选品机会 |
| "大促期间卖了多少" | 活动期间销量监控 |

不适用场景见上方【能力边界】。

**边界判断**：当用户说"销量""日销""卖了多少"时，若想看某个 ASIN 在一段时间内的每日预估销量，适用本技能；若想要关键词搜索量、类目排名或实时销量，则不适用。

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

# Jungle Scout ASIN 销售估算 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/tool-jungle-scout/sales-estimates/query`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| marketplace | string | 是 | 目标市场代码。可选值：`us`、`uk`、`de`、`in`、`ca`、`fr`、`it`、`es`、`mx`、`jp` |
| asin | string | 是 | 要查询的亚马逊 ASIN |
| startDate | string | 是 | 开始日期（格式：YYYY-MM-DD） |
| endDate | string | 是 | 结束日期（格式：YYYY-MM-DD）；必须早于当前日期 |

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
| salesEstimateList | array | 销售估算结果列表 |

### salesEstimateList 数组中每个对象

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | 查询的 ASIN |
| id | string | 数据点标识 |
| type | string | 资源类型，固定值 `sales_estimate_result` |
| parentAsin | string | 父体 ASIN（变体场景下返回） |
| isParent | boolean | 是否为父体商品 |
| isVariant | boolean | 是否为变体商品 |
| isStandalone | boolean | 是否为独立商品（非变体） |
| variants | array | 该父体下的变体 ASIN 数组 |
| dailyEstimates | array | 每日估算数据数组 |

### dailyEstimates 数组中每个对象

| 字段 | 类型 | 说明 |
|------|------|------|
| date | string | 数据日期（YYYY-MM-DD） |
| estimatedUnitsSold | integer | 当日预估售出件数 |
| lastKnownPrice | number | 最近已知价格（USD） |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `salesEstimateList` |
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
curl -X POST https://tool-gateway.linkfox.com/tool-jungle-scout/sales-estimates/query \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "us", "asin": "B0CXXX1234", "startDate": "2026-03-01", "endDate": "2026-03-31"}'
```

## 响应示例

```json
{
  "costToken": 1,
  "salesEstimateList": [
    {
      "asin": "B0CXXX1234",
      "id": "sales_estimate_B0CXXX1234_20260301",
      "type": "sales_estimate_result",
      "parentAsin": "B0CXXX0000",
      "isParent": false,
      "isVariant": true,
      "isStandalone": false,
      "variants": [],
      "dailyEstimates": [
        {
          "date": "2026-03-01",
          "estimatedUnitsSold": 35,
          "lastKnownPrice": 29.99
        },
        {
          "date": "2026-03-02",
          "estimatedUnitsSold": 42,
          "lastKnownPrice": 29.99
        },
        {
          "date": "2026-03-03",
          "estimatedUnitsSold": 38,
          "lastKnownPrice": 27.99
        }
      ]
    }
  ]
}
```
