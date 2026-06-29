---
name: metric-platform
description: "MetricHub多租户指标平台全流程编排：指标目录浏览、查询构建执行(九条铁律/九条消歧规则/快速计算语法)、数据可视化推荐、仪表盘编排。触发：查询指标、同环比、占比、排名、时间限定、metricDefinitions、timeConstraint、filters、dimensions、查看指标目录、创建仪表盘、配置Gateway"
---
# MetricHub 指标平台 Skill

## 平台能力概述

MetricHub 是一个多租户 SaaS 指标平台，基于 Aloudata CAN Gateway 语义层 API。提供以下核心能力：

1. **指标目录浏览** — 搜索、浏览、收藏指标，查看指标详情和可用维度
2. **查询构建与执行** — 可视化构建指标查询 JSON，通过 Gateway 执行并返回结果（**保留 metric-query 1.0.2 全部查询逻辑**）
3. **数据可视化** — 根据查询结果自动推荐并渲染图表（折线图/柱状图/饼图/表格等）
4. **仪表盘编排** — 将多个查询组合为可拖拽布局的仪表盘，支持全屏展示和自动刷新
5. **工作空间管理** — 多租户隔离，每个工作空间独立管理 API Key 和指标元数据

---

## 平台路由导航

当用户意图可以通过浏览器操作完成时，引导用户前往对应页面：

| 用户意图 | 操作 |
|---------|------|
| "查看指标目录""有哪些指标""搜索指标" | 导航到 `/:workspaceSlug/catalog` |
| "查询XX指标""帮我分析XX" | 导航到 `/:workspaceSlug/query` 并预填充指标 |
| "查看仪表盘""创建仪表盘" | 导航到 `/:workspaceSlug/dashboards` |
| "配置 Gateway""设置 API Key" | 导航到 `/:workspaceSlug/settings/gateway` |
| "查看查询历史" | 导航到 `/:workspaceSlug/query/history` |

---

## 指标查询构建（完全继承 metric-query 1.0.2）

以下内容从 metric-query 1.0.2 SKILL.md **原封不动**保留，作为平台查询能力的核心知识：

> **注意**: 当用户需要直接通过 Agent 构建并执行查询 JSON 时，使用本节的所有规则。当用户已登录 MetricHub 前端平台时，引导用户在平台上操作。

### 数据源

Gateway Search API: `GET {api_base_url}/api/metrics/search?keyword={关键词}`
Gateway Metrics Query API: `POST {api_base_url}/api/metrics/query`

**所有 Gateway 调用通过 MetricHub 后端代理**（`POST /api/v1/workspaces/{id}/queries/execute`），API Key 由平台按工作空间管理。

### 九条铁律（Iron Laws 1-9）

**铁律 1 — 相对时间必须用 NOW()，禁止硬编码日期**
"上月""上周""本年""昨天""近N天""去年""本季""上季" → **必须** `NOW()`。

**铁律 2 — metricDefinitions 中每个 key 必须同时在 metrics 数组中（包括辅助指标）**
定义了就必须注册。辅助计算指标也必须显式列为 metric。

**铁律 3 — 占比/排名 + filters = 分母/范围被缩小 → 结果恒 100%/恒为 1**
要"某个值在全局中的占比/排名" → 用 `resultFilters` 做展示筛选，**不用 filters**。

**铁律 4 — "同比"默认 = yoy；带粒度前缀时按前缀选择**
- 无限定 / "年同比" → `yoy`
- "月同比" → `mom`；"周同比" → `wow`；"季同比" → `qoq`

**铁律 5 — 一个指标只能做一次快速计算，不可链式叠加**
需要多步（如先算环比再排名）→ 用 metricDefinitions 分步。

**铁律 6 — MetricMatches 只能在 metricDefinitions 的 filters 中使用**
禁止放在顶层 filters。

**铁律 7 — 派生指标的 metric_time 粒度限制必须遵守**
标注"仅支持日粒度"的派生指标只能在 timeConstraint 锚定到天粒度时使用。

**铁律 8 — "月变化趋势"中的占比/排名范围维度必须是 metric_time__month**

**铁律 9 — 上下文不足时必须拒绝生成查询，返回空 JSON `{}`**

### 九条语义消歧规则（Rules A-I）

- **规则 A** — "总和" vs "分别"
- **规则 B** — 修饰语的作用域（"日均/月均"作用范围）
- **规则 C** — "占比"的两种含义（值占比 vs 数量占比）
- **规则 D** — "XX均"的聚合维度
- **规则 E** — "同比" vs "环比"
- **规则 F** — "对比去年末" ≠ "年同比"
- **规则 G** — "趋势" ≠ 同环比
- **规则 H** — "差异/差距/对比" ≠ 同环比
- **规则 I** — 简单优先

### 快速计算语法

**同环比**: `{指标}__sameperiod__{偏移粒度}__{方法}`
- 偏移粒度: `dod`, `wow`, `mom`, `qoq`, `yoy`, `moeom`, `qoeoq`, `yoeoy`
- 方法: `value`, `growthvalue`, `growth`, `decrease`, `decreaserate`

**占比**: `{指标}__proportion__{范围维度}`
- `proportion__` = 全局占比；`proportion__dim_A` = 组内占比

**排名**: `{指标}__{方式}__{顺序}__{范围维度}`
- 方式: `rank` / `rankDense` / `rowNumber`；顺序: `desc` / `asc`

**时间限定**: `{指标}__period__{限定}`
- 近N期: `7d`, `3w`, `6m`, `2q`, `1y`
- 本期至今: `ytd`, `qtd`, `mtd`, `wtd`

