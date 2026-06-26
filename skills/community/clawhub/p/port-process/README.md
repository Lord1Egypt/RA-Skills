# Port Process Skill - 端口进程管理技能

通过端口查找和管理系统进程的 OpenClaw 技能。

## 📁 目录结构

```
port-process/
├── SKILL.md              # 技能主文档（必须）
├── README.md             # 本文件（说明文档）
└── scripts/
    ├── find_port.py      # 查找占用端口的进程
    ├── kill_by_port.py   # 通过端口终止进程
    └── list_ports.py     # 列出所有监听端口
```

## 🚀 快速开始

### 查找端口占用

```bash
# 查找单个端口
python scripts/find_port.py 8080

# 查找多个端口
python scripts/find_port.py 8080 3000 5432

# JSON 输出
python scripts/find_port.py 8080 --json
```

### 终止端口进程

```bash
# 强制终止
python scripts/kill_by_port.py 8080

# 安全终止（先 SIGTERM，再 SIGKILL）
python scripts/kill_by_port.py 8080 --safe

# 仅预览，不执行
python scripts/kill_by_port.py 8080 --dry-run
```

### 列出所有端口

```bash
# 列出所有监听端口
python scripts/list_ports.py

# 仅 TCP
python scripts/list_ports.py --tcp

# 详细信息
python scripts/list_ports.py --verbose

# JSON 输出
python scripts/list_ports.py --json
```

## 💡 使用场景

### 开发调试

```bash
# 杀掉占用开发服务器端口的进程
python scripts/kill_by_port.py 3000
python scripts/kill_by_port.py 8000
```

### 自动化脚本

```bash
# 在启动服务前清理端口
python scripts/kill_by_port.py 8080 --dry-run || true
python scripts/kill_by_port.py 8080
./start-server.sh
```

## 🛠️ 手动命令（备忘）

这个技能源自这个经典命令：
```bash
lsof -ti :<port> | xargs kill -9
```

### 其他有用的命令

```bash
# 查找占用端口的进程
lsof -i :8080

# 查看所有监听端口
lsof -i -P | grep LISTEN

# 安全终止
lsof -ti :8080 | xargs kill -15
```

## 📝 技能创建说明

这个技能是从用户的一句话需求创建的：
> "lsof -ti :<port> | xargs kill -9 这个命令是通过端口杀进程。我想通过这个场景创建一个 skill"

技能包含了：
- ✅ 完整的 SKILL.md 文档
- ✅ 3 个实用 Python 脚本
- ✅ 跨平台支持（macOS/Linux）
- ✅ 安全模式和预览模式
- ✅ JSON 输出支持
