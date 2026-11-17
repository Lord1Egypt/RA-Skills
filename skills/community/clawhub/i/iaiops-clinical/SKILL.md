---
name: iaiops-clinical
description: >-
  Clinical-facility edition of iaiops — hospital / healthcare facilities as a
  distinct vertical from generic building management, with patient-safety framing.
  BACnet/IP BMS (isolation-room pressurization + medical-gas source monitoring),
  Modbus (medical-gas alarm panels / energy meters), OPC-UA (plant SCADA), plus
  the cross-protocol brain. Two signature safety checks: isolation_room_check
  (ASHRAE 170 / CDC negative/positive pressure) and medical_gas_check (NFPA 99 /
  HTM 02-01 O2 / medical air / vacuum source pressures). Use when the task mentions
  hospital, 医院, healthcare facility, clinical, 医疗设施, isolation room / 隔离病房 /
  负压病房 / AII / PE, operating room / OR / 手术室, ICU, medical gas / 医用气体 /
  医疗气体, oxygen / 氧气 / medical vacuum / 医用真空, or NFPA 99. Read-first; this
  edition's tool surface is read-only.
---

# iaiops-clinical — 医疗设施 edition（BACnet + Modbus + OPC-UA + 脑）

启动：`IAIOPS_MCP=clinical` / `iaiops-mcp-clinical`（= bacnet + modbus + opcua + 脑；
等价显式写法 `IAIOPS_MCP=bacnet,modbus,opcua`）。BACnet 需 extra：
`pip install iaiops[bacnet]`。典型现场：楼宇/暖通/隔离房压力走 BACnet BMS,医用气体
报警屏/表计走 Modbus,全院 SCADA 走 OPC-UA。

> **为什么单列 edition**：医院设施科的关注点是**患者安全**(隔离房压力、医用气体),
> 买家/合规(NFPA 99、感控)与普通楼宇物业不同 —— 所以从 `iaiops-building` 升格为独立
> edition。工具复用同一套楼宇/BACnet + 脑,叠加两个临床安全检查。

## 工具

### 临床安全检查（healthcare-facility;纯分析、只读、患者安全导向）
- `isolation_room_check` — 隔离病房压差合规（ASHRAE 170 / CDC：空气传染隔离 AII 负压、
  保护性环境 PE 正压,≥2.5 Pa）。检出 reversed(反向,可上报安全事件)/breach/low_margin,
  worst-first,每项引用读数。读数来自 `bacnet_read_points` 的压差 AI 点或历史库。
- `medical_gas_check` — 医用气体/真空源压力合规（NFPA 99 / HTM 02-01：O2/医用空气/N2O
  ~345–380 kPa、医用真空须够深）。检出 low_pressure / high_pressure / insufficient_vacuum /
  critical,worst-first,引用数值。读数来自 BACnet AI 点或气体报警屏。
- `or_environment_check` — 手术室通风合规（ASHRAE 170 Table 7.1：温度 20–24°C、相对湿度
  20–60%、换气 ≥20 ACH）。逐参数越界即 breach,worst-first,引用数值。读数来自 BACnet/BMS。

### BACnet/IP（read-first;BMS / 暖通 / 压力 / 气体点）
- `bacnet_discover` — Who-Is：本地 BACnet/IP 网上的设备
- `bacnet_object_list` — 设备的 object/point 列表
- `bacnet_read_property` — 单对象属性（默认 presentValue）
- `bacnet_read_points` — 所有 analog/binary/multistate 点的 presentValue（压差/气体压力快照）
- `bacnet_cov_subscribe` — 单对象有界 Change-of-Value 捕获
- `bacnet_read_trend_log` — 读设备 TrendLog 缓冲记录
- `bacnet_write_property` — **[WRITE][HIGH][MOC]** 写单对象属性（默认 `dry_run=True` + 双确认）

### Modbus-TCP / RTU（只读;医用气体报警屏、能耗表）
- `modbus_read_holding` `modbus_read_input` `modbus_read_coils` `modbus_read_discrete`
- `modbus_detect_byte_order` — 字节/字序自动探测
- `modbus_list_templates` / `modbus_apply_template` — 厂商寄存器模板 → 命名 tag
- `modbus_health_summary` — 寄存器 vs 阈值分类

### OPC-UA（只读;全院 SCADA / PLC 网关）
- `opcua_server_info` / `opcua_browse` / `opcua_read_node` / `opcua_read_many`
- `opcua_subscribe_sample` `opcua_read_alarms` `opcua_alarm_events`(A&C 带时间戳) `opcua_read_history`(HDA)
- `opcua_diagnose_connection` — 连接失败归因;`opcua_discover_tags` 仅给启发式语义建议，不是已确认的 `role`，不得据此填写 `tags`;
  `opcua_health_summary` 阈值分类;`opcua_anomaly_scan` 有界统计异常扫描

