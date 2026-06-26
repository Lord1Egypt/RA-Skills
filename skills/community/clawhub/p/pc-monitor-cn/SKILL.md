# pc-monitor-cn
name: pc-monitor-cn
version: 1.0.0

监控系统资源状态（CPU、内存、磁盘、网络）。

## 描述

提供系统资源的实时监控功能，包括：
- CPU 使用率
- 内存使用率
- 磁盘空间
- 网络状态

## 使用方式

```bash
# 查看所有系统状态
~/.openclaw/workspace/skills/system-monitor/scripts/monitor.sh

# 或者使用 Python 版本
~/.openclaw/workspace/skills/system-monitor/scripts/monitor.py
```

## 依赖

- Python 3.6+
- psutil (可选，用于更详细的监控)

## 配置

无特殊配置要求。
