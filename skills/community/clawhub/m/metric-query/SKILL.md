---
name: metric-query
description: |
  构建指标平台（语义层）的指标数据查询 API 请求。当用户需要查询指标数据、构造指标查询API请求体、使用同环比/占比/排名/时间限定等快速计算、定义临时指标、设置维度筛选过滤条件时，必须使用此 Skill。
  触发场景包括但不限于：用户提到"查询指标"、"指标API"、"指标数据"、"语义层查询"、"metrics query"、"同环比"、"占比"、"排名"、"时间限定"、"metricDefinitions"、"timeConstraint"、"filters"、"dimensions"，或需要帮助构造指标查询的 JSON 请求体时都应使用此 Skill。即使用户只是问如何筛选数据、如何做同比环比、如何定义临时指标，也应触发此 Skill。
  **重要：构建查询前，必须先通过 Gateway API 检索相关指标和维度信息，禁止凭记忆猜测指标名或维度名。**
permissions:
  - env:read 
  - network:outbound 
env_vars:
  - name: "CAN_API_KEY"
    description: "Aloudata CAN网关API访问密钥，需用户自行在~/.openclaw/.env中配置"
    required: true
domain_whitelist:
  - "gateway.can.aloudata.com" 
version: "1.0.2"
author: "Aloudata"
homepage: "https://aloudata.com/"
metadata.openclaw: {"emoji": "🔍"}
---

# 指标数据查询 API Skill

根据用户自然语言描述，**先通过 Gateway 检索指标和维度**，再生成语义接口 `/semantic/api/v1.1/metrics/query` 的请求体 JSON。

---

## 接口信息

### Gateway 搜索 API（Step 1 — 检索指标和维度）

**搜索指标**: GET `https://gateway.can.aloudata.com/api/metrics/search?keyword={关键词,可逗号分隔}&pageSize={数量}`
**单指标维度**: GET `https://gateway.can.aloudata.com/api/metrics/{metricName}/dimensions?keyword={可选过滤词}`
**批量指标维度**: GET `https://gateway.can.aloudata.com/api/metrics/dimensions?metricNames={指标1,指标2}&keyword={可选过滤词}`
**指标列表**: GET `https://gateway.can.aloudata.com/api/metrics/list?pageNumber={页码}&pageSize={数量}`
**指标目录**: GET `https://gateway.can.aloudata.com/api/metrics/categories`
**目录下指标**: GET `https://gateway.can.aloudata.com/api/metrics/categories/{categoryId}?pageSize={数量}`
**认证方式**：所有请求必须携带 API Key，通过请求头 `X-API-Key` 传递（也可通过 `?apikey=` 查询参数传递）。**返回格式为纯文本**，非 JSON。

**⚠️ 调用 Gateway 的两条铁律**：
1. **所有请求必须加 API Key 认证头 `-H "X-API-Key: $CAN_API_KEY"`**，`$CAN_API_KEY` 从环境变量读取（用户需在 `~/.openclaw/.env` 中配置 `CAN_API_KEY=cgk-xxxxxxxx`），未携带或无效 Key 将返回 401
2. **URL 中文参数必须 URL 编码**，使用 `--data-urlencode` + `-G` 让 curl 自动编码，禁止中文直接拼入 URL

> 示例：
> ```bash
> # 搜索单个指标
> curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/search?pageSize=5" --data-urlencode "keyword=客单价" -G
> # 批量搜索多个指标（逗号分隔）
> curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/search?pageSize=3" --data-urlencode "keyword=客单价,销售额" -G
> # 单指标维度查询（路径参数直接用 metricName）
> curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/AOV/dimensions"
> # 按关键词过滤维度（只返回匹配的维度，keyword 支持逗号分隔多关键词，匹配任一即返回）
> curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/AOV/dimensions" --data-urlencode "keyword=渠道" -G
> # 多关键词过滤维度（逗号分隔，匹配维度名/展示名/描述/维度值样本中任一关键词的维度都会返回）
> curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/AOV/dimensions" --data-urlencode "keyword=渠道,地区,品牌" -G
> # 批量指标维度查询（自动计算维度交集，keyword 同样支持多关键词）
> curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/dimensions?metricNames=AOV,retail_amt" --data-urlencode "keyword=渠道" -G
> # 指标目录（查看所有类目层级）
> curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/categories"
> # 查看指定目录下的指标
> curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/categories/{categoryId}?pageSize=20"
> # 指标列表（分页浏览全部指标）
> curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/list?pageNumber=1&pageSize=50"
> ```

### 指标查询 API（Step 2 — 执行数据查询）

**接口**: POST `https://gateway.can.aloudata.com/api/metrics/query`
**认证方式**：同上，必须携带 API Key 认证头。

> 示例（⚠️ 因为 timeConstraint 含单引号 `['metric_time']`，必须用 heredoc 传 JSON body，禁止用 `-d '...'` 单引号包裹）：
> ```bash
> curl -X POST "https://gateway.can.aloudata.com/api/metrics/query" \
>   -H "X-API-Key: $CAN_API_KEY" \
>   -H "Content-Type: application/json" \
>   -d @- <<'EOF'
> {"metrics": ["AOV"], "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"}
> EOF
> ```

---

## ⚡ 九条铁律（违反任何一条 = 错误）

构建 JSON 前，先逐条过一遍：

**铁律 1 — 相对时间必须用 NOW()，禁止硬编码日期（包括 timeConstraint 和 period 锚定）**
"上月""上周""本年""昨天""近N天""去年""本季""上季" 等相对时间 → **必须** `NOW()`。
- ✅ `DATEADD(DateTrunc(NOW(), "MONTH"), -1, "MONTH")`
- ❌ `DATEADD(DateTrunc('2026-03-05', "MONTH"), -1, "MONTH")`
- 唯一例外：用户明确说了"2025年4月"这样的具体日期 → 才可用 `"2025-04-01"`

**⚠️ 特别注意：period 锚定的 timeConstraint 也必须用 NOW()**
当使用 metricDefinitions + period 时，timeConstraint 作为 period 的锚定基准。如果用户说的是"本年至今""本月至今""近30天"等相对时间，锚定日期必须用 `DATEADD(DateTrunc(NOW(), "DAY"), -1, "DAY")` 表示"昨天"，**绝不可**将当前日期（如 `2026-03-06`）直接写入 timeConstraint。
- ✅ `"timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"`
- ❌ `"timeConstraint": "['metric_time__day']= \"2026-03-06\""`（硬编码当前日期）
- ❌ `"timeConstraint": "['metric_time__day']= \"2026-03-05\""`（硬编码昨天日期）

**铁律 2 — metricDefinitions 中每个 key 必须同时在 metrics 数组中（包括辅助指标）**
定义了就必须注册。自检：数 metricDefinitions 的 key → 逐个确认在 metrics 中存在。
**⚠️ 特别注意"辅助指标"**: 即使某个临时指标仅作为 `expr` 的中间计算变量（如 `"total": { "refMetric": "metric_A", "specifyDimension": ... }` 被 `"ratio": { "expr": "[val]/[total]" }` 引用），该辅助指标**也必须**出现在 metrics 数组中。API 不会自动推断依赖关系——metricDefinitions 中的每个 key 无论是最终输出还是中间计算，都需要在 metrics 中显式注册。
- ❌ `"metrics": ["ratio"]` + `"metricDefinitions": { "total": {...}, "ratio": { "expr": "[val]/[total]" } }`（`total` 未注册）
- ✅ `"metrics": ["total", "ratio"]` + `"metricDefinitions": { "total": {...}, "ratio": { "expr": "[val]/[total]" } }`

**铁律 3 — 占比/排名 + filters = 分母/范围被缩小 → 结果恒 100%/恒为 1**
要"某个值在全局中的占比/排名" → 用 **resultFilters** 做展示筛选，**不用 filters**。

**⚠️ 特别注意"渠道内占比/排名"场景**: 当用户问"Wholesale 渠道的**渠道内占比/排名**"时，含义是 Wholesale 在所有渠道中的占比/排名。此时：
- dimensions 必须包含渠道维度（如 `first_channel`），让所有渠道参与占比/排名计算
- 用 `resultFilters` 仅展示 Wholesale 的行
- ❌ 错误：`"filters": ["[first_channel]= \"Wholesale\""]` → 只剩 Wholesale 自己，占比恒 100%、排名恒 1
- ✅ 正确：`"resultFilters": ["[first_channel]= \"Wholesale\""]` → 分母包含所有渠道

