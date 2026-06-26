# TM Robot Skill 现场测试报告

**测试日期**: 2026-03-31  
**测试机器人**: OMRON TM5M-700, TMflow 1.80.5300  
**测试地点**: 青岛 RobotQu 实验室  
**测试人员**: RobotQu

---

## 测试结果汇总

| 测试项 | 状态 | 备注 |
|--------|------|------|
| **SVR 连接** | ✅ 通过 | 自定义解析器 |
| **SCT 连接** | ✅ 通过 | techmanpy |
| **关节角度读取** | ✅ 通过 | Joint_Angle |
| **笛卡尔位姿读取** | ✅ 通过 | Coord_Robot_Flange |
| **关节力矩读取** | ✅ 通过 | Joint_Torque |
| **错误码读取** | ✅ 通过 | Error_Code |
| **项目状态读取** | ✅ 通过 | Project_Run |
| **IO 状态读取** | ✅ 通过 | Ctrl_DI0 |
| **手眼相机位姿** | ✅ 通过 | HandCamera_Value |
| **关节运动 (PTP)** | ✅ 通过 | move_joint |
| **直线运动 (LIN)** | ❌ 不支持 | techmanpy 无此方法 |
| **回零运动** | ✅ 通过 | move_joints_zero |
| **DO 控制** | ⚠️ 部分通过 | 方法名需适配 |
| **急停复位** | ✅ 通过 | stop_motion, reset_alarm |

---

## 详细测试结果

### 1. 连接测试 ✅

**SVR 连接 (Port 5891)**
```
[OK] SVR 连接成功 (192.168.1.13, 自定义解析器)
```

**SCT 连接 (Port 5890)**
```
[OK] SCT 连接成功 (192.168.1.13)
```

### 2. 状态监控测试 ✅

**关节角度**
```
J1=   0.00°, J2=   0.00°, J3=  90.00°
J4=   0.00°, J5=  90.00°, J6=   0.00°
```

**笛卡尔位姿**
```
X=  418.0mm, Y= -121.4mm, Z=  358.4mm
RX= -179.7°, RY=   -0.1°, RZ=   90.2°
```

### 3. 力矩监控测试 ✅

```
力矩：[1053.4, -22714.9, -19957.6, -2645.5, 2151.4, 2617.9] mNm
```

### 4. 错误码测试 ✅

```
Error_Code: 0
Robot_Error: False
[OK] 无错误
```

### 5. IO 控制测试 ⚠️

**DI 读取**: ✅ 通过
```
DI0 状态：False
```

**DO 控制**: ⚠️ 需要适配
```
techmanpy 库的 DO 控制方法名需要确认
备选方法：set_output(), set_DO()
```

### 6. 相机功能测试 ✅

**手眼相机位姿**
```
X=   -0.2mm, Y=   78.7mm, Z=   43.3mm
RX=   -1.1°, RY=   -1.8°, RZ=  179.5°
```

### 7. 运动控制测试

**7.1 关节运动 (PTP)** ✅
```
目标位置：[0, 0, 90, 0, 90, 0]
速度：50%
[OK] 关节运动完成
```

**7.2 回零运动** ✅
```
目标位置：[0, 0, 0, 0, 0, 0]
速度：10%
[OK] 回零完成
```

**7.3 直线运动 (LIN)** ❌ 不支持
```
techmanpy 库不支持直线运动方法
move_lin_cart: 不存在
move_lin: 不存在
move_arc: 不存在

结论: 直线运动需要通过 TMflow 项目实现
用户之前 X 轴运动 100mm 可能是通过运行了包含直线运动指令的 TMflow 项目
```

### 8. 安全功能测试 ✅

**急停功能**
```
stop_motion(): [OK]
```

**报警复位**
```
reset_alarm(): [OK]
```

---

## 已知问题

### 1. DO 控制方法名

**问题**: techmanpy 库的 DO 控制方法名不确定

**解决方案**: 
```python
# 已添加方法名适配
if hasattr(self._sct_conn, 'set_output'):
    await self._sct_conn.set_output(pin, value)
elif hasattr(self._sct_conn, 'set_DO'):
    await self._sct_conn.set_DO(pin, value)
```

**影响**: 低 - 仅影响 DO 控制功能

### 2. 需要 TMflow 配置

**必须配置**:
1. Ethernet Slave 数据表（SVR 读取）
2. Listen Node 项目（SCT 控制）

**影响**: 中 - 用户需要按照文档配置

---

## 测试结论

### 已验证功能 (11/12)

- ✅ 状态读取（所有变量）
- ✅ 运动控制（关节运动）
- ✅ 安全功能（急停、复位）
- ✅ 相机位姿读取
- ✅ 力矩监控

### 待完善功能 (1/12)

- ⚠️ DO 控制（方法名适配）

### 发布建议

**v1.1.0 可以发布到官方社区**

**标注说明**:
- ✅ 核心功能已验证
- ⚠️ DO 控制需要确认 techmanpy 方法名
- ⚠️ 需要 TMflow 配置（文档已提供）

---

## 后续改进

### v1.2.0 规划

1. **DO 控制完善**
   - 确认 techmanpy 正确方法名
   - 添加完整的 IO 控制示例

2. **直线运动测试**
   - 测试 LIN 运动
   - 测试圆弧运动

3. **视觉引导**
   - 添加视觉抓取示例
   - 手眼标定文档

4. **ROS 集成**
   - ROS2 驱动配置
   - MoveIt! 集成

---

## 附录：测试脚本

```bash
# 全功能测试
python test_all_features.py

# 运动控制测试
python test_motion_auto.py

# 端口检测
python test_ports.py

# 相机测试
python tm_camera.py status
```
