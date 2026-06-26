# QNX性能分析方法详解

## 概述

J6B板端使用QNX实时操作系统，性能分析与Linux有所不同。本章介绍如何使用QNX工具进行性能分析。

---

## 工具对比

| 工具 | 用途 | 优势 | 适用场景 |
|------|------|------|----------|
| **hogs** | 进程级资源定位 | 快速、直观、占用少 | 快速找出资源占用大户 |
| **top** | 系统全景监控 | 全面、可排序、线程状态 | 详细分析进程状态 |
| **pidin** | 进程详情查看 | 信息丰富、QNX特有 | 查看进程详细信息 |

---

## hogs - 进程级"资源大户"定位器

### 基本用法

```bash
hogs                          # 默认每3秒刷新，按PID排序
hogs -i                       # 按占用率排序（最常用）
hogs -s 1                     # 每1秒更新一次
hogs -n                       # 只显示进程名，不显示完整路径
hogs -i -s 1                  # 组合使用：按占用率+1秒刷新
```

### 输出说明

```
PID       PIDS      MSEC    SYS     NAME
235527   18%       2253    75%     ./image_preprocess
240033    2%        330    11%     ./perception_od
241262    0%         18     0%     ./perception_rd
```

| 列 | 说明 |
|----|------|
| PID | 进程ID |
| PIDS | CPU占用百分比 |
| MSEC | 在采样窗口内占用的CPU毫秒数 |
| SYS | 内核态时间占比 |
| NAME | 进程名称 |

### 典型问题诊断

| 现象 | PIDS | SYS | 可能原因 |
|------|------|-----|----------|
| 正常计算 | 10-30% | 10-30% | 正常 |
| 疯狂计算 | >50% | <30% | 算法过重或死循环 |
| 系统调用过多 | >50% | >70% | 频繁系统调用、I/O密集 |

### 实战案例

**场景**：系统突然变卡，怀疑某个算法模块疯跑

```bash
# 执行命令
hogs -i -s 1
```

**观察**：如果发现某个进程的PIDS长期处于50%以上，且SYS比例很高

**结论**：该进程可能陷入死循环或系统调用过于频繁

---

## top - 系统级"全能监控台"

### 基本用法

```bash
top                          # 查看系统全景
top -p <PID>                 # 查看特定进程
top -p 12345,67890           # 查看多个进程
```

### 交互操作

| 按键 | 功能 |
|------|------|
| o + 列名 | 按指定列排序（如：`o cpu`） |
| ? | 帮助界面 |
| q | 退出 |
| space | 立即刷新 |

### 输出说明

```
root@hobot:/# top
Computing times...
112 processes; 1676 threads;
CPU states: 51.6% user, 0.9% kernel
Memory: 12287M total, 2562M avail, page size 4K
PID  TID PRI STATE       HH:MM:SS    CPU COMMAND
2945117  153  10 Rply       00:09:45  1.93% mainboard2
2945117  184  10 CdV        00:10:21  1.76% mainboard2
2945117   30   1 Mtx        00:04:54  1.13% mainboard2
```

| 部分 | 说明 |
|------|------|
| CPU states | user=用户态，kernel=内核态 |
| Memory | avail=可用内存，如果<500M需要关注 |
| STATE | 线程状态（见下表） |

### 线程状态（STATE列）

| 状态 | 说明 | 正常？ |
|------|------|--------|
| Run | 正在运行 | ✅ |
| Rply | 等待CPU调度 | ✅ |
| NSlp | 正常休眠 | ✅ |
| Mtx | 等待互斥锁 | ⚠️ 长时间可能有问题 |
| Sem | 等待信号量 | ⚠️ 长时间可能有问题 |
| Rcv | 等待接收消息 | ✅ |
| CdV | 等待条件变量 | ✅ |

### 典型问题诊断

| 现象 | STATE | 可能原因 |
|------|-------|----------|
| 正常 | Run/Rply/NSlp | 正常计算 |
| 锁竞争 | 长时间Mtx/Sem | 程序内部存在锁竞争 |
| 死锁 | 大量线程Mtx/Sem | 可能死锁 |

### 实战案例

**场景1**：系统内存告急

```bash
# 1. 查看内存状态
top

# 观察：查看Memory行的avail值
# 如果avail < 500M，说明内存紧张
```

**场景2**：怀疑多线程程序中有线程死锁

```bash
# 1. 查看进程线程状态
top -p <PID>

# 2. 观察STATE列
# 如果很多线程长时间卡在Mtx或Sem，说明存在严重锁竞争
```

---

## 性能分析标准流程

### 方式一：一键监控（推荐）

```
运行monitor_cpu.sh → 实时查看彩色输出 → 定位问题进程 → 深入分析
```

**启动方式**：
```bash
# 前台运行（实时查看）
/userdata/monitor_cpu.sh

# 后台运行（长期监控）
nohup /userdata/monitor_cpu.sh > /dev/null 2>&1 &
```

**输出解读**：
- 🔴 **红色进程**：CPU > 20%，需要关注
- 🟡 **黄色进程**：内存 > 10000K，可能内存占用高
- 📊 **TOP 15**：快速定位资源占用大户
- 📝 **自动日志**：保存到 `/userdata/log/cpu_monitor/`

