---
name: jf-open-pro-ptz-control
description: 杰峰云台设备控制技能（开发版）。支持云台方向控制、变倍聚焦、预置位管理、巡航计划、回到守望位等功能，适用于云台摄像头设备。
metadata:
  version: 1.0.0
  author: JFTech
  category: ptz
  tags:
    - 杰峰
    - 云台控制
    - PTZ
    - 预置位
    - 巡航
    - 变倍
    - 聚焦
  triggers:
    - 云台控制
    - PTZ 控制
    - 方向控制
    - 向上转/向下转/向左转/向右转
    - 变倍/聚焦
    - 预置位
    - 巡航计划
    - 回到守望位
  prerequisites:
    - 配置必需的环境变量
    - 设备需支持云台功能
    - 设备需已完成配网和绑定
    - 设备需在线
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-ptz-control - 杰峰云台设备控制技能（开发版）

## 技能描述

支持杰峰云台设备的全面控制功能：

- **云台方向控制** - 上/下/左/右/左上/左下/右上/右下八个方向
- **变倍和聚焦** - 光学变倍放大/缩小，聚焦远/近调节
- **预置位管理** - 设置/删除/转到/编辑预置位
- **巡航计划** - 添加/删除/开始/停止/清除巡航点
- **特殊预置位** - 移动追踪守望位（100）、自检回归预置位（128）

**适用场景：**
- 远程调整摄像头视角
- 快速定位到预设监控位置
- 自动巡航监控多个区域
- 变焦查看细节

## 触发词

- 云台控制 / PTZ 控制 / 方向控制
- 向上转 / 向下转 / 向左转 / 向右转
- 左上 / 左下 / 右上 / 右下
- 变倍 / 聚焦 / 放大 / 缩小
- 预置位 / 巡航 / 守望位

## 前置条件

### 硬件要求

1. **云台设备** - 设备需支持 PTZ 功能
2. **能力集验证** - `OtherFunction.SupportPTZDirectionControl` 为 `true`

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
| 云台方向控制 | `POST /gwp/v3/rtc/device/opdev/{token}` | POST | ✅ | ✅ |
| 变倍聚焦控制 | `POST /gwp/v3/rtc/device/opdev/{token}` | POST | ✅ | ✅ |
| 预置位操作 | `POST /gwp/v3/rtc/device/opdev/{token}` | POST | ✅ | ✅ |
| 巡航计划 | `POST /gwp/v3/rtc/device/opdev/{token}` | POST | ✅ | ✅ |
| 获取预置位列表 | `POST /gwp/v3/rtc/device/getconfig/{token}` | POST | ✅ | ✅ |
| 获取巡航配置 | `POST /gwp/v3/rtc/device/getconfig/{token}` | POST | ✅ | ✅ |

## 核心功能

### 1. 云台方向控制（Direction Control）

**API:** `POST /gwp/v3/rtc/device/opdev/{deviceToken}`

**Name:** `OPPTZControl`

**Command 参数：**
| 方向 | Command 值 |
|------|-----------|
| 上 | `DirectionUp` |
| 下 | `DirectionDown` |
| 左 | `DirectionLeft` |
| 右 | `DirectionRight` |
| 左上 | `DirectionLeftUp` |
| 左下 | `DirectionLeftDown` |
| 右上 | `DirectionRightUp` |
| 右下 | `DirectionRightDown` |

**Parameter 参数：**
| 参数 | 类型 | 说明 | 取值 |
|------|------|------|------|
| `Preset` | int | 运动控制 | `0`=开始运动，`-1`=停止运动 |
| `Channel` | int | 通道号 | `0`=第一通道 |
| `Step` | int | 运动速度 | `1-8`（1 最慢，8 最快） |

**⚠️ 重要：**
- **start/stop 指令需间隔 500ms**，避免并发冲突
- **未调用停止，设备会一直转到最大角度**

**操作步骤：**
1. 发送 start 指令（Preset=0）
2. 等待 500ms
3. 发送 stop 指令（Preset=-1）

### 2. 变倍和聚焦控制（Zoom & Focus）

**API:** `POST /gwp/v3/rtc/device/opdev/{deviceToken}`

**Name:** `OPPTZControl`

**Command 参数：**
| 功能 | Command 值 | 说明 |
|------|-----------|------|
| 变倍 - | `ZoomWide` | 缩小（广角） |
| 变倍 + | `ZoomTile` | 放大（长焦） |
| 聚焦 - | `FocusFar` | 聚焦远处 |
| 聚焦 + | `FocusNear` | 聚焦近处 |
| 光圈 - | `IrisSmall` | 缩小光圈 |
| 光圈 + | `IrisLarge` | 放大光圈 |

**Parameter 参数：**
| 参数 | 类型 | 说明 | 取值 |
|------|------|------|------|
| `Channel` | int | 通道号 | `0`=第一通道 |
| `Step` | int | 操作速度 | `1-8`（1 最慢，8 最快） |
| `Preset` | int | 开始/停止 | `0`=开始，`-1`=停止 |

**⚠️ 注意：** 变倍和聚焦不支持设置特定倍数，只能操作快慢。

### 3. 预置位管理（Preset）

**API:** `POST /gwp/v3/rtc/device/opdev/{deviceToken}`

**Name:** `OPPTZControl`

**Command 参数：**
| 操作 | Command 值 | 说明 |
|------|-----------|------|
| 设置预置位 | `SetPreset` | 保存当前位置为预置位 |
| 删除预置位 | `ClearPreset` | 删除指定预置位 |
| 转到预置位 | `GotoPreset` | 转动到指定预置位 |
| 编辑预置位名称 | `SetPresetName` | 修改预置位名称 |

