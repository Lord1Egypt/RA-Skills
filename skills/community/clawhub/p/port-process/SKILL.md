---
name: port-process
description: 通过端口查找和管理系统进程。支持查找占用端口的进程、杀掉占用端口的进程、查看端口使用情况等操作。适用于 macOS 和 Linux 系统。使用场景：(1) "谁占用了 8080 端口"，(2) "杀掉占用 3000 端口的进程"，(3) "查看当前端口使用情况"。
---

# Port Process - 端口进程管理

## 概述

通过端口查找和管理系统进程的工具集。支持跨平台（macOS/Linux）操作。

## 快速开始

### 查找占用端口的进程

```bash
# 方法一：使用 lsof（macOS/Linux）
lsof -ti :8080

# 方法二：使用 netstat（Linux）
netstat -tulpn | grep :8080

# 方法三：使用 ss（现代 Linux）
ss -tulpn | grep :8080
```

### 杀掉占用端口的进程

```bash
# 一键杀掉占用 8080 端口的进程
lsof -ti :8080 | xargs kill -9

# 或者使用提供的脚本
python3 scripts/kill_by_port.py 8080
```

## 任务分类

### 1. 查找端口占用

**查找单个端口：**
```bash
lsof -i :8080
```

**查找多个端口：**
```bash
lsof -i :8080 -i :3000
```

**显示进程详细信息：**
```bash
lsof -ti :8080 | xargs ps -fp
```

### 2. 终止端口进程

**安全终止（先尝试 SIGTERM）：**
```bash
lsof -ti :8080 | xargs kill -15
```

**强制终止（SIGKILL）：**
```bash
lsof -ti :8080 | xargs kill -9
```

**使用脚本安全终止：**
```bash
python3 scripts/kill_by_port.py 8080 --safe
```

### 3. 查看端口使用情况

**查看所有监听端口：**
```bash
# macOS
lsof -i -P | grep LISTEN

# Linux
netstat -tulpn
ss -tulpn
```

**查看特定用户的端口占用：**
```bash
lsof -i -u username
```

## 脚本使用

### scripts/kill_by_port.py

通过端口终止进程的安全脚本。

**用法：**
```bash
# 强制终止
python3 scripts/kill_by_port.py 8080

# 安全终止（先 SIGTERM，等待后再 SIGKILL）
python3 scripts/kill_by_port.py 8080 --safe

# 仅查看，不终止
python3 scripts/kill_by_port.py 8080 --dry-run
```

### scripts/find_port.py

查找占用端口的进程信息。

**用法：**
```bash
# 查找单个端口
python3 scripts/find_port.py 8080

# 查找多个端口
python3 scripts/find_port.py 8080 3000 5432

# 输出 JSON 格式
python3 scripts/find_port.py 8080 --json
```

### scripts/list_ports.py

列出所有正在使用的端口。

**用法：**
```bash
# 列出所有监听端口
python3 scripts/list_ports.py

# 仅显示 TCP 端口
python3 scripts/list_ports.py --tcp

# 仅显示 UDP 端口
python3 scripts/list_ports.py --udp

# 显示详细信息
python3 scripts/list_ports.py --verbose
```

## 跨平台兼容性

### macOS
- 使用 `lsof` 作为主要工具
- 支持 `netstat` 作为备选

### Linux
- 使用 `ss` 作为首选（现代系统）
- 使用 `netstat` 作为备选
- 支持 `lsof`

### Windows (WSL)
- 在 WSL 中使用 Linux 工具
- 如需管理 Windows 进程，使用 PowerShell

## 常见用例

### 开发场景
```bash
# 杀掉占用前端开发服务器端口的进程
python3 scripts/kill_by_port.py 3000

# 杀掉占用后端 API 端口的进程
python3 scripts/kill_by_port.py 8000

# 杀掉占用数据库端口的进程
python3 scripts/kill_by_port.py 5432
```

### 调试场景
```bash
# 查看是谁占用了端口
python3 scripts/find_port.py 8080

# 查看所有端口使用情况
python3 scripts/list_ports.py --verbose
```

### 自动化脚本
```bash
# 在启动服务前清理端口
python3 scripts/kill_by_port.py 8080 --dry-run || true
python3 scripts/kill_by_port.py 8080
./start-my-server.sh
```

## 安全提示

1. **先查看，后终止**：使用 `--dry-run` 或先运行 `find_port.py` 确认要终止的进程
2. **优先安全终止**：使用 `--safe` 选项给进程优雅退出的机会
3. **避免误杀**：仔细检查进程信息，特别是通用端口（如 22、80、443）
4. **备份重要数据**：在终止可能有状态的进程前，确保数据已保存

## 故障排除

### "lsof: command not found"
- **macOS**：通常预装了 lsof，如缺失可安装 Xcode Command Line Tools
- **Linux**：`sudo apt install lsof` (Debian/Ubuntu) 或 `sudo yum install lsof` (RHEL/CentOS)

### "端口没有被占用"但仍然无法绑定
- 检查 TIME_WAIT 状态：`netstat -an | grep TIME_WAIT`
- 等待一段时间或调整系统参数

### 权限不足
- 使用 `sudo` 运行以查看其他用户的进程
- 注意：使用 `sudo kill` 时要格外小心
