# JAKA Robotics Control Skill

节卡机器人控制技能，支持 Zu20/Zu12/Zu7/MiniCobo 全系列协作机器人。

## 功能特性

- ✅ 关节运动控制
- ✅ 直线运动控制
- ✅ 状态读取
- ✅ 末端工具 I/O 控制
- ✅ gRPC 通信（低延迟、高可靠）

## 快速开始

### 1. 安装 JAKA SDK

```bash
pip install jaka-sdk
```

或访问 JAKA 官网下载：
https://www.jaka.com/docs/guide/SDK/introduction.html

### 2. 配置机器人 IP

编辑 `jaka_cmd.py`，修改：
```python
ROBOT_IP = "192.168.57.128"  # 改成你的 MiniCobo IP
```

### 3. 使用 Python API

```python
from jaka_skill import JAKARobot

robot = JAKARobot("192.168.57.128", use_grpc=True)
robot.connect()

# 关节运动 (弧度)
robot.move_joint([0, 0, 0, 0, 0, 0], speed=0.5)

# 直线运动 (mm, rad)
robot.move_linear([300, 0, 200, 3.14, 0, 0], speed=100)

# 读取状态
state = robot.get_state()
print(state['joints_deg'])

robot.disconnect()
```

### 4. 命令行工具

```bash
# 读取状态
python jaka_cmd.py state

# 回零
python jaka_cmd.py home

# 关节运动 (角度)
python jaka_cmd.py joint 90 90 90 90 90 90

# 直线运动 (mm, 度)
python jaka_cmd.py linear 300 0 200 180 0 0
```

## 支持机型

- JAKA Zu20（实验室主力）
- JAKA Zu12
- JAKA Zu7
- JAKA MiniCobo（本技能测试机型）

## 环境要求

- Python 3.8+
- JAKA SDK V2.3.1+
- Windows

## 安全提示

⚠️ 首次使用前请确保：
- 工作空间内无人
- 急停按钮可用
- 先在低速环境测试
- T1 模式调试

## 作者

JMO / Robotqu (青岛)
- 网站：robotqu.com
- B 站：Robot_Qu 机器人社区

## 许可证

MIT-0
