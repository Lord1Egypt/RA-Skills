# JAKA Robotics Control Skill 使用说明

## ⚠️ 重要参数说明

### 直线运动速度参数

```python
robot.move_linear([x, y, z, rx, ry, rz], speed=200)
```

**speed 参数单位：mm/s**（不是倍率！）

| speed 值 | 实际速度 | 说明 |
|----------|----------|------|
| 100 | 100mm/s | 低速，精确操作 |
| 200 | 200mm/s | 中速，默认值 |
| 400 | 400mm/s | 高速 |
| 750 | 750mm/s | 最大速度（取决于机器人型号） |

### 常见错误

```python
# ❌ 错误理解：以为是倍率
robot.move_linear(target, speed=0.5)  # 实际只有 0.5mm/s！

# ✅ 正确用法
robot.move_linear(target, speed=200)  # 200mm/s
```

---

## 🚀 快速开始

### 1. 连接机器人

```python
from jaka_skill import JAKARobot

robot = JAKARobot("192.168.28.18")
robot.connect()
robot.enable_robot()
```

### 2. 关节运动

```python
import math

# 所有关节到 90 度
robot.move_joint([math.pi/2, 0, math.pi/2, 0, math.pi/2, 0], speed=0.5)
```

### 3. 直线运动

```python
# 沿 X 轴移动 20mm，速度 200mm/s
state = robot.get_state()
tcp = state['tcp_position']
target = [tcp[0]+20, tcp[1], tcp[2], tcp[3], tcp[4], tcp[5]]
robot.move_linear(target, speed=200)
```

---

## 📋 API 参考

### move_joint(joints, speed)

关节运动

| 参数 | 类型 | 说明 |
|------|------|------|
| joints | List[float] | 6 个关节角度（**弧度**） |
| speed | float | 速度倍率 0.0-1.0 |

**示例：**
```python
# J1 旋转 90 度
robot.move_joint([1.57, 0, 0, 0, 0, 0], speed=0.5)
```

---

### move_linear(pose, speed)

直线运动

| 参数 | 类型 | 说明 |
|------|------|------|
| pose | List[float] | [x,y,z,rx,ry,rz] (mm, 度) |
| speed | float | **速度 mm/s**（重要！） |

**示例：**
```python
# 沿 Z 轴向上 50mm
robot.move_linear([0, 0, 50, 0, 0, 0], speed=300)
```

---

## 🔧 底层 SDK API

本技能封装了 JAKA SDK 的以下 API：

### linear_move_extend

```python
robot.linear_move_extend(end_pos, move_mode, is_block, speed, acc, tol)
```

| 参数 | 单位 | 说明 |
|------|------|------|
| speed | **mm/s** | 笛卡尔空间速度 |
| acc | **mm/s²** | 加速度 |
| tol | **mm** | 终点误差 |

**官方文档：** https://www.jaka.com/docs/guide/SDK/Python.html

---

## ⚡ 性能参考

| 速度设置 | 实际速度 | 20mm 耗时 |
|----------|----------|-----------|
| 100mm/s | ~50mm/s | ~0.4s |
| 200mm/s | ~100mm/s | ~0.2s |
| 400mm/s | ~150mm/s | ~0.15s |

*实际速度受机器人负载、姿态等影响*

---

## 🐛 常见问题

### Q: 直线运动速度很慢？
**A:** 检查 speed 参数是否误用了倍率（如 0.5），应该是 mm/s（如 200）

### Q: 直线运动不执行？
**A:** 
1. 确认 J3=90°, J5=90° 姿态
2. 检查机器人是否已使能
3. 使用非阻塞模式 + 轮询

### Q: 移动距离不准确？
**A:** 调整 tol 参数（默认 0.1mm）

---

## 📝 更新日志

- **2026-03-27**: 修复速度参数单位问题（倍率 → mm/s）
- **2026-03-27**: 使用 linear_move_extend API
- **2026-03-23**: 初始版本

---

## 📚 参考资料

- [JAKA SDK 官方文档](https://www.jaka.com/docs/guide/SDK/Python.html)
- [JAKA SDK 下载](https://www.jaka.com/docs/guide/SDK/introduction.html)
- [RobotQu 社区](https://robotqu.com)