**铁律 4 — "同比"默认 = yoy；带粒度前缀时按前缀选择**
- 无限定 / "年同比" → `yoy`
- "月同比" → `mom`（与上月同期比）
- "周同比" → `wow`（与上周同期比）
- "季同比" → `qoq`（与上季同期比）
- ⚠️ 中文"同比"单独出现、无粒度前缀时，**一律映射为 yoy**，不可映射为 mom/qoq/wow

**铁律 5 — 一个指标只能做一次快速计算，不可链式叠加**
需要多步（如先算环比再排名）→ 用 metricDefinitions 分步。
- ❌ `retail_amt__sameperiod__mom__growth__rank__desc__first_channel`（链式：环比 + 排名）
- ❌ `retail_amt__sameperiod__yoy__growth__rankDense__desc__first_channel`（链式：同比 + 排名）
- ✅ 正确做法：先用 metricDefinitions 定义环比/同比临时指标，再对该临时指标做排名快速计算
```json
"metrics": ["mom_growth", "mom_growth__rankDense__desc__first_channel"],
"metricDefinitions": {
    "mom_growth": {
        "refMetric": "retail_amt",
        "indirections": ["sameperiod__mom__growth"]
    }
}
```
**典型场景——"各渠道增速前N的品牌"**: 这类需求必须分步：第1步用 metricDefinitions 定义环比增速临时指标；第2步对临时指标做渠道内排名。

**铁律 6 — MetricMatches 只能在 metricDefinitions 的 filters 中使用，禁止放在顶层 filters**
MetricMatches 是"基于指标值筛选维度值"的高级功能，**必须**包裹在临时指标定义（metricDefinitions）的 filters 中。
- ✅ `"metricDefinitions": { "temp": { "refMetric": "buyer_cnt", "filters": ["MetricMatches([vip_code], [retail_amt] >= 10000)"] } }`
- ❌ `"filters": ["MetricMatches([vip_code], [retail_amt] >= 10000)"]`（顶层 filters 不支持 MetricMatches）

**铁律 7 — 派生指标的 metric_time 粒度限制必须遵守**
候选指标中标注"metric_time维度仅支持日粒度"的派生指标（如 sales_yoy、retail_amt_ytd 等），**只能在 timeConstraint 锚定到天粒度时使用**（如 `['metric_time__day']= ...`）。当 timeConstraint 为周/月/季/年粒度时，**禁止使用**这些日粒度限制的派生指标，必须改用原子指标 + 快速计算语法。
- ✅ 上月销售额同比 → `retail_amt__sameperiod__yoy__growth`（原子指标+快速计算）
- ❌ 上月销售额同比 → `sales_yoy`（日粒度派生指标 + 月级 timeConstraint = 不兼容）

**铁律 8 — "月变化趋势"中的占比/排名范围维度必须是 metric_time__month**
当查询涉及"XX在YY内排名/占比的**月变化趋势**"时，范围维度必须是 `metric_time__month`（每月内独立计算排名/占比），而**非**实体维度或留空。
- ✅ `retail_amt__proportion__metric_time__month`（每月内各渠道占比）
- ✅ `retail_amt__rank__desc__metric_time__month`（每月内各渠道排名）
- ❌ `retail_amt__proportion__`（全局占比，无月内分组 → 排名/占比跨月混淆）
- ❌ `retail_amt__proportion__first_channel`（每渠道内占比 → 恒100%）

**铁律 9 — 上下文不足时必须拒绝生成查询，返回空 JSON `{}`，禁止虚构指标或忽视维度兼容性**
在生成 JSON 前，必须执行以下三项上下文充分性检查。任何一项不通过，**必须拒绝生成查询**，在 buildReason 中说明缺失原因，并返回空 JSON `{}`。
- **检查 A — 候选指标覆盖性**: 用户核心需求能否在候选指标表中找到对应指标？没有 → 禁止虚构指标名
- **检查 B — 维度兼容性**: 所选指标的「可分析维度」是否包含你要用的维度？不包含 → 禁止使用该维度
- **检查 C — 非查询意图**: 用户消息是纯问候或不含查询意图 → 返回空 JSON `{}`

> **核心原则**: 宁可在 buildReason 中诚实说明"候选指标/维度不足以回答此问题"，也不要为了"产出内容"而硬凑一个错误的查询。错误的查询比没有查询更有害——它会返回误导性数据。

---

## 0. 语义理解（构建前必做）

**⚠️ 非查询意图判断**: 如果用户消息**不包含任何数据查询意图**（如"你好""谢谢""当前日期是XX"等对话性消息），则**不应生成查询请求体**。此时应返回空 JSON `{}` 或在 buildReason 中说明"用户消息不含查询意图"。切勿为了"产出内容"而生成一个空 metrics 或无意义的请求体。

在写任何 JSON 之前，先把用户的问题拆解为四个维度：

| 维度 | 问自己 | 示例 |
|------|-------|------|
| **看什么**（指标） | 用户要看的业务量是什么？有没有修饰语（日均、不含税…）？ | "销售额""日均订单数""客单价（不含税）" |
| **怎么看**（分析方式） | 直接看值？还是要对比/占比/排名/趋势？ | "同比增长率""占比""排名前5""月趋势" |
| **看谁的**（维度 & 筛选） | 按什么维度拆分？筛选哪些范围？ | "各品牌""某渠道""某地区" |
| **看哪段时间**（时间） | 时间范围是什么？是否涉及时间对比？ | "上月""近7天""某月 vs 另一月" |

### 0.1 关键语义消歧

以下 9 条规则解决的是"怎么理解用户的中文"，而非"怎么写 JSON"。

**规则 A — "总和" vs "分别"**

| 用户说 | 含义 | dimensions 处理 |
|-------|------|----------------|
| "A 和 B 的某指标**分别**是多少" | 按 A、B 分组展示 | 保留维度 |
| "A 和 B 的某指标**总和**" | A+B 合并为一个数字 | 不放该维度 |
| "A 和 B 的某指标"（无修饰） | 歧义，默认"分别" | 保留维度 |

**规则 B — 修饰语的作用域**

"日均/月均/平均" 修饰的是**紧跟其后的所有并列项**：

- "各时段的**日均**某指标" → 所有时段都算日均
- "**总**指标A和**日均**指标B" → 指标A取总量，指标B取日均
- "上年末、本年至今…的**日均某指标**" → 所有时段全部算日均

**规则 C — "占比" 的两种含义**

| 用户说 | 含义 | 实现方式 |
|-------|------|---------|
| "某指标**占比**"（如"销售额占比"） | 值占比（金额/数量占比） | 直接用 proportion 快速计算 |
| "**某实体**占比"（如"款色占比""客户占比""门店数占比"） | 数量占比 | 需要先用**计数指标**统计数量，再对计数指标做 proportion |

判断标准：如果"占比"前面是一个**实体类型**（款色、客户、门店、SKU）而非指标（销售额、订单数），则是数量占比。

**规则 D — "XX均" 的聚合维度**

"XX均"中的"XX"就是聚合维度，不要替换为其他维度。在候选维度表中找到"XX"对应的维度名称，用 `multi_level_agg__avg,{该维度名}` 实现。

示例：
- "**店**均" → 找到门店对应的维度名 → `multi_level_agg__avg,{门店维度}`
- "**人**均" → 找到客户对应的维度名 → `multi_level_agg__avg,{客户维度}`，或用 expr: `[总指标]/[计数指标]`

**规则 E — "同比" vs "环比"**

| 用户说 | 映射 | 说明 |
|-------|------|------|
| "同比"（无限定） | **yoy** | 默认=年同比，详见铁律 4 |
| "年同比" | **yoy** | |
| "月同比" | **mom** | 与上月同期比 |
| "周同比" | **wow** | 与上周同期比 |
| "季同比" | **qoq** | 与上季同期比 |
| "环比" | 根据时间粒度选：日→dod，周→wow，月→mom，季→qoq | ❌ 不可映射为 yoy |

**规则 F — "对比去年末" ≠ "年同比"**

