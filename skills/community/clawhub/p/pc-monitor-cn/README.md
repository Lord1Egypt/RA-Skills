# System Monitor Skill

监控系统资源状态的 OpenClaw skill。

## 功能

- 🔸 CPU 使用率和温度
- 🔸 内存使用情况
- 🔸 磁盘空间
- 🔸 网络流量统计

## 使用方法

### 基本使用

```bash
# 运行监控脚本
~/.openclaw/workspace/skills/system-monitor/scripts/monitor.sh

# 或者使用 Python 版本
python3 ~/.openclaw/workspace/skills/system-monitor/scripts/monitor.py
```

### 输出格式

**人类可读格式（默认）：**
```bash
python3 scripts/monitor.py
```

**JSON 格式（用于程序调用）：**
```bash
python3 scripts/monitor.py --json
```

## 依赖

- Python 3.6+
- psutil

安装依赖：
```bash
# Debian/Ubuntu
apt install python3-psutil

# 或使用 pip
pip install psutil
```

## 集成到 OpenClaw

可以将此脚本集成到你的 OpenClaw 配置中，通过 cron 定时检查系统状态，或者在需要时手动调用。

## 文件结构

```
system-monitor/
├── SKILL.md           # Skill 描述
├── README.md          # 使用说明
└── scripts/
    ├── monitor.py     # Python 监控脚本
    └── monitor.sh     # Bash 包装脚本
```
