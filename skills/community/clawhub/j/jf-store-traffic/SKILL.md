---
name: jf-store-traffic
description: 杰峰连锁门店精准客流部署与数据分析技能。通过工作流完成门店创建、HA-5P-GM客流摄像头接入、精准客流算法配置（区域画框/进出店模式/外卖员过滤），并支持查询门店客流聚合统计（进店率/去重顾客数/批次/年龄性别分布），生成可视化 HTML 分析报告（KPI 总览/每日趋势/客群画像/进店批次）。当用户提到精准客流、门店客流、客流统计、客流部署、配置客流、连锁门店、进店率、客群分析、客流报告、客流报表、store traffic、foot traffic 时使用此技能。
---

# 杰峰连锁门店精准客流部署技能

## 1. 技能描述

本技能覆盖杰峰「连锁门店精准客流」行业方案的完整接入与数据运营：

- **门店管理** -- 创建 / 修改 / 删除门店
- **设备管理** -- 添加 / 删除客流摄像头（HA-5P-GM）
- **客流配置** -- 区域画框（out/in 四边形）、客流模式、算法开关、外卖员过滤、OSD 叠加、运行时段
- **数据统计** -- 查询门店客流聚合统计（总客流、进店率、去重数、进店批次、年龄/性别分布）
- **HTML 分析报告** -- 一键生成带 Tab 切换的可视化报告（KPI 卡片、每日趋势、客群画像、进店批次图表）
- **交互式配置工具页** -- 基于 Canvas 的可视化画框工具，在摄像头快照上绘制检测区域并导出 JSON 配置
- **有状态会话模型** -- `session.json` 自动传递中间参数（store id、nodeId、device id 等），步骤间无需手动搬运

字段级 API 细节（请求/响应字段、状态码、区域 Endpoint、名词解释）集中在 [references/api-reference.md](references/api-reference.md)，需要时再读取。

> **数据消费方式：** 本技能通过聚合统计接口 `/rtc/store/flowStatistics` 主动查询数据（不依赖回调推送，Agent 环境无公网接收地址），查询结果以表格或 HTML 报告形式呈现。

## 2. 前置条件

### 2.1 设备要求

| 项目 | 要求 |
|------|------|
| 型号 | **HA-5P-GM**（精准客流专用，不支持云台，吊顶安装前需手动调好视角） |
| 安装高度 | 不低于 2 米，以 30°-45° 俯角监控检测区域 |
| 安装位置 | 正对大门，同时可见店内/店外区域，人员正面进店（去重依赖正面抓拍比对），尽量无遮挡 |
| 带宽 | 单个摄像头预留 **4M 上行带宽**（2M 主码流 + 2M 图片上报） |

### 2.2 环境变量

| 变量名 | 必填 | 说明 | 默认值 |
|--------|------|------|--------|
| `JF_UUID` | 是 | 开放平台用户 uuid | - |
| `JF_APP_KEY` | 是 | 应用 appKey | - |
| `JF_APP_SECRET` | 是 | 应用 appSecret | - |
| `JF_MOVE_CARD` | 否 | 签名移位取模基数 | `2` |
| `JF_ENDPOINT` | 否 | API 域名 | `api-cn.jftechws.com` |

所有 API 调用由 `scripts/crypto.py` 自动计算签名（uuid+appKey+appSecret+timeMillis 拼接 → 移位 → 合并 → MD5），timeMillis 为 7 位计数器 + 13 位毫秒时间戳，实时生成。

### 2.3 授权与计费

精准客流算法需云端订阅计费（每日扣费）。SaaS 用户需提交工单申请开通端云精准客流算法授权；仅支持中国大陆地区销售，Endpoint 固定 `api-cn.jftechws.com`。

## 3. API 接口总览

| 功能 | 接口地址（https://Endpoint/gwp/v3 前缀） | 脚本命令 |
|------|----------|------|
| 创建门店 | `/rtc/store/create` | create-store |
| 修改门店 | `/rtc/store/edit` | edit-store |
| 删除门店 | `/rtc/store/delete` | delete-store |
| 添加客流设备 | `/rtc/device/addJfIpc` | add-device |
| 删除客流设备 | `/rtc/device/delete` | delete-device |
| 设备在线状态（诊断用，可选） | `/rtc/device/token` + `/rtc/device/status` | device-status |
| 设备快照（直播抽帧，唯一快照路径） | `/rtc/device/token` + `/rtc/device/login/{token}` + `/rtc/device/livestream/{token}` | snapshot |
| 绑定设备到账号（可选，非 addJfIpc 前置） | `/rtc/device/bind` | bind-device |
| 精准客流配置 | `/rtc/device/aiCrowdFlowConfig` | config-flow |
| 门店客流聚合统计 | `/rtc/store/flowStatistics` | flow-stats / flow-report |

