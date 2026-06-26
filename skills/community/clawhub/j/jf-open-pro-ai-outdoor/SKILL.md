---
name: jf-open-pro-ai-outdoor
description: 杰峰开放平台室外安防技能。提供车辆检测、异常告警、智能检测、灵敏度设置、检测区域配置、推送计划管理等功能，全面提升室外安防监控能力。
metadata:
  version: 1.0.0
  author: JFTech
  category: video
  tags:
    - 杰峰
    - 室外安防
    - 车辆检测
    - 异常告警
    - 智能检测
  triggers:
    - 室外安防
    - 车辆管理
    - 异常告警
    - 智能检测
    - 灵敏度设置
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
    - 需开通室外安防 AI 套餐
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-ai-outdoor - 室外安防技能

## 技能描述

杰峰开放平台室外安防技能，提供完整的室外安防监控解决方案。支持车辆检测、异常告警、智能检测、灵敏度设置、检测区域配置、推送计划管理等功能，全面提升室外安防监控能力。

**核心功能模块：**

| 模块 | 功能 | 原技能数量 |
|------|------|------------|
| **服务开关管理** | 查询/开关室外安防服务 | 2 个 |
| **异常提醒配置** | 查询/保存异常提醒配置 | 2 个 |
| **报警记录查询** | 查询报警记录列表 | 1 个 |
| **智能检测配置** | 查询/更新智能检测配置 | 2 个 |
| **灵敏度设置** | 查询/设置设备灵敏度 | 2 个 |
| **检测区域设置** | 查询/设置检测区域 | 2 个 |
| **推送配置管理** | 查询/保存推送配置 | 2 个 |
| **通知计划管理** | 增删改查通知计划 | 4 个 |
| **车辆管理** | 车辆增删改查、车牌识别 | 6 个 |
| **统计分析** | 统计查询、图表数据 | 3 个 |
| **设备认证** | 同步设备登录凭证 | 1 个 |

**合并说明：** 本技能由 28 个独立技能合并而成，提供统一的 API 接口和参数规范。

## 触发词

- 室外安防 / 车辆检测 / 异常告警
- 智能检测 / 灵敏度设置 / 检测区域
- 推送配置 / 通知计划 / 车辆管理

## ⚠️ 环境变量检查（使用前必读）

**使用本技能前，必须先检查以下 7 个必需环境变量是否已配置！**

### 检查清单

| 序号 | 环境变量 | 配置项 | 是否必需 | 检查状态 |
|------|----------|--------|----------|----------|
| 1 | `JF_UUID` | `jf_uuid` | ✅ 必需 | □ 已配置 |
| 2 | `JF_APP_KEY` | `jf_appKey` | ✅ 必需 | □ 已配置 |
| 3 | `JF_APP_SECRET` | `jf_secret` | ✅ 必需 | □ 已配置 |
| 4 | `JF_MOVE_CARD` | `jf_moveCard` | ✅ 必需 | □ 已配置 |
| 5 | `JF_DEVICE_SN` | `jf_device_sn` | ✅ 必需 | □ 已配置 |
| 6 | `JF_AUTHORIZATION` | `jf_authorization` | ✅ 必需 | □ 已配置 |
| 7 | `JF_USER` | `jf_user` | ✅ 必需 | □ 已配置 |

## 前置条件

### 前置条件

1. **设备在线** - 设备需在线且可访问
2. **设备绑定** - 设备需先绑定到开放平台账号
3. **套餐开通** - 需开通相应 AI 套餐 - 需开通室外安防 AI 套餐

签名算法** - 使用杰峰官方 `SignatureUtil.getEncryptStr()` 方法生成 signature
2. **时间戳算法** - 使用杰峰官方 `TimeMillisUtil.getTimMillis()` 方法生成 timeMillis
3. **设备绑定** - 设备需先绑定到开放平台账号

## 环境变量（使用前必须配置）

