---
name: hifleet-skills
description: >-
  HiFleet 综合技能：船位、档案、事故事件、制裁、海事处罚、轨迹/航程/航次、PSC、区域通航、港口、公开船货盘、港距排序、班轮船期、航线、气象、船队、AIS。Position, track, voyage, casualty, sanction, maritime penalty, PSC, port, public tonnage, liner schedule, fleet, weather, AIS.
version: 0.3.21
# 必选：本技能依赖鉴权，需先配置环境变量后再使用
requiredEnv:
  - HIFLEET_API_KEY
# 来源与联系（便于安全审核）
homepage: https://skills.hifleet.com
source: https://github.com/charleiWang/hifleet-skills
---

# 技能说明

本技能使用时需先配置 `api_key`；技能列表与触发词见 [references/skills_index.md](references/skills_index.md)。

## 安装获取

| 途径 | 地址 |
|------|------|
| ClawHub | https://clawhub.ai/charleiwang/skills/hifleet-skills |
| GitHub | https://github.com/charleiWang/hifleet-skills |
| 手动安装包（zip） | http://static.hifleet.com/download/skills/hifleet-skills-latest.zip |

完整安装步骤见 [INSTALL.md](INSTALL.md)；尚无 `api_key` 时见 [FIRST_SETUP.md](FIRST_SETUP.md)。

| 技能 | 状态 | 说明 |
|------|------|------|
| 船位 Ship Position | ✅ 已实现 | 获取最新船舶位置 |
| 档案 Archive | ✅ 已实现 | 船舶/公司档案 |
| 事故事件 Casualty & Events | ✅ 已实现 | 按 IMO 查事故/事件列表，按 eventId 查详情 |
| 制裁 Sanction | ✅ 已实现 | 按 IMO 评估船舶制裁风险（US/EU/UK/Canada/UN/CN） |
| 海事处罚 Maritime Penalty | ✅ 已实现 | 按船名/MMSI/时间查海事行政处罚公示 |
| 船舶档案统计 Ship Archive Statistics | ✅ 已实现 | 船旗、船型、公司船队等预聚合统计，以及船舶档案明细分页查询 |
| 红海/波斯湾通航 Strait Traffic | ✅ 已实现 | 海峡通航统计（曼德、苏伊士、好望角、霍尔木兹） |
| 区域船舶 Area Traffic | ✅ 已实现 | 查询指定区域内的当前船舶：支持 bbox、areaId（区域清单 id）或 polygon（WKT） |
| PSC 检查 PSC Inspection | ✅ 已实现 | 单船 PSC（按 IMO）→ 统计异常 `openclaw/anomalies*` → 宏观统计 `openclaw/stats/compare|defects/top|mix/compare` |
| 进港指南 Port guide | ✅ 已实现 | 进港指南港口列表/检索（港名或代码）、单港详情 |
| 租船 Charter | ✅ 已实现（内置模块） | 班轮（`hifleet-schedule`）；**公开船货**（`hifleet-opentonnages`） |
| 性能 Performance | 待实现 | 油耗、能效、主机性能 |
| 航程 Voyage | ✅ 已实现（部分） | 历史轨迹、航程、航线规划、历史挂靠、历史航次、上一港、当前停船|
| 航线 Route | 待实现 | 推荐航线、航路点 |
| 航运 Shipping | 待实现 | 运价、市场、新闻 |
| 气象海况 Weather | 待实现 | 风浪、台风、能见度 |
| 船队 Fleet | 待实现 | 多船监控、船队报表 |
| AIS | 待实现 | AIS 报文、轨迹回放 |
| 账户与用量 Account & Usage | ✅ 已实现 | 注册/登录/Key、积分充值/订阅/发票、混合计费额度；已有 Key 可换票打开 Skills 控制台 |

---

## api_key 配置（必填）

船位、档案、PSC、港口等已实现功能依赖 HiFleet API 鉴权：优先读取环境变量 `HIFLEET_API_KEY`，项目/ClawHub 内统一按 `api_key` 传入。

**用户尚无 api_key 时**：按 [FIRST_SETUP.md](FIRST_SETUP.md) 引导 **发验证码 →（按需人机）→ 验证码登录/注册（免密码）→ 配置 Key**；积分或订阅额度不足时引导 **充值/订阅 → 收银台付款 → 开票**，见 [references/account_onboarding_api.md](references/account_onboarding_api.md) 与 [references/billing_api.md](references/billing_api.md)。

## 常用定义

### API 基址（`{base}`）

- 默认：`https://api.hifleet.com`；其它部署设环境变量 **`HIFLEET_API_BASE`**（无末尾 `/`）。
- 下文与各分册接口均写作 **`{base}/路径`**，例如 `{base}/position/getcallport/token`。
- 说明见 [references/api_base.md](references/api_base.md)。

国际航行船舶 : 通常有有效的IMO注册号码的船舶
电子围栏: 区域范围

---

## 已实现功能

### 船位 / Ship Position

获取（岸基+卫星+移动）船舶最新位置信息。支持**关键字（船名或 MMSI）**查询，自动走“先搜船、再查位”的两步流程。

