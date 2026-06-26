# PSC 统计异常 API / PSC statistical anomaly API

查询 **PSC 日批统计异常事件**（表 `psc_anomaly_event`），与「按 IMO 查单船检查记录」的 [psc_api.md](psc_api.md) 互补。**均需**在 Query 中传 `api_key`（与 `pscapi/get` 相同，技能脚本从 `HIFLEET_API_KEY` 读取）。若网关已对路径统一鉴权、应用层暂不解析该参数，多余参数通常可忽略；与 `pscapi/get` 对齐便于同一 `api_key` 策略。

**多表字段语义（`authority` = 检查国、`ship_type`/`shipType` = 检查类型）**：见 **[psc_stats_field_semantics.md](psc_stats_field_semantics.md)**，OpenClaw 解读异常或向用户解释维度时应优先遵循该文档。

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 `HIFLEET_API_BASE`（无末尾 `/`）。见 [api_base.md](api_base.md)。

## 响应包装 HiResult

与 HiFleet 常见接口一致（以实际返回为准）：

| 字段 | 说明 |
|------|------|
| status | 成功多为字符串 `"1"` |
| msg | 如 `SUCCESS` |
| data | 业务载荷：列表接口为 `{ total, page, pageSize, list }`；详情为单条对象；summary 为数组 `[{ severity, cnt }, ...]` |

若返回顶层 `code` 为 **4004/4005/4001** 等，含义与 [psc_api.md](psc_api.md) 中 `api_key` / 权限说明类似（以服务端为准）。

---

## 重要：`shipType` / `authority`（摘要）

- **`shipType`**（库表 `ship_type`）：**检查类型**（源字段 `psc.type_ins`），**不是**船型。涉及表：`psc`、`psc_daily_stats`、`psc_daily_stats_roll`、`psc_anomaly_event` 等，**完整表清单与话术**见 [psc_stats_field_semantics.md](psc_stats_field_semantics.md)。  
- **`authority`**：**检查国/检查当局**，**不是**船舶注册国；船旗国用 **`flag`**。同上见语义文档。

---

## 1. 分页列表

| 项目 | 值 |
|------|-----|
| URL | `{base}/pscapi/openclaw/anomalies` |
| 方法 | GET |

### Query 参数

| 参数 | 必选 | 说明 |
|------|------|------|
| api_key | 是 | 接口授权 `api_key` |
| dateFrom | 否 | `yyyy-MM-dd`；与 `dateTo` 都省略时服务端默认最近约 30 天 |
| dateTo | 否 | `yyyy-MM-dd` |
| authority | 否 | 检查当局，精确匹配 |
| authorityContains | 否 | 检查当局**子串**匹配（SQL `LIKE %…%`），适合「China」等与库内全称不一致时；可与 `authority` 同时存在（AND） |
| flag | 否 | 船旗国，精确匹配 |
| flagContains | 否 | 船旗国**子串**匹配（同上） |
| port | 否 | 港口，精确匹配 |
| severity | 否 | 如 `HIGH` / `MEDIUM` / `LOW` |
| anomalyType | 否 | 如 `DETENTION_RATE_SPIKE`、`AVG_DEFECTS_SPIKE` |
| sliceType | 否 | `AUTHORITY_FLAG_PORT_TYPE`（日×当局×旗国×港口×检查类型）；`AUTHORITY_FLAG`（日×当局×旗国粗粒度，港口/检查类型占位 `__COARSE_ALL__`，更易检出「某检查国对某船旗」整体滞留率异常） |
| metric | 否 | 如 `detention_rate`、`avg_defects` |
| status | 否 | 如 `open` |
| page | 否 | 默认 `1` |
| pageSize | 否 | 默认 `20`，最大 `100` |

### data 结构（成功时）

- `total`：总条数  
- `page`、`pageSize`  
- `list`：事件数组，常见字段含 `id`、`title`、`dateStart`、`dateEnd`、`severity`、`metric`、`currentValue`、`baseline`、`changeRate`、`description`、`evidence`（多为 JSON 字符串）等。

---

## 2. 按严重级别汇总

