# PSC OpenClaw 统计 API（原始聚合 / 缺陷 / 占比）

与 **统计异常事件**（`openclaw/anomalies*`，见 [psc_anomaly_api.md](psc_anomaly_api.md)）及 **单船 PSC**（`pscapi/get`，见 [psc_api.md](psc_api.md)）并列，用于回答「哪里变严」「哪旗风险」「哪港严」「缺陷热点」「是否针对某旗」等 **可量化** 问题。

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 `HIFLEET_API_BASE`（无末尾 `/`）。见 [api_base.md](api_base.md)。Query 均需 **`api_key`**（与 `pscapi/get` 一致）。

**数据依赖**：

- 下列接口主要读 **`pscdata.psc`**（原始检查行）；大时间窗可能较慢，依赖库表索引（`doi`、`authority`、`flag`、`port` 等）。
- **`/openclaw/stats/defects/top`** 读 **`psc_defect_distribution`**，需 **newpsc** 已跑日批缺陷分布（与 `psc` 明细一致）。

**字段语义**：`authority`=检查国/当局，`flag`=船旗；`type_ins` 在 `mixDimension=TYPE_INS` 时为 **检查类型**（非船舶类型/船型），见 [psc_stats_field_semantics.md](psc_stats_field_semantics.md)。

---

## 1. 区间对比 `GET /pscapi/openclaw/stats/compare`

按维度聚合 **检查次数、滞留次数、滞留率**，并与 **等长上一段基线**（或自定义基线）对比，输出环比 **百分比**（`inspectionsChangePct`、`detentionRateChangePct` 等）。

| Query | 说明 |
|--------|------|
| dateFrom, dateTo | 当前区间 `yyyy-MM-dd`；**同时省略**时默认近 30 天（至昨天） |
| comparePrevious | 默认 `true`：基线 = 紧邻当前区间之前、**天数相同**的一段 |
| baseDateFrom, baseDateTo | 可选，显式指定基线区间（与 comparePrevious 二选一逻辑：若两者都传则用它） |
| groupBy | `GLOBAL` \| `AUTHORITY` \| `FLAG` \| `AUTHORITY_FLAG` \| `PORT` \| `AUTHORITY_PORT`；默认 `AUTHORITY` |
| authorityContains, flagContains, portContains | 可选，子串 `LIKE` |
| mou | 可选，精确 MOU 码（如 `tok`） |
| limit | 非 GLOBAL 时每维返回行数上限，默认 50，最大 200 |

**data 要点**：`periodCurrent`、`periodBaseline`、`rows[]`（含 `baselineDetentionRate`、`detentionRateChangePct` 等）。

**Agent 用法示例**：

- 「哪些国家检查变严」：`groupBy=AUTHORITY`，适当 `dateFrom`/`dateTo`，看 `detentionRateChangePct`、`inspectionsChangePct`。
- 「全球趋势」：`groupBy=GLOBAL`。
- 「哪港严 / 中国主要检查港口是哪些」：**必须调用本接口**，禁止用常识列表代替数据库结果。推荐：
  - `groupBy=PORT` + `authorityContains=China`（或库内实际出现的当局子串，如 `PRC`、`CHINA`），按 `inspections` 降序解读 `rows`；
  - 或 `groupBy=AUTHORITY_PORT` + `authorityContains=China`，同时看到当局与港口字段。
  - 完整路径示例：`GET {base}/pscapi/openclaw/stats/compare?api_key=...&groupBy=PORT&authorityContains=China&dateFrom=YYYY-MM-DD&dateTo=YYYY-MM-DD&limit=30`

**禁止**：在**未调用** `stats/compare`（或未拿到有效 JSON）时，向用户声称「港口接口故障」「无法获取港口排名」——除非请求确实返回错误码/超时，并应写明**具体错误**（如 `4001` 无权、`404` 未部署）。

