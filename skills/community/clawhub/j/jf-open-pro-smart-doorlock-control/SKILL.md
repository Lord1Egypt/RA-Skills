---
name: jf-open-pro-smart-doorlock-control
description: 杰峰智能门锁设备控制技能（开发版）。支持查询设备是否支持门锁能力、登录设备、获取设备接口访问令牌，以及远程一键开锁。
metadata:
  version: 1.0.0
  author: JFTech
  category: device
  tags:
    - 杰峰
    - 智能门锁
    - 远程开锁
    - 设备登录
    - 设备能力
  triggers:
    - 查询设备是否支持开锁
    - 设备支持门锁吗
    - 远程开锁
    - 一键开锁
    - 登录设备
    - 获取设备Token
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

# jf-open-pro-smart-doorlock-control - 杰峰智能门锁设备控制技能（开发版）

## 技能描述

支持杰峰智能门锁设备的远程控制功能：

- **查询设备是否支持开锁** - 查询设备能力集，确认是否支持门锁功能
- **登录设备** - 对门锁设备进行登录认证
- **获取设备接口访问令牌** - 获取 deviceToken 用于后续操作
- **远程一键开锁** - 远程发送开锁指令，控制门锁开启

**适用场景：**
- 远程给家人或访客开锁
- 确认设备是否支持门锁功能
- 设备登录与令牌管理

## 触发词

- 查询设备是否支持开锁 / 设备支持门锁吗
- 查询门锁配置 / 获取门锁配置
- 远程开锁 / 一键开锁 / 开锁
- 登录设备 / 设备登录
- 获取设备 Token

## 前置条件

### 硬件要求

1. **智能门锁** - 设备需为杰峰智能门锁设备

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
| 获取门锁配置 | `POST /gwp/v3/rtc/device/doorLockTransparent/{token}` | POST | ✅ | ✅ |
| 登录设备 | `POST /gwp/v3/rtc/device/login/{token}` | POST | ✅ | ✅ |
| 获取设备 Token | `POST /gwp/v3/rtc/device/token` | POST | ❌ | ❌ |
| 远程开锁 | `POST /gwp/v3/rtc/device/doorLockRemoteUnlock/{token}` | POST | ✅ | ✅ |

## 核心功能

### 1. 查询设备是否支持开锁

**API:** `POST /gwp/v3/rtc/device/getability/{deviceToken}`

**Name:** `DoorFunction`

**说明：** 查询设备能力集，确认设备是否支持门锁功能及相关特性。

**响应参数：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `DoorFunction.DoorAbilityMask` | int | 门锁能力掩码（按位标识各类门锁能力） |
| `DoorFunction.LocalAbilityMask` | int | 本地能力掩码（按位标识本地支持的能力） |
| `DoorFunction.UserManage` | object | 用户管理能力信息 |
| `DoorFunction.UserManage.TypeMsk` | int | 用户类型掩码 |
| `DoorFunction.AdminAbility` | int | 管理员能力值 |
| `DoorFunction.TmpPwdRange` | object | 临时密码范围配置 |
| `DoorFunction.TmpPwdRange.Start` | int | 临时密码起始值 |
| `DoorFunction.TmpPwdRange.End` | int | 临时密码结束值 |
| `DoorFunction.TmpPwdRange.UsrTypeMask` | int | 临时密码适用的用户类型掩码 |
| `DoorFunction.TipVolume` | int | 提示音量档位 |
| `DoorFunction.RebootMachine` | int | 重启设备支持标识 |
| `DoorFunction.OPTrans` | int | 透明传输能力标识 |
| `DoorFunction.IOTFaceModuleOta` | object | 人脸识别模块 OTA 信息 |
| `DoorFunction.IOTFaceModuleOta.Enable` | bool | 人脸识别模块 OTA 使能状态 |
| `DoorFunction.IOTFaceModuleOta.Pid` | int | 人脸识别模块产品 ID |
| `DoorFunction.IOTFaceModuleOta.ModuleName` | string | 人脸识别模块名称 |
| `DoorFunction.IOTFaceModuleOta.NavVersion` | string | 人脸识别模块导航版本 |
| `DoorFunction.QsCapMask` | int | 快速启动能力掩码 |
| `DoorFunction.QsPid` | int | 快速启动产品 ID |
| `DoorFunction.NavVersion` | string | 导航版本号 |

### 2. 获取门锁配置