| 用户说 | 含义 | 实现方式 |
|-------|------|---------|
| "同比""年同比" | 与**去年同期**对比 | `__sameperiod__yoy__growth` |
| "与**去年末**相比" | 与去年12月/去年最后一天对比 | metricDefinitions + period 定位去年末（如 `SPECIFY_DATE end day of -1 year`） |
| "与**上月末**相比" | 与上月最后一天对比 | `__sameperiod__moeom__growth`（需 day 粒度） |

**规则 G — "趋势" ≠ 同环比**

"趋势"/"变化趋势" = 按时间展开看值的变化，只需指标 + 时间维度。除非用户明确提到"同比""环比""增长率"，否则**不要**额外添加同环比指标。

**规则 H — "差异/差距/对比" ≠ 同环比**

"各XX之间的差异""A和B的差距" = 直接查出各自的值让用户比较，**不是**同比/环比。只有用户明确说"同比""环比""增长率"时才加同环比计算。

**规则 I — 简单优先**

如果用户问题可以用简单查询（指标 + 维度 + 时间）回答，就不要添加不必要的 metricDefinitions、同环比、占比、排名。例如：
- "昨天的同比增长率" → 直接 `metric_A__sameperiod__yoy__growth`，不需要 metricDefinitions
- "各渠道的销售额" → 直接查，不需要额外计算
- "日均销售额"（返回单个数字） → 用 metricDefinitions + period + preAggs `[{"granularity": "DAY", "calculateType": "AVG"}]`，**不要**在 dimensions 中加 `metric_time__day`（那样是按天展开，不是日均）
- "上月总销售额" → 只需 `retail_amt` + timeConstraint 上月，dimensions 为空，**不要**加 `metric_time__day` 展开

---

## 1. 参考数据（通过 Gateway API 动态获取）

**⚠️ 构建查询前，必须先通过 Gateway API 检索指标和维度，禁止凭记忆猜测。**

### 1.1 Step 1 — 搜索指标

从用户问题中提取核心业务关键词，调用 Gateway 搜索（**支持逗号分隔批量搜索**）：

```bash
# 单个关键词
curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/search?pageSize=5" --data-urlencode "keyword=客单价" -G
# 多个关键词（逗号分隔，中英文逗号均可）
curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/search?pageSize=3" --data-urlencode "keyword=客单价,销售额" -G
```

**返回纯文本格式**（已过滤非 ONLINE 指标），每行一个指标：
```
[客单价] 3 metric(s):
- AOV | 客单价 | 销售金额/购买客户数 (53 dims)
- l7d_AOV | 近7天客单价 [DERIVED] (53 dims)

[销售额] 2 metric(s):
- retail_amt | 销售金额 | 销售金额求和 (53 dims)
```
- 行首 `AOV` 是 **metricName**，放入 metrics 数组
- `[DERIVED]` = 派生指标，`(53 dims)` = 可用维度数量

**每次构建都做以下检查**：
1. 从返回结果中选择语义匹配的指标 → 取 **metricName**（行首英文名）放入 metrics
2. **已有派生指标须语义验证**：`[DERIVED]` 指标使用前必须确认其展示名语义与用户意图**完全一致**。
3. **维度兼容性**：多指标查询时，用批量维度接口自动算交集（见 Step 2）。

### 1.2 Step 2 — 查询维度（含维度值样本）

对 Step 1 选定的指标，调用 Gateway 获取可用维度。**支持单指标和批量指标两种方式**：

```bash
# 单指标维度（路径参数直接用 metricName）
curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/AOV/dimensions"
# 单指标 + keyword 过滤（大幅减少返回量，keyword 支持逗号分隔多关键词，匹配任一即返回）
curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/AOV/dimensions" --data-urlencode "keyword=渠道" -G
# 多关键词过滤维度（同时搜索多个维度方向，匹配维度名/展示名/描述/维度值样本中任一关键词）
curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/AOV/dimensions" --data-urlencode "keyword=渠道,地区,品牌" -G
# 批量指标维度（逗号分隔，自动计算维度交集，keyword 同样支持多关键词）
curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/dimensions?metricNames=AOV,retail_amt" --data-urlencode "keyword=渠道" -G
```

**单指标返回格式**：
```
Metric '客单价' (AOV), 53 dimension(s):
- first_channel(一级渠道): Direct, E-commerce, Retail, Wholesale
- gender(性别): 女, 男
```

**批量指标返回格式**（包含各指标维度 + 交集）：
```
## 客单价 (AOV), 2 dim(s):
- first_channel(一级渠道): Direct, E-commerce, Retail, Wholesale
- second_channel(二级渠道): Offline, Online

## 销售金额 (retail_amt), 2 dim(s):
- first_channel(一级渠道): Direct, E-commerce, Retail, Wholesale
- second_channel(二级渠道): Offline, Online

## COMMON dimensions (intersection), 2 dim(s):
- first_channel(一级渠道): Direct, E-commerce, Retail, Wholesale
- second_channel(二级渠道): Offline, Online
```
- 行首 `first_channel` 是 **dimName**，放入 dimensions / filters
- 冒号后是维度值样本
- **COMMON dimensions** 是多指标共有维度的交集，构建查询时 dimensions 只能从这里选

**⚠️ 优先使用 keyword 过滤**：当用户提到了具体的维度名或维度值（如"渠道""淘宝""女装"），用 `keyword` 参数过滤，只返回匹配的维度。**keyword 支持逗号分隔多关键词**（中英文逗号均可），匹配任一关键词即返回该维度，适合一次性搜索多个维度方向（如 `keyword=渠道,地区,品牌`）。匹配范围包括维度名、展示名、描述和维度值样本。
**⚠️ 多指标查询必须用批量接口**：一次拿到交集，避免多次调用。

**每次构建都做以下检查**：
1. 从返回结果中取 **dimName**（行首英文名）放入 dimensions / filters
2. **维度兼容性**：dimensions 中的**每一个**维度都必须出现在该指标的返回列表中
   - metric_time 是所有指标的可分析维度
   - metric_time__ 后的粒度后缀（`__day`, `__month`, `__year` 等）按指标类型限制：DERIVED 类型的时间限定派生指标通常仅支持 `__day` 粒度
3. **维度值匹配**：用 keyword 搜维度值可直接定位维度。例如用户说"淘宝" → 搜 `keyword=淘宝` → 返回 `order_platform_code(订单来源平台): ..., 天猫淘宝, ...`，直接用 `order_platform_code` 维度，filter 值为 `天猫淘宝`
4. **维度值精确抄写（⚠️ 极易出错）**：构建 filters 和 resultFilters 时，**必须严格按返回的维度值样本原始写法**填写，包括大小写、空格、标点符号
   - **规则：永远从返回的维度值样本中复制，不要自行猜测或规范化**
   - 如果样本值不包含用户提到的值，使用 `contains()` 模糊匹配或告知用户值可能不存在

---

## 2. JSON 格式规范

请求体为标准 JSON。**所有字符串值内部的双引号必须转义为 `\"`**。

```json
"filters": ["[dim_A]= \"value_1\""]
"timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = \"2025-04-01\""
```

---

## 3. 请求参数

### 3.1 metrics（必填）— 指标列表

```json
"metrics": ["metric_A", "metric_B"]
```

**快速计算不可链式叠加**（铁律 5）: 每个指标只能应用**一次**快速计算。需要多步计算时用 metricDefinitions 分步。

#### 3.1.1 同环比

**语法**: `{指标}__sameperiod__{偏移粒度}__{方法}`

**偏移粒度**:

| 用户说 | 偏移粒度 | | 用户说 | 偏移粒度 |
|-------|---------|---|-------|---------|
| 日环比 | `dod` | | 对比上月末 | `moeom` |
| 周环比 | `wow` | | 对比上季末 | `qoeoq` |
| 月环比 | `mom` | | 对比去年末 | `yoeoy` |
| 季环比 | `qoq` | | 对比上月初 | `mosom` |
| 年同比 | `yoy` | | 对比去年初 | `yosoy` |

所有偏移粒度支持 `{N}_` 前缀（如 `-2_yoy` = 2年前同期）。

> **选择规则**: "同比"→详见铁律 4；"环比"→按粒度选 `dod`/`wow`/`mom`/`qoq`。**仅当**用户明确说"对比XX期末/期初"时才用期末/期初偏移。

