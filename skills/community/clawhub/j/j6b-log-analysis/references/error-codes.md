# 常见错误识别和解决建议

## 错误识别流程

```
1. 定位问题模块 → 2. 查看相关日志 → 3. 匹配错误模式 → 4. 分析可能原因 → 5. 提供解决建议
```

---

## 常见错误模式

### 1. 感知丢失目标

**日志特征**：
```
Found 0 obstacles
Detection failed
No object detected
```

**可能原因**：
- 传感器被遮挡（灰尘、水渍、遮挡物）
- 光照条件不佳（过暗、过亮、强反光）
- 传感器标定参数偏差
- 传感器数据异常

**建议排查步骤**：
1. 检查传感器是否清洁
2. 查看传感器连接状态
3. 查看 calibration/ 目录下的标定参数
4. 检查 `image_preprocess` 模块日志

**相关日志**：
```bash
grep -i "obstacle\|detect\|found 0" /app/apa/log/{od,rd}/*.log
```

---

### 2. 规划失败

**日志特征**：
```
Path planning failed
No valid path
Planning timeout
```

**可能原因**：
- 感知输入异常（无有效障碍物或车位）
- 地图数据异常
- 起点/终点无效
- 规划参数配置错误

**建议排查步骤**：
1. 检查感知模块输出是否正常
2. 查看地图和定位状态
3. 检查 `/app/apa/planning/etc/` 配置参数

**相关日志**：
```bash
grep -i "plan\|path\|failed" /app/apa/log/planning/*.log
```

---

### 3. 定位漂移

**日志特征**：
```
Pose drift detected
Localization error
Pose jump
```

**可能原因**：
- GNSS信号丢失或漂移
- IMU数据异常
- 特征匹配失败
- 标定参数错误

**建议排查步骤**：
1. 查看GNSS和IMU数据质量
2. 检查传感器连接
3. 查看 calibration/ 下的标定参数

**相关日志**：
```bash
grep -i "drift\|localization\|pose" /app/apa/log/loc/*.log
```

---

### 4. CAN通信异常

**日志特征**：
```
CAN timeout
CAN frame lost
Communication error
```

**可能原因**：
- CAN线路连接问题
- 其他ECU异常
- 带宽占用过高

**建议排查步骤**：
1. 检查CAN线束连接
2. 查看各CAN通道状态
3. 检查板端网络配置

**CAN端口映射**：
| 板端CAN | 车端CAN |
|---------|---------|
| DWCAN7 | PCAN |
| DWCAN4 | CCAN |
| DWCAN6 | S1CAN |
| DWCAN1 | S2CAN |

**相关日志**：
```bash
grep -i "can\|timeout\|frame lost" /app/apa/log/sensorcenter/*.log
```

---

### 5. 进程崩溃/重启

**日志特征**：
```
Segmentation fault
Bus error
Process crashed
Process restart
```

**可能原因**：
- 空指针访问
- 内存越界
- 资源耗尽
- 依赖服务异常

**建议排查步骤**：
1. 查看 coredump 文件
2. 查看系统日志 slog2info
3. 查看重启原因 reset_reason.txt
4. 检查内存使用情况

**相关命令**：
```bash
# 查找coredump
ls -la /log/coredump/

# 查看重启原因
cat /log/reset_reason.txt

# 查看系统崩溃日志
slog2info | grep -i "crash\|segmentation"

# 检查内存
cat /log/lowmem.dmesg.txt
```

---

### 6. 系统性能问题

**日志特征**：
```
High CPU usage
System lag
Timeout
Response slow
```

**可能原因**：
- 某个进程资源占用过高
- 多进程竞争资源
- 死锁或循环等待

**建议排查步骤**：
1. 使用 `hogs -i` 找出资源占用大户
2. 使用 `top -p <PID>` 查看进程详情
3. 检查线程状态（Mtx/Sem 表示锁竞争）

**相关命令**：
```bash
# 快速定位占用CPU的进程
hogs -i -s 1

# 查看特定进程
top -p <PID>

# 查看所有planning相关进程
pidin | grep -E "planning|od|rd|loc|psd|sensorcenter"
```

---

## 错误日志搜索技巧

### 搜索关键词

```bash
# 搜索错误
grep -i "error" /app/apa/log/*/*.log

# 搜索失败
grep -i "fail" /app/apa/log/*/*.log

# 警告信息
grep -i "warn" /app/apa/log/*/*.log

# 崩溃相关
grep -i "crash\|segmentation\|abort" /app/apa/log/*/*.log

# 超时
grep -i "timeout" /app/apa/log/*/*.log
```

### 多模块联合搜索

```bash
# 查找最近10分钟的所有错误日志
find /app/apa/log/ -name "*.log" -mmin -10 -exec grep -l "error" {} \;

# 统计各模块错误数量
for dir in /app/apa/log/*/; do echo "$dir: $(grep -c "error" $dir/*.log 2>/dev/null)"; done
```

---

## Coredump分析

### 查找Coredump

```bash
ls -la /log/coredump/
```

### 分析步骤

1. **查看崩溃时的系统日志**
   ```bash
   slog2info | grep -A 20 "crash\|segmentation"
   ```

2. **查看重启原因**
   ```bash
   cat /log/reset_reason.txt
   ```

3. **查看内存状态**
   ```bash
   cat /log/lowmem.dmesg.txt
   cat /log/lowmem.ps.txt
   ```

4. **下载coredump到本地分析**
   ```bash
   scp root@192.168.1.10:/log/coredump/* ./
   ```

---

## 联系支持

如果以上方法无法解决问题，请收集以下信息：

1. 相关模块日志文件
2. 系统日志（slog2info输出）
3. coredump文件（如有）
4. 复现步骤
5. 问题截图或录屏