- **触发**：船位、位置、报位、在哪、MMSI、ship position、vessel position
- **输入**：关键字（船名或 MMSI）或直接 9 位 MMSI；`api_key` 从配置读取
- **API 详情**：[references/position_api.md](references/position_api.md)（含 shipSearch 与 position/get/token）
- **脚本**：`scripts/get_position.py`（支持关键字或 MMSI，可选用于命令行/集成）

**两步流程**：

1. **搜船**：用用户关键字调用 `position/shipSearch`（shipname、`api_key`、i18n=zh、count）。
2. **查位**：根据结果数量处理：
   - **0 条**：提示未找到，请检查关键字。
   - **1 条**：直接取该条 `mmsi`，调用 `position/position/get/token` 查位置并展示。
   - **多条**：若可推断用户目标船（如关键字为完整 MMSI 或唯一匹配船名），则用对应 MMSI 查位；否则列出船名/MMSI/船型/船籍等，**请用户选择具体 MMSI**，再按所选 MMSI 调用 `position/position/get/token` 查位置。

若用户已提供 **9 位数字 MMSI**，可直接调用 `position/position/get/token`。

### 档案 / Archive

根据 IMO 或 MMSI 获取船舶档案（基本信息、尺度、舱容、建造、入级、动力、公司信息、互保协会等）。接口支持 **imo 与 mmsi 二选一**；船名需先通过 shipSearch 得到 MMSI/IMO。

- **触发**：档案、船舶信息、船籍、船型、船东、管理公司、archive、vessel profile、ship info
- **输入**：IMO（7 位）或 MMSI（9 位）；`api_key` 从配置读取
- **API 详情**：[references/archive_api.md](references/archive_api.md)
- **脚本**：`scripts/get_archive.py`（支持 IMO 或 MMSI，MMSI 直接传 mmsi 参数，需 `api_key`）

**调用流程**：检查 `api_key` → 按 **IMO** 或 **MMSI** 调用档案接口（内贸船无 IMO 可传 MMSI）→ 解析 data，按 labelZh 分块展示。

### 事故事件 / Casualty & Events

查询船舶事故与海事事件（碰撞、搁浅、火灾等）：先按 **IMO** 取列表，再用列表中的 **eventId** 查详情（描述、位置、船舶、航次、货物、关联事件）。与网站船舶档案页「事故和事件」同源；**勿与** MSA 事故报告、海盗事件混用。

- **触发**：事故、事件、casualty、collision、grounding、海事事故、事故记录、事故详情 / casualty, marine casualty, incident, collision, grounding
- **输入**：列表需 **IMO**（7 位）；仅有船名时先 `shipSearch` 取 IMO；详情需 **eventId**（来自列表）。`api_key` 从配置读取
- **API 详情**：[references/casualty_api.md](references/casualty_api.md)
- **脚本**：`scripts/get_casualty.py list <IMO>`、`scripts/get_casualty.py detail <eventId>`

**调用流程**：检查 `api_key` →（无 IMO 则 shipSearch）→ `GET {base}/casualty/list/token?imo=...&api_key=...` → 展示列表 → 用户选定后 `GET {base}/casualty/detail/token?eventId=...&api_key=...`。无记录时如实说明，勿伪造。

### 制裁 / Sanction

按 **IMO** 评估船舶制裁风险（US SDN → EU → UK → Canada → UN → CN 依次命中），返回风险等级、来源、制裁对象与明细。

- **触发**：制裁、制裁风险、OFAC、SDN、是否被制裁、制裁名单 / sanction, sanction risk, OFAC, SDN, sanctioned vessel
- **输入**：Query 参数名必须是 **`imonumber`**（不是 `imo`）；仅有船名时先 `shipSearch`，取结果里的 IMO 填入 `imonumber`。`api_key` 从配置读取
- **正确接口（仅此）**：`GET/POST {base}/sanction/assess/shiprisk/token?imonumber={imo}&api_key=...`
- **勿调用**：网站路径 `/shipdetail/sanction/...`；勿用 `imo` 参数；勿与海事处罚 `/maritime/penalty/...`、制裁区港口 `/sanctions/port/token` 混淆
- **API 详情**：[references/sanction_api.md](references/sanction_api.md)
- **脚本**：`scripts/get_sanction.py <IMO>`

**调用流程**：检查 `api_key` →（无 IMO 则 shipSearch）→ 调上述 `/token` 接口 → 按 `riskLevel`（字符串 `HIGH_RISK` / `MEDIUM_RISK` / `LOW_RISK`）展示；高风险看 `data`，中风险看 `otherships`。

### 海事处罚 / Maritime Penalty

查询中国海事局**行政处罚**公示（案号、案由、处罚对象、处罚结果等）。数据为爬取入库的公示信息，**不是** PSC 或制裁名单。

- **触发**：海事处罚、行政处罚、海事局处罚、案号、案由 / maritime penalty, administrative penalty, MSA penalty
- **输入**：优先 `shipName`（中文船名/主体名）；可选 `mmsi`、`startTime`/`endTime`、分页。`api_key` 从配置读取
- **API 详情**：[references/maritime_penalty_api.md](references/maritime_penalty_api.md)
- **脚本**：`scripts/get_maritime_penalty.py --ship-name ...`（或 `--mmsi` / 时间范围）

