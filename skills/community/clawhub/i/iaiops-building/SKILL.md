---
name: iaiops-building
description: >-
  Building edition of iaiops — facility / HVAC / BMS / 厂务 over BACnet/IP
  (ASHRAE 135): Who-Is discovery, object/point lists, presentValue snapshots, COV
  capture, TrendLog reads, one MOC-gated property write; plus Modbus-TCP/RTU for
  meters/chillers and optional plain MQTT for IoT sensors, with the
  cross-protocol brain. Use when the task mentions BACnet, BACnet-IP, HVAC, AHU,
  chiller, VAV, BMS, building automation, facility management, 厂务, 楼宇自控,
  Who-Is, presentValue, or TrendLog; also IO-Link masters for smart building
  sensors (JSON interface, read-only), and the vendor supervisory-controller REST
  layer above BACnet (Metasys/OpenBlue, Niagara/oBIX) for point/alarm/trend reads
  and one MOC-gated command. Read-first, MOC-gated writes.
  Also supplier half-hourly (HH) electricity files — MPAN, base load, out-of-hours use, tariff time bands (meter_hh_check / meter_load_profile).
---

# iaiops-building — 楼宇/厂务 edition（BACnet + Modbus + IO-Link + MQTT + 脑）

启动：`IAIOPS_MCP=building` / `iaiops-mcp-building`（= bacnet + modbus + opcua + iolink + 脑）。
IoT 传感器走 MQTT 时叠加：`IAIOPS_MCP=building,sparkplug`。
安装：`pip install iaiops[building]`。BACnet 的 `host` 是**本机** BACnet/IP 接口
（`ip` 或 `ip/mask`）。

## 工具

### BACnet/IP（read-first；暖通/楼宇/厂务）
- `bacnet_discover` — Who-Is：本地 BACnet/IP 网上的设备
- `bacnet_object_list` — 设备的 object/point 列表
- `bacnet_read_property` — 单对象属性（默认 presentValue）
- `bacnet_read_points` — 所有 analog/binary/multistate 点的 presentValue（HVAC 快照）
- `bacnet_cov_subscribe` — 单对象有界 Change-of-Value 捕获
- `bacnet_read_trend_log` — 读设备 TrendLog 缓冲记录
- `bacnet_write_property` — **[WRITE][HIGH][MOC]** 写单对象属性（默认 off：
  `dry_run=True` + 审批双确认；可指挥楼宇设备 — 设定值、输出）

### Modbus-TCP / Modbus-RTU（只读；电表/冷机/表计）
- `modbus_read_holding` `modbus_read_input` `modbus_read_coils` `modbus_read_discrete`
- `modbus_detect_byte_order` / `modbus_list_templates` / `modbus_apply_template`
- `modbus_health_summary`

### IO-Link（只读；主站 JSON 接口 — 楼宇智能传感器）
- `iolink_master_info` — 主站身份（/deviceinfo）
- `iolink_ports` — 有界端口扫描（≤32：mode/status + 在线设备身份）
- `iolink_device_info` — 单端口设备身份
- `iolink_read_pdin` — 过程数据输入（raw hex + 字节数组；按 IODD 解码）
- `iolink_read_isdu` — ISDU 参数读（index/subindex 有界）
- `iolink_scan` — 主站 + 全端口一次性快照
- 配置 `flavor: iotcore`（ifm IoT-Core，默认）或 `rest`（plain-REST 主站）；v1 只读

### BAS 控制器层（edition 工具；厂商监控控制器 REST，在 BACnet **之上**）
厂商监控控制器（Johnson Controls Metasys/OpenBlue、Tridium Niagara oBIX/REST）把大量 BACnet
现场点/告警/趋势聚合在一个带鉴权的企业 REST 接口后面——与 `bacnet`（现场总线）互补、非重复。
Bearer/token 从加密 secret store 按 key 取（`secret_name`），不走明文参数。
- `bas_point_list` — 列控制器 point/object（跨厂商归一化：id/name/value/unit/status）
- `bas_point_read` — 单/多点 present-value
- `bas_alarm_list` — 控制器活动告警/事件（归一化）
- `bas_trend_read` — 单点历史趋势样本（有界 ≤5000）
- `bas_command` — **[WRITE][HIGH][MOC]**（默认 off：`dry_run=True` + 审批双确认；捕获改前值供 undo）。
  **生命安全点(fire/smoke/egress/加压)一律拒绝**——联网前即拒，绝不下发。
- 厂商方言（metasys/niagara：资源路径 + 字段别名）仅存在于连接器内；oBIX 原生 XML / 精确写语义 待核实。

### MQTT（可选叠加 sparkplug 组；IoT 传感器/网关）
- `mqtt_read_topic` — 裸 MQTT 有界收集；`uns_browse` — 主题树浏览
- 完整 Sparkplug B/UNS 工具清单见 **iaiops-factory** skill
- `mqtt_publish` — **[WRITE][HIGH][MOC]**（默认 off）

### 楼宇专属（edition 工具;仅随 building edition 加载,不进全局脑）
- `economizer_check` — AHU **经济器故障检测(FDD)**:检出同时供冷供热(纯浪费)、该用自然冷却
  却没用(室外够冷但新风阀在最小位且机械制冷开)、越高限还开阀(把热风引进来)。逐 AHU 判定,
  worst-first,每故障引用温度/状态。读数来自 BACnet AI/BI 点。
