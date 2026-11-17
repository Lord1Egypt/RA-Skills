---
name: iaiops-factory
description: >-
  Factory edition of iaiops — discrete-manufacturing lines: OPC-UA, Modbus-TCP/RTU,
  Siemens S7comm (S7-300/400/1200/1500), Mitsubishi MC/MELSEC, Omron FINS
  (CS/CJ/CP/NX), Allen-Bradley
  EtherNet/IP (ControlLogix/CompactLogix), EtherCAT (CoE/SOEM), PROFINET (DCP
  discovery), MTConnect (CNC machine tools), IO-Link (master JSON — sensor-level
  visibility), MQTT/Sparkplug B/UNS, plus the
  cross-protocol brain (downtime root-cause, OEE, asset inventory). Use for PLC,
  CNC, servo/drive bus, name-of-station, tag browse, Unified Namespace, or
  production-line troubleshooting tasks. Read-first, MOC-gated writes. Also covers
  Phoenix Contact PLCnext vPLC (via its built-in OPC-UA + Modbus servers).
---

# iaiops-factory — 离散制造 edition（11 协议 + 脑）

启动：`IAIOPS_MCP=factory` / `iaiops-mcp-factory`。PLCnext vPLC 现场用精简
`IAIOPS_MCP=plcnext` / `iaiops-mcp-plcnext`（= opcua+modbus，走 vPLC 内建服务）。
单协议现场直接 `IAIOPS_MCP=<协议>`。EtherCAT 需 extra：`pip install iaiops[ethercat]`；
PROFINET：`pip install iaiops[profinet]`（或 `iaiops[factory]` bundle）；Omron FINS 客户端为 in-repo 纯 stdlib 实现，无需第三方库。

## 工具

### OPC-UA（只读）
- `opcua_server_info` / `opcua_browse` / `opcua_read_node` / `opcua_read_many`
- `opcua_subscribe_sample` `opcua_read_alarms` `opcua_alarm_events`(A&C 带时间戳) `opcua_read_history`(HDA)
- `opcua_diagnose_connection` — 连接失败五类归因（证书/策略/认证/网络/配置）
- `opcua_discover_tags` — 发现点位并给出启发式语义建议；不是已确认的 `role`，不得据此填写 `tags`
- `opcua_health_summary` — tag vs 阈值分类；`opcua_anomaly_scan` — 有界统计异常扫描

### Modbus-TCP / Modbus-RTU（本 edition 只读）
- `modbus_read_holding`(FC03) `modbus_read_input`(FC04) `modbus_read_coils`(FC01)
  `modbus_read_discrete`(FC02) — 带解码提示
- `modbus_detect_byte_order` — 自动探测寄存器块字节/字序
- `modbus_list_templates` / `modbus_apply_template` — 厂商寄存器模板 → 命名 tag
- `modbus_health_summary` — 寄存器 vs 阈值分类

### Siemens S7comm（pyS7）
- `s7_cpu_info` `s7_read_area` `s7_read_db` `s7_read_many`
- `s7_write_db` — **[WRITE][HIGH][MOC]** 写 DB 单值（默认 off）

### 三菱 MC（3E；Q/L/iQ）
- `mc_cpu_status` `mc_read_words` `mc_read_bits` `mc_read_many`
- `mc_write_words` — **[WRITE][HIGH][MOC]**（默认 off）
- CC-Link 经主站读（零 CC-Link 硬件，见 docs/CCLINK.md）：`mc_cclink_templates`
  `mc_cclink_link_read`（RX/RY/RWr/RWw 刷新映像，模板默认值 `待核实` per 项目）
  `mc_cclink_network_health`（SB/SW 每站链路诊断：classic SW0080–；IE Field
  SB0049 + SW00B0– + SW00A0– baton pass）

### Omron FINS（in-repo stdlib 客户端；CS/CJ/CP/NX-via-FINS）
- `fins_cpu_info`(0501 CPU 型号/版本) `fins_cpu_status`(0601 运行状态/模式/故障字)
- `fins_read_words`(0101; DM/CIO/W/H/A/EM, ≤500 字) `fins_read_bits`
  `fins_read_many`(单会话批量, ≤20 项)