**方法**:

| 用户说 | 方法 | 计算 |
|-------|------|------|
| 同期/环比的值 | `value` | 对比期原值 |
| 增长了多少 | `growthvalue` | 当前 − 对比 |
| 增长率/增速 | `growth` | (当前 − 对比) / 对比 |
| 下降了多少 | `decrease` | 对比 − 当前 |
| 下降率 | `decreaserate` | (对比 − 当前) / 对比 |

**约束**: metric_time 须在 dimensions 或 timeConstraint 中出现；偏移粒度不可小于 metric_time 粒度；期末/期初偏移仅 `metric_time__day` 粒度可用。

**已有时间限定指标叠加同环比**: 候选指标中名称含时间限定后缀（如 `_ytd`、`_mtd` 等）的派生指标，可以叠加 `__sameperiod__` 快速计算，但必须：dimensions 含 `metric_time__day`，有 timeConstraint 锚定具体日期。**推荐用 metricDefinitions + period + indirections 替代**，语义更清晰。

#### 3.1.2 占比

**语法**: `{指标}__proportion__{范围维度}`

**数学含义**: `占比 = 当前行值 / 范围维度分组的汇总值`

| 范围维度写法 | 分母 |
|------------|------|
| `proportion__`（⚠️ 末尾有**两个下划线**，后面无维度名） | 全部数据汇总（全局占比） |
| `proportion__dim_A` | 按 dim_A 每组分别汇总（组内占比） |

> **选择规则**: 问"这一行占**谁**的比"。"占总体"→留空；"占 A 组内"→填 A。

**⚠️ 前提条件 — dimensions 必须包含参与占比计算的维度**: 使用 `proportion__`（全局占比）时，参与占比计算的实体维度（如渠道、品牌）**必须**出现在 `dimensions` 中，否则系统无法按该维度分组计算占比。
- ❌ `"dimensions": []` + `proportion__` → 没有分组维度，无法计算占比
- ✅ `"dimensions": ["first_channel"]` + `proportion__` → 按渠道分组，计算各渠道全局占比

**⚠️ 陷阱一 — 恒为 100%**: 范围维度覆盖了 dimensions 中所有非日期维度时，每行分母就是自己，占比恒为 100%。例如 `dimensions: ["dim_A"]` + `proportion__dim_A` → 100%。应改用 `proportion__`。

**⚠️ 陷阱二 — filters 缩小分母**: `filters` 在占比计算**前**过滤数据。如果用 filters 只留一个维度值，再算 `proportion__`，分母只有该值自身，占比恒为 100%。正确做法：用 **resultFilters** 做展示筛选。详见 §3.4 和示例 5.12。

#### 3.1.3 排名

**语法**: `{指标}__{方式}__{顺序}__{范围维度}`

- **方式**: `rank`（并列跳号）、`rankDense`（并列不跳）、`rowNumber`（不并列）
- **顺序**: `desc`（大=1）、`asc`（小=1）
- **范围维度**: 省略=全局排名；填 dim_A = dim_A 组内排名

**陷阱与占比完全相同**: 范围维度覆盖所有非日期维度 → 恒为 1；filters 缩小范围 → 排名失真。用 resultFilters 做展示筛选。

#### 3.1.4 时间限定

**语法**: `{指标}__period__{限定}`

| 类型 | 语法示例 |
|------|---------|
| 近N期 | `7d`, `3w`, `6m`, `2q`, `1y` |
| 本期至今 | `ytd`, `qtd`, `mtd`, `wtd` |
| 当前期间 | `cy`, `cq`, `cm`, `cw`, `cd` |

**约束**: 被引用指标不能已有时间限定；**必须有明确的时间锚定**（timeConstraint 或 dimensions 中的 metric_time）。

---

### 3.2 metricDefinitions（选填）— 临时指标定义

> **⚠️ 核心规则（铁律 2）— 必须双重注册**: metricDefinitions 中的**每一个** key **都必须同时出现在 metrics 数组中**（含辅助指标）。

**临时指标命名**: 必须与所有已有指标名称不同，避免命名冲突。建议加业务前缀/后缀以示区分。

```json
"metrics": ["my_temp_metric"],
"metricDefinitions": {
    "my_temp_metric": { "refMetric": "metric_A", ... }
}
```

**可配置属性**:

| 属性 | 说明 | 约束 |
|------|------|------|
| `refMetric` | 引用已有指标 | |
| `expr` | 复合表达式 `"[m1]+[m2]"` | 可引用其他临时指标 |
| `period` | 时间限定 | 仅支持相对偏移；`of` 后锚定粒度不可细于 timeConstraint 粒度 |
| `metricGrain` | 时间粒度 | DAY/WEEK/MONTH/QUARTER/YEAR |
| `preAggs` | 时间维度多层聚合 | **格式为数组** `[{...}]`；必须配合 period |
| `filters` | 业务限定 | 支持维度筛选和 MetricMatches |
| `indirections` | 衍生方式 | 同环比/占比/排名/多层聚合 |
| `specifyDimension` | 聚合维度控制 | `EXCLUDE` 排除外层分组影响 |

#### 3.2.1 period 语法

**仅支持相对日期偏移**，基于 timeConstraint 锚定的日期做偏移。

**`of` 后锚定粒度规则**: `of` 后的粒度**不可细于** timeConstraint 锚定粒度。
- timeConstraint 锚定到天 → `of` 可用 `day`、`week`、`month`、`quarter`、`year`
- timeConstraint 锚定到月 → `of` 可用 `month`、`quarter`、`year`（**不可用** `day`、`week`）

**to_date**（区间：偏移日 ~ 锚定日）:
```
"to_date -6 day of 0 day"    → 基准日前6天 ~ 基准日（共7日）
"to_date -29 day of 0 day"   → 共30日
"to_date -7 day of -1 day"   → 基准日前8天 ~ 前1天（共7日，不含基准日）
```

**grain_to_date**（某粒度起点 ~ 锚定点）:
```
"grain_to_date 0 year of 0 day"      → 本年初 ~ 基准日（本年至今）
"grain_to_date 0 month of 0 day"     → 本月初 ~ 基准日（本月至今）
"grain_to_date -1 year of -1 day"    → 去年初 ~ 去年的基准日前1天
"grain_to_date 0 year of 0 month"    → 本年初 ~ 基准月（锚定到月时）
```

**relative_date**（单一日期/月定位）:
```
"relative_date 0 month of 0 day"     → 基准日所在月
"relative_date -1 month of 0 day"    → 上月
"relative_date -5 month of 0 month"  → 5个月前（锚定到月时）
```

**SPECIFY_DATE**（期初/期末定位）:
```
"SPECIFY_DATE start day of -1 year"   → 上年第一天
"SPECIFY_DATE end day of -1 month"    → 上月最后一天
"SPECIFY_DATE end day of -1 year"     → 上年最后一天
"SPECIFY_DATE end month of -1 year"   → 上年最后一个月
```

**period 与 timeConstraint 配合**:
- timeConstraint 锚定到天 → period 用 `of 0 day` 表示该天
- timeConstraint 锚定到月 → period 用 `of 0 month` 表示该月
- 对比两个月份（如6月 vs 1月）→ timeConstraint 锚定到6月，period 用 `relative_date -5 month of 0 month` 定位1月

#### 3.2.2 preAggs（时间维度多层聚合）

**格式为数组**，必须配合 period。

```json
"preAggs": [{"granularity": "DAY", "calculateType": "AVG"}]
```

- `granularity`: DAY / WEEK / MONTH / QUARTER / YEAR
- `calculateType`: AVG / MAX / MIN

典型场景: "近30天日均" = period 限定30天 + preAggs 按 DAY 求 AVG。

**⚠️ preAggs 与 dimensions 中的时间粒度**: 使用 preAggs 按 DAY 聚合时，**不要**在外层 dimensions 中放 `metric_time__day`。preAggs 已经按日聚合再取 AVG/MAX/MIN，如果外层再按天展开，等于没有聚合。同理，preAggs 按 MONTH 聚合时不要在 dimensions 中放 `metric_time__month`。

**preAggs + 同比**: 含 preAggs 时不能直接叠加 `__sameperiod__`。须分别定义今年和去年的临时指标（各自含 period + preAggs），再用 expr 计算增长率。见示例 5.13。

