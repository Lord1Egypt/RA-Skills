---
name: tm-robot
description: >
  达明机器人 (Techman Robot / OMRON TM5) 控制技能。支持自定义 SVR 解析器、SCT 运动控制、状态监控。
  用于机器人编程、仿真、视觉集成、I/O 控制、状态监控等任务。
  
  触发词：TM 机器人、达明机器人、TM5、Techman、控制机器人、移动关节、直线运动、读取状态、机器人复位
  
metadata:
  openclaw:
    emoji: "🦾"
  author: RobotQu
  version: 1.1.0
  robot_model: OMRON TM5-700/TM5-900/TM12
  sdk: techmanpy + 自定义 SVR 解析器
---

# TM Robot Skill - 达明机器人控制

用于控制 OMRON TM5 协作机器人。支持关节运动、直线运动、I/O 控制、状态监控。

## ✅ 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| **SVR 状态读取** | ✅ 完全支持 | 自定义解析器，支持所有 TMflow 变量 |
| **SCT 运动控制** | ✅ 完全支持 | 关节运动、直线运动、回零 |
| **I/O 控制** | ✅ 完全支持 | 数字输出、数字输入读取 |
| **力控数据** | ✅ 支持 | TCP_Force, Joint_Torque |
| **错误监控** | ✅ 支持 | Error_Code, Robot_Error |

## 🧪 测试环境

**已验证的配置：**

| 项目 | 值 |
|------|-----|
| **机器人型号** | OMRON TM5M-700 |
| **TMflow 版本** | 1.80.5300 |
| **控制器型号** | TM5M-700 |
| **控制器序列号** | BC1934034 |
| **机器人 IP** | 192.168.1.13 |
| **测试日期** | 2026-03-31 |

**兼容的机器人型号：**

| 型号 | 状态 | 说明 |
|------|------|------|
| TM5-700 | ✅ 已验证 | 主力测试机型 |
| TM5-900 | ✅ 理论上兼容 | 同系列，协议相同 |
| TM12 | ✅ 理论上兼容 | 协议相同，关节数相同 |
| TM5-450 | ✅ 理论上兼容 | 同系列，协议相同 |
| TM7 系列 | ⚠️ 待验证 | 协议可能不同 |

> **说明**：所有使用 Ethernet Slave 协议的 TM 协作机器人都应该兼容。TM7 系列使用新协议，需要额外测试。

## ⚠️ 机器人端配置（使用前必读）

**本技能需要在机器人 TMflow 界面完成配置！**

### 机器人端配置步骤

#### 1. 启用 Ethernet Slave（Port 5891 - 状态读取）

TMflow → Robot Setting → Ethernet Slave → 开启 → 数据表

**推荐添加的变量（支持完整状态监控）：**
- `Joint_Angle` - 关节角度 (6 floats)
- `Coord_Robot_Flange` - 笛卡尔位姿 (9 floats)
- `Error_Code` - 错误码 (int)
- `Robot_Error` - 错误标志 (bool)
- `Project_Run` - 项目运行状态 (bool)
- `TCP_Force` - TCP 受力 (3 floats)
- `Joint_Torque` - 关节力矩 (6 floats)
- `Ctrl_DO0`~`Ctrl_DO7` - 数字输出
- `Ctrl_DI0`~`Ctrl_DI7` - 数字输入

#### 2. 运行 Listen Node 项目（Port 5890 - 运动控制）

TMflow → 新建项目 → 添加 Listen Node → 运行项目

### 连接测试

```bash
# 检测端口是否开放
python scripts/test_ports.py

# 测试 SVR 读取
python tm_robot.py
```

## 📦 安装

```bash
# 安装依赖
pip install techmanpy

# 验证安装
python -c "import techmanpy; print(techmanpy.__version__)"
```

## 🚀 使用方法

### 方法 1：作为 Python 模块导入

```python
from tm_robot import TMRobot, connect_robot
import asyncio

async def demo():
    # 连接机器人
    async with TMRobot("192.168.1.13") as robot:
        # 读取状态
        state = await robot.get_state()
        print(state)
        
        # 读取关节角度
        joints = await robot.get_joints()
        print(f"Joints: {joints}")
        
        # 读取笛卡尔位姿
        pose = await robot.get_pose()
        print(f"Pose: {pose}")
        
        # 关节运动到零位
        await robot.move_joints_zero()
        
        # 设置数字输出
        await robot.set_digital_output(0, True)

asyncio.run(demo())
```

