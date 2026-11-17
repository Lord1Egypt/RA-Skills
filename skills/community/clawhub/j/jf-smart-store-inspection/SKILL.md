---
name: jf-smart-store-inspection
version: 1.1.0
description: 杰峰蜂云智慧巡店部署与AI巡检运营技能。通过工作流完成门店创建、监控设备接入（GB28181/ONVIF+自研NVR/杰峰自研IPC）、AI巡检算法查询、AI巡检计划配置（离岗/工服/跌倒/客流/安全帽/视频质量诊断等）、检测区域画框、计划启停与巡检记录聚合，并生成含抓拍图墙的HTML分析报告。当用户提到智慧巡店、AI巡检、门店巡检、巡检计划、巡检记录、离岗检测、工服检测、跌倒检测、抓拍图墙、连锁门店巡检、smart store inspection、AI patrol 时使用此技能。
---

# 杰峰智慧巡店部署技能

## 1. 技能描述

本技能覆盖蜂云 SaaS「智慧巡店」行业方案的完整接入与AI巡检运营，与 `jf-store-traffic`（精准客流）、`jf-store-plate-recognition`（车牌识别）共用同一套开放平台签名与门店/设备管理骨架，专注 **AI巡检计划** 与 **巡检记录** 的全生命周期：

- **门店管理** -- 创建 / 修改 / 删除门店（`/rtc/store/*`）
- **设备管理** -- 添加 / 删除杰峰IPC（`/rtc/device/addJfIpc`、`/rtc/device/delete`）
- **AI巡检算法目录** -- 分页查询已授权的算法及默认参数（`aiPatrolAlgorithmPageQuery`）
- **AI巡检计划** -- 新增 / 编辑 / 分页查询 / 详情 / 启用 / 停用 / 删除（`aiPatrolAddOrEdit`、`aiPatrolPageQuery`、`aiPatrolDetail`、`aiPatrolStartAndStop`、`aiPatrolDelete`）
- **AI巡检记录** -- 分页查询巡检触发记录（含抓拍图 `cloudPictureUrl`）、按设备/算法/日期聚合、HTML 可视化报告（`aiPatrolRecordPageQuery`）
- **交互式区域画框** -- 基于设备快照绘制 `includeAreas` 多边形，8192 相对坐标输出
- **有状态会话模型** -- `session.json` 自动串联 store → device → patrolPlan

字段级 API 细节（请求/响应字段、状态码、算法目录字段含义）集中在 [references/api-reference.md](references/api-reference.md)，需要时再读取。

> **数据消费方式：** AI巡检记录通过 `aiPatrolRecordPageQuery` 主动分页拉取（不依赖回调），本技能 `patrol-report` 命令一次性抓取时间区间内所有记录并聚合成 HTML 报告。

## 2. 前置条件

### 2.1 服务开通

- **智慧巡店订阅**：5 店免费，超出 ¥25/店/月，按门店数计费（不含摄像头路数）。开通入口：企业管理 → 企业套餐。
- **AI算法授权**：AI巡检依赖算法中心的对应算法授权（离岗检测 / 工服检测 / 电动车检测 / 跌倒检测 / 未戴安全帽 / 视频质量诊断 / 客流检测 等），按算法计费。
- **摄像头接入**：门店摄像头需支持 GB28181 / ONVIF+杰峰自研NVR / 杰峰自研IPC，并归属到门店节点。

### 2.2 环境变量

| 变量名 | 必填 | 说明 | 默认值 |
|--------|------|------|--------|
| `JF_UUID` | 是 | 开放平台用户 uuid | - |
| `JF_APP_KEY` | 是 | 应用 appKey | - |
| `JF_APP_SECRET` | 是 | 应用 appSecret | - |
| `JF_MOVE_CARD` | 否 | 签名移位取模基数 | `2` |
| `JF_ENDPOINT` | 否 | API 域名 | `api-cn.jftechws.com` |

签名算法：`md5(merge(uuid+appKey+appSecret+timeMillis, shift(...)))`，`timeMillis` 为 7 位计数器 + 13 位毫秒时间戳，由 `scripts/crypto.py` 实时生成。

### 2.3 Python 依赖