#### 3.2.3 filters（业务限定）与 MetricMatches

临时指标可附加维度筛选：

```json
"my_metric": {
    "refMetric": "metric_A",
    "filters": ["[dim_X]= \"value_1\""]
}
```

**MetricMatches** — 基于指标值筛选维度值，再用筛选后的维度值计算指标：

`MetricMatches([维度名], [指标名] 运算符 值)`

**MetricMatches vs resultFilters**: 同指标筛选（"指标A≥某值的维度有哪些"）→ resultFilters；跨指标筛选（"指标A≥某值的维度有多少个"→ 用 A 筛维度值，再算 B）→ MetricMatches。

**MetricMatches 约束**: 每个 MetricMatches 仅支持一个指标条件。多指标条件须拆分为多个 MetricMatches（数组内为 AND）：

```json
"filters": [
    "MetricMatches([dim_X], [metric_C] > 30)",
    "MetricMatches([dim_X], [metric_D] < 0.2)"
]
```

#### 3.2.4 indirections（衍生方式）

```
"indirections": ["sameperiod__yoy__value"]                     → 年同比
"indirections": ["proportion__dim_A"]                           → dim_A 组内占比
"indirections": ["rank__desc__dim_A"]                           → dim_A 组内排名
"indirections": ["multi_level_agg__avg,dim_A"]                  → 非时间维度多层聚合
```

**多层聚合选择**: 时间维度多层聚合 → preAggs + period；非时间维度多层聚合 → indirections 的 multi_level_agg。

**period + indirections 组合（推荐）**: 不含 preAggs 的 period 指标做同环比 → 用 `period` + `indirections: ["sameperiod__yoy__growth"]`。含 preAggs 时不可用此组合，须手动分两步 + expr。

**multi_level_agg 与外层 dimensions 冲突**: 当聚合维度同时在外层 dimensions 中时，结果恒等于自身。必须添加 `specifyDimension: { "type": "EXCLUDE", "dimensions": "dim_X" }`。

---

### 3.3 dimensions（选填）— 分析维度

日期维度支持粒度后缀：`__year`, `__quarter`, `__month`, `__week`, `__day`。

**⚠️ 粒度后缀必须全部小写**: 维度名中的粒度后缀（`__day`, `__month`, `__year`, `__week`, `__quarter`）**必须使用小写字母**。这是 API 的硬性要求，大写会导致查询失败或返回空结果。
- ✅ `metric_time__day`, `metric_time__month`, `metric_time__year`
- ❌ `metric_time__DAY`, `metric_time__MONTH`, `metric_time__YEAR`（大写后缀 = 错误）

同理，orders 中引用维度名时也必须保持小写：
- ✅ `{"metric_time__day": "asc"}`
- ❌ `{"metric_time__DAY": "asc"}`

```json
"dimensions": ["metric_time__month", "dim_A"]
```

**⚠️ 维度兼容性校验**: 多指标查询时，dimensions 只能包含**所有指标都支持的维度**（取交集）。详见 §1 候选指标表检查 3。

---

### 3.4 filters 与 resultFilters

| | **filters** | **resultFilters** |
|---|---------|--------------|
| 等价于 | SQL WHERE | SQL HAVING |
| 影响 | 计算过程（分母、排名范围都会被影响） | 仅过滤返回行 |

**选择规则**:
1. 筛选字段是**时间相关**（metric_time、日期）→ **必须放** `timeConstraint`（⚠️ 禁止放 filters）
2. 筛选字段是**指标值或计算结果** → `resultFilters`
3. 筛选字段是**维度值**，需要影响计算 → `filters`
4. 筛选字段是**维度值**，但不应影响计算（占比/排名场景仅展示某些行） → `resultFilters`

**filters 语法**:
```
[dim_A]= "value"                    精确匹配
IN([dim_A], "v1", "v2")            包含
NotIn([dim_A], "v1")               排除
contains([dim_A], "x")             模糊
[dim_num]>= 100                    数值比较
['date_dim']>= "2023-08-01"       日期比较
```

**resultFilters 语法**:
```json
"resultFilters": ["[metric_M] > 1000"]
"resultFilters": ["[metric_M__sameperiod__mom__growth] > 0.05"]
"resultFilters": ["[dim_A]= \"value_1\""]
```

---

### 3.5 timeConstraint（选填）— 时间范围

timeConstraint 有**两个不同的角色**，构建时必须区分：

| 角色 | 说明 | 形式 |
|------|------|------|
| **角色 A：时间范围过滤** | 限定"查哪段时间的数据" | 一个区间（如近7天、上月） |
| **角色 B：period 锚定基准** | 给 period/sameperiod 提供相对偏移的基准点 | 一个具体日期或月份 |

**📋 timeConstraint 速查表**（根据用户时间表达直接查表复制）:

| 用户说 | timeConstraint |
|-------|---------------|
| 昨天 | `"['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"` |
| 今天 | `"['metric_time__day']= DateTrunc(NOW(), \"DAY\")"` |
| 上周 | `"DateTrunc(['metric_time'], \"WEEK\") = DATEADD(DateTrunc(NOW(), \"WEEK\"), -1, \"WEEK\")"` |
| 本周 | `"DateTrunc(['metric_time'], \"WEEK\") = DateTrunc(NOW(), \"WEEK\")"` |
| 上月 | `"DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")"` |
| 本月 | `"DateTrunc(['metric_time'], \"MONTH\") = DateTrunc(NOW(), \"MONTH\")"` |
| 上季 | `"DateTrunc(['metric_time'], \"QUARTER\") = DATEADD(DateTrunc(NOW(), \"QUARTER\"), -1, \"QUARTER\")"` |
| 本季 | `"DateTrunc(['metric_time'], \"QUARTER\") = DateTrunc(NOW(), \"QUARTER\")"` |
| 本年 | `"DateTrunc(['metric_time'], \"YEAR\") = DateTrunc(NOW(), \"YEAR\")"` |
| 去年 | `"DateTrunc(['metric_time'], \"YEAR\") = DATEADD(DateTrunc(NOW(), \"YEAR\"), -1, \"YEAR\")"` |
| 近7天 | `"DateTrunc(['metric_time'], \"DAY\") >= DATEADD(DateTrunc(NOW(), \"DAY\"), -7, \"DAY\") AND ['metric_time__day'] < DateTrunc(NOW(), \"DAY\")"` |
| 近30天 | `"DateTrunc(['metric_time'], \"DAY\") >= DATEADD(DateTrunc(NOW(), \"DAY\"), -30, \"DAY\") AND ['metric_time__day'] < DateTrunc(NOW(), \"DAY\")"` |
| 近12个月 | `"DateTrunc(['metric_time'], \"MONTH\") >= DATEADD(DateTrunc(NOW(), \"MONTH\"), -12, \"MONTH\") AND DateTrunc(['metric_time'], \"MONTH\") < DateTrunc(NOW(), \"MONTH\")"` |
| 2025年4月（具体月份） | `"DateTrunc(['metric_time'], \"MONTH\") = \"2025-04-01\""` |
| 2025-06-15（具体日期） | `"['metric_time__day']= \"2025-06-15\""` |

> ⚠️ 表中除最后两行外，全部使用 NOW()（详见铁律 1）。只有用户指定了具体日期/月份才用字面日期。

**用户未指定时间时的默认策略**（⚠️ **从上到下匹配，命中第一行即停止**）:

| 优先级 | 条件 | 默认 timeConstraint | 说明 |
|-------|------|-------------------|------|
| 1 | 查询中有 period / `__period__` / 已有时间限定派生指标 | 锚定昨天（角色 B） | period 自身定义时间窗口，timeConstraint 只提供基准点 |
| 2 | 查询中有 `__sameperiod__mom__` | 上月 | |
| 3 | 查询中有 `__sameperiod__wow__` | 上周 | |
| 4 | 查询中有 `__sameperiod__qoq__` | 上季 | |
| 5 | 查询中有 `__sameperiod__yoy__` | 上月 | |
| 6 | 查询中有 `__sameperiod__dod__` | 昨天 | |
| 7 | 查询中有排名/TOP-N 且无时间维度 | 近 30 天或上月 | 排名需足够数据量 |
| 8 | dimensions 含 `metric_time__month` | 近 12 个月 | |
| 9 | dimensions 含 `metric_time__quarter` | 本年 | |
| 10 | dimensions 含 `metric_time__week` | 近 12 周 | |
| 11 | 其他 | 近 7 天 | |

