# OpenClaw Robot Skills - 技能文档

**版本**: 1.0.0  
**作者**: RobotQu  
**许可**: MIT

---

## 📋 技能描述

用统一的 API 控制所有品牌的协作机器人。

当前支持：
- **OMRON TM** v1.1.0 - 完整支持
- **JAKA** v1.1.0 - 标准支持

---

## 🎯 核心功能

### 统一 API

所有品牌使用相同的接口：

```python
# 连接
await robot.connect()
await robot.disconnect()

# 状态
joints = await robot.get_joints()
pose = await robot.get_pose()

# 运动
await robot.move_joint(joints, speed)
await robot.move_relative_line(delta, speed)
await robot.move_circle(p1, p2, speed)

# 安全
await robot.stop()
await robot.reset_alarm()
```

### 已实现功能

| 功能 | TM | JAKA |
|------|----|----|
| 连接/断开 | ✅ | ✅ |
| 关节角度读取 | ✅ | ✅ |
| 笛卡尔位姿 | ✅ | ✅ |
| 关节运动 (PTP) | ✅ | ✅ |
| 直线运动 (LIN) | ✅ | ✅ |
| 圆弧运动 (ARC) | ✅ | ⏳ |
| 急停 | ✅ | ✅ |
| 报警复位 | ✅ | ⏳ |
| 相机支持 | ✅ | ⏳ |
| IO 控制 | ✅ | ✅ |

---

## 📦 包含的子技能

### 1. TM Robot (tm-robot/)

**OMRON TM 协作机器人控制**

- 状态监控（关节、位姿、力矩、错误码）
- 运动控制（PTP、LIN、ARC）
- 安全功能（急停、报警复位）
- 相机支持（手眼相机位姿）
- IO 控制（DI 读取）

**测试**: 17/17 现场测试通过

### 2. JAKA Robotics Control (jaka-robotics-control/)

**JAKA 协作机器人控制**

- 关节运动
- 直线运动
- 状态读取
- IO 控制

---

## 🔧 依赖

- Python >= 3.8
- techmanpy >= 1.0.0 (TM Robot 需要)
- JAKA SDK (JAKA 需要，已包含)

---

## 🚀 使用示例

### TM Robot 完整示例

```python
from tm_robot import TMRobot

async def main():
    robot = TMRobot(robot_ip="192.168.1.13")
    
    # 连接
    await robot.connect()
    print(f"已连接：{robot.robot_model}")
    
    # 获取状态
    joints = await robot.get_joints()
    print(f"关节角度：{joints}")
    
    # 运动到 home 位置
    await robot.move_joint([0, 0, 90, 0, 90, 0], speed=0.3)
    
    # 直线移动
    await robot.move_relative_line([100, 0, 0, 0, 0, 0], speed=0.2)
    
    # 断开
    await robot.disconnect()

await main()
```

### JAKA 完整示例

```python
from jaka_skill import JakaRobot

async def main():
    robot = JakaRobot(robot_ip="192.168.1.10")
    
    # 连接
    await robot.connect()
    
    # 获取关节角度
    joints = await robot.get_joints()
    print(f"当前关节：{joints}")
    
    # 直线运动
    await robot.move_linear([300, 0, 400, 180, 0, 90], speed=0.2)
    
    # 断开
    await robot.disconnect()

await main()
```

---

## 📚 文档

- TM Robot 详细文档：`tm-robot/SKILL.md`
- JAKA 详细文档：`jaka-robotics-control/SKILL.md`
- 统一 API 规范：`skills/API_SPEC.md`

---

## 🧪 测试

### TM Robot

```bash
cd tm-robot
python -m pytest tests/test_svr_parser.py -v
```

**结果**: 9/9 通过

### JAKA

```bash
cd jaka-robotics-control
python test_connect.py
```

---

## 🗺️ 路线图

| 阶段 | 目标 | 时间 |
|------|------|------|
| Phase 1 | TM + JAKA + Yamaha | 2026-04 |
| Phase 2 | ABB + FANUC | 2026-05 |
| Phase 3 | KUKA + Yaskawa | 2026-06 |
| Phase 4 | 10+ 品牌 | 2026-07 |
| Phase 5 | 20+ 品牌生态 | 2026-12 |

---

## 📞 支持

- **网站**: https://robotqu.com
- **B 站**: Robot_Qu 机器人社区
- **GitHub**: https://github.com/qujingyang28/openclaw-robot-skills

---

## 📄 许可证

MIT License

---

*One API to Rule Them All! 🤖*
