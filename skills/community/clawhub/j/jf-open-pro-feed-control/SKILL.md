---
name: jf-open-pro-feed-control
description: 杰峰智能宠物喂食器设备控制技能（开发版）。支持远程一键喂食、设置或查询定时喂食计划，以及配置设备端的宠物检测功能开关。
metadata:
  version: 1.0.0
  author: JFTech
  category: device
  tags:
    - 杰峰
    - 宠物喂食器
    - 智能喂食
    - 定时喂食
    - 宠物检测
    - 一键喂食
  triggers:
    - 查询设备是否支持喂食
    - 一键喂食
    - 远程喂食
    - 定时喂食计划
    - 查询喂食计划
    - 设置喂食计划
    - 宠物检测开关
    - 查询宠物检测
    - 开启宠物检测
    - 关闭宠物检测
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-feed-control - 杰峰智能宠物喂食器设备控制技能（开发版）

## 技能描述

支持杰峰智能宠物喂食器设备的远程控制功能：

- **查询设备是否支持喂食** - 查询设备能力集，确认是否支持喂食功能
- **一键喂食** - 远程发送喂食指令，控制设备出粮
- **定时喂食计划** - 查询和设置设备的定时喂食计划
- **宠物检测** - 查询和设置设备端的宠物检测功能开关

**适用场景：**
- 远程给宠物喂食
- 设置定时自动喂食计划
- 配置宠物检测自动触发喂食

## 触发词

- 查询设备是否支持喂食 / 设备支持喂食吗
- 一键喂食 / 远程喂食 / 手动喂食 / 立即喂食
- 定时喂食计划 / 查询喂食计划 / 设置喂食计划
- 宠物检测开关 / 查询宠物检测 / 开启宠物检测 / 关闭宠物检测

## 前置条件

### 硬件要求

1. **智能宠物喂食器** - 设备需为杰峰智能宠物喂食器

### 必需配置

1. **签名算法** - 使用杰峰官方移位加密算法生成 signature
2. **时间戳算法** - counter(7 位) + timeMillis(13 位)，实时生成
3. **设备绑定** - 设备需先绑定到开放平台账号

### 环境变量

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `JF_UUID` | 开放平台用户 uuid | - | ✅ |
| `JF_APP_KEY` | 开放平台应用 appKey | - | ✅ |
| `JF_APP_SECRET` | 开放平台应用密钥 | - | ✅ |
| `JF_MOVE_CARD` | 移动卡标识（用于签名） | `2` | ✅ |
| `JF_DEVICE_SN` | 设备序列号 | - | ✅ |
| `JF_DEVICE_TOKEN` | 设备接口访问令牌 | - | ✅ |
| `JF_ENDPOINT` | API 接入地址 | `api-cn.jftechws.com` | ❌ |

## API 接口

| 功能 | 地址 | 方法 | 需要 Token | 需要在线 |
|------|------|------|------------|----------|
| 查询设备能力 | `POST /gwp/v3/rtc/device/getability/{token}` | POST | ✅ | ✅ |
| 一键喂食 | `POST /gwp/v3/rtc/device/feeder/{token}` | POST | ✅ | ✅ |
| 查询定时喂食计划 | `POST /gwp/v3/rtc/device/iotPropSet/{token}` | POST | ✅ | ✅ |
| 设置定时喂食计划 | `POST /gwp/v3/rtc/device/iotPropSet/{token}` | POST | ✅ | ✅ |
| 查询宠物检测开关 | `POST /gwp/v3/rtc/device/petDetectionSwitchStatus/{token}` | POST | ✅ | ✅ |
| 设置宠物检测开关 | `POST /gwp/v3/rtc/device/petDetectionSwitchSetting/{token}` | POST | ✅ | ✅ |

## 核心功能

### 1. 查询设备是否支持喂食（FeederAbility）

**API:** `POST /gwp/v3/rtc/device/getability/{deviceToken}`

**Name:** `FeederAbility`

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| `FeedBlockAlarm` | int | 堵粮报警设置开关，`1`=显示，`0`=不显示 |
| `FoodShortageAlarm` | int | 余粮报警设置开关，`1`=显示，`0`=不显示 |
| `BoxNums` | int | 食物餐盘个数。无该字段或值为 `0` 表示老设备，默认为 `1` |
| `FeedSnap` | int | 是否支持喂食时抓图和喂食后延时抓图，`1`=支持，`0`=不支持 |

### 2. 一键喂食（Feed Control）