请求头（uuid、appKey、timeMillis、signature、X-Request-Id、Content-Type）由脚本自动处理。各接口字段详见 [references/api-reference.md](references/api-reference.md)。

## 4. 工作流 1：完整部署（从零配置）

为一家新门店完成全部配置：

```
1. 初始化会话
   python scripts/store_traffic.py --session ./session init

2. 创建门店
   python scripts/store_traffic.py --session ./session create-store --store-name "XX旗舰店" --address "XX市XX路XX号" --longitude 120.123456 --latitude 30.123456

3. 添加客流设备（无需预先绑定账号；设备须已通电联网，否则返回 4116）
   python scripts/store_traffic.py --session ./session add-device --sn "HA5PGMXXXXXXXX" --network-type 0 --device-name "入口摄像头" --device-username admin --device-password "password123"

4. 获取摄像头快照（HA-5P-GM 不支持 OPSNAP 云抓图，统一走直播抽帧）
   python scripts/store_traffic.py --session ./session snapshot --output ./snapshot.jpg

5. 生成交互式配置工具页
   python scripts/store_traffic.py --session ./session generate-config-page --snapshot snapshot.jpg --output ./config_tool.html

6. [用户在浏览器中打开 config_tool.html]
   - 在快照上绘制 店外框（out，蓝色）和 店内框（in，绿色），各 4 个顶点
   - 配置客流模式、算法开关、OSD、外卖员过滤、运行时段
   - 点击"生成配置 JSON" -> "下载 config_output.json"

7. 导入配置到设备
   python scripts/store_traffic.py --session ./session config-flow --from-file config_output.json

8. 确认部署状态
   python scripts/store_traffic.py --session ./session status
```

> **快照（实测，单一路径）：** HA-5P-GM 固件不支持 OPSNAP 云抓图（`/rtc/device/capture/{token}` 返回 `Ret=101`，设备状态码 101 = 设备不支持 RESTful API），**不要使用任何抓图接口**。`snapshot` 命令封装唯一快照链路：`/rtc/device/token`（Body `{"sns":[SN]}`，token 24 小时有效，命令每次自动重新获取）→ `/rtc/device/login/{token}`（Body `{"UserName":"admin","PassWord":""}`，空密码为出厂默认）→ `/rtc/device/livestream/{token}`（Body 须含 `username`/`password`，否则 4000）取主码流 FLV 地址 → PyAV 解码保存第 15 帧（依赖 `pip install av`，无需系统 ffmpeg）。输出直接交给 `generate-config-page --snapshot`。
>
> **4116 排查：** add-device 返回 `4116 Not found` 有两个实测成因：① 设备未联网（未在杰峰云注册上线），需设备通电联网后重试；② **调用应用（appKey）未开通精准客流服务**——同一台在线设备，未开通的应用返回 4116，已开通的应用返回 2000，需到开放平台为应用开通端云精准客流授权。addJfIpc 不校验账号绑定（实测：解绑后调用仍返回 4116 而非 29010）。`device-status` 诊断要求设备已绑定账号（token 接口对未绑定设备返回 29010 DEV_NOTEXIT），因此排查时可先 `bind-device` 再 `device-status` 确认在线状态；绑定仅用于诊断，不是 addJfIpc 的前置条件。

## 5. 工作流 2：查询客流统计数据（表格/JSON）

使用 `flowStatistics` 接口查询门店客流聚合统计：

```
# 查询当前会话门店今日数据（默认时间范围为当天）
python scripts/store_traffic.py --session ./session flow-stats

# 指定时间范围
python scripts/store_traffic.py --session ./session flow-stats --start "2026-07-01 00:00:00" --end "2026-07-13 23:59:59"

# 指定门店 / 设备 / 全部门店
python scripts/store_traffic.py --session ./session flow-stats --store-id 187886354593562624
python scripts/store_traffic.py --session ./session flow-stats --device-sn 391802e78fcfe6c5
python scripts/store_traffic.py --session ./session flow-stats --all-stores

# JSON 原始输出（便于二次加工/做报表）
python scripts/store_traffic.py --session ./session flow-stats --format json
```

