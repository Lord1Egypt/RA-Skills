---
name: iaiops
description: >-
  Route industrial/OT data-tap and troubleshooting tasks to the appropriate
  iaiops edition and governed MCP profile. Use for PLC/SCADA/CNC/RTU/IED,
  OPC-UA, Modbus, S7, MC, FINS, EtherNet/IP, EtherCAT, PROFINET, SECS/GEM,
  MTConnect, MQTT/Sparkplug, BACnet, HART, IO-Link and serial sensors; also
  factory, fab, process, building, water, pharma, clinical, warehouse,
  renewables and PLCnext work involving OEE, downtime, asset inventory or
  data quality. Read-first; device writes require MOC and are refused for
  safety: sis endpoints. Excludes IT/network gear, Kubernetes, hypervisors
  and backups.
---

# iaiops — ROUTER（识别现场 → 派发 edition skill + MCP profile）

这是**路由 skill**，本身不含工具表。识别任务的行业/协议 → 转到对应 **edition skill**
（工具清单、workflow、支持版本矩阵都在那边），并用对应 profile 启动 MCP（`IAIOPS_MCP=<x>`
环境变量，或等价 sugar 脚本 `iaiops-mcp-<x>`）。现场只暴露 1-2 个协议 + 跨协议脑，
单会话工具 ~15-30，模型不被淹。

## 路由表（关键词 → edition skill → MCP profile）

| 任务提到 | edition skill | MCP profile / entrypoint |
|---|---|---|
| SECS/GEM · SECS-II · HSMS · 半导体/显示 fab · wafer · panel · MES equipment · SVID/ECID · recipe | **iaiops-fab** | `IAIOPS_MCP=fab` / `iaiops-mcp-fab` |
| 离散制造产线 · PLC（S7/S7-1200/1500 · 三菱/MELSEC · Allen-Bradley/ControlLogix/CompactLogix · Omron/FINS/SYSMAC CS/CJ/CP/NX）· Modbus · EtherCAT/CoE/SOEM · PROFINET/DCP · MTConnect/CNC 机床 · Sparkplug B/UNS | **iaiops-factory** | `IAIOPS_MCP=factory` / `iaiops-mcp-factory` |
| 流程工业（化工/食品饮料/原料药合成）· HART/HART-IP · 变送器/阀门定位器 · 过程仪表 · DCS 旁路读取 | **iaiops-process** | `IAIOPS_MCP=process` / `iaiops-mcp-process`（有 UNS 时 `IAIOPS_MCP=process,sparkplug`） |
| BACnet/BACnet-IP · HVAC/暖通 · BMS/楼宇自控 · 厂务/facility · Who-Is · TrendLog · 供应商半小时电表数据/half-hourly (HH)/MPAN · 基础负荷/非营业时段用电/电价时段 | **iaiops-building** | `IAIOPS_MCP=building` / `iaiops-mcp-building` |
| 水处理/水厂 · pH · 浊度/turbidity · 电导率/conductivity · 加药/dosing · 泵站/pump station · 曝气 | **iaiops-water** | `IAIOPS_MCP=water` / `iaiops-mcp-water` |
| 仓储/物流中心 · 输送线/conveyor · 分拣/sorter · AGV/AMR · WMS/WCS · 托盘/穿梭车 · 物料搬运 | **iaiops-warehouse** | `IAIOPS_MCP=warehouse` / `iaiops-mcp-warehouse` |
| 医院设施/clinical facility · 负压/正压隔离病房 · 医用气体 · 手术室环境 · 医疗 BMS | **iaiops-clinical** | `IAIOPS_MCP=clinical` / `iaiops-mcp-clinical` |
| 制药/药厂 · GMP · 洁净室/洁净区 · Annex 1 · 压差梯度/pressure cascade · grade A/B/C/D · 尘埃粒子 · EMS/环境监测 · PW/WFI/纯化水/注射用水 · TOC · 生物反应器 · 冻干机 · 灌装线 · CSV/IQ/OQ · Annex 11 · Part 11 · 数据完整性/ALCOA | **iaiops-pharma** | `IAIOPS_MCP=pharma` / `iaiops-mcp-pharma` |
| 光伏/PV · 逆变器/inverter · 组串/string · 风电/风机 · 场站 SCADA · 新能源电站 | **iaiops-renewables** | `IAIOPS_MCP=renewables` / `iaiops-mcp-renewables` |
| Phoenix Contact PLCnext / vPLC（虚拟化 PLC，走内建 OPC-UA + Modbus-TCP） | **iaiops-plcnext** | `IAIOPS_MCP=plcnext` / `iaiops-mcp-plcnext` |
| 接一个传感器 · 传感器描述/profile · IODD 导入 · 读不懂寄存器/单位/字序 · 哨兵值 · Modbus RTU 仪表（RS-485/RS-232） · 串口 ASCII（称重仪表 / 气体分析仪 / 扫码枪）· 串口服务器 · 4–20 mA 经采集模块 · ESP32 传感节点 | **iaiops-sensor** | `IAIOPS_MCP=sensor` / `iaiops-mcp-sensor` |
| IO-Link · IO-Link master · 智能传感器/executor 参数 · pdin · ISDU（主站 JSON/REST 接口，只读；接入并解码一个传感器、导入 IODD → **iaiops-sensor**） | **iaiops-factory**（楼宇传感器场景 **iaiops-building**） | `IAIOPS_MCP=factory` / 单协议 `IAIOPS_MCP=iolink` / `iaiops-mcp-iolink` |

