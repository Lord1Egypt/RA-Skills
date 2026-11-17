---
name: iaiops-warehouse
description: >-
  Warehouse / intralogistics edition of iaiops — distribution centers, fulfillment,
  material handling: conveyors, sorters, palletizers, AS/RS, and AGV/AMR fleets.
  EtherNet/IP (Allen-Bradley / Rockwell conveyor & sorter PLCs), Profinet (Siemens
  material-handling lines), Modbus (VFDs / energy meters, with conveyor_vfd &
  agv_battery templates), OPC-UA (WMS/WCS gateways), and MQTT-Sparkplug (AMR / IoT
  telemetry) — plus the cross-protocol brain: predictive maintenance (pdm_forecast
  for conveyor-drive bearing/thermal trend), downtime triage, OEE/throughput, and
  alarm analysis. Use when the task mentions warehouse, 仓储, 物流, intralogistics,
  distribution center / DC, fulfillment, conveyor / 输送线, sorter / 分拣, palletizer,
  AS/RS / 立体库, AGV / AMR / 移动机器人, WMS / WCS, or material handling. Read-first;
  MQTT publish is MOC-gated; read-first.
---

# iaiops-warehouse — 仓储 / 物料搬运 edition（EtherNet/IP + Profinet + Modbus + OPC-UA + Sparkplug + 脑）

启动：`IAIOPS_MCP=warehouse` / `iaiops-mcp-warehouse`（= eip + profinet + modbus + opcua
+ sparkplug + 脑；等价显式写法 `IAIOPS_MCP=eip,profinet,modbus,opcua,sparkplug`）。
EtherNet/IP 需 extra：`pip install iaiops[eip]`。典型现场：输送/分拣 PLC 走
EtherNet/IP(Rockwell) 或 Profinet(Siemens),驱动/表计走 Modbus,WMS/WCS 网关走
OPC-UA,AGV/AMR 与 IoT 传感走 MQTT-Sparkplug。

> **定位**：复用既有跨协议脑的 **PdM（`pdm_forecast`）/ 停机分诊（`downtime_triage`）/
> OEE / 告警** 能力,针对物料搬运资产(输送带电机轴承、分拣驱动、AGV 电池)对症使用,提供
> 物料搬运专用的 Modbus 模板,并带一个 **仓储专属 edition 工具 `line_bottleneck`**
> (瓶颈工位定位;仅随本 edition 加载,不进全局脑)。

## 工具

### EtherNet/IP（Rockwell 输送/分拣 PLC；写=MOC）
- `eip_controller_info` — 控制器身份/状态
- `eip_list_tags` — 控制器 tag 列表
- `eip_read_tag` / `eip_read_many` — 读单/多 tag（输送段状态、分拣计数、速度）
- `eip_write_tag` — **[WRITE][HIGH][MOC]** 写 tag（默认 `dry_run=True` + 改前值 undo + 双确认）
- `plctype` 入参（或 config key）选驱动：`logix`（默认 Logix 符号 tag）、`slc`（老 AB 输送/分拣
  PLC-5/SLC-500/MicroLogix 走 PCCC 数据表 `N7:0`/`B3:0/0`/`F8:0`）、`micro800`。真 PCCC/Micro800 待核实。

### Profinet（Siemens 物料搬运线）
- `profinet_discover` — DCP 发现网上 IO 设备/station
- `profinet_identify_station` / `profinet_station_params` — station 身份与参数
- `profinet_asset_inventory` — IO 设备资产清单
- `profinet_dcp_set` — **[WRITE][HIGH][MOC]** DCP 设置站名/IP（默认 dry-run + 双确认）

### Modbus-TCP / RTU（只读；VFD 驱动、能耗表、AGV 电池 BMS）
- `modbus_read_holding` `modbus_read_input` `modbus_read_coils` `modbus_read_discrete`
- `modbus_detect_byte_order` — 字节/字序自动探测（驱动浮点/32 位常见坑）
- `modbus_list_templates` / `modbus_apply_template` — 厂商寄存器模板 → 命名 tag
  （物料搬运模板：`conveyor_vfd` 输送/分拣 VFD 遥测、`agv_battery` AGV/AMR 电池；均 `待核实`）
- `modbus_health_summary` — 寄存器 vs 阈值分类（如驱动温度/电流带）

### OPC-UA（只读；WMS/WCS 网关、线体 SCADA）
- `opcua_server_info` / `opcua_browse` / `opcua_read_node` / `opcua_read_many`
- `opcua_subscribe_sample` `opcua_read_alarms` `opcua_alarm_events`(A&C 带时间戳) `opcua_read_history`(HDA)
- `opcua_diagnose_connection` — 连接失败归因（证书/策略/认证/网络/配置）
- `opcua_discover_tags` — 发现点位并给出启发式语义建议；不是已确认的 `role`，不得据此填写 `tags`；`opcua_health_summary` 阈值分类;
  `opcua_anomaly_scan` 有界统计异常扫描

### MQTT-Sparkplug B（可选；AGV/AMR 车队、IoT 传感/网关的 UNS）
- `sparkplug_node_list` `sparkplug_subscribe_sample` `sparkplug_decode_payload`
- `mqtt_read_topic` `sparkplug_live_schema` `sparkplug_point_draft`
- `mqtt_publish` — **[WRITE][HIGH][MOC]**（默认 dry-run；需具名审批）
- UNS 选点：`iaiops mqtt point-draft --endpoint <name>` 或 MCP `sparkplug_point_draft`
  从有界 BIRTH 捕获提出未确认 refs；`role`/`label` 留空，由现场人员确认，不写配置。