### metricDefinitions 可配置属性

| 属性 | 说明 |
|------|------|
| `refMetric` | 引用已有指标 |
| `expr` | 复合表达式 `"[m1]+[m2]"` |
| `period` | 时间限定（仅支持相对偏移） |
| `preAggs` | 时间维度多层聚合（**数组格式** `[{...}]`） |
| `filters` | 业务限定（支持 MetricMatches） |
| `indirections` | 衍生方式（同环比/占比/排名/多层聚合） |
| `specifyDimension` | 聚合维度控制（EXCLUDE） |

### timeConstraint 速查表

| 用户说 | timeConstraint |
|-------|---------------|
| 昨天 | `"['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"` |
| 今天 | `"['metric_time__day']= DateTrunc(NOW(), \"DAY\")"` |
| 上周 | `"DateTrunc(['metric_time'], \"WEEK\") = DATEADD(DateTrunc(NOW(), \"WEEK\"), -1, \"WEEK\")"` |
| 本周 | `"DateTrunc(['metric_time'], \"WEEK\") = DateTrunc(NOW(), \"WEEK\")"` |
| 上月 | `"DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")"` |
| 本月 | `"DateTrunc(['metric_time'], \"MONTH\") = DateTrunc(NOW(), \"MONTH\")"` |
| 上季 | `"DateTrunc(['metric_time'], \"QUARTER\") = DATEADD(DateTrunc(NOW(), \"QUARTER\"), -1, \"QUARTER\")"` |
| 本年 | `"DateTrunc(['metric_time'], \"YEAR\") = DateTrunc(NOW(), \"YEAR\")"` |
| 去年 | `"DateTrunc(['metric_time'], \"YEAR\") = DATEADD(DateTrunc(NOW(), \"YEAR\"), -1, \"YEAR\")"` |
| 近7天 | `"DateTrunc(['metric_time'], \"DAY\") >= DATEADD(DateTrunc(NOW(), \"DAY\"), -7, \"DAY\") AND ['metric_time__day'] < DateTrunc(NOW(), \"DAY\")"` |
| 近30天 | `"DateTrunc(['metric_time'], \"DAY\") >= DATEADD(DateTrunc(NOW(), \"DAY\"), -30, \"DAY\") AND ['metric_time__day'] < DateTrunc(NOW(), \"DAY\")"` |
| 近12个月 | `"DateTrunc(['metric_time'], \"MONTH\") >= DATEADD(DateTrunc(NOW(), \"MONTH\"), -12, \"MONTH\") AND DateTrunc(['metric_time'], \"MONTH\") < DateTrunc(NOW(), \"MONTH\")"` |

### 常见错误模式速查（25种）

1. 占比恒为 100% — proportion 结果全为 100%
2. 排名恒为 1 — rank 结果全为 1
3. 硬编码日期替代 NOW() — timeConstraint 出现 `DateTrunc('YYYY-MM-DD', ...)`
4. 临时指标未加入 metrics — 临时指标在结果中缺失
5. 时间条件放在 filters — 时间过滤不生效
6. MetricMatches 放在顶层 filters — 查询报错
7. 链式快速计算 — `metric__sameperiod__mom__growth__rank__desc__dim`
8. 占比缺少分组维度 — dimensions 为空但使用 `proportion__`
9. 粒度后缀大小写错误 — `metric_time__DAY` 导致报错
10. 非查询消息生成无效请求体
11. 幻觉指标 — 使用候选表外的指标名
12. 维度不兼容 — 使用指标不支持的维度
13. 该拒不拒 — 上下文不足仍硬凑查询
14. timeConstraint + period 双重偏移
15. 临时指标命名冲突
16. 用错已有派生指标
17. 累计指标当当期指标
18. 候选维度不足时强行替代
19. preAggs 时 dimensions 含同粒度时间维度
20. 多指标查询未校验维度兼容性
21. 维度值大小写/格式不匹配
22. 用户问总量却添加了不必要的 dimensions
23. "日均"误用 metric_time__day 维度替代 preAggs
24. "近N年"时间范围缺少上界
25. 排名/TOP-N 按错误指标排序

---

## 数据可视化推荐

根据查询结果类型推荐最佳图表类型：

| 数据类型 | 推荐图表 | ECharts 类型 |
|---------|---------|-------------|
| 时间序列（单维度+时间） | 折线图 | `line` |
| 时间序列（多指标） | 面积图 | `area` |
| 维度对比（少类别） | 柱状图 | `bar` |
| 占比数据 | 饼图 | `pie` |
| 双变量关系 | 散点图 | `scatter` |
| 排名数据 | 排行榜表格 | `table` |
| 汇总数值 | 指标卡 | `metric_card` |

---

## 仪表盘编排

支持以下操作：
- **创建仪表盘**: POST `/api/v1/workspaces/{id}/dashboards`
- **添加图表**: POST `/api/v1/workspaces/{id}/dashboards/{db_id}/charts`
- **拖拽布局**: 使用 react-grid-layout 实现可拖拽、缩放的网格布局
- **自动刷新**: 设置 `refresh_interval` 秒数，0 表示不自动刷新
- **全屏展示**: 导航到 `/:workspaceSlug/dashboards/:id/full`

---

## 多租户模式

- 每个工作空间独立管理 Gateway API Key（通过 `/api/v1/workspaces/{id}/gateway/config` 配置）
- 指标元数据按工作空间隔离缓存
- 工作空间成员角色: `admin`（管理员）/ `editor`（编辑者）/ `viewer`（查看者）
- 所有 API 请求需携带 JWT Bearer Token
