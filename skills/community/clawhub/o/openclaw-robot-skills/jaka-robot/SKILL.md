# JAKA Robotics Control Skill

**Version:** 1.1.0  
**Author:** RobotQu  
**License:** MIT

## Description

JAKA 协作机器人控制技能，支持关节运动、直线运动、状态读取等。

## Features

- ✅ 关节运动
- ✅ 直线运动
- ✅ 状态读取
- ✅ IO 控制

## Requirements

- Python >= 3.6
- JAKA SDK (需要单独安装)

## Usage

```python
from jaka_robot import JAKARobot

robot = JAKARobot("192.168.1.10")
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

- 代码审查通过
- API 规范符合

## Support

- Website: https://robotqu.com
- Forum: https://robotqu.mbbs.cc
