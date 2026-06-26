---
name: lobster-agent
description: 服务器监控Agent，自动采集系统指标并上报到Coze大龙虾平台，支持CPU/内存/磁盘/网络监控、告警推送和自动节点注册。
---

# 🦞 小龙虾监控Agent Skill (lobster-agent)

## Overview
此Skill为服务器监控代理，可自动采集系统运行指标并上报到Coze大龙虾平台，具备以下核心功能：
1. **指标采集** – CPU使用率、负载、内存使用率、磁盘使用率、网络流量等。
2. **自动告警** – 当指标超过阈值时自动产生告警（支持warning/critical两级）。
3. **节点注册** – 安装时自动注册到Coze平台，生成唯一Node ID。
4. **数据上报** – 心跳包、监控数据、告警数据分别上报到对应数据集。
5. **系统服务** – 后台运行，开机自启，崩溃自动重启。

## Prerequisites
1. 操作系统：Linux（支持systemd）
2. 依赖：Python3、pip3、curl（系统默认一般已安装）
3. 网络：可访问Coze API（https://api.coze.cn）
4. 权限：root权限（安装系统服务需要）

## Usage Steps
### 1. 安装Agent
直接运行内置安装脚本即可完成全自动化安装：
```bash
# 自动执行安装流程（OpenClaw触发）
```
安装过程会自动完成：
- 环境检查和依赖安装（requests、psutil）
- 工作目录创建（/opt/lobster-agent、/var/log/lobster-agent）
- Agent主程序生成
- 节点自动注册，获取Node ID
- 配置文件生成
- 管理命令创建（/usr/local/bin/lobster）
- systemd服务创建并启动

### 2. 管理Agent
安装完成后可通过`lobster`命令管理服务：
```bash
# 查看服务状态
lobster status

# 查看实时日志
lobster logs

# 启动服务
lobster start

# 停止服务
lobster stop

# 重启服务
lobster restart

# 完全卸载
lobster uninstall
```

### 3. 配置说明
配置文件路径：`/opt/lobster-agent/config.json`
```json
{
  "node_id": "自动生成的节点ID",
  "api_key": "Coze API密钥",
  "coze_base_url": "Coze API地址",
  "dataset_ids": {
    "nodes": "节点信息数据集ID",
    "monitor_data": "监控数据数据集ID",
    "alerts": "告警数据数据集ID"
  },
  "heartbeat_interval": 300,  // 心跳间隔（秒）
  "report_interval": 1800,    // 监控数据上报间隔（秒）
  "enable_hardware_check": true,
  "enable_log_check": true
}
```

### 4. 告警阈值
| 指标 | Warning阈值 | Critical阈值 |
|------|-------------|--------------|
| CPU使用率 | >80% | >90% |
| 内存使用率 | >85% | >95% |
| 磁盘使用率 | >70% | >90% |

## Example
### 安装成功输出
```
🎉 ==============================================
✅ 小龙虾Agent安装成功！
📊 Node ID: 7618478715609055278
📝 管理命令: lobster [status|start|stop|restart|logs|uninstall]
📜 查看日志: lobster logs
🌐 数据已自动上报到Coze平台
🎉 ==============================================
```

### 查看状态
```bash
lobster status
```
**输出示例：**
```
● lobster-agent.service - Lobster Monitor Agent
     Loaded: loaded (/etc/systemd/system/lobster-agent.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2026-03-19 08:41:23 CST; 10min ago
   Main PID: 12345 (python3)
      Tasks: 1 (limit: 4915)
     Memory: 20.0M
     CGroup: /system.slice/lobster-agent.service
             └─12345 /usr/bin/python3 /opt/lobster-agent/main.py
```

## Data Structure
### 上报的监控数据字段
| 字段 | 类型 | 说明 |
|------|------|------|
| node_id | string | 节点唯一标识 |
| timestamp | string | 上报时间（YYYY-MM-DD HH:MM:SS） |
| cpu_usage | float | CPU使用率（%） |
| memory_usage | float | 内存使用率（%） |
| disk_usage | float | 磁盘使用率（%） |
| load_1 | float | 1分钟负载 |
| load_5 | float | 5分钟负载 |
| load_15 | float | 15分钟负载 |
| network_in | float | 入站流量（KB/s） |
| network_out | float | 出站流量（KB/s） |
| status | string | 节点状态（healthy/warning/critical） |
| alerts | string | 告警列表（JSON格式） |

## When Not to Use
- 非Linux操作系统（不支持systemd）
- 没有root权限的环境
- 无法访问Coze API的离线环境
- 仅需要本地监控不需要云端上报的场景

## References
- Coze API文档：https://www.coze.cn/docs/developer-docs/api
- 大龙虾监控平台：https://coze.cn/s/7618478715609055278
