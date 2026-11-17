---
name: iaiops-water
description: >-
  Water-treatment edition of iaiops — waterworks / wastewater plants / pump
  stations: Modbus-TCP/RTU (dosing skids, analyzers, flow meters), OPC-UA
  (plant SCADA / PLC read), HART-IP process instrumentation (pH, turbidity,
  conductivity, level, flow transmitters), plus the cross-protocol brain
  (downtime root-cause, data quality watchdog, OEE). Use when the task mentions
  water treatment, 水处理, 水厂, 污水, pH, 浊度, turbidity, 电导率, conductivity,
  dissolved oxygen, 加药, dosing pump, 泵站, pump station, aeration / 曝气, or
  lift station. Read-first; this edition's tool surface is read-only.
---

# iaiops-water — 水处理 edition（Modbus + OPC-UA + HART + 脑）

启动：`IAIOPS_MCP=water` / `iaiops-mcp-water`（= modbus + opcua + hart + 脑；
等价显式写法 `IAIOPS_MCP=modbus,opcua,hart`）。HART 需 extra：
`pip install iaiops[hart]`。典型现场：加药撬/分析仪走 Modbus，全厂 SCADA 走
OPC-UA，pH/浊度/电导率/液位/流量变送器走 HART（经网关）。

## 工具

### Modbus-TCP / Modbus-RTU（只读；加药撬、分析仪、流量计、泵站 RTU）
- `modbus_read_holding` `modbus_read_input` `modbus_read_coils` `modbus_read_discrete`
- `modbus_detect_byte_order` — 字节/字序自动探测（分析仪浮点数常见坑）
- `modbus_list_templates` / `modbus_apply_template` — 厂商寄存器模板 → 命名 tag
- `modbus_health_summary` — 寄存器 vs 阈值分类（如 pH 6.5-8.5 带）

### OPC-UA（只读；全厂 SCADA / PLC 网关）
- `opcua_server_info` / `opcua_browse` / `opcua_read_node` / `opcua_read_many`
- `opcua_subscribe_sample` `opcua_read_alarms` `opcua_alarm_events`(A&C 带时间戳) `opcua_read_history`(HDA)
- `opcua_diagnose_connection` — 连接失败归因（证书/策略/认证/网络/配置）
- `opcua_discover_tags` — 发现点位并给出启发式语义建议（构筑物/工艺段/设备）；不是已确认的 `role`，不得据此填写 `tags`
- `opcua_health_summary` — tag vs 阈值分类；`opcua_anomaly_scan` — 有界统计异常扫描

### HART-IP（只读；水质/过程变送器，经网关，端口 5094）
- `hart_device_identity` — 通用设备身份（command 0）
- `hart_primary_variable` — 主变量 PV（如 pH 值、NTU）
- `hart_dynamic_variables` — PV/SV/TV/QV + 回路电流（command 3）
- `hart_burst_sample` — 主动采样 burst 变量；`hart_burst_listen` — 被动监听 burst publish（待核实）

### 水处理专属（edition 工具;仅随 water edition 加载,不进全局脑）
- `disinfection_ct` — SWTR **消毒 CT 合规**:CT = 余氯(mg/L)×有效接触时间 T10(min);逐个
  接触池算 achieved CT 对比所需 CT(按州 CT 表按温度/pH/消毒剂查得,由调用方传入),给达标比与
  worst-first。纯分析,不内嵌 CT 表(传 required_ct);每比值引用输入。
- `water_quality_compliance` — **出厂水质合规**:逐采样点对浊度/余氯/pH 判限值(默认浊度 ≤1.0 NTU、
  余氯 0.2–4.0 mg/L、pH 6.5–8.5;可按许可证覆盖),越界即 breach,worst-first,引用数值。

### 跨协议脑（永远随 server 暴露）
- 诊断：`diagnose_dataflow` `downtime_root_cause` `downtime_root_cause_live` `downtime_triage`
  `learn_cause_weights` `rca_corpus_from_maintenance` `historian_health` `alarm_bad_actors` `tag_health`
  `subscription_health` `heartbeat_health` `alarm_flood_analysis` `alarm_cascade`
  `alarm_rationalization_worksheet`