storeId 缺省时自动取会话中的门店 id，无会话则查询全部门店。返回指标包括总客流、进/出/过店客流、进店率、去重数、单人/双人/三人/多人批次、年龄段与性别分布，字段含义见 [references/api-reference.md](references/api-reference.md#门店客流聚合统计字段)。

## 6. 工作流 3：生成 HTML 分析报告（推荐）

`flow-report` 在聚合统计接口基础上生成独立 HTML 报告（Tab 切换 + Chart.js 图表，浏览器打开即用，可直接发给业务方）：

```
# 默认：会话门店最近 7 天，输出 ./flow_report.html
python scripts/store_traffic.py --session ./session flow-report

# 指定时间范围与输出文件
python scripts/store_traffic.py --session ./session flow-report --start "2026-07-01 00:00:00" --end "2026-07-31 23:59:59" --output ./july_report.html

# 指定门店 / 设备 / 全部门店 / 自定义标题
python scripts/store_traffic.py --session ./session flow-report --store-id 187886354593562624
python scripts/store_traffic.py --session ./session flow-report --device-sn 391802e78fcfe6c5
python scripts/store_traffic.py --session ./session flow-report --all-stores --title "全国门店客流周报"
```

报告包含四个视图（Tab 切换）：

| Tab | 内容 |
|-----|------|
| 总览 | KPI 卡片（总客流/进店/出店/过店/进店率/去重顾客数）+ 原始 vs 去重过滤后对比柱状图 + 24 项指标明细表 |
| 趋势 | 每日总客流/进店/过店折线图 + 进店率（右轴） |
| 客群画像 | 年龄段分布条形图 + 性别占比环图 |
| 进店批次 | 单人/双人/三人/多人批次占比环图 |

数据获取策略：整段区间查询一次作为总览，再按自然日逐天查询（日间隔 0.5s 防限频）支撑趋势图；时间范围最长 62 天。storeId 解析优先级：`--store-id` > 会话门店 > 全部门店。

生成后将 HTML 文件路径提供给用户（file:// 链接），报告内数据已内联，离线可看（图表库走 CDN，加载失败时 KPI 与明细表仍可用）。

## 7. 工作流 4：修改门店 / 删除

```
# 修改门店（自动使用会话中的 store id）
python scripts/store_traffic.py --session ./session edit-store --store-name "XX旗舰店（新）" --address "新地址"

# 删除设备（先于门店删除）
python scripts/store_traffic.py --session ./session delete-device

# 删除门店
python scripts/store_traffic.py --session ./session delete-store
```

> **顺序很重要：** 门店下有设备时，先删设备再删门店。

## 8. 工作流 5：查看与调试

```
python scripts/store_traffic.py --session ./session status            # 部署进度
python scripts/store_traffic.py --session ./session status --format json
python scripts/store_traffic.py --session ./session reset             # 重置会话
```

## 9. CLI 直接配置客流（不使用工具页）

已知区域坐标时可直接下发（includeAreas 为 8192 相对坐标系 JSON 字符串，第一个框为店外 out、第二个为店内 in）：

```bash
python scripts/store_traffic.py --session ./session config-flow \
  --flow-type 0 --open-status 1 --osd 1 --filter-delivery 1 \
  --areas '[{"points":[{"X":1000,"Y":2000},{"X":3000,"Y":2000},{"X":3000,"Y":4000},{"X":1000,"Y":4000}],"name":"out"},{"points":[{"X":4000,"Y":2000},{"X":6000,"Y":2000},{"X":6000,"Y":4000},{"X":4000,"Y":4000}],"name":"in"}]' \
  --task-time '[{"start":"08:00:00","end":"22:00:00"}]'
```

客流模式：0 = 进过店（进店+过店同时统计），1 = 仅进店（走廊/过道场景，需与另一台过店摄像头配合），2 = 仅过店。

> **类型坑（实测）：** `flowType`/`openStatus`/`showOsdStatus`/`deliveryDriversStatus` 官方文档标注为 string，但真实 API 按 int 校验，传字符串返回 4000 "xxx is illegal"。脚本已自动转 int（`--from-file` 与 CLI 两条路径均适用）；`includeAreas`/`taskTime` 保持 JSON 字符串不变。

## 10. 交互式配置工具页

> **强制约束：** 区域配置必须使用本技能内置的配置工具页（`generate-config-page` 命令由 `assets/config_tool.html` 模板生成），**禁止 agent 自行创建配置工具**（不得另写画框页面、坐标映射或 JSON 导出逻辑）。8192 坐标归一、out/in 顺序与命名、每框 4 顶点约束、开关字段结构均已固化在模板中，自建工具极易产生坐标系或字段偏差导致配置错位。

`generate-config-page` 生成独立 HTML（`config_tool.html`），浏览器打开即用：

- 店外框（out，蓝色）/ 店内框（in，绿色），每框恰好 4 个顶点，依次点击放置，可拖拽调整、撤销、清空
- 内部将画面坐标映射为 **8192×8192** 相对坐标系，原点为画面左上角
- 配置面板：客流模式、算法开关、OSD 叠加、外卖员过滤（美团/饿了么/京东/顺丰）、运行时段（多段 HH:MM:SS）
- 导出：点击"生成配置 JSON" → "下载 config_output.json"，再交给 `config-flow --from-file` 下发

## 11. 会话状态（session.json）

会话目录由 `--session` 指定（默认 `./session`），文件 `<session_dir>/session.json`，每次保存自动备份 `session.json.bak`。

```json
{
  "sessionId": "uuid",
  "createdAt": "...", "updatedAt": "...",
  "steps": {
    "store":      { "completed": true, "data": { "id": "...", "nodeId": "...", "storeName": "..." } },
    "device":     { "completed": true, "data": { "id": "...", "deviceSN": "...", "status": 1 } },
    "flowConfig": { "completed": true, "data": { "configuredAt": "...", "params": { } } }
  }
}
```

自动参数传递：

| 上游步骤 | 传递字段 | 下游步骤 |
|----------|----------|----------|
| store | `nodeId` | add-device |
| store | `id` | edit-store, delete-store, flow-stats, flow-report |
| store | `storeName` | flow-report（报告标题） |
| device | `id` | config-flow, delete-device, generate-config-page |
| device | `deviceSN` | generate-config-page, flow-stats / flow-report(--device-sn 可选) |

## 12. 常用状态码

| 状态码 | 含义 | 处理建议 |
|--------|------|----------|
| `2000` | 成功 | 正常处理返回数据 |
| `4000` | 参数错误 | 检查 Body 字段与格式 |
| `4007` | timeMillis 过期 | 检查系统时钟，时间戳须实时生成 |
| `4009/4013` | 请求频率受限 | 等待 60 秒后重试（flow-report 逐日查询已内置 0.5s 间隔） |
| `28005` | 签名校验错误 | 核对 `JF_APP_SECRET`、`JF_MOVE_CARD` |
| `28006` | 未找到用户信息 | 检查 `JF_UUID` |
| `28007` | 请求头参数错误 | 检查鉴权请求头完整性 |
| `29001/29010/29011/29012` | 设备已存在 / 未绑定 / 已被其它账户添加 / 达上限 | 按提示处理设备绑定关系 |
| `4116` | Not found（addJfIpc 添加设备时） | ① 设备未联网/未在杰峰云注册上线（device-status 显示 notfound），需设备通电联网后重试；② 调用应用未开通精准客流服务（换已开通的应用即成功）。官方文档未要求 addJfIpc 前绑定账号 |
| `5000` | 服务端错误 | 稍后重试或联系技术支持 |

完整状态码见 [references/api-reference.md](references/api-reference.md#常用状态码)。

## 13. 注意事项

1. **仅支持 HA-5P-GM 型号**，不支持云台；安装视角须在吊顶前手动调好。
2. **8192 相对坐标系**：区域顶点为 0-8192 整数，原点画面左上角；必须绘制 out（店外，第一个）与 in（店内，第二个）两个四边形。
3. **进出店判定**：人体框底部中心点相对 IN/OUT 区域的位置变化，进店=OUT→IN，出店=IN→OUT，过店=仅经 OUT。
4. **多摄像头门店自动按门店维度合并去重**，无需额外设置；同比/环比/进店率/批次基于未去重数据统计。
5. **OSD 叠加为未去重数据**，每日 24 点清零；外卖员过滤开启后过滤美团、饿了么、京东、顺丰。
6. **去重顾客数**（sumRemoveDuplicateInboundCount）= 去重 + 外卖/店员等过滤后的进店人数，是衡量真实顾客数的核心指标。
7. **仅支持中国大陆**：Endpoint 固定 `api-cn.jftechws.com`。
8. 阈值/置信度建议使用默认值，调整选择在开店前或闭店后。
9. **禁止自建配置工具**：画框配置页必须由 `generate-config-page` 从内置 `assets/config_tool.html` 生成，agent 不得自行创建配置工具或坐标映射逻辑，保证不同 agent 加载后执行结果一致。

## 14. 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能定义与工作流 |
| `scripts/store_traffic.py` | 主 CLI -- 门店/设备/客流配置/统计/报告全部操作 |
| `scripts/crypto.py` | 杰峰 OpenAPI 签名与时间戳算法实现 |
| `assets/config_tool.html` | 交互式画框配置工具页模板 |
| `assets/flow_report_template.html` | HTML 分析报告模板（Tab + Chart.js，数据内联注入） |
| `references/api-reference.md` | 字段级 API 参考：请求/响应字段、状态码、Endpoint、名词解释 |