```bash
pip install requests
# 可选：仅当需要从直播流抓帧做画框配置时
pip install av -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 3. API 接口总览

| 功能 | 接口地址（`https://Endpoint/gwp/v3` 前缀） | 脚本命令 |
|------|----------|------|
| 创建门店 | POST `/rtc/store/create` | create-store |
| 修改门店 | POST `/rtc/store/edit` | edit-store |
| 删除门店 | POST `/rtc/store/delete` | delete-store |
| 添加设备（杰峰IPC） | POST `/rtc/device/addJfIpc` | add-device |
| 删除设备 | POST `/rtc/device/delete` | delete-device |
| AI巡检算法目录 | POST `/rtc/device/aiPatrolAlgorithmPageQuery` | list-algorithms |
| AI巡检计划新增/编辑 | POST `/rtc/device/aiPatrolAddOrEdit` | create-plan / edit-plan |
| AI巡检计划分页查询 | POST `/rtc/device/aiPatrolPageQuery` | list-plans |
| AI巡检计划详情 | POST `/rtc/device/aiPatrolDetail/{batchNumber}` | plan-detail |
| AI巡检计划启停 | POST `/rtc/device/aiPatrolStartAndStop` | start-plan / stop-plan |
| AI巡检计划删除 | POST `/rtc/device/aiPatrolDelete/{batchNumber}` | delete-plan |
| AI巡检记录分页 | POST `/rtc/device/aiPatrolRecordPageQuery` | list-records / patrol-report |
| 设备快照（直播抽帧） | POST `/rtc/device/token` + `/rtc/device/login/{token}` + `/rtc/device/livestream/{token}` | snapshot |

请求头（uuid、appKey、timeMillis、signature、X-Request-Id、Content-Type）由脚本自动处理。

## 4. 工作流 1：从零部署 AI 巡检

```
1. 初始化会话
   python scripts/smart_store_inspection.py --session ./session init

2. 创建门店
   python scripts/smart_store_inspection.py --session ./session create-store \
     --store-name "XX旗舰店" --address "XX市XX路XX号" --longitude 120.123456 --latitude 30.123456

3. 添加设备（deviceNetworkType=0 已配网，1 未配网；device-username 默认 admin）
   python scripts/smart_store_inspection.py --session ./session add-device \
     --sn "JFIPCXXXXXXXX" --network-type 0 --device-name "收银台摄像头"

4. 查看已授权的AI算法目录，选定 algorithmId
   python scripts/smart_store_inspection.py --session ./session list-algorithms
   python scripts/smart_store_inspection.py --session ./session list-algorithms --name "离岗"

5. 创建AI巡检计划（一个设备 × 一个算法）
   python scripts/smart_store_inspection.py --session ./session create-plan \
     --plan-name "收银台离岗巡检" \
     --time-type 0 --time-cycle "0" \
     --detail-time "09:00-12:00,14:00-18:00" \
     --algorithm-id 1001 --threshold 0.85 \
     --step 5 --duration-time 60
   # patrolRange 自动取会话中 device.id；如指定其他设备用 --patrol-range

6. （可选）绘制 includeAreas 检测区域
   python scripts/smart_store_inspection.py --session ./session snapshot
   python scripts/smart_store_inspection.py --session ./session generate-config-page --snapshot ./session/snapshot.jpg
   # 浏览器打开 config_tool.html → 绘制多边形 → 生成配置 JSON → 下载 plan_config.json
   python scripts/smart_store_inspection.py --session ./session edit-plan --from-file plan_config.json

7. 确认部署状态
   python scripts/smart_store_inspection.py --session ./session status
```

**timeType / timeCycle / detailTime 规则**：

| timeType | timeCycle 含义 | 示例 |
|----------|--------------|------|
| 0（每天） | 固定 `"0"` | `"0"` |
| 1（每周） | 星期数字，逗号分隔（1-7） | `"1,3,5"` = 周一三五 |
| 2（每月） | 日期数字，逗号分隔（1-31） | `"1,15,28"` = 每月 1/15/28 号 |

`detailTime` 格式 `HH:MM-HH:MM,HH:MM-HH:MM`，最多 5 段，**不允许重合、不允许跨天**。

## 5. 工作流 2：查询/管理 AI 巡检计划

```
# 分页查询全部计划
python scripts/smart_store_inspection.py --session ./session list-plans

# 过滤：按计划名 / 状态（1=运行中 2=暂停中）
python scripts/smart_store_inspection.py --session ./session list-plans --name "离岗" --status 1

# 查看单个计划详情（batch-number 缺省取会话中最后一个计划）
python scripts/smart_store_inspection.py --session ./session plan-detail --batch-number 123456
python scripts/smart_store_inspection.py --session ./session plan-detail --format json

# 启用 / 停用 / 删除
python scripts/smart_store_inspection.py --session ./session start-plan --id 123456
python scripts/smart_store_inspection.py --session ./session stop-plan  --id 123456
python scripts/smart_store_inspection.py --session ./session delete-plan --batch-number 123456

# 编辑：CLI 参数会覆盖已有 detail
python scripts/smart_store_inspection.py --session ./session edit-plan --id 123456 --threshold 0.9
```