### 跨协议脑（永远随 server 暴露）
- 诊断：`diagnose_dataflow` `downtime_root_cause` `downtime_root_cause_live` `downtime_triage`
  `learn_cause_weights` `rca_corpus_from_maintenance` `historian_health` `alarm_bad_actors` `tag_health`
  `subscription_health` `heartbeat_health` `alarm_flood_analysis` `alarm_cascade`
  `alarm_rationalization_worksheet`
- 预测维护：`pdm_forecast` —— 制冷/空压/真空泵趋势 + 到限时间
- 告警事件聚类：`alarm_event_clusters` — `alarm_bad_actors` 按**来源**排名,回答的是「哪台仪表最吵」,
  不是「哪个故障最吵」;一个把同一条件写成十种说法的厂会得到十个 bad actor。这个按事件**说了什么**分组。
  合并规则是**去掉大小写/标点/数字后的精确相等,不是相似度** —— 故意做笨,所以不需要模型、且可核对;
  每个簇都列出被合并的原文与来源。**它不主张两条措辞不同的告警是同一个故障**,那由人判断。
- 数据质量：`data_quality_scorecard` `data_quality_fleet_rollup`
- 分析：`oee_compute` `downtime_events` `oee_multidim` `monitor_changes`
- 上下文基线：`baseline_learn_contextual` `baseline_check_in_context` —— 一个位号只学一条带,
  在它有不止一个「正常」时就是错的(同一台干燥机 recipe A 走 180 °C、B 走 240 °C,一条带横跨两者,
  于是两个工况都不可能出错)。**上下文由人声明,绝不推断**(D16);某个上下文历史太薄就**拒学**,
  不借用别的上下文的样本;读数落在没学过的上下文里报 `unknown_context`,**绝不回落到全局带** ——
  回落等于把「这个工况从没见过」说成「这个工况正常」。
- 上下游归因：`downtime_attribution` —— RCA 只按**时间**加权,所以一次上游停机会让每台下游设备
  各自给出一个自信的本地根因。方向来自**声明的**产线顺序(D25:产线上共现是必然,拿它挖边等于
  制造因果),顺序来自时间戳,**两者都要成立**;没声明关系就报 `not_evaluable` 并给出补法。
- 资产：`asset_inventory` `cross_protocol_asset_model` `adopt_alias_map` `diff_alias_map`
- 设备公告对照：`device_advisory_check` —— `scan` 早就在读 vendor/model/firmware,却什么都没做。
  这条把它接上,并**刻意停在漏洞扫描器会继续往前走的地方**:只报「落在公告声明的版本范围内」,
  **不说「可利用」、不给严重度** —— 可达性与补偿控制决定那件事,而只读扫描看不见它们。
  **不内置任何 CVE 库**(过期却看着像最新的库比没有更糟),由现场挂载文件、离线可用,每条必须带来源。
  读不出固件报 `version_unknown`,读得出但排不了序报 `version_unparsed` —— 都不算通过;
  公告没提到的设备**不出现在结果里**,那是「未知」不是「没有」。
- 基线：`baseline_learn` `baseline_check` `baseline_record_change` `baseline_status`
- 合规/信创：`compliance_mapping` `compliance_frameworks` `compliance_dengbao_levels`
  `compliance_report` `compliance_evidence_bundle`
  `historian_push` `export_data` `historian_query` `historian_coverage` `stream_publish` `uns_publish`
  `stream_publish_event` `rca_narrate` `fleet_status` `fleet_incidents`
- 程序解读：`plc_program_outline` `plc_program_xref` `plc_program_section` `plc_program_visibility` `plc_program_xref_config`
- 导出来源守卫（#282）：AWL/SCL 的 `--live` 只允许 CLI 操作者显式给出 `--confirm-export-origin` 且 CPU 为 RUN；MCP 不能声明来源，故拒绝这类 live 读。S7 STOP/未知态也拒读。L5X/Logix 在线控制器名匹配仅是有限证据，不能证明导出来源。
- 程序变更基线：`plc_program_snapshot` `plc_program_drift` `plc_program_history` — 把「认可的那一版」
  的结构记下来（文件 SHA-256 + 每个 block 的结构指纹：声明/调用/分支条件/定时器，**不含行号、注释、
  block 顺序**，所以在文件顶上加一行注释不会把整份程序报成变更），之后问某一次导出**动没动**。
  三个判词咬得很紧：`identical` **只**由 SHA-256 相同得出；`logic_changed` 逐 block 指出哪一类变了；
  `changed_outside_extracted_structure` = 字节变了而结构指纹全同 —— 多半是注释/排版，但这些 parser
  是结构抽取不是文法，**所以它不叫「仅文档」，也不构成放行**。删历史只在 CLI（`iaiops program forget`）：
  删变更控制证据不该离 agent 只有一次调用。存的是 block 名 + 哈希 + 计数，**不落声明、源码行和注释**。