**调用流程**：检查 `api_key` → `GET {base}/maritime/penalty/list/token?shipName=...&api_key=...` → 展示 `list[].details`（案号、案由、处罚结果）。无记录如实说明。

### 船舶档案统计 / Ship Archive Statistics（OpenClaw）

查询船舶档案日批预聚合统计和当前批次的船舶档案明细，可回答特定船旗、船型、公司船队、建造年份、载重吨区间、船厂交付、证书到期或登记国的数量与分布问题；也可按条件分页检索船舶档案。该能力是**批次快照统计**，不是实时 AIS 数据或单船完整档案。

- **触发**：船旗船舶数量、某国船旗统计、船型分布、船队规模、公司有多少船、船龄分布、新造船趋势、载重吨分布、船厂交付、证书到期、船籍登记国、船舶档案统计、船舶档案明细 / ship archive statistics, fleet statistics, flag statistics, ship type distribution, company fleet, newbuild trend, DWT distribution, certificate expiry
- **输入**：统计查询需 `intent`；可选 `statDate`（`yyyy-MM-dd`）或 `batchNo` 以指定统计批次，二者均不传时取最近成功全量批次；可选 `filters`。明细列表额外支持 `page`、`pageSize` 和 IMO、MMSI、船旗、船型、船东、船名关键字等筛选。`api_key` 从配置读取。
- **API 详情**：[references/ship_archive_stats_api.md](references/ship_archive_stats_api.md)

**Agent 路由**：用户问“某船”本身的详细档案时，优先使用上方 **档案 / Archive**；用户问“多少艘、分布、趋势、排行、某公司船队规模”等聚合问题时使用本能力的 `/query`。用户需要满足条件的船舶逐条结果时使用 `/list`。调用前如需要确认数据批次或数据更新时间，先调用 `/meta`；不要把不同批次的结果混在一起比较。

### 航程 / Voyage（OpenClaw）

查询单船历史轨迹、挂靠、航次、上一离港及当前停船信息。**均需 `api_key`**；用户仅给船名/关键字时，先走 `position/shipSearch` 取得 MMSI（规则同船位技能）。

- **API 详情**：[references/voyage_api.md](references/voyage_api.md)

| 能力 | 接口 | 计费 |
|------|------|------|
| 历史轨迹（压缩） | `GET/POST {base}/position/trajectory/token` | 按轨迹点数阶梯（每 100 点 1 点，最低 2 点） |
| 历史轨迹（未压缩） | `GET/POST {base}/position/trajectory/nocompressed/token` | 按轨迹点数阶梯（每 100 点 1 点，最低 2 点） |
| 历史挂靠 | `GET/POST {base}/position/getcallport/token` | 按挂靠条数阶梯（每 20 条 1 点，最低 2 点） |
| 历史航次（简版） | `GET/POST {base}/position/getvoyagelist/token` | 按航次条数阶梯（每 20 条 1 点，最低 2 点） |
| 历史航次（详版） | `GET/POST {base}/portofcall/getvoyages` | 按航次条数阶梯（每 20 条 1 点，最低 2 点） |
| 上一港 | `GET/POST {base}/position/lastdeparture/token` | 固定计费（FIXED） |
| 当前停船 | `GET/POST {base}/position/getstop/token` | 固定计费（FIXED） |

#### 历史轨迹 / Track history

按 MMSI 与时间区间查询 AIS 历史轨迹点（与挂靠/航次不同，返回**点序列**）。

- **触发**：历史轨迹、轨迹回放、某时段走了哪、航行路线、track history、trajectory、AIS track
- **输入**：`mmsi`（必选）；`starttime`、`endtime`（必选，北京时间）；可选 `bbox`（`左经,下纬,右经,上纬`，仅 `zoom≥8` 时过滤）、`zoom`（默认 `7`，最大 `16`）
- **接口**：`GET/POST {base}/position/trajectory/token?mmsi={mmsi}&starttime={start}&endtime={end}&api_key=...`
- **时间窗**：压缩版约 **3 个月**；未压缩版约 **1 个月**（见 [voyage_api.md](references/voyage_api.md)）
- **响应**：`ships.offers.ship[]` 含 `ti`（报位时间）、`la`/`lo`、`sp`（航速）、`co`（航向）、`dis`（累计航程）、`isstoppoint` 及停船相关字段

#### 历史挂靠 / Port call history

查询某船在指定时间段内的靠港记录（已合并港外临时停船等噪声，按时间**降序**，最新在前）。

- **触发**：历史挂靠、靠港记录、挂港历史、去过哪些港、port call history、port calls
- **输入**：`mmsi`（必选）；`starttime`、`endtime`（必选，北京时间，如 `2019-01-01 00:00:00`）；可选 `accuracyval`（默认 `6`）
- **接口**：`GET/POST {base}/position/getcallport/token?mmsi={mmsi}&starttime={start}&endtime={end}&api_key=...`
- **响应**：`result=ok` 时 `list.shipRouteFeature[]` 含 `mPortname`/`cnportname`、`portcode`、`mUpdatetime`（到港/挂靠时间）、`mleavetime`（离港时间）、`country`/`countryCnName`、`lat`/`lon`、`fre`（近一年该港挂靠次数）等

