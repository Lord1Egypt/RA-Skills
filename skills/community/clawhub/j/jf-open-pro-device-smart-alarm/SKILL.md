---
name: jf-open-pro-device-smart-alarm
description: 杰峰设备智能报警技能（开发版）。支持设备能力集查询、智能报警开关设置、报警时间段配置、报警消息列表及图片获取等功能。
metadata:
  version: 1.0.0
  author: JFTech
  category: alarm
  tags:
    - 杰峰
    - 智能报警
    - 移动侦测
    - 报警配置
    - 报警消息
    - 报警图片
  triggers:
    - 查询报警配置
    - 设置报警开关
    - 开启报警
    - 关闭报警
    - 设置报警时间段
    - 查询报警消息
    - 获取报警图片
    - 报警列表
    - 移动侦测配置
    - 查询设备能力集
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
---

# jf-open-pro-device-smart-alarm - 杰峰设备智能报警技能（开发版）

## 技能描述

支持杰峰设备的智能报警管理功能，包括：
- 设备能力集查询（检查是否支持移动侦测/人体检测）
- 智能报警开关设置（开启/关闭移动侦测报警）
- 手机上报开关设置（MessageEnable）
- 报警时间段配置（支持全天 24 小时或自定义多个时间段）
- 报警消息列表查询
- 报警图片获取

## 触发词

- 查询报警配置 / 设置报警开关 / 开启报警 / 关闭报警
- 设置报警时间段 / 查询报警消息 / 获取报警图片
- 报警列表 / 移动侦测配置 / 查询设备能力集

## 前置条件

### 必需配置

1. **签名算法**：使用杰峰官方移位加密算法生成 signature
2. **时间戳算法**：counter(7 位) + timeMillis(13 位)，实时生成
3. **AES 加密算法**：用于敏感数据加密

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `JF_UUID` | 开放平台用户 uuid | 必需 |
| `JF_APP_KEY` | 开放平台应用 appKey | 必需 |
| `JF_APP_SECRET` | 开放平台应用密钥 | 必需 |
| `JF_MOVE_CARD` | 移动卡标识（用于签名） | `2` |
| `JF_DEVICE_SN` | 设备序列号 | 必需 |
| `JF_DEVICE_USERNAME` | 设备用户名 | `admin` |
| `JF_DEVICE_PASSWORD` | 设备密码 | 必需 |
| `JF_DEVICE_TOKEN` | 设备接口访问令牌 | 可选（自动获取） |
| `JF_ENDPOINT` | API 接入地址（Region） | `api-cn.jftechws.com` |

## 接入地址（Endpoint）

| 地区 | 编码 | 地址 |
|------|------|------|
| 中国 | CN | `api-cn.jftechws.com` |
| 亚洲 | AS | `api-as.jftechws.com` |
| 欧洲 | EU | `api-eu.jftechws.com` |
| 北美洲 | NA | `api-na.jftechws.com` |
| 南美洲 | SA | `api-sa.jftechws.com` |
| 俄罗斯 | RU | `api-ru.jftechws.com` |
| 非洲 | AF | `api-af.jftechws.com` |
| 大洋洲 | OC | `api-oc.jftechws.com` |

## 功能说明

### 1. 设备状态检查

**说明：** 执行后续功能前，先检查设备是否在线

**API:** `GET /gwp/v3/rtc/device/status`

**前置条件：** 需要 Authorization Token

### 2. 设备登录

**说明：** 登录成功后获取 deviceToken，用于后续设备配置操作

**API:** `POST /gwp/v3/rtc/device/login`

**返回：** deviceToken（设备接口访问令牌）

### 3. 查询设备能力集

**说明：** 检查设备是否支持智能报警功能

**API:** `POST /gwp/v3/rtc/device/getability`

**判断条件：** 
- `AlarmFunction.MotionDetect` 为 `true`，或
- `AlarmFunction.HumanDetection` 为 `true`

满足任一条件即表示设备支持智能报警。

### 4. 智能报警开关设置

**说明：** 开启/关闭移动侦测报警

**API:** 
- 获取配置：`POST /gwp/v3/rtc/device/getconfig/{deviceToken}`
- 设置配置：`POST /gwp/v3/rtc/device/setconfig/{deviceToken}`

**判断条件：** `Detect.MotionDetect.Enable` 为 `true` 表示开启

### 5. 手机上报开关设置

**说明：** 设置报警是否推送手机通知

**配置路径：** `Detect.MotionDetect.EventHandler.MessageEnable`

**判断条件：** `MessageEnable` 为 `true` 表示开启手机上报

### 6. 报警时间段设置

**说明：** 配置报警生效的时间段

**配置路径：** `Detect.MotionDetect.EventHandler.TimeSection`

**格式说明：**
- TimeSection 是二维数组，包含 7 个数组
- 按顺序分别表示：周日、周一、周二、周三、周四、周五、周六
- 每个子数组包含 6 个时间段字符串
- 格式：`"有效标志 开始时间 - 结束时间"`
  - `1` 表示该时间段有效
  - `0` 表示该时间段无效

**示例：**
```json
"TimeSection": [
  // 周日：0:00-24:00 全天报警
  ["1 00:00:00-24:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00"],
  // 周一：0:00-10:00 和 10:00-19:00 报警
  ["1 00:00:00-10:00:00", "0 10:00:00-19:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00"],
  // 周二：0:00-11:00、11:00-12:00、12:00-13:00 报警
  ["1 00:00:00-11:00:00", "0 11:00:00-12:00:00", "0 12:00:00-13:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00"],
  // 周三到周六：全天报警
  ["1 00:00:00-24:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00"],
  ["1 00:00:00-24:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00"],
  ["1 00:00:00-24:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00"],
  ["1 00:00:00-24:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00", "0 00:00:00-00:00:00"]
]
```