- 自证：`verify_determinism` — 把「拿掉模型、断网、同一份数据重跑、输出逐字节相同」**跑出来**：
  固定数据集过一遍分析层，规范化后取 SHA-256，在本进程跑两遍、再在两个不同 PYTHONHASHSEED 的
  全新解释器里各跑一遍（这一臂才抓得到集合/字典迭代顺序渗进结果），全程 socket 抛异常。
  给 CSV/验证团队的是一条能写进 IQ/OQ 的测试用例，不是一句形容词。
- 元：`protocols_supported`(产品能做什么)· `site_readiness`(这个站点今天能跑什么、还差什么;零联网)
  · `onboarding_status`(先判定路线：设备直读 / 已在 UNS broker，UNS 再按已存体检分 B1/B2；再给这条路上的下一步;零联网)
  · `onboarding_config_draft`(把已存的 scan 变成 config.yaml 端点草稿 —— **只写连接事实**：
    `value: null` 的字段是扫描没确认的，照抄它的 `caution`，别替人填也别删；`tags` 永远是空的，
    点位语义只能人来确认 `iaiops tags export|apply`)
- 调查层（§13，八步证据闭环）：`investigation_readiness` `investigation_open` `investigation_show`
  `investigation_list` — 「真出事时这个站能走到第几步、每个缺口还差什么」，以及对一个**已过去的窗口**
  逐步走完并留档（不碰设备）。缺口分两种:**你没供**(给命令) 与 **产品供不了**。
- 产线关系与机制库：`line_relation_declare` `line_relations_list` `mechanism_library_check`
  `mechanism_library_list` — 上下游由**人声明**（D25:线上下游共现是必然，推不出因果）；
  机制库按 ISO 14224 分 mode/mechanism/cause，**可排除、绝不确认**，
  库里没有这条原因 → `nothing_known`（不是「无异议」）。


## Workflows

- **SIS 禁写**：端点 `safety: sis` 拒绝所有设备写（包括 dry-run 预览），已有审批也不能放行；只读仍可用。

1. **Doctor-first**：`protocols_supported` → `iaiops doctor` → BACnet 先 `bacnet_discover`。
2. **患者安全巡检**：`bacnet_read_points` 读隔离房压差 AI 点 → `isolation_room_check`;
   读医用气体源压力点 → `medical_gas_check`。两者 worst-first,`reversed`/`critical`
   优先处置。**判定仅为结构性分析,现场 NFPA 99 报警屏/感控为准**。
3. **停机/告警**：设施设备停机用 `downtime_triage`;制冷/真空泵劣化用 `pdm_forecast`。
4. **MOC 写**：本 edition **读优先**;`bacnet_write_property` 为唯一写工具,统一走 MOC:
   `risk=HIGH` + 默认 `dry_run=True` + 改前值 undo + `iaiops approve` 具名审批双确认。
   **绝不对生命安全相关的暖通/气体系统未经授权下发。**

## 支持版本矩阵（内部 HLD §8，设计文档不随本仓发布;`待核实` 不得当既成事实）

| 协议 | 库(pin) | 规范/版本 | 覆盖 | 传输 | 自测 |
|---|---|---|---|---|---|
| BACnet/IP | `BAC0>=2023.6,<2026`（extra,over bacpypes3） | BACnet/IP（read + 单点写） | BMS/暖通/压力/气体点 | UDP/47808 | ⚠️ mock;真 BMS 待核实 |
| Modbus-TCP | `pymodbus>=3.5,<4` | App 1.1b3;FC 1/2/3/4/5/6/15/16 | 气体报警屏/表计/任意从站 | TCP/502 | ✅ |
| Modbus-RTU | `pymodbus>=3.5,<4` + `pyserial>=3.5` | Modbus serial (RTU) | 串口从站/表计 | RS-485/serial | ✅ socat PTY;物理 RS-485 待核实 |
| OPC-UA | `asyncua>=2.0,<3` | OPC UA 1.0x（DA+HA+AC 子集） | 全院 SCADA / PLC 网关 | opc.tcp | ✅ mock+HDA |

## 文件路径限制（0.31.0 起）

MCP 里**读**主机文件的工具（`plc_program_*`、`device_advisory_check`、`db=` 覆盖等）只读 `$IAIOPS_HOME`、配置目录和运维方在 `IAIOPS_AGENT_READ_DIRS` 列出的目录；**写**文件的工具（`export_data`、`compliance_report`、`compliance_evidence_bundle`、`alarm_rationalization_worksheet`）只写 `$IAIOPS_HOME/exports` 和 `IAIOPS_AGENT_WRITE_DIRS`。超出就拒绝——把文件放进这些目录，或让运维方在 shell 里跑 `iaiops` 命令（CLI 不受限）。
