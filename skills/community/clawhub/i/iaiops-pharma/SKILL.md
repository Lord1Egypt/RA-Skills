---
name: iaiops-pharma
description: >-
  Pharmaceutical-manufacturing edition of iaiops — GMP drug/biologics plants as a
  distinct vertical from generic buildings and municipal water. BACnet/IP BMS+EMS
  (cleanroom pressure cascade, temperature/RH), Modbus (PW/WFI skids, stills, EDI,
  analysers), HART-IP (conductivity / TOC / level transmitters), OPC-UA (DCS,
  bioreactors, plant SCADA), plus the cross-protocol brain. Three signature checks:
  cleanroom_pressure_cascade (EU GMP Annex 1 cascade, door by door),
  cleanroom_particle_check and pharma_water_check (USP 645 stage-1 procedure).
  Use when the task mentions pharma, 制药, 药厂, GMP, cleanroom / 洁净室 / 洁净区,
  Annex 1, 压差梯度, pressure cascade, grade A/B/C/D, 尘埃粒子 / particle count,
  EMS / 环境监测, PW / WFI / 纯化水 / 注射用水, TOC, 电导率, conductivity,
  bioreactor / 生物反应器, 冻干机 / lyophilizer, 灌装线 / filling line, CSV, IQ/OQ,
  Annex 11, Part 11, or 数据完整性 / ALCOA. Read-first; BACnet writes are MOC-gated.
---

# iaiops-pharma — 制药 edition（BACnet + Modbus + HART + OPC-UA + 脑）

启动：`IAIOPS_MCP=pharma` / `iaiops-mcp-pharma`（= bacnet + modbus + hart + opcua + 脑；
等价显式写法 `IAIOPS_MCP=bacnet,modbus,hart,opcua`）。BACnet 需 extra：
`pip install iaiops[bacnet]`；HART 需 `pip install iaiops[hart]`。

> **为什么单列 edition，而不是加协议**：制药**没有专用现场协议**。洁净室跑 BACnet，
> 制水跑 Modbus/HART，灌装冻干跑 S7，DCS 跑 OPC-UA —— 全在基座里了。
> 缺的从来是**语义**：`iaiops-water` 的指标是市政口径（DO / ORP / 余氯 / 氨氮 / 浊度），
> 而 PW/WFI 看的是电导率、TOC、回路温度，判法还不一样；iaiops-clinical 的隔离病房压差检查
> 判的是**一个房间**够不够负压（那个工具不在本 edition 的表面上），Annex 1 要的是**级联链**。
> 所以这个 edition 复用同一套协议栈和同一个脑，只叠三个制药语义检查。

> **不内嵌任何药典限值。** 尘埃粒子的 grade/state/size 表、USP <645> stage-1 电导率表、
> TOC 限值 —— 都属于**贵厂在其药典版本下已确认的质量标准**。把一份本仓无人能核的转录数字
> 放进来，最后就是它在决定一批环境算不算合格，而**出错的方向恰恰是好看的那一边**
> （限值抄松了，读起来就是「符合标准」）。所以限值由调用方传入，工具把它引用回来；
> 没给的项报 `no_limit` / `not_graded` 并点名，**绝不跳过、绝不当作通过**。

## 工具

### 制药专属（edition 工具;仅随 pharma edition 加载,不进全局脑）
- `cleanroom_pressure_cascade` — **洁净区压差级联**（EU GMP Annex 1）。不是「这间够不够负压」
  （那是 clinical edition 的隔离房检查），而是**从 A 到 D 这条链成不成立**：每一道跨级别的门
  都必须由洁净侧压向次洁净侧，链条只和最弱的那道门一样强。逐门判
  `correct` / `insufficient` / `reversed` / `unknown`，worst-first，每条引用压差与要求值。
  **相邻关系由人声明**（D25）：房间清单不含拓扑，猜门就是在编造这个检查本身要验的那层关系；
  不给 `doors` 就明说「未评估级联」并给出补法，房间读数照常判。
  `min_cascade_pa` 默认 10.0（Annex 1 指导值 10–15 Pa），**以贵厂确认值为准**。
- `cleanroom_particle_check` — **尘埃粒子**对比**你传入的**限值（`{grade: {state: {size: max}}}`）。
  逐（房间, 粒径）判 `within_limit` / `exceeded` / `no_limit` / `no_reading`，worst-first，
  两个数都引用。缺限值的项**单独计数**，不混进「通过」里。
- `pharma_water_check` — **PW / WFI**。价值在**程序**不在数字，两处最常做反的：
  ① stage-1 用的是**未温度补偿**的读数，且测得温度要**向下**取到表里的档位 ——
  拿变送器 25 °C 补偿输出去比这张表，是常见错误，而且**在回路温度下是往好看的方向错**，
  所以补偿过的读数（以及**没声明**补没补偿的读数）一律拒判并说明理由；
  ② **超出 stage-1 不是不合格**，是转 Stage 2 —— 判词按药典的说法写，不写 FAIL。
  TOC 限值与回路温度带同样由你声明；没声明的报 `not_graded`。

