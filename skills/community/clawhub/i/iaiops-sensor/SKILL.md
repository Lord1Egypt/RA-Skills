---
name: iaiops-sensor
description: >-
  Sensor edition of iaiops — connect one industrial sensor and read it correctly:
  draft a sensor profile from a vendor IODD, check it, read one channel once with
  its unit, accuracy band and verification level, then collect. Covers sensors on
  Modbus RTU/TCP (RS-485 / RS-232 / RS-422 / USB serial, 4–20 mA via I/O modules),
  IO-Link masters (JSON interface) and MQTT/Sparkplug nodes. Use when the task
  mentions a sensor, sensor profile, IODD, IO-Link device, process data / pdin,
  decoding registers into engineering units, float32 word order, sentinel /
  no-target values, Modbus RTU instruments (RS-485 / RS-232), or "接一个传感器 / 传感器描述 /
  读不懂寄存器 / 单位". The sensor tools are read-only and never write config; the
  server also exposes mqtt_publish (HIGH, MOC-gated) via the MQTT/Sparkplug set.
---

# iaiops-sensor — 传感器 edition（Modbus + IO-Link + MQTT/Sparkplug + 传感器工具 + 脑）

启动：`IAIOPS_MCP=sensor` / `iaiops-mcp-sensor`（= modbus + iolink + sparkplug + serial + 传感器工具 + 脑）。
安装：`pip install iaiops[sensor]`（一次拉齐 Modbus / IO-Link / MQTT 依赖）。
设计依据：HLD §16（连得上 / 读得懂 / 采得准）、§17（入口与描述库）。

## 接一个传感器：固定路径

1. **认出设备**：IO-Link 用 `iolink_ports` / `iolink_device_info` 看端口上的 vendor/device id；
   Modbus 设备没有可核对的数字身份 —— 型号由人确认。
2. **拿到描述（profile）**：先查描述库 `sensor_profile_list`（有就 `sensor_profile_show` 取文本，CLI 可
   `iaiops sensor show <id> --out <文件>` 复制一份）；IO-Link 有 IODD 时用 `sensor_import_iodd` 起草（**返回文本、不写盘**）。
   草稿一律 `verified: 待核实`，IODD 单位代码原样保留 —— 让人把单位改成真实单位。
   Modbus 传感器按规格书写描述（寄存器表、类型、字序、比例、量程、哨兵值）。
3. **检查**：`sensor_profile_check` —— 字段错一个就拒绝并指出是哪个。
4. **绑定（只能由人做）**：Modbus 端点写 `sensor_profile: <文件>`，点位写 `ch:<通道名>`；
   IO-Link 主站写 `port_profiles: {<端口>: <文件>}`，点位写 `port<N>/<通道名>`。
   **不要替用户改 config.yaml**（D51）：把要加的几行给用户，由人贴进去。
5. **试读一次**：`sensor_read_channel` —— 分开报告 `reachable` / `decodable`（设备回了错误码，
   比如寄存器地址写错，算「连得上、读不懂」，不是掉线），读得懂时给出
   值、单位、精度带、描述的核实等级。`untyped: true` 表示裸地址点，按 uint16 读，提醒补类型。
6. **看就绪度**：`site_readiness` —— 「持续采集」下列出未声明类型的点、读不了的点（含原因）、
   仍是 `待核实` 的描述、以及没有单位入库的通道。
7. **采集**：CLI `iaiops collect run <endpoint>`。哨兵 / NaN / 超量程 / 设备不符 / 过程数据长度不符
   都记为**盲区并带原因**，不当读数。

## 工具

### 传感器（只读，edition 模块）
- `sensor_import_iodd` — IODD → 草稿描述文本 + 「未导入」清单；不写盘、不改 config
- `sensor_profile_check` — 校验描述，列出通道 / 布局 / 单位 / 精度带 / 核实等级
- 上面两个只读 `$IAIOPS_HOME`、配置目录或运维方在 `IAIOPS_AGENT_READ_DIRS` 列出的目录下的文件，别处的路径不打开就拒绝 —— 把文件拷进去，或让人在 shell 里跑
  `iaiops sensor import-iodd | check`（CLI 读任何路径）
