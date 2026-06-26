# TM Robot 参考文档

## Ethernet Slave / SVR 配置

### 端口说明

| 端口 | 名称 | 用途 | 启用方式 |
|------|------|------|----------|
| **5890** | SCT / Listen Node | 运动控制 | 运行 Listen Node 项目 |
| **5891** | SVR / Ethernet Slave | 状态读取 | TMflow → Ethernet Slave 开启 |
| **5892** | STA | 状态广播 | 自动启用 |

### 配置步骤

#### 启用 Ethernet Slave（SVR）

1. TMflow → **Robot Setting** → **Ethernet Slave**
2. 点击开启
3. 配置数据表（添加需要的变量）
4. 设置通讯格式：**STRING** 或 **JSON**
5. 勾选 **写入允许**（如需外部写入）
6. 保存

#### 运行 Listen Node（SCT）

1. TMflow → 新建项目
2. 添加 **Listen Node**
3. 设置 Connection Timeout = 60000ms
4. 运行项目

### 通讯协议

```
$Header, Length, Data, *Checksum\r\n
```

- Header: `TMSVR`
- Mode: 0=响应状态, 1=BINARY, 2=STRING, 3=JSON

---

## 报警代码（RobotErrCode）

| 错误码 | 名称 | 含义 | 处理方法 |
|--------|------|------|----------|
| 0 | 无错误 | 正常运行 | - |
| E001 | Joint Limit Error | 关节角度超限 | 检查关节角度，重新归零 |
| E002 | Workspace Limit | 工作空间超限 | 移动机器人到安全位置 |
| E003 | Collision Detected | 碰撞检测触发 | 释放阻力，确认安全后复位 |
| E004 | E-Stop | 紧急停止触发 | 释放急停按钮，按复位 |
| E005 | Safety Door | 安全门打开 | 关闭安全门 |
| E006 | Motion Timeout | 运动超时 | 检查路径，增大超时时间 |
| E007 | Soft Limit | 软件限位触发 | 移动到安全位置 |
| E008 | Power Error | 电源异常 | 断电重启机器人 |
| E009 | Servo Error | 伺服异常 | 检查电机连接 |
| E010 | System Error | 系统错误 | 联系技术支持 |
| E011 | CRC Error | 通讯校验错误 | 检查网络连接 |
| E012 | Communication Timeout | 通讯超时 | 检查网线/Ping |
| E013 | Frame Error | 帧错误 | 重启通讯 |
| E014 | Command Error | 命令错误 | 检查命令格式 |
| E015 | Parameter Error | 参数错误 | 检查参数范围 |

## 通讯端口

| 端口 | 协议 | 用途 |
|------|------|------|
| 5890 | SCT | 实时控制（Listen Node） |
| 5891 | SVR | 状态读取（变量服务器） |
| 5892 | STA | 状态广播 |

## TMflow 常用变量

### 关节角度
```
Joint_Angle      # 当前关节角度 (J)
Joint_Target     # 目标关节角度 (J)
Joint_Actual     # 实际关节角度 (J)
```

### 笛卡尔位置
```
Pos_Actual       # 实际位置 (P): [x, y, z, rx, ry, rz]
Pos_Target       # 目标位置 (P)
Cartesian_Actual # 笛卡尔实际位置 (P)
```

### 机器人状态
```
RobotMode        # 机器人模式 (String)
RobotErrCode     # 错误码 (Int)
ProjectName      # 当前项目名 (String)
```

### 变量类型
- `J` = Joint angles (6 floats, degrees)
- `P` = Position (6 floats, mm + degrees)
- 空 = String/Int 类型

## 常见问题

### 连接超时
- 机器人离线或 IP 错误
- Listen Node 未启动
- 机器人处于报警状态（阻止新连接）

### 报警状态无法连接
- 报警状态下 SCT/SVR 连接都会被拒绝
- 必须先在机器人端手动复位
- 或断电重启

### 运动命令无响应
- 检查 RobotMode 是否为 Idle/Manual
- 确认急停未按下
- 检查碰撞检测是否触发

## 复位步骤

1. **TMflow 界面复位**：点击 "Reset" 或 "Acknowledge"
2. **控制器复位**：按下复位按钮
3. **断电重启**：关闭电源，等待 10 秒，重新开启