- `fins_write_words` — **[WRITE][HIGH][MOC]**（0102；默认 off）

### Allen-Bradley EtherNet/IP（pycomm3）
- `eip_controller_info` `eip_list_tags` `eip_read_tag` `eip_read_many`
- `eip_write_tag` — **[WRITE][HIGH][MOC]**（默认 off）
- **`plctype` 选驱动**（config key 或工具入参）：`logix`（默认；ControlLogix/CompactLogix/
  GuardLogix 符号 tag）、`slc`（PLC-5/SLC-500/MicroLogix PCCC 数据表：`N7:0` 整数、
  `B3:0/0` 位、`F8:0` 浮点、`T4:0.ACC`/`C5:0.ACC`；`eip_list_tags` 改列数据文件目录）、
  `micro800`（Micro820/850/870 符号变量，仅 IP）。真 PLC-5/SLC/MicroLogix/Micro800 待核实。

### EtherCAT（pysoem/SOEM；**Linux + root/CAP_NET_RAW + 专用网卡 + 真从站**）
- `ethercat_master_state` `ethercat_slaves` `ethercat_slave_info`
- `ethercat_read_sdo`(CoE SDO 上载) `ethercat_read_pdo`(输入过程映像单帧)
- `ethercat_write_sdo` / `ethercat_set_state` — **[WRITE][HIGH][MOC]**
  （AL-state 切换可 START/STOP 运动；默认 off）

### PROFINET（DCP 发现，layer-2 raw socket；不碰 RT 循环数据）
- `profinet_discover`(IdentifyAll) `profinet_identify_station`
  `profinet_station_params` `profinet_asset_inventory`
- `profinet_dcp_set` — **[WRITE][HIGH][MOC]** 重编址 name/IP（可断 IO 关系；默认 off）

### MTConnect（只读；CNC 机床 agent）
- `mtconnect_probe` `mtconnect_current` `mtconnect_sample` `mtconnect_assets`
- `mtconnect_oee_snapshot` — availability/execution/mode/program（OEE 输入）

### IO-Link（只读；主站 JSON 接口 — 传感器级可见性）
- `iolink_master_info` — 主站身份（/deviceinfo：productcode/serial/hw/sw）
- `iolink_ports` — 有界端口扫描（≤32：mode/status + 在线设备身份）
- `iolink_device_info` — 单端口设备身份（vendorid/deviceid/productname/serial/status）
- `iolink_read_pdin` — 过程数据输入（raw hex + 字节数组；按 IODD 解码）
- `iolink_read_isdu` — ISDU 参数读（iolreadacyclic，index/subindex 有界）
- `iolink_scan` — 主站 + 全端口一次性快照
- 配置 `flavor: iotcore`（ifm IoT-Core POST envelope，默认）或 `rest`
  （plain-REST GET，Balluff/Turck 类）；v1 只读，无写工具

### MQTT / Sparkplug B / UNS（含裸 MQTT）
- `mqtt_read_topic` `sparkplug_decode_payload` `sparkplug_subscribe_sample`
  `sparkplug_node_list`
- `uns_browse` `uns_topic_audit` `uns_schema_drift` `uns_live_audit`
  `sparkplug_live_schema` `sparkplug_point_draft` `uns_live_drift`
- UNS 选点：`iaiops mqtt point-draft --endpoint <name>` 或 MCP `sparkplug_point_draft`
  从有界 BIRTH 捕获提出未确认 refs；`role`/`label` 留空，由现场人员确认，不写配置。
- `mqtt_publish` — **[WRITE][HIGH][MOC]**（默认 off）

### 离散制造专属（edition 工具;仅随 factory edition 加载,不进全局脑）
- `changeover_analysis` — **换型/SMED 时长**:换型 = 上个产品末件到下个产品首件的间隔(OEE 可用率
  只汇总、不拆解)。从好件完成流按产品切换测每次换型,排最长、算均值/总换型时间,worst-first,
  每时长引用两端时间戳。纯分析,喂 MES/PLC 好件计数。