**Parameter 参数：**
| 参数 | 类型 | 说明 | 取值 |
|------|------|------|------|
| `Preset` | int | 预置位编号 | `1-255` |
| `Channel` | int | 通道号 | `0`=第一通道 |
| `PresetName` | string | 预置位名称 | 自定义名称 |

**特殊预置位：**
| 编号 | 名称 | 说明 |
|------|------|------|
| `100` | 移动追踪守望位 | 追踪停止后自动回归的位置 |
| `128` | 自检回归预置位 | 设备重启/自检后回归的位置 |

**设置步骤：**
1. 方向控制，转动设备到某一方向
2. 设置预置位（SetPreset）
3. 转动到其他方向
4. 转到预置位（GotoPreset）验证

### 4. 巡航计划（PTZ Tour）

**API:** `POST /gwp/v3/rtc/device/opdev/{deviceToken}`

**Name:** `OPPTZControl`

**Command 参数：**
| 操作 | Command 值 | 说明 |
|------|-----------|------|
| 添加巡航点 | `AddTour` | 往巡航线路添加预置点 |
| 删除巡航点 | `DeleteTour` | 从巡航线路删除预置点 |
| 开始巡航 | `StartTour` | 开始自动巡航 |
| 停止巡航 | `StopTour` | 停止巡航 |
| 清除巡航线路 | `ClearTour` | 清除整个巡航线路 |

**Parameter 参数：**
| 参数 | 类型 | 说明 | 取值 |
|------|------|------|------|
| `Preset` | int | 预置点编号 | `0-255` |
| `Tour` | int | 巡航线路编号 | `0`（默认） |
| `Channel` | int | 通道号 | `0`=第一通道 |
| `Step` | int | 转动速度 | `1-8`（添加巡航点时有效） |

**巡航说明：**
- 设备会在预设的预置点之间自动循环转动
- 可自定义点与点之间的转动速度
- 支持多条巡航线路

### 5. 获取预置位列表

**API:** `POST /gwp/v3/rtc/device/getconfig/{deviceToken}`

**Name:** `Uart.PTZPreset`

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| Uart.PTZPreset | object[] | 预置位列表 |
| ├─ Id | int | 预置位编号 |
| ├─ PresetName | string | 预置位名称 |

### 6. 获取巡航路径配置

**API:** `POST /gwp/v3/rtc/device/getconfig/{deviceToken}`

**Name:** `Uart.PTZTour`

## 使用示例

### 环境准备

```bash
# 设置环境变量
export JF_UUID="uuidxxxx"
export JF_APP_KEY="appkeyxxxx"
export JF_APP_SECRET="appsecretxxxx"
export JF_MOVE_CARD=0
export JF_DEVICE_SN="snxxx1"
export JF_DEVICE_TOKEN="NTQ0NzQ3YmE3MXwyYzFk..."
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 云台方向控制

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-ptz-control/scripts

# 向上转动
python3 ptz_control.py --action direction --direction up

# 向左转动
python3 ptz_control.py --action direction --direction left

# 向右下转动
python3 ptz_control.py --action direction --direction rightdown
```

### 2. 变倍和聚焦

```bash
# 变倍放大（拉近）
python3 ptz_control.py --action zoom --zoom in

# 变倍缩小（拉远）
python3 ptz_control.py --action zoom --zoom out

# 聚焦远处
python3 ptz_control.py --action focus --focus far

# 聚焦近处
python3 ptz_control.py --action focus --focus near
```

### 3. 预置位管理

```bash
# 设置预置位 1
python3 ptz_control.py --action set-preset --preset 1 --name "门口"

# 转到预置位 1
python3 ptz_control.py --action goto-preset --preset 1

# 删除预置位 1
python3 ptz_control.py --action clear-preset --preset 1

# 编辑预置位名称
python3 ptz_control.py --action set-preset-name --preset 1 --name "大门入口"

# 查询预置位列表
python3 ptz_control.py --action list-presets
```

### 4. 巡航计划

```bash
# 添加预置位 1 到巡航线路 0
python3 ptz_control.py --action add-tour --tour 0 --preset 1

# 添加预置位 2 到巡航线路 0
python3 ptz_control.py --action add-tour --tour 0 --preset 2

# 开始巡航
python3 ptz_control.py --action start-tour --tour 0

# 停止巡航
python3 ptz_control.py --action stop-tour --tour 0

# 清除巡航线路
python3 ptz_control.py --action clear-tour --tour 0

# 查询巡航配置
python3 ptz_control.py --action list-tours
```

### 5. 特殊预置位

```bash
# 设置移动追踪守望位（预置位 100）
python3 ptz_control.py --action set-preset --preset 100 --name "追踪守望位"

# 设置自检回归预置位（预置位 128）
python3 ptz_control.py --action set-preset --preset 128 --name "自检回归位"

# 转到移动追踪守望位
python3 ptz_control.py --action goto-preset --preset 100
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

## 注意事项

1. **设备要求** - 设备需支持云台 PTZ 功能
2. **deviceToken 有效期** - 24 小时，过期需重新获取
3. **设备在线要求** - 所有操作需要设备在线
4. **start/stop 间隔** - 方向控制指令需间隔 500ms
5. **未停止会持续转动** - 未调用 stop 设备会转到最大角度
6. **预置位编号** - 建议使用 1-199，200 以后可能为特殊用途
7. **特殊预置位** - 100=移动追踪守望位，128=自检回归预置位
8. **变倍聚焦** - 不支持设置特定倍数，只能操作快慢

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/ptz_control.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