### BACnet/IP（read-first;BMS / EMS / 洁净室压差、温湿度）
- `bacnet_discover` — Who-Is：本地 BACnet/IP 网上的设备
- `bacnet_object_list` — 设备的 object/point 列表
- `bacnet_read_property` — 单对象属性（默认 presentValue）
- `bacnet_read_points` — 所有 analog/binary/multistate 点的 presentValue（压差/温湿度快照）
- `bacnet_cov_subscribe` — 单对象有界 Change-of-Value 捕获
- `bacnet_read_trend_log` — 读设备 TrendLog 缓冲记录
- `bacnet_write_property` — **[WRITE][HIGH][MOC]** 写单对象属性（默认 `dry_run=True` + 双确认）

### Modbus-TCP / Modbus-RTU（只读；多效蒸馏水机、EDI/RO、分配撬、分析仪）
- `modbus_read_holding` `modbus_read_input` `modbus_read_coils` `modbus_read_discrete`
- `modbus_detect_byte_order` — 字节/字序自动探测（分析仪浮点数常见坑）
- `modbus_list_templates` / `modbus_apply_template` — 厂商寄存器模板 → 命名 tag
- `modbus_health_summary` — 寄存器 vs 阈值分类

### HART-IP（只读；电导率 / TOC / 液位 / 流量变送器，经网关，端口 5094）
- `hart_device_identity` — 通用设备身份（command 0）
- `hart_primary_variable` — 主变量 PV
- `hart_dynamic_variables` — PV/SV/TV/QV + 回路电流（command 3）
- `hart_burst_sample` — 主动采样 burst 变量；`hart_burst_listen` — 被动监听（待核实）

### OPC-UA（只读；DCS、生物反应器、层析/超滤、全厂 SCADA、MES 对下）
- `opcua_server_info` / `opcua_browse` / `opcua_read_node` / `opcua_read_many`
- `opcua_subscribe_sample` `opcua_read_alarms` `opcua_alarm_events`(A&C 带时间戳) `opcua_read_history`(HDA)
- `opcua_diagnose_connection` — 连接失败归因（证书/策略/认证/网络/配置）
- `opcua_discover_tags` — 发现点位并给出启发式语义建议；不是已确认的 `role`，不得据此填写 `tags`
- `opcua_health_summary` — tag vs 阈值分类；`opcua_anomaly_scan` — 有界统计异常扫描

### 跨协议脑（永远随 server 暴露）
- 诊断：`diagnose_dataflow` `downtime_root_cause` `downtime_root_cause_live` `downtime_triage`
  `learn_cause_weights` `rca_corpus_from_maintenance` `historian_health` `alarm_bad_actors` `tag_health`
  `subscription_health` `heartbeat_health` `alarm_flood_analysis` `alarm_cascade`
  `alarm_rationalization_worksheet`
- 告警事件聚类：`alarm_event_clusters` — `alarm_bad_actors` 按**来源**排名,回答的是「哪台仪表最吵」,
  不是「哪个故障最吵」;一个把同一条件写成十种说法的厂会得到十个 bad actor。这个按事件**说了什么**分组。
  合并规则是**去掉大小写/标点/数字后的精确相等,不是相似度** —— 故意做笨,所以不需要模型、且可核对;
  每个簇都列出被合并的原文与来源。**它不主张两条措辞不同的告警是同一个故障**,那由人判断。
- 数据质量：`data_quality_scorecard` `data_quality_fleet_rollup`（GMP 重点：电极老化 flatline /
  staleness / 量程外 —— 坏数据绝不静默插值，因为「插出来的数」进不了 GxP 记录）
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

1. **Doctor-first**：`protocols_supported` → `iaiops doctor` → BACnet 先 `bacnet_discover`，
   OPC-UA 先 `opcua_diagnose_connection`，HART 先 `hart_device_identity`。
2. **先勘察，再取数，最后才说明**：`iaiops scan`（只读、端口白名单、零发包预览、自包含 HTML）
   出一份 BACnet/Modbus 设备清单 —— 大多数药厂拿不出一份可信的 OT 资产表，而
   62443-2-1 / NIS2 / 等保都从资产清册开始。然后 `iaiops readiness` 说明**这个站今天能跑哪些场景、
   每个缺口还差什么**。
3. **洁净区**：`bacnet_read_points` 取压差点 → 声明门的相邻关系 → `cleanroom_pressure_cascade`；
   粒子计数配上**你们的**限值 → `cleanroom_particle_check`。EMS 报警泛滥用
   `alarm_flood_analysis` + `alarm_rationalization_worksheet`（一次压差波动刷几百条、
   有用的那条被淹掉，是制药常态）。