### 7. 获取报警消息列表

**说明：** 查询设备云存报警消息列表

**API:** `POST /gwp/v3/rtc/device/getDeviceAlarmList/{deviceToken}`

**注意：** 此功能**不需要设备在线**，**不需要设备登录**

**参数：**
- `startTime`: 开始时间（yyyy-MM-dd HH:mm:ss）
- `endTime`: 结束时间（yyyy-MM-dd HH:mm:ss）
- `pageNum`: 页数
- `pageSize`: 每页数量（1-100）
- `alarmEvent`: 报警类型（可选）

### 8. 获取报警图片

**说明：** 获取报警消息对应的图片 URL

**API:** `POST /gwp/v3/rtc/device/getPicUrl/{deviceToken}`

**注意：** 此功能**不需要设备在线**，**不需要设备登录**

**查询场景：**
1. **精确查询**：通过 alarmIds 直接获取指定报警的图片
2. **条件查询**：根据时间范围查询该时间段内所有报警图片
3. **组合查询**：时间范围 + 报警类型筛选

**图片有效期：** 24 小时

## API 接口汇总

| 功能 | 地址 | 方法 | 需要登录 | 需要在线 |
|------|------|------|----------|----------|
| 设备状态 | `GET /gwp/v3/rtc/device/status` | GET | ✅ | ✅ |
| 设备登录 | `POST /gwp/v3/rtc/device/login` | POST | - | ✅ |
| 能力集查询 | `POST /gwp/v3/rtc/device/getability` | POST | ✅ | ✅ |
| 获取配置 | `POST /gwp/v3/rtc/device/getconfig/{token}` | POST | ✅ | ✅ |
| 设置配置 | `POST /gwp/v3/rtc/device/setconfig/{token}` | POST | ✅ | ✅ |
| 报警列表 | `POST /gwp/v3/rtc/device/getDeviceAlarmList/{token}` | POST | ❌ | ❌ |
| 报警图片 | `POST /gwp/v3/rtc/device/getPicUrl/{token}` | POST | ❌ | ❌ |

## 使用示例

### 1. 查询设备能力集

```bash
export JF_UUID="uuidxxxx"
export JF_APP_KEY="appkeyxxxx"
export JF_APP_SECRET="appsecretxxxx"
export JF_DEVICE_SN="2e87cdb6381cxxxx"
export JF_DEVICE_USERNAME="admin"
export JF_DEVICE_PASSWORD="***"

python scripts/smart_alarm.py --action get-ability
```

### 2. 查询报警配置

```bash
python scripts/smart_alarm.py --action get-config
```

### 3. 开启/关闭报警开关

```bash
# 开启报警
python scripts/smart_alarm.py --action set-switch --enable true

# 关闭报警
python scripts/smart_alarm.py --action set-switch --enable false
```

### 4. 设置手机上报开关

```bash
# 开启手机上报
python scripts/smart_alarm.py --action set-message-notify --enable true

# 关闭手机上报
python scripts/smart_alarm.py --action set-message-notify --enable false
```

### 5. 设置报警时间段

```bash
# 设置全天 24 小时报警
python scripts/smart_alarm.py --action set-time-section --schedule all-day

# 设置自定义时间段（周一到周五 9:00-18:00）
python scripts/smart_alarm.py --action set-time-section --days 1,2,3,4,5 --start 09:00:00 --end 18:00:00
```

### 6. 查询报警消息列表

```bash
# 查询今日报警消息
python scripts/smart_alarm.py --action get-alarm-list --start "2026-05-07 00:00:00" --end "2026-05-07 23:59:59"

# 查询指定报警类型（人体检测）
python scripts/smart_alarm.py --action get-alarm-list --event appEventHumanDetectAlarm
```

### 7. 获取报警图片

```bash
# 根据报警 ID 获取图片
python scripts/smart_alarm.py --action get-alarm-pic --alarm-ids 229991742,229991238

# 根据时间段获取图片
python scripts/smart_alarm.py --action get-alarm-pic --start "2026-05-07 00:00:00" --end "2026-05-07 23:59:59"
```

## 报警类型

| 报警事件 | 说明 |
|----------|------|
| `appEventHumanDetectAlarm` | 人体检测报警 |
| `appEventVehicleDetectAlarm` | 车辆检测报警 |
| `appEventPetDetectAlarm` | 宠物检测报警 |
| `Thirdpart` | 自定义报警消息类型 |

## 注意事项

1. **设备登录**：配置类操作（getconfig/setconfig）需要先登录设备获取 deviceToken
2. **设备在线**：配置类操作需要设备在线才能生效
3. **报警查询**：获取报警消息列表和图片不需要设备在线或登录
4. **签名算法**：使用杰峰官方移位加密算法生成 signature
5. **时间戳**：counter(7 位) + timeMillis(13 位)，需实时生成，服务器会校验过期
6. **图片有效期**：获取的报警图片 URL 有效期为 24 小时
7. **时间段格式**：TimeSection 是二维数组，按顺序表示周日到周六

## 错误处理

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 40103 | 无效 Token | 检查 deviceToken 是否有效，重新登录 |
| 40104 | 无效 appKey | 检查 appKey 配置 |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

## 相关文件

- `scripts/smart_alarm.py` - Python 执行脚本
- `scripts/crypto.py` - 签名/时间戳/加密工具
