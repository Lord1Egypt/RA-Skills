---
name: iaiops-renewables
description: >-
  Renewables edition of iaiops — solar PV plants and wind farms: PV inverters /
  string combiners and wind-turbine controllers over Modbus (SUN2000 / Growatt /
  generic wind-turbine templates), plant SCADA over OPC-UA, and MQTT-Sparkplug
  telemetry, plus the cross-protocol brain (PdM, downtime, OEE, alarm) and a
  renewables signature tool pv_performance (underperforming-string detection).
  Use when the task mentions solar / 光伏 / PV / photovoltaic, inverter / 逆变器 /
  组串 / string / combiner, irradiance / 辐照 / POA, wind / 风电 / turbine / 风机 /
  nacelle / pitch / yaw, plant SCADA, performance ratio, soiling / 积灰 / shading /
  遮挡, or 电站. Read-first; MQTT publish is MOC-gated.
  Also supplier half-hourly (HH) electricity files for the site's import meter — base load, out-of-hours use, tariff time bands.
---

# iaiops-renewables — 光伏 / 风电 edition（Modbus + OPC-UA + Sparkplug + 脑）

启动：`IAIOPS_MCP=renewables` / `iaiops-mcp-renewables`（= modbus + opcua + sparkplug
+ 脑；等价 `IAIOPS_MCP=modbus,opcua,sparkplug`）。典型现场：逆变器/组串汇流箱、风机控制器
走 Modbus,全站 SCADA 走 OPC-UA,遥测经 MQTT-Sparkplug。语义层已含 irradiance / wind_speed /
rotor_speed / pitch / yaw / state_of_charge 等可再生类别（`opcua_discover_tags` 只给启发式类别建议；不是已确认的 `role`，不得据此填写 `tags`）。

## 工具

### 可再生专属（edition 工具;仅随 renewables edition 加载,不进全局脑）
- `pv_performance` — **组串/逆变器欠发检测**:算各组串性能比(有 `expected_w` 用之,或
  额定×辐照/1000,否则对全场中位数),低于阈值即 underperforming(积灰/遮挡/熔丝断/组件失效),
  ~0 功率为 offline。worst-first,每比值引用输入。纯分析,喂逆变器/汇流箱 Modbus 或站 SCADA。

### Modbus-TCP / RTU（只读;逆变器、汇流箱、风机控制器、表计）
- `modbus_read_holding` `modbus_read_input` `modbus_read_coils` `modbus_read_discrete`
- `modbus_detect_byte_order` — 字节/字序自动探测
- `modbus_list_templates` / `modbus_apply_template` — 厂商模板 → 命名 tag
  （可再生模板:`huawei_sun2000_inverter`、`growatt_inverter`、`generic_wind_turbine`;均 `待核实`）
- `modbus_health_summary` — 寄存器 vs 阈值分类

### OPC-UA（只读;全站 SCADA / PLC 网关）
- `opcua_server_info` / `opcua_browse` / `opcua_read_node` / `opcua_read_many`
- `opcua_subscribe_sample` `opcua_read_alarms` `opcua_alarm_events`(A&C 带时间戳) `opcua_read_history`(HDA)
- `opcua_diagnose_connection` `opcua_discover_tags` `opcua_health_summary` `opcua_anomaly_scan`

### MQTT-Sparkplug B（可选;电站遥测 / IoT 网关 UNS）
- `sparkplug_node_list` `sparkplug_subscribe_sample` `sparkplug_decode_payload`
- `mqtt_read_topic` `sparkplug_live_schema` `sparkplug_point_draft`
- `mqtt_publish` — **[WRITE][HIGH][MOC]**（默认 dry-run；需具名审批）
- UNS 选点：`iaiops mqtt point-draft --endpoint <name>` 或 MCP `sparkplug_point_draft`
  从有界 BIRTH 捕获提出未确认 refs；`role`/`label` 留空，由现场人员确认，不写配置。
- `uns_browse` `uns_topic_audit` `uns_schema_drift` `uns_live_audit` `uns_live_drift`