4. **制水**：Modbus/HART 取电导率、TOC、回路温度 → `pharma_water_check`，
   记得声明 `temperature_compensated`。
5. **给 CSV / 验证团队**：`verify_determinism`（或 `iaiops verify determinism --out record.json`）——
   固定数据集、断网、两个不同 PYTHONHASHSEED 的全新解释器，输出 SHA-256。
   这是一条能写进 IQ/OQ 的测试用例：「移除模型、重跑标准数据集、比对哈希值一致」。
   拿结论的那一段**故意不让模型碰**，四层之下零模型 import，有守卫测试盯着。
6. **变更控制**：PLC 程序变更 = GMP 变更控制，未记录的变更是数据完整性缺陷。
   `plc_program_snapshot` 记下认可的那一版，`plc_program_drift` 问后来的导出动没动 ——
   注意 `changed_outside_extracted_structure` **不是放行**。
7. **MOC 写**：本 edition 的制药检查**全只读**。`bacnet_write_property` 是唯一的写口，
   `risk=HIGH` + 默认 `dry_run=True` + 改前值 undo + `iaiops approve` 具名审批双确认。
   **洁净区/生命安全相关对象未经授权绝不写。**

## 现在做不到的（说出来比假装支持有用）

| 缺口 | 影响 | 状态 |
|---|---|---|
| 没有 OSIsoft / AVEVA PI 连接器 | 药厂历史库十有八九是 PI，「tap 架在 historian 旁边」这句话在现场落不了地 | ❌ 未做；接入路径有商业/许可门槛，**待核实** |
| S7comm 无真机验证 | 灌装线/冻干机以西门子为主 | ⚠️ `pyS7` 已接入，真机 **待核实**（且 S7 不在本 edition 的默认 profile 里，需显式加 `s7`） |
| BACnet live HVAC / COV / 写路径 | 只读采集没问题，写与 COV 订阅未在真实 BMS 上验证 | ⚠️ **待核实** |
| GxP 对照只覆盖 Annex 11 / Part 11（`compliance_frameworks` 的 `gxp` 列，自 0.27.0） | Annex 22（AI）未做；对照是产品自评，不是验证 | ⚠️ 部分 |
| LIMS / QMS / MES | **不做**，且是有意的：它们走 REST/DB 不走现场协议，且一碰就进 Part 11 电子记录范围 | ⛔ 超出范围 |

## 支持版本矩阵（内部 HLD §8，设计文档不随本仓发布；`待核实` 不得当既成事实）

| 协议 | 库(pin) | 规范/版本 | 覆盖 | 传输 | 自测 |
|---|---|---|---|---|---|
| BACnet/IP | `BAC0>=2023.6,<2026`（其下为 bacpypes3） | BACnet/IP (ASHRAE 135) | BMS/EMS 控制器、压差/温湿度点 | UDP/47808 | ✅ 进程内虚拟设备；live HVAC/COV/写 待核实 |
| Modbus-TCP | `pymodbus>=3.5,<4` | App 1.1b3；FC 1/2/3/4/5/6/15/16 | 制水撬/分析仪/任意 TCP 从站 | TCP/502 | ✅ |
| Modbus-RTU | `pymodbus>=3.5,<4` + `pyserial>=3.5` | Modbus serial (RTU) | 串口从站 | RS-485/serial | ✅ socat PTY；物理 RS-485 待核实 |
| HART-IP | `hart-protocol>=2023.6,<2025`（extra） | HART-IP（经网关） | 电导率/TOC/液位/流量变送器 | UDP/TCP 5094 | ⚠️ codec CI 自测；真机网关 待核实 |
| OPC-UA | `asyncua>=2.0,<3` | OPC UA 1.0x（DA+HA+AC 子集） | DCS / 反应器 / SCADA | opc.tcp | ✅ 进程内 + 证书 Sign/SignAndEncrypt；第三方 server + X509 用户令牌 待核实 |

## 文件路径限制（0.31.0 起）

MCP 里**读**主机文件的工具（`plc_program_*`、`device_advisory_check`、`db=` 覆盖等）只读 `$IAIOPS_HOME`、配置目录和运维方在 `IAIOPS_AGENT_READ_DIRS` 列出的目录；**写**文件的工具（`export_data`、`compliance_report`、`compliance_evidence_bundle`、`alarm_rationalization_worksheet`）只写 `$IAIOPS_HOME/exports` 和 `IAIOPS_AGENT_WRITE_DIRS`。超出就拒绝——把文件放进这些目录，或让运维方在 shell 里跑 `iaiops` 命令（CLI 不受限）。