**API:** `POST /gwp/v3/rtc/device/doorLockTransparent/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 | 取值 |
|------|------|------|------|------|
| `Name` | string | ✅ | 方法名称 | `OPDoorLockProCmd` |
| `OPDoorLockProCmd.Cmd` | string | ✅ | 命令码 | `GetDoorConfig` |

**请求示例：**
```json
{
  "Name": "OPDoorLockProCmd",
  "OPDoorLockProCmd": {
    "Cmd": "GetDoorConfig"
  }
}
```

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| `DoorConfig.PirConfig.Enable` | bool | 逗留侦测是否使能 |
| `DoorConfig.PirConfig.sensitivity` | int | 灵敏度：低/中/高（0/1/2） |
| `DoorConfig.UnlockDirection.Direction` | int | 方向：左/右（0/1） |
| `DoorConfig.AutoLock.LockMode` | int | 手动上锁/自动上锁（0/1） |
| `DoorConfig.AutoLock.AutoLockInterval` | int | 自动锁定时间：10~99 秒 |
| `DoorConfig.UnlockMode.mode` | int | 单开模式/组合模式（0/1） |
| `DoorConfig.VolumeControl.Volume` | int | 音量：静音/小/中/大（0/1/2/3） |
| `DoorConfig.FaceAlarmTone.Enable` | bool | 人脸声音开关是否使能 |
| `DoorConfig.MotorTorque.Torque` | int | 扭矩：小/中/大（0/1/2） |
| `DoorConfig.NormalOpenMode.Mode` | int | 常开模式：关闭/开启（0/1） |
| `DoorConfig.DeployDefense.Enable` | int | 布防状态：撤防/布防（0/1） |

### 3. 登录设备

**API:** `POST /gwp/v3/rtc/device/login/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| `UserName` | string | ✅ | 设备用户名，恢复出厂后部分设备默认为 `admin` | `admin` |
| `PassWord` | string | ❌ | 设备登录密码 | `123456` |
| `KeepaliveTime` | int | ❌ | 保活时长，单位秒（默认 5 分钟，最长 24 小时） | `300` |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| `Ret` | int | 设备登录状态码（100=成功） |
| `DeviceType` | string | 设备类型（IOT/IPC/DVR 等） |
| `AliveInterval` | int | 客户端与设备保活时间周期，单位秒 |
| `ChannelNum` | int | 设备通道数 |
| `SessionID` | string | 会话 ID |

**说明：** 设备默认 1 分钟无操作自动断开连接，若需保持长时间连接可设置 `KeepaliveTime` 进行保活。

### 3. 获取设备接口访问令牌

**API:** `POST /gwp/v3/rtc/device/token`

**说明：** 获取 deviceToken，用于后续的门锁操作。Token 有效期 24 小时。

### 4. 远程一键开锁

**API:** `POST /gwp/v3/rtc/device/doorLockRemoteUnlock/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 | 取值 |
|------|------|------|------|------|
| `sn` | string | ✅ | 设备序列号 | - |
| `props.doorLock.remoteUnlock.password` | string | ❌ | 锁端密码（密码开锁时必填） | - |
| `props.doorLock.remoteOneKeyUnlock` | int | ❌ | 无密码一键开锁标记，填 `1` | - |
| `props.doorLock.userType` | int | ❌ | 远程开锁为 `5` | `5` |
| `props.doorLock.memberID` | int | ❌ | 成员 ID，`1` 表示主账号 | `1` |

**说明：** 支持两种开锁方式。提供密码时使用密码开锁，不提供密码时使用无密码一键开锁。

## 使用示例

### 环境准备

```bash
# 设置环境变量（使用占位符，请替换为实际值）
export JF_UUID="uuidxxxx"
export JF_APP_KEY="appkeyxxxx"
export JF_APP_SECRET="appsecretxxxx"
export JF_MOVE_CARD="2"
export JF_DEVICE_SN="snxxx1"
export JF_DEVICE_TOKEN="NTQ0NzQ3YmE3MXwyYzFk..."
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 查询设备是否支持开锁

```bash
cd ~/.qoderwork/skills/jf-open-pro-smart-doorlock-control/scripts

python3 doorlock_control.py --action check-support
```

### 2. 获取门锁配置

```bash
python3 doorlock_control.py --action get-config
```

### 3. 登录设备

```bash
# 使用默认用户名 admin 登录
python3 doorlock_control.py --action login --username "admin" --password "123456"

# 设置保活时长为 10 分钟
python3 doorlock_control.py --action login --username "admin" --password "123456" --keepalive-time 600
```

### 4. 获取设备 Token

```bash
python3 doorlock_control.py --action get-token --device-sn "snxxx1"
```

### 5. 远程一键开锁

```bash
# 无密码一键开锁
python3 doorlock_control.py --action unlock

# 使用密码开锁
python3 doorlock_control.py --action unlock --password "123456"
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

1. **设备要求** - 仅智能门锁设备支持此功能
2. **deviceToken 有效期** - 24 小时，过期需重新获取
3. **设备在线要求** - 远程开锁需要设备在线
4. **安全性** - 远程开锁涉及物理安全，请谨慎操作
5. **登录要求** - 部分设备可能需要先登录才能执行开锁操作

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/doorlock_control.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
