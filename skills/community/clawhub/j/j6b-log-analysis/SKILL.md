---
name: j6b-log-analysis
description: J6B泊车系统日志读取和分析。支持：日志文件定位、日志读取、常见错误识别、日志下载、系统资源性能分析。使用场景：查看日志、分析报错、排查问题、性能诊断、下载日志到本地。触发词：日志、log、slog2info、tail、grep、报错、错误、异常、失败、故障、性能、CPU、占用、下载、scp。
---

# J6B泊车日志分析Skill

## 快速导航

| 参考文档 | 说明 |
|----------|------|
| [log-locations.md](references/log-locations.md) | 各模块日志路径详细说明 |
| [error-codes.md](references/error-codes.md) | 常见错误识别和解决建议 |
| [performance.md](references/performance.md) | QNX性能分析方法详解（含monitor_cpu.sh脚本） |
| [qnx-commands.md](references/qnx-commands.md) | QNX命令参考 |
| [troubleshooting.md](references/troubleshooting.md) | 故障排查案例库 |
| [report-template-system-resource.md](references/report-template-system-resource.md) | ⭐ 系统资源分析报告模板（必读） |

### 自动化脚本

| 脚本 | 说明 | 用法 |
|------|------|------|
| [monitor_cpu.sh](scripts/monitor_cpu.sh) | 综合CPU监控（彩色+日志） | `./monitor_cpu.sh` |
| [download_log.sh](scripts/download_log.sh) | 批量下载日志（打包/逐模块） | `./download_log.sh [-a] [-c IP] [模块名]` |
| [analyze_log.sh](scripts/analyze_log.sh) | 日志错误分析（模式识别+报告） | `./analyze_log.sh [-l] [-r] [模块名]` |

#### download_log.sh 使用

```bash
# 下载所有模块日志
./download_log.sh

# 下载单个模块
./download_log.sh planning

# 打包模式（大数据量推荐）
./download_log.sh -a

# 指定百兆网口
./download_log.sh -c 192.168.2.10 planning

# 指定保存目录
./download_log.sh -o /tmp/logs planning od rd
```

#### analyze_log.sh 使用

```bash
# 分析板端所有模块
./analyze_log.sh

# 分析指定模块
./analyze_log.sh planning od rd

# 分析本地已下载的日志
./analyze_log.sh -l planning

# 生成分析报告
./analyze_log.sh -r
```

---

## ⚠️ 报告输出规范

**当用户要求分析系统资源时，必须严格按照 [report-template-system-resource.md](references/report-template-system-resource.md) 模板输出。**

### 报告结构（7章）

| 章节 | 内容 |
|------|------|
| 第1章 系统健康度 | CPU/内存/进程数/线程数总览 + CPU统计(Min/Max/Avg/Idle) |
| 第2章 CPU占用 TOP 15 | 排名、进程名、CPU%、SYS%、判定 |
| 第3章 内存占用 TOP 15 | 排名、进程名、内存、判定 |
| 第4章 线程状态异常 | Mtx/Sem异常线程列表 |
| 第5章 泊车业务进程状态 | 13个业务进程的运行状态、PID、在线时长 |
| 第6章 TOP完整输出 | top命令原始输出 |
| 第7章 重点关注项 | 异常汇总 + 可能原因 + 排查建议 |

### 判定阈值

| 指标 | 🟢 正常 | 🟡 注意 | 🔴 告警 |
|------|---------|---------|---------|
| 单进程 CPU | < 10% | 10% ~ 50% | > 50% |
| 系统总 CPU | < 50% | 50% ~ 80% | > 80% |
| 单进程内存 | < 200M | 200M ~ 500M | > 500M |
| 可用内存 | > 2000M | 500M ~ 2000M | < 500M |
| 线程 Mtx/Sem | 0 个 | 1 ~ 3 个 | > 3 个 |

### 泊车业务进程清单（第5章必须覆盖）

sensorcenter, image_preprocess, perception_rd, perception_od, perception_fusion, dr, loc, pad, gridmap, planning, ui_control, adaptercom, nos_adasSimtool

---

## 常用操作速查

### F1: 日志文件定位

**主日志路径**: `/app/apa/log/`
**Coredump路径**: `/log/coredump`

各模块日志快速查找：

| 模块 | 命令 |
|------|------|
| planning | `ls -la /app/apa/log/planning/` |
| perception (od/rd) | `ls -la /app/apa/log/{od,rd}/` |
| loc | `ls -la /app/apa/log/loc/` |
| sensorcenter | `ls -la /app/apa/log/sensorcenter/` |
| 所有模块 | `ls -la /app/apa/log/` |

### F2: 基础日志读取

```bash
# 查看最新日志
tail -100 /app/apa/log/planning/*.log

# 实时跟踪
tail -f /app/apa/log/planning/*.log

# 搜索错误
grep -i "error" /app/apa/log/planning/*.log

# 查看系统日志
slog2info | grep -i planning
```

