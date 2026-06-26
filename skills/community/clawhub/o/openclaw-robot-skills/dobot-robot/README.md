# DOBOT CR10A Python SDK

DOBOT CR10A 机械臂 Python TCP/IP 控制 SDK，基于越疆官方 V4 API。

## 📦 安装

### 前置要求
- Python 3.6+
- NumPy
- 网络配置：本机 IP 需设置为 192.168.X.X 网段

### 安装依赖
```bash
pip install numpy
```

### 网络配置
1. 设置本机 IP 为 192.168.X.X 网段
2. 确保机器人处于 TCP/IP 模式 (在 DobotStudio Pro 中设置)
3. 确保 29999 和 30004 端口未被占用

## 🚀 快速开始

```python
from dobot_api import DobotApiDashboard, DobotApiFeedBack

# 连接机器人
dashboard = DobotApiDashboard("192.168.5.1", 29999)
feedback = DobotApiFeedBack("192.168.5.1", 30004)

# 使能机器人
dashboard.ClearError()
dashboard.EnableRobot()

# 关节空间运动
dashboard.MovJ(0, 0, 90, 0, 90, 0, 1)  # coordinateMode=1 关节模式

# 笛卡尔空间运动
dashboard.MovJ(100, -250, 400, 180, 90, 0, 0)  # coordinateMode=0 笛卡尔模式

# 获取状态
joints = dashboard.GetAngle()  # 关节角度
pose = dashboard.GetPose()     # 笛卡尔坐标

# 下使能
dashboard.DisableRobot()
dashboard.close()
feedback.close()
```

## 📋 API 参考

### 基础控制
| 方法 | 说明 | 示例 |
|------|------|------|
| `EnableRobot()` | 使能机器人 | `dashboard.EnableRobot()` |
| `DisableRobot()` | 下使能 | `dashboard.DisableRobot()` |
| `ClearError()` | 清除错误 | `dashboard.ClearError()` |
| `SpeedFactor(speed)` | 设置速度比例 (0-100) | `dashboard.SpeedFactor(50)` |
| `AccJ(speed)` | 关节加速度比例 | `dashboard.AccJ(50)` |
| `AccL(speed)` | 直线加速度比例 | `dashboard.AccL(50)` |

### 运动控制
| 方法 | 说明 | 示例 |
|------|------|------|
| `MovJ(..., coordinateMode)` | 关节运动 | `MovJ(0,0,90,0,90,0, 1)` |
| `MovL(..., coordinateMode)` | 直线运动 | `MovL(100,-250,400,180,90,0, 0)` |
| `Arc(...)` | 圆弧运动 | `Arc(x1,y1,z1,rx1,ry1,rz1, x2,y2,z2,rx2,ry2,rz2, 0)` |
| `Circle(...)` | 整圆运动 | `Circle(..., count=1)` |
| `ServoJ(...)` | 关节伺服 | `ServoJ(0,0,90,0,90,0, t=0.1)` |

### 状态查询
| 方法 | 说明 | 返回值 |
|------|------|--------|
| `GetAngle()` | 获取关节角度 | `{J1,J2,J3,J4,J5,J6}` |
| `GetPose()` | 获取笛卡尔坐标 | `{X,Y,Z,RX,RY,RZ}` |
| `RobotMode()` | 获取机器人模式 | Mode 值 |

### 数字 IO
| 方法 | 说明 | 示例 |
|------|------|------|
| `DO(index, status)` | 数字输出 | `DO(1, 1)` |
| `GetDO(index)` | 读取输出 | `GetDO(1)` |
| `DI(index)` | 数字输入 | `DI(1)` |

## 🧪 测试脚本

| 脚本 | 说明 | 状态 |
|------|------|------|
| `test_joint_angles.py` | 关节角度控制测试 | ✅ |
| `test_joint_limits.py` | J1-J6 限位测试 | ✅ |
| `test_sdk_system.py` | SDK 系统功能测试 | ✅ |
| `test_motion_commands.py` | 运动指令测试 | ✅ |
| `test_draw_square.py` | 画正方形测试 | ✅ |

## 📊 测试结果

### 仿真环境支持情况

**✅ 完全支持:**
- 关节空间运动 (MovJ joint mode)
- 笛卡尔空间运动 (MovJ pose mode)
- 6 轴关节控制
- 基础状态查询
- 数字 IO (部分引脚)

**❌ 不支持:**
- MovL 直线运动 (返回 -2)
- Arc/Circle 圆弧运动 (返回 -2)
- ServoJ/ServoP 伺服控制 (返回 -2)
- 力控功能 (返回 -2)
- 安全功能 (返回 -1/-2)

### 错误码说明

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| `0` | ✅ 成功 | - |
| `-1` | ❌ 参数错误 | 检查参数范围 |
| `-2` | ❌ 功能不支持 | 仿真环境限制 |
| `-40001` | ❌ 索引无效 | 检查 IO 引脚编号 |

## 🔧 坐标系说明

### coordinateMode 参数
- `0` = pose 方式 (笛卡尔坐标) `{X,Y,Z,RX,RY,RZ}`
- `1` = joint 方式 (关节坐标) `{J1,J2,J3,J4,J5,J6}`

### 关节范围参考
| 关节 | 范围 | 说明 |
|------|------|------|
| J1 | -180° ~ 180° | 底座旋转 |
| J2 | -135° ~ 135° | 下臂 |
| J3 | -150° ~ 150° | 上臂 |
| J4 | -180° ~ 180° | 手腕旋转 |
| J5 | -180° ~ 180° | 手腕弯曲 |
| J6 | -360° ~ 360° | 手腕扭转 |

## 📝 使用示例

### 示例 1: 关节空间运动
```python
# 移动到关节角度
dashboard.MovJ(0, 0, 90, 0, 90, 0, 1)
```

### 示例 2: 笛卡尔空间运动
```python
# 移动到笛卡尔坐标
dashboard.MovJ(100, -250, 400, 180, 90, 0, 0)
```

### 示例 3: 获取当前状态
```python
# 获取关节角度
result = dashboard.GetAngle()
# 解析：0,{J1,J2,J3,J4,J5,J6},GetAngle()

# 获取笛卡尔坐标
result = dashboard.GetPose()
# 解析：0,{X,Y,Z,RX,RY,RZ},GetPose()
```

### 示例 4: 数字 IO 控制
```python
# 设置 DO1 为 ON
dashboard.DO(1, 1)

# 读取 DI1 状态
result = dashboard.DI(1)
```

## ⚠️ 注意事项

1. **安全第一** - 运行前确保机器人处于安全位置
2. **网络配置** - 确保 IP 在同一网段
3. **端口占用** - 确保 29999 和 30004 端口未被占用
4. **机器人模式** - 确保机器人处于 TCP/IP 控制模式
5. **仿真限制** - 仿真环境不支持所有功能，真机才能完整测试

## 📚 官方文档

- 官方 SDK: `official-sdk/`
- README_V4.pdf: 完整 API 文档
- 官方 GitHub: https://github.com/Dobot-Arm/TCP-IP-CR-Python-V4

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

基于越疆官方 SDK 修改，遵循原项目许可证。

## 📞 技术支持

- DOBOT 官方文档：https://www.dobot-robot.com/
- 本项目 Issue: https://github.com/your-repo/dobot-robot/issues

---

*Last updated: 2026-04-01*
*Tested with: DOBOT CR10A (仿真环境)*
