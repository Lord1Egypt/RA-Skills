# 部署详细步骤

## 1. 监控服务器部署（monitor_install.sh）

```bash
# 设置飞书 Webhook 并执行（支持环境变量传参）
FEISHU_WEBHOOK_URL="https://open.larksuite.com/open-apis/bot/v2/hook/xxx" \
GRAFANA_PORT=3000 \
DATA_RETENTION=60d \
  bash /opt/monitor/monitor_install.sh
```

脚本自动完成：
1. 下载并安装 Prometheus 3.5.1、Alertmanager 0.29.0、Pushgateway 1.5.1、Grafana 10.4.19
2. 生成配置文件（Prometheus rules/prometheus.yml、Alertmanager alertmanager.yml）
3. 部署飞书 Webhook 服务（webhook.py）
4. 创建 systemd 服务并启动

**关键配置文件**：
- `/opt/monitor/feishu/webhook.env` — 飞书 Webhook URL（部署后需检查）
- `/opt/monitor/prometheus/rules.yml` — 告警规则（可按需调整阈值）
- `/opt/monitor/prometheus/prometheus.yml` — Prometheus 配置

## 2. 游戏服务器部署（Ansible）

### 目录结构
```
/opt/game_monitor/
├── main.yml                 # Ansible Playbook
└── templates/               # 模板文件
    ├── game_agent.py        # 采集脚本
    ├── game_monitor.service # systemd 服务
    └── game_monitor         # logrotate 配置
```

### 执行部署
```bash
cd /opt/game_monitor
ansible-playbook main.yml -l <主机组> \
  -e "PUSHGATEWAY=http://<pushgateway>:9091" \
  -e "MYSQL_USER=<mysql_user>" \
  -e "MYSQL_PASSWORD=<your_mysql_password>" \
  -e "GAME_ROOT_DIR=/data/game" \
  -e "GAME_PROCESS_NAME=java"
```

### 验证部署
```bash
# 检查服务状态
ansible <主机组> -m shell -a "systemctl status game_monitor"

# 查看日志
ansible <主机组> -m shell -a "tail -5 /var/log/game_monitor/agent.log"

# 检查 Pushgateway 上线
curl -s http://<pushgateway>:9091/metrics | grep jvm_up

# 检查环境变量
ansible <主机组> -m shell -a "cat /opt/game_monitor/env.conf"
```

## 3. 部署后验证

```bash
# Prometheus
curl -s "http://<prometheus>:9090/api/v1/query?query=jvm_up" | jq

# Alertmanager
curl -s "http://<alertmanager>:9093/api/v1/status" | jq

# Grafana
# 访问 http://<grafana>:3000，默认账号 admin（部署后请修改密码）
```

## 环境变量说明

### Agent 环境变量（/opt/game_monitor/env.conf）

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `PUSHGATEWAY` | ✅ | — | Pushgateway 地址 |
| `PUSH_INTERVAL` | | `60` | 采集推送间隔（秒） |
| `MYSQL_USER` | | 空 | MySQL 用户（无 MySQL 可留空） |
| `MYSQL_PASSWORD` | | 空 | MySQL 密码 |
| `MYSQL_HOST` | | `127.0.0.1` | MySQL 地址 |
| `MYSQL_PORT` | | `3306` | MySQL 端口 |
| `GAME_ROOT_DIR` | | `/data/game` | 游戏服根目录 |
| `GAME_PROCESS_NAME` | | `java` | Java 进程标识 |
| `HISTO_INTERVAL` | | `600` | 类直方图采集间隔（秒） |

### Webhook 环境变量（/opt/monitor/feishu/webhook.env）

| 变量 | 必填 | 说明 |
|------|------|------|
| `FEISHU_WEBHOOK_URL` | ✅ | 飞书机器人 Webhook 地址 |
| `WEBHOOK_PORT` | | 监听端口（默认 5000） |
| `PUSH_INTERVAL` | | 与 agent 保持一致 |

## 敏感信息管理建议

- 使用 Ansible Vault 加密 `MYSQL_PASSWORD`
- `FEISHU_WEBHOOK_URL` 写入 `/opt/monitor/feishu/webhook.env`，文件权限 600
- 监控服务器安全组：仅允许运维 IP 访问 Prometheus(9090)、Grafana(3000)