### 方式二：手动三步法

```
第一步：hogs -i → 找出占用CPU的进程
第二步：top -p <PID> → 查看该进程详情
第三步：分析 → 判断是算法太重还是逻辑锁死
```

### 示例

```bash
# 第一步：找出占用CPU的进程
hogs -i
# 发现 planning 进程占用 25%

# 第二步：查看该进程详情
top -p <planning的PID>

# 第三步：分析
# - 如果线程状态多为 Run：算法太重，需优化
# - 如果很多线程卡在 Mtx/Sem：存在锁竞争，需检查代码
```

### 诊断结论速查表

| PIDS | SYS | STATE | 可能原因 | 解决方法 |
|------|-----|-------|----------|----------|
| >50% | <30% | 多Run | 算法过重 | 优化算法、降低频率 |
| >50% | >70% | 多Run | 死循环/系统调用频繁 | 检查代码逻辑 |
| 正常 | 正常 | 多Mtx/Sem | 锁竞争 | 减小锁粒度、缩短持锁时间 |
| 正常 | 正常 | 多NSlp | 正常 | 无需处理 |
| 高 | 高 | 多Mtx/Sem | 可能死锁 | 检查锁逻辑 |

---

## 常见性能问题及诊断

### 1. 单个进程占用过高

**症状**：某个PIDS持续>50%

**诊断**：
```bash
hogs -i -s 1
top -p <PID>
```

**可能原因**：
- 死循环
- 算法复杂度过高
- 频繁系统调用

**解决**：
- 检查代码逻辑
- 优化算法
- 减少系统调用

---

### 2. 内存不足

**症状**：Memory avail < 500M

**诊断**：
```bash
top
cat /log/lowmem.dmesg.txt
```

**可能原因**：
- 内存泄漏
- 缓存过大
- 数据结构过大

**解决**：
- 重启相关进程
- 减少缓存大小
- 检查内存泄漏

---

### 3. 锁竞争严重

**症状**：大量线程卡在Mtx/Sem

**诊断**：
```bash
top -p <PID>
# 观察STATE列
```

**可能原因**：
- 锁粒度过大
- 持锁时间过长
- 死锁

**解决**：
- 减小锁粒度
- 缩短持锁时间
- 检查死锁

---

## 监控脚本示例

### monitor_cpu.sh - 综合CPU监控脚本（推荐）

**功能特性**：
- 彩色输出，实时监控
- CPU占用TOP15排名
- 内存占用TOP15排名
- 系统概要和统计信息
- 日志自动记录
- 自动清理7天前的旧日志

**使用方法**：

```bash
# 上传脚本到板端
scp /path/to/monitor_cpu.sh root@192.168.1.10:/userdata/

# SSH登录板端
ssh root@192.168.1.10

# 添加执行权限
chmod +x /userdata/monitor_cpu.sh

# 运行监控
/userdata/monitor_cpu.sh

# 后台运行
nohup /userdata/monitor_cpu.sh > /dev/null 2>&1 &

# 查看日志
tail -f /userdata/log/cpu_monitor/cpu_monitor_*.log
```

**配置参数**（可在脚本开头修改）：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| INTERVAL | 3 | 刷新间隔（秒） |
| LOG_DIR | /userdata/log/cpu_monitor | 日志目录 |
| MAX_LOG_DAYS | 7 | 日志保留天数 |

**输出示例**：
```
【系统概要】
  IDLE   60.7%  Idle
  ...
【hogs CPU占用 TOP 15】
PID      CPU%    MEM     STACK   PATH
─────────────────────────────────────────────────
235527   18%     250K    64K     ./image_preprocess
240033    2%     180K    48K     ./perception_od
【统计摘要】
  进程数: 112, 线程数: 1676
  内存: FreeMem: 2562M
```

### 持续监控资源占用

```bash
#!/bin/bash
# 监控资源占用，保存到文件

while true; do
    echo "===== $(date) =====" >> /tmp/resource_monitor.log
    hogs -i >> /tmp/resource_monitor.log
    sleep 60
done
```

### 定期快照

```bash
#!/bin/bash
# 每分钟保存一次进程快照

while true; do
    pidin > /tmp/pidin_$(date +%Y%m%d_%H%M%S).txt
    sleep 60
done
```

---

## 性能优化建议

| 优化方向 | 具体措施 |
|----------|----------|
| 算法优化 | 减少计算复杂度、使用更高效的算法 |
| 并发优化 | 减小锁粒度、使用无锁数据结构 |
| 内存优化 | 减少内存分配、使用对象池 |
| I/O优化 | 批量读写、异步I/O |
| 日志优化 | 减少日志频率、使用日志级别 |

---

## 与Linux命令对比参考

| 功能 | QNX | Linux |
|------|-----|-------|
| 进程查看 | `pidin` | `ps` |
| 实时监控 | `top`, `hogs` | `top`, `htop` |
| 结束进程 | `slay` | `kill` |
| 系统日志 | `slog2info` | `journalctl` |
| 内存信息 | `showmem` | `free` |