**⚠️ 排名/TOP-N 查询的时间范围**: 当用户问"TOP10商品""排名前5的XX"但未指定时间时，默认用**近 30 天**或**上月**（而非近 7 天）。原因：排名类查询需要足够数据量才有统计意义，7 天可能样本不足。

**⚠️ 不可双重偏移**: 当 timeConstraint 已限定到某时段（如"上季度"），metricDefinitions 的 period 不应再做同方向的额外偏移，否则会叠加成"上上季度"。正确做法：timeConstraint 锚定基准，period 从基准点偏移到目标。

---

### 3.6 其他参数

**orders** — 排序列须在 metrics 或 dimensions 中:
```json
"orders": [{"metric_time__day": "asc"}, {"metric_M": "desc"}]
```

**limit**（默认100）/ **offset**（默认1）

**queryResultType** — `SQL_AND_DATA`（默认）/ `SQL` / `DATA`

---

## 4. 构建流程

**API Json 查询请求体的构建思路，需要记录以下关键决策**:
1. 时间判断："用户说'{时间词}' → 相对时间 → NOW()" 或 "用户指定'{具体日期}' → 字面日期"
2. 如使用 metricDefinitions：列出每个 key，确认均在 metrics 中
3. 如涉及占比/排名：说明选 filters 还是 resultFilters 及原因
4. 如多个指标的可分析维度不同：说明维度兼容性检查结果，列出取交集后的合法维度

### 步骤 0：语义解析

按 §0 将用户问题拆解为"看什么 / 怎么看 / 看谁的 / 看哪段时间"四维度，并逐条检查 §0.1 的 9 条消歧规则（A~I）。

输出：明确的指标列表、分析方式、维度筛选需求、时间范围。

### 步骤 1：通过 Gateway 检索指标

从用户问题中提取核心业务关键词，调用 Gateway API 搜索指标：

```bash
curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/search?pageSize=10" --data-urlencode "keyword={关键词}" -G
```

从返回结果中取 `metricName` 放入 metrics 数组。**校验**: `status` 须为 `ONLINE`。

**决策点**:
- 候选中有"看似相关"的已有派生指标（`type=DERIVED`）？→ **查看其 `displayName` 的完整描述**，验证其语义是否与用户意图完全一致。常见误用场景：
  - 时间累计指标（展示名含"至今""累计"）→ 只在用户确实要累计值时使用，不可用于"月度趋势"等当期值场景
  - 近N日指标（展示名含"近7日""近30日"）→ 确认其时间口径是否与用户要求一致
- 用户说了"日均""月均"？→ 按规则 B 判断修饰范围，确保所有被修饰的指标都有对应的 preAggs 处理
- 如果搜索结果为空或不匹配，尝试更换关键词重新搜索（如"销售额"搜不到可试"销售金额"）

### 步骤 2：通过 Gateway 查询维度 + 兼容性校验

对步骤 1 选定的指标，调用 Gateway API 获取可用维度：

```bash
curl -H "X-API-Key: $CAN_API_KEY" "https://gateway.can.aloudata.com/api/metrics/{metricCode}/dimensions"
```

从返回结果中取 `dimName` 作为维度名称。返回的维度列表即该指标的**全部可分析维度**。

**决策点**:
- **维度值匹配**：通过 `sampleValues` 判断用户提到的值属于哪个维度。例如用户说"淘宝" → 查看各维度的 sampleValues，发现 `订单来源平台` 包含"天猫淘宝" → 使用 `order_platform_code`，filter 值为"天猫淘宝"
- **维度兼容性（多指标时逐指标核查）**：分别查询各指标的维度列表，dimensions 只能包含**所有指标都有的维度**（取交集）。发现冲突时排除不兼容的指标或维度，在 buildReason 中说明
- **候选维度不足**：如果用户要的实体在返回的维度中找不到对应维度，在 buildReason 中说明维度缺失，**不要用不相关维度替代**

### 步骤 3：识别快速计算

**同环比**: 按规则 E 选择偏移粒度；按规则 F 区分"同比" vs "对比期末"。

**占比**: 确定范围维度后，执行以下检查：
```
范围维度是否覆盖了 dimensions 中所有非日期维度？
├─ 是 → 恒为 100%！改为 proportion__（全局占比）或调整范围维度
└─ 否 → OK
```

**排名**: 同上检查恒为 1。

### 步骤 4：识别临时指标

跨时段对比、自定义计算、附加业务限定 → 使用 metricDefinitions。

**校验**:
- 临时指标名称在 metrics 数组中？
- 临时指标名称与已有指标不冲突？
- period 的 `of` 后粒度不细于 timeConstraint 锚定粒度？
- preAggs 格式为数组 `[{...}]` 且配合了 period？
- 不含 preAggs 的 period 指标做同环比 → 用 indirections（推荐）
- 含 preAggs 的 period 指标做同环比 → 手动分两步 + expr

### 步骤 5：筛选条件

**filters vs resultFilters 决策树**:

```
需要筛选？
│
├─ 筛选字段是指标值或计算结果？
│   └─ 是 → resultFilters
│
├─ 查询涉及占比或排名？
│   ├─ 是 → 该筛选是否应影响占比分母/排名范围？
│   │   ├─ 是（如"某渠道内各品牌占比"→ 该渠道限定范围） → filters
│   │   └─ 否（如"某渠道在所有渠道中的占比"→ 只展示该渠道） → resultFilters
│   └─ 否 → filters
│
└─ 普通维度值筛选 → filters
```

**校验**: 筛选值须与 dimensions.csv 维度值一致。

### 步骤 6：时间范围

按 §3.5 的默认策略决策树，确定 timeConstraint 的形式和值。

**校验**:
- 使用 period 时 → timeConstraint 是否为具体日期/月份（而非区间）？
- timeConstraint 与 period 是否存在双重偏移？

### 步骤 7：排序分页

排序列须在 metrics 或 dimensions 中。rank 排序用 `asc`（排名小=好）。

### 步骤 8：输出前自检

生成 JSON 后，逐项检查：

1. ✅ 字符串内双引号已用 `\"` 转义
2. ✅ metricDefinitions 中每个 key（含辅助指标）都在 metrics 数组中（铁律 2）
3. ✅ 临时指标名不与已有指标重名
4. ✅ 占比范围维度不会导致恒 100%；排名范围维度不会导致恒为 1（铁律 3）
5. ✅ filters 未不当缩小占比分母/排名范围（全局占比/排名应用 resultFilters）
6. ✅ 同环比偏移粒度匹配用户意图（铁律 4：无限定→yoy；月同比→mom；周同比→wow；季同比→qoq）
7. ✅ period 的 `of` 后粒度不细于 timeConstraint 锚定粒度
8. ✅ preAggs 格式为数组、配合了 period、且聚合粒度与 dimensions 时间粒度不冲突
9. ✅ timeConstraint 与 period 无双重偏移
10. ✅ 快速计算未链式叠加（铁律 5）
11. ✅ "日均/月均"场景使用了 preAggs（非 dimensions 展开），且所有被修饰的指标都已应用
12. ✅ 已有派生指标的语义与用户意图完全匹配；日粒度限制的派生指标未在非天粒度 timeConstraint 下使用（铁律 7）
13. ✅ multi_level_agg 聚合维度与外层 dimensions 冲突时，添加了 specifyDimension EXCLUDE
14. ✅ 相对时间使用 `NOW()`，未硬编码日期（铁律 1）
15. ✅ 每个指标的可用维度（Gateway API 返回的维度列表）都覆盖了 dimensions 中的全部维度（多指标取交集）
16. ✅ 时间过滤条件在 timeConstraint 中，而非 filters 中；MetricMatches 在 metricDefinitions 中（铁律 6）
17. ✅ filters/resultFilters 中的维度值**严格匹配** Gateway API 返回的 sampleValues 原始写法；dimensions/orders 粒度后缀全部小写
18. ✅ 用户要单个汇总数字时无多余维度；"月变化趋势"占比/排名范围维度是 `metric_time__month`；TOP-N 排序指标正确
19. ✅ curl 命令使用 heredoc（`-d @- <<'EOF'`）传递 JSON body，**禁止**用 `-d '...'` 单引号包裹（`['metric_time']` 中的单引号会导致 shell 解析错误或产生非法转义如 `\x27`）