### F3: 日志下载

**网络信息**：
- 千兆网口：192.168.1.10
- 百兆网口：192.168.2.10
- 用户名：root

```bash
# 单个模块日志
scp root@192.168.1.10:/app/apa/log/planning/*.log ./

# 批量下载所有日志
scp root@192.168.1.10:/app/apa/log/*.log ./

# 打包下载
ssh root@192.168.1.10 "tar czf /tmp/logs.tar.gz -C /app/apa/log ."
scp root@192.168.1.10:/tmp/logs.tar.gz ./
```

### F4: 进程状态查看

```bash
# 查看进程详情（QNX特有）
pidin -p planning

# 查看CPU占用
hogs | grep -E "planning|od|rd|loc|psd|sensorcenter"

# 查看系统状态
top
```

### F5: 系统资源性能分析

#### 方式一：快速诊断（推荐新手）

```bash
# 综合监控脚本（彩色输出+自动日志）
/userdata/monitor_cpu.sh
```

**特性**：
- 🎨 彩色输出：高CPU红色、警告黄色
- 📊 TOP 15排名：CPU占用、内存占用
- 📝 自动日志：保存到 `/userdata/log/cpu_monitor/`
- 🔄 自动清理：7天后自动删除旧日志
- ⏱️ 实时刷新：每3秒更新一次

#### 方式二：手动三步法（推荐熟练用户）

```bash
# 第一步：找出占用CPU的进程
hogs -i -s 1

# 第二步：查看该进程详情
top -p <PID>

# 第三步：分析线程状态
# - Run: 正常计算
# - Mtx/Sem: 锁竞争，需检查
# - NSlp: 正常休眠
```

#### 诊断结论参考

| PIDS | SYS | STATE | 可能原因 |
|------|-----|-------|----------|
| >50% | <30% | 多Run | 算法过重，需优化 |
| >50% | >70% | 多Run | 死循环或系统调用频繁 |
| 正常 | 正常 | 多Mtx/Sem | 锁竞争严重，检查代码 |
| 正常 | 正常 | 多NSlp | 正常休眠 |

#### 后台监控脚本使用

```bash
# 上传脚本到板端
scp scripts/monitor_cpu.sh root@192.168.1.10:/userdata/

# SSH登录板端
ssh root@192.168.1.10

# 添加执行权限
chmod +x /userdata/monitor_cpu.sh

# 前台运行（实时查看）
/userdata/monitor_cpu.sh

# 后台运行（适合长期监控）
nohup /userdata/monitor_cpu.sh > /dev/null 2>&1 &

# 查看监控日志
tail -f /userdata/log/cpu_monitor/cpu_monitor_*.log

# 停止后台进程
kill $(pidof monitor_cpu.sh)
```

---

## 工作流程

### 场景1：泊车失败，需要查看日志

1. **定位日志路径**
   ```bash
   ls -la /app/apa/log/
   ```

2. **查看最新错误**
   ```bash
   grep -i "error\|fail" /app/apa/log/planning/*.log | tail -50
   ```

3. **实时跟踪**
   ```bash
   tail -f /app/apa/log/planning/*.log
   ```

4. **如需下载分析**
   ```bash
   scp root@192.168.1.10:/app/apa/log/planning/*.log ./
   ```

### 场景2：系统卡顿，需要分析性能

1. **快速启动综合监控**
   ```bash
   /userdata/monitor_cpu.sh
   ```

2. **观察监控输出**
   - CPU占用 > 80% 红色警告
   - 内存占用 > 10000K 黄色提示
   - 查看TOP 15排名定位问题进程

3. **深入分析**
   ```bash
   # 查看目标进程详情
   top -p <PID>
   ```

4. **分析问题**
   - PIDS高 + SYS高 → 可能死循环或系统调用频繁
   - 多线程卡在Mtx/Sem → 存在锁竞争

5. **查看历史监控日志**
   ```bash
   tail -100 /userdata/log/cpu_monitor/cpu_monitor_*.log
   ```

### 场景3：进程崩溃，需要分析coredump

1. **查找coredump文件**
   ```bash
   ls -la /log/coredump/
   ```

2. **查看崩溃原因**
   ```bash
   cat /log/reset_reason.txt
   ```

3. **结合日志分析**
   ```bash
   slog2info | grep -i "crash\|segmentation"
   ```

---

## 网络连接

**连接到板端**：
```bash
# 千兆网口
ssh root@192.168.1.10

# 百兆网口
ssh root@192.168.2.10
```

**测试连接**：
```bash
ping 192.168.1.10
```

---

## QNX vs Linux 常用命令对比

| 功能 | QNX | Linux |
|------|-----|-------|
| 查看进程详情 | `pidin` | `ps` |
| 结束进程 | `slay` | `kill` |
| 系统日志 | `slog2info` | `journalctl` |
| 资源监控 | `hogs`, `top` | `top`, `htop` |