| 变量名 | 配置项 | 说明 | 默认值 | 必需 |
|--------|------|------|--------|------|
| `JF_UUID` | `jf_uuid` | 开放平台用户 uuid | - | ✅ |
| `JF_APP_KEY` | `jf_appKey` | 开放平台应用 appKey | - | ✅ |
| `JF_APP_SECRET` | `jf_secret` | 开放平台应用密钥 | - | ✅ |
| `JF_MOVE_CARD` | `jf_moveCard` | 移动卡标识（用于签名） | `7` | ✅ |
| `JF_DEVICE_SN` | `jf_device_sn` | 设备序列号 | - | ✅ |
| `JF_AUTHORIZATION` | `jf_authorization` | 用户 token (JWT) | - | ✅ |
| `JF_USER` | `jf_user` | 用户 ID | - | ✅ |
| `JF_ENDPOINT` | - | API 接入地址 | `api-cn.jftechws.com` | ❌ |

## API 接口总览

### 1. 服务开关管理

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询服务状态 | `switch_manager.py --action get` | `/outdoorSecurity/ai/analysis/switch/get` | POST |
| 开关服务 | `switch_manager.py --action change` | `/outdoorSecurity/ai/analysis/switch/change` | POST |

### 2. 异常提醒配置

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询异常配置 | `alarm_config.py --action list` | `/outdoorSecurity/abnormalAlarmConfig/list` | POST |
| 保存异常配置 | `alarm_config.py --action save` | `/outdoorSecurity/abnormalAlarmConfig/save` | POST |

### 3. 报警记录查询

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询报警列表 | `alarm_query.py --action page` | `/child/alarm/page` | POST |

### 4. 智能检测配置

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询智能配置 | `smart_config.py --action list` | `/outdoorSecurity/smartConfig/list` | POST |
| 更新智能配置 | `smart_config.py --action update` | `/outdoorSecurity/smartConfig/update` | POST |

### 5. 灵敏度设置

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询灵敏度 | `sensitivity_manager.py --action get` | `/outdoorSecurity/devInfo/getSensitivity` | POST |
| 设置灵敏度 | `sensitivity_manager.py --action set` | `/outdoorSecurity/devInfo/setSensitivity` | POST |

### 6. 检测区域设置

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询检测区域 | `area_config.py --action get` | `/outdoorSecurity/areaConfig/get` | POST |
| 设置检测区域 | `area_config.py --action update` | `/outdoorSecurity/areaConfig/update` | POST |

### 7. 推送配置管理

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询推送配置 | `push_config.py --action query` | `/outdoorSecurity/pushConfig/query` | POST |
| 保存推送配置 | `push_config.py --action save` | `/outdoorSecurity/pushConfig/save` | POST |

### 8. 通知计划管理

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询通知计划 | `push_plan.py --action query` | `/outdoorSecurity/pushPlan/query` | POST |
| 新增通知计划 | `push_plan.py --action add` | `/outdoorSecurity/pushPlan/add` | POST |
| 更新通知计划 | `push_plan.py --action update` | `/outdoorSecurity/pushPlan/update` | POST |
| 删除通知计划 | `push_plan.py --action delete` | `/outdoorSecurity/pushPlan/delete` | POST |

### 9. 车辆管理

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询车辆列表 | `car_manager.py --action list` | `/outdoorSecurity/car/list` | POST |
| 查询车辆数量 | `car_manager.py --action count` | `/outdoorSecurity/car/count` | POST |
| 添加车辆 | `car_manager.py --action add` | `/outdoorSecurity/car/add` | POST |
| 编辑车辆 | `car_manager.py --action edit` | `/outdoorSecurity/car/edit` | POST |
| 删除车辆 | `car_manager.py --action del` | `/outdoorSecurity/car/del` | POST |
| 车牌识别 | `car_manager.py --action preview` | `/outdoorSecurity/car/preview` | POST |

### 10. 统计分析

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 查询统计次数 | `stats_query.py --action count` | `/outdoorSecurity/static/count` | POST |
| 查询当日图表 | `stats_query.py --action day-chart` | `/outdoorSecurity/static/dayDataChart` | POST |
| 查询周图表 | `stats_query.py --action week-chart` | `/outdoorSecurity/static/weekDataChart` | POST |

### 11. 设备认证

| 功能 | 脚本 | API 路径 | 方法 |
|------|------|---------|------|
| 同步设备凭证 | `device_auth.py --action save` | `/outdoorSecurity/devInfo/save` | POST |

## 核心功能详解

### 1. 服务开关管理

**查询服务状态：** `POST /outdoorSecurity/ai/analysis/switch/get`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| sn | string | ✅ | 设备序列号 |
| user | string | ✅ | 用户 ID |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 平台状态码（2000=成功） |
| data.aiAnalysisSwitch | boolean | 服务开启状态（true=开启） |

