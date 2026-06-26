# PSC 统计相关表：OpenClaw 字段语义说明

面向 Agent / 用户说明：**不要按字面误解列名**。与单船 `pscapi/get` 同源的底层表多在库 `pscdata`（以实际部署为准）。

---

## 1. `authority`（检查国 / 检查当局）

**在所有下列表中，`authority` 表示的是「船舶接受 PSC 检查时的检查国/检查当局」**（实施检查的一方、检查发生地对应的监管主体），**不是**船舶的**注册国**、**不是**船旗国。

| 表名 | 说明 |
|------|------|
| `psc` | 列表源表，检查当局 |
| `psc_daily_stats` | 日聚合 |
| `psc_daily_stats_roll` | 滚动汇总（由 daily_stats 汇总而来） |
| `psc_defect_distribution` | 缺陷分布日表 |
| `psc_port_authority_daily` | 港口×当局日表 |
| `psc_company_daily` | 公司维度日表（若有） |
| `psc_anomaly_event` | 异常事件；`slice_type` 含细切片 `AUTHORITY_FLAG_PORT_TYPE` 与粗切片 `AUTHORITY_FLAG`（后者 `port`/`ship_type` 占位 `__COARSE_ALL__`，表示当局×旗国汇总） |
| `psc_anomalies` | 兼容用异常表 |

**船旗国 / 注册国**在业务上通常对应字段 **`flag`**（或数据源中的 flag 含义），**不要**与 `authority` 混淆。

**对用户复述时的建议话术**：

- 说 **「检查国」「检查当局」**，避免说「authority 是国家注册」。
- 对比「某检查国对某船旗」时：一边是 **`authority`**（谁查），一边是 **`flag`**（船挂哪旗）。

---

## 2. `ship_type` / API 中的 `shipType`（实为检查类型）

下列来源中，**名为 `ship_type` 或与展示字段 `shipType` 对应的维度，均表示 PSC 源表中的检查类型 `type_ins`**（如初次检查、后续检查、跟进检查等），**不是**船舶类型（散货船、油轮、集装箱船等）。

| 位置 | 字段名 | 含义 |
|------|--------|------|
| `psc` | `type_ins` | 检查类型（源字段） |
| `psc_daily_stats` | `ship_type` | 由 `type_ins` 填入，**列名易误解**，实为检查类型 |
| `psc_daily_stats_roll` | `ship_type` | 与 daily_stats 一致 |
| `psc_anomaly_event` | `ship_type` / 接口 `shipType` | 与上同 |

**未列出的表**（如 `psc_port_authority_daily`、`psc_company_daily`、`psc_defect_distribution`、`psc_anomalies`）若**无** `ship_type` 列，则不存在该维度；若有扩展列，以库表注释或后端文档为准。

**对用户复述时的建议话术**：

- 使用 **「检查类型」「type_ins 维度」**，**不要**说成「船舶类型」「船型」。
- 若用户明确要 **按真实船型** 的统计或异常：说明 **当前该套日批/异常链路不按船型分桶**，需后端增加船型字段或按 IMO 关联船型库后再统计。

---

## 3. 与技能文档的交叉引用

- OpenClaw 调异常接口的 URL 与参数：见 [psc_anomaly_api.md](psc_anomaly_api.md)。
- 单船检查记录：`pscapi/get`，见 [psc_api.md](psc_api.md)。

---

*文档随 newpsc / 数据模型变更时需同步修订。*
