# 日志文件路径详细说明

## 日志系统概述

### 路径信息

| 项目 | 路径 | 说明 |
|------|------|------|
| **主日志路径** | `/app/apa/log/` | 泊车算法日志文件存放目录 |
| **Coredump路径** | `/log/coredump/` | 程序崩溃堆栈信息 |
| **系统日志** | `/log/` | 系统诊断与日志（含reset_reason.txt等） |

### 写入机制

- **写入方式**: 轮转循环写入
- **目的**: 保证EMMC不超过使用上限
- **说明**: 旧日志会被自动覆盖，重要日志需及时下载

---

## 各模块日志目录

### 1. dr - 航迹推算模块

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/dr/` |
| **模块路径** | `/app/apa/dr/` |
| **功能** | 航迹推算（Dead Reckoning） |

**查看日志**:
```bash
ls -la /app/apa/log/dr/
tail -f /app/apa/log/dr/*.log
```

---

### 2. loc - 定位建图模块

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/loc/` |
| **模块路径** | `/app/apa/loc/` |
| **功能** | 定位建图（Localization） |

**查看日志**:
```bash
ls -la /app/apa/log/loc/
tail -f /app/apa/log/loc/*.log
```

---

### 3. sensorcenter - 传感器中心

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/sensorcenter/` |
| **模块路径** | `/app/apa/sensorcenter/` |
| **功能** | 传感器数据采集与分发 |

**查看日志**:
```bash
ls -la /app/apa/log/sensorcenter/
tail -f /app/apa/log/sensorcenter/*.log
```

**同时查看模块内的日志**:
```bash
ls -la /app/apa/sensorcenter/bin/log/
```

---

### 4. image_preprocess - 图像预处理模块

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/image_preprocess/` |
| **模块路径** | `/app/apa/image_preprocess/` |
| **功能** | 图像预处理（畸变校正、ROI提取等） |

**查看日志**:
```bash
ls -la /app/apa/log/image_preprocess/
tail -f /app/apa/log/image_preprocess/*.log
```

---

### 5. od - 目标检测模块

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/od/` |
| **模块路径** | `/app/apa/od/` |
| **功能** | 目标检测（Object Detection） |

**查看日志**:
```bash
ls -la /app/apa/log/od/
tail -f /app/apa/log/od/*.log
```

---

### 6. rd - 车位检测模块

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/rd/` |
| **模块路径** | `/app/apa/rd/` |
| **功能** | 车位检测（Road Detection） |

**查看日志**:
```bash
ls -la /app/apa/log/rd/
tail -f /app/apa/log/rd/*.log
```

---

### 7. psd - 车位融合模块

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/psd/` |
| **模块路径** | `/app/apa/psd/` |
| **功能** | 车位融合（Parking Spot Detection） |

**查看日志**:
```bash
ls -la /app/apa/log/psd/
tail -f /app/apa/log/psd/*.log
```

**查看data数据**:
```bash
ls -la /app/apa/psd/etc/data1-6/
```

---

### 8. gridmap - 栅格地图融合模块

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/gridmap/` |
| **模块路径** | `/app/apa/gridmap/` |
| **功能** | 栅格地图融合 |

**查看日志**:
```bash
ls -la /app/apa/log/gridmap/
tail -f /app/apa/log/gridmap/*.log
```

**同时查看模块日志**:
```bash
ls -la /app/apa/gridmap/gridmap_log/
```

---

### 9. planning - 规划控制模块

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/planning/` |
| **模块路径** | `/app/apa/planning/` |
| **功能** | 路径规划与控制 |

**查看日志**:
```bash
ls -la /app/apa/log/planning/
tail -f /app/apa/log/planning/*.log
```

**查看data数据**:
```bash
ls -la /app/apa/planning/etc/data1-6/
```

---

### 10. ui_control - UI控制

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/ui_control/` |
| **模块路径** | `/app/apa/ui_control/` |
| **功能** | 界面控制 |

**查看日志**:
```bash
ls -la /app/apa/log/ui_control/
tail -f /app/apa/log/ui_control/*.log
```

---

### 11. perception_fusion - 感知融合

| 项目 | 信息 |
|------|------|
| **日志路径** | `/app/apa/log/perception_fusion/` |
| **模块路径** | `/app/apa/perception_fusion_J6cam/` |
| **功能** | 多传感器感知融合 |

**查看日志**:
```bash
ls -la /app/apa/log/perception_fusion/
tail -f /app/apa/log/perception_fusion/*.log
```

---

## 快速查找命令

```bash
# 查看所有模块日志目录
ls -la /app/apa/log/

# 查找特定模块的日志文件
find /app/apa/log/ -name "*planning*" -type f

# 查看所有日志文件大小
du -sh /app/apa/log/*/

# 查找最近的日志文件
find /app/apa/log/ -name "*.log" -type f -mtime -1

# 查找包含错误关键词的日志
grep -l "error" /app/apa/log/*/*.log
```

---

## 日志下载到本地

### 单个模块日志
```bash
scp root@192.168.1.10:/app/apa/log/planning/*.log ./
```

### 批量下载所有模块日志
```bash
scp root@192.168.1.10:/app/apa/log/*/*.log ./
```

### 打包下载
```bash
# 板端打包
ssh root@192.168.1.10 "tar czf /tmp/logs.tar.gz -C /app/apa/log ."

# 下载压缩包
scp root@192.168.1.10:/tmp/logs.tar.gz ./

# 本地解压
tar xzf logs.tar.gz
```

### 下载整个模块目录
```bash
scp -r root@192.168.1.10:/app/apa/log/planning/ ./
```