| 项目 | 值 |
|------|-----|
| URL | `{base}/pscapi/openclaw/anomalies/summary` |
| 方法 | GET |

### Query 参数

与列表相同筛选：`api_key` 必填；`dateFrom`、`dateTo`、`authority`、`authorityContains`、`flag`、`flagContains`、`port`、`severity`、`anomalyType`、`sliceType`、`metric`、`status` 可选（日期默认逻辑同列表）。

### data 结构

数组，元素示例：`{ "severity": "HIGH", "cnt": 12 }`。

---

## 3. 单条详情

| 项目 | 值 |
|------|-----|
| URL | `{base}/pscapi/openclaw/anomalies/{id}` |
| 方法 | GET |

### Query 参数

| 参数 | 必选 |
|------|------|
| api_key | 是 |

路径 `{id}` 为事件主键（数字）。

失败时可能返回 `status` 非 1 或业务错误文案（如记录不存在）。

---

## OpenClaw 调用建议（常规）

1. 先 **summary** 再 **list** 再 **get {id}**（见上）。  
2. 精确筛选：`authority`/`flag`/`port` 须与入库字符串**一致**；自然语言（如「中国检查」）优先试 **`authorityContains`**（或 `flagContains`），避免精确值拼写不一致导致 0 条。  
3. 用户问「某检查国近期哪些船旗风险高 / 滞留异常」时：在日期窗内调用 **list/summary**，宜带 **`sliceType=AUTHORITY_FLAG`** 看粗粒度事件；再按需查细切片 `AUTHORITY_FLAG_PORT_TYPE`。  
4. 仅输出接口返回内容，**不编造**未出现在 `list`/`summary` 中的事件。

---

## OpenClaw：异常表数据量过少时的规则（必读）

`psc_anomaly_event` 由离线统计模型写入，**行数少或为空是常见情况**，与「全球/某国 PSC 是否严峻」**不能等同**。

### 禁止表述

- 不得因 `total=0` 或 summary 全 0 而声称：**「没有 PSC 风险」「没有滞留问题」「监管很宽松/很严」**等未经验证的结论。  
- 不得暗示异常表覆盖「所有 PSC 异常」——本表仅为**当前模型与阈值下**的统计异常快照。

### 必须表述（当 `total == 0` 或极小时）

1. **界定范围**：说明结果是「**统计异常事件表**在请求条件（日期、当局、旗国、港口等）下的查询结果」，不是全库 PSC 原始记录。  
2. **可能原因**（择要说明，不必全列）：  
   - 检测参数较严（如单日切片检查次数下限、Z 分数阈值）；  
   - 仅命中**细切片**时样本分散在港口/检查类型上，周维度「滞留件数」上升未必形成单日 Z 异常；部署 **`AUTHORITY_FLAG` 粗切片**并补跑日批后可改善；  
   - 未做或未做完历史 **异常补算**（`backfill-anomalies`）；  
   - 筛选字段与数据库**字符串不完全一致**（优先试 `authorityContains` / `flagContains`）；  
   - 时间窗过窄。  
3. **可执行建议**（面向终端用户）：放宽日期、去掉部分筛选重试；若关心**具体船舶**，改用 **单船 PSC**（`pscapi/get`，见 [psc_api.md](psc_api.md)）。  
4. **可执行建议**（面向运维/内部）：在 newpsc 中调整 `psc.stats`（如 `min-inspections`、Z 阈值）并全量重跑异常补算（详见项目运维说明）。

### 当 `total` 为个位数（如 1～10）

- 如实列出条目，并注明 **事件数量很少，仅作参考，不宜单独支撑宏观政策或市场结论**。  
- 可提示：扩大 `dateFrom`～`dateTo` 或减少过滤条件后再查。

### 能力边界（回复用户时可用）

| 需求 | 应用哪类能力 |
|------|----------------|
| 某时段「模型认定的」统计异常事件 | `openclaw/anomalies*` |
| 某船检查史、缺陷、滞留记录 | `pscapi/get`（IMO），勿用异常表代替 |

---

## 脚本

`scripts/get_psc_anomalies.py`：`list` / `summary` / get `<id>`，从环境变量读取 `api_key` 与可选 `HIFLEET_API_BASE`。