### 港口数据拿不到时的排查（不是缺接口）

| 现象 | 常见原因 |
|------|-----------|
| `4001` / 权限错误 | `api_key` **未开通** `/pscapi/openclaw/stats/*`（仅开了 `anomalies` 或 `pscapi/get` 不够）；需在 HiFleet 网关/权限中放行上述路径。 |
| `404` | **线上未部署**含 `openclaw/stats` 的 `hifleet.data.api` 版本。 |
| `rows` 为空或很少 | `authorityContains` 与库内 `psc.authority` **写法不一致**（可换子串重试）；或 **`psc.port` 大量为空**被 SQL 过滤（`port` 非空的行才会进 `PORT`/`AUTHORITY_PORT` 分组）。 |
| Agent 仍答「技术故障」 | 多为 **未按技能调用接口**或 **臆测**；应以实际 HTTP 响应为准。 |

**说明**：返回的 `port` 为库内存储形式（可能是英文港名、代码等），与口语「上海港」可能不完全一致，需如实展示或说明映射关系。

---

## 2. 缺陷 Top `GET /pscapi/openclaw/stats/defects/top`

| Query | 说明 |
|--------|------|
| dateFrom, dateTo | 同 compare；同时省略默认近 30 天 |
| authorityContains, flagContains | 可选 |
| limit | 默认 30，最大 200 |

**data**：`defectRecordSum`（区间内缺陷记录条数合计）、`list[]` 含 `defectCode`、`defectCount`、`shareOfDefectRecordsPct`（占合计比例，**非**「占滞留原因」 unless 业务上另行定义）。

---

## 3. 占比对比（针对性）`GET /pscapi/openclaw/stats/mix/compare`

在筛选条件下，各 **船旗** 或 **`type_ins`（检查类型）** 占 **该条件下检查总次数** 的比重，**近期 vs 基线**。

| Query | 说明 |
|--------|------|
| dateFromRecent, dateToRecent | 近期区间；同时省略默认近 30 天 |
| dateFromBase, dateToBase | 可选；省略则基线为与近期 **等长** 的前一段 |
| mixDimension | `FLAG`（默认）或 `TYPE_INS` |
| authorityContains 等 | 与 compare 相同 |
| limit | 每段返回 Top 行数，默认 20，最大 200 |

**data**：`rows[]` 含 `mixKey`、`shareRecent`、`shareBaseline`（0～1）、`shareDeltaPoints`（百分点差，如 0.25 表示 +25 个百分点）、`detentionRateRecent` / `detentionRateBaseline`。

**话术约束**：仅说明 **占比与变化**，避免断言「政治性针对」；`TYPE_INS` **不是**散货船/油轮等船型。

---

## 与九类问题的对应（能力边界）

| 用户问题类型 | 主要接口 | 说明 |
|--------------|-----------|------|
| 监管变严 / 国家趋势 | compare + anomalies | compare 给可引用数字；anomalies 给模型异常 |
| 船旗风险 | compare `groupBy=FLAG` + anomalies `AUTHORITY_FLAG` | 结合两段看 |
| 港口 / 检查国 | compare `PORT` / `AUTHORITY_PORT` + authorityContains | |
| 缺陷热点 | defects/top | 需分布表；非「滞留主因」专用模型 |
| 整体趋势 | compare `GLOBAL` | |
| 是否针对某旗 / 某类检查 | mix/compare `FLAG` 或 `TYPE_INS` | 占比变化，非因果 |
| 「预测」 | 无专用接口 | 仅可基于多段 compare 做谨慎表述 |
| 避开哪 | 综合 compare + anomalies | 不给投资建议，给事实与提醒 |
| 某船 / IMO | pscapi/get | |

---

## 脚本

`scripts/get_psc_openclaw_stats.py`：`compare` / `defects` / `mix` 子命令，从环境变量读取 `api_key` 与可选 `HIFLEET_API_BASE`。
