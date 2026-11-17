# 🤖 OpenClaw Robot Skills

**用统一的 API 控制所有品牌的协作机器人！**

*One API to Rule Them All!*

---

## 🎯 项目愿景

让机器人控制像换电池一样简单 —— **统一接口，即插即用**

---

## ✅ 已支持品牌

| 品牌 | 版本 | 状态 | 支持级别 |
|------|------|------|----------|
| **OMRON TM** | v1.1.0 | ✅ 已发布 | Level 3 (完整) |
| **JAKA** | v1.1.0 | ✅ 已发布 | Level 2 (标准) |

---

## 🚀 快速开始

### 安装

```bash
openclaw skills install openclaw-robot-skills
```

### 使用 TM 机器人

```python
from tm_robot import TMRobot

robot = TMRobot(robot_ip="192.168.1.13")
await robot.connect()

# 获取状态
joints = await robot.get_joints()
pose = await robot.get_pose()

# 运动控制
await robot.move_joint([0, 0, 90, 0, 90, 0], speed=0.3)
await robot.move_relative_line([100, 0, 0, 0, 0, 0], speed=0.2)

await robot.disconnect()
```

### 使用 JAKA 机器人

```python
from jaka_skill import JakaRobot

robot = JakaRobot(robot_ip="192.168.1.10")
await robot.connect()

# 获取状态
joints = await robot.get_joints()

# 运动控制
await robot.move_linear([300, 0, 400, 180, 0, 90], speed=0.2)

await robot.disconnect()
```

---

## 🏗️ 统一 API

所有品牌遵循相同的接口：

```python
# 连接
await robot.connect()
await robot.disconnect()

# 状态读取
joints = await robot.get_joints()      # 关节角度
pose = await robot.get_pose()          # 笛卡尔位姿

# 运动控制
await robot.move_joint(joints, speed)           # 关节运动
await robot.move_relative_line(delta, speed)    # 直线运动
await robot.move_circle(p1, p2, speed)          # 圆弧运动

# 安全功能
await robot.stop()
await robot.reset_alarm()
```

---

## 📦 项目结构

```
openclaw-robot-skills/
├── manifest.json              # 技能元数据
├── README.md                  # 本文档
├── robot_skills.py            # 统一入口（可选）
│
├── tm-robot/                  # TM Robot 技能
│   ├── tm_robot.py
│   ├── SKILL.md
│   ├── examples/
│   └── tests/
│
└── jaka-robotics-control/     # JAKA 技能
    ├── jaka_skill.py
    ├── SKILL.md
    └── examples/
```

---

## 🗺️ 路线图

### Phase 1 (2026-04) - 基础
- [x] TM Robot v1.1.0
- [x] JAKA v1.1.0
- [ ] Yamaha v1.0.0

### Phase 2 (2026-05) - 四大家族
- [ ] ABB v1.0.0
- [ ] FANUC v1.0.0
- [ ] KUKA v0.5.0 (beta)
- [ ] Yaskawa v0.5.0 (beta)

### Phase 3 (2026-06) - 扩展
- [ ] 10+ 品牌支持
- [ ] ROS2 集成
- [ ] 完整生态系统

---

## 🎯 品牌支持级别

| Level | 说明 | 功能 |
|-------|------|------|
| **Level 1** | 基础支持 | 连接、状态读取、基本运动 |
| **Level 2** | 标准支持 | Level 1 + 完整运动控制、IO |
| **Level 3** | 完整支持 | Level 2 + 安全功能、相机、高级特性 |

---

## 📞 支持

- **作者**: RobotQu
- **网站**: https://robotqu.com
- **GitHub**: https://github.com/qujingyang28/openclaw-robot-skills
- **B 站**: Robot_Qu 机器人社区

---

## 📄 许可证

MIT License - 开源免费使用

---

*One API to Rule Them All! 🤖*