- `zone_comfort` — **区域舒适度 + 室内空气质量**(ASHRAE 55/62.1):逐区判温度 20–26°C、相对湿度
  30–60%、CO₂ ≤1000 ppm(通风充分性代理),越界即 breach,worst-first,引用数值。读数来自 BACnet AI 点。

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
- 告警事件聚类：`alarm_event_clusters` — `alarm_bad_actors` 按**来源**排名,回答的是「哪台仪表最吵」,
  不是「哪个故障最吵」;一个把同一条件写成十种说法的厂会得到十个 bad actor。这个按事件**说了什么**分组。
  合并规则是**去掉大小写/标点/数字后的精确相等,不是相似度** —— 故意做笨,所以不需要模型、且可核对;
  每个簇都列出被合并的原文与来源。**它不主张两条措辞不同的告警是同一个故障**,那由人判断。
- 数据质量：`data_quality_scorecard` `data_quality_fleet_rollup`
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
- 医疗设施（healthcare facility 安全）：`isolation_room_check` — 隔离病房压差合规（ASHRAE 170 / CDC：空气传染隔离 AII 负压、保护性环境 PE 正压，≥2.5 Pa）；检出反向/不足/低裕度,worst-first,每项引用读数。读数来自 `bacnet_read_points` 的压差 AI 点或历史库,纯分析。
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

1. **Doctor-first**：`protocols_supported` → `iaiops doctor` → `bacnet_discover`
   （Who-Is 有响应才谈读点）。
2. **Read-first**：`bacnet_object_list` → `bacnet_read_points` 快照 →
   趋势用 `bacnet_read_trend_log`，变化捕获用 `bacnet_cov_subscribe`；
   "没数据"用 `diagnose_dataflow`，坏点排名用 `tag_health`。
3. **MOC 写**：`bacnet_write_property`、`bas_command`（与可选 `mqtt_publish`）为
   **[WRITE][HIGH][MOC]**：默认 `dry_run=True`、捕获改前值供 undo、
   `iaiops approve` 具名审批双确认。写设定值可影响在运楼宇设备 ——
   未经授权绝不写。

## 支持版本矩阵（内部 HLD §8，设计文档不随本仓发布；`待核实` 不得当既成事实）

| 协议 | 库(pin) | 规范/版本 | 覆盖 | 传输 | 自测 |
|---|---|---|---|---|---|
| BACnet/IP | `BAC0>=2023.6,<2026`（extra） | ASHRAE 135 Annex J | 暖通/楼宇/厂务控制器 | UDP/47808 | ✅ 读路径 verified 2026-07-02（真 bacpypes3 虚拟设备）；live HVAC 写/COV/trend 待核实 |
| Modbus-TCP | `pymodbus>=3.5,<4` | App 1.1b3；FC 1/2/3/4/5/6/15/16 | 电表/冷机/任意 TCP 从站 | TCP/502 | ✅ |
| Modbus-RTU | `pymodbus>=3.5,<4` + `pyserial>=3.5` | Modbus serial (RTU) | 串口表计 | RS-485/serial | ✅ socat PTY verified 2026-07-02；物理 RS-485 待核实 |
| IO-Link | `requests>=2.31,<3`（复用 MTConnect pin） | IO-Link Master JSON Integration（IOLINK-JSON）；ifm IoT-Core / plain-REST 双 flavor | 带 JSON/REST 接口的主站（ifm/Balluff/Turck 类） | HTTP REST/JSON | ✅ mock 主站（双 flavor）；live master 待核实 |
| MQTT | `paho-mqtt>=2.0,<3` | MQTT 3.1.1/5（裸 MQTT + SpB） | IoT 传感器/网关/Broker | TCP/1883/8883 | ✅ |
| BAS: Metasys OpenBlue REST | `requests>=2.31,<3`（复用 MTConnect pin，无新 HTTP 依赖） | Metasys REST API v4（`/objects`·`/alarms`·`/trendedAttributes`）；JC OpenBlue 监控控制器 | NAE/SNE/SNC 类监控控制器聚合的 BACnet 现场点 | HTTPS + Bearer token | ✅ mock 控制器（in-repo）；live 设备写/trend/告警 待核实 |
| BAS: Niagara 4 oBIX/REST | `requests>=2.31,<3`（复用 MTConnect pin，无新 HTTP 依赖） | Niagara 4 oBIX/REST（`/obix/config`·`/obix/alarms`·`/obix/histories`）；JSON 建模，原生 oBIX-XML 待核实 | Tridium JACE / Niagara Supervisor 下的点/告警/历史 | HTTPS + Bearer token | ✅ mock 控制器（in-repo）；live 设备 + oBIX-XML 编码 待核实 |

## 文件路径限制（0.31.0 起）

MCP 里**读**主机文件的工具（`plc_program_*`、`device_advisory_check`、`db=` 覆盖等）只读 `$IAIOPS_HOME`、配置目录和运维方在 `IAIOPS_AGENT_READ_DIRS` 列出的目录；**写**文件的工具（`export_data`、`compliance_report`、`compliance_evidence_bundle`、`alarm_rationalization_worksheet`）只写 `$IAIOPS_HOME/exports` 和 `IAIOPS_AGENT_WRITE_DIRS`。超出就拒绝——把文件放进这些目录，或让运维方在 shell 里跑 `iaiops` 命令（CLI 不受限）。
