# DOBOT CR10A 快速参考卡片

## 🔌 连接
```python
dashboard = DobotApiDashboard("192.168.5.1", 29999)
feedback = DobotApiFeedBack("192.168.5.1", 30004)
```

## ⚡ 快速使能
```python
dashboard.ClearError()
dashboard.EnableRobot()
sleep(1)
```

## 🎯 运动控制

### 关节空间
```python
# MovJ(关节 1, 关节 2, 关节 3, 关节 4, 关节 5, 关节 6, 1)
dashboard.MovJ(0, 0, 90, 0, 90, 0, 1)
```

### 笛卡尔空间
```python
# MovJ(X, Y, Z, RX, RY, RZ, 0)
dashboard.MovJ(100, -250, 400, 180, 90, 0, 0)
```

## 📊 状态查询
```python
# 关节角度
joints = dashboard.GetAngle()  # {J1,J2,J3,J4,J5,J6}

# 笛卡尔坐标
pose = dashboard.GetPose()     # {X,Y,Z,RX,RY,RZ}
```

## 🔘 数字 IO
```python
dashboard.DO(1, 1)   # DO1 ON
dashboard.DO(1, 0)   # DO1 OFF
result = dashboard.DI(1)  # 读取 DI1
```

## ⚙️ 参数设置
```python
dashboard.SpeedFactor(50)  # 速度 50%
dashboard.AccJ(50)         # 关节加速度 50%
dashboard.AccL(50)         # 直线加速度 50%
```

## 🔧 坐标系
- `coordinateMode=0` → 笛卡尔坐标 {X,Y,Z,RX,RY,RZ}
- `coordinateMode=1` → 关节坐标 {J1,J2,J3,J4,J5,J6}

## ⚠️ 错误码
- `0` → 成功
- `-1` → 参数错误
- `-2` → 功能不支持 (仿真)
- `-40001` → IO 索引无效

## 🛑 安全关闭
```python
dashboard.DisableRobot()
dashboard.close()
feedback.close()
```

## 📝 关节范围
| 轴 | 范围 |
|----|------|
| J1 | ±180° |
| J2 | ±135° |
| J3 | ±150° |
| J4 | ±180° |
| J5 | ±180° |
| J6 | ±360° |

## 💡 提示
1. 首次使用先在仿真环境测试
2. 真机操作注意工作空间安全
3. 奇异点位置可能触发保护
4. 定期备份重要程序

---
*快速参考 v1.0 - 2026-04-01*
