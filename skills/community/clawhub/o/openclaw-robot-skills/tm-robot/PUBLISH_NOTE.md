# TM Robot Skill v1.1.0 发布说明

**发布日期**: 2026-03-31  
**适用机器人**: OMRON TM5/TM 系列协作机器人  
**TMflow 版本**: 1.80+

---

## 🎉 新功能

### 核心功能
- ✅ **状态监控** - 关节角度、笛卡尔位姿、力矩、错误码、项目状态
- ✅ **运动控制** - 关节 PTP、直线 LIN、圆弧 ARC、回零
- ✅ **安全功能** - 急停、报警复位
- ✅ **相机支持** - 手眼相机位姿读取
- ✅ **IO 监控** - DI 状态读取

### 代码质量
- ✅ **100% 类型注解** - 完整的类型提示
- ✅ **日志系统** - 完整的操作日志
- ✅ **单元测试** - 9 个测试用例全部通过
- ✅ **自定义 SVR 解析器** - 高性能状态读取（替代官方解析器）

---

## 📦 安装

```bash
# 克隆技能
git clone https://github.com/RobotQu/tm-robot-skill.git

# 安装依赖
pip install techmanpy

# 运行测试
cd skills/tm-robot
python examples/complete_demo.py
```

---

## 🚀 快速开始

```python
from tm_robot import TMRobot
import asyncio

async def main():
    robot = TMRobot('192.168.1.13')
    
    # 连接
    await robot.connect_all()
    
    # 读取状态
    joints = await robot.get_joints()
    pose = await robot.get_pose()
    
    # 运动控制
    await robot.move_joint([0, 0, 90, 0, 90, 0], speed=0.3)
    await robot.move_relative_line([100, 0, 0, 0, 0, 0], speed=0.2)
    
    # 断开
    await robot.disconnect()

asyncio.run(main())
```

---

## 📊 现场测试结果

**测试机器人**: OMRON TM5M-700, TMflow 1.80.5300  
**测试通过率**: 17/17 = 100% ✅

| 功能 | 状态 | 备注 |
|------|------|------|
| 关节运动 PTP | ✅ | 完全支持 |
| 直线运动 LIN | ✅ | 需要 TMflow 项目 |
| 圆弧运动 ARC | ✅ | 需要 TMflow 项目 |
| 状态读取 | ✅ | 关节、位姿、力矩、错误码 |
| 相机位姿 | ✅ | 手眼相机 |
| 急停/复位 | ✅ | 安全功能 |

---

## ⚠️ 重要说明

### 直线/圆弧运动

直线和圆弧运动**需要 TMflow 项目配合**：

1. 在 TMflow 中创建项目
2. 添加 Listen Node
3. 运行项目

**关节运动 (PTP) 无需 TMflow 项目**，可直接控制。

### DO 控制

当前版本**不支持 DO 控制**（techmanpy 库限制）。

替代方案：
- 通过 TMflow 项目控制
- 使用 Modbus TCP 协议

---

## 📁 文件结构

```
skills/tm-robot/
├── SKILL.md              # 技能文档
├── README.md             # 使用说明
├── tm_robot.py           # 主 API (600 行)
├── tm_camera.py          # 相机支持
├── examples/             # 示例代码
├── scripts/              # 实用脚本
├── tests/                # 单元测试
└── docs/                 # 技术文档
```

---

## 🔧 API 参考

### 连接
```python
await robot.connect_svr()      # SVR 连接（状态读取）
await robot.connect_sct()      # SCT 连接（运动控制）
await robot.connect_all()      # 同时连接
await robot.disconnect()       # 断开连接
```

### 状态读取
```python
joints = await robot.get_joints()    # 关节角度
pose = await robot.get_pose()        # 笛卡尔位姿
torque = robot.get_torque()          # 关节力矩
error = robot.get_error_code()       # 错误码
```

### 运动控制
```python
await robot.move_joint([0, 0, 90, 0, 90, 0], speed=0.3)           # 关节运动
await robot.move_relative_line([100, 0, 0, 0, 0, 0], speed=0.2)   # 直线相对
await robot.move_absolute_line([500, -100, 400, 180, 0, 90])      # 直线绝对
await robot.move_circle(point1, point2, speed=0.3)                # 圆弧
await robot.move_joints_zero(speed=0.1)                           # 回零
```

### 安全功能
```python
await robot.stop_motion()      # 急停
await robot.reset_alarm()      # 复位报警
```

---

## 🐛 已知问题

1. **直线/圆弧运动需要 TMflow 项目** - 文档已说明
2. **DO 控制不支持** - 计划 v1.2.0 通过 Modbus TCP 实现

---

## 📞 技术支持

- **完整文档**: `skills/tm-robot/README.md`
- **测试报告**: `skills/tm-robot/TEST_REPORT.md`
- **示例代码**: `skills/tm-robot/examples/`
- **RobotQu 网站**: https://robotqu.com
- **B 站**: Robot_Qu 机器人社区

---

## 🎯 后续计划 (v1.2.0)

- [ ] DO 控制（Modbus TCP）
- [ ] 视觉引导抓取
- [ ] 力控功能
- [ ] ROS2 驱动
- [ ] 更多实用脚本

---

**v1.1.0 发布状态**: ✅ 生产就绪

---

*发布作者：RobotQu*  
*测试地点：青岛 RobotQu 实验室*  
*测试日期：2026-03-31*
