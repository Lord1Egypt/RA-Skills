---
name: jf-open-pro-device-battery-manage
description: 杰峰低功耗设备电池管理技能（开发版）。支持查询低电量阈值范围、设置低电量模式阈值等电池管理功能。
metadata:
  version: 1.4.0
  author: JFTech
  category: device
  tags:
    - 杰峰
    - 低功耗设备
    - 电池管理
    - 低电量模式
    - 电量阈值
  triggers:
    - 查询低电量阈值
    - 设置低电量阈值
    - 低电量模式
    - 电池管理
    - 电量配置
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-device-battery-manage - 杰峰低功耗设备电池管理技能（开发版）

## 技能描述

支持杰峰低功耗设备的电池管理功能：

- **查询低电量阈值范围** - 获取设备支持的电量阈值最小值和最大值
- **设置低电量阈值** - 配置设备自动进入低电量模式的电量阈值

**适用场景：** 低功耗电池设备、太阳能供电设备等

## 触发词

- 查询低电量阈值 / 设置低电量阈值
- 低电量模式 / 电池管理 / 电量配置

## 前置条件

### 硬件要求

1. **低功耗设备** - 设备需支持低功耗功能（电池设备/太阳能供电设备）

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

| 功能 | 地址 | 方法 |
|------|------|------|
| 获取低电量阈值范围 | `POST /gwp/v3/rtc/device/getconfig/{token}` | POST |
| 设置低电量阈值 | `POST /gwp/v3/rtc/device/setconfig/{token}` | POST |

## 核心功能

### 1. 获取低电量阈值范围（Ability.AovAbility）

**API:** `POST /gwp/v3/rtc/device/getconfig/{deviceToken}`

**Name:** `Ability.AovAbility`

**说明:** 查询设备支持的阈值范围（**只返回** LowElectrMin 和 LowElectrMax）

**响应参数：**
| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| LowElectrMin | int | 最小电量阈值（%） | `Ability.AovAbility.LowElectrMin` |
| LowElectrMax | int | 最大电量阈值（%） | `Ability.AovAbility.LowElectrMax` |

**响应示例:**
```json
{
  "code": 2000,
  "data": {
    "Ability.AovAbility": {
      "LowElectrMin": 10,
      "LowElectrMax": 40
    },
    "Name": "Ability.AovAbility",
    "Ret": 100
  }
}
```

> 💡 **注意:** `Ability.AovAbility` 也返回 `LowElectrThreshold` 字段，但**不使用**该字段。当前生效的阈值从 `Dev.LowElectrMode.PowerThreshold` 获取。

### 2. 查询当前低电量阈值（Dev.LowElectrMode）

**API:** `POST /gwp/v3/rtc/device/getconfig/{deviceToken}`

**Name:** `Dev.LowElectrMode`

**说明:** 查询当前**已生效**的低电量阈值

**响应参数：**
| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| PowerThreshold | int | 当前低电量阈值（%） | `Dev.LowElectrMode.PowerThreshold` |

**响应示例:**
```json
{
  "code": 2000,
  "data": {
    "Dev.LowElectrMode": {
      "PowerThreshold": 20
    },
    "Name": "Dev.LowElectrMode",
    "Ret": 100
  }
}
```

### 3. 设置低电量阈值（Dev.LowElectrMode）

**API:** `POST /gwp/v3/rtc/device/setconfig/{deviceToken}`

**Name:** `Dev.LowElectrMode`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| PowerThreshold | int | ✅ | 自动进入低电量模式的电量阈值（%） |

**请求示例：**
```json
{
  "Name": "Dev.LowElectrMode",
  "Dev.LowElectrMode": {
    "PowerThreshold": 20
  }
}
```

**官方文档:**
- [获取低电量阈值取值范围配置](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=9bf993f3140ad9f9b4390fee750ba740&lang=zh)
- [设置低电量阈值配置](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=b246b44faa8c4d41a3f10e3de95b892a&lang=zh)

---

### 📊 API 使用规范

| 功能 | API Name | 字段 | 用途 |
|------|----------|------|------|
| **查询范围** | `Ability.AovAbility` | `LowElectrMin`, `LowElectrMax` | 获取阈值的最小/最大值 |
| **查询当前值** | `Dev.LowElectrMode` | `PowerThreshold` | 获取已生效的阈值 |
| **设置阈值** | `Dev.LowElectrMode` | `PowerThreshold` | 设置新阈值 |

### 4. 获取范围 + 设置阈值（组合操作）

**推荐流程：** 先获取设备支持的阈值范围，查询当前值，验证后设置新阈值

```bash
# 一步完成：查询范围 + 查询当前值 + 设置阈值（自动验证）
python3 battery_manage.py --action get-and-set --threshold 20
```

**执行流程：**
1. 获取阈值范围（使用 `Ability.AovAbility`）
2. 查询当前阈值（使用 `Dev.LowElectrMode`）
3. 验证输入阈值是否在范围内
4. 设置新阈值（使用 `Dev.LowElectrMode`）

## 使用示例

### 环境准备

```bash
# 设置环境变量（使用占位符，请替换为实际值）
export JF_UUID="uuidxxxx"
export JF_APP_KEY="appkeyxxxx"
export JF_APP_SECRET="appsecretxxxx"
export JF_MOVE_CARD="2"
export JF_DEVICE_SN="devicesnxxxx"
export JF_DEVICE_TOKEN="devicetokenxxxx"
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 查询低电量阈值范围

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-device-battery-manage/scripts

# 查询设备支持的电量阈值范围
python3 battery_manage.py --action get-range
```

### 2. 设置低电量阈值

```bash
# 设置低电量阈值为 15%
python3 battery_manage.py --action set-threshold --threshold 15

# 设置低电量阈值为 20%
python3 battery_manage.py --action set-threshold --threshold 20
```

### 3. 查询并设置（推荐流程）

```bash
# 方式一：分步执行
python3 battery_manage.py --action get-range
python3 battery_manage.py --action set-threshold --threshold 15

# 方式二：一步完成（推荐）- 自动获取范围并验证
python3 battery_manage.py --action get-and-set --threshold 15
```

## 参数说明

### 电量阈值（LowElectrThreshold）

| 参数 | 取值范围 | 说明 |
|------|----------|------|
| LowElectrThreshold | LowElectrMin ~ LowElectrMax | 自动进入低电量模式的电量百分比 |

**示例：**
- 如果 LowElectrMin=10，LowElectrMax=30
- 则 LowElectrThreshold 可设置为 10-30 之间的任意值
- 当设备电量低于设定值时，自动进入低电量模式

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

## 注意事项

1. **设备支持** - 仅低功耗电池设备/太阳能供电设备支持此功能
2. **阈值范围** - 设置的阈值必须在设备支持的范围内（LowElectrMin ~ LowElectrMax）
3. **低电量模式** - 进入低电量模式后设备功能可能受限
4. **Token 有效期** - deviceToken 有效期 24 小时，过期需重新获取
5. **推荐流程** - 使用 `get-and-set` 组合操作可自动获取范围并验证，避免手动查询

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/battery_manage.py` | 主脚本（查询/设置阈值） |
| `scripts/crypto.py` | 签名/时间戳加密工具 |
| `scripts/get_device_token.py` | 获取设备 Token |
| `scripts/get_current_threshold.py` | 查询当前阈值 |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