- 单协议深用（只有一种设备）：直接 `IAIOPS_MCP=opcua`（或 modbus/s7/mc/fins/eip/mtconnect/
  sparkplug/ethercat/secsgem/profinet/bacnet/hart），等价脚本 `iaiops-mcp-<协议>`。
- 跨行业只问 OEE/停机根因/资产盘点/数据质量：任一 profile 均可 —— 跨协议脑
  （诊断/OEE/资产/合规）**默认随 server 暴露**，选覆盖现场协议的 profile 即可；
  纯脑场景可用 `IAIOPS_MCP=brain` / `iaiops-mcp-brain`（只暴露脑，零协议）。
- 说不清行业但报了协议名：按协议列选含它的最小 profile；都不沾 → `iaiops doctor` +
  `protocols_supported` 先看现场配置了什么。

## 部署（0.10.0 起：无默认，必须选菜单）

- **裸启动 `iaiops-mcp`（不设 `IAIOPS_MCP`）不再暴露全部工具**：打印选择菜单到
  stderr 并 exit 2。必须设 `IAIOPS_MCP=<selection>` 或用预置入口 `iaiops-mcp-<name>`。
  `IAIOPS_MCP=menu` 显式打印同一菜单（带各 selection 工具数）后退出。
- `IAIOPS_MCP=all` 仍可**显式**使用（power user；>100 工具时启动日志给洪泛警告）。
- **多进程站点（1 脑 + N 协议）**：跑一个 `iaiops-mcp-brain`（只脑），协议 server 各自
  加 `IAIOPS_MCP_NO_BRAIN=1`（如 `IAIOPS_MCP_NO_BRAIN=1 iaiops-mcp-opcua`）去掉脑，
  避免跨 server 工具重名；`protocols_supported`（发现工具）在 NO_BRAIN 下仍然保留。

## Energy 协议 → 另一个包（不在本 server）

IEC 60870-5-104 / IEC-104、DNP3 / outstation、IEC 61850 / MMS / IED、变电站/
substation、电力/能源/utility SCADA → 用独立的 **iaiops-energy**
（`pip install iaiops-energy`，然后 `iaiops-energy-mcp`；
github.com/industrial-aiops/industrial-aiops-energy）。它复用本包的 core + 脑；
monitor-direction only。**不要**尝试用本 server 的 profile 覆盖能源协议。

## 安全不变量（所有 edition 一致，路由前先记住）

- **Read-first**：默认只读；先 `protocols_supported` 看能力、`iaiops doctor`
  验链路，再谈读，最后才谈写。
- **写 = MOC（Management-of-Change）**：The 10 write tools（`s7_write_db`、
  `mc_write_words`、`fins_write_words`、`mqtt_publish`、`eip_write_tag`、`ethercat_write_sdo`、
  `ethercat_set_state`、`profinet_dcp_set`、`bacnet_write_property`、`bas_command`）全部
  `risk=HIGH`、默认 `dry_run=True`、捕获改前值供 undo（`bas_command` 另对生命安全点一律拒绝）。
  这 10 个是**设备**写。写历史库/时序库那类不改变现场状态的写另计，
  由 edition skill 逐个列明 —— 别把「10」当成全部写面。
- **审批**：真实写入需具名审批人 —— CLI `iaiops approve` 双重确认后才放行。
- **SIS 禁写**：端点标 `safety: sis` 后，所有设备写连 dry-run 预览都拒绝；审批不能覆盖此边界。
- **未经授权绝不写生产控制系统**；AI 结论仅 advisory，引用真实信号出处，宁可
  `insufficient_evidence` 不臆测。
