# DOBOT Robot Skill

**Version:** 1.0.0  
**Author:** RobotQu  
**License:** MIT

## Description

DOBOT CR10A 机械臂 Python SDK，支持 6 轴关节控制、笛卡尔运动、IO 控制等。

## Features

- ✅ 6 轴关节空间控制
- ✅ 笛卡尔空间运动
- ✅ 数字 IO 控制
- ✅ 状态实时监控
- ✅ 丰富的测试脚本
- ✅ 详细的中文文档

## Requirements

- Python >= 3.6
- numpy

## Usage

```python
from dobot_api import DobotApiDashboard

dashboard = DobotApiDashboard("192.168.5.1", 29999)

# 使能
dashboard.EnableRobot()

# 关节空间运动
dashboard.MovJ(0, 0, 90, 0, 90, 0, 1)

# 笛卡尔空间运动
dashboard.MovJ(100, -250, 400, 180, 90, 0, 0)

# 获取状态
joints = dashboard.GetAngle()
pose = dashboard.GetPose()

# 下使能
dashboard.DisableRobot()
dashboard.close()
```

## Testing

- 仿真测试通过
- 6 轴关节控制 100% 可用
- 测试环境：DOBOT CR10A (仿真)

## Support

- Website: https://robotqu.com
- Forum: https://robotqu.mbbs.cc
- Bilibili: Robot_Qu 机器人社区