### 方法 2：命令行工具

```bash
# 读取机器人状态
python tm_robot.py state

# 读取关节角度
python tm_robot.py joints

# 读取笛卡尔位姿
python tm_robot.py pose

# 回零（所有关节到 0°）
python tm_robot.py zero

# 停止运动
python tm_robot.py stop

# 复位报警
python tm_robot.py reset
```

## 📊 支持的 SVR 变量

### 状态变量
| 变量名 | 类型 | 说明 |
|--------|------|------|
| `Error_Code` | int | 错误码（0=无错误）|
| `Robot_Error` | bool | 错误标志 |
| `Project_Run` | bool | 项目运行中 |
| `Project_Pause` | bool | 项目暂停 |
| `Robot_Light` | int | 机器人灯状态 |
| `MA_Mode` | int | 手动/自动模式 |

### 运动学变量
| 变量名 | 类型 | 说明 |
|--------|------|------|
| `Joint_Angle` | 6 floats | 关节角度 (度) |
| `Joint_Speed` | 6 floats | 关节速度 (度/s) |
| `Joint_Torque` | 6 floats | 关节力矩 (mNm) |
| `Coord_Robot_Flange` | 9 floats | 法兰笛卡尔位姿 |
| `Coord_Robot_Tool` | 9 floats | 工具笛卡尔位姿 |

### 力控变量
| 变量名 | 类型 | 说明 |
|--------|------|------|
| `TCP_Force` | 3 floats | TCP 受力 (N) |
| `TCP_Force3D` | float | TCP 受力大小 |
| `TCP_Speed` | 6 floats | TCP 速度 |

### I/O 变量
| 变量名 | 类型 | 说明 |
|--------|------|------|
| `Ctrl_DO0`~`Ctrl_DO7` | bool | 控制器数字输出 |
| `Ctrl_DI0`~`Ctrl_DI7` | bool | 控制器数字输入 |
| `End_DO0`~`End_DO3` | bool | 末端数字输出 |
| `End_DI0`~`End_DI3` | bool | 末端数字输入 |

## 🔧 技术细节

### SVR 协议解析

本技能使用**自定义 SVR 解析器**直接解析 TMflow 的原始 socket 数据，而不是依赖 techmanpy 的 Binary 解析器。

**原因：** TMflow 的 SVR 协议是 **ASCII 变量名 + 二进制数据** 的混合格式，techmanpy 的解析器不兼容。

**协议格式：**
```
Header: $TMSVR,3279,1,1,\n (ASCII)
Body: [变量名\x00][类型码][\x00][数据...][\x??\x00] 重复
```

**类型码：**
- `0x01`: bool (1 byte)
- `0x04`: int32 (4 bytes, little-endian)
- `0x18`: 6 floats (24 bytes)
- `0x24`: 9 floats (36 bytes)
- `0x0C`: 3 floats (12 bytes)

## 📁 文件结构

```
skills/tm-robot/
├── SKILL.md           # 技能文档（本文件）
├── README.md          # 详细配置指南
├── tm_robot.py        # 核心 API
├── config.py          # 配置
├── scripts/           # 测试脚本
│   ├── test_ports.py      # 端口检测
│   ├── test_connection.py # 连接测试
│   └── ...
└── docs/              # 详细文档
    ├── error_codes.md     # 错误码
    └── ...
```

## 🐛 故障排除

### SVR 连接失败
1. 检查 Ethernet Slave 是否开启
2. 确认数据表中有变量
3. 运行 `python scripts/test_ports.py` 检测端口

### SCT 连接失败
1. 确认 Listen Node 项目正在运行
2. 检查机器人 IP 是否正确
3. 确认防火墙未阻止 5890 端口

### 变量读取失败
1. 确认变量已在 TMflow 数据表中添加
2. 检查变量名拼写（区分大小写）
3. 运行 `python tm_robot.py` 测试解析器

## 📚 参考资料

- [TMflow 官方文档](https://www.tm-robot.com/)
- [techmanpy GitHub](https://github.com/TechmanRobotInc/techmanpy)
- [TM Export 工具](https://github.com/TechmanRobotInc/TM_Export)
