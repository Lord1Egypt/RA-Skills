# 杰峰精准客流 OpenAPI 参考

本文件为 `jf-store-traffic` 技能的详细 API 参考。SKILL.md 只保留工作流，字段级细节集中在此。

## 目录

1. [通用请求规范](#通用请求规范)
2. [接口清单](#接口清单)
3. [门店接口字段](#门店接口字段)
4. [设备接口字段](#设备接口字段)
5. [精准客流配置字段](#精准客流配置字段)
6. [门店客流聚合统计字段](#门店客流聚合统计字段)
7. [常用状态码](#常用状态码)
8. [区域 Endpoint](#区域-endpoint)
9. [名词解释](#名词解释)

---

## 通用请求规范

- 基础地址：`https://{Endpoint}/gwp/v3`，精准客流当前仅支持中国大陆 `api-cn.jftechws.com`
- 请求方法：全部 POST，`Content-Type: application/json`
- 鉴权请求头（脚本自动计算，无需手动处理）：

| 请求头 | 说明 |
|--------|------|
| uuid | 开放平台用户 uuid |
| appKey | 开放平台应用 appKey |
| timeMillis | 7 位计数器 + 13 位毫秒时间戳，共 20 位；服务器实时校验过期，必须实时生成 |
| signature | uuid+appKey+appSecret+timeMillis 拼接 → 移位算法（moveCard）→ 与原字节数组合并 → MD5 |
| X-Request-Id | 可选，32 位无中划线 UUID，便于链路追踪 |

> **已知文档坑：** 官方「签名算法验证参考示例」表中的期望签名与其输入不自洽（步骤示例中间字符串有缺字笔误），对拍会失败。`scripts/crypto.py` 的实现与已在生产验证的杰峰其它 OpenAPI 技能完全一致，勿因对拍失败而修改算法；以真实 API 调用返回 code=2000 为准。

## 接口清单

| 功能 | 路径（相对 /gwp/v3） | 脚本命令 |
|------|---------------------|----------|
| 创建门店 | `/rtc/store/create` | create-store |
| 修改门店 | `/rtc/store/edit` | edit-store |
| 删除门店 | `/rtc/store/delete` | delete-store |
| 添加客流设备 | `/rtc/device/addJfIpc` | add-device |
| 删除客流设备 | `/rtc/device/delete` | delete-device |
| 精准客流配置 | `/rtc/device/aiCrowdFlowConfig` | config-flow |
| 门店客流聚合统计 | `/rtc/store/flowStatistics` | flow-stats / flow-report |
| 设备在线状态（诊断用，可选） | `/rtc/device/token` + `/rtc/device/status` | device-status |
| 设备绑定（可选，非 addJfIpc 前置） | `/rtc/device/bind` | bind-device |
| 查询设备列表 | `/rtc/device/list` | （无） |

## 门店接口字段

### 创建门店 `/rtc/store/create`

请求 Body：

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| storeName | string | 是 | 门店名称 |
| storeAddress | string | 否 | 门店地址 |
| longitude | int | 否 | 经度 |
| latitude | int | 否 | 纬度 |

响应 `data.model`：`id`（门店 id）、`nodeId`（节点 id）。二者必须保存：修改/删除门店用 `id`，添加设备用 `nodeId`。

### 修改门店 `/rtc/store/edit`

Body：`id`（必须，创建门店返回的 id）+ 与创建门店相同的可选字段（storeName 必须）。

### 删除门店 `/rtc/store/delete`

Body：`id`（必须）。若门店下有设备，建议先删除设备。

## 设备接口字段

### 设备诊断接口（可选，非 addJfIpc 前置）

官方文档中 addJfIpc 仅要求 nodeId / deviceNetworkType / sn，**无绑定前置条件**（实测：设备解绑后调 addJfIpc 仍返回 4116 而非 29010，证明 addJfIpc 不校验账号绑定）。以下接口用于 add-device 失败（4116）时排查设备是否联网：

- **查询在线状态**（脚本命令 `device-status`）：先调 `/rtc/device/token`（Body `{"sns": ["设备序列号", ...]}`，最多 500 个；响应 `data` 直接为数组 `[{"sn": "...", "token": "..."}]`，token 有效期 24 小时），再调 `/rtc/device/status`（Body `{"deviceTokenList": ["token", ...]}`；响应 `data` 为数组 `[{"uuid": "序列号", "status": "online"|"notfound", ...}]`）。`status=notfound` 表示设备未在杰峰云注册上线，**此时 addJfIpc 返回 4116**，需设备通电联网后重试。**注意：** token 接口要求设备已绑定当前账号，未绑定返回 `29010 DEV_NOTEXIT`，故该诊断路径需先 bind-device。
- **绑定设备**（脚本命令 `bind-device`，可选）：`/rtc/device/bind`，Body `{"sn": "设备序列号"}`。响应 `data.model` 含 `id`（形如 `cn6a...`）等绑定信息。绑定与否不影响 addJfIpc 结果；绑定的作用是让 device-status 诊断可用。
- **4116 的两个实测成因：** ① 设备未联网/未在杰峰云注册上线（device-status 显示 notfound）；② 调用应用（appKey）未开通精准客流服务——同一台在线设备，未开通应用返回 4116、已开通应用返回 2000。排查顺序：先确认设备在线，再确认应用授权。
- **设备登录与直播抽帧快照（实测，技能命令 `snapshot`，唯一快照路径）：** HA-5P-GM 不支持 OPSNAP 云抓图（`/rtc/device/capture/{token}` 返回 `Ret=101`，设备状态码 101 = 设备不支持 RESTful API），**不要使用抓图接口**。链路：`/rtc/device/token`（Body `{"sns":[SN]}`，token 有效期 24 小时）→ `/rtc/device/login/{deviceToken}`（token 在路径；Body `{"UserName":"admin","PassWord":""}`，空密码为出厂默认；可选 `KeepaliveTime` 秒，默认保活 5 分钟最长 24 小时）→ 成功 `Ret=100` → `/rtc/device/livestream/{token}`（Body 必须含 `username`/`password`，否则 4000 "username and loginToken is nil"；`channel`/`stream`/`protocol` 如 `"0"/"0"/"flv"`）取主码流 FLV 地址，PyAV 解码保存第 15 帧为 snapshot.jpg（依赖 `pip install av`，无需系统 ffmpeg）。`snapshot` 命令封装全链路（每次自动取新 token），默认输出 `<session>/snapshot.jpg`，可直接交给 `generate-config-page --snapshot`。
- **云端数据全零排查（实测）：** flowStatistics 全零时，临时下发 `showOsdStatus=1` 再抓帧看设备端 OSD 计数（进入/离开/经过）。OSD 有计数而云端零 → 设备端算法与区域正常，卡在设备→云端上报/汇聚延迟（实测：配置生效 30 分钟后设备端 经过:12、云端仍全零，汇聚疑似小时级滞后）；OSD 也无计数 → 新区域下尚无穿越事件（检查录像/画面是否有人走过框）。验证完记得按需恢复 showOsdStatus。
- **解绑设备**：`/rtc/device/unbind/{deviceToken}`，token 置于 URL 路径，Body 传空 JSON `{}`。解绑后 token 接口对该 SN 返回 29010。
- **查询设备列表** `/rtc/device/list`：Body `{"page": 1, "limit": 100}`（注意是 `limit` 不是 `pageSize`）。响应 `data.deviceList`：`[{"id", "sn", "username"}]`。

### 添加客流设备 `/rtc/device/addJfIpc`

请求 Body：

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| nodeId | string | 是 | 创建门店返回的 nodeId |
| deviceNetworkType | string | 是 | 0-设备已配网，1-设备未配网 |
| sn | string | 是 | 设备序列号 |
| deviceName | string | 否 | 设备名称 |
| deviceUsername | string | 否 | 设备用户名（出厂默认 admin，密码为空） |
| devicePassword | string | 否 | 设备密码 |

响应 `data.model`：`id`（设备 id，配置客流规则/删除设备时使用）、`name`、`status`（0-离线 1-在线 2-无）、`accessStatus`（0-未注册 1-已注册）、`deviceSN`、经纬度及 sip 接入信息。

### 删除客流设备 `/rtc/device/delete`

Body：`id`（必须，添加设备返回的设备 id）。响应 `data.model` 为 bool。

## 精准客流配置字段

`/rtc/device/aiCrowdFlowConfig`，所有配置项除 id 外均为非必须（按需下发）：

> **类型坑（实测）：** `flowType`/`openStatus`/`showOsdStatus`/`deliveryDriversStatus` 文档标注为 string，但真实 API 按 int 校验，传字符串返回 4000 "xxx is illegal"（与 addJfIpc 的 `deviceNetworkType` 同款坑）。下发时须传 int；`includeAreas`/`taskTime` 保持 JSON 字符串。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 设备 id（添加设备响应），必须 |
| includeAreas | string | 区域 JSON 字符串。两个框：第一个为店外框（out），第二个为店内框（in）；相对坐标系 8192×8192，原点为画面左上角。格式：`[{"points":[{"X":2119,"Y":3056},{"X":1753,"Y":4995},{"X":4724,"Y":4681},{"X":4200,"Y":2916}],"name":"out"},{"points":[...],"name":"in"}]` |
| flowType | string | 客流模式：0-进过店（进店+过店），1-仅进店，2-仅过店 |
| openStatus | string | 客流算法开关：1-开启，0-关闭 |
| showOsdStatus | string | OSD 叠加：0-关闭，1-开启。画面叠加未去重的进/出/过店数据，每日 24 点清零 |
| deliveryDriversStatus | string | 过滤外卖员：0-不过滤，1-过滤（美团、饿了么、京东、顺丰） |
| taskTime | string | 算法生效时间段 JSON 字符串，支持多段：`[{"start":"08:00:00","end":"16:59:59"}]` |

区域规则：人体框底部中心点相对 IN/OUT 框的位置判断行为。进店=OUT→IN，出店=IN→OUT，过店=仅经过 OUT。

## 门店客流聚合统计字段

`/rtc/store/flowStatistics`

请求 Body：

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| storeId | string | 否 | 门店 id，不传查询全部门店 |
| deviceSn | string | 否 | 设备序列号，不传查询全部设备 |
| startTime | string | 是 | 开始时间 yyyy-MM-dd HH:mm:ss |
| endTime | string | 是 | 结束时间 yyyy-MM-dd HH:mm:ss |

响应 `data.model` 字段：

| 字段 | 含义 |
|------|------|
| sumFlowCount | 总客流 |
| sumInboundCount / sumOutboundCount / sumPassCount | 进店 / 出店 / 过店客流 |
| inboundRate | 进店率（百分比，进店客流/总客流） |
| sumDedInboundCount / sumDedOutboundCount / sumDedPassCount | 进店 / 出店 / 过店去重数 |
| sumRemoveDuplicateFlowCount | 去重总客流 |
| sumRemoveDuplicateInboundCount / OutboundCount / PassCount | 去重后进/出/过店客流（叠加过滤后） |
| sumSingleBatchCount / sumDoubleBatchCount / sumThreeBatchCount / sumManyBatchCount | 单人 / 双人 / 三人 / 多人进店批次数量 |
| sumChildrenCount / sumYoungCount / sumMiddleCount / sumOldCount / sumAgeUnknownCount | 孩童 / 青年 / 中年 / 老年 / 年龄未知数 |
| sumManCount / sumWomanCount / sumGenderUnknownCount | 男 / 女 / 性别未知数 |

多摄像头门店自动按门店维度合并去重；同比、环比、进店率、批次等基于未去重数据统计。

## 常用状态码

| 状态码 | 含义 | 处理建议 |
|--------|------|----------|
| 2000 | 请求成功 | 正常处理 data |
| 4000 | 参数错误 | 检查 Body 字段与格式 |
| 4007 | timeMillis 过期 | 检查系统时钟，时间戳需实时生成 |
| 4009 / 4013 | 请求频率受限 | 等待 60 秒后重试 |
| 28001~28004 | 服务不支持/不可用/过期/次数上限 | 检查开发者账号余额与套餐 |
| 28005 | 签名校验错误 | 核对 appSecret、moveCard 与签名算法 |
| 28006 | 未找到用户信息 | 检查 uuid 是否正确 |
| 28007 | 请求头参数错误 | 检查 uuid/appKey/timeMillis/signature 请求头完整性 |
| 29001 | 设备已存在 | 设备已被添加 |
| 29010 | 用户没有此设备 | 先完成设备绑定 |
| 29011 | 设备已被其它账户添加 | 与原账户解绑 |
| 29012 | 添加设备达到上限（100 个） | 清理无用设备 |
| 4116 | Not found（addJfIpc） | ① 设备未联网/未在杰峰云注册上线（device-status 显示 notfound），需设备通电联网；② 调用应用未开通精准客流服务（换已开通应用即成功）。官方未要求 addJfIpc 前绑定账号 |
| 5000 | 服务器错误 | 稍后重试或联系技术支持 |

完整状态码见官方文档「OPEN API 请求状态码」。

## 区域 Endpoint

| 地区 | RegionCode | Endpoint |
|------|-----------|----------|
| 中国大陆 | AS:CN | api-cn.jftechws.com |
| 泰国 | AS:TH | api-as-th.jftechws.com |
| 亚洲其他/大洋洲/港澳台 | AS | api-as.jftechws.com |
| 欧洲/非洲 | EU | api-eu.jftechws.com |
| 北美 | NA | api-na.jftechws.com |
| 南美 | SA | api-sa.jftechws.com |
| 俄罗斯 | EU:RU | api-ru.jftechws.com |

精准客流产品目前仅支持中国大陆地区销售与接入，固定使用 `api-cn.jftechws.com`。

## 名词解释

| 名词 | 描述 |
|------|------|
| 总客流 | 店铺门口经过的客流加上进入店铺的客流 |
| 进店客流 | 从店外进入店内的客流（含顾客/店员/快递/外卖人次） |
| 出店客流 | 从店内离开到店外的客流 |
| 过店客流 | 店铺门口经过的客流量（不区分方向） |
| 顾客数 | 进店客流去重后的顾客数，可配置去除外卖、快递、店员 |
| 进店率 | 进店客流 / 总客流 × 100% |
| 进店批次 | 同一时间段进店的顾客为一组，时间段可配置，默认 3 秒（范围 2~10 秒） |
| 外卖员过滤 | 支持过滤美团、饿了么、京东、顺丰人员 |
| 客群分析 | 对去重后进店顾客分析年龄段和性别占比 |