### 步骤 9：展示查询请求 JSON（⚠️ 必做，不可跳过）

**每次执行指标查询时，必须向用户展示完整的查询请求 JSON 体。**

在通过 curl 执行查询时，必须以格式化的 JSON 代码块向用户展示本次发送的请求体，格式如下：

````
📋 **查询请求 JSON：**
```json
{
    "metrics": [...],
    "dimensions": [...],
    ...
}
```
````

**具体要求**：
1. **展示时机**：在展示查询结果的同时，必须以独立的 JSON 代码块展示请求体，确保用户能清晰看到发送了什么请求
2. **格式要求**：使用格式化（缩进）的 JSON，便于用户阅读和调试
3. **完整性**：展示的 JSON 必须与实际发送给 API 的请求体**完全一致**，不可省略任何字段
4. **多次查询**：如果一次对话中执行多个查询，每个查询都必须单独展示其请求 JSON
5. **查询失败时**：查询报错时也要展示请求 JSON，方便用户排查问题

---

## 5. 完整示例

### 5.1 基础查询 + 筛选 + 排序

上周某维度值每天的 metric_A，按日期升序：
```json
{
    "metrics": ["metric_A"],
    "dimensions": ["metric_time__day"],
    "filters": ["[dim_A]= \"value_1\""],
    "timeConstraint": "DateTrunc(['metric_time'], \"WEEK\") = DATEADD(DateTrunc(NOW(), \"WEEK\"), -1, \"WEEK\")",
    "orders": [{"metric_time__day": "asc"}]
}
```


上月 A渠道和 B 渠道销售金额：
```json
{
    "metrics": ["retail_amt"],
    "dimensions": ["channel"],
    "filters": ["IN([channel], \"A\", \"B\")"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")",
    "limit": 100,
    "offset": 1
}
```

### 5.2 同环比 — 月环比增长率

上月各 dim_A 的 metric_A 及月环比增长率，增速前10名：
```json
{
    "metrics": ["metric_A", "metric_A__sameperiod__mom__growth"],
    "dimensions": ["dim_A"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")",
    "orders": [{"metric_A__sameperiod__mom__growth": "desc"}],
    "limit": 10
}
```

### 5.3 全局占比

上月各 dim_A 的 metric_A 占总体的比例：
```json
{
    "metrics": ["metric_A", "metric_A__proportion__"],
    "dimensions": ["dim_A"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")"
}
```

### 5.4 月内占比 + 月内排名

今年各 dim_A 的 metric_A 月内占比和月内排名趋势：
```json
{
    "metrics": [
        "metric_A",
        "metric_A__proportion__metric_time__month",
        "metric_A__rank__desc__metric_time__month"
    ],
    "dimensions": ["metric_time__month", "dim_A"],
    "timeConstraint": "DateTrunc(['metric_time'], \"YEAR\") = DateTrunc(NOW(), \"YEAR\")",
    "orders": [{"metric_time__month": "asc"}]
}
```
注意：范围维度是 `metric_time__month`（每月内比较各 dim_A），不是 `dim_A`（否则每个 dim_A 值只有自己，恒 100%/恒为 1）。

### 5.5 跨时间段对比 — period + timeConstraint

某年5月 vs 2月各 dim_A 的 metric_A 增幅（⚠️ 此处用字面日期因为用户指定了具体月份）：
```json
{
    "metrics": ["may_val", "feb_val", "growth_rate"],
    "metricDefinitions": {
        "may_val": {
            "refMetric": "metric_A",
            "period": "relative_date 0 month of 0 month"
        },
        "feb_val": {
            "refMetric": "metric_A",
            "period": "relative_date -3 month of 0 month"
        },
        "growth_rate": { "expr": "([may_val]-[feb_val])/[feb_val]" }
    },
    "dimensions": ["dim_A"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = \"2025-05-01\"",
    "orders": [{"growth_rate": "desc"}]
}
```

### 5.6 日均 — preAggs

某个指定日期的近11天日均 metric_A（⚠️ 此处用字面日期因为锚定到特定日期）：
```json
{
    "metrics": ["daily_avg"],
    "metricDefinitions": {
        "daily_avg": {
            "refMetric": "metric_A",
            "period": "to_date -10 day of 0 day",
            "preAggs": [{"granularity": "DAY", "calculateType": "AVG"}]
        }
    },
    "timeConstraint": "['metric_time__day']= \"2024-11-11\""
}
```

### 5.7 MetricMatches — 跨指标筛选维度值

上月 metric_A ≥ 某阈值的 dim_X 数量（用 metric_B 计数）：
```json
{
    "metrics": ["filtered_cnt"],
    "metricDefinitions": {
        "filtered_cnt": {
            "refMetric": "metric_B",
            "filters": ["MetricMatches([dim_X], [metric_A] >= 10000)"]
        }
    },
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")"
}
```

### 5.8 resultFilters — 按指标值筛选结果

某个指定月份 metric_A 在指定范围内的 dim_A 及排名（⚠️ 字面日期：用户指定了具体月份）：
```json
{
    "metrics": ["metric_A", "metric_A__rank__desc"],
    "dimensions": ["dim_A"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = \"2025-12-01\"",
    "resultFilters": ["[metric_A] >= 300000 AND [metric_A] <= 500000"],
    "orders": [{"metric_A": "desc"}]
}
```

### 5.9 非时间维度多层聚合 — "XX均"

上季度某筛选条件下的 dim_X 均 metric_A：
```json
{
    "metrics": ["avg_per_dim_X"],
    "metricDefinitions": {
        "avg_per_dim_X": {
            "refMetric": "metric_A",
            "indirections": ["multi_level_agg__avg,dim_X"]
        }
    },
    "filters": ["[dim_B]= \"value_1\"", "[dim_C]= \"value_2\""],
    "timeConstraint": "DateTrunc(['metric_time'], \"QUARTER\") = DATEADD(DateTrunc(NOW(), \"QUARTER\"), -1, \"QUARTER\")"
}
```

### 5.10 多时间窗口对比

近7天和近30天某筛选条件下的 metric_A：
```json
{
    "metrics": ["val_7d", "val_30d"],
    "metricDefinitions": {
        "val_7d": {
            "refMetric": "metric_A",
            "period": "to_date -6 day of 0 day",
            "filters": ["[dim_A]= \"value_1\""]
        },
        "val_30d": {
            "refMetric": "metric_A",
            "period": "to_date -29 day of 0 day",
            "filters": ["[dim_A]= \"value_1\""]
        }
    },
    "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"
}
```

### 5.11 组内排名 + 全局排名

某月各 dim_A、dim_B 的 metric_A，及 dim_A 组内排名和全局排名：
```json
{
    "metrics": [
        "metric_A",
        "metric_A__rank__desc__dim_A",
        "metric_A__rank__desc"
    ],
    "dimensions": ["metric_time__day", "dim_A", "dim_B"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DateTrunc(NOW(), \"MONTH\")",
    "limit": 100
}
```

### 5.12 单个值的全局占比 — resultFilters 展示筛选（⚠️ 易错）

上月 dim_A 某值的 metric_A 全局占比：

✅ 正确：
```json
{
    "metrics": ["metric_A", "metric_A__proportion__"],
    "dimensions": ["dim_A"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")",
    "resultFilters": ["[dim_A]= \"value_1\""]
}
```

❌ 错误（占比恒为 100%）：
```json
{
    "filters": ["[dim_A]= \"value_1\""],
    "metrics": ["metric_A", "metric_A__proportion__"],
    "dimensions": ["dim_A"]
}
```
**原因**: filters 在计算前过滤掉其他值，分母只剩 value_1 自身。

### 5.13 日均 + 同比 — preAggs 手动拆分

