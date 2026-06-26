# OpenClaw Robot Skills

**Version:** 2.0.0  
**Author:** RobotQu  
**License:** MIT

## Description

用统一的 API 控制所有品牌的协作机器人

已支持品牌 (v2.0.0):
- ✅ OMRON TM v1.1.0 - 现场测试通过
- ✅ JAKA v1.1.0 - 代码审查通过
- ✅ DOBOT v1.0.0 - 仿真测试通过

项目愿景：让机器人控制像换电池一样简单
长期目标：支持 20+ 机器人品牌

## Features

- ✅ 统一 API 设计
- ✅ 6 轴关节控制
- ✅ 笛卡尔空间运动
- ✅ 数字 IO 控制
- ✅ 状态实时监控
- ✅ 完整的中文文档

## Requirements

- Python >= 3.6
- numpy (DOBOT)
- techmanpy >= 1.0.0 (TM)
- JAKA SDK (JAKA)

## Structure

```
submission/
├── tm-robot/          # TM Robot 技能
├── jaka-robot/        # JAKA 技能
└── dobot-robot/       # DOBOT 技能
```

## Usage

```python
# TM Robot
from tm_robot import TMRobot
robot = TMRobot("192.168.1.10")
await robot.connect()

# JAKA Robot
from jaka_robot import JAKARobot
robot = JAKARobot("192.168.1.10")
await robot.connect()

# DOBOT Robot
from dobot_api import DobotApiDashboard
dashboard = DobotApiDashboard("192.168.5.1", 29999)
dashboard.EnableRobot()
```

## Testing

- TM: 17/17 现场测试通过
- JAKA: API 审查通过
- DOBOT: 6 轴关节 100% 测试通过

## Support

- Website: https://robotqu.com
- Forum: https://robotqu.mbbs.cc
- Bilibili: Robot_Qu 机器人社区

## License

MIT License