### Gateway MES/SCADA 读层（edition 工具；厂商 SCADA/MES 平台 HTTP web API — **只读**）
厂商 SCADA/MES 平台的 **Gateway HTTP/web API** 暴露 MES 侧生产面（模块健康、tag 树、当前值、
活动告警、tag 历史）——这是基座 `opcua` connector 覆盖不到的部分。该平台**同时**跑一个 OPC-UA
server，但那已由 `opcua` connector 处理，本读层**不碰 OPC-UA**。全部**只读**（`risk=low`），
**无任何写工具**——是厂商官方 MCP 模块的受治理/只读补集（差异化在审计/预算/回滚 harness，不在写）。
- `ignition_gateway_status` — 网关/模块健康 + 可达性（Gateway doctor 步；`{gateway, modules[]}`）
- `ignition_tag_browse` — 按 provider/path 浏览 tag 树（`{name, path, type, has_children}`）
- `ignition_tag_read` — 单/多 tag 当前值/质量/时间戳（`{path, value, quality, timestamp}`）
- `ignition_alarm_status` — 活动/已确认告警列表（归一化）
- `ignition_tag_history` — 单 tag 时间窗历史（有界聚合样本 ≤5000）
- API token/key 从加密 secret store 按 key 名取，绝不内联；`flavor`（webdev/gateway：资源路径 +
  字段别名）仅存在于连接器内；确切 API 版本/路径 + live gateway 待核实。

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

1. **Doctor-first**：`protocols_supported` → `iaiops doctor`（或 `opcua_diagnose_connection`
   之类协议自检）→ 再读数。
2. **Read-first**：browse/list → 单点读 → 批量/采样；"没数据"用 `diagnose_dataflow`，
   停机用 `downtime_root_cause_live`（advisory + 证据链）。
3. **MOC 写**：本 edition 的 8 个写工具（s7/mc/fins/eip/ethercat×2/profinet/mqtt）统一
   `risk=HIGH` + 默认 `dry_run=True` + 改前值 undo + `iaiops approve` 具名审批
   双确认。未经授权绝不写生产控制系统。

## 支持版本矩阵（内部 HLD §8，设计文档不随本仓发布；`待核实` 不得当既成事实）