#### 历史航次 / Voyage history

**路由建议**：

| 用户意图 | 优先接口 |
|----------|-----------|
| 最近航次、默认时间窗、不需自定义区间 | `position/getvoyagelist/token`（服务端默认约最近 10 个月，仅传 `mmsi`） |
| 指定起止时间、需航程/航速/吃水等明细 | `portofcall/getvoyages` |

- **触发**：历史航次、航次列表、从哪到哪、航行记录、voyage history、voyage list
- **简版输入**：`mmsi`
- **详版输入**：`mmsi`；`starttime`、`endtime`（必选，北京时间）；可选 `accuracyval`（默认 `5`）、`updatedistance`（默认 `1`，是否补算航程距离）
- **简版接口**：`GET/POST {base}/position/getvoyagelist/token?mmsi={mmsi}&api_key=...`
- **详版接口**：`GET/POST {base}/portofcall/getvoyages?mmsi={mmsi}&starttime={start}&endtime={end}&api_key=...`
- **简版响应**：`list.voyage[]` 含 `startport`/`endport`、`startportcode`/`endportcode`、`starttime`/`endtime`、`timelong`（航行小时数）
- **详版响应**：`result=OK` 时 `list[]` 为 `ShipVoyageBean`，额外含中英文港名与国家、最大/平均航速、航程（海里）、吃水等

#### 上一港 / Last departure

查询船舶最近一次离港港口与离港时间。

- **触发**：上一港、上次离港、从哪出发、last port、last departure、previous port
- **输入**：`mmsi`
- **接口**：`GET/POST {base}/position/lastdeparture/token?mmsi={mmsi}&api_key=...`
- **响应**：`result=ok` 时 `list` 为单条 `LastDeparture`：`portcode`、`portname`、`departtime`（北京时间）、`country`、`countryCode`

#### 当前停船 / Current stop

查询船舶最新停船/到港位置与停船时长（同 legacy `/portofcall/get/shipstoppedplaceandtime` 语义）。

- **触发**：当前停船、停在哪、在港停多久、锚泊、current stop、stopped at port
- **输入**：`mmsi`
- **接口**：`GET/POST {base}/position/getstop/token?mmsi={mmsi}&api_key=...`
- **响应**：`message=ok` 时 `data[]` 含 `portcode`、`enportname`/`cnportname`、`encountry`/`cncountry`、`lat`/`lon`、`stoptime`、`starttime`、`accumulatetime`（累计停船时长描述）

**调用流程**：检查 `api_key` → 若无 MMSI 则 `shipSearch` → 按上表选接口 → 解析并展示；无数据时如实说明（`result=failed` / `empty` / `data` 或轨迹 `ship[]` 为空），勿伪造轨迹点、挂靠或航次。

### 红海与波斯湾海峡通航 / Strait Traffic

咽喉航道通航船舶统计，支持曼德海峡、苏伊士运河、好望角、霍尔木兹海峡，按日期区间与方向返回船型统计及船舶明细。**无 `api_key` 仅可查最近 1 周，有 `api_key` 时间区间不限**。