`edit-plan` 会先 `aiPatrolDetail/{id}` 拉取当前配置，再用 CLI 参数或 `--from-file` 局部覆盖后重新提交，避免遗漏必填字段。

## 6. 工作流 3：查询 AI 巡检记录

```
# 表格模式：显示前 20 条
python scripts/smart_store_inspection.py --session ./session list-records \
  --begin 2026-09-01 --end 2026-09-28

# JSON 模式：导出全部记录（自动分页翻页，默认最多 20 页 × 50 条 = 1000 条）
python scripts/smart_store_inspection.py --session ./session list-records \
  --begin 2026-09-01 --end 2026-09-28 --format json --max-pages 40 > records.json

# 按设备/算法过滤（多值用逗号分隔）
python scripts/smart_store_inspection.py --session ./session list-records \
  --device-id "186146507762831360,186146507762831361" \
  --algorithm-id "1001,1002"
```

**记录字段**：`releaseTime`（下发时间）、`deviceName`/`deviceId`、`algorithmName`/`algorithmId`、`cloudPictureUrl`（云截图 URL）、`detailData`（AI 详情 JSON 字符串）、`roiParam`（ROI 信息）、`deleteStatus`（设备是否已删除）。

## 7. 工作流 4：生成 HTML 分析报告（推荐）

`patrol-report` 一次性抓取指定区间的全部巡检记录，聚合后生成独立 HTML 报告（数据内联，浏览器打开即用，可直接发给业务方）：

```
# 默认：最近 7 天，输出 ./patrol_report.html
python scripts/smart_store_inspection.py --session ./session patrol-report

# 指定时间范围与输出
python scripts/smart_store_inspection.py --session ./session patrol-report \
  --begin 2026-09-01 --end 2026-09-28 --output ./sept_report.html

# 按设备/算法过滤 + 自定义标题
python scripts/smart_store_inspection.py --session ./session patrol-report \
  --device-id 186146507762831360 --title "XX旗舰店9月AI巡检报告"
```

**报告视图（Tab 切换）**：

| Tab | 内容 |
|-----|------|
| 总览 | KPI 卡片（总记录/含图数/设备数/算法数）+ 每日趋势 SVG 柱状图 + Top 10 设备横向条形图 + 算法分布横向条形图 |
| 抓拍图墙 | 网格化展示 `cloudPictureUrl` 抓拍图，支持设备/算法/关键词过滤，点击图片全屏 Lightbox |
| 按设备 | 每设备记录数明细表 |
| 按算法 | 每算法触发次数明细表 |
| 记录明细 | 完整表格（ID/时间/设备/算法/抓拍图链接/详情） |

图表全部为纯 SVG 内联（不依赖 CDN），生成后将 HTML 文件路径以 `file://` 链接提供给用户。

## 8. 交互式区域画框（includeAreas）

`generate-config-page` 从内置 `assets/config_tool.html` 模板生成独立 HTML，浏览器打开即用：

- 支持在快照上添加**多个多边形**，每个至少 3 个顶点，闭合后计入 `includeAreas`
- 内部按 **8192 × 8192 相对坐标系**归一，原点为画面左上角
- 右侧参数面板可填写 `patrolName / algorithmId / threshold / timeType / timeCycle / detailTime / step / durationTime / mosaic`，导出为 `plan_config.json`
- `patrolRange` 自动填入会话中的 device id
- 导出后：`create-plan --from-file plan_config.json` 或 `edit-plan --from-file plan_config.json`

> **强制约束：** 画框配置页必须由 `generate-config-page` 生成，agent 不得自行创建配置工具或坐标映射逻辑，保证 8192 坐标系与字段结构一致。

## 9. 会话状态（session.json）

会话目录由 `--session` 指定（默认 `./session`），文件 `<session_dir>/session.json`，每次保存自动备份 `session.json.bak`。

```json
{
  "sessionId": "uuid",
  "createdAt": "...", "updatedAt": "...",
  "steps": {
    "store":      { "completed": true, "data": { "id": "...", "nodeId": "...", "storeName": "..." } },
    "device":     { "completed": true, "data": { "id": "...", "deviceSN": "...", "status": 1 } },
    "patrolPlan": { "completed": true, "data": { "batchNumber": "...", "patrolName": "...", "params": { } } }
  }
}
```

自动参数传递：

| 上游步骤 | 传递字段 | 下游步骤 |
|----------|----------|----------|
| store | `nodeId` | add-device |
| store | `id` | edit-store, delete-store |
| device | `id` | create-plan（作为 `patrolRange` 默认值）, delete-device, generate-config-page |
| device | `deviceSN` | snapshot |
| patrolPlan | `batchNumber` | plan-detail, start-plan, stop-plan, delete-plan, edit-plan |

