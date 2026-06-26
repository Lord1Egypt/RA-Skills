# 监控与日志管理

## 目录

- [1. 系统监控工具](#1-系统监控工具)
- [2. Prometheus + Node Exporter](#2-prometheus--node-exporter)
- [3. Grafana 可视化](#3-grafana-可视化)
- [4. 日志管理](#4-日志管理)
- [5. 日志轮转](#5-日志轮转)
- [6. 集中式日志](#6-集中式日志)
- [7. 告警配置](#7-告警配置)
- [8. 常见故障排查](#8-常见故障排查)

---

## 1. 系统监控工具

### 1.1 实时监控

```bash
# top — 进程级 CPU/内存实时监控
top -bn1 | head -20        # 非交互模式，取前 20 行
top -u username             # 只看指定用户的进程

# htop — 增强版 top（需安装）
apt install htop   # Ubuntu
yum install htop   # RHEL
htop

# glances — 全面系统监控仪表盘（需安装）
pip3 install glances
glances
glances -w                  # Web 模式（http://host:61208）
glances --export csv --export-csv-file /tmp/metrics.csv  # 导出 CSV

# dstat — 综合资源统计（CPU/磁盘/网络/内存）
dstat -cdnm 5               # 每 5 秒刷新
dstat -cdnm --top-cpu --top-mem  # 含 top 进程

# nmon — IBM 出品的性能监控
nmon                         # 交互模式
nmon -f -s 30 -c 120        # 后台采集（每 30 秒，共 120 次 = 1 小时）
```

### 1.2 历史数据分析（sar）

```bash
# 安装 sysstat
apt install sysstat   # Ubuntu
yum install sysstat   # RHEL

# 启用数据采集
systemctl enable --now sysstat

# 查看 CPU 历史
sar -u                      # 今天的 CPU 使用率
sar -u -f /var/log/sa/sa01  # 指定日期（1号）
sar -u -s 09:00:00 -e 12:00:00  # 指定时间范围

# 查看内存历史
sar -r                      # 内存使用率
sar -S                      # Swap 使用率

# 查看磁盘 I/O 历史
sar -d                      # 磁盘活动
sar -b                      # I/O 传输速率

# 查看网络历史
sar -n DEV                  # 网络接口统计
sar -n SOCK                 # 套接字统计
sar -n TCP                  # TCP 统计

# 查看负载历史
sar -q                      # 运行队列和负载
```

### 1.3 /proc 和 /sys 文件系统

```bash
# 系统信息
cat /proc/cpuinfo | grep "model name" | head -1
cat /proc/meminfo | head -10
cat /proc/loadavg
cat /proc/uptime

# 进程信息
cat /proc/<pid>/status      # 进程状态
cat /proc/<pid>/cmdline     # 启动命令
cat /proc/<pid>/fd          # 文件描述符
ls -la /proc/<pid>/fd | wc -l  # FD 数量

# 网络信息
cat /proc/net/tcp           # TCP 连接表
cat /proc/net/dev           # 网络接口统计

# 磁盘信息
cat /proc/diskstats         # 磁盘 I/O 统计
cat /proc/mdstat            # RAID 状态
```

---

## 2. Prometheus + Node Exporter

### 2.1 安装 Node Exporter

```bash
# 下载（检查最新版本：https://github.com/prometheus/node_exporter/releases）
NODE_EXPORTER_VERSION="1.8.2"
wget https://github.com/prometheus/node_exporter/releases/download/v${NODE_EXPORTER_VERSION}/node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz
tar xzf node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz
cp node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64/node_exporter /usr/local/bin/

# 创建系统用户
useradd -r -s /usr/sbin/nologin node_exporter

# 创建 systemd 服务
cat > /etc/systemd/system/node_exporter.service << 'EOF'
[Unit]
Description=Prometheus Node Exporter
After=network.target

[Service]
Type=simple
User=node_exporter
ExecStart=/usr/local/bin/node_exporter \
  --collector.systemd \
  --collector.processes \
  --web.listen-address=:9100
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now node_exporter

# 验证
curl -s http://localhost:9100/metrics | head -20
```

### 2.2 安装 Prometheus

```bash
PROMETHEUS_VERSION="2.53.0"
wget https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
tar xzf prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
cp prometheus-${PROMETHEUS_VERSION}.linux-amd64/{prometheus,promtool} /usr/local/bin/
mkdir -p /etc/prometheus /var/lib/prometheus

# 配置文件
cat > /etc/prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerts/*.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node"
    static_configs:
      - targets:
          - "localhost:9100"
          - "server2:9100"
          - "server3:9100"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["localhost:9093"]
EOF

# 创建系统用户和服务
useradd -r -s /usr/sbin/nologin prometheus
chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus

cat > /etc/systemd/system/prometheus.service << 'EOF'
[Unit]
Description=Prometheus Monitoring
After=network.target

[Service]
Type=simple
User=prometheus
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --storage.tsdb.retention.time=30d \
  --web.listen-address=:9090
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now prometheus

# 验证
curl -s http://localhost:9090/-/healthy
```

### 2.3 常用 PromQL 查询

```promql
# CPU 使用率（百分比）
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 内存使用率
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100

# 磁盘使用率
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100

# 磁盘 I/O 利用率
irate(node_disk_io_time_seconds_total[5m]) * 100

# 网络流量（入/出，bytes/s）
irate(node_network_receive_bytes_total{device="eth0"}[5m])
irate(node_network_transmit_bytes_total{device="eth0"}[5m])

# 系统负载
node_load1 / count(node_cpu_seconds_total{mode="idle"}) by (instance)

# TCP 连接状态
node_netstat_Tcp_CurrEstab
node_sockstat_TCP_tw              # TIME_WAIT 数量

# 文件描述符使用率
node_filefd_allocated / node_filefd_maximum * 100

# 上下文切换率
irate(node_context_switches_total[5m])
```

---

## 3. Grafana 可视化

### 3.1 安装 Grafana

```bash
# Ubuntu/Debian
apt install -y apt-transport-https software-properties-common
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor -o /usr/share/keyrings/grafana.gpg
echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://apt.grafana.com stable main" > /etc/apt/sources.list.d/grafana.list
apt update && apt install grafana

# RHEL/CentOS
cat > /etc/yum.repos.d/grafana.repo << 'EOF'
[grafana]
name=grafana
baseurl=https://rpm.grafana.com
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://rpm.grafana.com/gpg.key
EOF
yum install grafana

# 启动
systemctl enable --now grafana-server
# 访问 http://host:3000（默认 admin/admin）
```

### 3.2 推荐 Dashboard

```text
# 导入预置 Dashboard（Grafana → Import → 输入 ID）
1860  — Node Exporter Full（最全面的系统监控面板）
11074 — Node Exporter for Prometheus（简洁版）
13978 — Node Exporter Quickstart（快速入门版）
```

### 3.3 Grafana 配置加固

```ini
# /etc/grafana/grafana.ini

[server]
http_port = 3000
root_url = https://grafana.example.com

[security]
admin_user = admin
admin_password = <strong-password>
disable_gravatar = true
cookie_secure = true

[auth.anonymous]
enabled = false

[users]
allow_sign_up = false

[alerting]
enabled = true
```

---

## 4. 日志管理

### 4.1 journalctl 高级查询

```bash
# 按服务
journalctl -u nginx -f                    # 实时跟踪
journalctl -u nginx --since "1 hour ago"  # 最近 1 小时
journalctl -u nginx --since "2026-04-01" --until "2026-04-02"

# 按优先级
journalctl -p err                          # 只看 error 及以上
journalctl -p warning..err                 # warning 到 error
# 优先级：emerg(0) alert(1) crit(2) err(3) warning(4) notice(5) info(6) debug(7)

# 按进程/用户
journalctl _PID=1234
journalctl _UID=1000
journalctl _COMM=sshd

# 内核日志
journalctl -k                             # 当前启动
journalctl -k -b -1                       # 上次启动

# 输出格式
journalctl -u nginx -o json               # JSON 格式
journalctl -u nginx -o json-pretty        # JSON 美化
journalctl -u nginx -o short-iso          # ISO 时间格式

# 统计
journalctl --disk-usage                    # 日志占用空间
journalctl --list-boots                    # 启动记录列表
```

### 4.2 rsyslog 配置

```bash
# /etc/rsyslog.conf 或 /etc/rsyslog.d/50-custom.conf

# 按设施和优先级过滤
auth,authpriv.*           /var/log/auth.log
kern.*                    /var/log/kern.log
mail.*                    /var/log/mail.log
*.emerg                   :omusrmsg:*

# 按程序名过滤
:programname, isequal, "nginx" /var/log/nginx/syslog.log
& stop

# 模板（自定义日志格式）
template(name="CustomFormat" type="string"
  string="%timegenerated:::date-rfc3339% %HOSTNAME% %syslogtag%%msg%\n")

# 远程转发
# UDP
*.* @syslog-server:514
# TCP
*.* @@syslog-server:514
# TCP + TLS
*.* @@(o)syslog-server:6514

# 重启
systemctl restart rsyslog
```

### 4.3 syslog-ng 配置

```bash
# /etc/syslog-ng/syslog-ng.conf

source s_local {
    system();
    internal();
};

destination d_remote {
    tcp("syslog-server" port(514));
};

filter f_error {
    level(err..emerg);
};

log {
    source(s_local);
    filter(f_error);
    destination(d_remote);
};
```

---

## 5. 日志轮转

### 5.1 logrotate 配置

```bash
# 全局配置：/etc/logrotate.conf
# 应用配置：/etc/logrotate.d/

# 示例：Nginx 日志轮转
cat > /etc/logrotate.d/nginx << 'EOF'
/var/log/nginx/*.log {
    daily                  # 每天轮转
    missingok              # 文件不存在不报错
    rotate 30              # 保留 30 个轮转文件
    compress               # 压缩旧日志
    delaycompress          # 延迟一次压缩（便于日志分析）
    notifempty             # 空文件不轮转
    create 0640 www-data adm  # 创建新文件的权限
    sharedscripts          # 多个日志文件只执行一次脚本
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 $(cat /var/run/nginx.pid)
    endscript
}
EOF

# 示例：应用日志轮转（按大小）
cat > /etc/logrotate.d/myapp << 'EOF'
/var/log/myapp/*.log {
    size 100M              # 超过 100M 轮转
    rotate 10              # 保留 10 个
    compress
    copytruncate           # 复制后截断（不需要重启应用）
    dateext                # 用日期作为后缀
    dateformat -%Y%m%d     # 日期格式
    maxage 90              # 删除超过 90 天的日志
}
EOF

# 测试轮转（不实际执行）
logrotate -d /etc/logrotate.d/nginx

# 强制执行轮转
logrotate -f /etc/logrotate.d/nginx

# 查看轮转状态
cat /var/lib/logrotate/status
```

### 5.2 journald 日志管理

```bash
# /etc/systemd/journald.conf
[Journal]
Storage=persistent         # 持久化（默认 volatile 重启丢失）
SystemMaxUse=2G            # 最大占用 2G
SystemMaxFileSize=200M     # 单文件最大 200M
MaxRetentionSec=90day      # 保留 90 天
Compress=yes               # 压缩
ForwardToSyslog=yes        # 转发到 syslog

# 重启 journald
systemctl restart systemd-journald

# 手动清理
journalctl --vacuum-size=1G    # 保留 1G
journalctl --vacuum-time=30d   # 保留 30 天
journalctl --vacuum-files=10   # 保留 10 个文件
```

---

## 6. 集中式日志

### 6.1 ELK Stack（Elasticsearch + Logstash + Kibana）

```bash
# === Elasticsearch ===
# 安装（以 8.x 为例）
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elasticsearch.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" > /etc/apt/sources.list.d/elastic-8.x.list
apt update && apt install elasticsearch

# 配置 /etc/elasticsearch/elasticsearch.yml
# cluster.name: my-cluster
# node.name: node-1
# network.host: 0.0.0.0
# discovery.type: single-node
# xpack.security.enabled: false  # 测试环境

systemctl enable --now elasticsearch

# === Logstash ===
apt install logstash

# 配置 /etc/logstash/conf.d/syslog.conf
cat > /etc/logstash/conf.d/syslog.conf << 'LOGSTASH_EOF'
input {
  syslog {
    port => 5514
    type => "syslog"
  }
  beats {
    port => 5044
  }
}

filter {
  if [type] == "syslog" {
    grok {
      match => { "message" => "%{SYSLOGTIMESTAMP:timestamp} %{SYSLOGHOST:hostname} %{DATA:program}(?:\[%{POSINT:pid}\])?: %{GREEDYDATA:log_message}" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "syslog-%{+YYYY.MM.dd}"
  }
}
LOGSTASH_EOF

systemctl enable --now logstash

# === Kibana ===
apt install kibana
# 配置 /etc/kibana/kibana.yml
# server.host: "0.0.0.0"
# elasticsearch.hosts: ["http://localhost:9200"]
systemctl enable --now kibana
# 访问 http://host:5601
```

### 6.2 Loki + Promtail（轻量替代方案）

```bash
# === Promtail（日志采集器）===
PROMTAIL_VERSION="3.1.0"
wget https://github.com/grafana/loki/releases/download/v${PROMTAIL_VERSION}/promtail-linux-amd64.zip
unzip promtail-linux-amd64.zip
chmod +x promtail-linux-amd64
mv promtail-linux-amd64 /usr/local/bin/promtail

# 配置
mkdir -p /etc/promtail
cat > /etc/promtail/config.yml << 'EOF'
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /var/lib/promtail/positions.yaml

clients:
  - url: http://loki-server:3100/loki/api/v1/push

scrape_configs:
  - job_name: syslog
    static_configs:
      - targets: [localhost]
        labels:
          job: syslog
          host: ${HOSTNAME}
          __path__: /var/log/syslog

  - job_name: auth
    static_configs:
      - targets: [localhost]
        labels:
          job: auth
          host: ${HOSTNAME}
          __path__: /var/log/auth.log

  - job_name: nginx
    static_configs:
      - targets: [localhost]
        labels:
          job: nginx
          host: ${HOSTNAME}
          __path__: /var/log/nginx/*.log
    pipeline_stages:
      - regex:
          expression: '^(?P<remote_addr>\S+) .* \[(?P<time_local>.*)\] "(?P<method>\S+) (?P<request>\S+) .*" (?P<status>\d+) (?P<body_bytes_sent>\d+)'
      - labels:
          method:
          status:
EOF

# 创建 systemd 服务
cat > /etc/systemd/system/promtail.service << 'EOF'
[Unit]
Description=Promtail Log Agent
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/promtail -config.file=/etc/promtail/config.yml
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now promtail

# === Loki（日志存储）===
# 通常部署在专用服务器上
LOKI_VERSION="3.1.0"
wget https://github.com/grafana/loki/releases/download/v${LOKI_VERSION}/loki-linux-amd64.zip
unzip loki-linux-amd64.zip
mv loki-linux-amd64 /usr/local/bin/loki

# 在 Grafana 中添加 Loki 数据源：
# URL: http://loki-server:3100
# 使用 LogQL 查询日志
```

### 6.3 Filebeat（轻量日志采集器）

```bash
# 安装
apt install filebeat

# 配置 /etc/filebeat/filebeat.yml
cat > /etc/filebeat/filebeat.yml << 'EOF'
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/syslog
      - /var/log/auth.log
    fields:
      type: syslog

  - type: log
    enabled: true
    paths:
      - /var/log/nginx/access.log
    fields:
      type: nginx-access

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "filebeat-%{+yyyy.MM.dd}"

# 或输出到 Logstash
# output.logstash:
#   hosts: ["logstash:5044"]
EOF

# 启用模块
filebeat modules enable system nginx
filebeat setup   # 初始化索引模板和 Dashboard

systemctl enable --now filebeat
```

---

## 7. 告警配置

### 7.1 Prometheus Alertmanager

```bash
# 安装 Alertmanager
ALERTMANAGER_VERSION="0.27.0"
wget https://github.com/prometheus/alertmanager/releases/download/v${ALERTMANAGER_VERSION}/alertmanager-${ALERTMANAGER_VERSION}.linux-amd64.tar.gz
tar xzf alertmanager-${ALERTMANAGER_VERSION}.linux-amd64.tar.gz
cp alertmanager-${ALERTMANAGER_VERSION}.linux-amd64/alertmanager /usr/local/bin/

# 配置
mkdir -p /etc/alertmanager
cat > /etc/alertmanager/alertmanager.yml << 'EOF'
global:
  resolve_timeout: 5m
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alertmanager@example.com'
  smtp_auth_username: 'alertmanager@example.com'
  smtp_auth_password: '<password>'

route:
  group_by: ['alertname', 'instance']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'email-ops'

  routes:
    - match:
        severity: critical
      receiver: 'email-ops'
      repeat_interval: 1h
    - match:
        severity: warning
      receiver: 'email-ops'
      repeat_interval: 8h

receivers:
  - name: 'email-ops'
    email_configs:
      - to: 'ops-team@example.com'
        send_resolved: true

  - name: 'webhook'
    webhook_configs:
      - url: 'http://alertbot:8080/webhook'
        send_resolved: true

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
EOF

# 创建服务并启动
# ... (类似 node_exporter 的 systemd 配置)
```

### 7.2 告警规则

```yaml
# /etc/prometheus/alerts/system.yml
groups:
  - name: system
    rules:
      - alert: HighCpuUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU 使用率过高 ({{ $labels.instance }})"
          description: "CPU 使用率 {{ $value | printf \"%.1f\" }}% 持续 5 分钟"

      - alert: HighMemoryUsage
        expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "内存使用率过高 ({{ $labels.instance }})"
          description: "内存使用率 {{ $value | printf \"%.1f\" }}%"

      - alert: DiskSpaceLow
        expr: (1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "磁盘空间不足 ({{ $labels.instance }})"
          description: "{{ $labels.mountpoint }} 使用率 {{ $value | printf \"%.1f\" }}%"

      - alert: DiskSpaceCritical
        expr: (1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 > 95
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "磁盘空间严重不足 ({{ $labels.instance }})"

      - alert: HighLoadAverage
        expr: node_load15 / count(node_cpu_seconds_total{mode="idle"}) by (instance) > 2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "系统负载过高 ({{ $labels.instance }})"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "服务不可达 ({{ $labels.instance }})"

      - alert: HighNetworkErrors
        expr: irate(node_network_receive_errs_total[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "网络接收错误率过高 ({{ $labels.instance }})"

      - alert: TooManyOpenFiles
        expr: node_filefd_allocated / node_filefd_maximum * 100 > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "文件描述符使用率过高 ({{ $labels.instance }})"
```

### 7.3 企业微信/钉钉 Webhook 告警

```bash
# 企业微信 Webhook
# Alertmanager 配置 webhook receiver，指向中间件
# 中间件将 Alertmanager 格式转为企业微信格式

# 使用 prometheus-webhook-dingtalk（钉钉）
# 或自定义脚本转发到企业微信

# 简单的 Webhook 转发脚本示例
cat > /opt/alert-webhook.py << 'PYTHON_EOF'
#!/usr/bin/env python3
"""Alertmanager Webhook → 企业微信"""
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

WECOM_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"

class AlertHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length))

        for alert in body.get('alerts', []):
            status = "🔴 触发" if alert['status'] == 'firing' else "✅ 恢复"
            msg = {
                "msgtype": "markdown",
                "markdown": {
                    "content": f"## {status} {alert['labels'].get('alertname', 'Unknown')}\n"
                               f"**实例**: {alert['labels'].get('instance', 'N/A')}\n"
                               f"**描述**: {alert['annotations'].get('description', 'N/A')}\n"
                               f"**时间**: {alert.get('startsAt', 'N/A')[:19]}"
                }
            }
            requests.post(WECOM_WEBHOOK, json=msg)

        self.send_response(200)
        self.end_headers()

HTTPServer(('0.0.0.0', 8080), AlertHandler).serve_forever()
PYTHON_EOF
```

---

## 8. 常见故障排查

### 日志空间爆满

```bash
# 1. 查看日志占用
du -sh /var/log/*  | sort -rh | head -10
journalctl --disk-usage

# 2. 紧急清理
journalctl --vacuum-size=500M
find /var/log -name "*.gz" -mtime +30 -delete
truncate -s 0 /var/log/syslog.1   # 清空指定日志

# 3. 检查 logrotate 是否正常
cat /var/lib/logrotate/status
logrotate -d /etc/logrotate.conf   # 调试模式

# 4. 检查 journald 配置
journalctl --verify   # 验证日志完整性
```

### Prometheus 查询慢

```bash
# 1. 检查存储
du -sh /var/lib/prometheus/

# 2. 检查 TSDB 状态
curl -s http://localhost:9090/api/v1/status/tsdb | python3 -m json.tool

# 3. 优化查询
# 避免使用 rate() 在大时间范围上
# 使用 recording rules 预聚合

# 4. 调整保留时间
# --storage.tsdb.retention.time=15d
```

### Node Exporter 指标缺失

```bash
# 1. 检查运行状态
systemctl status node_exporter
curl -s http://localhost:9100/metrics | grep node_cpu

# 2. 检查 collector 是否启用
curl -s http://localhost:9100/metrics | grep "^# HELP" | wc -l

# 3. 启用额外 collector
# ExecStart 添加 --collector.systemd --collector.processes
```