- `sensor_read_channel` — 读一个点一次，三级分开报告；读不了的点在联系设备之前就拒绝
- `sensor_profile_list` / `sensor_profile_show` — 查随包的描述库（电表、光伏逆变器等，默认 `待核实`）；
  IO-Link 可按 vendor/device id 过滤 —— **只是建议**，同一设备号可能有多种过程数据布局

### Modbus（只读；RTU 走 RS-485 / RS-232 / USB 串口，TCP 走网口）
- `modbus_read_holding` `modbus_read_input` `modbus_read_coils` `modbus_read_discrete`
- `modbus_detect_byte_order` — float32 / 32 位字序不确定时先探测，**描述里必须写明字序**
- `modbus_health_summary` — 支持带类型的点（`ir:0:float32:CDAB`）；`ch:` 通道尚不支持（会返回 unknown）

### 串口 ASCII（只读）
- `serial_sniff` — 听一段时间、返回原始行（latin-1 显示每个字节）；**什么都不发**；独占打开，端口被占用就拒绝

### IO-Link（只读；主站 JSON 接口）
- `iolink_master_info` `iolink_ports` `iolink_device_info` `iolink_read_pdin` `iolink_read_isdu` `iolink_scan`

### MQTT / Sparkplug（改造用传感节点，如 ESP32）
- `sparkplug_node_list` `sparkplug_subscribe_sample` `mqtt_read_topic` `uns_browse` `sparkplug_point_draft`
- 采集要求端点写 `stale_after_s`（停发和读数不变在线上分不出来）
- UNS 选点：`iaiops mqtt point-draft --endpoint <name>` 或 MCP `sparkplug_point_draft`
  从有界 BIRTH 捕获提出未确认 refs；`role`/`label` 留空，由现场人员确认，不写配置。
- ⚠️ `mqtt_publish` —— 本菜单里**唯一的设备写**：`[WRITE][risk=HIGH][MOC]`，默认 dry-run，
  需要审批；接传感器用不到它，别为「试一下」去发布

### 跨协议脑（随 server 暴露）
- `site_readiness` `diagnose_dataflow` `data_quality_scorecard`

## 支持版本

| 路径 | 库 pin | 规范 / 覆盖 | 传输 | 自测 |
|---|---|---|---|---|
| Modbus RTU / TCP | `pymodbus>=3.5,<4`、`pyserial>=3.5` | Modbus Application Protocol；FC01–FC04；16/32 位与 float32 全部字序 | RS-485 / RS-232 / RS-422 / USB 串口；TCP | 进程内假客户端；实验机局域网上对**自建** Modbus 模拟器走查（验证阶梯 2b，非第三方设备；float32 CDAB、NaN、超量程） |
| IO-Link 主站 | `requests>=2.31,<3` | IO-Link 1.1 过程数据 + IODD 位偏移约定；ifm IoT-Core JSON（`待核实`：只对模拟主站验证过；其他厂商路径同样 `待核实`） | HTTP | 进程内模拟主站；实验机局域网上对**自建**模拟主站走查（验证阶梯 2c：两端都是我们的；哨兵、换传感器、PD 长度） |
| 串口 ASCII | `pyserial>=3.5` | 按描述逐份 `待核实`（行尾 / 编码 / 正则 / 状态码） | RS-232 / RS-485 / RS-422 / USB 串口；串口服务器原始 TCP | pty 对（真实 pyserial 路径）+ 本机 TCP；实验机局域网上对**自建**称重模拟器走查（验证阶梯 2c：两端都是我们的，非第三方仪表） |
| MQTT / Sparkplug | `paho-mqtt>=2.0,<3`、`protobuf>=4.25,<8` | Sparkplug B；纯 MQTT 只有陈旧判断 | TCP（TLS / 代理认证 `待核实`） | 真实代理录制回放 |