- **触发**：红海、波斯湾、海峡通航、曼德海峡、苏伊士运河、好望角、霍尔木兹、strait traffic、Red Sea、Persian Gulf
- **输入**：海峡名称或 oid；可选开始/结束日期（yyyy-MM-dd），不传默认最近 7 天；可选 i18n（zh/en）。`api_key` 从配置读取，有则时间不限。
- **API 文档**：[references/strait_traffic_api.md](references/strait_traffic_api.md)；完整接口以 [ShowDoc 45/2234](http://showdoc.hifleet.com/web/#/45/2234) 为准。
- **脚本**：`scripts/get_strait_traffic.py`（海峡名或 oid + 可选 startdate/enddate/i18n，有 `api_key` 可查超 7 天）

**接口**：**POST** `{base}/position/statisticzonetraffic`，Query 参数 oid、startdate、enddate、i18n（可选）、`api_key`（可选）。**海峡 oid**：曼德海峡 24480、苏伊士运河 132808、好望角 1062830、霍尔木兹海峡 24471。无 `api_key` 时校验时间区间 ≤ 7 天。

### 区域船舶 / Area Traffic

查询当前指定区域内的船舶列表。支持三种区域指定方式：**矩形 bbox**、**区域 id（areaId）** 或 **WKT 多边形（polygon）**。用户仅文字描述区域（如 [波斯湾]「红海」「北太平洋」「马六甲海峡」）时，先查区域清单再按 areaId 查询。

- **触发**：区域船舶、范围内船舶、区域船位、某区域有多少船、area traffic、vessels in area
- **输入**：① 矩形区域（左下经度、左下纬度、右上经度、右上纬度）；或 ② 区域名称/海区/贸易区（先调区域清单接口，用 name/cnName 匹配得到 id，再按 areaId 查）；或 ③ WKT 格式 polygon；`api_key` 必填
- **API 详情**：[references/area_traffic_api.md](references/area_traffic_api.md)（gettraffic 支持 bbox、areaId、polygon）；[references/areas_api.md](references/areas_api.md)（区域清单）
- **脚本**：`scripts/get_areas.py`（获取区域清单，供按名称选区域）；`scripts/get_area_traffic.py`（bbox 四参数、`--area-id <id>` 或 `--polygon "POLYGON((...))"`，需 `api_key`）

**调用流程**：检查 `api_key` → 若用户给的是**矩形坐标**：组 bbox → GET `{base}/position/gettraffic/token?bbox=...&api_key=...`；若用户给的是**文字描述**：GET `{base}/position/areas/token`（可选 `api_key`）→ 用 name/cnName 匹配得 id → GET `{base}/position/gettraffic/token?areaId={id}&api_key=...`；若用户给的是**WKT 多边形**：GET `{base}/position/gettraffic/token?polygon=...&api_key=...` → 解析 list 展示船名、MMSI、经纬度、航速、状态、目的港等。

### 进港指南 / Port guide

港口列表检索与单港详细信息。列表可用 `portName` 或 `portCode` 筛选；。

- **触发**：进港指南港口、港口信息、port guide、port detail
- **输入**：列表步可选港名、港口代码；详情步必选港口 id（来自上一步的 `piuid`）；`api_key` 从配置读取；可选 `HIFLEET_API_BASE`
- **API 详情**：[references/port_api.md](references/port_api.md)
- **脚本**：`scripts/get_port.py`（子命令 `search [--port-name] [--port-code]`、`detail <portId>`）

**调用流程**：检查 `api_key` → 调列表接口（按需加 `portName`、`portCode`）→ 展示命中项并请用户确认 → 用 `piuid` 调详情接口。

### 租船 / Charter

租船能力拆为**两个**分册：

| 分册 | 能力 | 说明 |
|------|------|------|
| **`hifleet-schedule/`** | 班轮船期 | 散杂货/滚装/集装箱；联系方式按需 unlock |
| **`hifleet-opentonnages/`** | **公开船盘 + 公开货盘** | 列表查船货信息；**联系方式按需**（记录 id + unlock）；可选 enrich |

- **触发**：租船、船盘、货盘、**公开船盘/公开货盘/平台船货**、班轮船期 / charter, open vessel, cargo, public tonnage, public cargo, marketplace, liner schedule
- **执行入口**：班轮 → `hifleet-schedule/SKILL.md`；**公开船货** → `hifleet-opentonnages/SKILL.md`

### 集装箱红海饶航 / Container ship Red Sea detour

集装箱船舶绕航红海每日统计，按日期区间与方向返回船型统计及船舶明细。**无 `api_key` 仅可查最近 1 周，有 `api_key` 时间区间不限**。

- **触发**：红海饶航、集装箱饶航、Container ship Red Sea detour
- **输入**：必选选开始/结束日期（yyyy-MM-dd）。`api_key` 从配置读取，有则时间不限。
- **API 文档**：[references/avoidredsea_traffic_api.md](references/avoidredsea_traffic_api.md)；
- **脚本**：`scripts/get_avoidredsea_traffic.py`（ 必选 starttiime/endtime，有 `api_key` 可查超 7 天）

### PSC 检查 / PSC Inspection

根据 **IMO** 查询船舶 **港口国监督检查（PSC）** 数据。接口为 **GET** `{base}/pscapi/get`，**必须**带 `api_key`（与其它需鉴权接口一致）。支持用户直接提供 IMO，或提供**船名/关键字**、**9 位 MMSI** 时先走 `position/shipSearch`，从命中结果的 `imonumber` 取得 IMO 再请求 PSC；**无 IMO 的内贸船**无法调本接口。

- **触发**：PSC、港口国监督、港口国检查、滞留、缺陷、检查记录、port state control、PSC inspection、detention、deficiency
- **输入**：IMO（6～7 位数字，可带 `IMO` 前缀）；或船名/关键字；或 9 位 MMSI（与船位技能相同，先搜船再取 IMO）；`api_key` 从配置读取
- **API 详情**：[references/psc_api.md](references/psc_api.md)
- **脚本**：`scripts/get_psc.py`（`IMO` / `船名` / `船名 + MMSI` / `MMSI`）

**调用流程**：检查 `api_key` → 若用户已给 **IMO**：GET `pscapi/get?imo={imo}&api_key=...` → 解析并展示（脚本对常见 `status`+`data` / `list` 结构做分条输出，否则整段 JSON）。若用户给 **船名或 MMSI 关键字**：与船位相同的搜船规则（0/1/多条、多条时让用户选 MMSI）→ 取选定船的 `imonumber`；若为空则提示无 IMO、无法查 PSC → 有 IMO 再调 `pscapi/get`。

#### PSC 统计异常（OpenClaw，同属 PSC 技能）

基于日批统计的 **异常事件表**（`psc_anomaly_event`），与「单船 PSC 记录」互补：回答**某时段、某当局/旗国/港口**等维度下「滞留率/平均缺陷是否相对历史显著升高」等宏观问题。**均需 `api_key`**（与 `pscapi/get` 相同）。

**OpenClaw 字段语义必守**：详见 [references/psc_stats_field_semantics.md](references/psc_stats_field_semantics.md)。核心：`authority` 表示检查国/检查当局，不是船籍国；`ship_type` / `shipType` 表示检查类型，不是船型。真实船型统计当前日批维度不提供。接口细节见 [references/psc_anomaly_api.md](references/psc_anomaly_api.md)。

- **触发**：PSC 异常、统计异常、滞留率飙升、缺陷异常、港口国监督风险、HIGH 严重度 PSC 事件、PSC anomaly、detention spike、deficiency spike、PSC statistics risk
- **输入**：可选日期区间（`yyyy-MM-dd`）；可选 `authority`/`flag`/`port`（精确）、**`authorityContains`/`flagContains`（子串 LIKE，适合「中国/China」等）**、`sliceType`（**`AUTHORITY_FLAG`**=当局×旗国粗粒度异常；**`AUTHORITY_FLAG_PORT_TYPE`**=含港口×检查类型细切片）、`severity`、`anomalyType` 等；列表支持 `page`、`pageSize`
- **API 详情**：[references/psc_anomaly_api.md](references/psc_anomaly_api.md)
- **脚本**：`scripts/get_psc_anomalies.py`（子命令 `list` / `summary` / `get <id>`）

**三类调用**（Agent 按需组合）：

1. **汇总**：`GET {base}/pscapi/openclaw/anomalies/summary?api_key=...&dateFrom=...&dateTo=...` → 按 `severity` 计数，适合先答「严重异常有多少」。
2. **列表**：`GET {base}/pscapi/openclaw/anomalies?api_key=...`（同上筛选 + 分页）→ `data.list` 展示 `title`、`dateEnd`、`severity`、`metric` 等。
3. **详情**：`GET {base}/pscapi/openclaw/anomalies/{id}?api_key=...` → 展开 `description`、`evidence`（JSON 字符串可格式化）。

**数据稀疏时的回答规则（OpenClaw 必守）**  
`psc_anomaly_event` 可能只有极少行或全空，**不得**据此下结论「没有 PSC 风险」「监管很松」等。须遵守 [references/psc_anomaly_api.md](references/psc_anomaly_api.md) 中的 **「异常表数据量过少」专节**，要点如下：

| 情况 | Agent 应做 |
|------|------------|
| `list` 的 `total == 0` 或 summary 全为 0 | 明确说：**仅表示「统计异常事件表」在当前筛选/时间窗内无命中**，不代表无 PSC 活动、不代表无滞留；原因可能是检测阈值严、切片样本不足、未跑全量 `backfill-anomalies`、或 `authority`/`flag`/`port` 与库内**精确字符串**不一致。 |
| `total` 为个位数（如 1～5） | 如实列出；注明 **样本极少、不宜做宏观推断**；可建议放宽日期、减少筛选维度，或改用单船 PSC。 |
| 用户问「中国/巴拿马」等自然语言 | 优先用 **`authorityContains`/`flagContains`**（如 `China`、`Panama`）再查异常表；宏观「某检查国对哪些船旗」优先 **`sliceType=AUTHORITY_FLAG`**；仍 0 条时再说明精确值可能不一致或模型未命中。 |
| 用户要「某船有没有被查」 | **不要用异常表代替**：应走上文 **PSC 检查**（`pscapi/get` + IMO）。 |
| 用户问「为什么一直没有异常」 | 可简述：日批模型只标记**相对历史基线显著升高**的切片；`min-inspections`、Z 阈值、是否已跑异常补算均会影响条数；运维侧可调 newpsc `psc.stats` 或补跑 `backfill-anomalies`（不展开实现细节除非用户是运维）。 |

#### PSC 宏观统计（OpenClaw，原始聚合 / 缺陷 / 占比）

与 **异常事件表**互补：直接基于 **`pscdata.psc`**（及 **`psc_defect_distribution`**）做可引用数字，支撑「哪国变严」「哪旗/哪港风险」「缺陷热点」「是否某旗占比上升」等；**不替代**因果推断与预测。

- **文档**：[references/psc_openclaw_stats_api.md](references/psc_openclaw_stats_api.md)（含与九类问题的映射与能力边界）
- **脚本**：`scripts/get_psc_openclaw_stats.py`（`compare` / `defects` / `mix`）

**Agent 路由建议**：

| 用户意图 | 优先接口 |
|----------|-----------|
| 国家/全局监管变严、检查量/滞留率环比 | `GET {base}/pscapi/openclaw/stats/compare`（`groupBy=AUTHORITY`/`GLOBAL`，可用 `authorityContains`） |
| 船旗风险排行、某旗滞留率 | `compare` + `groupBy=FLAG`；结合 `anomalies` |
| **中国/某国主要检查港口、哪港严** | **`stats/compare` 必调**：`groupBy=PORT` 或 `AUTHORITY_PORT` + `authorityContains`（如 `China`）；**禁止**在未请求接口时用常识港口列表冒充数据；**禁止**谎称「港口接口故障」除非返回明确错误（并说明 code）。 |
| 最近查什么缺陷、缺陷码热点 | `GET {base}/pscapi/openclaw/stats/defects/top`（需 newpsc 已写缺陷分布表） |
| 是否「针对」某旗 / 检查类型占比变化 | `GET {base}/pscapi/openclaw/stats/mix/compare`（`mixDimension=FLAG` 或 `TYPE_INS`）；**勿断言政治针对**，`TYPE_INS` **不是**散货船等船型 |
| 统计模型认定的异常 spike | 仍用 `openclaw/anomalies*` |
| 某船/IMO | `pscapi/get` |

**合规**：勿输出投资建议（「必避开某港」）；可陈述事实与风险提示。无「风险预测」专用接口，对未来表述须谨慎。


### 账户与用量 / Account & Usage

用户询问**积分余额、调用记录、扣费流水**，或需 **注册、充值、订阅、开发票** 时使用（与业务查询共用同一 `api_key`）。账户查询**本身不扣积分**。

- **触发**：积分、余额、还剩多少、用了多少、调用记录、扣费、消费、流水、注册、开户、充值、订阅、包月、Token Plan、付费、发票、控制台、打开控制台、用 api_key 登录、account balance、usage、credits、billing、invoice、signup、console SSO
- **入门**：[FIRST_SETUP.md](FIRST_SETUP.md)（无 Key 时必读）
- **注册与 Key**：[references/account_onboarding_api.md](references/account_onboarding_api.md)（已实现）
- **换票进控制台**：[references/console_sso_api.md](references/console_sso_api.md)（已有 Key 时打开用量/钱包，无需再验证码登录）
- **充值与发票**：[references/billing_api.md](references/billing_api.md)（已实现）
- **用量查询**：[references/account_api.md](references/account_api.md)（已实现）
- **脚本**：`scripts/open_console.py`（换票并打开 `consoleUrl`）

**Agent 路由（必守）**：

| 用户意图 | 接口 / 文档 |
|----------|-------------|
| 没有 api_key、怎么开始、注册 | [FIRST_SETUP.md](FIRST_SETUP.md) → `send-code` → `register`（402 时打开 `register-capture.html`） |
| 打开控制台、看用量页、钱包、用 api_key 登录 | [console_sso_api.md](references/console_sso_api.md) → 换票 → 打开 `consoleUrl`（skills.hifleet.com） |
| 介绍 Skills / 产品页 | `https://skills.hifleet.com/`（无需换票） |
| 还能用多少积分 | `GET/POST {base}/openclaw/account/summary` → 只向用户强调 **`availablePoints`**（含混合计费可调用量） |
| 我的订阅、周期额度 | `GET {base}/openclaw/billing/subscription` 或 `token-plans` 中的 `quota` |
| 积分不足、充值、订阅、买单 | [billing_api.md](references/billing_api.md) → `token-plans` → `billing/orders` → `paymentPageUrl` |
| 付了吗、到账了吗 | `billing/orders/{orderId}` + `account/summary` 或 `billing/subscription` |
| 取消订阅、超额用积分 | `billing/subscription/cancel`、`billing/subscription/over-quota` |
| 发票、开票、报销 | [billing_api.md](references/billing_api.md) §4 |
| 最近调了哪些接口 | `{base}/openclaw/account/usage/details` |
| 什么时候真正扣款 | `{base}/openclaw/account/transactions` |
| 按小时统计 | `{base}/openclaw/account/usage` |

**积分不足（业务调用失败时）**：

1. 业务接口返回 `code=4021` 或 `summary.availablePoints <= 0` → 先 `billing/subscription` 区分周期额度用尽还是无充值积分，再引导充值或续订（勿伪造付款链接）。  
2. 下单成功后发送 **`paymentPageUrl`** 完整链接，让用户在收银台选微信/支付宝；勿硬编码支付渠道。  
3. 支付成功后：积分单用 `summary` + `transactions`（`direction=IN`）确认；订阅单用 `billing/subscription` 确认额度。

**回答规则**：

1. 优先朗读或改写响应中的 **`agentSummary`**；列表可引用 **`items[].itemSummary`**。  
2. 余额问题**只引用 `availablePoints`**，勿自行对 `accountBalance` 与 `pendingDeduction` 做加减。  
3. **调用明细 ≠ 积分流水**：明细是每次请求；流水是账户真正入账/出账。用户问「扣了没有」而流水暂无 → 说明可能**待入账**（小时结算后出现在 `transactions`）。  
4. 勿向用户解释内部结算、unsettled 等运维术语；`pendingDeduction` 出现时按 `balanceHint` / `agentSummary` 简述即可。  
5. 勿伪造积分、调用次数、流水、支付链接或发票。完整 **api_key 仅注册/轮换时展示一次**，后续对话只显示前缀与末 4 位。

---

## 安全与合规

本技能仅向 `{base}`（默认 `https://api.hifleet.com`，可由 `HIFLEET_API_BASE` 覆盖）下的船位/档案/航程/PSC/海峡通航/区域船舶等固定路径发起只读请求（GET 或 POST）；鉴权接口使用 `api_key`。基址约定见 [references/api_base.md](references/api_base.md)；详见 [SECURITY.md](SECURITY.md)。

## 参考资料与脚本

| 路径 | 说明 |
|------|------|
| [SECURITY.md](SECURITY.md) | 安全说明（网络行为、Token 用途、无动态代码） |
| [INSTALL.md](INSTALL.md) | 安装获取：ClawHub / GitHub / zip 手动安装包 |
| [references/api_base.md](references/api_base.md) | API 基址 `{base}` 与 `HIFLEET_API_BASE` 约定 |
| [references/skills_index.md](references/skills_index.md) | 技能清单（中英双语、触发词） |
| [references/position_api.md](references/position_api.md) | 船位 API 完整说明与响应字段 |
| [references/archive_api.md](references/archive_api.md) | 档案 API 说明与 data 分类 |
| [references/casualty_api.md](references/casualty_api.md) | 事故事件 API：按 IMO 列表、按 eventId 详情 |
| [references/sanction_api.md](references/sanction_api.md) | 制裁风险评估 API：按 IMO（US/EU/UK/Canada/UN/CN） |
| [references/maritime_penalty_api.md](references/maritime_penalty_api.md) | 海事行政处罚 API：按船名/MMSI/时间 |
| [references/ship_archive_stats_api.md](references/ship_archive_stats_api.md) | 船舶档案统计 API：聚合统计、档案明细分页和批次元信息（OpenClaw） |
| [references/voyage_api.md](references/voyage_api.md) | 航程 API：历史挂靠、历史航次、上一港、当前停船（OpenClaw） |
| [references/strait_traffic_api.md](references/strait_traffic_api.md) | 红海/波斯湾海峡通航 API（oid、时间范围） |
| [references/area_traffic_api.md](references/area_traffic_api.md) | 区域船舶 API（bbox、areaId、polygon、api_key） |
| [references/areas_api.md](references/areas_api.md) | 区域清单 API（海区/贸易区列表，供按名称选 areaId） |
| [references/psc_api.md](references/psc_api.md) | PSC 检查 API（pscapi/get，imo + api_key） |
| [references/psc_anomaly_api.md](references/psc_anomaly_api.md) | PSC 统计异常 API（openclaw/anomalies*，api_key，可选 HIFLEET_API_BASE） |
| [references/psc_openclaw_stats_api.md](references/psc_openclaw_stats_api.md) | PSC 宏观统计（openclaw/stats/compare、defects/top、mix/compare） |
| [references/psc_stats_field_semantics.md](references/psc_stats_field_semantics.md) | PSC 多表字段语义：`authority`=检查国、`ship_type`=检查类型（非船型） |
| [FIRST_SETUP.md](FIRST_SETUP.md) | 首次配置：注册、api_key、充值、发票全链路 |
| [references/account_onboarding_api.md](references/account_onboarding_api.md) | 账户入门：注册、登录、api_key 发放（已实现） |
| [references/console_sso_api.md](references/console_sso_api.md) | Skills 控制台 SSO：api_key 换票打开 skills.hifleet.com 控制台 |
| [references/billing_api.md](references/billing_api.md) | 计费与发票：积分包、订阅、收银台、混合额度、开票（已实现） |
| [references/account_api.md](references/account_api.md) | 账户与用量：summary / usage / usage/details / transactions（需 `api_key`，已实现） |
| scripts/open_console.py | 用 `HIFLEET_API_KEY` 换票并打开控制台 `consoleUrl` |
| scripts/get_position.py | 按关键字或 MMSI 获取船位（需 `api_key`；可选 `HIFLEET_API_BASE`） |
| scripts/get_archive.py | 按 IMO 或 MMSI 获取船舶档案（需 `api_key`；可选 `HIFLEET_API_BASE`） |
| scripts/get_casualty.py | 事故事件：`list <IMO>` / `detail <eventId>`（需 `api_key`；可选 `HIFLEET_API_BASE`） |
| scripts/get_sanction.py | 制裁风险评估：`<IMO>`（需 `api_key`；可选 `HIFLEET_API_BASE`） |
| scripts/get_maritime_penalty.py | 海事行政处罚：`--ship-name` / `--mmsi` / 时间（需 `api_key`） |
| scripts/get_strait_traffic.py | 海峡通航统计（POST `{base}/position/statisticzonetraffic`）；可选 `HIFLEET_API_BASE` |
| scripts/get_avoidredsea_traffic.py | 集装箱红海饶航（POST `{base}/routerisk/getAvoidRedSeaDetail/token`）；可选 `HIFLEET_API_BASE` |
| scripts/get_areas.py | 区域清单（`{base}/position/areas/token`）；可选 `HIFLEET_API_BASE` |
| scripts/get_area_traffic.py | 区域船舶（`{base}/position/gettraffic/token`，需 `api_key`）；可选 `HIFLEET_API_BASE` |
| scripts/get_psc.py | PSC 检查（需 `api_key`；可选 `HIFLEET_API_BASE`） |
| scripts/get_psc_anomalies.py | PSC 统计异常：list / summary / get id（需 `api_key`，可选 HIFLEET_API_BASE） |
| scripts/get_psc_openclaw_stats.py | PSC 宏观统计：compare / defects / mix（需 `api_key`，可选 HIFLEET_API_BASE） |