**开关服务：** `POST /outdoorSecurity/ai/analysis/switch/change`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| sn | string | ✅ | 设备序列号 |
| user | string | ✅ | 用户 ID |
| aiAnalysisSwitch | boolean | ✅ | true 开启，false 关闭 |

### 2. 异常提醒配置

**异常类型枚举：**
| 枚举值 | 说明 |
|--------|------|
| `HumanDetect` | 人形检测 |
| `VehicleDetect` | 车辆检测 |
| `IntrusionAlarm` | 入侵报警 |
| `LoiteringAlarm` | 徘徊报警 |
| `AudioAlarm` | 声音报警 |

**查询异常配置：** `POST /outdoorSecurity/abnormalAlarmConfig/list`

**保存异常配置：** `POST /outdoorSecurity/abnormalAlarmConfig/save`

### 3. 报警记录查询

**查询报警列表：** `POST /child/alarm/page`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| sn | string | ✅ | 设备序列号 |
| user | string | ✅ | 用户 ID |
| startTime | string | ✅ | 开始时间（秒值） |
| endTime | string | ✅ | 结束时间（秒值） |
| msgType | string | ❌ | 异常类型 |
| page | integer | ✅ | 页码 |
| rows | integer | ✅ | 每页条数 |

### 4. 智能检测配置

**智能检测类型：**
| 枚举值 | 说明 |
|--------|------|
| `HumanDetect` | 人形检测 |
| `VehicleDetect` | 车辆检测 |
| `IntrusionDetect` | 入侵检测 |
| `LoiteringDetect` | 徘徊检测 |

**查询智能配置：** `POST /outdoorSecurity/smartConfig/list`

**更新智能配置：** `POST /outdoorSecurity/smartConfig/update`

### 5. 灵敏度设置

**灵敏度范围：** 1-10（1=最低，10=最高）

**查询灵敏度：** `POST /outdoorSecurity/devInfo/getSensitivity`

**设置灵敏度：** `POST /outdoorSecurity/devInfo/setSensitivity`

### 6. 检测区域设置

**检测区域格式：** JSON 数组，包含多边形坐标点

**查询检测区域：** `POST /outdoorSecurity/areaConfig/get`

**设置检测区域：** `POST /outdoorSecurity/areaConfig/update`

### 7. 推送配置管理

**推送模式：**
| 枚举值 | 说明 |
|--------|------|
| `RealTime` | 实时推送 |
| `Scheduled` | 定时推送 |
| `Disabled` | 禁用推送 |

**查询推送配置：** `POST /outdoorSecurity/pushConfig/query`

**保存推送配置：** `POST /outdoorSecurity/pushConfig/save`

### 8. 通知计划管理

**查询通知计划：** `POST /outdoorSecurity/pushPlan/query`

**新增通知计划：** `POST /outdoorSecurity/pushPlan/add`

**更新通知计划：** `POST /outdoorSecurity/pushPlan/update`

**删除通知计划：** `POST /outdoorSecurity/pushPlan/delete`

### 9. 车辆管理

**查询车辆列表：** `POST /outdoorSecurity/car/list`

**添加车辆：** `POST /outdoorSecurity/car/add`

**编辑车辆：** `POST /outdoorSecurity/car/edit`

**删除车辆：** `POST /outdoorSecurity/car/del`

**车牌识别：** `POST /outdoorSecurity/car/preview`

### 10. 统计分析

**查询统计次数：** `POST /outdoorSecurity/static/count`

**查询当日图表：** `POST /outdoorSecurity/static/dayDataChart`

**查询周图表：** `POST /outdoorSecurity/static/weekDataChart`

### 11. 设备认证

**同步设备凭证：** `POST /outdoorSecurity/devInfo/save`

## 使用示例

### 环境准备

```bash
# 设置环境变量
export JF_UUID="<your-uuid>"
export JF_APP_KEY="<your-appkey>"
export JF_APP_SECRET="<your-secret>"
export JF_MOVE_CARD="7"
export JF_DEVICE_SN="<your-device-sn>"
export JF_AUTHORIZATION="eyJhbGciOiJIUzI1NiIs..."
export JF_USER="<your-uuid>"
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 查询服务状态

```bash
cd /root/.openclaw/workspace/skills/aiscene/jf-open-pro-ai-outdoor/scripts