**API:** `POST /gwp/v3/rtc/device/feeder/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 | 取值 |
|------|------|------|------|------|
| `sn` | string | ✅ | 设备序列号 | - |
| `props` | object | ✅ | 喂食参数 | - |
| `props.feed` | int | ✅ | 喂食份数 | 正整数 |

**请求示例：**
```json
{
  "sn": "device-sn",
  "props": {
    "feed": 1
  }
}
```

### 3. 定时喂食计划（Feed Schedule）

**查询/设置 API:** `POST /gwp/v3/rtc/device/iotPropSet/{deviceToken}`

**查询请求体：**
```json
{
  "sn": "设备序列号",
  "props": ["feedPlan"]
}
```

**设置请求体：**
```json
{
  "sn": "设备序列号",
  "props": {
    "feedPlan": [
      {
        "enable": true,
        "cron": "0 31 10 * * 1,2,3,4,5,6,0",
        "action": {
          "feed": 1
        }
      }
    ]
  }
}
```

**定时计划项（feedPlan）：**

| 字段 | 类型 | 说明 | 取值 |
|------|------|------|------|
| `enable` | boolean | 定时器是否开启 | `true`=启用，`false`=禁用 |
| `cron` | string | cron 时间表达式 | `0 {minute} {hour} * * {weekdays}` |
| `action.feed` | int | 投食份数 | 正整数 |

**操作方法（method）：**

| 方法 | 说明 |
|------|------|
| `Add` | 增加自动喂食时间点 |
| `Modify` | 修改已设定的自动喂食时间点 |
| `Delete` | 删除已设定的自动喂食时间点 |
| `Clear` | 删除全部自动喂食计划 |

### 4. 宠物检测开关（Pet Detection）

**查询 API:** `POST /gwp/v3/rtc/device/petDetectionSwitchStatus/{deviceToken}`

**设置 API:** `POST /gwp/v3/rtc/device/petDetectionSwitchSetting/{deviceToken}`

**查询响应：**
| 字段 | 类型 | 说明 |
|------|------|------|
| `Switch` | string | 开关状态：`ON`=开启，`OFF`=关闭 |
| `Ret` | int | 设备响应状态码 |

**设置请求体：**
```json
{
  "Switch": "ON"
}
```

## 使用示例

### 环境准备

```bash
# 设置环境变量（使用占位符，请替换为实际值）
export JF_UUID="uuidxxxx"
export JF_APP_KEY="appkeyxxxx"
export JF_APP_SECRET="appsecretxxxx"
export JF_MOVE_CARD="5"
export JF_DEVICE_SN="snxxx1"
export JF_DEVICE_TOKEN="NTQ0NzQ3YmE3MXwyYzFk..."
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 查询设备是否支持喂食

```bash
cd ~/.qoderwork/skills/jf-open-pro-feed-control/scripts

python3 feed_control.py --action check-support
```

### 2. 一键喂食

```bash
# 喂食一次（默认 1 份）
python3 feed_control.py --action feed-once

# 喂食 2 份
python3 feed_control.py --action feed-once --portion 2
```

### 3. 定时喂食计划

```bash
# 查询当前定时喂食计划
python3 feed_control.py --action get-schedule

# 设置定时喂食计划（配置文件方式）
python3 feed_control.py --action set-schedule --schedule-file schedule.json

# 快速添加一条计划（每天 8:00 喂食 2 份）
python3 feed_control.py --action add-schedule \
  --hour 8 --minute 0 --portion 2 \
  --repeat "Mon,Tue,Wed,Thu,Fri,Sat,Sun"
```

### 4. 宠物检测

```bash
# 查询宠物检测开关状态
python3 feed_control.py --action get-pet-detect

# 开启宠物检测
python3 feed_control.py --action set-pet-detect --enable true

# 关闭宠物检测
python3 feed_control.py --action set-pet-detect --enable false
```

## 状态码

### 平台状态码

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 28007 | Header 参数错误 | 检查 uuid、appKey、timeMillis、signature |
| 40103 | 无效 Token | deviceToken 过期，重新获取 |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

### 设备状态码（Ret）

| Ret | 说明 |
|-----|------|
| 100 | 成功 |
| 103 | 非法请求（设备不支持该功能） |
| 106 | 用户名或密码错误 |

## 注意事项

1. **设备要求** - 仅智能宠物喂食器设备支持此功能
2. **deviceToken 有效期** - 24 小时，过期需重新获取
3. **设备在线要求** - 所有操作需要设备在线
4. **出粮份数** - 建议在设备支持的最小和最大份数范围内设置
5. **定时计划** - 最多支持 10 条定时计划
6. **重复周期** - 支持按星期重复，使用英文缩写：`Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`, `Sun`

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/feed_control.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