- 告警事件聚类：`alarm_event_clusters` — `alarm_bad_actors` 按**来源**排名,回答的是「哪台仪表最吵」,
  不是「哪个故障最吵」;一个把同一条件写成十种说法的厂会得到十个 bad actor。这个按事件**说了什么**分组。
  合并规则是**去掉大小写/标点/数字后的精确相等,不是相似度** —— 故意做笨,所以不需要模型、且可核对;
  每个簇都列出被合并的原文与来源。**它不主张两条措辞不同的告警是同一个故障**,那由人判断。
- 数据质量：`data_quality_scorecard` `data_quality_fleet_rollup`（水质仪表重点：
  电极老化 flatline / staleness / 量程外 —— 坏数据绝不静默插值）
- 分析：`oee_compute` `downtime_events` `oee_multidim` `monitor_changes`
  `health_summary` (deprecated) `anomaly_scan` (deprecated)
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
  （change-log 基线：拒学薄历史、只报持续越带、每次告警必引基线样本 —— 非黑盒异常检测）
- 合规/信创：`compliance_mapping` `compliance_frameworks` `compliance_dengbao_levels`
  `compliance_report` `compliance_evidence_bundle`
  `historian_push` `export_data` `historian_query` `historian_coverage` `stream_publish` `uns_publish` `stream_publish_event` `rca_narrate` `fleet_status` `fleet_incidents` `pdm_forecast`
  `historian_push` `export_data`
- 程序解读：`plc_program_outline` `plc_program_xref` `plc_program_section` `plc_program_visibility` `plc_program_xref_config`（解读导出的 ST/AWL/L5X 程序,只读文件,强制引用行号）
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

1. **Doctor-first**：`protocols_supported` → `iaiops doctor` → HART 先
   `hart_device_identity`，OPC-UA 先 `opcua_diagnose_connection`。
2. **Read-first**：水质巡检 = `modbus_apply_template`/`hart_primary_variable` 读
   pH/浊度/电导率 → `opcua_health_summary` 对阈值 → 异常用 `opcua_anomaly_scan`；
   泵站"没数据"用 `diagnose_dataflow`，停机用 `downtime_root_cause_live`。
3. **MOC 写**：本 edition 工具表面**全只读**（加药量/泵启停不经本工具下发）。
   若现场确需写，须切到含写工具的 profile 并走统一 MOC：`risk=HIGH` +
   默认 `dry_run=True` + 改前值 undo + `iaiops approve` 具名审批双确认。
   未经授权绝不写生产控制系统。

## 支持版本矩阵（内部 HLD §8，设计文档不随本仓发布；`待核实` 不得当既成事实）

| 协议 | 库(pin) | 规范/版本 | 覆盖 | 传输 | 自测 |
|---|---|---|---|---|---|
| Modbus-TCP | `pymodbus>=3.5,<4` | App 1.1b3；FC 1/2/3/4/5/6/15/16 | 分析仪/加药撬/任意 TCP 从站 | TCP/502 | ✅ |
| Modbus-RTU | `pymodbus>=3.5,<4` + `pyserial>=3.5` | Modbus serial (RTU) | 串口从站（泵站 RTU/表计） | RS-485/serial | ✅ socat PTY verified 2026-07-02；物理 RS-485 待核实 |
| OPC-UA | `asyncua>=2.0,<3` | OPC UA 1.0x（DA+HA+AC 子集） | 任意合规 Server / SCADA | opc.tcp | ✅ mock+HDA |
| HART-IP | `hart-protocol>=2023.6,<2025`（extra） | HART-IP（经网关） | 水质/过程变送器 | UDP/TCP 5094 | ⚠️ codec CI 自测；真机网关 待核实 |

## 文件路径限制（0.31.0 起）

MCP 里**读**主机文件的工具（`plc_program_*`、`device_advisory_check`、`db=` 覆盖等）只读 `$IAIOPS_HOME`、配置目录和运维方在 `IAIOPS_AGENT_READ_DIRS` 列出的目录；**写**文件的工具（`export_data`、`compliance_report`、`compliance_evidence_bundle`、`alarm_rationalization_worksheet`）只写 `$IAIOPS_HOME/exports` 和 `IAIOPS_AGENT_WRITE_DIRS`。超出就拒绝——把文件放进这些目录，或让运维方在 shell 里跑 `iaiops` 命令（CLI 不受限）。