- 各协议的验证状态（✅ 已自测 / 待核实）见 edition skill 的支持版本矩阵，
  标 `待核实` 的不得当既成事实。

## 先回答「这个站能干什么」，再谈干（0.24.0）

路由到 edition **之前**，这两条不分行业、任何现场都先跑，而且**零联网**：

- **先分路线**：`iaiops onboard status` 从 `config.yaml` 推导这个站在哪条路上 ——
  **设备直读**（还没有 UNS，或正在建）或 **已在 UNS broker 上**（接入 → 命名空间体检 →
  选点 → 语义 → 采集 → 提问，**不扫描**：扫描永远识别不出 MQTT）。UNS 路线再按**已存的**
  `uns-live-audit` 结论分 **B1**（干净）与 **B2**（治理本身就是工作）；没有体检记录时它说
  「B1/B2 未知」，**agent 不许替它判断**。什么都没配或两种端点都有时，它给出两个选项且一个都
  不选 —— 把两个都转述给用户，不要替用户挑。
- 设备路线（`--track devices`）——「这个站走到六步里的哪一步、**下一条命令是什么**」。
  六步（勘察 → 端点入 config → 每个端点的点表 → 点表**语义** → 采集 → 提问）一直都在，
  但从来没有东西说过顺序。每次都从本地库和 `config.yaml` 现推，**没有状态文件会过期**：
  手改过 config.yaml、恢复过备份，答案照样是真的。给人**一条**命令，给五条等于没给。
- `iaiops onboard draft` —— 把已存的 scan 变成 `config.yaml` 端点草稿，**不写 config.yaml**
  （和 `tags apply` 一样，人来合并）。只有**已确认**的协议才成为端点：端口开着只说明有人在听，
  不等于它说这个协议。每个值都写明扫描观测到了什么（S7 实际应答的 slot、MELSEC 自报的
  `plctype`、OPC-UA 是否有无加密端点/是否要凭据）；**扫描定不下来的字段以注释形式输出**并说明
  在等什么 —— 不是省略，省略等于让协议默认值悄悄生效（Modbus 网关按 unit 1 读，读的是另一台机器）。
  `tags:` 恒为空。**草稿里 `value: null` 的字段，agent 不许代填，也不许删掉它的 `caution`。**
- `iaiops readiness` ——「这个站点今天能跑哪些场景、每个缺口还差什么」，
  按「补上它能解锁多少」排序。它**只报告，绝不代填**。
- `iaiops investigate plan` ——「真出事时能走到那八步里的第几步」。缺口分两种，别混：
  **你还没供**（会直接给出该跑的命令）与 **产品供不了**（标 `not_yet_expressible`）。
  这两个把人送去完全不同的地方。

对一个**已经过去的**窗口逐步走完并留档：`iaiops investigate open|show|list`。
不碰设备 —— 窗口已经过去，证据就是当时采到的。三条都能 `--report x.html`
出可转发的自包含文件。

两步需要**人先声明**，agent 不许代答：

- `iaiops relations declare` —— 产线上下游。D25：线上下游共现是必然，
  从时间推不出因果，所以只能声明。
- `iaiops knowledge mount` —— ISO 14224 故障机理库，**可排除、绝不确认**；
  库里没有这条原因返回 `nothing_known`，**那不是「无异议」**。

**点表语义（`role:`）只能人给** —— 哪个位号是产量计数器是工艺知识，猜错会得出一个
看着合理的 OEE，比报错更糟（D16）。输入口是 `iaiops tags export|apply|page`：
导出的 `role` 列是**空的**，哪怕紧挨着一个叫 `GoodPartsCounter` 的位号。
**这一层故意没有 MCP 工具 —— 让 agent 填 role 列正是 D16 禁止的那个猜测。**
遇到它，把表交给现场的人，不要自己填。

UNS 选点可用 `iaiops mqtt point-draft --endpoint <name>`（对应 MCP 入口见
edition skill）从有界 Sparkplug BIRTH 捕获生成**未确认**点位草稿；
`role`、`label` 留空，由现场人员确认，命令不写配置。短时捕获不代表点位全集。

CLI 与 MCP 是否都有入口以对应 edition skill 的工具表为准；本 skill 只负责路由。

## Setup（各 edition 相同）

`iaiops init` 交互写 `~/.iaiops/config.yaml`；凭据进加密存储
（`~/.iaiops/secrets.enc`，主密码 `IAIOPS_MASTER_PASSWORD`）。`iaiops doctor`
逐端点探活。协议参数、模拟器自测、MCP JSON 示例见 README 与各 edition skill。