真实 IO-Link 主站的身份字段编码、真实厂商 IODD 仍 `待核实`。

## 点位写法

| 写法 | 含义 |
|---|---|
| `ch:fz` | Modbus 端点描述里的通道 `fz`（带单位、量程、哨兵） |
| `port2/distance` | IO-Link 主站 2 号口描述里的通道 `distance` |
| `ir:0:float32:CDAB` / `hr:12:int16*0.1` | 带类型的 Modbus 点：表 / 地址 / 类型 / 字序 / 比例（**32 位必须写字序**） |
| `di:3:low` / `co:0:high` | 开关量（NPN / PNP / 干接点，接在 DI 模块上）：离散输入 / 线圈 + **必填的有效电平**；值 = 1 动作 / 0 未动作。常闭开关写 `low` |
| `40` | 裸地址：一个保持寄存器按 uint16 读 —— 兼容旧配置，readiness 标「未声明类型」 |

## 串口 ASCII 仪表（称重仪表、气体分析仪、扫码枪、老式测量仪）

接法：本机串口（RS-232 / RS-485 / RS-422 / USB 虚拟串口：`serial_port`、`baudrate`…）或**串口服务器**的原始 TCP
（`host` / `port`）—— 同一份描述通用。端点 `protocol: serial` + `sensor_profile:`，点位写 `ch:<通道名>`。

1. **先看原始行**：`serial_sniff`（CLI `iaiops serial sniff <endpoint>`）—— 只听、**什么都不发**、不需要描述。
2. **写描述**：`framing`（行尾、编码）、`mode: listen`（仪表持续推送）或 `poll` + `query`（只能发这一条）；
   通道 `layout: {pattern: <匹配整行的正则，含 value 组>}`、`status`（ok / invalid 状态码）、`unit` / `unit_from`。
3. **规矩**：
   - 串口**独占**打开；被别的程序占用就拒绝，**绝不抢**（现场称重软件可能正用着它）。
   - `poll` 只发描述里写死的查询，且端点必须声明 `bus: dedicated`；`bus: shared`（RS-485 上已有主站）只能旁听。
     **去皮 / 清零 / 校准不是读，不能写进 query。**
   - `listen` 必须写 `stale_after_s`；超时没有新行 = 没有读数（盲区），不沿用上一条。
   - 不稳定 / 超载状态、没有完全匹配的行、单位与声明不符 —— 一律盲区，不「尽量解析」。
   - 采集要求通道有**固定 `unit`**：只靠每行自带单位的通道，kg 和 g 会混进同一条序列。

## 开关量传感器（NPN / PNP / 干接点）

它们从不直接接电脑：接在 PLC 上就读 PLC 位号；接在 Modbus DI 模块上就用 `di:` / `co:` 点，或在描述里写
`layout: {table: discrete | coil, address: N, active: high | low}`（`signal` 只能是 `level` / `event`）。
**有效电平必须写**：常闭开关在「有工件」时输出 0，猜错会把有和无整个反过来。
**开关量不能当产量计数**：轮询会漏掉短脉冲，`site_readiness` 会在 OEE 下报 `count_source` 缺口 ——
产量要读 DI 模块或 PLC 的计数寄存器。去抖交给模块 / PLC 的输入滤波，tap 不做软件去抖。

## 边界

- **SIS 禁写**：端点 `safety: sis` 拒绝所有设备写（包括 dry-run 预览），已有审批也不能放行；只读仍可用。

- **传感器工具只读**：不写设备、不改 config、不做传感器配置（重新示教、改量程不在本 edition）。
  同一 server 带的 `mqtt_publish` 是受 MOC 约束的写，见上。
- **描述不是背书**：`待核实` 的描述只表示「照资料这样解码」，报告里一直带着这个等级。
- **语义仍由人给**：描述只管「读得懂」，不说哪个通道是产量计数（D16 / D43）。
- 串口 ASCII 仪表见上一节；IO-Link 开关量（SIO）模式与端口读时自动建议描述仍是后续。