- `uns_browse` `uns_topic_audit` `uns_schema_drift` `uns_live_audit` `uns_live_drift`

### 仓储专属（edition 工具;仅随 warehouse edition 加载,不进全局脑）
- `line_bottleneck` — 产线/物料搬运**瓶颈工位定位**(约束理论 TOC:最低吞吐工位即瓶颈,
  设定整线速率;starved/blocked 佐证——瓶颈上游被 blocked、下游被 starved)。纯分析,
  喂 WMS/WCS/MES/PLC 计数的每工位吞吐或节拍,worst-first,每项引用数值。
- `sortation_health` — 分拣机**读码率/无读/误分拣**分析:按每件分拣记录(是否读到条码、
  应分/实分格口)算三率对标,排出误分拣最多的格口(卡阻/映射错)。纯分析,读 WCS/分拣 PLC 事件。

### 跨协议脑（永远随 server 暴露）
- 诊断：`diagnose_dataflow` `downtime_root_cause` `downtime_root_cause_live` `downtime_triage`
  `learn_cause_weights` `rca_corpus_from_maintenance` `historian_health` `alarm_bad_actors` `tag_health`
  `subscription_health` `heartbeat_health` `alarm_flood_analysis` `alarm_cascade`
  `alarm_rationalization_worksheet`
- 预测维护：`pdm_forecast` —— 输送带电机轴承/温升、分拣驱动、AGV 电池的趋势 + 到限时间
  （早于 `baseline_check` 的越带告警;喂 `conveyor_vfd`/`agv_battery` 模板读出的温度/电流）
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

1. **Doctor-first**：`protocols_supported` → `iaiops doctor` → EtherNet/IP 先
   `eip_controller_info`,OPC-UA 先 `opcua_diagnose_connection`。
2. **输送带 PdM**：`modbus_apply_template`(`conveyor_vfd`) 读 drive_temperature /
   motor_current 序列 → `pdm_forecast(warn_high=...)` 估到限时间 → `imminent/degrading`
   即提前派维护。AGV 车队同理用 `agv_battery` 模板 + `pdm_forecast` 盯 SOC/温度衰减。
3. **停机分诊**：分拣线停机 = `downtime_triage`(告警 cascade + RCA + PdM 前兆一次给出),
   或 `downtime_root_cause_live` 现采证据链;吞吐掉速用 OEE/`oee_multidim` 定位瓶颈工位。
4. **MOC 写**：本 edition **读优先**;EtherNet/IP `eip_write_tag`、Profinet `profinet_dcp_set`、`mqtt_publish`
   为写工具,统一走 MOC:`risk=HIGH` + 默认 `dry_run=True` + 改前值 undo + `iaiops approve`
   具名审批双确认。未经授权绝不写生产控制系统。

## 支持版本矩阵（内部 HLD §8，设计文档不随本仓发布;`待核实` 不得当既成事实）

| 协议 | 库(pin) | 规范/版本 | 覆盖 | 传输 | 自测 |
|---|---|---|---|---|---|
| EtherNet/IP | `pycomm3>=1.2,<2`（extra） | CIP / EtherNet/IP；Logix tag + PCCC 数据表 | AB/Rockwell ControlLogix/CompactLogix + PLC-5/SLC-500/MicroLogix（PCCC）+ Micro800（`plctype` 选） | TCP/44818 | ⚠️ mock（含 SLCDriver）；真 PLC 待核实 |
| Profinet | `pnio-dcp>=1.1,<3`（extra） | PN-DCP（发现/命名） | 现场 IO 设备/station | Ethernet(raw)/UDP | ⚠️ 发现层自测;真设备 待核实 |
| Modbus-TCP | `pymodbus>=3.5,<4` | App 1.1b3；FC 1/2/3/4/5/6/15/16 | VFD/能耗表/AGV BMS/任意从站 | TCP/502 | ✅ |
| Modbus-RTU | `pymodbus>=3.5,<4` + `pyserial>=3.5` | Modbus serial (RTU) | 串口从站/表计 | RS-485/serial | ✅ socat PTY;物理 RS-485 待核实 |
| OPC-UA | `asyncua>=2.0,<3` | OPC UA 1.0x（DA+HA+AC 子集） | WMS/WCS 网关 / SCADA | opc.tcp | ✅ mock+HDA |
| MQTT-Sparkplug B | `paho-mqtt>=2.0,<3`（extra） | Sparkplug B 3.0 | AGV/AMR / IoT 网关 UNS | MQTT/1883/8883 | ✅ broker mock |

## 文件路径限制（0.31.0 起）

MCP 里**读**主机文件的工具（`plc_program_*`、`device_advisory_check`、`db=` 覆盖等）只读 `$IAIOPS_HOME`、配置目录和运维方在 `IAIOPS_AGENT_READ_DIRS` 列出的目录；**写**文件的工具（`export_data`、`compliance_report`、`compliance_evidence_bundle`、`alarm_rationalization_worksheet`）只写 `$IAIOPS_HOME/exports` 和 `IAIOPS_AGENT_WRITE_DIRS`。超出就拒绝——把文件放进这些目录，或让运维方在 shell 里跑 `iaiops` 命令（CLI 不受限）。