本年至今日均 metric_A 及年同比：
```json
{
    "metrics": ["ytd_daily_avg", "ly_ytd_daily_avg", "yoy_growth"],
    "metricDefinitions": {
        "ytd_daily_avg": {
            "refMetric": "metric_A",
            "period": "grain_to_date 0 year of 0 day",
            "preAggs": [{"granularity": "DAY", "calculateType": "AVG"}]
        },
        "ly_ytd_daily_avg": {
            "refMetric": "metric_A",
            "period": "grain_to_date -1 year of -1 day",
            "preAggs": [{"granularity": "DAY", "calculateType": "AVG"}]
        },
        "yoy_growth": {
            "expr": "([ytd_daily_avg]-[ly_ytd_daily_avg])/[ly_ytd_daily_avg]"
        }
    },
    "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"
}
```

### 5.14 时间限定 + 同环比 — period + indirections（推荐）

本年至今 metric_A 及年同比（不含 preAggs 时的推荐写法）：
```json
{
    "metrics": ["ytd_val", "ytd_val_ly", "ytd_yoy_growth"],
    "metricDefinitions": {
        "ytd_val": {
            "refMetric": "metric_A",
            "period": "grain_to_date 0 year of 0 day"
        },
        "ytd_val_ly": {
            "refMetric": "metric_A",
            "period": "grain_to_date 0 year of 0 day",
            "indirections": ["sameperiod__yoy__value"]
        },
        "ytd_yoy_growth": {
            "refMetric": "metric_A",
            "period": "grain_to_date 0 year of 0 day",
            "indirections": ["sameperiod__yoy__growth"]
        }
    },
    "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"
}
```

### 5.15 全局均值对比 — multi_level_agg + specifyDimension

某个指定季度各 dim_A 的 metric_A 与全局平均值的对比（⚠️ 字面日期：用户指定了具体季度）：
```json
{
    "metrics": ["metric_A", "global_avg"],
    "metricDefinitions": {
        "global_avg": {
            "refMetric": "metric_A",
            "indirections": ["multi_level_agg__avg,dim_A"],
            "specifyDimension": { "type": "EXCLUDE", "dimensions": "dim_A" }
        }
    },
    "dimensions": ["dim_A"],
    "timeConstraint": "DateTrunc(['metric_time'], \"QUARTER\") = \"2025-01-01\""
}
```
注意：缺少 specifyDimension 时，每个 dim_A 分组内只有自己，均值恒等于自身值。

### 5.16 环比增速 + 排名 — 多步拆分（⚠️ 铁律5高频违反场景）

上月各渠道销售额环比增速前3的品牌（先算环比再排名，**禁止链式叠加**）：
```json
{
    "metrics": ["retail_amt", "mom_growth", "mom_growth__rankDense__desc__first_channel"],
    "metricDefinitions": {
        "mom_growth": {
            "refMetric": "retail_amt",
            "indirections": ["sameperiod__mom__growth"]
        }
    },
    "dimensions": ["first_channel", "product_brand_name"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")",
    "resultFilters": ["[mom_growth__rankDense__desc__first_channel] <= 3"],
    "orders": [{"first_channel": "asc"}, {"mom_growth__rankDense__desc__first_channel": "asc"}]
}
```
**关键**: `retail_amt__sameperiod__mom__growth__rankDense__desc__first_channel` 是链式叠加（违反铁律5）。正确做法是先定义环比临时指标 `mom_growth`，再对它做排名快速计算。

### 5.17 占比 + 同比 + 排名 — resultFilters 展示筛选（⚠️ 铁律3高频违反场景）

2025年4月 Wholesale 渠道的销售额、年同比、渠道内占比、渠道内排名：
```json
{
    "metrics": [
        "retail_amt",
        "retail_amt__sameperiod__yoy__growth",
        "retail_amt__proportion__",
        "retail_amt__rankDense__desc"
    ],
    "dimensions": ["first_channel"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = \"2025-04-01\"",
    "resultFilters": ["[first_channel]= \"Wholesale\""]
}
```
**关键**: 渠道内占比和排名需要所有渠道参与计算，所以 Wholesale 筛选必须放在 `resultFilters`（而非 `filters`）。如果用 `filters` 筛选 Wholesale，分母/排名范围只剩自己，占比恒 100%、排名恒 1。

---

## 6. 常见错误模式

### 速查表 — 与铁律/规则直接对应的错误（详见对应铁律）

| 模式 | 现象 | 对应规则 |
|------|------|---------|
| 1. 占比恒为 100% | proportion 结果全为 100% | 铁律 3 + §3.1.2 陷阱一/二 |
| 2. 排名恒为 1 | rank 结果全为 1 | 铁律 3 |
| 3. 硬编码日期替代 NOW() | timeConstraint 出现 `DateTrunc('YYYY-MM-DD', ...)` | 铁律 1 |
| 4. 临时指标未加入 metrics | 临时指标在结果中缺失 | 铁律 2 |
| 5. 时间条件放在 filters | 时间过滤不生效 | §3.4 选择规则 1 |
| 6. MetricMatches 放在顶层 filters | 查询报错 | 铁律 6 |
| 7. 链式快速计算 | `metric__sameperiod__mom__growth__rank__desc__dim` | 铁律 5 + 示例 5.16 |
| 8. 占比缺少分组维度 | dimensions 为空但使用 `proportion__` | §3.1.2 前提条件 |
| 9. 粒度后缀大小写错误 | `metric_time__DAY` 导致报错 | §3.3 小写规则 |
| 10. 非查询消息生成无效请求体 | "你好"生成空 metrics 请求体 | 铁律 9 检查 C |
| 11. 幻觉指标 | 使用候选表外的指标名 | 铁律 9 检查 A |
| 12. 维度不兼容 | 使用指标不支持的维度 | 铁律 9 检查 B |
| 13. 该拒不拒 | 上下文不足仍硬凑查询 | 铁律 9 |

### 详细说明 — 需要额外理解的错误模式

**❌ 模式 14：timeConstraint + period 双重偏移**
timeConstraint 已偏移到目标时段，period 又额外偏移 → 叠加成"上上期"。正确做法：timeConstraint 锚定基准，period 从基准点偏移到目标。

**❌ 模式 15：临时指标命名冲突**
metricDefinitions 中临时指标名与已有指标重名 → 查询行为不可预测。临时指标名加业务前缀/后缀以示区分。

**❌ 模式 16：用错已有派生指标**
已有派生指标的语义（展示名描述的实体、范围、时间口径）与用户意图不匹配。**必须回到候选指标表核查展示名描述**，不匹配时改用原子指标 + 快速计算。

**❌ 模式 17：累计指标当当期指标**
用了"至今累计"类派生指标做月度/日度趋势，导致值逐月递增。趋势场景用原始指标 + 时间粒度维度。

**❌ 模式 18：候选维度不足时强行替代**
候选维度中无用户要的实体维度，模型用不相关维度替代。应在 buildReason 中说明缺失，不强行替代。

**❌ 模式 19：preAggs 时 dimensions 含同粒度时间维度**
preAggs 按 DAY 聚合但 dimensions 有 `metric_time__day` → 先按日展开再取均值，日均=原值。preAggs 聚合粒度不应与 dimensions 时间粒度相同。

**❌ 模式 20：多指标查询未校验维度兼容性**
多个指标的可分析维度不同时，必须取交集。特别注意"所有维度"标注的指标与有限列表指标混用的场景。

**❌ 模式 21：维度值大小写/格式不匹配**
filters 中的维度值与候选维度表不一致（如 `"e-commerce"` vs `"E-commerce"`；`"2025 新款"` vs `"2025新款"`）。**必须严格按候选维度表原始写法**。

**❌ 模式 22：用户问总量却添加了不必要的 dimensions**
用户问"上月销售额是多少"（总数），dimensions 应为空。**⚠️ 例外**: 问题含"**每天/每日/分天/分日/每一天**"时应添加 `metric_time__day`。

**❌ 模式 23："日均"误用 metric_time__day 维度替代 preAggs**
"日均" = metricDefinitions + period + preAggs `[{"granularity": "DAY", "calculateType": "AVG"}]`，**不是**在 dimensions 中加 `metric_time__day`。

**❌ 模式 24："近N年"时间范围缺少上界**
"近3年"须同时有下界和上界：`>= DATEADD(DateTrunc(NOW(), "YEAR"), -3, "YEAR") AND < DateTrunc(NOW(), "YEAR")`。

**❌ 模式 25：排名/TOP-N 按错误指标排序**
排序指标必须与用户关注的指标一致。TOP-N 默认按**用户提到的第一个指标** desc 排序。