# 查询室外安防服务状态
python3 switch_manager.py --action get \
  --sn "<your-device-sn>" \
  --user "<your-uuid>" \
  --uuid "<your-uuid>" \
  --appkey "<your-appkey>" \
  --secret "<your-secret>" \
  --auth "<your-uuid>" \
  --movecard 7
```

### 2. 开关服务

```bash
# 开启室外安防服务
python3 switch_manager.py --action change --enable true \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 关闭室外安防服务
python3 switch_manager.py --action change --enable false \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 3. 查询异常提醒配置

```bash
python3 alarm_config.py --action list \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 4. 查询报警记录

```bash
# 查询最近 7 天的报警记录
python3 alarm_query.py --action page \
  --start-time 1733241600 --end-time 1733846399 \
  --page 1 --rows 10 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 5. 车辆管理

```bash
# 查询车辆列表
python3 car_manager.py --action list \
  --user "<your-uuid>"

# 添加车辆
python3 car_manager.py --action add \
  --plate-number "浙 A12345" \
  --color "黑色" \
  --type "小型车" \
  --user "<your-uuid>"
```

### 6. 查询统计数据

```bash
# 查询统计次数
python3 stats_query.py --action count \
  --start-time 1733241600 --end-time 1733327999 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 查询当日图表
python3 stats_query.py --action day-chart \
  --start-time 1733241600 --end-time 1733327999 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

## 状态码

### 平台状态码

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 28007 | Header 参数错误 | 检查 uuid、appKey、timeMillis、signature |
| 40103 | 无效 Token | authorization 过期，重新获取 |
| 12504 | 授权失败 - 设备未开通套餐 | 登录开放平台为设备绑定室外安防套餐卡 |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

### 错误码 12504 详细处理步骤

**错误信息：** `authorize failed,Please check it in the open platform`

**原因：** 设备未开通室外安防服务，或未绑定套餐卡

**解决步骤：**

1. 登录杰峰开放平台：https://developer.jftech.com
2. 进入 **套餐管理** / **服务管理**
3. 找到 **室外安防** 套餐
4. 为设备购买并绑定套餐卡
5. 等待配置生效（通常 1-5 分钟）
6. 重新调用 API 测试

## 注意事项

1. **时间格式** - 通知计划时间格式为 `HH:mm:ss`
2. **工作日枚举** - 1=周一，2=周二，...，7=周日
3. **时间戳** - 统计查询使用秒级时间戳
4. **套餐开通** - 使用前需确保设备已开通室外安防套餐
5. **Token 有效期** - authorization 需在有效期内
6. **签名算法** - 使用杰峰官方移位加密算法
7. **灵敏度范围** - 1-10，1=最低灵敏度，10=最高灵敏度

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/switch_manager.py` | 服务开关管理脚本 |
| `scripts/alarm_config.py` | 异常提醒配置脚本 |
| `scripts/alarm_query.py` | 报警记录查询脚本 |
| `scripts/smart_config.py` | 智能检测配置脚本 |
| `scripts/sensitivity_manager.py` | 灵敏度设置脚本 |
| `scripts/area_config.py` | 检测区域设置脚本 |
| `scripts/push_config.py` | 推送配置管理脚本 |
| `scripts/push_plan.py` | 通知计划管理脚本 |
| `scripts/car_manager.py` | 车辆管理脚本 |
| `scripts/stats_query.py` | 统计分析脚本 |
| `scripts/device_auth.py` | 设备认证脚本 |
| `scripts/jf_signature.py` | 签名算法工具（符号链接） |
| `references/outdoor-api.md` | API 参考文档 |

## 参考文档