### 半小时电表数据（edition 工具;随 building / renewables 加载;只读,不连设备）
- `meter_hh_check` — 供应商半小时(HH)CSV 里有什么:宽表(日期 + 46–50 时段列)或长表(时间戳 + kWh)、
  各 MPAN 起止、被拒的行/格及原因、解析时做的每个假设。空格/非数字=**缺失,不是 0**;日期只认英式日在前。
- `meter_load_profile` — 每个表:覆盖率(缺口计数,**不外推**)、实测 kWh、估算读数占比(文件无标志时为
  `unknown`)、峰值 kW 及时间、夜间基础负荷(00:00–05:00 中位数)、按**声明的**营业时间算的非营业时段用电、
  高于基础负荷的非营业用电(**机会提示,不是保证的节省**)、完整日工作日/休息日均值、负荷率、发现与警告;
  传 `tariff` 时按时段算钱 + 移出最贵时段的**上限**(不含 VAT/CCL/kVA/DUoS 单列项)。
- HTML 报告只在 CLI:`iaiops meter profile FILE --tariff t.yaml --report out.html`。DUoS 红/黄/绿时段因配网区域而异,
  **不内置**,请按合同写进 tariff。示例:`demo/metering/`。

### 跨协议脑（永远随 server 暴露）
- 诊断：`diagnose_dataflow` `downtime_root_cause` `downtime_root_cause_live` `downtime_triage`
  `learn_cause_weights` `rca_corpus_from_maintenance` `historian_health` `alarm_bad_actors` `tag_health`
  `subscription_health` `heartbeat_health` `alarm_flood_analysis` `alarm_cascade`
  `alarm_rationalization_worksheet`
- 预测维护：`pdm_forecast` —— 逆变器温升、风机轴承/齿轮箱趋势 + 到限时间
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

1. **Doctor-first**：`protocols_supported` → `iaiops doctor` → OPC-UA 先 `opcua_diagnose_connection`。
2. **欠发排查**：`modbus_apply_template`(`huawei_sun2000_inverter`) 读各组串功率(+辐照) →
   `pv_performance` 排欠发组串 → 结合 `pdm_forecast` 盯逆变器温升趋势。
3. **停机/告警**：`downtime_triage`;风机齿轮箱/轴承劣化用 `pdm_forecast`。
4. **MOC 写**：逆变器限功率/风机偏航不经本工具下发；可选的 `mqtt_publish` 是
   **[WRITE][HIGH][MOC]**，默认 dry-run，需具名审批与双确认。

## 支持版本矩阵（内部 HLD §8，设计文档不随本仓发布;`待核实` 不得当既成事实）

| 协议 | 库(pin) | 规范/版本 | 覆盖 | 传输 | 自测 |
|---|---|---|---|---|---|
| Modbus-TCP | `pymodbus>=3.5,<4` | App 1.1b3;FC 1/2/3/4/5/6/15/16 | 逆变器/汇流箱/风机/表计 | TCP/502 | ✅ |
| Modbus-RTU | `pymodbus>=3.5,<4` + `pyserial>=3.5` | Modbus serial (RTU) | 串口从站/表计 | RS-485/serial | ✅ socat PTY;物理 RS-485 待核实 |
| OPC-UA | `asyncua>=2.0,<3` | OPC UA 1.0x（DA+HA+AC 子集） | 全站 SCADA / PLC 网关 | opc.tcp | ✅ mock+HDA |
| MQTT-Sparkplug B | `paho-mqtt>=2.0,<3`（extra） | Sparkplug B 3.0 | 电站遥测 / IoT 网关 UNS | MQTT/1883/8883 | ✅ broker mock |

## 文件路径限制（0.31.0 起）

MCP 里**读**主机文件的工具（`plc_program_*`、`device_advisory_check`、`db=` 覆盖等）只读 `$IAIOPS_HOME`、配置目录和运维方在 `IAIOPS_AGENT_READ_DIRS` 列出的目录；**写**文件的工具（`export_data`、`compliance_report`、`compliance_evidence_bundle`、`alarm_rationalization_worksheet`）只写 `$IAIOPS_HOME/exports` 和 `IAIOPS_AGENT_WRITE_DIRS`。超出就拒绝——把文件放进这些目录，或让运维方在 shell 里跑 `iaiops` 命令（CLI 不受限）。
