# 智慧巡店 API 字段级参考

所有接口前缀：`https://api-cn.jftechws.com/gwp/v3`。请求头（`uuid`、`appKey`、`timeMillis`、`signature`、`X-Request-Id`、`Content-Type`）由 `scripts/crypto.py` 与主脚本自动生成，业务侧只需关心 Body 与响应字段。

签名算法：`md5(merge_bytes(utf8(uuid+appKey+appSecret+timeMillis), shift(...)))`，`timeMillis` = 7 位计数器 + 13 位毫秒时间戳。

## 目录

- [1. 门店管理](#1-门店管理)
- [2. 设备管理](#2-设备管理)
- [3. AI 巡检算法目录](#3-ai-巡检算法目录)
- [4. AI 巡检计划](#4-ai-巡检计划)
- [5. AI 巡检记录](#5-ai-巡检记录)
- [6. 常用状态码](#常用状态码)
- [7. 名词解释](#名词解释)

---

## 1. 门店管理

### 1.1 创建门店 `POST /rtc/store/create`

**Body**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| storeName | string | 是 | 门店名称 |
| storeAddress | string | 否 | 门店地址 |
| longitude | int/float | 否 | 经度 |
| latitude | int/float | 否 | 纬度 |

**响应 `data.model`**

| 字段 | 说明 |
|------|------|
| id | **门店 id**（后续修改/删除、聚合统计用） |
| nodeId | **节点 id**（`addJfIpc` 必需） |

### 1.2 修改门店 `POST /rtc/store/edit`

Body 需带 `id`（创建门店响应的 id），其余字段与 create 一致。

### 1.3 删除门店 `POST /rtc/store/delete`

Body：`{"id": "<storeId>"}`。删除前须先删门店下的所有设备。

---

## 2. 设备管理

### 2.1 添加设备 `POST /rtc/device/addJfIpc`

**Body**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| nodeId | string | 是 | 创建门店响应的 `nodeId` |
| deviceNetworkType | int | 是 | 0=已配网, 1=未配网 |
| sn | string | 是 | 设备序列号 |
| deviceName | string | 否 | 设备名称 |
| deviceUsername | string | 否 | 设备用户名（默认 admin） |
| devicePassword | string | 否 | 设备密码 |

**响应 `data.model`**

| 字段 | 说明 |
|------|------|
| id | **设备资源 id**（后续 AI 巡检 `patrolRange`、`deviceIdList` 用） |
| name | 设备名称 |
| status | 0=离线, 1=在线, 2=无 |
| accessStatus | 0=未注册, 1=已注册 |
| deviceSN | 序列号 |
| longitude / latitude | 经纬度 |
| sipServer / sipDomain / sipServerNum / serverPortNum | GB28181 相关 |
| accessId / accessIdPwd | 接入 id 与密码 |

### 2.2 删除设备 `POST /rtc/device/delete`

Body：`{"id": "<deviceResourceId>"}`。响应 `data.model` 为 bool。

---

## 3. AI 巡检算法目录

### 3.1 分页查询算法 `POST /rtc/device/aiPatrolAlgorithmPageQuery`

**Body**（PageDTO 结构）

```json
{ "pageSize": 20, "pageNo": 1, "param": { "algorithmName": "客流" } }
```

`param.algorithmName` 为可选模糊过滤。

**响应 `data.model.datas[]` 字段**

| 字段 | 说明 |
|------|------|
| algorithmId | **算法主键**（`create-plan` 时用） |
| algorithmName | 算法名称（如"离岗检测"、"工服检测"、"客流检测"） |
| paramShowSwitch | 参数标签展示开关（位与运算） |
| datasetShowSwitch | 关联库展示开关（位与运算） |
| step | 抽帧频率（默认值） |
| timeInterval | 时间间隔 |
| threshold | 置信度（默认值） |
| excludeAreas | 反向区域 |
| includeAreas | 正向区域 |
| remark | 描述 |
| stepRange | 频率范围（如 "1-30"） |
| minStep / maxStep | 最小/最大频率 |
| durationTime | 持续时长（秒） |
| dedInterval | 批次间隔（秒） |
| analysisCycle | 分析周期（分钟） |
| flowType | 客流模式：0=进过店, 1=进店, 2=过店（仅客流算法有效） |
| deliveryDriversStatus | 外卖员过滤：0=不过滤, 1=过滤 |
| colorCode | 色彩标识 |

---

## 4. AI 巡检计划

### 4.1 新增/编辑 `POST /rtc/device/aiPatrolAddOrEdit`

**Body**（编辑时须带 `id`，其余字段与新增一致；建议先 `aiPatrolDetail/{id}` 拉取当前值再合并覆盖）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 编辑必填 | 计划 id / 批次号 |
| patrolName | string | 是 | 计划名称 |
| timeType | int | 是 | 0=每天, 1=每周, 2=每月 |
| timeCycle | string | 是 | 日="0"；周="1,3,5"（1-7）；月="1,15,28"（1-31）；只传数字，逗号分隔 |
| detailTime | string | 是 | `HH:MM-HH:MM,HH:MM-HH:MM`，**最多 5 段，不允许重合，不允许跨天** |
| patrolRange | string | 是 | **巡检设备资源 id**（`addJfIpc` 响应的 `model.id`） |
| algorithmId | string | 是 | 算法 id（从算法目录获取） |
| threshold | string | 是 | 置信度 `0.01~0.99`（字符串类型） |
| step | int | 否 | 检测频率（抽帧） |
| timeInterval | int | 否 | 时间间隔 |
| includeAreas | string | 否 | 正向区域 JSON 字符串：`[{"name":"area1","points":[{"X":0-8192,"Y":0-8192},...]}]` |
| durationTime | int | 否 | 持续时长（秒） |
| mosaic | string | 否 | 马赛克类型：`face`（人脸）/`plate`（车牌）/`human`（人体），多值逗号分隔 |
| specialParam | string | 否 | 特殊参数（算法专有） |

**约束**

- 一个计划 = **一台设备 × 一个算法**；多算法或多设备需分别建计划。
- `timeType=0` 时 `timeCycle` 固定 `"0"`。
- `includeAreas` 是 **JSON 字符串**（非对象），8192 相对坐标系，原点画面左上角。

### 4.2 分页查询 `POST /rtc/device/aiPatrolPageQuery`

**Body**

```json
{ "pageSize": 20, "pageNo": 1, "param": { "patrolName": "离岗", "status": 1 } }
```

`param.status`：1=运行中, 2=暂停中。

**响应 `data.model.datas[]` 字段**

id / patrolName / timeType / timeCycle / detailTime / patrolRange / deviceName / algorithmId / step / timeInterval / includeAreas / threshold / durationTime / mosaic。

### 4.3 详情 `POST /rtc/device/aiPatrolDetail/{batchNumber}`

Path 参数 `batchNumber` = 计划 id，body 传 `{}`。响应 `data.model` 字段与分页查询一致，另含 `specialParam`。

> ⚠️ 必须用 POST：网关未注册该路径的 GET 路由，GET 一律 404 Route Not Found（2026-10-09 实测）。

### 4.4 启停 `POST /rtc/device/aiPatrolStartAndStop`

Body：`{"id": "<batchNumber>", "openSwitch": 1}`，`openSwitch` 1=启用, 0=停用。响应 `data.model` 为 bool。

### 4.5 删除 `POST /rtc/device/aiPatrolDelete/{batchNumber}`

**POST** 请求（body 传 `{}`），Path 参数即计划批次号。响应 `data.model` 为 bool。删除后不可恢复。

> ⚠️ 必须用 POST：网关未注册该路径的 GET 路由，GET 一律 404 Route Not Found（2026-10-09 实测）。

---

## 5. AI 巡检记录

### 5.1 分页查询 `POST /rtc/device/aiPatrolRecordPageQuery`

**Body**

```json
{
  "pageSize": 50, "pageNo": 1,
  "param": {
    "beginTime": "2026-09-01",
    "endTime":   "2026-09-28",
    "deviceIdList":    ["186146507762831360"],
    "algorithmIdList": ["1001", "1002"]
  }
}
```

- `beginTime` / `endTime` 格式 **`yyyy-MM-dd`**（日期，非日期时间）。
- `deviceIdList` / `algorithmIdList` 为可选数组，多值批量查询。
- 分页：响应 `model.hasNext=true` 时递增 `pageNo` 继续拉取。

**响应 `data.model.datas[]` 字段**

| 字段 | 说明 |
|------|------|
| id | 记录 ID |
| releaseTime | 任务下发时间 `yyyy-MM-dd HH:mm:ss` |
| deviceName | 设备名称 |
| deviceId | 设备资源 id |
| cloudPictureUrl | **云截图全路径**（可直接访问的 HTTPS URL） |
| deleteStatus | 设备是否已删除：1=是, 0=否 |
| algorithmName | 算法名称 |
| algorithmId | 算法 ID |
| detailData | AI 记录详情信息（字符串，通常为 JSON） |
| roiParam | AI 记录消息 ROI 信息 |

---

## 常用状态码

| code | 含义 | 处理建议 |
|------|------|----------|
| 2000 | Success | 正常处理 |
| 4000 | 参数错误 | 检查 Body 字段与类型（int vs string）、枚举值、`detailTime` 段数与格式、`threshold` 范围 |
| 4007 | timeMillis 过期 | 系统时钟偏差或 timeMillis 未实时生成 |
| 4009 / 4013 | 请求频率受限 | 稍等重试；分页调用建议间隔 200~500ms |
| 28005 | 签名校验错误 | 核对 `JF_APP_SECRET`、`JF_MOVE_CARD` |
| 28006 | 未找到用户信息 | 检查 `JF_UUID` |
| 28007 | 请求头参数错误 | 检查 uuid/appKey/timeMillis/signature 完整性 |
| 29001 | 设备已存在 | 该 SN 已被本账号添加 |
| 29010 | 设备未绑定 | 设备未绑定到当前账号 |
| 29011 | 设备已被其它账户添加 | 需先解绑 |
| 29012 | 设备数达上限 | 清理无用设备或申请扩容 |
| 4116 | Not found | add-device 时：① 设备未联网；② 应用未开通智慧巡店/AI算法授权 |
| 5000 | 服务端错误 | 稍后重试或联系技术支持 |

---

## 名词解释

### 巡检方式

| 方式 | 执行端 | 触发方式 |
|------|--------|----------|
| **视频巡检** | PC Web | 巡检计划（视频巡检类）按日/周/月自动生成任务；巡检人远程调取门店监控实时画面，逐点位按考评模板打分 |
| **图片巡检** | PC Web | 抓拍计划按周期+时间点自动抓拍；巡检人对系统抓拍图片逐张评分 |
| **抽查巡检** | PC Web | 管理者即时发起，不走计划 |
| **AI巡检** | 算法自动 | AI巡检计划（算法+门店摄像头+周期）；算法自动识别异常并抓拍留证 |
| **现场巡检** | 移动端 APP | 巡检计划（现场巡检类：门店自检 / 督导巡店）；到店实地拍照打分 |
| **摇一摇巡检** | 移动端 APP | 巡检人到店摇一摇手机即时发起 |

本技能覆盖 **AI巡检** 全流程（算法目录 / 计划 CRUD / 记录查询）。视频巡检、图片巡检、抽查巡检、现场巡检、摇一摇巡检及考评模板、事件中心、事件分析等功能属于蜂云 SaaS 前端页面能力，暂未开放 OpenAPI。

### 考评体系

| 名词 | 说明 |
|------|------|
| 考评模板 | 巡检评分标准依据，由考评类→考评项→分值→合格分数线层级配置而成 |
| 考评类 | 模板下的一级分类（如卫生、服务、安全、门店环境） |
| 考评项 | 模板下的具体检查点 |
| 合格分数线 | 巡检达标的最低分值 |
| 自动留证 | 模板开关；开启后巡检过程可触发自动抓拍 |

### 计划与任务

| 名词 | 说明 |
|------|------|
| 巡检计划 | 周期性自动巡检任务配置，分现场/视频两类模板 |
| AI巡检计划 | 定时任务 + AI 算法 + 门店摄像头，自动巡查 |
| 抓拍计划 | 按周期与时间点自动抓取门店画面，进入图片巡检 |
| 门店自检 | 现场巡检模式之一：任务下发门店，门店人员 APP 自查 |
| 督导巡店 | 现场巡检模式之一：任务指派督导人员到店实地核查 |
| 任务处理时效 | 巡检人收到任务后需完成核查的限定时长（分钟） |
| 抄送人 | 接收任务与巡检结果通知的人员 |

### 记录、分析与事件闭环

| 名词 | 说明 |
|------|------|
| 巡检记录 | 全部巡检结果汇总，分「人工/AI」；含得分/是否合格/是否逾期/巡检方式 |
| 提交事件 | 不合格巡检记录转入事件中心整改闭环的操作入口 |
| 事件中心 | 五个 TAB：我的整改 / 我的验收 / 我的发起 / AI发起 / 抄送我的 |
| 整改 / 验收 / 打回 | 事件闭环三动作 |
| 巡检分析 | 巡检次数、合格率、覆盖率、门店排名、员工排名等 |
| 事件分析 | 事件统计、门店事件排名、事件等级占比等 |
| 验收人 / 整改人 | AI巡检计划中分离设置的两个角色 |

### 计费

| 项 | 计费 |
|----|------|
| 智慧巡店订阅 | 5 店免费，超出 ¥25/店/月，按门店数计费 |
| 杰峰设备接入 | 免费 |
| 三方设备接入 | ¥2/路/月 |
| 媒体流量 / 带宽套餐 | ¥2/G 或带宽档位 |
| AI 算法授权 | 按算法计费产品（AI检测类） |
| 云存储套餐卡 | 按套餐卡规格 |
| 国标北向级联 | ¥1/路/月 |