- [杰峰开放平台](https://developer.jftech.com)
- [签名算法](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh)
- [时间戳算法](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh)
- [室外安防 API 文档](https://docs.jftech.com/)

---

# 📋 前置配置文档（环境变量缺失时参考）

> **⚠️ 重要提示：** 如果在使用本技能时发现缺少必需的环境变量，请先完成以下配置步骤，然后再继续操作。

## 必需环境变量清单

以下 **7 个环境变量** 必须全部配置，缺一不可：

| # | 变量名 | 配置项 | 说明 |
|---|--------|--------|------|
| 1 | `JF_UUID` | `jf_uuid` | 开放平台用户 uuid |
| 2 | `JF_APP_KEY` | `jf_appKey` | 开放平台应用 appKey |
| 3 | `JF_APP_SECRET` | `jf_secret` | 开放平台应用密钥 |
| 4 | `JF_MOVE_CARD` | `jf_moveCard` | 移动卡标识（用于签名） |
| 5 | `JF_DEVICE_SN` | `jf_device_sn` | 设备序列号 |
| 6 | `JF_AUTHORIZATION` | `jf_authorization` | 用户 token (JWT) |
| 7 | `JF_USER` | `jf_user` | 用户 ID |

---

## 参数获取指南

### 1. JF_UUID（jf_uuid）

**获取方式：**
- 登录杰峰开放平台：https://developer.jftech.com
- 进入 **个人中心** 或 **开发者信息**
- 复制您的用户 UUID

**说明：** 这是您在杰峰开放平台的唯一用户标识

---

### 2. JF_APP_KEY（jf_appKey）

**获取方式：**
- 登录杰峰开放平台：https://developer.jftech.com
- 进入 **应用管理** → **我的应用**
- 选择或创建一个应用
- 复制应用的 `appKey`

**说明：** 这是您创建的应用的唯一标识

---

### 3. JF_APP_SECRET（jf_secret）

**获取方式：**
- 登录杰峰开放平台：https://developer.jftech.com
- 进入 **应用管理** → **我的应用**
- 选择对应的应用
- 查看应用详情，复制 `secret` 密钥

**说明：** 这是应用的密钥，用于 API 签名，请妥善保管

---

### 4. JF_MOVE_CARD（jf_moveCard）

**获取方式：**
- **方式一：** 通过 appKey 查询接口获取并缓存（24 小时有效）
- **方式二：** 登录杰峰开放平台，进入应用详情页查看

**说明：** 移动卡标识，用于签名算法生成

---

### 5. JF_DEVICE_SN（jf_device_sn）

**获取方式：**
- 查看设备底部标签或包装盒上的序列号
- 或在杰峰开放平台 **设备管理** 中查看已绑定的设备

**说明：** 设备的唯一序列号，格式通常为 16 位十六进制字符串

---

### 6. JF_AUTHORIZATION（jf_authorization）⭐

**获取方式（二选一）：**

#### 方式 A：使用杰峰用户系统
> 请参考 **用户登录接口** 获取 Authorization 值
> 
> 调用登录接口后，从响应中提取 `authorization` 字段（JWT Token）

#### 方式 B：使用开发者自己的用户系统
> 传值参考 **套餐卡使用说明** 中的 `userId`
> 
> 将您的用户系统生成的 userId 作为 authorization 值传入

**说明：** 用户鉴权 Token，用于 API 请求的身份验证

---

### 7. JF_USER（jf_user）

**获取方式：**
- 与 `JF_UUID` 通常相同
- 或在杰峰开放平台 **个人中心** 查看用户 ID

**说明：** 用户 ID，用于 API 请求中标识当前用户

---

## 配置示例

完成上述参数获取后，在您的环境中设置：

```bash
# 设置环境变量（请替换为您的实际值）
export JF_UUID="your-uuid-here"
export JF_APP_KEY="your-appkey-here"
export JF_APP_SECRET="your-secret-here"
export JF_MOVE_CARD="your-movecard-here"
export JF_DEVICE_SN="your-device-sn-here"
export JF_AUTHORIZATION="your-authorization-token-here"
export JF_USER="your-user-id-here"
export JF_ENDPOINT="api-cn.jftechws.com"  # 可选，默认值
```

---

## 验证配置

配置完成后，可以先调用一个简单的接口验证配置是否正确：

```bash
# 查询服务状态（验证配置）
python3 switch_manager.py --action get \
  --sn "$JF_DEVICE_SN" \
  --user "$JF_USER"
```

如果返回 `code: 2000`，说明配置成功！

---

## 重要提醒

> **使用原则：** 后续所有 API 调用，必须严格使用用户环境变量中配置的参数值，**不允许**技能自己发散去获取或推算参数！
> 
> 这样可以确保：
> - 参数来源可控、可追溯
> - 避免使用错误的或过期的凭证
> - 符合安全和审计要求