| 协议 | 库(pin) | 规范/版本 | 覆盖 | 传输 | 自测 |
|---|---|---|---|---|---|
| OPC-UA | `asyncua>=2.0,<3` | OPC UA 1.0x（DA+HA+AC 子集） | 任意合规 Server | opc.tcp | ✅ mock+HDA |
| Modbus-TCP | `pymodbus>=3.5,<4` | App 1.1b3；FC 1/2/3/4（读）；写 FC05/06/15/16 未实现（read-only）；字节序探测+厂商模板 | 任意 TCP 从站 | TCP/502 | ✅ |
| Modbus-RTU | `pymodbus>=3.5,<4` + `pyserial>=3.5` | Modbus serial (RTU) | 串口从站 | RS-485/serial | ✅ socat PTY 真串口链路 verified 2026-07-02；物理 RS-485 待核实 |
| S7comm | `pyS7>=2.8,<3` | ISO-on-TCP (RFC1006) | S7-300/400/1200/1500（后者需开 PUT/GET、关 optimized DB） | TCP/102 | ✅ |
| 三菱 MC | `pymcprotocol>=0.3,<1` | MC/SLMP 3E（1E 待核实） | Q/L/QnA/iQ-R/iQ-L | TCP/UDP | ✅ |
| Omron FINS | in-repo stdlib client（无第三方 pin） | FINS per Omron W227/W342（0101/0102/0501/0601 子集；CS/CJ-mode 区码） | CS/CJ/CP/NX(NJ via FINS) 家族（厂内覆盖 待核实） | UDP 9600（默认）+ FINS/TCP | ✅ in-repo mock responder 验证（tests/test_fins.py）；live PLC 待核实 |
| EtherNet/IP | `pycomm3>=1.2,<2` | EtherNet/IP+CIP：Logix tag + PCCC 数据表 | AB Logix（ControlLogix/CompactLogix/GuardLogix）+ PLC-5/SLC-500/MicroLogix（PCCC）+ Micro800（`plctype` 选） | TCP/44818 | ✅ mock（Logix + SLCDriver）；真 PLC-5/SLC/MicroLogix/Micro800 待核实 |
| EtherCAT | `pysoem>=1.1,<2`（extra） | EtherCAT；CoE SDO/PDO | SOEM 兼容主从 | Linux+root+真从站 | ⚠️ 无软仿真；真机 待核实 |
| PROFINET | `pnio-dcp>=1.1,<3`（extra） | DCP 发现/诊断，**不碰 RT 循环** | 西门子系 PN 站 | L2 raw socket | ✅ mock；真机 待核实 |
| MTConnect | `requests>=2.31,<3` | MTConnect 1.x | CNC/机床（agent） | HTTP REST | ✅ 静态XML |
| IO-Link | `requests>=2.31,<3`（复用 MTConnect pin） | IO-Link Master JSON Integration（IOLINK-JSON）；ifm IoT-Core / plain-REST 双 flavor | 带 JSON/REST 接口的主站（ifm/Balluff/Turck 类） | HTTP REST/JSON | ✅ mock 主站（双 flavor）；live master 待核实 |
| MQTT/Sparkplug B | `paho-mqtt>=2.0,<3` + `protobuf>=4.25,<8` | MQTT 3.1.1/5；SpB(Tahu)；亦支持裸 MQTT | SpB 边缘/Broker；UNS | TCP/1883/8883 | ✅ |
| PLCnext vPLC | 复用 OPC-UA/Modbus pin | 菲尼克斯 PLCnext 内建 OPC-UA(4840)+Modbus-TCP | Phoenix Contact vPLC | opc.tcp+TCP/502 | ✅ 路由验证（`tests/test_plcnext_route.py`）；活体 待核实 |
| Gateway MES/SCADA 读层: WebDev | `requests>=2.31,<3`（复用 MTConnect pin，无新 HTTP 依赖） | Gateway HTTP web API（WebDev 模块 JSON 端点：`/system/webdev/...` — status·tags/browse·tags/read·alarms·tags/history）；**只读**，不碰平台 OPC-UA server（由 opcua connector 覆盖）；确切 API 版本/路径 待核实 | 平台 Gateway 聚合的 provider tag / 告警 / 历史 | HTTPS + token/API-key | ✅ mock 网关（in-repo，双 flavor）；live gateway + 确切 API 版本/路径 待核实 |
| Gateway MES/SCADA 读层: Gateway | `requests>=2.31,<3`（复用 MTConnect pin，无新 HTTP 依赖） | Gateway HTTP web API（内建状态/系统函数 REST：`/data/status`·`/data/tags`·`/data/alarms` 布局）；**只读**，JSON 建模，确切路径树 待核实 | 平台 Gateway 状态/模块/tag/告警/历史 | HTTPS + token/API-key | ✅ mock 网关（in-repo，双 flavor）；live gateway + 确切 API 版本/路径 待核实 |

## 文件路径限制（0.31.0 起）

MCP 里**读**主机文件的工具（`plc_program_*`、`device_advisory_check`、`db=` 覆盖等）只读 `$IAIOPS_HOME`、配置目录和运维方在 `IAIOPS_AGENT_READ_DIRS` 列出的目录；**写**文件的工具（`export_data`、`compliance_report`、`compliance_evidence_bundle`、`alarm_rationalization_worksheet`）只写 `$IAIOPS_HOME/exports` 和 `IAIOPS_AGENT_WRITE_DIRS`。超出就拒绝——把文件放进这些目录，或让运维方在 shell 里跑 `iaiops` 命令（CLI 不受限）。