## 10. 常用状态码

| 状态码 | 含义 | 处理建议 |
|--------|------|----------|
| `2000` | 成功 | 正常处理返回数据 |
| `4000` | 参数错误 | 检查 Body 字段与类型（int vs string）、枚举值、`detailTime` 段数与格式 |
| `4007` | timeMillis 过期 | 检查系统时钟；timeMillis 需实时生成 |
| `4009/4013` | 请求频率受限 | 稍等重试；`patrol-report` 已内置 0.2s 分页间隔 |
| `28005` | 签名校验错误 | 核对 `JF_APP_SECRET`、`JF_MOVE_CARD` |
| `28006` | 未找到用户信息 | 检查 `JF_UUID` |
| `28007` | 请求头参数错误 | 检查鉴权请求头完整性 |
| `29001/29010/29011/29012` | 设备已存在 / 未绑定 / 已被其它账户添加 / 达上限 | 按提示处理设备绑定关系 |
| `4116` | Not found（add-device 时） | ① 设备未联网；② 应用未开通智慧巡店/AI算法授权 |
| `5000` | 服务端错误 | 稍后重试或联系技术支持 |

完整状态码见 [references/api-reference.md](references/api-reference.md#常用状态码)。

## 11. 注意事项

1. **AI巡检计划是「一设备一算法一计划」**：同一台设备跑多个算法需要创建多个计划；同一算法跑多台设备也需为每台设备分别建计划。
2. **`detailTime` 严格约束**：最多 5 段，格式 `HH:MM-HH:MM`，段间不允许重合、不允许跨天（如 `22:00-02:00` 非法）。
3. **`threshold` 范围 0.01~0.99**：字符串类型，过低误报多，过高漏报多，建议 0.75~0.9。
4. **`patrolRange` = 设备资源 id**：即 `addJfIpc` 响应的 `model.id`，不是 SN 也不是 nodeId。
5. **`includeAreas`**：JSON 字符串（非对象），格式 `[{"name":"area1","points":[{"X":0-8192,"Y":0-8192},...]}]`；留空即整幅画面。
6. **`mosaic`**：字符串，多值用逗号分隔，可选 `face`（人脸）/`plate`（车牌）/`human`（人体）。
7. **计划状态**：`aiPatrolPageQuery` 的 `param.status` 取值 `1=运行中`、`2=暂停中`。启停用 `aiPatrolStartAndStop`（`openSwitch: 1/0`）。
8. **详情/删除走 POST + 路径参数**：`aiPatrolDelete/{batchNumber}` 与 `aiPatrolDetail/{batchNumber}` 必须用 POST 调用（body 传 `{}`），网关未注册这两个路径的 GET 路由——GET 一律返回 `404 Route Not Found`（2026-10-09 实测），脚本已用 `api_post` 封装。
9. **AI巡检记录 `beginTime` / `endTime` 格式为 `yyyy-MM-dd`**（日期，非日期时间）。
10. **抓拍图片是云端 URL**：`cloudPictureUrl` 直接可访问，无需二次鉴权；HTML 报告用 `<img src>` 引用，离线打开需保证网络可达。
11. **仅支持中国大陆**：Endpoint 固定 `api-cn.jftechws.com`。
12. **计费提示**：智慧巡店按门店数计费（5 店免费+¥25/店/月），AI 算法按算法计费产品单独出账，抓拍产生的媒体流量按 ¥2/G 或带宽套餐计费。
13. **创建/删除设备前先验活**：`create-plan` 若 `patrolRange` 指向已删除的设备资源，后端会返回 `2000` 但 `data` 为空且计划不落库（静默 no-op）。先调 `POST /rtc/device/token`（body `{"sns":["<SN>"]}`）验证设备存活，返回 `29010`（DEV_NOTEXIT）即设备已不在此账号下；`delete-device`/`delete-store` 返回 `4116`（Not found）同样意味着资源早已不存在。

## 12. 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能定义与工作流 |
| `scripts/smart_store_inspection.py` | 主 CLI，覆盖门店/设备/算法/计划/记录/报告全部操作 |
| `scripts/crypto.py` | 杰峰 OpenAPI 签名与时间戳算法实现 |
| `assets/config_tool.html` | 交互式 includeAreas 画框配置工具页模板（多多边形，8192 相对坐标） |
| `assets/patrol_report_template.html` | AI 巡检记录 HTML 分析报告模板（Tab + 抓拍图墙 + 纯 SVG 图表，数据内联） |
| `references/api-reference.md` | 字段级 API 参考：请求/响应字段、算法目录字段、状态码、名词解释 |
