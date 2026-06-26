# TM Robot Skill

**Version:** 1.1.0  
**Author:** RobotQu  
**License:** MIT

## Description

OMRON TM 协作机器人控制技能，支持状态监控、运动控制、安全功能等。

## Features

- ✅ 状态监控（关节、位姿、力矩、错误码）
- ✅ 运动控制（关节 PTP、直线 LIN、圆弧 ARC）
- ✅ 安全功能（急停、报警复位）
- ✅ 相机支持（手眼相机位姿）
- ✅ IO 控制（DI 读取）

## Requirements

- Python >= 3.6
- techmanpy >= 1.0.0

## Usage

```python
from tm_robot import TMRobot

robot = TMRobot("192.168.1.10")
await robot.connect()

# 获取状态
joints = await robot.get_joints()
pose = await robot.get_pose()

# 运动控制
await robot.move_joint([0, 0, 90, 0, 90, 0], speed=50)
await robot.move_line([100, 0, 0], speed=50)

await robot.disconnect()
```

## Testing

- 现场测试通过 (17/17)
- 测试环境：OMRON TM5M-700, TMflow 1.80.5300

## Support

- Website: https://robotqu.com
- Forum: https://robotqu.mbbs.cc
