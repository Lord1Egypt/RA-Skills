# 快速开始

**适用场景**: 已安装 Glances，开始监控系统资源

---

## 一、启动终端交互模式

### 目标

使用最简单的方式启动 Glances，查看实时系统状态

### 最简单的启动方式

**AI执行说明**: AI 可以直接执行启动命令并解读输出

```bash
# 直接启动（终端交互界面）
glances
```

**期望结果**:

Glances 会显示一个全屏终端界面，包含以下区域（从上到下）：
```
┌──── 系统信息 ──────────────────────────────────────────────┐
│ hostname (OS) - uptime - Load: 1.2 | 1.5 | 1.8           │
├──── CPU ────────────────────────── 内存 ───────────────────┤
│ 23.4% user  0.2% sys                74.8% 12.1G/16G       │
├──── 磁盘 I/O ───────────────────── 网络 ───────────────────┤
│ sda: 1.2MB/s R  0.5MB/s W          eth0: 2.5MB/s ↑↓      │
├──── 进程列表 ───────────────────────────────────────────────┤
│ PID    NAME         CPU%  MEM%  ...                        │
└────────────────────────────────────────────────────────────┘
```

---

## 二、理解界面布局

### 颜色含义

Glances 使用颜色标识资源状态，帮助快速识别问题：

| 颜色 | 状态 | 含义 |
|------|------|------|
| 绿色 | OK | 正常，资源充足 |
| 蓝色 | Careful | 需要关注，使用偏高 |
| 黄色 | Warning | 警告，使用较高 |
| 红色 | Critical | 严重，需立即处理 |

### 默认告警阈值

| 资源 | Careful | Warning | Critical |
|------|---------|---------|---------|
| CPU | 50% | 70% | 90% |
| 内存 | 50% | 70% | 90% |
| Swap | 50% | 70% | 90% |
| 磁盘使用率 | 50% | 70% | 90% |

---

## 三、交互界面快捷键

**AI执行说明**: AI 会提示可用的快捷键操作

在 Glances 界面内按以下键操作：

### 全局控制

| 按键 | 功能 |
|------|------|
| `q` 或 `ESC` | 退出 Glances |
| `h` | 显示帮助界面 |
| `d` | 切换磁盘 I/O 显示 |
| `f` | 切换文件系统显示 |
| `n` | 切换网络接口显示 |
| `s` | 切换传感器显示 |
| `D` | 切换 Docker 容器显示 |
| `e` | 切换硬盘 SMART 信息 |

### 进程列表控制

| 按键 | 功能 |
|------|------|
| `a` | 自动排序（默认） |
| `c` | 按 CPU 排序 |
| `m` | 按内存排序 |
| `i` | 按 I/O 排序 |
| `p` | 按进程名排序 |
| `t` | 按时间排序 |
| `u` | 按用户排序 |
| `ENTER` | 展开选中进程（树形视图） |
| `k` | 终止选中进程（发送 SIGKILL） |
| `/` | 过滤进程（按名称搜索） |

### 显示调整

| 按键 | 功能 |
|------|------|
| `1` | 显示每个 CPU 核心（而不是汇总）|
| `2` | 显示 CPU 左侧（汇总与 IRIX 模式）|
| `l` | 显示/隐藏告警日志 |
| `w` | 清除已确认的告警日志 |
| `x` | 删除已确认的严重和警告告警 |
| `z` | 清除所有进程过滤器 |
| `+` | 增加进程数量 |
| `-` | 减少进程数量 |
| `F` | 显示文件系统空闲空间 |

---

## 四、启动 Web UI 模式

### 通过浏览器访问监控界面

**AI执行说明**: AI 可以启动 Web 服务器并提供访问地址

```bash
# 安装 Web UI 依赖（如未安装）
pip3 install bottle

# 启动 Web 服务器模式（监听所有网络接口）
glances -w

# 指定监听地址和端口
glances -w --bind 0.0.0.0 --port 61208

# 添加访问密码保护
glances -w --username --password
```

启动后，在浏览器中访问：
```
http://localhost:61208
```

**远程访问**（替换 IP 为服务器实际地址）:
```
http://192.168.1.100:61208
```

---

## 五、快速查看特定指标

### 非交互模式（stdout 输出）

**AI执行说明**: AI 可以获取单个或多个指标的即时值

```bash
# 输出 CPU 总使用率
glances --stdout cpu.total

# 输出内存使用率
glances --stdout mem.percent

# 输出多个指标（逗号分隔）
glances --stdout cpu.total,mem.percent,load.min1

# 持续输出，每秒刷新（Ctrl+C 停止）
glances --stdout cpu.total --time 1

# 输出 5 次后退出
glances --stdout cpu.total --count 5
```

**期望输出**:
```
cpu.total: 23.4
mem.percent: 74.8
load.min1: 1.25
```

---

## 六、查看系统摘要

### 一行快速摘要

```bash
# 以 CSV 格式输出所有指标（仅一次，用于脚本）
glances --stdout-csv cpu.total,mem.percent,swap.percent --count 1

# 查看系统摘要（JSON 格式）
glances --stdout-json cpu,mem,load --count 1
```

---

## 七、调整刷新频率

### 修改数据刷新间隔

**AI执行说明**: AI 可以根据需求调整监控精度

```bash
# 默认刷新间隔为 2 秒
glances

# 设置刷新间隔为 5 秒（降低 CPU 占用）
glances -t 5

# 设置刷新间隔为 1 秒（更精细监控）
glances -t 1

# Web 模式也支持自定义间隔
glances -w -t 3
```

---

## 八、仅监控特定插件

### 启用或禁用插件

```bash
# 禁用进程列表（减少 CPU 占用）
glances --disable-plugin processlist

# 禁用多个插件
glances --disable-plugin processlist,docker,sensors

# 只启用特定插件
glances --enable-plugin cpu,mem,load,network

# 查看所有可用插件
glances --list-plugins
```

---

## 九、进程过滤

### 只关注特定进程

**AI执行说明**: AI 可以根据你的需求过滤进程列表

```bash
# 只显示包含 "python" 的进程
glances --process-filter python

# 过滤支持正则表达式
glances --process-filter "nginx|apache"

# 在交互界面中动态过滤（按 / 键）
```

---

## 十、快速获取帮助

```bash
# 查看所有命令行参数
glances --help

# 查看版本信息
glances --version

# 查看插件列表
glances --list-plugins
```

---

## 完成确认

### 检查清单

- [ ] 成功启动 Glances 终端界面
- [ ] 理解颜色告警含义
- [ ] 掌握基本快捷键操作
- [ ] 学会启动 Web UI 模式
- [ ] 学会使用 `--stdout` 提取单个指标

### 下一步

继续阅读 [高级用法](03-advanced-usage.md) 学习服务端模式、数据导出、告警配置等高级功能
