---
name: pg-game-monitor
description: Prometheus + Grafana 监控方案，专为**单台物理机部署多个 Java 游戏进程 + 自建 MySQL**的场景设计。Java 进程通过 jstat/jcmd 无侵入采集 JVM 运行时指标（堆内存、新生代、老年代、GC、线程、类内存），MySQL 通过 pymysql 采集（Buffer Pool、进程内存）。监控重点围绕**内存使用率**，适配游戏服高频 GC 和大内存占用的特点。通过 Pushgateway 推送数据，Grafana 可视化，Alertmanager + 飞书 Webhook 告警，支持 Ansible 批量部署。
triggers:
  - (.*) JVM (.*) 监控 (.*)
  - (.*) MySQL (.*) 监控 (.*)
  - (.*) Java (.*) 告警 (.*)
  - (.*) Prometheus (.*) 游戏 (.*)
  - (.*) Grafana (.*) Dashboard (.*)
  - (.*) Pushgateway (.*) 部署 (.*)
  - (.*) GC (.*) 压力 (.*)
  - (.*) 堆内存 (.*) 告警 (.*)
  - 游戏服 (.*) 监控状态
  - 查看 (.*) JVM 指标
  - 查询 (.*) MySQL 状态
  - 触发 告警 测试
required_environment_variables:
  - PUSHGATEWAY
  - FEISHU_WEBHOOK_URL
---

# Java 多进程游戏服监控方案

基于 Prometheus + Grafana，专为**单台物理机多 Java 进程 + 自建 MySQL**场景设计。监控重点围绕**内存使用率**，适配游戏服大内存、高 GC 压力的特点。

## 架构

```
┌─────────────────────────────────────────────────────────┐
│                     单台物理游戏服务器                      │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Java进程1 │  │ Java进程2 │  │ Java进程3 │  │ MySQL  │  │
│  │ (JVM)    │  │ (JVM)    │  │ (JVM)    │  │        │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  │
│       │ jstat/jcmd  │ jstat/jcmd  │ jstat/jcmd   │ pymysql
│       └─────────────┴──────┬──────┴──────────────┘
│                            │
│                    game_agent.py
│                            │
│                       push │ Pushgateway ◄── Prometheus ──► Alertmanager
│                            │                                   │
│                            │                            Feishu/Lark Webhook
│                            │
│                      query │ Grafana
└─────────────────────────────────────────────────────────┘
```

## 环境变量配置

所有配置均通过环境变量注入，无硬编码。

### game_agent.py（采集 Agent）

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `PUSHGATEWAY` | ✅ | — | Pushgateway 地址，如 `http://pushgateway:9091` |
| `PUSH_INTERVAL` | | `60` | 采集推送间隔（秒） |
| `MYSQL_USER` | | 空 | MySQL 用户名（无 MySQL 时可留空） |
| `MYSQL_PASSWORD` | | 空 | MySQL 密码 |
| `MYSQL_HOST` | | `127.0.0.1` | MySQL 地址 |
| `MYSQL_PORT` | | `3306` | MySQL 端口 |
| `GAME_ROOT_DIR` | | `/data/game` | 游戏服目录根路径 |
| `GAME_PROCESS_NAME` | | `java` | Java 进程标识（cmdline 匹配关键字） |
| `AGENT_LOG_FILE` | | `/var/log/game_monitor/agent.log` | 日志路径 |
| `HISTO_INTERVAL` | | `600` | 类直方图采集间隔（秒，0 表示关闭） |

### webhook.py（告警接收服务）

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `FEISHU_WEBHOOK_URL` | ✅ | — | 飞书机器人 Webhook URL |
| `WEBHOOK_PORT` | | `5000` | 监听端口 |
| `PUSH_INTERVAL` | | `60` | 与 agent 保持一致（用于格式化） |

## 快速部署

### 监控服务器（All-in-One）

```bash
# 一键部署（需先设置飞书 Webhook）
FEISHU_WEBHOOK_URL="https://open.larksuite.com/..." bash monitor_install.sh
```

### 游戏服务器（Ansible 批量）

```bash
ansible-playbook main.yml -l <hosts> \
  -e "PUSHGATEWAY=http://<pushgateway>:9091" \
  -e "MYSQL_USER=<user>" \
  -e "MYSQL_PASSWORD=<your_mysql_password>" \
  -e "GAME_ROOT_DIR=/data/game" \
  -e "GAME_PROCESS_NAME=java"
```

## 核心文件

| 文件 | 说明 |
|------|------|
| `monitor_install.sh` | 监控服务器一键部署（Prometheus/Grafana/Alertmanager/Pushgateway） |
| `game_agent.py` | 游戏服务器指标采集脚本（jstat + jcmd，无侵入） |
| `main.yml` | Ansible Playbook，批量部署 agent |
| `webhook.py` | 告警 Webhook 服务，转发至飞书/ Lark |
| `rules.yml` | Prometheus 告警规则（JVM + MySQL） |
| `game_monitor.service` | systemd 服务配置 |
| `game_monitor` | logrotate 日志轮转配置 |

## 指标清单

### JVM 指标（通过 jstat 采集）

| 指标 | 说明 | 标签 |
|------|------|------|
| `heap_used_bytes` | 堆内存已使用量 | hostname, game_dir |
| `heap_committed_bytes` | 堆内存提交量 | hostname, game_dir |
| `young_used_bytes` | 新生代（Eden+S0+S1）已使用 | hostname, game_dir |
| `old_used_bytes` | 老年代已使用 | hostname, game_dir |
| `gc_time_seconds` | 本周期 GC 耗时（delta） | hostname, game_dir |
| `gc_count` | 本周期 GC 次数（delta） | hostname, game_dir |
| `threads_live` | 活跃线程数 | hostname, game_dir |
| `jvm_up` | JVM 上线状态 | hostname, game_dir |
| `jvm_class_bytes` | Top 50 类内存占用 | hostname, game_dir, class |
| `jvm_class_instance_count` | Top 50 类实例数量 | hostname, game_dir, class |

### MySQL 指标（通过 pymysql 采集）

| 指标 | 说明 | 标签 |
|------|------|------|
| `mysql_up` | MySQL 连接状态 | hostname |
| `mysql_process_resident_memory_bytes` | MySQL 进程 RSS | hostname |
| `innodb_buffer_pool_bytes_data` | InnoDB Buffer Pool 已使用 | hostname |
| `innodb_buffer_pool_bytes_total` | InnoDB Buffer Pool 总大小 | hostname |

## Grafana Dashboard

预置 3 个 Dashboard JSON，开箱即用：`references/files/`

| 文件 | 面板内容 |
|------|----------|
| `jvm_dashboard.json` | 堆内存使用量/率、新生代、老年代、GC 耗时、线程数 |
| `jvm_class_dashboard.json` | Top10 类内存/实例数排行、选中类趋势、Top20 快照表 |
| `mysql_dashboard.json` | MySQL 存活、RSS 内存、Buffer Pool 概览及使用率 |

导入方式：Grafana → Dashboards → Import → 上传 JSON → 选择 Prometheus 数据源。

## 告警规则

| 告警 | 条件 | 级别 |
|------|------|------|
| `JVMHeapUsageHigh` | 堆内存使用率 > 85%，持续 5 分钟（JVM 预热 1 小时后） | warning |
| `JVMGcPressureWarning` | GC 时间占采集周期 > 30%，持续 3 分钟 | warning |
| `JVMGcPressureCritical` | GC 时间占采集周期 > 60%，持续 2 分钟 | critical |
| `MySQLDown` | MySQL 连接失败，持续 2 分钟 | critical |
| `MySQLBufferPoolHigh` | InnoDB Buffer Pool > 85%，持续 5 分钟 | warning |
| `MySQLMemoryHigh` | MySQL RSS > 8GB，持续 5 分钟 | warning |

## 故障排查

### Agent 不上线
```bash
systemctl status game_monitor
tail -f /var/log/game_monitor/agent.log
# 检查环境变量
cat /opt/game_monitor/env.conf
```

### Pushgateway 无数据
```bash
curl -s http://<pushgateway>:9091/-/healthy
curl -s "http://<prometheus>:9090/api/v1/targets" | jq '.data.activeTargets'
```

### 飞书告警未收到
```bash
curl -X POST "http://<webhook>:5000/webhook?level=warning" \
  -H "Content-Type: application/json" -d '{"alerts":[]}'
journalctl -u feishu -f
```

## 参考文档

- 部署详细步骤：`references/deploy.md`
- 告警规则说明：`references/rules.md`
- Grafana 配置指南：`references/grafana.md`
- 监控架构规划：`references/planning.md`
- 常见问题：`references/faq.md`
